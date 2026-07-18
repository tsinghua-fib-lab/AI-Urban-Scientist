from __future__ import annotations

from typing import Any

from .lint_contract import assert_lint_clean


REQUIRED_VALIDATION = ["resolver", "probe", "download", "verifier"]
EXECUTABILITY_OPTIONAL_KEYS = [
    "executability_hint",
    "required_params",
    "missing_params",
    "resolver_hint",
    "api_query_template",
    "direct_file_pattern",
    "metadata_url",
    "source_metadata",
    "future_probe_hint",
    "needs_follow_up",
    "follow_up_reason",
    "requestability_conditions",
    "probe_failure_policy",
    "requires_layer_metadata",
    "supported_geography_examples",
    "validation_notes",
]


def build_dossier_fragment(
    *,
    source_skill_id: str,
    source_card_id: str,
    need_ids: list[str],
    route_goal: str,
    candidate_resources: list[dict[str, Any]],
    positive_evidence: list[dict[str, Any]],
    negative_evidence: list[dict[str, Any]],
) -> dict[str, Any]:
    fragment = {
        "route_id": _route_id(source_skill_id, source_card_id),
        "route_type": "source_skill",
        "route_goal": str(route_goal),
        "source_skill_id": str(source_skill_id),
        "source_card_id": str(source_card_id),
        "input_need_ids": [str(need_id) for need_id in need_ids],
        "tools_used": [f"source_skill:{source_skill_id}"],
        "candidate_resources": [
            _normalize_candidate_resource(resource) for resource in candidate_resources
        ],
        "positive_evidence": positive_evidence,
        "negative_evidence": negative_evidence,
        "finality": "not_final",
        "consumer_authority": "none",
    }
    assert_lint_clean(fragment)
    return fragment


def build_resource_intents(fragment: dict[str, Any]) -> list[dict[str, Any]]:
    intents: list[dict[str, Any]] = []
    for resource in fragment.get("candidate_resources", []):
        need_ids = resource.get("need_ids") or fragment.get("input_need_ids", [])
        for need_id in need_ids:
            intent = {
                "need_id": str(need_id),
                "source_route_id": str(fragment["route_id"]),
                "route_type": "source_skill",
                "resource_url": str(resource["url"]),
                "download_candidate": {
                    "url": str(resource["url"]),
                    "access_method": str(resource.get("access_method", "direct")),
                    "role": str(resource.get("role", "primary")),
                    "is_direct_download_candidate": _is_direct_download_candidate(resource),
                    "needs_follow_up": bool(resource.get("needs_follow_up", True)),
                    "missing_params": list(resource.get("missing_params", [])),
                    "policy_required_for_full_download": "fetch_full_allowed",
                },
                "role": str(resource.get("role", "primary")),
                "access_method": str(resource.get("access_method", "direct")),
                "why_sufficient": str(fragment.get("route_goal", "")),
                "required_validation": list(REQUIRED_VALIDATION),
                "finality": "not_final",
                "consumer_authority": "none",
            }
            for optional_key in EXECUTABILITY_OPTIONAL_KEYS:
                if optional_key in resource:
                    intent[optional_key] = resource[optional_key]
            assert_lint_clean(intent)
            intents.append(intent)
    return intents


def _normalize_candidate_resource(resource: dict[str, Any]) -> dict[str, Any]:
    normalized = {
        "url": str(resource["url"]),
        "role": str(resource.get("role", "primary")),
        "access_method": str(resource.get("access_method", "direct")),
        "download_candidate": {
            "url": str(resource["url"]),
            "access_method": str(resource.get("access_method", "direct")),
            "role": str(resource.get("role", "primary")),
            "is_direct_download_candidate": _is_direct_download_candidate(resource),
            "needs_follow_up": bool(resource.get("needs_follow_up", True)),
            "missing_params": list(resource.get("missing_params", [])),
            "policy_required_for_full_download": "fetch_full_allowed",
        },
        "need_ids": [str(need_id) for need_id in resource.get("need_ids", [])],
        "required_validation": list(REQUIRED_VALIDATION),
        "finality": "not_final",
        "consumer_authority": "none",
    }
    for optional_key in [
        "source_skill_id",
        "source_card_id",
        "description",
        "publisher",
        *EXECUTABILITY_OPTIONAL_KEYS,
    ]:
        if optional_key in resource:
            normalized[optional_key] = resource[optional_key]
    assert_lint_clean(normalized)
    return normalized


def _route_id(source_skill_id: str, source_card_id: str) -> str:
    return f"source_skill:{source_skill_id}:{source_card_id}"


def _is_direct_download_candidate(resource: dict[str, Any]) -> bool:
    access_method = str(resource.get("access_method", "")).lower()
    executability_hint = str(resource.get("executability_hint", "")).lower()
    missing_params = list(resource.get("missing_params", []))
    if missing_params:
        return False
    if resource.get("needs_follow_up") is True and "metadata" in access_method:
        return False
    return any(
        token in access_method
        for token in ("direct", "download", "file", "csv", "zip", "geojson", "parquet", "api")
    ) or executability_hint in {"resolvable_resource", "executable_resource_candidate"}
