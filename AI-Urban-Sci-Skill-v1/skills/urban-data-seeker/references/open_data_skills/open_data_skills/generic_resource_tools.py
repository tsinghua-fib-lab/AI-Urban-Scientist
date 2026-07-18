from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from open_data_skills.tool_contract import (
    build_tool_result,
    copy_capped_bytes,
    fail_closed_result,
    fetch_file_artifact,
    fetch_mode,
    fetch_text_with_live_gate,
    policy_allows,
    policy_reason,
    read_json_file,
    validation_check,
    write_json_fetch_artifact,
    write_json_sample,
)


def run_json_probe(
    *,
    source_skill_id: str,
    publisher: str,
    metadata_url: str = "",
    used_platform_tools: list[str] | None = None,
) -> None:
    parser = argparse.ArgumentParser(description=f"Probe a {source_skill_id} JSON/API response.")
    parser.add_argument("--policy", default="discovery_only")
    parser.add_argument("--fixture-response")
    parser.add_argument("--url", default="")
    parser.add_argument("--expected-field", action="append", default=[])
    args = parser.parse_args()
    input_payload = {
        "fixture_response": bool(args.fixture_response),
        "url": args.url,
        "expected_fields": list(args.expected_field),
    }
    provenance = {"source_url": args.url, "metadata_url": metadata_url, "publisher": publisher}
    if not policy_allows(args.policy, "probe"):
        _print(fail_closed_result(source_skill_id=source_skill_id, tool_type="probe", policy=args.policy, input_payload=input_payload, reason=policy_reason(args.policy, "probe"), provenance=provenance, used_platform_tools=used_platform_tools))
        return
    try:
        payload = _load_json(args.fixture_response, args.url)
        checks = _json_checks(payload, args.expected_field)
        result = {"status": "probe_requestable" if all(check["passed"] for check in checks) else "needs_follow_up", "record_count": _record_count(payload)}
    except Exception as exc:
        checks = [validation_check("probe_exception", False, reason=type(exc).__name__)]
        result = {"status": "needs_follow_up", "reason": str(exc)}
    _print(build_tool_result(source_skill_id=source_skill_id, tool_type="probe", policy=args.policy, input_payload=input_payload, result=result, provenance=provenance, validation={"checks": checks}, used_platform_tools=used_platform_tools))


def run_json_fetch(
    *,
    source_skill_id: str,
    publisher: str,
    metadata_url: str = "",
    used_platform_tools: list[str] | None = None,
    default_name: str = "sample.json",
) -> None:
    parser = argparse.ArgumentParser(description=f"Fetch a capped {source_skill_id} JSON/API sample.")
    parser.add_argument("--policy", default="discovery_only")
    parser.add_argument("--fixture-response")
    parser.add_argument("--url", default="")
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--max-records", type=int, default=100)
    args = parser.parse_args()
    input_payload = {
        "fixture_response": bool(args.fixture_response),
        "url": args.url,
        "max_records": args.max_records,
        "download_mode": fetch_mode(args.policy),
    }
    provenance = {"source_url": args.url, "metadata_url": metadata_url, "publisher": publisher}
    if not policy_allows(args.policy, "fetch"):
        _print(fail_closed_result(source_skill_id=source_skill_id, tool_type="fetch", policy=args.policy, input_payload=input_payload, reason=policy_reason(args.policy, "fetch"), provenance=provenance, used_platform_tools=used_platform_tools))
        return
    try:
        raw_payload = _load_json(args.fixture_response, args.url)
        payload = raw_payload if fetch_mode(args.policy) == "full" else _cap_json(raw_payload, args.max_records)
        artifact = write_json_fetch_artifact(Path(args.output_dir) / default_name, payload, policy=args.policy)
        checks = [
            validation_check("sample_written", True),
            validation_check(
                "fetch_scope",
                True,
                download_mode=fetch_mode(args.policy),
                max_records=args.max_records,
            ),
        ]
        result = {"status": "fetched", "record_count": _record_count(payload)}
        artifacts = [artifact]
    except Exception as exc:
        checks = [validation_check("fetch_exception", False, reason=type(exc).__name__)]
        result = {"status": "needs_follow_up", "reason": str(exc)}
        artifacts = []
    _print(build_tool_result(source_skill_id=source_skill_id, tool_type="fetch", policy=args.policy, input_payload=input_payload, result=result, provenance=provenance, artifacts=artifacts, validation={"checks": checks}, used_platform_tools=used_platform_tools))


