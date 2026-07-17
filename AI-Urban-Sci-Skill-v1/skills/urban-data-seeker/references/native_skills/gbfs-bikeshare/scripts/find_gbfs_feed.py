from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


OPEN_DATA_SKILLS_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(OPEN_DATA_SKILLS_ROOT))

from open_data_skills.lint_contract import assert_lint_clean
from open_data_skills.route_bridge import build_dossier_fragment, build_resource_intents


SOURCE_SKILL_ID = "gbfs_bikeshare"
SOURCE_CARD_ID = "gbfs_bikeshare_feeds"
SYSTEMS_CATALOG = "https://github.com/MobilityData/gbfs/blob/master/systems.csv"


def main() -> None:
    parser = argparse.ArgumentParser(description="Emit not-final GBFS bikeshare source hints.")
    parser.add_argument("--need-id", required=True)
    parser.add_argument("--need-text", required=True)
    parser.add_argument("--system-name", required=True)
    parser.add_argument("--region", required=True)
    parser.add_argument("--feed-url")
    args = parser.parse_args()

    payload = build_payload(
        need_id=args.need_id,
        need_text=args.need_text,
        system_name=args.system_name,
        region=args.region,
        feed_url=args.feed_url,
    )
    print(json.dumps(payload, indent=2, sort_keys=True))


def build_payload(
    *,
    need_id: str,
    need_text: str,
    system_name: str,
    region: str,
    feed_url: str | None,
) -> dict[str, object]:
    resource_url = feed_url or SYSTEMS_CATALOG
    negative_evidence = []
    if not feed_url:
        negative_evidence.append(
            {
                "type": "missing_feed_url",
                "message": "No concrete GBFS discovery URL was supplied; use catalog evidence before selecting a system feed.",
            }
        )
    candidate_resources = [
        {
            "url": resource_url,
            "role": "primary",
            "access_method": "api_or_catalog",
            "need_ids": [need_id],
            "source_skill_id": SOURCE_SKILL_ID,
            "source_card_id": SOURCE_CARD_ID,
            "description": "GBFS discovery or systems catalog lead; system identity, endpoints, freshness, and history suitability still require validation.",
            "publisher": "MobilityData or local bikeshare publisher",
        }
    ]
    fragment = build_dossier_fragment(
        source_skill_id=SOURCE_SKILL_ID,
        source_card_id=SOURCE_CARD_ID,
        need_ids=[need_id],
        route_goal=f"Find GBFS bikeshare source-prior leads for {system_name} in {region}.",
        candidate_resources=candidate_resources,
        positive_evidence=[
            {
                "type": "source_prior",
                "message": "Bikeshare feed need matched GBFS workflow.",
                "system_name": system_name,
                "region": region,
            }
        ],
        negative_evidence=negative_evidence,
    )
    fragment["ambiguities"] = [
        {
            "type": "system_feed_history_ambiguity",
            "message": "GBFS system identity, feed endpoint coverage, freshness, and real-time versus historical suitability require downstream validation.",
        }
    ]
    fragment["verification_notes"] = [
        "Validate GBFS discovery JSON and endpoint URLs.",
        "Validate system identity and region fit.",
        "Check real-time versus historical suitability before retrospective use.",
    ]
    resource_intents = build_resource_intents(fragment)
    payload = {
        "source_skill_id": SOURCE_SKILL_ID,
        "source_card_id": SOURCE_CARD_ID,
        "finality": "not_final",
        "consumer_authority": "none",
        "query": {
            "need_id": need_id,
            "need_text": need_text,
            "system_name": system_name,
            "region": region,
            "feed_url_supplied": bool(feed_url),
        },
        "candidate_resources": fragment["candidate_resources"],
        "route_dossier_fragment": fragment,
        "resource_intents": resource_intents,
    }
    assert_lint_clean(payload)
    return payload


if __name__ == "__main__":
    main()
