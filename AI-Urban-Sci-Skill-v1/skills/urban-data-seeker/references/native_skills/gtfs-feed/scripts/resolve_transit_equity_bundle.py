from __future__ import annotations

import argparse
import json
import sys
import urllib.request
from pathlib import Path
from typing import Any


OPEN_DATA_SKILLS_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(OPEN_DATA_SKILLS_ROOT))

from open_data_skills.tool_contract import build_tool_result, validation_check


SOURCE_SKILL_ID = "gtfs_feed"
PRESETS = {
    "chicago": {
        "agency": "Chicago Transit Authority",
        "gtfs_zip_url": "https://www.transitchicago.com/downloads/schedulenet/gtfs.zip",
        "tracts_zip_url": "https://www2.census.gov/geo/tiger/TIGER2023/TRACT/tl_2023_17_tract.zip",
        "acs_api_template": "https://api.census.gov/data/2023/acs/acs5?get=NAME,B01003_001E,B19013_001E&for=tract:*&in=state:17%20county:031",
        "notes": "CTA GTFS covers schedule routes/stops/trips; TIGER/ACS county tract resources support equity joins for Cook County/Chicago analysis.",
    },
    "nyc": {
        "agency": "Metropolitan Transportation Authority",
        "gtfs_zip_url": "https://rrgtfsfeeds.s3.amazonaws.com/gtfs_subway.zip",
        "tracts_zip_url": "https://www2.census.gov/geo/tiger/TIGER2023/TRACT/tl_2023_36_tract.zip",
        "acs_api_template": "https://api.census.gov/data/2023/acs/acs5?get=NAME,B01003_001E,B19013_001E&for=tract:*&in=state:36",
        "notes": "MTA subway GTFS is a direct static feed; TIGER/ACS state tract resources should be filtered to NYC counties downstream.",
    },
}
REQUIRED_GTFS_MEMBERS = ["agency.txt", "stops.txt", "routes.txt", "trips.txt", "stop_times.txt", "calendar.txt"]


def main() -> None:
    parser = argparse.ArgumentParser(description="Resolve a GTFS plus tract/ACS bundle for transit accessibility or equity analysis.")
    parser.add_argument("--policy", default="discovery_only")
    parser.add_argument("--city", choices=sorted(PRESETS), default="chicago")
    parser.add_argument("--probe", action="store_true", help="Probe the GTFS zip and TIGER zip headers/contents with bounded requests.")
    args = parser.parse_args()

    preset = PRESETS[args.city]
    checks = [
        validation_check("gtfs_url_present", bool(preset["gtfs_zip_url"])),
        validation_check("tracts_url_present", bool(preset["tracts_zip_url"])),
        validation_check("acs_api_template_present", bool(preset["acs_api_template"])),
    ]
    probe_result: dict[str, Any] = {"status": "not_probed"}
    if args.probe:
        probe_result = {
            "gtfs": _probe_zip_url(preset["gtfs_zip_url"]),
            "tracts": _probe_head(preset["tracts_zip_url"]),
        }
        checks.extend(probe_result["gtfs"].pop("checks"))
        checks.extend(probe_result["tracts"].pop("checks"))

    result = {
        "status": "bundle_ready",
        "city": args.city,
        "agency": preset["agency"],
        "direct_download_urls": {
            "gtfs_static_zip": preset["gtfs_zip_url"],
            "census_tiger_tracts_zip": preset["tracts_zip_url"],
        },
        "api_urls": {
            "acs5_tract_variables_template": preset["acs_api_template"],
        },
        "required_gtfs_members": REQUIRED_GTFS_MEMBERS,
        "notes": preset["notes"],
        "probe": probe_result,
    }
    print(
        json.dumps(
            build_tool_result(
                source_skill_id=SOURCE_SKILL_ID,
                tool_type="download_link",
                policy=args.policy,
                input_payload={"city": args.city, "probe": args.probe},
                result=result,
                provenance={
                    "source_url": preset["gtfs_zip_url"],
                    "metadata_url": "https://gtfs.org/schedule/reference/",
                    "publisher": preset["agency"],
                },
                validation={"checks": checks},
            ),
            indent=2,
            sort_keys=True,
        )
    )


def _probe_zip_url(url: str) -> dict[str, Any]:
    try:
        request = urllib.request.Request(url, headers={"User-Agent": "open-data-skill-probe/1.0"})
        with urllib.request.urlopen(request, timeout=45) as response:
            payload = response.read(2_000_000)
            status = response.status
            content_type = response.headers.get("content-type", "")
        has_zip_magic = payload.startswith(b"PK")
        return {
            "status": "ok",
            "http_status": status,
            "content_type": content_type,
            "sample_bytes": len(payload),
            "zip_magic": has_zip_magic,
            "checks": [
                validation_check("gtfs_http_200", status == 200, http_status=status),
                validation_check("gtfs_zip_magic", has_zip_magic),
            ],
        }
    except Exception as exc:
        return {
            "status": "probe_failed",
            "error": f"{type(exc).__name__}: {exc}",
            "checks": [validation_check("gtfs_zip_probe", False, reason=type(exc).__name__)],
        }


def _probe_head(url: str) -> dict[str, Any]:
    try:
        request = urllib.request.Request(url, method="HEAD", headers={"User-Agent": "open-data-skill-probe/1.0"})
        with urllib.request.urlopen(request, timeout=20) as response:
            status = response.status
            content_type = response.headers.get("content-type", "")
            length = response.headers.get("content-length", "")
        return {
            "status": "ok",
            "http_status": status,
            "content_type": content_type,
            "content_length": length,
            "checks": [validation_check("tiger_head_200", status == 200, http_status=status)],
        }
    except Exception as exc:
        return {
            "status": "probe_failed",
            "error": f"{type(exc).__name__}: {exc}",
            "checks": [validation_check("tiger_head_probe", False, reason=type(exc).__name__)],
        }


if __name__ == "__main__":
    main()
