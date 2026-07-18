from __future__ import annotations

import argparse
import json
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

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
class ApiPayloadConfig:
    source_skill_id: str
    publisher: str
    metadata_url: str
    sample_filename: str
    payload_label: str
    result_path: tuple[str | int, ...] | None
    required_item_keys: tuple[str, ...] = ()
    required_top_level_keys: tuple[str, ...] = ()
    min_items: int = 1
    used_platform_tools: tuple[str, ...] = field(default_factory=tuple)
    credential_required: bool = False
    credential_label: str = "credential"
    credential_env_var: str | None = None
    credential_header_name: str | None = None
    credential_query_param: str | None = None


def classify_api_payload(config: ApiPayloadConfig, payload: Any) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    items = _extract_items(payload, config.result_path)
    first_item = items[0] if items else None
    top_keys_ok = isinstance(payload, dict) and all(key in payload for key in config.required_top_level_keys)
    if not config.required_top_level_keys:
        top_keys_ok = isinstance(payload, (dict, list))
    item_keys_ok = isinstance(first_item, dict) and all(_field_present(first_item, key) for key in config.required_item_keys)
    if not config.required_item_keys:
        item_keys_ok = bool(items)
    checks = [
        validation_check("payload_shape", isinstance(payload, (dict, list))),
        validation_check("top_level_keys", top_keys_ok, required_keys=list(config.required_top_level_keys)),
        validation_check("result_collection_present", len(items) >= config.min_items, result_count=len(items), min_items=config.min_items),
        validation_check("sample_item_keys", item_keys_ok, required_keys=list(config.required_item_keys)),
    ]
    passed = all(check["passed"] for check in checks)
    result = {
        "status": "probe_requestable" if passed else "needs_follow_up",
        "reason": f"{config.source_skill_id}_{config.payload_label}_shape_ok" if passed else f"{config.source_skill_id}_{config.payload_label}_shape_incomplete",
        "result_count": len(items),
    }
    return result, checks


def run_probe_cli(config: ApiPayloadConfig) -> None:
    parser = argparse.ArgumentParser(description=f"Probe a {config.source_skill_id} {config.payload_label} response.")
    parser.add_argument("--policy", default="discovery_only")
    parser.add_argument("--fixture-response")
    parser.add_argument("--url", default="")
    _add_credential_args(parser, config)
    args = parser.parse_args()
    credential = _resolve_credential(args, config)
    input_payload = {
        "fixture_response": bool(args.fixture_response),
        "url": args.url,
        "download_mode": fetch_mode(args.policy),
        "credential_required": config.credential_required,
        "credential_supplied": bool(credential),
        "credential_location": _credential_location(config),
    }
    provenance = {"source_url": args.url, "metadata_url": config.metadata_url, "publisher": config.publisher}
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
    if _credential_missing_for_live_request(args.fixture_response, args.url, config, credential):
        _print(
            fail_closed_result(
                source_skill_id=config.source_skill_id,
                tool_type="probe",
                policy=args.policy,
                input_payload=input_payload,
                reason=f"{config.credential_label}_required_for_live_request",
                provenance=provenance,
                used_platform_tools=list(config.used_platform_tools),
            )
        )
        return
    try:
        payload = _load_json(config, args.fixture_response, args.url, credential=credential)
        result, checks = classify_api_payload(config, payload)
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


def run_fetch_cli(config: ApiPayloadConfig) -> None:
    parser = argparse.ArgumentParser(description=f"Fetch a capped {config.source_skill_id} {config.payload_label} sample.")
    parser.add_argument("--policy", default="discovery_only")
    parser.add_argument("--fixture-response")
    parser.add_argument("--url", default="")
    parser.add_argument("--output-dir", required=True)
    _add_credential_args(parser, config)
    args = parser.parse_args()
    credential = _resolve_credential(args, config)
    input_payload = {
        "fixture_response": bool(args.fixture_response),
        "url": args.url,
        "credential_required": config.credential_required,
        "credential_supplied": bool(credential),
        "credential_location": _credential_location(config),
    }
    provenance = {"source_url": args.url, "metadata_url": config.metadata_url, "publisher": config.publisher}
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
    if _credential_missing_for_live_request(args.fixture_response, args.url, config, credential):
        _print(
            fail_closed_result(
                source_skill_id=config.source_skill_id,
                tool_type="fetch",
                policy=args.policy,
                input_payload=input_payload,
                reason=f"{config.credential_label}_required_for_live_request",
                provenance=provenance,
                used_platform_tools=list(config.used_platform_tools),
            )
        )
        return
    try:
        payload = _load_json(config, args.fixture_response, args.url, credential=credential)
        probe_result, checks = classify_api_payload(config, payload)
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


