from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


OPEN_DATA_SKILLS_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(OPEN_DATA_SKILLS_ROOT))

from open_data_skills.route_bridge import build_dossier_fragment, build_resource_intents


SOURCE_SKILL_ID = "noaa_weather"
SOURCE_CARD_ID = "noaa_climate_weather"
DEFAULT_ENTRYPOINT = "https://www.ncei.noaa.gov/cdo-web/search"
NOAA_DATA_API = "https://www.ncdc.noaa.gov/cdo-web/api/v2/data"
REQUIRED_PARAMS = ["dataset", "station", "start_date", "end_date", "variables"]


def main() -> None:
    parser = argparse.ArgumentParser(description="Emit not-final NOAA weather source hints.")
    parser.add_argument("--need-id", required=True)
    parser.add_argument("--need-text", required=True)
    parser.add_argument("--dataset", default="")
    parser.add_argument("--station")
    parser.add_argument("--variables")
    parser.add_argument("--start-date")
    parser.add_argument("--end-date")
    parser.add_argument("--entrypoint-url", default=DEFAULT_ENTRYPOINT)
    args = parser.parse_args()

    payload = build_payload(
        need_id=args.need_id,
        need_text=args.need_text,
        dataset=args.dataset,
        station=args.station,
        variables=args.variables,
        start_date=args.start_date,
        end_date=args.end_date,
        entrypoint_url=args.entrypoint_url,
    )
    print(json.dumps(payload, indent=2, sort_keys=True))


def build_payload(
    *,
    need_id: str,
    need_text: str,
    dataset: str,
    station: str | None,
    variables: str | None,
    start_date: str | None,
    end_date: str | None,
    entrypoint_url: str,
) -> dict[str, object]:
    variable_list = _split_csv(variables)
    missing_params = _missing_params(
        {
            "dataset": dataset,
            "station": station,
            "start_date": start_date,
            "end_date": end_date,
            "variables": variable_list,
        }
    )
    executability_hint = "resolvable_resource" if not missing_params else "source_landing"
    candidate_resources = [
        {
            "url": NOAA_DATA_API if not missing_params else entrypoint_url,
            "role": "primary",
            "access_method": "api_or_search",
            "need_ids": [need_id],
            "source_skill_id": SOURCE_SKILL_ID,
            "source_card_id": SOURCE_CARD_ID,
            "description": "NOAA/NCEI search or API entrypoint; requested station, time range, and variables still require validation.",
            "executability_hint": executability_hint,
            "required_params": list(REQUIRED_PARAMS),
            "missing_params": missing_params,
            "resolver_hint": {
                "resolver_family": "noaa_data_service",
                "target_executability_hint": "resolvable_resource",
                "not_executable_until_params_complete": True,
            },
            "api_query_template": {
                "url": NOAA_DATA_API,
                "headers": {
                    "token": "{NOAA_CDO_TOKEN}"
                },
                "query_params": {
                    "datasetid": "{dataset}",
                    "stationid": "{station}",
                    "startdate": "{start_date}",
                    "enddate": "{end_date}",
                    "datatypeid": "{variables}",
                    "limit": "1000",
                },
            },
            "future_probe_hint": {
                "method": "GET_LIGHT",
                "expected_status": [200],
                "notes": "Probe only after dataset, station, dates, variables, and NOAA CDO token availability are complete.",
            },
            "validation_notes": [
                "Validate station identity and geographic fit.",
                "Validate requested variables and date coverage.",
                "Use the NOAA CDO token header for CDO API probes; do not put the token in route dossiers or final reports.",
                "Do not treat the NOAA API root or search page as an executable resource when parameters are missing.",
            ],
        }
    ]
    route_goal = f"Find NOAA {dataset} weather source leads."
    fragment = build_dossier_fragment(
        source_skill_id=SOURCE_SKILL_ID,
        source_card_id=SOURCE_CARD_ID,
        need_ids=[need_id],
        route_goal=route_goal,
        candidate_resources=candidate_resources,
        positive_evidence=[
            {
                "type": "source_prior",
                "message": "Weather, precipitation, temperature, station, or NOAA need matched NOAA workflow.",
                "dataset": dataset,
            }
        ],
        negative_evidence=[],
    )
    fragment["ambiguities"] = [
        {
            "type": "station_time_variable_ambiguity",
            "message": "NOAA station/time/variable ambiguity remains until station identity, requested dates, and variables are validated.",
        }
    ]
    fragment["verification_notes"] = [
        "Validate station identity and geographic fit.",
        "Validate requested variables and date coverage.",
        "Treat API/search access, token, and rate-limit issues as downstream access evidence.",
    ]
    fragment["executability_hint"] = executability_hint
    resource_intents = build_resource_intents(fragment)

    return {
        "source_skill_id": SOURCE_SKILL_ID,
        "source_card_id": SOURCE_CARD_ID,
        "finality": "not_final",
        "consumer_authority": "none",
        "query": {
            "need_id": need_id,
            "need_text": need_text,
            "dataset": dataset,
            "station": station,
            "variables": variable_list,
            "start_date": start_date,
            "end_date": end_date,
            "missing_params": missing_params,
        },
        "candidate_resources": fragment["candidate_resources"],
        "route_dossier_fragment": fragment,
        "resource_intents": resource_intents,
    }


def _split_csv(value: str | None) -> list[str]:
    if not value:
        return []
    return [item.strip() for item in value.split(",") if item.strip()]


def _missing_params(values: dict[str, object]) -> list[str]:
    missing: list[str] = []
    for key in REQUIRED_PARAMS:
        value = values.get(key)
        if value in (None, "", []):
            missing.append(key)
    return missing


if __name__ == "__main__":
    main()
