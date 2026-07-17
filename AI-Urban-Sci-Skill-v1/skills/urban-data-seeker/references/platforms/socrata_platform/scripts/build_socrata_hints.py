from __future__ import annotations

import argparse
import json
import re
from urllib.parse import quote_plus, urlparse


PACKAGE_ID = "socrata_platform"
REQUIRED_VALIDATION = ["resolver", "probe", "download", "verifier"]
VIEW_ID_RE = re.compile(r"^[a-z0-9]{4}-[a-z0-9]{4}$", re.IGNORECASE)


def main() -> None:
    parser = argparse.ArgumentParser(description="Emit not-final Socrata platform hints.")
    parser.add_argument("--need-id", required=True)
    parser.add_argument("--url", required=True)
    parser.add_argument("--query", default="")
    args = parser.parse_args()

    payload = build_payload(need_id=args.need_id, url=args.url, query=args.query)
    print(json.dumps(payload, indent=2, sort_keys=True))


def build_payload(*, need_id: str, url: str, query: str) -> dict[str, object]:
    parsed = parse_socrata_url(url)
    resource_hints = [
        {
            "role": "rows_csv_export",
            "url": f"https://{parsed['domain']}/resource/{parsed['id']}.csv",
            "metadata_url": f"https://{parsed['domain']}/api/views/{parsed['id']}.json",
            "access_method": "socrata_rows_export",
            "need_ids": [need_id],
            "required_validation": REQUIRED_VALIDATION,
            "finality": "not_final",
            "consumer_authority": "none",
            "executability_hint": "resolvable_resource",
            "needs_follow_up": True,
            "follow_up_reason": "socrata_rows_export_requires_metadata_or_get_probe",
            "required_params": ["domain", "view_id"],
            "missing_params": [],
            "requestability_conditions": [
                "validate_view_metadata",
                "metadata response confirms rowsUpdatedAt or columns",
                "GET rows export returns a non-error CSV response",
                "confirm fields, row availability, and time coverage downstream",
            ],
            "probe_failure_policy": {
                "head_404": "needs_follow_up",
                "http_404": "needs_follow_up",
                "non_csv_or_socrata_error": "needs_follow_up",
            },
            "resolver_hint": {
                "resolver_family": "socrata_rows_export",
                "stable_view_id": parsed["id"],
                "requires_metadata_validation": True,
                "target_executability_hint": "resolvable_resource",
            },
            "api_query_template": {
                "url": f"https://{parsed['domain']}/resource/{parsed['id']}.csv",
                "query_params": {
                    "$limit": "{limit}",
                    "$select": "{columns}",
                },
            },
            "direct_file_pattern": {
                "format": "csv",
                "url_template": "https://{domain}/resource/{view_id}.csv",
            },
            "future_probe_hint": {
                "method": "GET_LIGHT",
                "expected_status": [200],
                "notes": (
                    "Use a capped GET or metadata probe; Socrata HEAD failures are not enough to "
                    "decide export requestability."
                ),
            },
            "validation_notes": [
                "A Socrata view id can form a rows export URL, but it does not decide research fit.",
                "A rows.csv shape is only a resolver hint until metadata or capped GET confirms it.",
                "Validate fields, rows, time coverage, and portal metadata downstream.",
            ],
        },
        {
            "role": "catalog_search",
            "url": build_catalog_search_url(parsed["domain"], query or parsed["id"]),
            "access_method": "socrata_catalog_search",
            "need_ids": [need_id],
            "required_validation": REQUIRED_VALIDATION,
            "finality": "not_final",
            "consumer_authority": "none",
            "executability_hint": "source_landing",
            "required_params": ["domain", "query"],
            "missing_params": [],
            "resolver_hint": {
                "resolver_family": "socrata_catalog_search",
                "target_executability_hint": "resolvable_resource",
            },
            "future_probe_hint": {
                "method": "GET_LIGHT",
                "expected_status": [200],
                "notes": "Use catalog search to find source candidates; do not treat search pages as data resources.",
            },
            "validation_notes": [
                "Catalog search output is a source landing/search hint, not an executable data resource.",
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
                "message": "Socrata domain and view id were parsed from the supplied URL.",
            }
        ],
        "negative_evidence": [],
        "source_skill_usage": {
            "allowed_context": "Tools/Scripts Used",
            "can_decide_research_fit": False,
            "message": "A SourceSkill may use these mechanics, but must decide source-family suitability itself.",
        },
    }


def parse_socrata_url(url: str) -> dict[str, str]:
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise ValueError("Socrata URL must be an absolute http(s) URL")
    path_parts = [part for part in parsed.path.split("/") if part]
    view_id = next((part for part in reversed(path_parts) if VIEW_ID_RE.match(part)), "")
    if not view_id:
        raise ValueError("Socrata URL must include a four-by-four dataset view id")
    return {
        "kind": "socrata_dataset",
        "domain": parsed.netloc.lower(),
        "id": view_id.lower(),
        "input_url": url,
    }


def build_catalog_search_url(domain: str, query: str) -> str:
    return f"https://{domain}/browse?limitTo=datasets&q={quote_plus(query)}"


def classify_socrata_export_probe(
    *,
    method: str,
    status_code: int,
    content_type: str = "",
    body: str = "",
) -> dict[str, object]:
    normalized_method = method.upper()
    normalized_content_type = content_type.lower()
    body_prefix = body[:512].lower()

    if normalized_method == "HEAD" and status_code >= 400:
        return {
            "status": "needs_follow_up",
            "requestable": False,
            "reason": "head_probe_not_authoritative_for_socrata_export",
        }
    if status_code == 200 and normalized_method.startswith("GET"):
        if "text/csv" in normalized_content_type and "error" not in body_prefix:
            return {
                "status": "probe_requestable",
                "requestable": True,
                "reason": "capped_get_returned_csv",
            }
    return {
        "status": "needs_follow_up",
        "requestable": False,
        "reason": "socrata_export_probe_requires_follow_up",
    }


if __name__ == "__main__":
    main()
