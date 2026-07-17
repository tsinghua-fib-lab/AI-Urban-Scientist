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
    fetch_mode,
    fetch_text_with_live_gate,
    policy_allows,
    policy_reason,
    read_json_file,
    validation_check,
    write_json_fetch_artifact,
)


SOURCE_SKILL_ID = "census_acs"


def main() -> None:
    parser = argparse.ArgumentParser(description="Fetch a capped Census ACS table sample.")
    parser.add_argument("--policy", default="discovery_only")
    parser.add_argument("--url", default="")
    parser.add_argument("--fixture-response")
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--max-rows", type=int, default=100)
    args = parser.parse_args()
    input_payload = {
        "url": args.url,
        "fixture_response": bool(args.fixture_response),
        "max_rows": args.max_rows,
        "download_mode": fetch_mode(args.policy),
    }
    provenance = {
        "source_url": args.url,
        "metadata_url": "https://api.census.gov/data.html",
        "publisher": "U.S. Census Bureau",
    }
    if not policy_allows(args.policy, "fetch"):
        print(json.dumps(fail_closed_result(
            source_skill_id=SOURCE_SKILL_ID,
            tool_type="fetch",
            policy=args.policy,
            input_payload=input_payload,
            reason=policy_reason(args.policy, "fetch"),
            provenance=provenance,
        ), indent=2, sort_keys=True))
        return

    try:
        payload = read_json_file(args.fixture_response) if args.fixture_response else json.loads(fetch_text_with_live_gate(args.url))
        if not isinstance(payload, list) or not payload:
            raise ValueError("acs_response_not_json_array")
        sample = payload if fetch_mode(args.policy) == "full" else [payload[0], *payload[1 : args.max_rows + 1]]
        artifact = write_json_fetch_artifact(Path(args.output_dir) / "acs_table_sample.json", sample, policy=args.policy)
        checks = [
            validation_check("json_array_response", True),
            validation_check("fetch_scope", fetch_mode(args.policy) == "full" or len(sample) <= args.max_rows + 1, download_mode=fetch_mode(args.policy), max_rows=args.max_rows),
        ]
        result = {"status": "fetched", "row_count": max(0, len(sample) - 1)}
        artifacts = [artifact]
    except Exception as exc:
        checks = [validation_check("fetch_exception", False, reason=type(exc).__name__)]
        result = {"status": "needs_follow_up", "reason": str(exc)}
        artifacts = []

    print(json.dumps(build_tool_result(
        source_skill_id=SOURCE_SKILL_ID,
        tool_type="fetch",
        policy=args.policy,
        input_payload=input_payload,
        result=result,
        provenance=provenance,
        artifacts=artifacts,
        validation={"checks": checks},
    ), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
