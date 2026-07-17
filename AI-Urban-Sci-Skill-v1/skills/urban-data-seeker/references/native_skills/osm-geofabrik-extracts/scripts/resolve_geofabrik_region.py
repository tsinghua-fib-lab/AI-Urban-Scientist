#!/usr/bin/env python3
"""Resolve the smallest matching Geofabrik extract from the official index."""

from __future__ import annotations

import argparse
import json
import re
import urllib.error
import urllib.request
from typing import Any


INDEX_URL = "https://download.geofabrik.de/index-v1.json"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--region", required=True, help="City, state, country, or Geofabrik region name.")
    parser.add_argument("--format", choices=("pbf", "shp"), default="pbf")
    parser.add_argument("--max-candidates", type=int, default=8)
    parser.add_argument("--probe", action="store_true")
    args = parser.parse_args()

    index = get_json(INDEX_URL)
    candidates = rank_candidates(index.get("features", []), args.region, args.format)
    candidates = candidates[: max(args.max_candidates, 1)]
    if args.probe:
        for candidate in candidates:
            url = candidate.get("direct_download_url", "")
            candidate["probe"] = head_probe(url) if url else {"ok": False, "reason": "missing_url"}

    selected = candidates[0] if candidates else None
    payload = {
        "source_skill_id": "osm-geofabrik-extracts",
        "query": {"region": args.region, "format": args.format},
        "index_url": INDEX_URL,
        "selected": selected,
        "candidate_count": len(candidates),
        "candidates": candidates,
        "direct_download_url": selected.get("direct_download_url", "") if selected else "",
        "landing_or_index_url": selected.get("region_page_url", "https://download.geofabrik.de/") if selected else "https://download.geofabrik.de/",
        "finality": "candidate_until_probe_and_coverage_check",
        "strict_success_rule": "Use the smallest official extract whose Geofabrik name/id matches the requested geography. Do not fall back to a country extract when a city/region extract exists.",
    }
    print(json.dumps(payload, indent=2, sort_keys=True))


def get_json(url: str) -> dict[str, Any]:
    request = urllib.request.Request(url, headers={"User-Agent": "urban-data-geofabrik-resolver/1.0"})
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.loads(response.read().decode("utf-8", "replace"))


def rank_candidates(features: list[dict[str, Any]], region: str, fmt: str) -> list[dict[str, Any]]:
    query_tokens = tokenize(region)
    query_norm = " ".join(query_tokens)
    candidates: list[dict[str, Any]] = []
    for feature in features:
        props = feature.get("properties") or {}
        urls = props.get("urls") or {}
        url = urls.get(fmt)
        if not url:
            continue
        name = str(props.get("name") or "")
        region_id = str(props.get("id") or "")
        parent = str(props.get("parent") or "")
        searchable = " ".join([name, region_id.replace("-", " "), parent.replace("-", " ")]).lower()
        searchable_tokens = set(tokenize(searchable))
        overlap = len(set(query_tokens) & searchable_tokens)
        if not overlap and query_norm not in searchable:
            continue
        exact_bonus = 0
        if query_norm == " ".join(tokenize(name)) or query_norm == " ".join(tokenize(region_id.replace("-", " "))):
            exact_bonus += 100
        if query_norm and query_norm in searchable:
            exact_bonus += 40
        # Prefer more specific child extracts when scores are otherwise similar.
        depth = url.replace("https://download.geofabrik.de/", "").count("/")
        score = exact_bonus + overlap * 10 + depth
        candidates.append(
            {
                "name": name,
                "id": region_id,
                "parent": parent,
                "format": fmt,
                "direct_download_url": url,
                "region_page_url": url.rsplit("-", 1)[0] + ".html" if "-latest" in url else "https://download.geofabrik.de/",
                "score": score,
                "match_reason": {
                    "query_tokens": query_tokens,
                    "overlap": sorted(set(query_tokens) & searchable_tokens),
                    "exact_or_substring_bonus": exact_bonus,
                    "path_depth_preference": depth,
                },
            }
        )
    return sorted(candidates, key=lambda item: (-int(item["score"]), len(str(item["direct_download_url"]))))


def tokenize(value: str) -> list[str]:
    return [token for token in re.split(r"[^a-z0-9]+", value.lower()) if token]


def head_probe(url: str) -> dict[str, Any]:
    try:
        request = urllib.request.Request(url, method="HEAD", headers={"User-Agent": "urban-data-geofabrik-resolver/1.0"})
        with urllib.request.urlopen(request, timeout=30) as response:
            return {
                "ok": 200 <= response.status < 400,
                "http_status": response.status,
                "content_type": response.headers.get("content-type", ""),
                "content_length": response.headers.get("content-length", ""),
                "last_modified": response.headers.get("last-modified", ""),
                "final_url": response.geturl(),
            }
    except urllib.error.HTTPError as exc:
        return {"ok": False, "http_status": exc.code, "error": str(exc)}
    except Exception as exc:
        return {"ok": False, "http_status": None, "error": str(exc)}


if __name__ == "__main__":
    main()
