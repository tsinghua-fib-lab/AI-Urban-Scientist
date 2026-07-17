from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


OPEN_DATA_SKILLS_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(OPEN_DATA_SKILLS_ROOT))

from open_data_skills.lint_contract import assert_lint_clean
from open_data_skills.route_bridge import build_dossier_fragment, build_resource_intents


SOURCE_SKILL_ID = "open_aq"
SOURCE_CARD_ID = "open_aq"
ENTRYPOINT_URL = "https://api.openaq.org/v3/measurements"
REQUIRED_PARAMS = ["pollutant", "location", "start_date", "end_date"]


def main() -> None:
    parser = argparse.ArgumentParser(description="Emit not-final OpenAQ source hints.")
    parser.add_argument("--need-id", required=True)
    parser.add_argument("--need-text", required=True)
    parser.add_argument("--pollutant", default="")
    parser.add_argument("--location", default="")
    parser.add_argument("--start-date", default="")
    parser.add_argument("--end-date", default="")
    args = parser.parse_args()

    payload = build_payload(
        need_id=args.need_id,
        need_text=args.need_text,
        pollutant=args.pollutant,
        location=args.location,
        start_date=args.start_date,
        end_date=args.end_date,
    )
    print(json.dumps(payload, indent=2, sort_keys=True))


def build_payload(
    *,
    need_id: str,
    need_text: str,
    pollutant: str,
    location: str,
    start_date: str,
    end_date: str,
) -> dict[str, object]:
    missing_params = _missing_params(
        {
            "pollutant": pollutant,
            "location": location,
            "start_date": start_date,
            "end_date": end_date,
        }
    )
    executability_hint = "resolvable_resource" if not missing_params else "source_landing"
    resource = {
        "url": ENTRYPOINT_URL,
        "role": "primary",
        "access_method": "api_or_direct",
        "need_ids": [need_id],
        "source_skill_id": SOURCE_SKILL_ID,
        "source_card_id": SOURCE_CARD_ID,
        "description": "OpenAQ measurements API entrypoint with pollutant, location, and date parameters requiring downstream validation.",
        "publisher": "OpenAQ",
        "executability_hint": executability_hint,
        "required_params": list(REQUIRED_PARAMS),
        "missing_params": missing_params,
        "resolver_hint": {
            "resolver_family": "open_aq_api",
            "target_executability_hint": "resolvable_resource",
            "requires_location_resolution": True,
        },
        "api_query_template": {
            "url": ENTRYPOINT_URL,
            "query_params": {
                "parameters": "{pollutant}",
                "locations": "{location}",
                "date_from": "{start_date}",
                "date_to": "{end_date}",
            },
        },
        "future_probe_hint": {
            "method": "GET_LIGHT",
            "expected_status": [200],
            "notes": "Probe a small measurements request after resolving location and pollutant identifiers.",
        },
        "validation_notes": [
            "Validate pollutant names and units against OpenAQ metadata.",
            "Validate location identity, provider coverage, timestamps, and paging.",
        ],
    }
    fragment = build_dossier_fragment(
        source_skill_id=SOURCE_SKILL_ID,
        source_card_id=SOURCE_CARD_ID,
        need_ids=[need_id],
        route_goal=f"Find OpenAQ pollutant measurements for {location or 'an unresolved location'}.",
        candidate_resources=[resource],
        positive_evidence=[
            {
                "type": "source_prior",
                "message": "Air-quality measurement need matched OpenAQ API workflow.",
                "pollutant": pollutant,
                "location": location,
            }
        ],
        negative_evidence=[],
    )
    fragment["ambiguities"] = [
        {
            "type": "pollutant_location_time_ambiguity",
            "message": "OpenAQ pollutant, location, provider, and time-window ambiguity remains until resolved and probed.",
        }
    ]
    fragment["verification_notes"] = [
        "Resolve location and pollutant identifiers before route approval.",
        "Validate paging, units, coordinates, provider metadata, and timestamps.",
    ]
    fragment["executability_hint"] = executability_hint
    payload = {
        "source_skill_id": SOURCE_SKILL_ID,
        "source_card_id": SOURCE_CARD_ID,
        "finality": "not_final",
        "consumer_authority": "none",
        "query": {
            "need_id": need_id,
            "need_text": need_text,
            "pollutant": pollutant,
            "location": location,
            "start_date": start_date,
            "end_date": end_date,
            "missing_params": missing_params,
        },
        "candidate_resources": fragment["candidate_resources"],
        "route_dossier_fragment": fragment,
        "resource_intents": build_resource_intents(fragment),
    }
    assert_lint_clean(payload)
    return payload


def _missing_params(values: dict[str, object]) -> list[str]:
    return [key for key in REQUIRED_PARAMS if values.get(key) in (None, "", [])]


if __name__ == "__main__":
    main()
