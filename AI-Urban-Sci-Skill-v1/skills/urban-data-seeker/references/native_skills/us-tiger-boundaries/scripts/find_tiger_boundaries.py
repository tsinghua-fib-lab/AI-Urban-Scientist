from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


OPEN_DATA_SKILLS_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(OPEN_DATA_SKILLS_ROOT))

from open_data_skills.lint_contract import assert_lint_clean
from open_data_skills.route_bridge import build_dossier_fragment, build_resource_intents


SOURCE_SKILL_ID = "us_tiger_boundaries"
SOURCE_CARD_ID = "us_tiger_boundaries"
DEFAULT_ENTRYPOINT = "https://www.census.gov/geographies/mapping-files/time-series/geo/tiger-line-file.html"


def main() -> None:
    parser = argparse.ArgumentParser(description="Emit not-final Census TIGER boundary source hints.")
    parser.add_argument("--need-id", required=True)
    parser.add_argument("--need-text", required=True)
    parser.add_argument("--vintage", required=True)
    parser.add_argument("--geography", required=True)
    parser.add_argument("--state")
    parser.add_argument("--entrypoint-url", default=DEFAULT_ENTRYPOINT)
    args = parser.parse_args()

    payload = build_payload(
        need_id=args.need_id,
        need_text=args.need_text,
        vintage=args.vintage,
        geography=args.geography,
        state=args.state,
        entrypoint_url=args.entrypoint_url,
    )
    print(json.dumps(payload, indent=2, sort_keys=True))


def build_payload(
    *,
    need_id: str,
    need_text: str,
    vintage: str,
    geography: str,
    state: str | None,
    entrypoint_url: str,
) -> dict[str, object]:
    candidate_resources = [
        {
            "url": entrypoint_url,
            "role": "primary",
            "access_method": "landing_page",
            "need_ids": [need_id],
            "source_skill_id": SOURCE_SKILL_ID,
            "source_card_id": SOURCE_CARD_ID,
            "description": "Census TIGER/Line entrypoint; concrete ZIP path, geometry type, scope, and join keys still require validation.",
            "publisher": "U.S. Census Bureau",
        }
    ]
    fragment = build_dossier_fragment(
        source_skill_id=SOURCE_SKILL_ID,
        source_card_id=SOURCE_CARD_ID,
        need_ids=[need_id],
        route_goal=f"Find Census TIGER boundary source-prior leads for {vintage} {geography}.",
        candidate_resources=candidate_resources,
        positive_evidence=[
            {
                "type": "source_prior",
                "message": "Official boundary geometry need matched Census TIGER workflow.",
                "vintage": vintage,
                "geography": geography,
                "state": state,
            }
        ],
        negative_evidence=[],
    )
    fragment["ambiguities"] = [
        {
            "type": "vintage_geography_boundary_ambiguity",
            "message": "TIGER vintage/geography/boundary ambiguity remains until state scope, file availability, geometry type, CRS, and join keys are validated.",
        }
    ]
    fragment["verification_notes"] = [
        "Validate vintage, geography level, and state or national scope.",
        "Probe concrete ZIP paths before use.",
        "Validate geometry type, CRS, and GEOID/join-key fields.",
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
            "vintage": vintage,
            "geography": geography,
            "state": state,
        },
        "candidate_resources": fragment["candidate_resources"],
        "route_dossier_fragment": fragment,
        "resource_intents": resource_intents,
    }
    assert_lint_clean(payload)
    return payload


if __name__ == "__main__":
    main()
