from __future__ import annotations

import argparse
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .lint_contract import assert_lint_clean
from .route_bridge import build_dossier_fragment, build_resource_intents
from .tool_contract import (
    build_tool_result,
    copy_capped_bytes,
    fail_closed_result,
    fetch_file_artifact,
    fetch_mode,
    fetch_bytes_with_live_gate,
    policy_allows,
    policy_reason,
    validation_check,
)


@dataclass(frozen=True)
class DirectFileConfig:
    source_skill_id: str
    source_card_id: str
    publisher: str
    landing_url: str
    docs_url: str
    url_template: str
    source_family: str
    resolver_family: str
    entity_label: str
    route_description: str
    sample_filename: str
    expected_suffixes: tuple[str, ...]
    expected_magic_prefixes: tuple[bytes, ...] = ()
    required_inputs: tuple[str, ...] = ()
    access_method: str = "direct_file_download"
    validation_notes: tuple[str, ...] = field(default_factory=tuple)


def build_direct_file_payload(
    config: DirectFileConfig,
    *,
    need_id: str,
    need_text: str,
    query: str,
    geography: str,
    time_range: str,
) -> dict[str, Any]:
    values = {"query": query, "geography": geography, "time_range": time_range}
    missing_params = [key for key in config.required_inputs if not values.get(key, "").strip()]
    url = _render_url(config.url_template, values)
    primary_resource = {
        "url": url,
        "role": "primary",
        "access_method": config.access_method,
        "need_ids": [need_id],
        "source_skill_id": config.source_skill_id,
        "source_card_id": config.source_card_id,
        "description": config.route_description,
        "publisher": config.publisher,
        "metadata_url": config.docs_url,
        "executability_hint": "needs_follow_up" if missing_params else "resolvable_resource",
        "required_params": list(config.required_inputs),
        "missing_params": missing_params,
        "needs_follow_up": True,
        "follow_up_reason": "direct_file_parameters_incomplete" if missing_params else "direct_file_probe_required",
        "resolver_hint": {
            "resolver_family": config.resolver_family,
            "source_family": config.source_family,
            "entity_label": config.entity_label,
            "search_http_method": "GET",
            "access_status": "open",
            "authorization_required": False,
            "query": query,
            "geography": geography,
            "time_range": time_range,
        },
        "api_query_template": {"method": "GET", "url": config.url_template, "query_params": {}},
        "future_probe_hint": {
            "method": "HEAD_OR_RANGE_GET",
            "expected_status": [200],
            "notes": "Probe suffix, content type, sample bytes, license, and archive contents before full acquisition.",
        },
        "requestability_conditions": [
            "All required URL template parameters are concrete.",
            "A capped probe confirms the expected direct-file shape.",
            "License and version are acceptable for the downstream use case.",
        ],
        "validation_notes": list(_validation_notes(config)),
        "source_metadata": {
            "parser": f"{config.source_skill_id}_direct_file_v1",
            "parser_state": "parsed_not_validated",
            "source_family": config.source_family,
            "query": query,
            "geography": geography,
            "time_range": time_range,
            "platform_mechanics": "direct_file_url_template",
            "validation_required": ["url_template", "probe", "archive_inspection", "license_check"],
        },
    }
    fragment = build_dossier_fragment(
        source_skill_id=config.source_skill_id,
        source_card_id=config.source_card_id,
        need_ids=[need_id],
        route_goal=f"Find {config.entity_label} direct files for: {need_text}",
        candidate_resources=[primary_resource],
        positive_evidence=[
            {
                "type": "source_prior",
                "message": f"Need matched the {config.entity_label} direct-file source family.",
                "query": query,
                "geography": geography,
                "time_range": time_range,
            }
        ],
        negative_evidence=[{"type": "missing_params", "missing_params": missing_params}] if missing_params else [],
    )
    fragment["ambiguities"] = [
        "Direct-file URL construction does not prove the file is the correct version, level, geometry type, or license for the task.",
    ]
    fragment["verification_notes"] = list(primary_resource["validation_notes"])
    fragment["executability_hint"] = primary_resource["executability_hint"]
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


def inspect_direct_file(config: DirectFileConfig, name: str, data: bytes) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    checks = [
        validation_check("file_non_empty", len(data) > 0, size_bytes=len(data)),
        validation_check("expected_suffix", any(name.lower().endswith(suffix) for suffix in config.expected_suffixes), expected_suffixes=list(config.expected_suffixes)),
    ]
    if name.lower().endswith(".zip"):
        checks.append(validation_check("zip_magic", data.startswith(b"PK")))
    if config.expected_magic_prefixes:
        checks.append(
            validation_check(
                "expected_magic_prefix",
                any(data.startswith(prefix) for prefix in config.expected_magic_prefixes),
                expected_prefixes=[prefix.hex() for prefix in config.expected_magic_prefixes],
            )
        )
    if name.lower().endswith((".json", ".geojson")):
        checks.append(validation_check("json_or_geojson_shape", data.lstrip().startswith(b"{") or data.lstrip().startswith(b"[")))
    passed = all(check["passed"] for check in checks)
    return {
        "status": "probe_requestable" if passed else "needs_follow_up",
        "reason": f"{config.source_skill_id}_direct_file_shape_ok" if passed else f"{config.source_skill_id}_direct_file_shape_incomplete",
        "size_bytes": len(data),
    }, checks


def run_find_cli(config: DirectFileConfig, build_payload_fn) -> None:
    parser = argparse.ArgumentParser(description=f"Emit not-final {config.entity_label} direct-file hints.")
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


