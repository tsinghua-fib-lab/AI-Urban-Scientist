from __future__ import annotations

import argparse
import csv
import io
import json
import sys
import zipfile
from pathlib import Path


OPEN_DATA_SKILLS_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(OPEN_DATA_SKILLS_ROOT))

from open_data_skills.tool_contract import build_tool_result, fail_closed_result, policy_allows, policy_reason, validation_check


SOURCE_SKILL_ID = "gtfs_feed"
REQUIRED_MEMBERS = ["agency.txt", "stops.txt", "routes.txt", "trips.txt", "stop_times.txt"]
REQUIRED_COLUMNS = {
    "agency.txt": ["agency_name", "agency_url", "agency_timezone"],
    "stops.txt": ["stop_id", "stop_name", "stop_lat", "stop_lon"],
    "routes.txt": ["route_id", "route_type"],
    "trips.txt": ["route_id", "service_id", "trip_id"],
    "stop_times.txt": ["trip_id", "arrival_time", "departure_time", "stop_id", "stop_sequence"],
}


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate GTFS static feed zip members.")
    parser.add_argument("--policy", default="discovery_only")
    parser.add_argument("--input-file", required=True)
    parser.add_argument("--start-date", default="")
    parser.add_argument("--end-date", default="")
    args = parser.parse_args()
    input_payload = {"input_file": args.input_file, "start_date": args.start_date, "end_date": args.end_date}
    provenance = {"source_url": "", "metadata_url": "", "publisher": "Transit agency or feed publisher"}
    if not policy_allows(args.policy, "validate"):
        print(json.dumps(fail_closed_result(source_skill_id=SOURCE_SKILL_ID, tool_type="validate", policy=args.policy, input_payload=input_payload, reason=policy_reason(args.policy, "validate"), provenance=provenance), indent=2, sort_keys=True))
        return
    checks = _checks(Path(args.input_file), start_date=args.start_date, end_date=args.end_date)
    passed = all(check["passed"] for check in checks)
    print(json.dumps(build_tool_result(source_skill_id=SOURCE_SKILL_ID, tool_type="validate", policy=args.policy, input_payload=input_payload, result={"status": "validation_passed" if passed else "validation_failed"}, provenance=provenance, validation={"checks": checks}), indent=2, sort_keys=True))


def _checks(path: Path, *, start_date: str = "", end_date: str = "") -> list[dict[str, object]]:
    try:
        with zipfile.ZipFile(path) as archive:
            names = {name.split("/", 1)[-1] for name in archive.namelist()}
            tables = {
                member: _read_csv_member(archive, member)
                for member in sorted((set(REQUIRED_MEMBERS) | {"calendar.txt", "calendar_dates.txt"}) & names)
            }
        checks = [validation_check(f"member_present:{name}", name in names) for name in REQUIRED_MEMBERS]
        for member, columns in REQUIRED_COLUMNS.items():
            header = tables.get(member, {}).get("header", [])
            for column in columns:
                checks.append(validation_check(f"column_present:{member}:{column}", column in header))
        checks.extend(_foreign_key_checks(tables))
        checks.append(validation_check("service_calendar_present", "calendar.txt" in names or "calendar_dates.txt" in names))
        if start_date or end_date:
            checks.append(_service_date_coverage_check(tables, start_date, end_date))
        return checks
    except Exception as exc:
        return [validation_check("zip_open", False, reason=type(exc).__name__)]


def _read_csv_member(archive: zipfile.ZipFile, member: str) -> dict[str, object]:
    with archive.open(member) as raw:
        text = io.TextIOWrapper(raw, encoding="utf-8-sig", errors="replace", newline="")
        reader = csv.DictReader(text)
        rows = []
        for index, row in enumerate(reader):
            if index >= 5000:
                break
            rows.append(row)
        return {"header": list(reader.fieldnames or []), "rows": rows}


def _foreign_key_checks(tables: dict[str, dict[str, object]]) -> list[dict[str, object]]:
    routes = {row.get("route_id") for row in _rows(tables, "routes.txt")}
    stops = {row.get("stop_id") for row in _rows(tables, "stops.txt")}
    trips = _rows(tables, "trips.txt")
    trip_ids = {row.get("trip_id") for row in trips}
    stop_times = _rows(tables, "stop_times.txt")
    service_ids = _service_ids(tables)
    return [
        validation_check("foreign_key:trips.route_id->routes.route_id", all(row.get("route_id") in routes for row in trips)),
        validation_check("foreign_key:trips.service_id->calendar.service_id", bool(service_ids) and all(row.get("service_id") in service_ids for row in trips)),
        validation_check("foreign_key:stop_times.trip_id->trips.trip_id", all(row.get("trip_id") in trip_ids for row in stop_times)),
        validation_check("foreign_key:stop_times.stop_id->stops.stop_id", all(row.get("stop_id") in stops for row in stop_times)),
    ]


def _service_date_coverage_check(tables: dict[str, dict[str, object]], start_date: str, end_date: str) -> dict[str, object]:
    requested_start = _gtfs_date(start_date)
    requested_end = _gtfs_date(end_date)
    ranges = []
    for row in _rows(tables, "calendar.txt"):
        ranges.append((row.get("start_date", ""), row.get("end_date", "")))
    for row in _rows(tables, "calendar_dates.txt"):
        date = row.get("date", "")
        if date:
            ranges.append((date, date))
    covered = any((not requested_start or start <= requested_start) and (not requested_end or end >= requested_end) for start, end in ranges if start and end)
    return validation_check("service_date_coverage", covered, requested_start=requested_start, requested_end=requested_end)


def _service_ids(tables: dict[str, dict[str, object]]) -> set[str]:
    service_ids = {row.get("service_id") for row in _rows(tables, "calendar.txt")}
    service_ids.update(row.get("service_id") for row in _rows(tables, "calendar_dates.txt"))
    return {value for value in service_ids if value}


def _rows(tables: dict[str, dict[str, object]], member: str) -> list[dict[str, str]]:
    rows = tables.get(member, {}).get("rows", [])
    return rows if isinstance(rows, list) else []


def _gtfs_date(value: str) -> str:
    return value.replace("-", "") if value else ""


if __name__ == "__main__":
    main()
