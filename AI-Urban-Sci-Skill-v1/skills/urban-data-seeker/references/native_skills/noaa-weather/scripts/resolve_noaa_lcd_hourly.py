from __future__ import annotations

import argparse
import json
import sys
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any


OPEN_DATA_SKILLS_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(OPEN_DATA_SKILLS_ROOT))

from open_data_skills.tool_contract import build_tool_result, validation_check


SOURCE_SKILL_ID = "noaa_weather"
NCEI_DATA_SERVICE = "https://www.ncei.noaa.gov/access/services/data/v1"
DEFAULT_DATASET = "local-climatological-data"
PRESET_STATIONS = {
    "chicago": ["72530094846", "72534014819"],
    "houston": ["72243012960"],
}
LCD_HOURLY_FIELDS = [
    "STATION",
    "NAME",
    "LATITUDE",
    "LONGITUDE",
    "DATE",
    "HourlyDryBulbTemperature",
    "HourlyDewPointTemperature",
    "HourlyRelativeHumidity",
    "HourlyWindSpeed",
    "HourlyPrecipitation",
]


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Resolve NOAA NCEI Local Climatological Data hourly observation API URLs."
    )
    parser.add_argument("--policy", default="discovery_only")
    parser.add_argument("--city", choices=sorted(PRESET_STATIONS), default="")
    parser.add_argument("--stations", default="", help="Comma-separated NCEI LCD station identifiers.")
    parser.add_argument("--start-date", required=True, help="YYYY-MM-DD or ISO datetime.")
    parser.add_argument("--end-date", required=True, help="YYYY-MM-DD or ISO datetime.")
    parser.add_argument("--format", choices=["json", "csv"], default="csv")
    parser.add_argument("--units", choices=["metric", "standard"], default="metric")
    parser.add_argument("--probe", action="store_true", help="Run a bounded live probe of the generated API URL.")
    args = parser.parse_args()

    stations = _resolve_stations(args.city, args.stations)
    url = _build_url(
        dataset=DEFAULT_DATASET,
        stations=stations,
        start_date=args.start_date,
        end_date=args.end_date,
        output_format=args.format,
        units=args.units,
    )
    checks = [
        validation_check("dataset_is_lcd_hourly", True, dataset=DEFAULT_DATASET),
        validation_check("stations_present", bool(stations), stations=stations),
        validation_check("date_range_present", bool(args.start_date and args.end_date)),
        validation_check("station_metadata_requested", True),
    ]
    probe_result: dict[str, Any] = {"status": "not_probed"}
    if args.probe:
        probe_result = _probe_url(url)
        checks.extend(probe_result.pop("checks"))

    result = {
        "status": "api_url_ready" if stations else "needs_station_selection",
        "dataset": DEFAULT_DATASET,
        "city_preset": args.city,
        "stations": stations,
        "api_url": url,
        "direct_download_url": url if args.format == "csv" else "",
        "format": args.format,
        "units": args.units,
        "expected_fields": LCD_HOURLY_FIELDS,
        "probe": probe_result,
    }
    provenance = {
        "source_url": url,
        "metadata_url": "https://www.ncei.noaa.gov/access/services/data/v1",
        "publisher": "NOAA National Centers for Environmental Information",
    }
    print(
        json.dumps(
            build_tool_result(
                source_skill_id=SOURCE_SKILL_ID,
                tool_type="download_link",
                policy=args.policy,
                input_payload={
                    "city": args.city,
                    "stations": stations,
                    "start_date": args.start_date,
                    "end_date": args.end_date,
                    "format": args.format,
                    "units": args.units,
                    "probe": args.probe,
                },
                result=result,
                provenance=provenance,
                validation={"checks": checks},
            ),
            indent=2,
            sort_keys=True,
        )
    )


def _resolve_stations(city: str, station_csv: str) -> list[str]:
    if station_csv:
        return [item.strip() for item in station_csv.split(",") if item.strip()]
    return list(PRESET_STATIONS.get(city, []))


def _build_url(
    *,
    dataset: str,
    stations: list[str],
    start_date: str,
    end_date: str,
    output_format: str,
    units: str,
) -> str:
    params = {
        "dataset": dataset,
        "stations": ",".join(stations),
        "startDate": start_date,
        "endDate": end_date,
        "format": output_format,
        "includeStationName": "true",
        "includeStationLocation": "true",
        "units": units,
    }
    return f"{NCEI_DATA_SERVICE}?{urllib.parse.urlencode(params)}"


def _probe_url(url: str) -> dict[str, Any]:
    try:
        request = urllib.request.Request(url, headers={"User-Agent": "open-data-skill-probe/1.0"})
        with urllib.request.urlopen(request, timeout=30) as response:
            payload = response.read(200_000)
            text = payload.decode("utf-8", errors="replace")
            content_type = response.headers.get("content-type", "")
            status = response.status
        has_station = "STATION" in text
        has_time = "DATE" in text
        has_temp = "HourlyDryBulbTemperature" in text
        return {
            "status": "ok" if status == 200 else "unexpected_status",
            "http_status": status,
            "content_type": content_type,
            "sample_bytes": len(payload),
            "checks": [
                validation_check("http_200", status == 200, http_status=status),
                validation_check("has_station_field", has_station),
                validation_check("has_datetime_field", has_time),
                validation_check("has_hourly_temperature_field", has_temp),
            ],
        }
    except Exception as exc:
        return {
            "status": "probe_failed",
            "error": f"{type(exc).__name__}: {exc}",
            "checks": [validation_check("live_probe", False, reason=type(exc).__name__)],
        }


if __name__ == "__main__":
    main()
