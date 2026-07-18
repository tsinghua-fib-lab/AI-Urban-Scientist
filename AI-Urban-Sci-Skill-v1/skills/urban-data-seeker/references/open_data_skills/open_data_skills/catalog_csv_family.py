from __future__ import annotations

import argparse
import csv
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
class CatalogCsvConfig:
    source_skill_id: str
    source_card_id: str
    publisher: str
    landing_url: str
    docs_url: str
    catalog_url: str
    source_family: str
    resolver_family: str
    entity_label: str
    route_description: str
    sample_filename: str
    required_columns: tuple[str, ...]
    access_method: str = "catalog_csv_export"
    delimiter: str = ","
    required_inputs: tuple[str, ...] = ()
    validation_notes: tuple[str, ...] = field(default_factory=tuple)
    used_platform_tools: tuple[str, ...] = ()


def build_catalog_csv_payload(
    config: CatalogCsvConfig,
    *,
    need_id: str,
    need_text: str,
    query: str,
    geography: str,
    time_range: str,
) -> dict[str, Any]:
    missing_params = _missing_params(config, query=query, geography=geography, time_range=time_range)
    catalog_url = _render_url(config.catalog_url, query=query, geography=geography, time_range=time_range)
    primary_resource = {
        "url": catalog_url,
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
        "follow_up_reason": "catalog_export_parameters_incomplete" if missing_params else "catalog_export_requires_local_filtering",
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
        "api_query_template": {"method": "GET", "url": config.catalog_url, "query_params": {}},
        "future_probe_hint": {
            "method": "HEAD_OR_RANGE_GET",
            "expected_status": [200],
            "notes": "Probe a capped catalog export sample before resolving individual resource download URLs.",
        },
        "requestability_conditions": [
            "The public catalog export is reachable.",
            "Local filtering maps the user need to a concrete dataset row.",
            "The selected row exposes a usable resource download URL and license.",
        ],
        "validation_notes": list(_validation_notes(config)),
        "source_metadata": {
            "parser": f"{config.source_skill_id}_catalog_csv_v1",
            "parser_state": "parsed_not_validated",
            "source_family": config.source_family,
            "query": query,
            "geography": geography,
            "time_range": time_range,
            "platform_mechanics": "catalog_csv_export",
            "validation_required": ["csv_header_parser", "row_filter", "resource_url_probe", "license_check"],
        },
    }
    fragment = build_dossier_fragment(
        source_skill_id=config.source_skill_id,
        source_card_id=config.source_card_id,
        need_ids=[need_id],
        route_goal=f"Find {config.entity_label} catalog rows for: {need_text}",
        candidate_resources=[
            primary_resource,
            {
                "url": config.docs_url,
                "role": "reference_docs",
                "access_method": "developer_docs",
                "need_ids": [need_id],
                "source_skill_id": config.source_skill_id,
                "source_card_id": config.source_card_id,
                "description": f"Official {config.entity_label} metadata API documentation.",
                "publisher": config.publisher,
                "executability_hint": "source_landing",
                "required_params": [],
                "missing_params": [],
                "needs_follow_up": True,
                "follow_up_reason": "documentation_requires_downstream_resolution",
                "validation_notes": ["Documentation is not proof that row-level files are available or reusable."],
            },
        ],
        positive_evidence=[
            {
                "type": "source_prior",
                "message": f"Need matched the {config.entity_label} source family.",
                "query": query,
                "geography": geography,
                "time_range": time_range,
            }
        ],
        negative_evidence=[{"type": "missing_params", "missing_params": missing_params}] if missing_params else [],
    )
    fragment["ambiguities"] = [
        "The catalog export is a discovery index; selected rows still need row-level URL, format, freshness, and license checks.",
    ]
    fragment["verification_notes"] = list(primary_resource["validation_notes"])
    fragment["executability_hint"] = "needs_follow_up" if missing_params else "resolvable_resource"
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


