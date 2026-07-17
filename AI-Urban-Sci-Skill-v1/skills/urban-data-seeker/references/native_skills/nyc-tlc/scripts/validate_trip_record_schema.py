from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


OPEN_DATA_SKILLS_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(OPEN_DATA_SKILLS_ROOT))

from open_data_skills.tool_contract import build_tool_result, fail_closed_result, policy_allows, policy_reason, validation_check


SOURCE_SKILL_ID = "nyc_tlc"
CORE_COLUMNS = {
    "yellow": {"tpep_pickup_datetime", "tpep_dropoff_datetime", "PULocationID", "DOLocationID", "fare_amount", "trip_distance"},
    "green": {"lpep_pickup_datetime", "lpep_dropoff_datetime", "PULocationID", "DOLocationID", "fare_amount", "trip_distance"},
    "fhv": {"pickup_datetime", "dropOff_datetime", "PUlocationID", "DOlocationID"},
    "fhvhv": {"pickup_datetime", "dropoff_datetime", "PULocationID", "DOLocationID"},
}


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate basic NYC TLC trip-record parquet identity.")
    parser.add_argument("--policy", default="discovery_only")
    parser.add_argument("--input-file", required=True)
    parser.add_argument("--vehicle-type", default="")
    parser.add_argument("--year", default="")
    parser.add_argument("--month", default="")
    parser.add_argument("--schema-fixture")
    args = parser.parse_args()
    input_payload = {"input_file": args.input_file, "vehicle_type": args.vehicle_type, "year": args.year, "month": args.month, "schema_fixture": bool(args.schema_fixture)}
    provenance = {"source_url": "", "metadata_url": "https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page", "publisher": "New York City Taxi and Limousine Commission"}
    if not policy_allows(args.policy, "validate"):
        print(json.dumps(fail_closed_result(source_skill_id=SOURCE_SKILL_ID, tool_type="validate", policy=args.policy, input_payload=input_payload, reason=policy_reason(args.policy, "validate"), provenance=provenance), indent=2, sort_keys=True))
        return
    try:
        path = Path(args.input_file)
        data = path.read_bytes()
        expected = f"{args.vehicle_type}_tripdata_{args.year}-{int(args.month):02d}" if args.vehicle_type and args.year and args.month else ""
        checks = [
            validation_check("parquet_magic_prefix", data[:4] == b"PAR1"),
            validation_check("parquet_magic_suffix", len(data) >= 8 and data[-4:] == b"PAR1"),
            validation_check("filename_vehicle_year_month", expected in path.name),
        ]
        columns, schema_source = _schema_columns(path, args.schema_fixture)
        checks.append(validation_check("schema_readable", bool(columns), source=schema_source))
        if columns:
            required = CORE_COLUMNS.get(args.vehicle_type, set())
            missing = sorted(required - set(columns))
            checks.append(validation_check("core_schema_columns_present", not missing, missing_columns=missing))
        else:
            checks.append(validation_check("core_schema_columns_present", False, missing_columns=sorted(CORE_COLUMNS.get(args.vehicle_type, set()))))
        result = {"status": "validation_passed" if all(check["passed"] for check in checks) else "validation_failed"}
    except Exception as exc:
        checks = [validation_check("validate_exception", False, reason=type(exc).__name__)]
        result = {"status": "validation_failed", "reason": str(exc)}
    print(json.dumps(build_tool_result(source_skill_id=SOURCE_SKILL_ID, tool_type="validate", policy=args.policy, input_payload=input_payload, result=result, provenance=provenance, validation={"checks": checks}), indent=2, sort_keys=True))


def _schema_columns(path: Path, fixture_path: str | None) -> tuple[list[str], str]:
    if fixture_path:
        payload = json.loads(Path(fixture_path).read_text(encoding="utf-8"))
        columns = payload.get("columns", []) if isinstance(payload, dict) else []
        return [str(column) for column in columns], "fixture"
    try:
        import pyarrow.parquet as pq  # type: ignore

        schema = pq.read_schema(path)
        return list(schema.names), "pyarrow"
    except Exception:
        return [], "unavailable"


if __name__ == "__main__":
    main()
