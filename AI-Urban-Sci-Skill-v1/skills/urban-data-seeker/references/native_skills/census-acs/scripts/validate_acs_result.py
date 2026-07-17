from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


OPEN_DATA_SKILLS_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(OPEN_DATA_SKILLS_ROOT))

from open_data_skills.tool_contract import (
    build_tool_result,
    fail_closed_result,
    policy_allows,
    policy_reason,
    read_json_file,
    validation_check,
)


SOURCE_SKILL_ID = "census_acs"


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate a Census ACS JSON-array sample.")
    parser.add_argument("--policy", default="discovery_only")
    parser.add_argument("--input-file", required=True)
    parser.add_argument("--variables", default="")
    parser.add_argument("--geography", default="")
    parser.add_argument("--state", default="")
    parser.add_argument("--county", default="")
    parser.add_argument("--tract", default="")
    parser.add_argument("--min-rows", type=int, default=1)
    args = parser.parse_args()
    input_payload = {
        "input_file": args.input_file,
        "variables": _split_csv(args.variables),
        "geography": args.geography,
        "state": args.state,
        "county": args.county,
        "tract": args.tract,
        "min_rows": args.min_rows,
    }
    provenance = {
        "source_url": "",
        "metadata_url": "https://api.census.gov/data.html",
        "publisher": "U.S. Census Bureau",
    }
    if not policy_allows(args.policy, "validate"):
        print(json.dumps(fail_closed_result(
            source_skill_id=SOURCE_SKILL_ID,
            tool_type="validate",
            policy=args.policy,
            input_payload=input_payload,
            reason=policy_reason(args.policy, "validate"),
            provenance=provenance,
        ), indent=2, sort_keys=True))
        return

    try:
        payload = read_json_file(args.input_file)
        checks = _checks(
            payload,
            _split_csv(args.variables),
            geography=args.geography,
            state=args.state,
            county=args.county,
            tract=args.tract,
            min_rows=args.min_rows,
        )
        passed = all(check["passed"] for check in checks)
        result = {"status": "validation_passed" if passed else "validation_failed"}
    except Exception as exc:
        checks = [validation_check("validate_exception", False, reason=type(exc).__name__)]
        result = {"status": "validation_failed", "reason": str(exc)}

    print(json.dumps(build_tool_result(
        source_skill_id=SOURCE_SKILL_ID,
        tool_type="validate",
        policy=args.policy,
        input_payload=input_payload,
        result=result,
        provenance=provenance,
        validation={"checks": checks},
    ), indent=2, sort_keys=True))


def _checks(
    payload: object,
    variables: list[str],
    *,
    geography: str = "",
    state: str = "",
    county: str = "",
    tract: str = "",
    min_rows: int = 1,
) -> list[dict[str, object]]:
    checks: list[dict[str, object]] = []
    is_array = isinstance(payload, list) and bool(payload)
    checks.append(validation_check("json_array_response", is_array))
    header = payload[0] if is_array else []
    has_header = isinstance(header, list)
    checks.append(validation_check("header_row_present", has_header))
    data_rows = payload[1:] if isinstance(payload, list) else []
    checks.append(validation_check("data_rows_present", len(data_rows) > 0))
    checks.append(validation_check("min_rows_met", len(data_rows) >= min_rows, min_rows=min_rows, row_count=len(data_rows)))
    for variable in variables:
        checks.append(validation_check(f"variable_present:{variable}", has_header and variable in header))
        index = header.index(variable) if has_header and variable in header else -1
        checks.append(validation_check(f"variable_numeric:{variable}", index >= 0 and all(_is_number(row[index]) for row in data_rows if isinstance(row, list) and len(row) > index)))
    for column in _geography_columns(geography):
        checks.append(validation_check(f"geography_column_present:{column}", has_header and column in header))
    expected_values = {"state": state, "county": county, "tract": tract}
    for column, expected in expected_values.items():
        if expected and has_header and column in header:
            index = header.index(column)
            checks.append(validation_check(f"geography_value_matches:{column}", all(isinstance(row, list) and len(row) > index and str(row[index]) == expected for row in data_rows)))
    return checks


def _split_csv(value: str) -> list[str]:
    return [item.strip() for item in value.split(",") if item.strip()]


def _geography_columns(geography: str) -> list[str]:
    normalized = geography.strip().lower().replace("_", " ")
    if normalized == "county":
        return ["state", "county"]
    if normalized == "tract":
        return ["state", "county", "tract"]
    if normalized == "block group":
        return ["state", "county", "tract", "block group"]
    return []


def _is_number(value: object) -> bool:
    try:
        float(str(value))
        return True
    except ValueError:
        return False


if __name__ == "__main__":
    main()
