from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


OPEN_DATA_SKILLS_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(OPEN_DATA_SKILLS_ROOT))

from open_data_skills.tool_contract import build_tool_result, fail_closed_result, fetch_file_artifact, fetch_mode, policy_allows, policy_reason, validation_check


SOURCE_SKILL_ID = "nyc_tlc"


def main() -> None:
    parser = argparse.ArgumentParser(description="Fetch a capped NYC TLC trip-record sample.")
    parser.add_argument("--policy", default="discovery_only")
    parser.add_argument("--fixture-file")
    parser.add_argument("--url", default="")
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--max-bytes", type=int, default=1_000_000)
    args = parser.parse_args()
    input_payload = {"fixture_file": bool(args.fixture_file), "url": args.url, "max_bytes": args.max_bytes, "download_mode": fetch_mode(args.policy)}
    provenance = {"source_url": args.url, "metadata_url": "https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page", "publisher": "New York City Taxi and Limousine Commission"}
    if not policy_allows(args.policy, "fetch"):
        print(json.dumps(fail_closed_result(source_skill_id=SOURCE_SKILL_ID, tool_type="fetch", policy=args.policy, input_payload=input_payload, reason=policy_reason(args.policy, "fetch"), provenance=provenance), indent=2, sort_keys=True))
        return
    try:
        target = Path(args.output_dir) / "nyc_tlc_trip_record_sample.parquet"
        artifact = fetch_file_artifact(
            fixture_file=args.fixture_file,
            url=args.url,
            target=target,
            policy=args.policy,
            max_bytes=args.max_bytes,
            artifact_format="parquet",
        )
        checks = [
            validation_check("sample_written", True),
            validation_check(
                "fetch_scope",
                fetch_mode(args.policy) == "full" or target.stat().st_size <= args.max_bytes,
                download_mode=fetch_mode(args.policy),
                max_bytes=args.max_bytes,
            ),
        ]
        result = {"status": "fetched", "size_bytes": target.stat().st_size}
        artifacts = [artifact]
    except Exception as exc:
        checks = [validation_check("fetch_exception", False, reason=type(exc).__name__)]
        result = {"status": "needs_follow_up", "reason": str(exc)}
        artifacts = []
    print(json.dumps(build_tool_result(source_skill_id=SOURCE_SKILL_ID, tool_type="fetch", policy=args.policy, input_payload=input_payload, result=result, provenance=provenance, artifacts=artifacts, validation={"checks": checks}), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
