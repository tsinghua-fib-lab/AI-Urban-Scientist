from __future__ import annotations

import argparse
import json
from urllib.parse import quote_plus, urlencode, urlparse


PACKAGE_ID = "sdmx_platform"
REQUIRED_VALIDATION = ["resolver", "probe", "download", "verifier"]


def main() -> None:
    parser = argparse.ArgumentParser(description="Emit not-final SDMX platform hints.")
    parser.add_argument("--need-id", required=True)
    parser.add_argument("--url", required=True)
    parser.add_argument("--agency", default="all")
    parser.add_argument("--dataflow", required=True)
    parser.add_argument("--key", default="")
    parser.add_argument("--query", default="")
    args = parser.parse_args()

    payload = build_payload(
        need_id=args.need_id,
        url=args.url,
        agency=args.agency,
        dataflow=args.dataflow,
        key=args.key,
        query=args.query,
    )
    print(json.dumps(payload, indent=2, sort_keys=True))


def build_payload(*, need_id: str, url: str, agency: str, dataflow: str, key: str, query: str) -> dict[str, object]:
    parsed = parse_sdmx_url(url, agency=agency, dataflow=dataflow)
    missing_params = [] if key else ["key"]
    resource_hints = [
        {
            "role": "dataflow_metadata",
            "url": build_dataflow_url(parsed["base_url"], agency, dataflow),
            "access_method": "sdmx_dataflow_metadata",
            "need_ids": [need_id],
            "required_validation": REQUIRED_VALIDATION,
            "finality": "not_final",
            "consumer_authority": "none",
            "executability_hint": "source_landing",
            "required_params": ["base_url", "agency", "dataflow"],
            "missing_params": [],
            "resolver_hint": {
                "resolver_family": "sdmx_dataflow",
                "agency": agency,
                "dataflow": dataflow,
                "target_executability_hint": "resolvable_resource",
            },
            "future_probe_hint": {
                "method": "GET_LIGHT",
                "expected_status": [200],
                "notes": "Probe dataflow metadata and provider SDMX version before building data queries.",
            },
            "validation_notes": [
                "Dataflow metadata is discovery evidence, not a data resource.",
                "Validate dimensions, codelists, and SDMX REST version downstream.",
            ],
        },
        {
            "role": "data_query",
            "url": build_data_query_url(parsed["base_url"], dataflow, key),
            "access_method": "sdmx_data_query",
            "need_ids": [need_id],
            "required_validation": REQUIRED_VALIDATION,
            "finality": "not_final",
            "consumer_authority": "none",
            "executability_hint": "resolvable_resource" if key else "source_landing",
            "needs_follow_up": True,
            "follow_up_reason": "sdmx_data_query_requires_structure_and_dimension_validation",
            "required_params": ["base_url", "dataflow", "key"],
            "missing_params": missing_params,
            "requestability_conditions": [
                "provider SDMX version and REST profile are known",
                "dataflow exists and dimension key is valid",
                "requested period and content type are supported",
                "response is data, not an SDMX error or structure-only payload",
            ],
            "resolver_hint": {
                "resolver_family": "sdmx_data_query",
                "agency": agency,
                "dataflow": dataflow,
                "key": key,
                "target_executability_hint": "resolvable_resource",
            },
            "api_query_template": {
                "url": f"{parsed['base_url']}/data/{{dataflow}}/{{key}}",
                "query_params": {
                    "startPeriod": "{start_period}",
                    "endPeriod": "{end_period}",
                },
            },
            "future_probe_hint": {
                "method": "GET_LIGHT",
                "expected_status": [200],
                "notes": "Use a small period range and inspect SDMX error payloads before extraction.",
            },
            "validation_notes": [
                "Validate dimensions and codelists before treating a series key as executable.",
                "Provider-specific SDMX URL shapes may require an adapter before probing.",
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
            "agency": agency,
            "dataflow": dataflow,
            "key": key,
            "query": query,
        },
        "parsed": parsed,
        "resource_hints": resource_hints,
        "positive_evidence": [
            {
                "type": "platform_parse",
                "message": "SDMX base URL, agency, dataflow, and optional key were parsed from the supplied inputs.",
            }
        ],
        "negative_evidence": [],
        "source_skill_usage": {
            "allowed_context": "Tools/Scripts Used",
            "can_decide_research_fit": False,
            "message": "A SourceSkill may use SDMX mechanics after deciding source-family fit.",
        },
    }


def parse_sdmx_url(url: str, *, agency: str, dataflow: str) -> dict[str, str]:
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise ValueError("SDMX URL must be an absolute http(s) URL")
    base_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path.rstrip('/')}"
    return {
        "kind": "sdmx_dataflow",
        "domain": parsed.netloc.lower(),
        "id": dataflow,
        "agency": agency,
        "base_url": base_url,
        "input_url": url,
    }


def build_dataflow_url(base_url: str, agency: str, dataflow: str) -> str:
    return f"{base_url}/dataflow/{quote_plus(agency)}/{quote_plus(dataflow)}/latest"


def build_data_query_url(base_url: str, dataflow: str, key: str) -> str:
    query = urlencode({"startPeriod": "{start_period}", "endPeriod": "{end_period}"})
    key_part = quote_plus(key) if key else "{key}"
    return f"{base_url}/data/{quote_plus(dataflow)}/{key_part}?{query}"


if __name__ == "__main__":
    main()
