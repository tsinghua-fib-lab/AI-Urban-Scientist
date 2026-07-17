from __future__ import annotations

import argparse
import json
from urllib.parse import parse_qs, quote_plus, urlparse


PACKAGE_ID = "dataverse_platform"
REQUIRED_VALIDATION = ["resolver", "probe", "download", "verifier"]


def main() -> None:
    parser = argparse.ArgumentParser(description="Emit not-final Dataverse platform hints.")
    parser.add_argument("--need-id", required=True)
    parser.add_argument("--url", required=True)
    parser.add_argument("--query", default="")
    args = parser.parse_args()

    payload = build_payload(need_id=args.need_id, url=args.url, query=args.query)
    print(json.dumps(payload, indent=2, sort_keys=True))


def build_payload(*, need_id: str, url: str, query: str) -> dict[str, object]:
    parsed = parse_dataverse_url(url)
    encoded_id = quote_plus(parsed["id"])
    resource_hints = [
        {
            "role": "dataset_api",
            "url": f"https://{parsed['domain']}/api/datasets/:persistentId/?persistentId={encoded_id}",
            "access_method": "dataverse_dataset_metadata",
            "need_ids": [need_id],
            "required_validation": REQUIRED_VALIDATION,
            "finality": "not_final",
            "consumer_authority": "none",
            "executability_hint": "resolvable_resource",
            "required_params": ["domain", "persistent_id"],
            "missing_params": [],
            "resolver_hint": {
                "resolver_family": "dataverse_persistent_id",
                "persistent_id": parsed["id"],
                "target_executability_hint": "resolvable_resource",
            },
            "api_query_template": {
                "url": "https://{domain}/api/datasets/:persistentId/",
                "query_params": {
                    "persistentId": "{persistent_id}",
                },
            },
            "future_probe_hint": {
                "method": "GET_LIGHT",
                "expected_status": [200],
                "notes": "Probe dataset metadata before inspecting versions or file listings.",
            },
            "validation_notes": [
                "Validate dataset identity, version, citation metadata, terms, and access status.",
                "Dataset metadata is not a final file resource.",
            ],
        },
        {
            "role": "file_listing_api",
            "url": f"https://{parsed['domain']}/api/datasets/:persistentId/versions/:latest/files?persistentId={encoded_id}",
            "access_method": "dataverse_file_listing",
            "need_ids": [need_id],
            "required_validation": REQUIRED_VALIDATION,
            "finality": "not_final",
            "consumer_authority": "none",
            "executability_hint": "resolvable_resource",
            "required_params": ["domain", "persistent_id"],
            "missing_params": [],
            "resolver_hint": {
                "resolver_family": "dataverse_file_listing",
                "persistent_id": parsed["id"],
                "target_executability_hint": "resolvable_resource",
                "requires_file_selection": True,
            },
            "api_query_template": {
                "url": "https://{domain}/api/datasets/:persistentId/versions/:latest/files",
                "query_params": {
                    "persistentId": "{persistent_id}",
                },
            },
            "future_probe_hint": {
                "method": "GET_LIGHT",
                "expected_status": [200],
                "notes": "Probe file listing and validate file-level metadata before acquisition.",
            },
            "validation_notes": [
                "Validate file count, formats, checksums, restricted-file status, and selected version.",
                "Do not pick files without SourceSkill or route-runner fit validation.",
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
                "message": "Dataverse domain and persistent id were parsed from the supplied URL.",
            }
        ],
        "negative_evidence": [],
        "source_skill_usage": {
            "allowed_context": "Tools/Scripts Used",
            "can_decide_research_fit": False,
            "message": "A SourceSkill may use Dataverse mechanics after deciding source-family fit.",
        },
    }


def parse_dataverse_url(url: str) -> dict[str, str]:
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise ValueError("Dataverse URL must be an absolute http(s) URL")
    query = parse_qs(parsed.query)
    persistent_id = (query.get("persistentId") or query.get("persistentid") or [""])[0]
    if not persistent_id:
        parts = [part for part in parsed.path.split("/") if part]
        persistent_id = next((part for part in parts if part.startswith("doi:")), "")
    if not persistent_id:
        raise ValueError("Dataverse URL must include a persistentId or DOI")
    return {
        "kind": "dataverse_dataset",
        "domain": parsed.netloc.lower(),
        "id": persistent_id,
        "input_url": url,
    }


if __name__ == "__main__":
    main()
