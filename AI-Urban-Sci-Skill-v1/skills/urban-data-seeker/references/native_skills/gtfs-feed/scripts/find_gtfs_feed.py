from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from urllib.parse import urlparse


OPEN_DATA_SKILLS_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(OPEN_DATA_SKILLS_ROOT))

from open_data_skills.route_bridge import build_dossier_fragment, build_resource_intents


SOURCE_SKILL_ID = "gtfs_feed"
SOURCE_CARD_ID = "public_transit_gtfs_feeds"


def main() -> None:
    parser = argparse.ArgumentParser(description="Emit not-final GTFS feed hints.")
    parser.add_argument("--need-id", required=True)
    parser.add_argument("--need-text", required=True)
    parser.add_argument("--feed-name", required=True)
    parser.add_argument("--feed-url")
    args = parser.parse_args()

    payload = build_payload(
        need_id=args.need_id,
        need_text=args.need_text,
        feed_name=args.feed_name,
        feed_url=args.feed_url,
    )
    print(json.dumps(payload, indent=2, sort_keys=True))


def build_payload(*, need_id: str, need_text: str, feed_name: str, feed_url: str | None) -> dict[str, object]:
    candidate_resources = []
    positive_evidence = [
        {
            "type": "source_prior",
            "message": "Transit schedule need matched GTFS feed workflow.",
            "feed_name": feed_name,
        }
    ]
    negative_evidence = []
    if feed_url:
        is_zip_endpoint = _looks_like_gtfs_zip(feed_url)
        executability_hint = "executable_resource" if is_zip_endpoint else "source_landing"
        resource = {
            "url": feed_url,
            "role": "primary",
            "access_method": "direct" if is_zip_endpoint else "agency_landing",
            "need_ids": [need_id],
            "source_skill_id": SOURCE_SKILL_ID,
            "source_card_id": SOURCE_CARD_ID,
            "description": (
                "Candidate GTFS static feed zip URL; content still requires GTFS zip validation."
                if is_zip_endpoint
                else "Candidate agency or developer landing page; resolve to a concrete GTFS zip before download."
            ),
            "executability_hint": executability_hint,
            "required_params": ["feed_name", "feed_url"],
            "missing_params": [],
            "resolver_hint": {
                "resolver_family": "gtfs_static_feed",
                "target_executability_hint": "executable_resource",
                "expected_content": "GTFS static feed zip",
            },
            "future_probe_hint": {
                "method": "HEAD" if is_zip_endpoint else "GET_LIGHT",
                "expected_content_type": "application/zip" if is_zip_endpoint else "text/html",
                "notes": (
                    "Probe zip endpoint before any downstream acquisition."
                    if is_zip_endpoint
                    else "Inspect landing page for current GTFS zip links before any downstream acquisition."
                ),
            },
            "validation_notes": [
                "Future verifier must inspect GTFS zip contents for stops.txt/routes.txt/trips.txt.",
                "Agency landing pages are source_landing hints, not feed zip resources.",
            ],
        }
        if is_zip_endpoint:
            resource["direct_file_pattern"] = {
                "format": "gtfs_zip",
                "filename_glob": "*.zip",
                "required_members": ["stops.txt", "routes.txt", "trips.txt"],
            }
        candidate_resources.append(
            resource
        )
    else:
        negative_evidence.append(
            {
                "type": "missing_feed_url",
                "message": "No concrete GTFS feed URL was supplied; do not guess a feed URL.",
            }
        )

    route_goal = f"Find GTFS feed leads for {feed_name}."
    fragment = build_dossier_fragment(
        source_skill_id=SOURCE_SKILL_ID,
        source_card_id=SOURCE_CARD_ID,
        need_ids=[need_id],
        route_goal=route_goal,
        candidate_resources=candidate_resources,
        positive_evidence=positive_evidence,
        negative_evidence=negative_evidence,
    )
    fragment["ambiguities"] = [
        {
            "type": "gtfs_zip_validation_required",
            "message": "GTFS zip future validation requires stops.txt/routes.txt/trips.txt before success can be claimed.",
        },
        {
            "type": "agency_feed_freshness_ambiguity",
            "message": "Agency/feed identity and service-date freshness must be checked downstream.",
        },
    ]
    fragment["verification_notes"] = [
        "Probe URL availability before download.",
        "Future verifier must inspect GTFS zip contents for stops.txt/routes.txt/trips.txt.",
        "Do not treat this hint as an approval, planning artifact, or completed acquisition.",
    ]
    fragment["executability_hint"] = (
        candidate_resources[0]["executability_hint"] if candidate_resources else "source_landing"
    )
    resource_intents = build_resource_intents(fragment)

    return {
        "source_skill_id": SOURCE_SKILL_ID,
        "source_card_id": SOURCE_CARD_ID,
        "finality": "not_final",
        "consumer_authority": "none",
        "query": {
            "need_id": need_id,
            "need_text": need_text,
            "feed_name": feed_name,
        },
        "candidate_resources": fragment["candidate_resources"],
        "route_dossier_fragment": fragment,
        "resource_intents": resource_intents,
    }


def _looks_like_gtfs_zip(url: str) -> bool:
    parsed = urlparse(str(url or ""))
    return parsed.scheme in {"http", "https"} and parsed.path.lower().endswith(".zip")


if __name__ == "__main__":
    main()
