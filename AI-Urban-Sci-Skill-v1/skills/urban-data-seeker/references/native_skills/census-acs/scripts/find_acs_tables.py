from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from urllib.parse import urlencode


OPEN_DATA_SKILLS_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(OPEN_DATA_SKILLS_ROOT))

from open_data_skills.route_bridge import build_dossier_fragment, build_resource_intents


SOURCE_SKILL_ID = "census_acs"
SOURCE_CARD_ID = "us_census_acs"
REQUIRED_PARAMS = ["year", "survey", "geography", "variables"]
GEOGRAPHY_PREDICATES = {
    "county": {
        "normalized": "county",
        "for": "county:*",
        "in": [],
        "example": "for=county:*&in=state:{state}",
    },
    "tract": {
        "normalized": "tract",
        "for": "tract:*",
        "in": ["state:*", "county:*"],
        "example": "for=tract:*&in=state:{state}&in=county:{county}",
    },
    "block group": {
        "normalized": "block group",
        "for": "block group:*",
        "in": ["state:*", "county:*", "tract:*"],
        "example": "for=block group:*&in=state:{state}&in=county:{county}&in=tract:{tract}",
    },
}
GEOGRAPHY_ALIASES = {
    "block-group": "block group",
    "block_group": "block group",
}


def main() -> None:
    parser = argparse.ArgumentParser(description="Emit not-final Census ACS source hints.")
    parser.add_argument("--need-id", required=True)
    parser.add_argument("--need-text", required=True)
    parser.add_argument("--year", default="")
    parser.add_argument("--survey", default="")
    parser.add_argument("--geography", default="")
    parser.add_argument("--variables")
    parser.add_argument("--state", default="")
    parser.add_argument("--county", default="")
    parser.add_argument("--tract", default="")
    args = parser.parse_args()

    payload = build_payload(
        need_id=args.need_id,
        need_text=args.need_text,
        year=args.year,
        survey=args.survey,
        geography=args.geography,
        variables=args.variables,
        state=args.state,
        county=args.county,
        tract=args.tract,
    )
    print(json.dumps(payload, indent=2, sort_keys=True))


def build_payload(
    *,
    need_id: str,
    need_text: str,
    year: str,
    survey: str,
    geography: str,
    variables: str | None,
    state: str = "",
    county: str = "",
    tract: str = "",
) -> dict[str, object]:
    api_root = f"https://api.census.gov/data/{year}/acs/{survey}"
    variable_list = _split_csv(variables)
    geography_key = _normalize_geography(geography)
    supported_geography = geography_key in GEOGRAPHY_PREDICATES
    base_missing_params = _missing_params(
        {
            "year": year,
            "survey": survey,
            "geography": geography if supported_geography else "",
            "variables": variable_list,
        }
    )
    missing_params = list(base_missing_params)
    if not missing_params and supported_geography:
        missing_params.extend(
            _missing_geography_predicates(
                geography_key=geography_key,
                state=state,
                county=county,
                tract=tract,
            )
        )
    executability_hint = "resolvable_resource" if not missing_params else "source_landing"
    api_hint = (
        build_acs_api_hint(
            year=year,
            survey=survey,
            geography=geography,
            variables=variable_list,
            state=state,
            county=county,
            tract=tract,
        )
        if not missing_params
        else {
            "url": api_root,
            "query_params": {
                "get": "NAME,{variables}",
                "for": "{geography}",
            },
            "normalized_geography": geography_key,
        }
    )
    needs_follow_up = bool(missing_params)
    follow_up_reason = _follow_up_reason(missing_params, supported_geography)
    candidate_resources = [
        {
            "url": api_hint["url"],
            "role": "primary",
            "access_method": "api_or_direct",
            "need_ids": [need_id],
            "source_skill_id": SOURCE_SKILL_ID,
            "source_card_id": SOURCE_CARD_ID,
            "description": "Candidate Census ACS API dataset root; variables, geography, and year still require validation.",
            "executability_hint": executability_hint,
            "needs_follow_up": needs_follow_up,
            "follow_up_reason": follow_up_reason,
            "required_params": list(REQUIRED_PARAMS),
            "missing_params": missing_params,
            "requestability_conditions": [
                "Census API returns a JSON array response",
                "variables are valid for the selected ACS year and survey",
                "geography predicate is supported by Census API",
                "HTTP 200 HTML Missing Key response is needs_follow_up",
            ],
            "probe_failure_policy": {
                "http_200_non_json": "needs_follow_up",
                "http_200_html_missing_key": "needs_follow_up",
                "html_or_error_payload": "needs_follow_up",
                "missing_or_unsupported_params": "needs_follow_up",
            },
            "supported_geography_examples": {
                spec["normalized"]: spec["example"]
                for spec in GEOGRAPHY_PREDICATES.values()
            },
            "resolver_hint": {
                "resolver_family": "census_acs_api",
                "target_executability_hint": "resolvable_resource",
                "not_executable_until_params_complete": True,
                "normalized_geography": api_hint["normalized_geography"],
                "requires_geography_predicates": _required_geography_predicates(
                    geography_key
                ),
            },
            "api_query_template": {
                "url": "https://api.census.gov/data/{year}/acs/{survey}",
                "query_params": _template_query_params(
                    geography_key, api_hint["query_params"]
                ),
            },
            "future_probe_hint": {
                "method": "GET_LIGHT",
                "expected_status": [200],
                "expected_content_type": "application/json",
                "notes": "Probe a parameterized ACS API request only after variables, geography, survey, and year are complete.",
            },
            "validation_notes": [
                "Validate requested ACS variables or table ids.",
                "Probe the concrete query URL, not the ACS API root, when params are complete.",
                "Validate geography predicates and year availability.",
                "Do not treat the ACS API root as an executable resource when variables are missing.",
            ],
        }
    ]
    route_goal = f"Find Census ACS {survey} table/API leads for {year} {geography} data."
    fragment = build_dossier_fragment(
        source_skill_id=SOURCE_SKILL_ID,
        source_card_id=SOURCE_CARD_ID,
        need_ids=[need_id],
        route_goal=route_goal,
        candidate_resources=candidate_resources,
        positive_evidence=[
            {
                "type": "source_prior",
                "message": "ACS, demographic, census geography, or variable need matched Census ACS workflow.",
                "survey": survey,
                "year": year,
            }
        ],
        negative_evidence=[],
    )
    fragment["ambiguities"] = [
        {
            "type": "variable_geography_year_ambiguity",
            "message": "ACS variable/geography/year ambiguity remains until variables, summary level, predicates, and vintage availability are validated.",
        }
    ]
    fragment["verification_notes"] = [
        "Validate requested ACS variables or table ids.",
        "Validate geography level, predicates, and year availability.",
        "Keep demographic attributes separate from boundary resources unless the route explicitly needs both.",
    ]
    fragment["executability_hint"] = executability_hint
    resource_intents = build_resource_intents(fragment)

    return {
        "source_skill_id": SOURCE_SKILL_ID,
        "source_card_id": SOURCE_CARD_ID,
        "finality": "not_final",
        "consumer_authority": "none",
        "query": {
            "need_id": need_id,
            "need_text": need_text,
            "year": year,
            "survey": survey,
            "geography": geography,
            "state": state,
            "county": county,
            "tract": tract,
            "variables": variable_list,
            "missing_params": missing_params,
        },
        "candidate_resources": fragment["candidate_resources"],
        "route_dossier_fragment": fragment,
        "resource_intents": resource_intents,
    }