def run_validate_cli(config: ApiPayloadConfig) -> None:
    parser = argparse.ArgumentParser(description=f"Validate a {config.source_skill_id} {config.payload_label} sample.")
    parser.add_argument("--policy", default="discovery_only")
    parser.add_argument("--input-file", required=True)
    args = parser.parse_args()
    input_payload = {"input_file": args.input_file}
    provenance = {"source_url": "", "metadata_url": config.metadata_url, "publisher": config.publisher}
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
        payload = read_json_file(args.input_file)
        probe_result, checks = classify_api_payload(config, payload)
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


def _load_json(config: ApiPayloadConfig, fixture_response: str | None, url: str, *, credential: str | None = None) -> Any:
    if fixture_response:
        return read_json_file(fixture_response)
    live_url, headers = _authenticated_request_parts(config, url, credential=credential)
    return json.loads(fetch_text_with_live_gate(live_url, headers=headers))


def _add_credential_args(parser: argparse.ArgumentParser, config: ApiPayloadConfig) -> None:
    help_suffix = ""
    if config.credential_env_var:
        help_suffix = f" Defaults to ${config.credential_env_var} when unset."
    parser.add_argument("--credential", default="", help=f"{config.credential_label} for live requests.{help_suffix}")
    parser.add_argument("--api-key", default="", help="Alias for --credential when the source uses an API key.")
    parser.add_argument("--token", default="", help="Alias for --credential when the source uses a token.")


def _resolve_credential(args: argparse.Namespace, config: ApiPayloadConfig) -> str | None:
    value = (args.credential or args.api_key or args.token or "").strip()
    if value:
        return value
    if config.credential_env_var:
        env_value = os.environ.get(config.credential_env_var, "").strip()
        if env_value:
            return env_value
    return None


def _credential_location(config: ApiPayloadConfig) -> str:
    if config.credential_header_name:
        return f"header:{config.credential_header_name}"
    if config.credential_query_param:
        return f"query:{config.credential_query_param}"
    return "none"


def _credential_missing_for_live_request(
    fixture_response: str | None,
    url: str,
    config: ApiPayloadConfig,
    credential: str | None,
) -> bool:
    return bool(config.credential_required and not fixture_response and url and not credential)


def _authenticated_request_parts(
    config: ApiPayloadConfig,
    url: str,
    *,
    credential: str | None,
) -> tuple[str, dict[str, str]]:
    headers: dict[str, str] = {}
    live_url = url
    if not credential:
        return live_url, headers
    if config.credential_header_name:
        headers[config.credential_header_name] = credential
    if config.credential_query_param:
        live_url = _with_query_param(url, config.credential_query_param, credential)
    return live_url, headers


def _with_query_param(url: str, key: str, value: str) -> str:
    parts = urlsplit(url)
    query = [(k, v) for k, v in parse_qsl(parts.query, keep_blank_values=True) if k != key]
    query.append((key, value))
    return urlunsplit((parts.scheme, parts.netloc, parts.path, urlencode(query), parts.fragment))


def _extract_items(payload: Any, path: tuple[str | int, ...] | None) -> list[Any]:
    cursor = payload
    if path is not None:
        for key in path:
            if isinstance(key, int):
                if not isinstance(cursor, list) or key >= len(cursor):
                    return []
                cursor = cursor[key]
            else:
                if not isinstance(cursor, dict) or key not in cursor:
                    return []
                cursor = cursor[key]
    if isinstance(cursor, list):
        return cursor
    if isinstance(cursor, dict):
        return [cursor]
    return []


def _field_present(item: dict[str, Any], dotted_key: str) -> bool:
    cursor: Any = item
    for part in dotted_key.split("."):
        if not isinstance(cursor, dict) or part not in cursor:
            return False
        cursor = cursor[part]
    return True


def _print(payload: dict[str, Any]) -> None:
    print(json.dumps(payload, indent=2, sort_keys=True))
