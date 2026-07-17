from __future__ import annotations

import argparse
import json
from urllib.parse import quote_plus, urlparse


PACKAGE_ID = "ckan_platform"
REQUIRED_VALIDATION = ["resolver", "probe", "download", "verifier"]


def main() -> None:
    parser = argparse.ArgumentParser(description="Emit not-final CKAN platform hints.")
    parser.add_argument("--need-id", required=True)
    parser.add_argument("--url", required=True)
    parser.add_argument("--query", default="")
    args = parser.parse_args()

    payload = build_payload(need_id=args.need_id, url=args.url, query=args.query)
    print(json.dumps(payload, indent=2, sort_keys=True))


def build_payload(*, need_id: str, url: str, query: str) -> dict[str, object]:
    parsed = parse_ckan_url(url)
    search_query = query or parsed["id"]
    resource_hints = [
        {
            "role": "package_search",
            "url": f"https://{parsed['domain']}/api/3/action/package_search?q={quote_plus(search_query)}",
            "access_method": "ckan_package_search",
            "need_ids": [need_id],
            "required_validation": REQUIRED_VALIDATION,
            "finality": "not_final",
            "consumer_authority": "none",
            "executability_hint": "source_landing",
            "required_params": ["domain", "query"],
            "missing_params": [],
            "resolver_hint": {
                "resolver_family": "ckan_package_search",
                "target_executability_hint": "resolvable_resource",
                "search_query": search_query,
            },
            "api_query_template": {
                "url": "https://{domain}/api/3/action/package_search",
                "query_params": {
                    "q": "{query}",
                },
            },
            "future_probe_hint": {
                "method": "GET_LIGHT",
                "expected_status": [200],
                "notes": "Probe package_search only as discovery metadata, not as a final data resource.",
            },
            "validation_notes": [
                "Package search is portal metadata and does not decide research fit.",
                "Validate package identity, resources, formats, freshness, and licenses downstream.",
            ],
        },
        {
            "role": "package_show",
            "url": f"https://{parsed['domain']}/api/3/action/package_show?id={quote_plus(parsed['id'])}",
            "access_method": "ckan_package_metadata",
            "need_ids": [need_id],
            "required_validation": REQUIRED_VALIDATION,
            "finality": "not_final",
            "consumer_authority": "none",
            "executability_hint": "resolvable_resource",
            "required_params": ["domain", "package_id"],
            "missing_params": [],
            "resolver_hint": {
                "resolver_family": "ckan_package_show",
                "stable_package_id": parsed["id"],
                "target_executability_hint": "resolvable_resource",
            },
            "api_query_template": {
                "url": "https://{domain}/api/3/action/package_show",
                "query_params": {
                    "id": "{package_id}",
                },
            },
            "future_probe_hint": {
                "method": "GET_LIGHT",
                "expected_status": [200],
                "notes": "Probe package_show and inspect resource entries before any downstream acquisition.",
            },
            "validation_notes": [
                "Validate package metadata and each resource URL before treating any resource as usable.",
                "CKAN package metadata can contain stale, indirect, or access-controlled resources.",
            ],
        },
    ]
    return {
        "platform_package_id": PACKAGE_ID,
        "package_type": "platform_tool",
        "finality": "not_final",
        "consumer_authority": "none",
        "input": {
            "need_id": need_id,
            "url": url,
            "query": query,
        },
        "parsed": parsed,
        "resource_hints": resource_hints,
        "positive_evidence": [
            {
                "type": "platform_parse",
                "message": "CKAN portal domain and package slug were parsed from the supplied URL.",
            }
        ],
        "negative_evidence": [],
        "source_skill_usage": {
            "allowed_context": "Tools/Scripts Used",
            "can_decide_research_fit": False,
            "message": "A SourceSkill may use CKAN mechanics after deciding source-family fit.",
        },
    }


def parse_ckan_url(url: str) -> dict[str, str]:
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise ValueError("CKAN URL must be an absolute http(s) URL")
    parts = [part for part in parsed.path.split("/") if part]
    package_id = ""
    if "dataset" in parts:
        index = parts.index("dataset")
        if len(parts) > index + 1:
            package_id = parts[index + 1]
    if not package_id:
        package_id = parts[-1] if parts else ""
    if not package_id:
        raise ValueError("CKAN URL must include a dataset/package slug")
    return {
        "kind": "ckan_package",
        "domain": parsed.netloc.lower(),
        "id": package_id,
        "input_url": url,
    }


if __name__ == "__main__":
    main()
