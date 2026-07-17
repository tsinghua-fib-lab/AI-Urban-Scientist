#!/usr/bin/env python3
"""Build and optionally probe Legistar or Chicago eLMS legislative API URLs."""

from __future__ import annotations

import argparse
import json
import urllib.error
import urllib.parse
import urllib.request
from typing import Any


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--system", choices=("legistar", "chicago-elms"), default="legistar")
    parser.add_argument("--client", default="", help="Legistar client slug such as seattle, chicago, nyc. Not used for chicago-elms.")
    parser.add_argument("--query", default="")
    parser.add_argument("--top", type=int, default=10)
    parser.add_argument("--probe", action="store_true")
    args = parser.parse_args()
    payload = build_payload(args)
    print(json.dumps(payload, indent=2, sort_keys=True))


def build_payload(args: argparse.Namespace) -> dict[str, Any]:
    if args.system == "chicago-elms":
        params = {"top": str(max(args.top, 1))}
        if args.query:
            params["search"] = args.query
        api_url = f"https://api.chicityclerkelms.chicago.gov/search?{urllib.parse.urlencode(params)}"
        landing = "https://chicityclerkelms.chicago.gov/"
        metadata = "https://api.chicityclerkelms.chicago.gov/swagger.json"
    else:
        if not args.client:
            raise SystemExit("--client is required for generic Legistar Web API")
        params = {"$top": str(max(args.top, 1))}
        if args.query:
            escaped = args.query.replace("'", "''")
            params["$filter"] = f"contains(MatterTitle,'{escaped}') or contains(MatterName,'{escaped}')"
        api_url = f"https://webapi.legistar.com/v1/{args.client}/matters?{urllib.parse.urlencode(params)}"
        landing = f"https://{args.client}.legistar.com/"
        metadata = "https://webapi.legistar.com/"
    payload: dict[str, Any] = {
        "source_skill_id": "legistar-platform",
        "system": args.system,
        "api_url": api_url,
        "landing_or_index_url": landing,
        "metadata_url": metadata,
        "direct_download_url": "",
        "finality": "candidate_until_probe_and_record_detail_check",
        "strict_success_rule": "A generic portal page is not strict success. Return a working search/detail API and, when needed, per-record attachment/text URLs.",
        "fields_to_validate": ["title", "introduced/final dates", "status", "sponsor/body", "record id", "attachments/text"],
    }
    if args.probe:
        payload["api_probe"] = get_json(api_url)
        payload["metadata_probe"] = get_json(metadata)
    return payload


def get_json(url: str) -> dict[str, Any]:
    try:
        request = urllib.request.Request(url, headers={"User-Agent": "urban-data-skill-legistar-resolver/1.0"})
        with urllib.request.urlopen(request, timeout=30) as response:
            body = response.read(200000).decode("utf-8", "replace")
            return {"ok": True, "http_status": response.status, "content_type": response.headers.get("content-type", ""), "sample": json.loads(body)}
    except urllib.error.HTTPError as exc:
        return {"ok": False, "http_status": exc.code, "error": str(exc)}
    except Exception as exc:
        return {"ok": False, "http_status": None, "error": str(exc)}


if __name__ == "__main__":
    main()

