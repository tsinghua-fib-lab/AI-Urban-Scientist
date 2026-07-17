from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


OPEN_DATA_SKILLS_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(OPEN_DATA_SKILLS_ROOT))

from open_data_skills.tool_contract import build_tool_result, fail_closed_result, fetch_bytes_with_live_gate, policy_allows, policy_reason, validation_check


SOURCE_SKILL_ID = "nyc_tlc"


def main() -> None:
    parser = argparse.ArgumentParser(description="Probe a NYC TLC monthly trip-record file sample.")
    parser.add_argument("--policy", default="discovery_only")
    parser.add_argument("--fixture-file")
    parser.add_argument("--url", default="")
    parser.add_argument("--vehicle-type", default="")
    parser.add_argument("--year", default="")
    parser.add_argument("--month", default="")
    args = parser.parse_args()
    input_payload = {"fixture_file": bool(args.fixture_file), "url": args.url, "vehicle_type": args.vehicle_type, "year": args.year, "month": args.month}
    provenance = {"source_url": args.url, "metadata_url": "https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page", "publisher": "New York City Taxi and Limousine Commission"}
    if not policy_allows(args.policy, "probe"):
        print(json.dumps(fail_closed_result(source_skill_id=SOURCE_SKILL_ID, tool_type="probe", policy=args.policy, input_payload=input_payload, reason=policy_reason(args.policy, "probe"), provenance=provenance), indent=2, sort_keys=True))
        return
    try:
        prefix = Path(args.fixture_file).read_bytes()[:4] if args.fixture_file else fetch_bytes_with_live_gate(args.url, max_bytes=4)
        filename = Path(args.fixture_file or args.url).name
        checks = [
            validation_check("parquet_magic_prefix", prefix == b"PAR1"),
            validation_check("filename_vehicle_year_month", _expected_stem(args.vehicle_type, args.year, args.month) in filename),
        ]
        passed = all(check["passed"] for check in checks)
        result = {"status": "probe_requestable" if passed else "needs_follow_up"}
    except Exception as exc:
        checks = [validation_check("probe_exception", False, reason=type(exc).__name__)]
        result = {"status": "needs_follow_up", "reason": str(exc)}
    print(json.dumps(build_tool_result(source_skill_id=SOURCE_SKILL_ID, tool_type="probe", policy=args.policy, input_payload=input_payload, result=result, provenance=provenance, validation={"checks": checks}), indent=2, sort_keys=True))


def _expected_stem(vehicle_type: str, year: str, month: str) -> str:
    return f"{vehicle_type}_tripdata_{year}-{int(month):02d}" if vehicle_type and year and month else ""


if __name__ == "__main__":
    main()
