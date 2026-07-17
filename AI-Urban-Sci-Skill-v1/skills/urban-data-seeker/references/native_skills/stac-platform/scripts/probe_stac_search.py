#!/usr/bin/env python3
"""Run a bounded STAC item search and report asset download candidates."""

from __future__ import annotations

import argparse
import json
import urllib.error
import urllib.parse
import urllib.request
from typing import Any


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--catalog-url", required=True)
    parser.add_argument("--collection", required=True)
    parser.add_argument("--bbox", default="")
    parser.add_argument("--datetime", default="")
    parser.add_argument("--asset", default="")
    parser.add_argument("--limit", type=int, default=5)
    parser.add_argument("--probe-assets", action="store_true")
    args = parser.parse_args()
    payload = search(args)
    print(json.dumps(payload, indent=2, sort_keys=True))


def search(args: argparse.Namespace) -> dict[str, Any]:
    params = {"collections": args.collection, "limit": str(max(args.limit, 1))}
    if args.bbox:
        params["bbox"] = args.bbox
    if args.datetime:
        params["datetime"] = args.datetime
    search_url = f"{args.catalog_url.rstrip('/')}/search?{urllib.parse.urlencode(params)}"
    response = get_json(search_url)
    assets: list[dict[str, Any]] = []
    if response.get("ok"):
        for feature in (response.get("json") or {}).get("features", []):
            for name, asset in (feature.get("assets") or {}).items():
                if args.asset and args.asset != name:
                    continue
                href = asset.get("href")
                if not href:
                    continue
                item = {
                    "item_id": feature.get("id"),
                    "asset": name,
                    "href": href,
                    "type": asset.get("type", ""),
                    "roles": asset.get("roles", []),
                    "datetime": (feature.get("properties") or {}).get("datetime", ""),
                }
                if args.probe_assets and href.startswith("http"):
                    item["probe"] = head_probe(href)
                assets.append(item)
    return {
        "source_skill_id": "stac-platform",
        "api_url": search_url,
        "query_probe": response if not response.get("ok") else {"ok": True, "http_status": response.get("http_status"), "feature_count": len((response.get("json") or {}).get("features", []))},
        "candidate_assets": assets,
        "selected": assets[0] if assets else None,
        "finality": "candidate_until_asset_probe_and_semantic_check",
        "strict_success_rule": "A STAC collection/items URL is not a direct file. Strict success requires a concrete asset href or executable item-search URL with item/assets verified.",
    }


def get_json(url: str) -> dict[str, Any]:
    try:
        with urllib.request.urlopen(url, timeout=30) as response:
            return {"ok": True, "http_status": response.status, "json": json.loads(response.read().decode("utf-8", "replace"))}
    except urllib.error.HTTPError as exc:
        return {"ok": False, "http_status": exc.code, "error": str(exc)}
    except Exception as exc:
        return {"ok": False, "http_status": None, "error": str(exc)}


def head_probe(url: str) -> dict[str, Any]:
    try:
        request = urllib.request.Request(url, method="HEAD", headers={"User-Agent": "urban-data-skill-stac-resolver/1.0"})
        with urllib.request.urlopen(request, timeout=20) as response:
            return {"ok": 200 <= response.status < 400, "http_status": response.status, "content_type": response.headers.get("content-type", ""), "content_length": response.headers.get("content-length", "")}
    except urllib.error.HTTPError as exc:
        return {"ok": False, "http_status": exc.code, "error": str(exc)}
    except Exception as exc:
        return {"ok": False, "http_status": None, "error": str(exc)}


if __name__ == "__main__":
    main()

