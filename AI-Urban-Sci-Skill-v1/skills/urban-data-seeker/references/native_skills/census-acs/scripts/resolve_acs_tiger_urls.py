#!/usr/bin/env python3
"""Build paired ACS API and TIGER/Line URLs for tract/block-group workflows."""

from __future__ import annotations

import argparse
import json
import os
import urllib.error
import urllib.parse
import urllib.request
from typing import Any


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--year", default="2023")
    parser.add_argument("--survey", default="acs5", choices=("acs5", "acs1"))
    parser.add_argument("--geography", default="tract", choices=("tract", "block group", "county", "place"))
    parser.add_argument("--state", required=True, help="Two-digit FIPS state code.")
    parser.add_argument("--county", default="", help="Three-digit FIPS county code when needed.")
    parser.add_argument("--tract", default="")
    parser.add_argument("--variables", default="B19013_001E,B08303_001E,B25077_001E,B01003_001E")
    parser.add_argument("--api-key", default=os.environ.get("CENSUS_API_KEY", ""))
    parser.add_argument("--probe", action="store_true")
    args = parser.parse_args()

    payload = build_payload(args)
    if args.probe:
        payload["variable_probes"] = [get_json(url) for url in payload["variable_metadata_urls"][:5]]
        payload["tiger_probe"] = head_probe(payload["tiger_boundary_url"])
        if args.api_key:
            payload["acs_api_probe"] = get_json(payload["api_url"])
        else:
            payload["acs_api_probe"] = {
                "ok": False,
                "http_status": 302,
                "reason": "census_data_api_key_required_in_current_environment",
            }
    print(json.dumps(payload, indent=2, sort_keys=True))


def build_payload(args: argparse.Namespace) -> dict[str, Any]:
    variables = [item.strip() for item in args.variables.split(",") if item.strip()]
    params = {"get": ",".join(["NAME", *variables])}
    params.update(geography_params(args))
    if args.api_key:
        params["key"] = args.api_key
    api_root = f"https://api.census.gov/data/{args.year}/acs/{args.survey}"
    api_url = f"{api_root}?{urllib.parse.urlencode(params, quote_via=urllib.parse.quote)}"
    tiger_year = args.year
    tiger_layer = "TRACT" if args.geography == "tract" else "BG" if args.geography == "block group" else "COUNTY" if args.geography == "county" else "PLACE"
    tiger_url = f"https://www2.census.gov/geo/tiger/TIGER{tiger_year}/{tiger_layer}/tl_{tiger_year}_{args.state}_{tiger_layer.lower()}.zip"
    variable_urls = [f"{api_root}/variables/{urllib.parse.quote(variable)}.json" for variable in variables]
    return {
        "source_skill_id": "census-acs",
        "api_url": api_url if args.api_key else "",
        "api_url_template": f"{api_root}?{urllib.parse.urlencode({**params, 'key': '{CENSUS_API_KEY}'}, quote_via=urllib.parse.quote)}",
        "variable_metadata_urls": variable_urls,
        "tiger_boundary_url": tiger_url,
        "direct_download_url": tiger_url,
        "landing_or_index_url": "https://api.census.gov/data.html",
        "query": {
            "year": args.year,
            "survey": args.survey,
            "geography": args.geography,
            "state": args.state,
            "county": args.county,
            "tract": args.tract,
            "variables": variables,
            "api_key_supplied": bool(args.api_key),
        },
        "access_boundary": "Current Census Data API requests from this environment require a Census API key; variable metadata and TIGER/Line boundary ZIP files are public without a key.",
        "finality": "boundary_plus_geometry_direct_until_acs_key_probe",
        "strict_success_rule": "For ACS attributes, strict success needs a concrete API URL that returns JSON rows with a valid key. TIGER/Line geometry ZIP alone is not enough for socioeconomic attributes.",
    }


def geography_params(args: argparse.Namespace) -> dict[str, str]:
    if args.geography == "tract":
        require(args.county, "--county is required for tract geography")
        return {"for": "tract:*", "in": f"state:{args.state} county:{args.county}"}
    if args.geography == "block group":
        require(args.county, "--county is required for block group geography")
        require(args.tract, "--tract is required for block group geography")
        return {"for": "block group:*", "in": f"state:{args.state} county:{args.county} tract:{args.tract}"}
    if args.geography == "county":
        return {"for": "county:*", "in": f"state:{args.state}"}
    return {"for": "place:*", "in": f"state:{args.state}"}


def require(value: str, message: str) -> None:
    if not value:
        raise SystemExit(message)


def get_json(url: str) -> dict[str, Any]:
    try:
        request = urllib.request.Request(url, headers={"User-Agent": "urban-data-census-resolver/1.0"})
        with urllib.request.urlopen(request, timeout=30) as response:
            body = response.read(500000).decode("utf-8", "replace")
            return {"ok": True, "http_status": response.status, "content_type": response.headers.get("content-type", ""), "json": json.loads(body)}
    except urllib.error.HTTPError as exc:
        return {"ok": False, "http_status": exc.code, "error": str(exc)}
    except Exception as exc:
        return {"ok": False, "http_status": None, "error": str(exc)}


def head_probe(url: str) -> dict[str, Any]:
    try:
        request = urllib.request.Request(url, method="HEAD", headers={"User-Agent": "urban-data-census-resolver/1.0"})
        with urllib.request.urlopen(request, timeout=30) as response:
            return {"ok": 200 <= response.status < 400, "http_status": response.status, "content_type": response.headers.get("content-type", ""), "content_length": response.headers.get("content-length", ""), "last_modified": response.headers.get("last-modified", "")}
    except urllib.error.HTTPError as exc:
        return {"ok": False, "http_status": exc.code, "error": str(exc)}
    except Exception as exc:
        return {"ok": False, "http_status": None, "error": str(exc)}


if __name__ == "__main__":
    main()
