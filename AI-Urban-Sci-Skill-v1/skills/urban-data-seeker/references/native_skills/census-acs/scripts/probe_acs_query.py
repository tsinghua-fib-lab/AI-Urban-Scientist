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
    fetch_text_with_live_gate,
    policy_allows,
    policy_reason,
    read_json_file,
    validation_check,
)


SOURCE_SKILL_ID = "census_acs"


def main() -> None:
    parser = argparse.ArgumentParser(description="Probe a concrete Census ACS API response shape.")
    parser.add_argument("--policy", default="discovery_only")
    parser.add_argument("--url", default="")
    parser.add_argument("--fixture-response")
    parser.add_argument("--variables", default="")
    parser.add_argument("--geography", default="")
    args = parser.parse_args()
    input_payload = {
        "url": args.url,
        "fixture_response": bool(args.fixture_response),
        "variables": _split_csv(args.variables),
        "geography": args.geography,
    }
    provenance = {
        "source_url": args.url,
        "metadata_url": "https://api.census.gov/data.html",
        "publisher": "U.S. Census Bureau",
    }
    if not policy_allows(args.policy, "probe"):
        print(json.dumps(fail_closed_result(
            source_skill_id=SOURCE_SKILL_ID,
            tool_type="probe",
            policy=args.policy,
            input_payload=input_payload,
            reason=policy_reason(args.policy, "probe"),
            provenance=provenance,
        ), indent=2, sort_keys=True))
        return

    try:
        payload = read_json_file(args.fixture_response) if args.fixture_response else json.loads(fetch_text_with_live_gate(args.url))
        checks = _validate_acs_json(payload, _split_csv(args.variables))
        passed = all(check["passed"] for check in checks)
        result = {
            "status": "probe_requestable" if passed else "needs_follow_up",
            "row_count": max(0, len(payload) - 1) if isinstance(payload, list) else 0,
        }
    except Exception as exc:  # fail closed on malformed fixture or disabled live fetch
        checks = [validation_check("probe_exception", False, reason=type(exc).__name__)]
        result = {"status": "needs_follow_up", "reason": str(exc)}

    print(json.dumps(build_tool_result(
        source_skill_id=SOURCE_SKILL_ID,
        tool_type="probe",
        policy=args.policy,
        input_payload=input_payload,
        result=result,
        provenance=provenance,
        validation={"checks": checks},
    ), indent=2, sort_keys=True))


def _validate_acs_json(payload: object, variables: list[str]) -> list[dict[str, object]]:
    checks: list[dict[str, object]] = []
    is_array = isinstance(payload, list) and bool(payload)
    checks.append(validation_check("json_array_response", is_array))
    header = payload[0] if is_array else []
    has_header = isinstance(header, list)
    checks.append(validation_check("header_row_present", has_header))
    checks.append(validation_check("data_rows_present", isinstance(payload, list) and len(payload) > 1))
    for variable in variables:
        checks.append(validation_check(f"variable_present:{variable}", has_header and variable in header))
    return checks


def _split_csv(value: str) -> list[str]:
    return [item.strip() for item in value.split(",") if item.strip()]


if __name__ == "__main__":
    main()
