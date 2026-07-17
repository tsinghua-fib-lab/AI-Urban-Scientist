from __future__ import annotations

import argparse
import json
from urllib.parse import urlencode, urlparse


PACKAGE_ID = "arcgis_platform"
REQUIRED_VALIDATION = ["resolver", "probe", "download", "verifier"]


def main() -> None:
    parser = argparse.ArgumentParser(description="Emit not-final ArcGIS platform hints.")
    parser.add_argument("--need-id", required=True)
    parser.add_argument("--url", required=True)
    parser.add_argument("--query", default="")
    args = parser.parse_args()

    payload = build_payload(need_id=args.need_id, url=args.url, query=args.query)
    print(json.dumps(payload, indent=2, sort_keys=True))


def build_payload(*, need_id: str, url: str, query: str) -> dict[str, object]:
    parsed = parse_arcgis_url(url)
    query_url = build_query_url(parsed["service_url"], parsed.get("layer_id"))
    has_layer_id = bool(parsed.get("layer_id"))
    follow_up_reason = (
        "arcgis_query_requires_layer_metadata_and_error_payload_check"
        if has_layer_id
        else "arcgis_query_requires_layer_id"
    )
    resource_hints = [
        {
            "role": "query_json",
            "url": query_url,
            "metadata_url": (
                f"{parsed['service_url']}/{parsed['layer_id']}?f=pjson"
                if has_layer_id
                else f"{parsed['service_url']}?f=pjson"
            ),
            "access_method": "arcgis_rest_query",
            "need_ids": [need_id],
            "required_validation": REQUIRED_VALIDATION,
            "finality": "not_final",
            "consumer_authority": "none",
            "executability_hint": "resolvable_resource" if has_layer_id else "source_landing",
            "needs_follow_up": True,
            "follow_up_reason": follow_up_reason,
            "requires_layer_metadata": True,
            "required_params": ["service_url", "layer_id"],
            "missing_params": [] if has_layer_id else ["layer_id"],
            "requestability_conditions": [
                "service metadata confirms the layer id and query capability",
                "layer metadata says supportsQuery is true",
                "query response has no ArcGIS JSON error payload",
                "pagination and max record count are known before extraction",
            ],
            "probe_failure_policy": {
                "http_200_json_error_payload": "needs_follow_up",
                "missing_layer_metadata": "needs_follow_up",
                "pagination_unknown": "needs_follow_up",
            },
            "resolver_hint": {
                "resolver_family": "arcgis_feature_server_query",
                "target_executability_hint": "resolvable_resource",
                "requires_layer_metadata": True,
                "requires_pagination_check": True,
            },
            "api_query_template": {
                "url": f"{parsed['service_url']}/{{layer_id}}/query",
                "query_params": {
                    "where": "1=1",
                    "outFields": "*",
                    "f": "json",
                    "resultOffset": "{result_offset}",
                    "resultRecordCount": "{page_size}",
                },
            },
            "future_probe_hint": {
                "method": "GET_LIGHT",
                "expected_status": [200],
                "notes": (
                    "Probe layer query response, reject HTTP 200 JSON error payloads, and inspect "
                    "pagination metadata before any downstream acquisition."
                ),
            },
            "validation_notes": [
                "Validate layer id, geometry type, fields, and max record count before treating the query as executable.",
                "HTTP 200 is insufficient if the ArcGIS JSON response contains an error object.",
                "FeatureServer queries may require pagination for complete extraction.",
            ],
        },
        {
            "role": "service_metadata",
            "url": f"{parsed['service_url']}?f=pjson",
            "access_method": "arcgis_rest_metadata",
            "need_ids": [need_id],
            "required_validation": REQUIRED_VALIDATION,
            "finality": "not_final",
            "consumer_authority": "none",
            "executability_hint": "source_landing",
            "required_params": ["service_url"],
            "missing_params": [],
            "resolver_hint": {
                "resolver_family": "arcgis_service_metadata",
                "target_executability_hint": "resolvable_resource",
            },
            "future_probe_hint": {
                "method": "GET_LIGHT",
                "expected_status": [200],
                "notes": "Use metadata to choose a layer and pagination strategy; metadata alone is not a data resource.",
            },
            "validation_notes": [
                "Service metadata is a source landing/metadata hint, not an executable data resource.",
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
                "message": "ArcGIS service type, service name, and layer id were parsed from the supplied URL.",
            }
        ],
        "negative_evidence": [],
        "source_skill_usage": {
            "allowed_context": "Tools/Scripts Used",
            "can_decide_research_fit": False,
            "message": "A SourceSkill may use these mechanics, but must decide source-family suitability itself.",
        },
    }


def parse_arcgis_url(url: str) -> dict[str, str]:
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise ValueError("ArcGIS URL must be an absolute http(s) URL")
    parts = [part for part in parsed.path.split("/") if part]
    service_index = _find_service_index(parts)
    service_type = parts[service_index]
    service_name = parts[service_index - 1]
    service_path = "/" + "/".join(parts[: service_index + 1])
    layer_id = ""
    if len(parts) > service_index + 1 and parts[service_index + 1].isdigit():
        layer_id = parts[service_index + 1]
    return {
        "kind": "arcgis_layer",
        "domain": parsed.netloc.lower(),
        "id": service_name,
        "service_type": service_type,
        "layer_id": layer_id,
        "service_url": f"{parsed.scheme}://{parsed.netloc}{service_path}",
        "input_url": url,
    }


def build_query_url(service_url: str, layer_id: str | None) -> str:
    layer_path = f"{service_url}/{layer_id}" if layer_id else service_url
    query = urlencode(
        {
            "where": "1=1",
            "outFields": "*",
            "f": "json",
        }
    )
    return f"{layer_path}/query?{query}"


def classify_arcgis_query_probe_payload(payload: object) -> dict[str, object]:
    if not isinstance(payload, dict):
        return {
            "status": "needs_follow_up",
            "requestable": False,
            "requires_layer_metadata": True,
            "reason": "arcgis_probe_payload_not_object",
        }
    if isinstance(payload.get("error"), dict):
        return {
            "status": "needs_follow_up",
            "requestable": False,
            "requires_layer_metadata": True,
            "reason": "arcgis_json_error_payload",
        }
    if "features" in payload or "fields" in payload:
        return {
            "status": "probe_requestable",
            "requestable": True,
            "requires_layer_metadata": False,
            "reason": "arcgis_query_payload_has_data_shape",
        }
    return {
        "status": "needs_follow_up",
        "requestable": False,
        "requires_layer_metadata": True,
        "reason": "arcgis_query_payload_missing_data_shape",
    }


def _find_service_index(parts: list[str]) -> int:
    for index, part in enumerate(parts):
        if part in {"FeatureServer", "MapServer"}:
            if index == 0:
                raise ValueError("ArcGIS service URL must include a service name before service type")
            return index
    raise ValueError("ArcGIS URL must include FeatureServer or MapServer")


if __name__ == "__main__":
    main()
