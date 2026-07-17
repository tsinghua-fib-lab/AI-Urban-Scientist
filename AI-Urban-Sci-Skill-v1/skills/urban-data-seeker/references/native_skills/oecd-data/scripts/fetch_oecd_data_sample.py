from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


OPEN_DATA_SKILLS_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(OPEN_DATA_SKILLS_ROOT))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from open_data_skills.tool_contract import build_tool_result, fail_closed_result, fetch_bytes_with_live_gate, fetch_file_artifact, fetch_mode, policy_allows, policy_reason
from probe_oecd_data_api import inspect_oecd_metadata


SOURCE_SKILL_ID = "oecd_data"
PUBLISHER = "OECD"
METADATA_URL = "https://www.oecd.org/en/data/insights/data-explainers/2024/09/api.html"
USED_PLATFORM_TOOLS = ["sdmx_platform"]


def main() -> None:
    parser = argparse.ArgumentParser(description="Fetch a capped OECD SDMX metadata sample.")
    parser.add_argument("--policy", default="discovery_only")
    parser.add_argument("--fixture-file")
    parser.add_argument("--url", default="")
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--max-bytes", type=int, default=1_000_000)
    args = parser.parse_args()
    input_payload = {"fixture_file": bool(args.fixture_file), "url": args.url, "max_bytes": args.max_bytes, "download_mode": fetch_mode(args.policy)}
    provenance = {"source_url": args.url, "metadata_url": METADATA_URL, "publisher": PUBLISHER}
    if not policy_allows(args.policy, "fetch"):
        print(json.dumps(fail_closed_result(source_skill_id=SOURCE_SKILL_ID, tool_type="fetch", policy=args.policy, input_payload=input_payload, reason=policy_reason(args.policy, "fetch"), provenance=provenance, used_platform_tools=USED_PLATFORM_TOOLS), indent=2, sort_keys=True))
        return
    try:
        name = Path(args.fixture_file or args.url).name
        data = Path(args.fixture_file).read_bytes() if args.fixture_file else fetch_bytes_with_live_gate(args.url, max_bytes=min(args.max_bytes, 32768))
        probe_result, checks = inspect_oecd_metadata(name=name, data=data)
        if probe_result["status"] != "probe_requestable":
            raise ValueError(str(probe_result["reason"]))
        target = Path(args.output_dir) / "oecd_data_sample.xml"
        artifact = fetch_file_artifact(fixture_file=args.fixture_file, url=args.url, target=target, policy=args.policy, max_bytes=args.max_bytes, artifact_format="xml")
        checks.append({"name": "sample_written", "passed": True})
        result = {"status": "fetched", "reason": probe_result["reason"], "size_bytes": artifact["size_bytes"]}
        artifacts = [artifact]
    except Exception as exc:
        result = {"status": "needs_follow_up", "reason": str(exc)}
        checks = [{"name": "fetch_exception", "passed": False, "reason": type(exc).__name__}]
        artifacts = []
    print(json.dumps(build_tool_result(source_skill_id=SOURCE_SKILL_ID, tool_type="fetch", policy=args.policy, input_payload=input_payload, result=result, provenance=provenance, artifacts=artifacts, validation={"checks": checks}, used_platform_tools=USED_PLATFORM_TOOLS), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
