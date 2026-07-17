from __future__ import annotations

import argparse
import json
from urllib.parse import urlencode, urlparse


PACKAGE_ID = "stac_platform"
REQUIRED_VALIDATION = ["resolver", "probe", "download", "verifier"]


def main() -> None:
    parser = argparse.ArgumentParser(description="Emit not-final STAC platform hints.")
    parser.add_argument("--need-id", required=True)
    parser.add_argument("--url", required=True)
    parser.add_argument("--collection", default="")
    parser.add_argument("--bbox", default="")
    parser.add_argument("--datetime", default="")
    parser.add_argument("--query", default="")
    args = parser.parse_args()

    payload = build_payload(
        need_id=args.need_id,
        url=args.url,
        collection=args.collection,
        bbox=args.bbox,
        datetime_value=args.datetime,
        query=args.query,
    )
    print(json.dumps(payload, indent=2, sort_keys=True))


def build_payload(
    *,
    need_id: str,
    url: str,
    collection: str,
    bbox: str,
    datetime_value: str,
    query: str,
) -> dict[str, object]:
    parsed = parse_stac_url(url, collection=collection)
    collection_id = parsed["id"] if parsed["id"] else collection
    missing_params = [] if collection_id else ["collection"]
    resource_hints = [
        {
            "role": "catalog_metadata",
            "url": parsed["catalog_url"],
            "access_method": "stac_catalog_metadata",
            "need_ids": [need_id],
            "required_validation": REQUIRED_VALIDATION,
            "finality": "not_final",
            "consumer_authority": "none",
            "executability_hint": "source_landing",
            "required_params": ["catalog_url"],
            "missing_params": [],
            "resolver_hint": {
                "resolver_family": "stac_catalog",
                "target_executability_hint": "resolvable_resource",
            },
            "future_probe_hint": {
                "method": "GET_LIGHT",
                "expected_status": [200],
                "notes": "Probe catalog conformance and links before collection or item search.",
            },
            "validation_notes": [
                "Catalog metadata is a landing hint, not a data resource.",
                "Validate STAC conformance classes and collection links downstream.",
            ],
        },
        {
            "role": "collection_metadata",
            "url": build_collection_url(parsed["catalog_url"], collection_id),
            "access_method": "stac_collection_metadata",
            "need_ids": [need_id],
            "required_validation": REQUIRED_VALIDATION,
            "finality": "not_final",
            "consumer_authority": "none",
            "executability_hint": "resolvable_resource" if collection_id else "source_landing",
            "required_params": ["catalog_url", "collection"],
            "missing_params": missing_params,
            "resolver_hint": {
                "resolver_family": "stac_collection",
                "collection_id": collection_id,
                "target_executability_hint": "resolvable_resource",
            },
            "future_probe_hint": {
                "method": "GET_LIGHT",
                "expected_status": [200],
                "notes": "Probe collection metadata for extent, license, summaries, and asset descriptions.",
            },
            "validation_notes": [
                "Collection metadata must be checked for spatial/temporal extent and asset roles.",
            ],
        },
        {
            "role": "item_search",
            "url": build_search_url(parsed["catalog_url"], collection_id, bbox, datetime_value, limit="10"),
            "access_method": "stac_item_search",
            "need_ids": [need_id],
            "required_validation": REQUIRED_VALIDATION,
            "finality": "not_final",
            "consumer_authority": "none",
            "executability_hint": "resolvable_resource" if collection_id else "source_landing",
            "needs_follow_up": True,
            "follow_up_reason": "stac_item_search_requires_conformance_and_asset_validation",
            "required_params": ["catalog_url", "collection"],
            "missing_params": missing_params,
            "requestability_conditions": [
                "catalog advertises item-search conformance or endpoint",
                "collection exists and extent overlaps requested geography/time",
                "item response has no API error payload",
                "asset roles and media types match downstream needs",
            ],
            "resolver_hint": {
                "resolver_family": "stac_item_search",
                "collection_id": collection_id,
                "bbox": bbox,
                "datetime": datetime_value,
                "target_executability_hint": "resolvable_resource",
            },
            "api_query_template": {
                "url": f"{parsed['catalog_url']}/search",
                "query_params": {
                    "collections": "{collection}",
                    "bbox": "{bbox}",
                    "datetime": "{datetime}",
                    "limit": "{limit}",
                },
            },
            "future_probe_hint": {
                "method": "GET_LIGHT",
                "expected_status": [200],
                "notes": "Use a capped item search; do not download assets until a downstream policy allows it.",
            },
            "validation_notes": [
                "Validate item count, pagination, asset hrefs, asset roles, CRS, and licensing.",
                "Cloud asset access may require signed URLs or provider-specific auth.",
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
            "collection": collection,
            "bbox": bbox,
            "datetime": datetime_value,
            "query": query,
        },
        "parsed": parsed,
        "resource_hints": resource_hints,
        "positive_evidence": [
            {
                "type": "platform_parse",
                "message": "STAC catalog root and collection id were parsed from the supplied inputs.",
            }
        ],
        "negative_evidence": [],
        "source_skill_usage": {
            "allowed_context": "Tools/Scripts Used",
            "can_decide_research_fit": False,
            "message": "A SourceSkill may use STAC mechanics after deciding source-family fit.",
        },
    }


def parse_stac_url(url: str, *, collection: str = "") -> dict[str, str]:
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise ValueError("STAC URL must be an absolute http(s) URL")
    path = parsed.path.rstrip("/")
    parts = [part for part in path.split("/") if part]
    collection_id = collection
    if "collections" in parts:
        index = parts.index("collections")
        if len(parts) > index + 1:
            collection_id = collection_id or parts[index + 1]
        path = "/" + "/".join(parts[:index])
    if path.endswith("/search"):
        path = path[: -len("/search")]
    catalog_url = f"{parsed.scheme}://{parsed.netloc}{path}".rstrip("/")
    return {
        "kind": "stac_collection" if collection_id else "stac_catalog",
        "domain": parsed.netloc.lower(),
        "id": collection_id,
        "catalog_url": catalog_url,
        "input_url": url,
    }


def build_collection_url(catalog_url: str, collection: str) -> str:
    return f"{catalog_url}/collections/{collection}" if collection else f"{catalog_url}/collections"


def build_search_url(catalog_url: str, collection: str, bbox: str, datetime_value: str, *, limit: str) -> str:
    params: dict[str, str] = {"limit": limit}
    if collection:
        params["collections"] = collection
    if bbox:
        params["bbox"] = bbox
    if datetime_value:
        params["datetime"] = datetime_value
    return f"{catalog_url}/search?{urlencode(params)}"


if __name__ == "__main__":
    main()
