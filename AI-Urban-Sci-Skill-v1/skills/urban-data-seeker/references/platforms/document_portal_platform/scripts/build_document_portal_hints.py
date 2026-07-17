from __future__ import annotations

import argparse
import json
from urllib.parse import urlparse


PACKAGE_ID = "document_portal_platform"
REQUIRED_VALIDATION = ["resolver", "probe", "download", "verifier"]


def main() -> None:
    parser = argparse.ArgumentParser(description="Emit not-final document portal platform hints.")
    parser.add_argument("--need-id", required=True)
    parser.add_argument("--url", required=True)
    parser.add_argument("--document-url", default="")
    args = parser.parse_args()
    payload = build_payload(need_id=args.need_id, url=args.url, document_url=args.document_url)
    print(json.dumps(payload, indent=2, sort_keys=True))


def build_payload(*, need_id: str, url: str, document_url: str) -> dict[str, object]:
    parsed = parse_document_portal_url(url)
    resource_hints = [
        {
            "role": "portal_landing",
            "url": url,
            "access_method": "document_portal_landing",
            "need_ids": [need_id],
            "required_validation": REQUIRED_VALIDATION,
            "finality": "not_final",
            "consumer_authority": "none",
            "executability_hint": "source_landing",
            "required_params": ["url"],
            "missing_params": [],
            "resolver_hint": {
                "resolver_family": "document_portal_page",
                "target_executability_hint": "resolvable_resource",
            },
            "validation_notes": [
                "Validate whether the landing page links to the relevant official document.",
            ],
        }
    ]
    if document_url:
        resource_hints.append(
            {
                "role": "document_candidate",
                "url": document_url,
                "access_method": "document_portal_document",
                "need_ids": [need_id],
                "required_validation": REQUIRED_VALIDATION,
                "finality": "not_final",
                "consumer_authority": "none",
                "executability_hint": "resolvable_resource",
                "required_params": ["document_url"],
                "missing_params": [],
                "resolver_hint": {
                    "resolver_family": "document_candidate",
                    "target_executability_hint": "resolvable_resource",
                },
                "validation_notes": [
                    "Validate version, adoption status, geography, and whether the file is the intended plan/report artifact.",
                ],
            }
        )
    return {
        "platform_package_id": PACKAGE_ID,
        "package_type": "platform_tool",
        "finality": "not_final",
        "consumer_authority": "none",
        "input": {"need_id": need_id, "url": url, "document_url": document_url},
        "parsed": parsed,
        "resource_hints": resource_hints,
        "positive_evidence": [
            {
                "type": "platform_parse",
                "message": "Document portal landing and optional document candidate were normalized from supplied URLs.",
            }
        ],
        "negative_evidence": [],
        "source_skill_usage": {
            "allowed_context": "Tools/Scripts Used",
            "can_decide_research_fit": False,
            "message": "A SourceSkill may use these mechanics, but must decide source-family suitability itself.",
        },
    }


def parse_document_portal_url(url: str) -> dict[str, str]:
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise ValueError("Document portal URL must be an absolute http(s) URL")
    return {
        "kind": "document_portal",
        "domain": parsed.netloc.lower(),
        "input_url": url,
    }


if __name__ == "__main__":
    main()
