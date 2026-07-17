#!/usr/bin/env python3
"""Resolve CKAN package metadata into resource download candidates."""

from __future__ import annotations

import argparse
import json
import urllib.error
import urllib.parse
import urllib.request
from typing import Any


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--domain", required=True)
    parser.add_argument("--package-id", default="")
    parser.add_argument("--query", default="")
    parser.add_argument("--format", default="")
    parser.add_argument("--probe", action="store_true")
    args = parser.parse_args()
    payload = resolve(args.domain, package_id=args.package_id, query=args.query, wanted_format=args.format, probe=args.probe)
    print(json.dumps(payload, indent=2, sort_keys=True))


def resolve(domain: str, *, package_id: str, query: str, wanted_format: str, probe: bool) -> dict[str, Any]:
    if package_id:
        package = ckan_action(domain, "package_show", {"id": package_id})
    else:
        search = ckan_action(domain, "package_search", {"q": query, "rows": "5"})
        results = (((search.get("result") or {}).get("results")) or []) if search.get("success") else []
        package = {"success": bool(results), "result": results[0] if results else {}}
    resources = []
    for resource in (package.get("result") or {}).get("resources", []) if package.get("success") else []:
        url = resource.get("url") or ""
        if not url:
            continue
        fmt = (resource.get("format") or resource.get("mimetype") or "").lower()
        if wanted_format and wanted_format.lower() not in fmt and wanted_format.lower() not in url.lower():
            continue
        candidate = {
            "name": resource.get("name") or resource.get("description") or "",
            "resource_id": resource.get("id") or "",
            "format": resource.get("format") or "",
            "mimetype": resource.get("mimetype") or "",
            "direct_download_url": url,
            "last_modified": resource.get("last_modified") or resource.get("created") or "",
            "package_id": (package.get("result") or {}).get("name") or package_id,
        }
        if probe:
            candidate["probe"] = head_probe(url)
        resources.append(candidate)
    return {
        "source_skill_id": "ckan-platform",
        "metadata_url": build_action_url(domain, "package_show", {"id": (package.get("result") or {}).get("name") or package_id}) if package.get("success") else "",
        "candidate_resources": resources,
        "selected": resources[0] if resources else None,
        "finality": "candidate_until_resource_probe_and_semantic_check",
        "strict_success_rule": "CKAN package_search is discovery only. Strict success requires selecting and probing a package resource URL.",
    }


def ckan_action(domain: str, action: str, params: dict[str, str]) -> dict[str, Any]:
    url = build_action_url(domain, action, params)
    try:
        with urllib.request.urlopen(url, timeout=30) as response:
            return json.loads(response.read().decode("utf-8", "replace"))
    except Exception as exc:
        return {"success": False, "error": str(exc), "url": url}


def build_action_url(domain: str, action: str, params: dict[str, str]) -> str:
    return f"https://{domain}/api/3/action/{action}?{urllib.parse.urlencode(params)}"


def head_probe(url: str) -> dict[str, Any]:
    try:
        request = urllib.request.Request(url, method="HEAD", headers={"User-Agent": "urban-data-skill-ckan-resolver/1.0"})
        with urllib.request.urlopen(request, timeout=20) as response:
            return {"ok": 200 <= response.status < 400, "http_status": response.status, "content_type": response.headers.get("content-type", ""), "content_length": response.headers.get("content-length", "")}
    except urllib.error.HTTPError as exc:
        return {"ok": False, "http_status": exc.code, "error": str(exc)}
    except Exception as exc:
        return {"ok": False, "http_status": None, "error": str(exc)}


if __name__ == "__main__":
    main()

