from __future__ import annotations

import argparse
import json
from urllib.parse import quote_plus, urlparse


PACKAGE_ID = "legistar_platform"
REQUIRED_VALIDATION = ["resolver", "probe", "download", "verifier"]


def main() -> None:
    parser = argparse.ArgumentParser(description="Emit not-final Legistar platform hints.")
    parser.add_argument("--need-id", required=True)
    parser.add_argument("--url", required=True)
    parser.add_argument("--query", default="")
    args = parser.parse_args()
    payload = build_payload(need_id=args.need_id, url=args.url, query=args.query)
    print(json.dumps(payload, indent=2, sort_keys=True))


def build_payload(*, need_id: str, url: str, query: str) -> dict[str, object]:
    parsed = parse_legistar_url(url)
    search_url = f"https://{parsed['domain']}/Legislation.aspx"
    if query:
        search_url = f"{search_url}?Search={quote_plus(query)}"
    resource_hints = [
        {
            "role": "legislation_search",
            "url": search_url,
            "access_method": "legistar_legislation_search",
            "need_ids": [need_id],
            "required_validation": REQUIRED_VALIDATION,
            "finality": "not_final",
            "consumer_authority": "none",
            "executability_hint": "source_landing",
            "required_params": ["domain", "query"],
            "missing_params": [] if query else ["query"],
            "resolver_hint": {
                "resolver_family": "legistar_search",
                "target_executability_hint": "resolvable_resource",
            },
            "validation_notes": [
                "Validate whether a returned portal record is the right bill, resolution, or ordinance.",
                "Confirm whether the portal copy is official or informational only.",
            ],
        },
        {
            "role": "calendar_entrypoint",
            "url": f"https://{parsed['domain']}/Calendar.aspx",
            "access_method": "legistar_calendar",
            "need_ids": [need_id],
            "required_validation": REQUIRED_VALIDATION,
            "finality": "not_final",
            "consumer_authority": "none",
            "executability_hint": "source_landing",
            "required_params": ["domain"],
            "missing_params": [],
            "resolver_hint": {
                "resolver_family": "legistar_calendar",
                "target_executability_hint": "resolvable_resource",
            },
            "validation_notes": [
                "Validate meeting date, agenda linkage, and downloadable attachment URLs downstream.",
            ],
        },
    ]
    return {
        "platform_package_id": PACKAGE_ID,
        "package_type": "platform_tool",
        "finality": "not_final",
        "consumer_authority": "none",
        "input": {"need_id": need_id, "url": url, "query": query},
        "parsed": parsed,
        "resource_hints": resource_hints,
        "positive_evidence": [
            {
                "type": "platform_parse",
                "message": "Legistar portal mechanics were parsed from the supplied URL.",
            }
        ],
        "negative_evidence": [],
        "source_skill_usage": {
            "allowed_context": "Tools/Scripts Used",
            "can_decide_research_fit": False,
            "message": "A SourceSkill may use these mechanics, but must decide source-family suitability itself.",
        },
    }


def parse_legistar_url(url: str) -> dict[str, str]:
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise ValueError("Legistar URL must be an absolute http(s) URL")
    return {
        "kind": "legistar_portal",
        "domain": parsed.netloc.lower(),
        "input_url": url,
    }


if __name__ == "__main__":
    main()
