from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable


FORBIDDEN_FINAL_CHAIN_FIELDS = {
    "approved_url",
    "approved_urls",
    "ordered_urls",
    "resource_plan",
    "resource_plans",
    "resource_plan_validations",
    "download_success",
    "downloaded_file",
    "downloaded_files",
    "downloaded_manifest",
    "downloaded_path",
    "downloaded_bytes",
    "local_path",
    "verifier_success",
    "final_candidate_ranking",
    "final_score",
    "final_success",
    "final_answer",
}

FORBIDDEN_BENCHMARK_FIELDS = {
    "answer_key",
    "answer_url",
    "answer_urls",
    "benchmark_case",
    "benchmark_case_id",
    "benchmark_id",
    "expected_answer",
    "expected_url",
    "expected_urls",
    "gold_url",
    "gold_urls",
}


@dataclass(frozen=True)
class LintIssue:
    path: str
    field: str
    code: str
    severity: str = "error"
    message: str = ""

    def to_dict(self) -> dict[str, str]:
        return {
            "path": self.path,
            "field": self.field,
            "code": self.code,
            "severity": self.severity,
            "message": self.message,
        }


def lint_payload(payload: Any) -> list[dict[str, str]]:
    issues: list[LintIssue] = []
    for path, field in _walk_keys(payload):
        if field in FORBIDDEN_FINAL_CHAIN_FIELDS:
            issues.append(
                LintIssue(
                    path=path,
                    field=field,
                    code="forbidden_final_chain_field",
                    message="SourceSkill artifacts must not contain final-chain authority fields.",
                )
            )
        if field in FORBIDDEN_BENCHMARK_FIELDS:
            issues.append(
                LintIssue(
                    path=path,
                    field=field,
                    code="forbidden_benchmark_answer_field",
                    message="SourceSkill artifacts must not encode benchmark answer-table fields.",
                )
            )
    return [issue.to_dict() for issue in issues]


def assert_lint_clean(payload: Any) -> None:
    issues = lint_payload(payload)
    if issues:
        formatted = ", ".join(issue["path"] for issue in issues)
        raise ValueError(f"SourceSkill payload contains forbidden fields: {formatted}")


def classify_known_source() -> dict[str, object]:
    return {
        "name": "known_source",
        "is_skill": False,
        "category": "legacy_source_prior_registry",
        "migration_target": "SourceCard plus SourceSkill metadata/scripts",
        "guardrail": (
            "known_source is source-prior evidence only, not a skill and not an "
            "answer table for benchmark cases."
        ),
    }


def _walk_keys(value: Any, prefix: str = "") -> Iterable[tuple[str, str]]:
    if isinstance(value, dict):
        for key, item in value.items():
            field = str(key)
            path = f"{prefix}.{field}" if prefix else field
            yield path, field
            yield from _walk_keys(item, path)
    elif isinstance(value, list):
        for index, item in enumerate(value):
            path = f"{prefix}[{index}]" if prefix else f"[{index}]"
            yield from _walk_keys(item, path)
