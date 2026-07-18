from __future__ import annotations

import json
import os
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.request import Request, urlopen

from open_data_skills.lint_contract import assert_lint_clean


TOOL_RESULT_SCHEMA = "open_data_tool_result.v1"
DEFAULT_POLICY = "discovery_only"
LIVE_FETCH_ENV = "AI_OPEN_DATA_SKILLS_LIVE_FETCH"

POLICIES = {
    "discovery_only",
    "probe_allowed",
    "fetch_sample_allowed",
    "fetch_full_allowed",
    "validate_allowed",
}

POLICY_BY_TOOL_TYPE = {
    "probe": {"probe_allowed"},
    "fetch": {"fetch_sample_allowed", "fetch_full_allowed"},
    "validate": {"validate_allowed"},
}


def build_tool_result(
    *,
    source_skill_id: str,
    tool_type: str,
    policy: str,
    input_payload: dict[str, Any],
    result: dict[str, Any],
    provenance: dict[str, Any] | None = None,
    artifacts: list[dict[str, Any]] | None = None,
    validation: dict[str, Any] | None = None,
    used_platform_tools: list[str] | None = None,
) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "schema": TOOL_RESULT_SCHEMA,
        "source_skill_id": source_skill_id,
        "tool_type": tool_type,
        "policy": normalize_policy(policy),
        "used_platform_tools": list(used_platform_tools or []),
        "input": dict(input_payload),
        "result": dict(result),
        "provenance": _with_retrieved_at(provenance or {}),
        "artifacts": list(artifacts or []),
        "validation": validation or {"checks": []},
        "finality": "not_final",
        "consumer_authority": "none",
    }
    assert_lint_clean(payload)
    return payload


def fail_closed_result(
    *,
    source_skill_id: str,
    tool_type: str,
    policy: str,
    input_payload: dict[str, Any],
    reason: str,
    provenance: dict[str, Any] | None = None,
    used_platform_tools: list[str] | None = None,
) -> dict[str, Any]:
    return build_tool_result(
        source_skill_id=source_skill_id,
        tool_type=tool_type,
        policy=policy,
        input_payload=input_payload,
        result={"status": "needs_follow_up", "reason": reason},
        provenance=provenance,
        artifacts=[],
        validation={
            "checks": [
                {
                    "name": "policy_gate",
                    "passed": False,
                    "reason": reason,
                }
            ]
        },
        used_platform_tools=used_platform_tools,
    )


def normalize_policy(policy: str | None) -> str:
    normalized = policy or DEFAULT_POLICY
    if normalized not in POLICIES:
        return DEFAULT_POLICY
    return normalized


def policy_allows(policy: str | None, tool_type: str) -> bool:
    return normalize_policy(policy) in POLICY_BY_TOOL_TYPE.get(tool_type, set())


def policy_reason(policy: str | None, tool_type: str) -> str:
    return f"policy_{normalize_policy(policy)}_disallows_{tool_type}"


def read_json_file(path: str | Path) -> Any:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def write_json_sample(path: Path, payload: Any) -> dict[str, Any]:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    return {
        "kind": "sample_data",
        "path": str(path),
        "format": "json",
        "size_bytes": path.stat().st_size,
    }


def write_json_fetch_artifact(path: Path, payload: Any, *, policy: str) -> dict[str, Any]:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    mode = fetch_mode(policy)
    return {
        "kind": "full_data" if mode == "full" else "sample_data",
        "path": str(path),
        "format": "json",
        "size_bytes": path.stat().st_size,
        "capped": mode != "full",
        "download_mode": mode,
    }


def copy_capped_bytes(source: Path, target: Path, *, max_bytes: int) -> dict[str, Any]:
    target.parent.mkdir(parents=True, exist_ok=True)
    with source.open("rb") as src, target.open("wb") as dst:
        dst.write(src.read(max(0, max_bytes)))
    return {
        "kind": "sample_data",
        "path": str(target),
        "format": target.suffix.lstrip(".") or "binary",
        "size_bytes": target.stat().st_size,
        "capped": True,
    }


def copy_fetch_artifact(
    source: Path,
    target: Path,
    *,
    policy: str,
    max_bytes: int,
    artifact_kind: str = "sample_data",
    artifact_format: str | None = None,
) -> dict[str, Any]:
    target.parent.mkdir(parents=True, exist_ok=True)
    mode = fetch_mode(policy)
    with source.open("rb") as src, target.open("wb") as dst:
        if mode == "full":
            shutil.copyfileobj(src, dst)
        else:
            dst.write(src.read(max(0, max_bytes)))
    return _file_artifact(target, policy=policy, artifact_kind=artifact_kind, artifact_format=artifact_format)


