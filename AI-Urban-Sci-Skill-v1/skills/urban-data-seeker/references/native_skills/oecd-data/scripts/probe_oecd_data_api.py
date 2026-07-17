from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


OPEN_DATA_SKILLS_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(OPEN_DATA_SKILLS_ROOT))

from open_data_skills.tool_contract import build_tool_result, fail_closed_result, fetch_bytes_with_live_gate, policy_allows, policy_reason


SOURCE_SKILL_ID = "oecd_data"
PUBLISHER = "OECD"
METADATA_URL = "https://www.oecd.org/en/data/insights/data-explainers/2024/09/api.html"
USED_PLATFORM_TOOLS = ["sdmx_platform"]
EXPECTED_SUFFIXES = (".xml", ".sdmx", ".txt")


def main() -> None:
    parser = argparse.ArgumentParser(description="Probe an OECD SDMX dataflow metadata response.")
    parser.add_argument("--policy", default="discovery_only")
    parser.add_argument("--fixture-file")
    parser.add_argument("--url", default="")
    args = parser.parse_args()
    input_payload = {"fixture_file": bool(args.fixture_file), "url": args.url}
    provenance = {"source_url": args.url, "metadata_url": METADATA_URL, "publisher": PUBLISHER}
    if not policy_allows(args.policy, "probe"):
        print(json.dumps(fail_closed_result(source_skill_id=SOURCE_SKILL_ID, tool_type="probe", policy=args.policy, input_payload=input_payload, reason=policy_reason(args.policy, "probe"), provenance=provenance, used_platform_tools=USED_PLATFORM_TOOLS), indent=2, sort_keys=True))
        return
    try:
        name = Path(args.fixture_file or args.url).name
        data = Path(args.fixture_file).read_bytes() if args.fixture_file else fetch_bytes_with_live_gate(args.url, max_bytes=32768)
        result, checks = inspect_oecd_metadata(name=name, data=data)
    except Exception as exc:
        result = {"status": "needs_follow_up", "reason": str(exc)}
        checks = [{"name": "probe_exception", "passed": False, "reason": type(exc).__name__}]
    print(json.dumps(build_tool_result(source_skill_id=SOURCE_SKILL_ID, tool_type="probe", policy=args.policy, input_payload=input_payload, result=result, provenance=provenance, validation={"checks": checks}, used_platform_tools=USED_PLATFORM_TOOLS), indent=2, sort_keys=True))


def inspect_oecd_metadata(*, name: str, data: bytes) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    text = data.decode("utf-8", errors="ignore")
    suffix_ok = any(name.lower().endswith(suffix) for suffix in EXPECTED_SUFFIXES)
    structure_ok = "<message:Structure" in text or "<Structure" in text
    dataflow_ok = "<structure:Dataflow" in text or "<Dataflow" in text
    named_ok = "<common:Name" in text or "Dataflow id=" in text
    checks = [
        {"name": "expected_suffix", "passed": suffix_ok, "expected_suffixes": list(EXPECTED_SUFFIXES)},
        {"name": "sdmx_structure_present", "passed": structure_ok},
        {"name": "dataflow_present", "passed": dataflow_ok},
        {"name": "dataflow_name_present", "passed": named_ok},
    ]
    passed = all(check["passed"] for check in checks)
    result = {"status": "probe_requestable" if passed else "needs_follow_up", "reason": "oecd_dataflow_metadata_shape_ok" if passed else "oecd_dataflow_metadata_shape_incomplete"}
    return result, checks


if __name__ == "__main__":
    main()
