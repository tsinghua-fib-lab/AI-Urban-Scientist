from __future__ import annotations

import argparse
import json


def main() -> None:
    parser = argparse.ArgumentParser(description="Build deterministic SDMX REST endpoint templates.")
    parser.add_argument("--base-url", default="https://sdmx.oecd.org/public/rest/v1")
    parser.add_argument("--agency", default="all")
    parser.add_argument("--dataflow", default="all")
    parser.add_argument("--version", default="latest")
    parser.add_argument("--flow-ref", default="{agency},{datastructure}@{dataflow}")
    parser.add_argument("--key", default="all")
    parser.add_argument("--start-period", default="2024")
    parser.add_argument("--end-period", default="2024")
    args = parser.parse_args()
    base = args.base_url.rstrip("/")
    dataflow_url = f"{base}/dataflow/{args.agency}/{args.dataflow}/{args.version}"
    payload = {
        "source_skill_id": "sdmx-platform",
        "finality": "platform_template",
        "input": vars(args),
        "direct_eval_recommendation": {
            "skill_id": "sdmx-platform",
            "status": "API_PASS",
            "api_url": dataflow_url,
            "probe_method": "GET",
            "expected_http_status": 200,
            "notes": "Return the verified SDMX metadata API entry for the supplied base URL instead of inferring every dimension. The default base URL is only a public smoke-test example.",
        },
        "candidate_resources": [
            {
                "role": "dataflow_metadata",
                "url": dataflow_url,
                "access_method": "sdmx_dataflow",
                "executability_hint": "direct_api",
            },
            {
                "role": "datastructure_metadata",
                "url": f"{base}/datastructure/{args.agency}/{args.dataflow}/{args.version}?references=all&detail=allstubs",
                "access_method": "sdmx_datastructure",
                "executability_hint": "direct_api",
            },
            {
                "role": "bounded_data_query",
                "url": f"{base}/data/{args.flow_ref}/{args.key}?startPeriod={args.start_period}&endPeriod={args.end_period}&dimensionAtObservation=AllDimensions",
                "access_method": "sdmx_data",
                "executability_hint": "api_template" if "{" in args.flow_ref else "direct_api",
            },
        ],
        "minimal_probe": [
            "Probe dataflow metadata first with a normal GET; do not use Range headers.",
            "Probe datastructure with references=all before constructing a series key.",
            "Run a bounded data query with startPeriod/endPeriod before any broad extraction.",
        ],
    }
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