def run_json_validate(
    *,
    source_skill_id: str,
    publisher: str,
    metadata_url: str = "",
    used_platform_tools: list[str] | None = None,
) -> None:
    parser = argparse.ArgumentParser(description=f"Validate a {source_skill_id} JSON/API sample.")
    parser.add_argument("--policy", default="discovery_only")
    parser.add_argument("--input-file", required=True)
    parser.add_argument("--expected-field", action="append", default=[])
    args = parser.parse_args()
    input_payload = {"input_file": args.input_file, "expected_fields": list(args.expected_field)}
    provenance = {"source_url": "", "metadata_url": metadata_url, "publisher": publisher}
    if not policy_allows(args.policy, "validate"):
        _print(fail_closed_result(source_skill_id=source_skill_id, tool_type="validate", policy=args.policy, input_payload=input_payload, reason=policy_reason(args.policy, "validate"), provenance=provenance, used_platform_tools=used_platform_tools))
        return
    try:
        payload = read_json_file(args.input_file)
        checks = _json_checks(payload, args.expected_field)
        result = {"status": "validation_passed" if all(check["passed"] for check in checks) else "validation_failed"}
    except Exception as exc:
        checks = [validation_check("validate_exception", False, reason=type(exc).__name__)]
        result = {"status": "validation_failed", "reason": str(exc)}
    _print(build_tool_result(source_skill_id=source_skill_id, tool_type="validate", policy=args.policy, input_payload=input_payload, result=result, provenance=provenance, validation={"checks": checks}, used_platform_tools=used_platform_tools))


def run_access_check(
    *,
    source_skill_id: str,
    publisher: str,
    metadata_url: str = "",
    access_status: str = "unknown",
    authorization_required: bool = False,
    not_open_download: bool = False,
    used_platform_tools: list[str] | None = None,
) -> None:
    parser = argparse.ArgumentParser(description=f"Check access constraints for {source_skill_id}.")
    parser.add_argument("--policy", default="discovery_only")
    parser.add_argument("--url", default="")
    parser.add_argument("--has-token", action="store_true")
    args = parser.parse_args()
    input_payload = {
        "url": args.url,
        "has_token": bool(args.has_token),
        "access_status": access_status,
        "authorization_required": authorization_required,
        "not_open_download": not_open_download,
    }
    blocked = not_open_download or authorization_required or access_status in {
        "paid",
        "restricted",
        "application_required",
        "registration_required",
    }
    token_missing = authorization_required and not args.has_token
    checks = [
        validation_check("declares_access_status", bool(access_status and access_status != "unknown"), access_status=access_status),
        validation_check("not_open_download_flag_checked", True, not_open_download=not_open_download),
        validation_check("authorization_requirement_checked", not token_missing, authorization_required=authorization_required),
    ]
    status = "needs_follow_up" if blocked or token_missing else "probe_requestable"
    reason = "access_or_license_follow_up_required" if blocked or token_missing else "public_metadata_or_api_route"
    provenance = {"source_url": args.url, "metadata_url": metadata_url, "publisher": publisher}
    _print(
        build_tool_result(
            source_skill_id=source_skill_id,
            tool_type="access_check",
            policy=args.policy,
            input_payload=input_payload,
            result={"status": status, "reason": reason},
            provenance=provenance,
            validation={"checks": checks},
            used_platform_tools=used_platform_tools,
        )
    )


