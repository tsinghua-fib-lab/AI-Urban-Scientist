#!/usr/bin/env python3
"""Build public Socrata data/API URLs from a verified domain and view id."""

from __future__ import annotations

import argparse
import json
from urllib.parse import quote, urlencode


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--domain", required=True)
    parser.add_argument("--view-id", required=True)
    parser.add_argument("--format", choices=("csv", "json", "geojson"), default="csv")
    parser.add_argument("--limit", type=int, default=100, help="Sample row limit. Ignored when --full-export is set.")
    parser.add_argument("--full-export", action="store_true", help="Emit an unbounded export URL suitable as a final data URL after metadata validation.")
    parser.add_argument("--where", default="")
    parser.add_argument("--select", default="")
    args = parser.parse_args()
    params = {} if args.full_export else {"$limit": str(max(args.limit, 1))}
    if args.where:
        params["$where"] = args.where
    if args.select:
        params["$select"] = args.select
    query = urlencode(params, quote_via=quote)
    url = f"https://{args.domain}/resource/{args.view_id}.{args.format}"
    if query:
        url = f"{url}?{query}"
    metadata_url = f"https://{args.domain}/api/views/{args.view_id}.json"
    payload = {
        "source_skill_id": "socrata-platform",
        "direct_download_url": url if args.format == "csv" else "",
        "api_url": url if args.format in {"json", "geojson"} else f"https://{args.domain}/resource/{args.view_id}.json",
        "metadata_url": metadata_url,
        "rows_export_url": f"https://{args.domain}/api/views/{args.view_id}/rows.csv?accessType=DOWNLOAD",
        "resource_base": f"https://{args.domain}/resource/{args.view_id}",
        "landing_or_index_url": f"https://{args.domain}/d/{args.view_id}",
        "probe": {"method": "GET", "bounded_by": None if args.full_export else "$limit"},
        "authorization_required": False,
        "finality": "candidate_until_metadata_and_sample_probe",
        "strict_success_rule": "A $limit sample URL is not a final direct download. For strict pass, return rows_export_url or a filtered resource URL that covers the requested data.",
    }
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
