from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from urllib.parse import urlencode


OPEN_DATA_SKILLS_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(OPEN_DATA_SKILLS_ROOT))

from open_data_skills.lint_contract import assert_lint_clean
from open_data_skills.route_bridge import build_dossier_fragment, build_resource_intents


SOURCE_SKILL_ID = "world_bank_indicators"
SOURCE_CARD_ID = "world_bank_indicators_api"
LANDING_URL = "https://data.worldbank.org/indicator"


def main() -> None:
    parser = argparse.ArgumentParser(description="Emit not-final World Bank indicator source hints.")
    parser.add_argument("--need-id", required=True)
    parser.add_argument("--need-text", required=True)
    parser.add_argument("--country", default="")
    parser.add_argument("--indicator", default="")
    parser.add_argument("--start-year", default="")
    parser.add_argument("--end-year", default="")
    args = parser.parse_args()
    payload = build_payload(
        need_id=args.need_id,
        need_text=args.need_text,
        country=args.country,
        indicator=args.indicator,
        start_year=args.start_year,
        end_year=args.end_year,
    )
    print(json.dumps(payload, indent=2, sort_keys=True))


def build_payload(*, need_id: str, need_text: str, country: str, indicator: str, start_year: str, end_year: str) -> dict[str, object]:
    missing = [name for name, value in {"country": country, "indicator": indicator}.items() if not value]
    url = build_api_url(country, indicator, start_year, end_year) if not missing else LANDING_URL
    resource = {
        "url": url,
        "role": "primary",
        "access_method": "world_bank_indicator_api" if not missing else "source_landing",
        "need_ids": [need_id],
        "source_skill_id": SOURCE_SKILL_ID,
        "source_card_id": SOURCE_CARD_ID,
        "description": "World Bank indicator API lead; indicator metadata, units, paging, and coverage require validation.",
        "publisher": "World Bank",
        "executability_hint": "resolvable_resource" if not missing else "source_landing",
        "required_params": ["country", "indicator"],
        "missing_params": missing,
        "resolver_hint": {
            "resolver_family": "world_bank_indicator",
            "country": country,
            "indicator": indicator,
            "start_year": start_year,
            "end_year": end_year,
            "date_range_status": "closed" if start_year and end_year else "open_or_missing",
        },
        "api_query_template": {
            "url": "https://api.worldbank.org/v2/country/{country}/indicator/{indicator}",
            "query_params": {"format": "json", "date": "{start_year}:{end_year}", "per_page": "{per_page}"},
        },
        "future_probe_hint": {"method": "GET_LIGHT", "expected_status": [200], "notes": "Probe metadata and a small page before acquisition."},
        "validation_notes": [
            "Validate indicator definition, country code, date coverage, units, and paging.",
            "Only closed start/end year ranges are encoded as World Bank date parameters.",
        ],
    }
    negative = [{"type": "missing_params", "missing_params": missing}] if missing else []
    fragment = build_dossier_fragment(
        source_skill_id=SOURCE_SKILL_ID,
        source_card_id=SOURCE_CARD_ID,
        need_ids=[need_id],
        route_goal=f"Find World Bank indicator hints for: {need_text}",
        candidate_resources=[resource],
        positive_evidence=[{"type": "source_prior", "message": "Need matched World Bank country indicator workflow."}],
        negative_evidence=negative,
    )
    fragment["ambiguities"] = [{"type": "indicator_country_time_ambiguity", "message": "Indicator code, country code, and time coverage require validation."}]
    fragment["verification_notes"] = resource["validation_notes"]
    payload = {"source_skill_id": SOURCE_SKILL_ID, "source_card_id": SOURCE_CARD_ID, "finality": "not_final", "consumer_authority": "none", "query": {"need_id": need_id, "need_text": need_text, "country": country, "indicator": indicator, "start_year": start_year, "end_year": end_year}, "candidate_resources": fragment["candidate_resources"], "route_dossier_fragment": fragment, "resource_intents": build_resource_intents(fragment)}
    assert_lint_clean(payload)
    return payload


def build_api_url(country: str, indicator: str, start_year: str, end_year: str) -> str:
    params = {"format": "json", "per_page": "1000"}
    if start_year and end_year:
        params["date"] = f"{start_year}:{end_year}"
    return f"https://api.worldbank.org/v2/country/{country}/indicator/{indicator}?" + urlencode(params)


if __name__ == "__main__":
    main()
