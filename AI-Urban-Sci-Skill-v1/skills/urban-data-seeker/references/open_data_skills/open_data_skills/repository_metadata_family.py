from __future__ import annotations

import argparse
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any
from urllib.parse import urlencode

from .lint_contract import assert_lint_clean
from .route_bridge import build_dossier_fragment, build_resource_intents
from .tool_contract import (
    build_tool_result,
    fail_closed_result,
    fetch_mode,
    fetch_text_with_live_gate,
    policy_allows,
    policy_reason,
    read_json_file,
    validation_check,
    write_json_fetch_artifact,
    write_json_sample,
)


@dataclass(frozen=True)
class RepositoryMetadataConfig:
    source_skill_id: str
    source_card_id: str
    publisher: str
    landing_url: str
    docs_url: str
    search_url: str
    source_family: str
    resolver_family: str
    entity_label: str
    route_description: str
    result_path: tuple[str, ...] | None
    required_item_keys: tuple[str, ...]
    sample_filename: str
    access_method: str = "metadata_api_search"
    access_status: str = "open"
    authorization_required: bool = False
    authorization_param: str = "authorization"
    not_open_download: bool = False
    search_http_method: str = "GET"
    default_executability_hint: str = "resolvable_resource"
    follow_up_reason: str = "metadata_validation_required"
    used_platform_tools: tuple[str, ...] = ()
    query_params: tuple[tuple[str, str], ...] = field(default_factory=tuple)
    required_inputs: tuple[str, ...] = ("query",)
    body_template: dict[str, Any] | None = None
    validation_notes: tuple[str, ...] = field(default_factory=tuple)
    requestability_conditions: tuple[str, ...] = field(default_factory=tuple)


def build_repository_payload(
    config: RepositoryMetadataConfig,
    *,
    need_id: str,
    need_text: str,
    query: str,
    geography: str,
    time_range: str,
) -> dict[str, Any]:
    missing_params = _missing_params_with_values(
        config,
        values={"query": query, "geography": geography, "time_range": time_range},
    )
    primary_url = _build_primary_url(config, query=query, geography=geography, time_range=time_range)
    executability_hint = _executability_hint(config, missing_params=missing_params)
    follow_up_reason = _follow_up_reason(config, missing_params=missing_params)

    primary_resource = {
        "url": primary_url,
        "role": "primary",
        "access_method": config.access_method,
        "need_ids": [need_id],
        "source_skill_id": config.source_skill_id,
        "source_card_id": config.source_card_id,
        "description": config.route_description,
        "publisher": config.publisher,
        "metadata_url": config.docs_url,
        "executability_hint": executability_hint,
        "required_params": list(config.required_inputs),
        "missing_params": missing_params,
        "needs_follow_up": True,
        "follow_up_reason": follow_up_reason,
        "resolver_hint": {
            "resolver_family": config.resolver_family,
            "source_family": config.source_family,
            "entity_label": config.entity_label,
            "search_http_method": config.search_http_method,
            "access_status": config.access_status,
            "authorization_required": config.authorization_required,
            "query": query,
            "geography": geography,
            "time_range": time_range,
        },
        "api_query_template": _api_query_template(config),
        "future_probe_hint": {
            "method": "METADATA_ONLY",
            "expected_status": [200],
            "notes": "Probe official metadata responses or validated fixtures before downstream acquisition.",
        },
        "requestability_conditions": list(_requestability_conditions(config)),
        "validation_notes": list(_validation_notes(config)),
        "source_metadata": {
            "parser": f"{config.source_skill_id}_metadata_v1",
            "parser_state": "parsed_not_validated",
            "source_family": config.source_family,
            "query": query,
            "geography": geography,
            "time_range": time_range,
            "platform_mechanics": f"{config.search_http_method.lower()}_metadata_search",
            "validation_required": ["metadata_parser", "resolver", "probe", "verifier"],
        },
    }

    candidate_resources = [primary_resource]
    secondary_url = config.docs_url if config.docs_url != primary_url else config.landing_url
    if secondary_url and secondary_url != primary_url:
        candidate_resources.append(
            {
                "url": secondary_url,
                "role": "reference_docs",
                "access_method": "developer_docs",
                "need_ids": [need_id],
                "source_skill_id": config.source_skill_id,
                "source_card_id": config.source_card_id,
                "description": f"Official {config.entity_label} documentation or landing page.",
                "publisher": config.publisher,
                "executability_hint": "source_landing",
                "required_params": [],
                "missing_params": [],
                "needs_follow_up": True,
                "follow_up_reason": "documentation_requires_downstream_resolution",
                "validation_notes": [
                    "Developer documentation or landing pages are reference routes, not proof of file-level accessibility.",
                ],
            }
        )

    fragment = build_dossier_fragment(
        source_skill_id=config.source_skill_id,
        source_card_id=config.source_card_id,
        need_ids=[need_id],
        route_goal=f"Find {config.entity_label} metadata leads for: {need_text}",
        candidate_resources=candidate_resources,
        positive_evidence=[
            {
                "type": "source_prior",
                "message": f"Need matched the {config.entity_label} source family.",
                "query": query,
                "geography": geography,
                "time_range": time_range,
            }
        ],
        negative_evidence=_negative_evidence(config, missing_params=missing_params),
    )
    fragment["ambiguities"] = [
        "Record identity, version choice, DOI targeting, file availability, and reuse rights still require downstream validation.",
    ]
    fragment["verification_notes"] = list(primary_resource["validation_notes"])
    fragment["executability_hint"] = executability_hint
    payload = {
        "source_skill_id": config.source_skill_id,
        "source_card_id": config.source_card_id,
        "finality": "not_final",
        "consumer_authority": "none",
        "query": {
            "need_id": need_id,
            "need_text": need_text,
            "query": query,
            "geography": geography,
            "time_range": time_range,
            "missing_params": missing_params,
        },
        "candidate_resources": fragment["candidate_resources"],
        "route_dossier_fragment": fragment,
        "resource_intents": build_resource_intents(fragment),
    }
    assert_lint_clean(payload)
    return payload