def inspect_catalog_csv(config: CatalogCsvConfig, name: str, data: bytes) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    text = data.decode("utf-8-sig", errors="replace")
    reader = csv.DictReader(text.splitlines(), delimiter=config.delimiter)
    rows = list(reader)
    fieldnames = reader.fieldnames or []
    field_set = {field.strip() for field in fieldnames if field}
    checks = [
        validation_check("csv_shape", bool(field_set)),
        validation_check("rows_present", len(rows) > 0, row_count=len(rows)),
        validation_check("expected_suffix", name.lower().endswith(".csv"), expected_suffix=".csv"),
    ]
    for column in config.required_columns:
        checks.append(validation_check(f"column_present:{column}", column in field_set))
    passed = all(check["passed"] for check in checks)
    return {
        "status": "probe_requestable" if passed else "needs_follow_up",
        "reason": f"{config.source_skill_id}_catalog_csv_shape_ok" if passed else f"{config.source_skill_id}_catalog_csv_shape_incomplete",
        "row_count": len(rows),
    }, checks


def run_find_cli(config: CatalogCsvConfig, build_payload_fn) -> None:
    parser = argparse.ArgumentParser(description=f"Emit not-final {config.entity_label} catalog export hints.")
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


def run_probe_cli(config: CatalogCsvConfig) -> None:
    parser = argparse.ArgumentParser(description=f"Probe a {config.entity_label} catalog CSV export.")
    parser.add_argument("--policy", default="discovery_only")
    parser.add_argument("--fixture-file")
    parser.add_argument("--url", default="")
    args = parser.parse_args()
    input_payload = {"fixture_file": bool(args.fixture_file), "url": args.url}
    provenance = {"source_url": args.url, "metadata_url": config.docs_url, "publisher": config.publisher}
    if not policy_allows(args.policy, "probe"):
        _print(
            fail_closed_result(
                source_skill_id=config.source_skill_id,
                tool_type="probe",
                policy=args.policy,
                input_payload=input_payload,
                reason=policy_reason(args.policy, "probe"),
                provenance=provenance,
                used_platform_tools=list(config.used_platform_tools),
            )
        )
        return
    try:
        name, data = _load_csv_bytes(args.fixture_file, args.url)
        result, checks = inspect_catalog_csv(config, name, data)
    except Exception as exc:
        result = {"status": "needs_follow_up", "reason": str(exc)}
        checks = [validation_check("probe_exception", False, reason=type(exc).__name__)]
    _print(
        build_tool_result(
            source_skill_id=config.source_skill_id,
            tool_type="probe",
            policy=args.policy,
            input_payload=input_payload,
            result=result,
            provenance=provenance,
            validation={"checks": checks},
            used_platform_tools=list(config.used_platform_tools),
        )
    )


def run_fetch_cli(config: CatalogCsvConfig) -> None:
    parser = argparse.ArgumentParser(description=f"Fetch a capped {config.entity_label} catalog CSV sample.")
    parser.add_argument("--policy", default="discovery_only")
    parser.add_argument("--fixture-file")
    parser.add_argument("--url", default="")
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--max-bytes", type=int, default=1_000_000)
    args = parser.parse_args()
    input_payload = {"fixture_file": bool(args.fixture_file), "url": args.url, "max_bytes": args.max_bytes, "download_mode": fetch_mode(args.policy)}
    provenance = {"source_url": args.url, "metadata_url": config.docs_url, "publisher": config.publisher}
    if not policy_allows(args.policy, "fetch"):
        _print(
            fail_closed_result(
                source_skill_id=config.source_skill_id,
                tool_type="fetch",
                policy=args.policy,
                input_payload=input_payload,
                reason=policy_reason(args.policy, "fetch"),
                provenance=provenance,
                used_platform_tools=list(config.used_platform_tools),
            )
        )
        return
    try:
        target = Path(args.output_dir) / config.sample_filename
        artifact = fetch_file_artifact(
            fixture_file=args.fixture_file,
            url=args.url,
            target=target,
            policy=args.policy,
            max_bytes=args.max_bytes,
            artifact_format="csv",
        )
        result, checks = inspect_catalog_csv(config, target.name, target.read_bytes())
        if result["status"] != "probe_requestable":
            raise ValueError(result["reason"])
        checks.append(validation_check("sample_written", True))
        checks.append(
            validation_check(
                "fetch_scope",
                fetch_mode(args.policy) == "full" or target.stat().st_size <= args.max_bytes,
                download_mode=fetch_mode(args.policy),
                max_bytes=args.max_bytes,
            )
        )
        artifacts = [artifact]
        result = {"status": "fetched", "reason": result["reason"]}
    except Exception as exc:
        result = {"status": "needs_follow_up", "reason": str(exc)}
        checks = [validation_check("fetch_exception", False, reason=type(exc).__name__)]
        artifacts = []
    _print(
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
        )
    )