def _split_csv(value: str | None) -> list[str]:
    if not value:
        return []
    return [item.strip() for item in value.split(",") if item.strip()]


def build_acs_api_hint(
    *,
    year: str,
    survey: str,
    geography: str,
    variables: list[str],
    state: str = "",
    county: str = "",
    tract: str = "",
) -> dict[str, object]:
    geography_key = _normalize_geography(geography)
    if geography_key not in GEOGRAPHY_PREDICATES:
        raise ValueError(f"Unsupported ACS geography: {geography}")

    predicate = GEOGRAPHY_PREDICATES[geography_key]
    query_params: dict[str, object] = {
        "get": f"NAME,{','.join(variables)}",
        "for": predicate["for"],
    }
    in_predicates = _build_in_predicates(
        geography_key=geography_key,
        state=state,
        county=county,
        tract=tract,
    )
    if in_predicates:
        query_params["in"] = in_predicates

    api_root = f"https://api.census.gov/data/{year}/acs/{survey}"
    return {
        "url": f"{api_root}?{urlencode(query_params, doseq=True)}",
        "query_params": query_params,
        "normalized_geography": predicate["normalized"],
    }


def _normalize_geography(value: str) -> str:
    normalized = value.strip().lower()
    return GEOGRAPHY_ALIASES.get(normalized, normalized)


def _missing_params(values: dict[str, object]) -> list[str]:
    missing: list[str] = []
    for key in REQUIRED_PARAMS:
        value = values.get(key)
        if value in (None, "", []):
            missing.append(key)
    return missing


def _missing_geography_predicates(
    *,
    geography_key: str,
    state: str,
    county: str,
    tract: str,
) -> list[str]:
    required = _required_geography_predicates(geography_key)
    values = {"state": state, "county": county, "tract": tract}
    return [name for name in required if not values.get(name)]


def _required_geography_predicates(geography_key: str) -> list[str]:
    if geography_key == "county":
        return ["state"]
    if geography_key == "tract":
        return ["state", "county"]
    if geography_key == "block group":
        return ["state", "county", "tract"]
    return []


def _build_in_predicates(
    *,
    geography_key: str,
    state: str,
    county: str,
    tract: str,
) -> list[str]:
    predicates: list[str] = []
    if geography_key in {"county", "tract", "block group"}:
        predicates.append(f"state:{state}")
    if geography_key in {"tract", "block group"}:
        predicates.append(f"county:{county}")
    if geography_key == "block group":
        predicates.append(f"tract:{tract}")
    return predicates


def _template_query_params(geography_key: str, query_params: object) -> dict[str, object]:
    if not isinstance(query_params, dict):
        return {"get": "NAME,{variables}", "for": "{geography}"}
    templated = dict(query_params)
    templated["get"] = "NAME,{variables}"
    if geography_key == "county":
        templated["in"] = ["state:{state}"]
    elif geography_key == "tract":
        templated["in"] = ["state:{state}", "county:{county}"]
    elif geography_key == "block group":
        templated["in"] = ["state:{state}", "county:{county}", "tract:{tract}"]
    return templated


def _follow_up_reason(missing_params: list[str], supported_geography: bool) -> str:
    if missing_params:
        if not supported_geography and "geography" in missing_params:
            return "census_acs_unsupported_geography"
        if any(param in missing_params for param in ("state", "county", "tract")):
            return "census_acs_missing_geography_predicates"
        return "census_acs_missing_required_params"
    return "census_acs_complete_params_ready_for_api_probe"


if __name__ == "__main__":
    main()