def write_url_fetch_artifact(
    url: str,
    target: Path,
    *,
    policy: str,
    max_bytes: int,
    timeout: int = 20,
    artifact_kind: str = "sample_data",
    artifact_format: str | None = None,
) -> dict[str, Any]:
    target.parent.mkdir(parents=True, exist_ok=True)
    mode = fetch_mode(policy)
    limit = None if mode == "full" else max(0, max_bytes)
    _stream_url_to_path_with_live_gate(url, target, max_bytes=limit, timeout=timeout)
    return _file_artifact(target, policy=policy, artifact_kind=artifact_kind, artifact_format=artifact_format)


def fetch_file_artifact(
    *,
    fixture_file: str | None,
    url: str,
    target: Path,
    policy: str,
    max_bytes: int,
    artifact_kind: str = "sample_data",
    artifact_format: str | None = None,
) -> dict[str, Any]:
    if fixture_file:
        return copy_fetch_artifact(
            Path(fixture_file),
            target,
            policy=policy,
            max_bytes=max_bytes,
            artifact_kind=artifact_kind,
            artifact_format=artifact_format,
        )
    return write_url_fetch_artifact(
        url,
        target,
        policy=policy,
        max_bytes=max_bytes,
        artifact_kind=artifact_kind,
        artifact_format=artifact_format,
    )


def fetch_mode(policy: str | None) -> str:
    return "full" if normalize_policy(policy) == "fetch_full_allowed" else "sample"


def fetch_text_with_live_gate(
    url: str,
    *,
    max_bytes: int | None = 512_000,
    timeout: int = 20,
    headers: dict[str, str] | None = None,
) -> str:
    if os.environ.get(LIVE_FETCH_ENV) != "1":
        raise RuntimeError("live_fetch_env_not_enabled")
    request = Request(url, headers=_request_headers(headers))
    with urlopen(request, timeout=timeout) as response:
        data = response.read() if max_bytes is None else response.read(max(0, max_bytes))
        return data.decode("utf-8", errors="replace")


def fetch_bytes_with_live_gate(
    url: str,
    *,
    max_bytes: int | None = 512_000,
    timeout: int = 20,
    headers: dict[str, str] | None = None,
) -> bytes:
    if os.environ.get(LIVE_FETCH_ENV) != "1":
        raise RuntimeError("live_fetch_env_not_enabled")
    request = Request(url, headers=_request_headers(headers))
    with urlopen(request, timeout=timeout) as response:
        return response.read() if max_bytes is None else response.read(max(0, max_bytes))


def validation_check(name: str, passed: bool, **details: Any) -> dict[str, Any]:
    check = {"name": name, "passed": bool(passed)}
    check.update(details)
    return check


def _with_retrieved_at(provenance: dict[str, Any]) -> dict[str, Any]:
    enriched = dict(provenance)
    enriched.setdefault("source_url", "")
    enriched.setdefault("metadata_url", "")
    enriched.setdefault("publisher", "")
    enriched.setdefault("retrieved_at", datetime.now(timezone.utc).isoformat())
    return enriched


def _stream_url_to_path_with_live_gate(
    url: str,
    target: Path,
    *,
    max_bytes: int | None,
    timeout: int,
    headers: dict[str, str] | None = None,
) -> None:
    if os.environ.get(LIVE_FETCH_ENV) != "1":
        raise RuntimeError("live_fetch_env_not_enabled")
    request = Request(url, headers=_request_headers(headers))
    remaining = max_bytes
    with urlopen(request, timeout=timeout) as response, target.open("wb") as dst:
        while True:
            chunk_size = 1024 * 1024
            if remaining is not None:
                if remaining <= 0:
                    break
                chunk_size = min(chunk_size, remaining)
            chunk = response.read(chunk_size)
            if not chunk:
                break
            dst.write(chunk)
            if remaining is not None:
                remaining -= len(chunk)


def _request_headers(headers: dict[str, str] | None = None) -> dict[str, str]:
    merged = {"User-Agent": "open-data-skills/0.1"}
    for key, value in (headers or {}).items():
        if key and value:
            merged[str(key)] = str(value)
    return merged


def _file_artifact(
    target: Path,
    *,
    policy: str,
    artifact_kind: str,
    artifact_format: str | None,
) -> dict[str, Any]:
    mode = fetch_mode(policy)
    return {
        "kind": "full_data" if mode == "full" else artifact_kind,
        "path": str(target),
        "format": artifact_format or target.suffix.lstrip(".") or "binary",
        "size_bytes": target.stat().st_size,
        "capped": mode != "full",
        "download_mode": mode,
    }
