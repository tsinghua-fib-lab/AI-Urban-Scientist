from __future__ import annotations

import argparse
import json
import sys
import zipfile
from pathlib import Path


OPEN_DATA_SKILLS_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(OPEN_DATA_SKILLS_ROOT))

from open_data_skills.tool_contract import build_tool_result, fail_closed_result, policy_allows, policy_reason, validation_check


SOURCE_SKILL_ID = "gtfs_feed"
REQUIRED_MEMBERS = ["agency.txt", "stops.txt", "routes.txt", "trips.txt", "stop_times.txt"]


def main() -> None:
    parser = argparse.ArgumentParser(description="Probe a GTFS static feed zip.")
    parser.add_argument("--policy", default="discovery_only")
    parser.add_argument("--fixture-zip")
    parser.add_argument("--url", default="")
    args = parser.parse_args()
    input_payload = {"fixture_zip": bool(args.fixture_zip), "url": args.url}
    provenance = {"source_url": args.url, "metadata_url": "", "publisher": "Transit agency or feed publisher"}
    if not policy_allows(args.policy, "probe"):
        print(json.dumps(fail_closed_result(source_skill_id=SOURCE_SKILL_ID, tool_type="probe", policy=args.policy, input_payload=input_payload, reason=policy_reason(args.policy, "probe"), provenance=provenance), indent=2, sort_keys=True))
        return
    checks = _zip_checks(Path(args.fixture_zip)) if args.fixture_zip else [validation_check("live_probe_not_implemented", False)]
    passed = all(check["passed"] for check in checks)
    print(json.dumps(build_tool_result(source_skill_id=SOURCE_SKILL_ID, tool_type="probe", policy=args.policy, input_payload=input_payload, result={"status": "probe_requestable" if passed else "needs_follow_up"}, provenance=provenance, validation={"checks": checks}), indent=2, sort_keys=True))


def _zip_checks(path: Path) -> list[dict[str, object]]:
    try:
        with zipfile.ZipFile(path) as archive:
            names = {name.split("/", 1)[-1] for name in archive.namelist()}
        return [validation_check(f"member_present:{name}", name in names) for name in REQUIRED_MEMBERS]
    except Exception as exc:
        return [validation_check("zip_open", False, reason=type(exc).__name__)]


if __name__ == "__main__":
    main()