def run_file_probe(
    *,
    source_skill_id: str,
    publisher: str,
    metadata_url: str = "",
    expected_suffixes: list[str] | None = None,
) -> None:
    parser = argparse.ArgumentParser(description=f"Probe a {source_skill_id} direct file resource.")
    parser.add_argument("--policy", default="discovery_only")
    parser.add_argument("--fixture-file")
    parser.add_argument("--url", default="")
    parser.add_argument("--expected-column", action="append", default=[])
    args = parser.parse_args()
    input_payload = {"fixture_file": bool(args.fixture_file), "url": args.url, "expected_columns": list(args.expected_column)}
    provenance = {"source_url": args.url, "metadata_url": metadata_url, "publisher": publisher}
    if not policy_allows(args.policy, "probe"):
        _print(fail_closed_result(source_skill_id=source_skill_id, tool_type="probe", policy=args.policy, input_payload=input_payload, reason=policy_reason(args.policy, "probe"), provenance=provenance))
        return
    try:
        path = Path(args.fixture_file) if args.fixture_file else None
        checks = _file_checks(path, args.url, args.expected_column, expected_suffixes or [])
        result = {"status": "probe_requestable" if all(check["passed"] for check in checks) else "needs_follow_up"}
    except Exception as exc:
        checks = [validation_check("probe_exception", False, reason=type(exc).__name__)]
        result = {"status": "needs_follow_up", "reason": str(exc)}
    _print(build_tool_result(source_skill_id=source_skill_id, tool_type="probe", policy=args.policy, input_payload=input_payload, result=result, provenance=provenance, validation={"checks": checks}))


def run_file_fetch(
    *,
    source_skill_id: str,
    publisher: str,
    metadata_url: str = "",
    default_name: str = "resource_sample.dat",
) -> None:
    parser = argparse.ArgumentParser(description=f"Fetch a capped {source_skill_id} file sample.")
    parser.add_argument("--policy", default="discovery_only")
    parser.add_argument("--fixture-file")
    parser.add_argument("--url", default="")
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--max-bytes", type=int, default=1_000_000)
    args = parser.parse_args()
    input_payload = {"fixture_file": bool(args.fixture_file), "url": args.url, "max_bytes": args.max_bytes, "download_mode": fetch_mode(args.policy)}
    provenance = {"source_url": args.url, "metadata_url": metadata_url, "publisher": publisher}
    if not policy_allows(args.policy, "fetch"):
        _print(fail_closed_result(source_skill_id=source_skill_id, tool_type="fetch", policy=args.policy, input_payload=input_payload, reason=policy_reason(args.policy, "fetch"), provenance=provenance))
        return
    try:
        target = Path(args.output_dir) / default_name
        artifact = fetch_file_artifact(
            fixture_file=args.fixture_file,
            url=args.url,
            target=target,
            policy=args.policy,
            max_bytes=args.max_bytes,
        )
        checks = [
            validation_check("sample_written", True),
            validation_check(
                "fetch_scope",
                fetch_mode(args.policy) == "full" or target.stat().st_size <= args.max_bytes,
                download_mode=fetch_mode(args.policy),
                max_bytes=args.max_bytes,
            ),
        ]
        result = {"status": "fetched", "size_bytes": target.stat().st_size}
        artifacts = [artifact]
    except Exception as exc:
        checks = [validation_check("fetch_exception", False, reason=type(exc).__name__)]
        result = {"status": "needs_follow_up", "reason": str(exc)}
        artifacts = []
    _print(build_tool_result(source_skill_id=source_skill_id, tool_type="fetch", policy=args.policy, input_payload=input_payload, result=result, provenance=provenance, artifacts=artifacts, validation={"checks": checks}))


def run_file_validate(
    *,
    source_skill_id: str,
    publisher: str,
    metadata_url: str = "",
    expected_suffixes: list[str] | None = None,
) -> None:
    parser = argparse.ArgumentParser(description=f"Validate a {source_skill_id} file sample.")
    parser.add_argument("--policy", default="discovery_only")
    parser.add_argument("--input-file", required=True)
    parser.add_argument("--expected-column", action="append", default=[])
    args = parser.parse_args()
    input_payload = {"input_file": args.input_file, "expected_columns": list(args.expected_column)}
    provenance = {"source_url": "", "metadata_url": metadata_url, "publisher": publisher}
    if not policy_allows(args.policy, "validate"):
        _print(fail_closed_result(source_skill_id=source_skill_id, tool_type="validate", policy=args.policy, input_payload=input_payload, reason=policy_reason(args.policy, "validate"), provenance=provenance))
        return
    try:
        checks = _file_checks(Path(args.input_file), "", args.expected_column, expected_suffixes or [])
        result = {"status": "validation_passed" if all(check["passed"] for check in checks) else "validation_failed"}
    except Exception as exc:
        checks = [validation_check("validate_exception", False, reason=type(exc).__name__)]
        result = {"status": "validation_failed", "reason": str(exc)}
    _print(build_tool_result(source_skill_id=source_skill_id, tool_type="validate", policy=args.policy, input_payload=input_payload, result=result, provenance=provenance, validation={"checks": checks}))


