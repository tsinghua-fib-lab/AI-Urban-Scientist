from __future__ import annotations

import argparse
import html
import json
import re
import sys
from pathlib import Path


OPEN_DATA_SKILLS_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(OPEN_DATA_SKILLS_ROOT))

from open_data_skills.tool_contract import fetch_text_with_live_gate


SOURCE_SKILL_ID = "nyc_tlc"
SOURCE_CARD_ID = "nyc_tlc_trip_records"
REQUIRED_VALIDATION = ["resolver", "probe", "download", "verifier"]
DEFAULT_ENTRYPOINT = "https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page"
SUPPORTED_VEHICLE_TYPES = {"yellow", "green", "fhv", "fhvhv"}


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Emit not-final NYC TLC trip-record resource hints for route discovery."
    )
    parser.add_argument("--vehicle-type", required=True, choices=sorted(SUPPORTED_VEHICLE_TYPES))
    parser.add_argument("--year", required=True)
    parser.add_argument("--month", required=True)
    parser.add_argument("--need-id", required=True)
    parser.add_argument("--html-fixture")
    parser.add_argument("--entrypoint-url", default=DEFAULT_ENTRYPOINT)
    args = parser.parse_args()

    year = _normalize_year(args.year)
    month = _normalize_month(args.month)
    page_text = _load_page_text(args.entrypoint_url, args.html_fixture)
    candidates = find_trip_record_urls(page_text, args.vehicle_type, year, month)

    payload = build_payload(
        vehicle_type=args.vehicle_type,
        year=year,
        month=month,
        need_id=args.need_id,
        entrypoint_url=args.entrypoint_url,
        candidates=candidates,
    )
    print(json.dumps(payload, indent=2, sort_keys=True))


def find_trip_record_urls(page_text: str, vehicle_type: str, year: str, month: str) -> list[str]:
    filename = f"{vehicle_type}_tripdata_{year}-{month}.parquet"
    url_pattern = re.compile(r"https?://[^\s\"'<>]+/" + re.escape(filename), re.IGNORECASE)
    return sorted({html.unescape(match.group(0)) for match in url_pattern.finditer(page_text)})


def build_payload(
    *,
    vehicle_type: str,
    year: str,
    month: str,
    need_id: str,
    entrypoint_url: str,
    candidates: list[str],
) -> dict[str, object]:
    candidate_resources = [
        {
            "url": url,
            "role": "primary",
            "access_method": "direct",
            "need_ids": [need_id],
            "source_skill_id": SOURCE_SKILL_ID,
            "source_card_id": SOURCE_CARD_ID,
            "finality": "not_final",
            "consumer_authority": "none",
            "required_validation": REQUIRED_VALIDATION,
            "executability_hint": "executable_resource",
            "required_params": ["vehicle_type", "year", "month"],
            "missing_params": [],
            "direct_file_pattern": {
                "format": _format_from_trip_url(url),
                "filename": f"{vehicle_type}_tripdata_{year}-{month}.{_format_from_trip_url(url)}",
                "source_family": "nyc_tlc_monthly_trip_records",
            },
            "resolver_hint": {
                "resolver_family": "nyc_tlc_monthly_tripdata",
                "target_executability_hint": "executable_resource",
                "requires_official_entrypoint_match": True,
            },
            "future_probe_hint": {
                "method": "HEAD",
                "expected_status": [200],
                "notes": "Probe the monthly direct file URL before any downstream acquisition.",
            },
            "validation_notes": [
                "Only matched official monthly trip-record links receive executable_resource hints.",
                "Validate file format and schema downstream before any success claim.",
            ],
        }
        for url in candidates
    ]
    route_goal = f"Find NYC TLC {vehicle_type} trip record file leads for {year}-{month}."
    if candidate_resources:
        positive_evidence = [
            {
                "type": "source_prior",
                "message": "NYC TLC official trip-record naming pattern matched.",
                "entrypoint_url": entrypoint_url
            }
        ]
        negative_evidence: list[dict[str, str]] = []
    else:
        positive_evidence = [
            {
                "type": "entrypoint_checked",
                "message": "NYC TLC trip-record entrypoint was searched for the requested file.",
                "entrypoint_url": entrypoint_url
            }
        ]
        negative_evidence = [
            {
                "type": "no_match",
                "message": (
                    "No concrete monthly trip-record file link matched the requested "
                    f"{vehicle_type} {year}-{month} inputs."
                )
            }
        ]
    fragment = {
        "route_id": f"source_skill:{SOURCE_SKILL_ID}:{SOURCE_CARD_ID}",
        "route_type": "source_skill",
        "route_goal": route_goal,
        "source_skill_id": SOURCE_SKILL_ID,
        "source_card_id": SOURCE_CARD_ID,
        "input_need_ids": [need_id],
        "tools_used": [f"source_skill:{SOURCE_SKILL_ID}"],
        "candidate_resources": candidate_resources,
        "positive_evidence": positive_evidence,
        "negative_evidence": negative_evidence,
        "finality": "not_final",
        "consumer_authority": "none"
    }
    fragment["executability_hint"] = (
        "executable_resource" if candidate_resources else "source_landing"
    )
    resource_intents = [
        {
            "need_id": need_id,
            "source_route_id": fragment["route_id"],
            "route_type": "source_skill",
            "resource_url": resource["url"],
            "role": resource["role"],
            "access_method": resource["access_method"],
            "why_sufficient": route_goal,
            "required_validation": REQUIRED_VALIDATION,
            "finality": "not_final",
            "consumer_authority": "none",
            "executability_hint": resource["executability_hint"],
            "required_params": resource["required_params"],
            "missing_params": resource["missing_params"],
            "direct_file_pattern": resource["direct_file_pattern"],
            "resolver_hint": resource["resolver_hint"],
            "future_probe_hint": resource["future_probe_hint"],
            "validation_notes": resource["validation_notes"],
        }
        for resource in candidate_resources
    ]

    return {
        "source_skill_id": SOURCE_SKILL_ID,
        "source_card_id": SOURCE_CARD_ID,
        "finality": "not_final",
        "consumer_authority": "none",
        "query": {
            "vehicle_type": vehicle_type,
            "year": year,
            "month": month,
            "need_id": need_id
        },
        "candidate_resources": candidate_resources,
        "route_dossier_fragment": fragment,
        "resource_intents": resource_intents
    }


def _load_page_text(entrypoint_url: str, fixture_path: str | None) -> str:
    if fixture_path:
        return Path(fixture_path).read_text(encoding="utf-8")
    return fetch_text_with_live_gate(entrypoint_url)


def _normalize_year(value: str) -> str:
    if not re.fullmatch(r"\d{4}", value):
        raise ValueError("--year must be a four digit year")
    return value


def _normalize_month(value: str) -> str:
    if not re.fullmatch(r"\d{1,2}", value):
        raise ValueError("--month must be one or two digits")
    month = int(value)
    if not 1 <= month <= 12:
        raise ValueError("--month must be between 1 and 12")
    return f"{month:02d}"


def _format_from_trip_url(url: str) -> str:
    lowered = str(url or "").lower()
    if lowered.endswith(".parquet"):
        return "parquet"
    if lowered.endswith(".csv"):
        return "csv"
    return "unknown"


if __name__ == "__main__":
    main()