def run_validate_cli(config: CatalogCsvConfig) -> None:
    parser = argparse.ArgumentParser(description=f"Validate a {config.entity_label} catalog CSV sample.")
    parser.add_argument("--policy", default="discovery_only")
    parser.add_argument("--input-file", required=True)
    args = parser.parse_args()
    input_payload = {"input_file": args.input_file}
    provenance = {"source_url": "", "metadata_url": config.docs_url, "publisher": config.publisher}
    if not policy_allows(args.policy, "validate"):
        _print(
            fail_closed_result(
                source_skill_id=config.source_skill_id,
                tool_type="validate",
                policy=args.policy,
                input_payload=input_payload,
                reason=policy_reason(args.policy, "validate"),
                provenance=provenance,
                used_platform_tools=list(config.used_platform_tools),
            )
        )
        return
    try:
        path = Path(args.input_file)
        probe_result, checks = inspect_catalog_csv(config, path.name, path.read_bytes())
        result = {"status": "validation_passed" if probe_result["status"] == "probe_requestable" else "validation_failed"}
    except Exception as exc:
        result = {"status": "validation_failed", "reason": str(exc)}
        checks = [validation_check("validate_exception", False, reason=type(exc).__name__)]
    _print(
        build_tool_result(
            source_skill_id=config.source_skill_id,
            tool_type="validate",
            policy=args.policy,
            input_payload=input_payload,
            result=result,
            provenance=provenance,
            validation={"checks": checks},
            used_platform_tools=list(config.used_platform_tools),
        )
    )


def _load_csv_bytes(fixture_file: str | None, url: str) -> tuple[str, bytes]:
    if fixture_file:
        path = Path(fixture_file)
        return path.name, path.read_bytes()
    return Path(url).name or "catalog.csv", fetch_bytes_with_live_gate(url, max_bytes=1_000_000)


def _render_url(catalog_url: str, *, query: str, geography: str, time_range: str) -> str:
    values = {"query": query, "geography": geography, "time_range": time_range}
    rendered = catalog_url
    for key, value in values.items():
        rendered = rendered.replace(f"{{{key}}}", value)
    return rendered


def _missing_params(config: CatalogCsvConfig, *, query: str, geography: str, time_range: str) -> list[str]:
    values = {"query": query, "geography": geography, "time_range": time_range}
    return [required_input for required_input in config.required_inputs if not values.get(required_input, "").strip()]


def _validation_notes(config: CatalogCsvConfig) -> tuple[str, ...]:
    if config.validation_notes:
        return config.validation_notes
    return (
        "Validate row-level dataset identity, resource URL, format, freshness, and license before final download.",
        "Catalog exports are discovery metadata, not proof that linked files remain downloadable.",
    )


def _print(payload: dict[str, Any]) -> None:
    print(json.dumps(payload, indent=2, sort_keys=True))