def run_probe_cli(config: DirectFileConfig) -> None:
    parser = argparse.ArgumentParser(description=f"Probe a {config.entity_label} direct file sample.")
    parser.add_argument("--policy", default="discovery_only")
    parser.add_argument("--fixture-file")
    parser.add_argument("--url", default="")
    args = parser.parse_args()
    input_payload = {"fixture_file": bool(args.fixture_file), "url": args.url}
    provenance = {"source_url": args.url, "metadata_url": config.docs_url, "publisher": config.publisher}
    if not policy_allows(args.policy, "probe"):
        _print(fail_closed_result(source_skill_id=config.source_skill_id, tool_type="probe", policy=args.policy, input_payload=input_payload, reason=policy_reason(args.policy, "probe"), provenance=provenance))
        return
    try:
        name, data = _load_bytes(args.fixture_file, args.url)
        result, checks = inspect_direct_file(config, name, data)
    except Exception as exc:
        result = {"status": "needs_follow_up", "reason": str(exc)}
        checks = [validation_check("probe_exception", False, reason=type(exc).__name__)]
    _print(build_tool_result(source_skill_id=config.source_skill_id, tool_type="probe", policy=args.policy, input_payload=input_payload, result=result, provenance=provenance, validation={"checks": checks}))


def run_fetch_cli(config: DirectFileConfig) -> None:
    parser = argparse.ArgumentParser(description=f"Fetch a capped {config.entity_label} direct file sample.")
    parser.add_argument("--policy", default="discovery_only")
    parser.add_argument("--fixture-file")
    parser.add_argument("--url", default="")
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--max-bytes", type=int, default=1_000_000)
    args = parser.parse_args()
    input_payload = {"fixture_file": bool(args.fixture_file), "url": args.url, "max_bytes": args.max_bytes, "download_mode": fetch_mode(args.policy)}
    provenance = {"source_url": args.url, "metadata_url": config.docs_url, "publisher": config.publisher}
    if not policy_allows(args.policy, "fetch"):
        _print(fail_closed_result(source_skill_id=config.source_skill_id, tool_type="fetch", policy=args.policy, input_payload=input_payload, reason=policy_reason(args.policy, "fetch"), provenance=provenance))
        return
    try:
        target = Path(args.output_dir) / config.sample_filename
        artifact = fetch_file_artifact(
            fixture_file=args.fixture_file,
            url=args.url,
            target=target,
            policy=args.policy,
            max_bytes=args.max_bytes,
        )
        probe_result, checks = inspect_direct_file(config, target.name, target.read_bytes())
        checks.append(validation_check("sample_written", True))
        checks.append(
            validation_check(
                "fetch_scope",
                fetch_mode(args.policy) == "full" or target.stat().st_size <= args.max_bytes,
                download_mode=fetch_mode(args.policy),
                max_bytes=args.max_bytes,
            )
        )
        result = {"status": "fetched", "reason": probe_result["reason"]}
        artifacts = [artifact]
    except Exception as exc:
        result = {"status": "needs_follow_up", "reason": str(exc)}
        checks = [validation_check("fetch_exception", False, reason=type(exc).__name__)]
        artifacts = []
    _print(build_tool_result(source_skill_id=config.source_skill_id, tool_type="fetch", policy=args.policy, input_payload=input_payload, result=result, provenance=provenance, artifacts=artifacts, validation={"checks": checks}))


def run_validate_cli(config: DirectFileConfig) -> None:
    parser = argparse.ArgumentParser(description=f"Validate a {config.entity_label} direct file sample.")
    parser.add_argument("--policy", default="discovery_only")
    parser.add_argument("--input-file", required=True)
    args = parser.parse_args()
    input_payload = {"input_file": args.input_file}
    provenance = {"source_url": "", "metadata_url": config.docs_url, "publisher": config.publisher}
    if not policy_allows(args.policy, "validate"):
        _print(fail_closed_result(source_skill_id=config.source_skill_id, tool_type="validate", policy=args.policy, input_payload=input_payload, reason=policy_reason(args.policy, "validate"), provenance=provenance))
        return
    try:
        path = Path(args.input_file)
        probe_result, checks = inspect_direct_file(config, path.name, path.read_bytes())
        result = {"status": "validation_passed" if probe_result["status"] == "probe_requestable" else "validation_failed"}
    except Exception as exc:
        result = {"status": "validation_failed", "reason": str(exc)}
        checks = [validation_check("validate_exception", False, reason=type(exc).__name__)]
    _print(build_tool_result(source_skill_id=config.source_skill_id, tool_type="validate", policy=args.policy, input_payload=input_payload, result=result, provenance=provenance, validation={"checks": checks}))


def _load_bytes(fixture_file: str | None, url: str) -> tuple[str, bytes]:
    if fixture_file:
        path = Path(fixture_file)
        return path.name, path.read_bytes()
    return Path(url).name or "resource.dat", fetch_bytes_with_live_gate(url, max_bytes=1_000_000)


def _render_url(url_template: str, values: dict[str, str]) -> str:
    rendered = url_template
    for key, value in values.items():
        rendered = rendered.replace(f"{{{key}}}", value)
    return rendered


def _validation_notes(config: DirectFileConfig) -> tuple[str, ...]:
    if config.validation_notes:
        return config.validation_notes
    return (
        "Validate the selected file version, format, CRS, geometry level, license, and archive contents before final use.",
        "A direct URL template is not proof that the selected file satisfies the analytic need.",
    )


def _print(payload: dict[str, Any]) -> None:
    print(json.dumps(payload, indent=2, sort_keys=True))