def _load_json(fixture_response: str | None, url: str) -> Any:
    if fixture_response:
        return read_json_file(fixture_response)
    return json.loads(fetch_text_with_live_gate(url))


def _json_checks(payload: Any, expected_fields: list[str]) -> list[dict[str, Any]]:
    checks = [
        validation_check("json_shape", isinstance(payload, (dict, list))),
        validation_check("no_error_payload", not _has_error_payload(payload)),
        validation_check("arcgis_transfer_not_exceeded", not _arcgis_transfer_exceeded(payload)),
        validation_check("records_present", _record_count(payload) > 0),
    ]
    for field in expected_fields:
        checks.append(validation_check(f"field_present:{field}", _field_present(payload, field)))
    return checks


def _field_present(payload: Any, field: str) -> bool:
    if isinstance(payload, dict):
        if field in payload:
            return True
        return any(_field_present(value, field) for value in payload.values() if isinstance(value, (dict, list)))
    if isinstance(payload, list):
        return any(_field_present(item, field) for item in payload[:20] if isinstance(item, (dict, list)))
    return False


def _record_count(payload: Any) -> int:
    if isinstance(payload, list):
        return len(payload)
    if isinstance(payload, dict):
        for key in ("results", "data", "features", "items", "series", "observations"):
            value = payload.get(key)
            if isinstance(value, list):
                return len(value)
        return 1
    return 0


def _has_error_payload(payload: Any) -> bool:
    if isinstance(payload, dict):
        if isinstance(payload.get("error"), (dict, str)):
            return True
        if isinstance(payload.get("errors"), list) and payload.get("errors"):
            return True
        return any(_has_error_payload(value) for value in payload.values() if isinstance(value, (dict, list)))
    if isinstance(payload, list):
        return any(_has_error_payload(item) for item in payload if isinstance(item, (dict, list)))
    return False


def _arcgis_transfer_exceeded(payload: Any) -> bool:
    if isinstance(payload, dict):
        if payload.get("exceededTransferLimit") is True:
            return True
        return any(_arcgis_transfer_exceeded(value) for value in payload.values() if isinstance(value, (dict, list)))
    if isinstance(payload, list):
        return any(_arcgis_transfer_exceeded(item) for item in payload if isinstance(item, (dict, list)))
    return False


def _cap_json(payload: Any, max_records: int) -> Any:
    if isinstance(payload, list):
        return payload[:max_records]
    if isinstance(payload, dict):
        capped = dict(payload)
        for key in ("results", "data", "features", "items", "series", "observations"):
            if isinstance(capped.get(key), list):
                capped[key] = capped[key][:max_records]
        return capped
    return payload


def _file_checks(path: Path | None, url: str, expected_columns: list[str], expected_suffixes: list[str]) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []
    name = path.name if path else url
    if expected_suffixes:
        checks.append(validation_check("expected_suffix", any(name.lower().endswith(suffix) for suffix in expected_suffixes), expected_suffixes=expected_suffixes))
    if path:
        exists = path.exists()
        checks.append(validation_check("file_exists", exists))
        checks.append(validation_check("file_non_empty", exists and path.stat().st_size > 0))
        if expected_columns:
            first_line = path.read_text(encoding="utf-8", errors="replace").splitlines()[0] if exists else ""
            columns = {column.strip() for column in first_line.split(",")}
            for column in expected_columns:
                checks.append(validation_check(f"column_present:{column}", column in columns))
    return checks


def _print(payload: dict[str, Any]) -> None:
    print(json.dumps(payload, indent=2, sort_keys=True))
