from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


OPEN_DATA_SKILLS_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(OPEN_DATA_SKILLS_ROOT))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from open_data_skills.tool_contract import build_tool_result, fail_closed_result, policy_allows, policy_reason
from probe_oecd_data_api import inspect_oecd_metadata


SOURCE_SKILL_ID = "oecd_data"
PUBLISHER = "OECD"
METADATA_URL = "https://www.oecd.org/en/data/insights/data-explainers/2024/09/api.html"
USED_PLATFORM_TOOLS = ["sdmx_platform"]


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate an OECD SDMX metadata sample.")
    parser.add_argument("--policy", default="discovery_only")
    parser.add_argument("--input-file", required=True)
    args = parser.parse_args()
    input_payload = {"input_file": args.input_file}
    provenance = {"source_url": "", "metadata_url": METADATA_URL, "publisher": PUBLISHER}
    if not policy_allows(args.policy, "validate"):
        print(json.dumps(fail_closed_result(source_skill_id=SOURCE_SKILL_ID, tool_type="validate", policy=args.policy, input_payload=input_payload, reason=policy_reason(args.policy, "validate"), provenance=provenance, used_platform_tools=USED_PLATFORM_TOOLS), indent=2, sort_keys=True))
        return
    try:
        path = Path(args.input_file)
        result_probe, checks = inspect_oecd_metadata(name=path.name, data=path.read_bytes())
        result = {"status": "validation_passed" if result_probe["status"] == "probe_requestable" else "validation_failed"}
    except Exception as exc:
        result = {"status": "validation_failed", "reason": str(exc)}
        checks = [{"name": "validate_exception", "passed": False, "reason": type(exc).__name__}]
    print(json.dumps(build_tool_result(source_skill_id=SOURCE_SKILL_ID, tool_type="validate", policy=args.policy, input_payload=input_payload, result=result, provenance=provenance, validation={"checks": checks}, used_platform_tools=USED_PLATFORM_TOOLS), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
