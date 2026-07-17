from __future__ import annotations

import argparse
import json
from urllib.parse import quote, urlencode, urlparse


PACKAGE_ID = "odata_platform"
REQUIRED_VALIDATION = ["resolver", "probe", "download", "verifier"]


def main() -> None:
    parser = argparse.ArgumentParser(description="Emit not-final OData platform hints.")
    parser.add_argument("--need-id", required=True)
    parser.add_argument("--url", required=True)
    parser.add_argument("--entity-set", default="")
    parser.add_argument("--query", default="")
    args = parser.parse_args()

    payload = build_payload(need_id=args.need_id, url=args.url, entity_set=args.entity_set, query=args.query)
    print(json.dumps(payload, indent=2, sort_keys=True))


def build_payload(*, need_id: str, url: str, entity_set: str, query: str) -> dict[str, object]:
    parsed = parse_odata_url(url, entity_set=entity_set)
    missing_params = [] if parsed["id"] else ["entity_set"]
    resource_hints = [
        {
            "role": "service_document",
            "url": parsed["service_root"],
            "access_method": "odata_service_document",
            "need_ids": [need_id],
            "required_validation": REQUIRED_VALIDATION,
            "finality": "not_final",
            "consumer_authority": "none",
            "executability_hint": "source_landing",
            "required_params": ["service_root"],
            "missing_params": [],
            "resolver_hint": {
                "resolver_family": "odata_service_document",
                "target_executability_hint": "resolvable_resource",
            },
            "future_probe_hint": {
                "method": "GET_LIGHT",
                "expected_status": [200],
                "notes": "Probe service document for entity sets and version information.",
            },
            "validation_notes": [
                "Service documents are metadata hints, not data resources.",
            ],
        },
        {
            "role": "metadata_document",
            "url": f"{parsed['service_root']}/$metadata",
            "access_method": "odata_metadata_document",
            "need_ids": [need_id],
            "required_validation": REQUIRED_VALIDATION,
            "finality": "not_final",
            "consumer_authority": "none",
            "executability_hint": "source_landing",
            "required_params": ["service_root"],
            "missing_params": [],
            "resolver_hint": {
                "resolver_family": "odata_metadata",
                "target_executability_hint": "resolvable_resource",
            },
            "future_probe_hint": {
                "method": "GET_LIGHT",
                "expected_status": [200],
                "notes": "Probe metadata and validate entity sets, fields, keys, and OData version.",
            },
            "validation_notes": [
                "Metadata must be checked before building filters or selecting fields.",
            ],
        },
        {
            "role": "entity_query",
            "url": build_entity_query_url(parsed["service_root"], parsed["id"]),
            "access_method": "odata_entity_query",
            "need_ids": [need_id],
            "required_validation": REQUIRED_VALIDATION,
            "finality": "not_final",
            "consumer_authority": "none",
            "executability_hint": "resolvable_resource" if parsed["id"] else "source_landing",
            "needs_follow_up": True,
            "follow_up_reason": "odata_entity_query_requires_metadata_field_and_paging_validation",
            "required_params": ["service_root", "entity_set"],
            "missing_params": missing_params,
            "requestability_conditions": [
                "metadata confirms entity set name",
                "selected fields and filters are valid",
                "paging and service limits are known",
                "response is data, not an OData error payload",
            ],
            "resolver_hint": {
                "resolver_family": "odata_entity_query",
                "entity_set": parsed["id"],
                "target_executability_hint": "resolvable_resource",
            },
            "api_query_template": {
                "url": f"{parsed['service_root']}/{{entity_set}}",
                "query_params": {
                    "$top": "{limit}",
                    "$select": "{columns}",
                    "$filter": "{filter}",
                },
            },
            "future_probe_hint": {
                "method": "GET_LIGHT",
                "expected_status": [200],
                "notes": "Use a capped query and inspect OData error payloads before extraction.",
            },
            "validation_notes": [
                "Validate fields, filters, page tokens, and service version downstream.",
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
            "entity_set": entity_set,
            "query": query,
        },
        "parsed": parsed,
        "resource_hints": resource_hints,
        "positive_evidence": [
            {
                "type": "platform_parse",
                "message": "OData service root and entity set were parsed from the supplied inputs.",
            }
        ],
        "negative_evidence": [],
        "source_skill_usage": {
            "allowed_context": "Tools/Scripts Used",
            "can_decide_research_fit": False,
            "message": "A SourceSkill may use OData mechanics after deciding source-family fit.",
        },
    }


def parse_odata_url(url: str, *, entity_set: str = "") -> dict[str, str]:
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise ValueError("OData URL must be an absolute http(s) URL")
    path = parsed.path.rstrip("/")
    service_root = f"{parsed.scheme}://{parsed.netloc}{path}".rstrip("/")
    return {
        "kind": "odata_entity_set" if entity_set else "odata_service",
        "domain": parsed.netloc.lower(),
        "id": entity_set,
        "service_root": service_root,
        "input_url": url,
    }


def build_entity_query_url(service_root: str, entity_set: str) -> str:
    target = f"{service_root}/{quote(entity_set)}" if entity_set else service_root
    query = urlencode({"$top": "{limit}", "$select": "{columns}"})
    return f"{target}?{query}"


if __name__ == "__main__":
    main()