def classify_repository_payload(
    config: RepositoryMetadataConfig,
    payload: Any,
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    payload_shape_ok = isinstance(payload, (dict, list))
    items = _extract_items(payload, config.result_path)
    first_item = items[0] if items else None
    item_keys_ok = isinstance(first_item, dict) and all(key in first_item for key in config.required_item_keys)
    checks = [
        validation_check("payload_shape", payload_shape_ok),
        validation_check("result_collection_present", len(items) > 0, result_count=len(items)),
        validation_check("sample_item_keys", item_keys_ok, required_keys=list(config.required_item_keys)),
    ]
    passed = all(check["passed"] for check in checks)
    result = {
        "status": "probe_requestable" if passed else "needs_follow_up",
        "reason": f"{config.source_skill_id}_metadata_shape_ok" if passed else f"{config.source_skill_id}_metadata_shape_incomplete",
        "result_count": len(items),
    }
    return result, checks


def run_find_cli(config: RepositoryMetadataConfig, build_payload_fn) -> None:
    parser = argparse.ArgumentParser(description=f"Emit not-final {config.entity_label} source hints.")
    parser.add_argument("--need-id", required=True)
    parser.add_argument("--need-text", required=True)
    parser.add_argument("--query", default="")
    parser.add_argument("--geography", default="")
    parser.add_argument("--time-range", default="")
    args = parser.parse_args()
    payload = build_payload_fn(
        need_id=args.need_id,
        need_text=args.need_text,
        query=args.query,
        geography=args.geography,
        time_range=args.time_range,
    )
    print(json.dumps(payload, indent=2, sort_keys=True))


def run_probe_cli(config: RepositoryMetadataConfig) -> None:
    parser = argparse.ArgumentParser(description=f"Probe a {config.entity_label} metadata response.")
    parser.add_argument("--policy", default="discovery_only")
    parser.add_argument("--fixture-response")
    parser.add_argument("--url", default="")
    args = parser.parse_args()
    input_payload = {"fixture_response": bool(args.fixture_response), "url": args.url, "download_mode": fetch_mode(args.policy)}
    provenance = {"source_url": args.url, "metadata_url": config.docs_url, "publisher": config.publisher}
    if not policy_allows(args.policy, "probe"):
        print(
            json.dumps(
                fail_closed_result(
                    source_skill_id=config.source_skill_id,
                    tool_type="probe",
                    policy=args.policy,
                    input_payload=input_payload,
                    reason=policy_reason(args.policy, "probe"),
                    provenance=provenance,
                    used_platform_tools=list(config.used_platform_tools),
                ),
                indent=2,
                sort_keys=True,
            )
        )
        return
    try:
        payload = read_json_file(args.fixture_response) if args.fixture_response else json.loads(fetch_text_with_live_gate(args.url))
        result, checks = classify_repository_payload(config, payload)
    except Exception as exc:
        result = {"status": "needs_follow_up", "reason": str(exc)}
        checks = [validation_check("probe_exception", False, reason=type(exc).__name__)]
    print(
        json.dumps(
            build_tool_result(
                source_skill_id=config.source_skill_id,
                tool_type="probe",
                policy=args.policy,
                input_payload=input_payload,
                result=result,
                provenance=provenance,
                validation={"checks": checks},
                used_platform_tools=list(config.used_platform_tools),
            ),
            indent=2,
            sort_keys=True,
        )
    )


def run_fetch_cli(config: RepositoryMetadataConfig) -> None:
    parser = argparse.ArgumentParser(description=f"Fetch a capped {config.entity_label} metadata sample.")
    parser.add_argument("--policy", default="discovery_only")
    parser.add_argument("--fixture-response")
    parser.add_argument("--url", default="")
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()
    input_payload = {"fixture_response": bool(args.fixture_response), "url": args.url}
    provenance = {"source_url": args.url, "metadata_url": config.docs_url, "publisher": config.publisher}
    if not policy_allows(args.policy, "fetch"):
        print(
            json.dumps(
                fail_closed_result(
                    source_skill_id=config.source_skill_id,
                    tool_type="fetch",
                    policy=args.policy,
                    input_payload=input_payload,
                    reason=policy_reason(args.policy, "fetch"),
                    provenance=provenance,
                    used_platform_tools=list(config.used_platform_tools),
                ),
                indent=2,
                sort_keys=True,
            )
        )
        return
    try:
        payload = read_json_file(args.fixture_response) if args.fixture_response else json.loads(fetch_text_with_live_gate(args.url))
        probe_result, checks = classify_repository_payload(config, payload)
        if probe_result["status"] != "probe_requestable":
            raise ValueError(str(probe_result["reason"]))
        artifact = write_json_fetch_artifact(Path(args.output_dir) / config.sample_filename, payload, policy=args.policy)
        checks.append(validation_check("sample_written", True))
        result = {"status": "fetched", "reason": probe_result["reason"]}
        artifacts = [artifact]
    except Exception as exc:
        result = {"status": "needs_follow_up", "reason": str(exc)}
        checks = [validation_check("fetch_exception", False, reason=type(exc).__name__)]
        artifacts = []
    print(
        json.dumps(
            build_tool_result(
                source_skill_id=config.source_skill_id,
                tool_type="fetch",
                policy=args.policy,
                input_payload=input_payload,
                result=result,
                provenance=provenance,
                artifacts=artifacts,
                validation={"checks": checks},
                used_platform_tools=list(config.used_platform_tools),
            ),
            indent=2,
            sort_keys=True,
        )
    )


def run_validate_cli(config: RepositoryMetadataConfig) -> None:
    parser = argparse.ArgumentParser(description=f"Validate a {config.entity_label} metadata sample.")
    parser.add_argument("--policy", default="discovery_only")
    parser.add_argument("--input-file", required=True)
    args = parser.parse_args()
    input_payload = {"input_file": args.input_file}
    provenance = {"source_url": "", "metadata_url": config.docs_url, "publisher": config.publisher}
    if not policy_allows(args.policy, "validate"):
        print(
            json.dumps(
                fail_closed_result(
                    source_skill_id=config.source_skill_id,
                    tool_type="validate",
                    policy=args.policy,
                    input_payload=input_payload,
                    reason=policy_reason(args.policy, "validate"),
                    provenance=provenance,
                    used_platform_tools=list(config.used_platform_tools),
                ),
                indent=2,
                sort_keys=True,
            )
        )
        return
    try:
        payload = read_json_file(args.input_file)
        probe_result, checks = classify_repository_payload(config, payload)
        result = {"status": "validation_passed" if probe_result["status"] == "probe_requestable" else "validation_failed"}
    except Exception as exc:
        result = {"status": "validation_failed", "reason": str(exc)}
        checks = [validation_check("validate_exception", False, reason=type(exc).__name__)]
    print(
        json.dumps(
            build_tool_result(
                source_skill_id=config.source_skill_id,
                tool_type="validate",
                policy=args.policy,
                input_payload=input_payload,
                result=result,
                provenance=provenance,
                validation={"checks": checks},
                used_platform_tools=list(config.used_platform_tools),
            ),
            indent=2,
            sort_keys=True,
        )
    )


def _build_primary_url(
    config: RepositoryMetadataConfig,
    *,
    query: str,
    geography: str,
    time_range: str,
) -> str:
    values = {"query": query, "geography": geography, "time_range": time_range}
    base_search_url = config.search_url
    for key, value in values.items():
        base_search_url = base_search_url.replace(f"{{{key}}}", value)
    if config.search_http_method != "GET":
        return config.docs_url if not any(token in config.search_url for token in ("{query}", "{geography}", "{time_range}")) else base_search_url
    params = []
    for key, value in config.query_params:
        rendered_value = value
        for template_key, template_value in values.items():
            rendered_value = rendered_value.replace(f"{{{template_key}}}", template_value)
        if rendered_value:
            params.append((key, rendered_value))
    if not params:
        return base_search_url
    return f"{base_search_url}?{urlencode(params)}"


def _api_query_template(config: RepositoryMetadataConfig) -> dict[str, Any]:
    if config.search_http_method == "GET":
        query_params: dict[str, Any] = {}
        for key, value in config.query_params:
            query_params[key] = value
        return {"method": "GET", "url": config.search_url, "query_params": query_params}
    payload: dict[str, Any] = {"method": config.search_http_method, "url": config.search_url}
    if config.body_template is not None:
        payload["json_body"] = config.body_template
    return payload


def _missing_params(config: RepositoryMetadataConfig, *, query: str) -> list[str]:
    return _missing_params_with_values(config, values={"query": query, "geography": "", "time_range": ""})


def _missing_params_with_values(config: RepositoryMetadataConfig, *, values: dict[str, str]) -> list[str]:
    missing = []
    for required_input in config.required_inputs:
        if not values.get(required_input, "").strip():
            missing.append(required_input)
    if config.authorization_required:
        missing.append(config.authorization_param)
    return missing


def _executability_hint(config: RepositoryMetadataConfig, *, missing_params: list[str]) -> str:
    if missing_params:
        return "needs_follow_up"
    if config.search_http_method != "GET":
        return "needs_follow_up"
    if config.not_open_download:
        return "source_landing"
    return config.default_executability_hint


def _follow_up_reason(config: RepositoryMetadataConfig, *, missing_params: list[str]) -> str:
    if missing_params:
        return f"{config.source_skill_id}_parameters_incomplete"
    if config.search_http_method != "GET":
        return f"{config.source_skill_id}_request_construction_required"
    return config.follow_up_reason


def _negative_evidence(config: RepositoryMetadataConfig, *, missing_params: list[str]) -> list[dict[str, Any]]:
    negative: list[dict[str, Any]] = []
    if missing_params:
        negative.append({"type": "missing_params", "missing_params": missing_params})
    if config.authorization_required or config.access_status in {"registration_required", "restricted", "paid", "application_required"}:
        negative.append(
            {
                "type": "access_constraint",
                "access_status": config.access_status,
                "message": "This SourceSkill cannot bypass account, license, or rate-limit requirements.",
            }
        )
    return negative


def _validation_notes(config: RepositoryMetadataConfig) -> tuple[str, ...]:
    if config.validation_notes:
        return config.validation_notes
    return (
        "Validate record identity, version choice, API freshness, and license before any acquisition flow.",
        "Do not treat metadata reachability as proof that underlying data files are downloadable or reusable.",
    )


def _requestability_conditions(config: RepositoryMetadataConfig) -> tuple[str, ...]:
    if config.requestability_conditions:
        return config.requestability_conditions
    return (
        "The query resolves to a concrete public record family.",
        "Downstream validation confirms version, DOI, and access rights.",
        "Any rate-limit or account requirements are satisfied under policy.",
    )


def _extract_items(payload: Any, path: tuple[str, ...] | None) -> list[Any]:
    if path is None:
        return payload if isinstance(payload, list) else []
    cursor = payload
    for key in path:
        if not isinstance(cursor, dict) or key not in cursor:
            return []
        cursor = cursor[key]
    if isinstance(cursor, list):
        return cursor
    if isinstance(cursor, dict):
        return [cursor]
    return []
