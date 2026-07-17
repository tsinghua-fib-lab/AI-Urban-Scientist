from __future__ import annotations

import sys
from pathlib import Path

OPEN_DATA_SKILLS_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(OPEN_DATA_SKILLS_ROOT))

from open_data_skills.repository_metadata_family import RepositoryMetadataConfig, build_repository_payload, run_find_cli


CONFIG = RepositoryMetadataConfig(
    source_skill_id="who_gho",
    source_card_id="who_gho_odata",
    publisher="World Health Organization",
    landing_url="https://www.who.int/data/gho",
    docs_url="https://www.who.int/data/gho/info/gho-odata-api",
    search_url="https://ghoapi.azureedge.net/api/Indicator",
    source_family="who_gho_odata",
    resolver_family="who_gho_indicator_catalog",
    entity_label="WHO GHO indicator catalog",
    route_description="WHO GHO health indicator leads using the official OData API indicator catalog.",
    result_path=("value",),
    required_item_keys=("IndicatorCode", "IndicatorName"),
    sample_filename="who_gho_sample.json",
    access_method="who_gho_indicator_query",
    used_platform_tools=("odata_platform",),
    query_params=(("$filter", "contains(IndicatorName,'{query}')"), ("$top", "10")),
    required_inputs=("query", "geography"),
    validation_notes=(
        "Validate indicator identity, OData entity semantics, geography dimensions, and time filters before any extraction flow.",
        "Indicator catalog matches do not by themselves resolve the final entity set, disaggregation, or units.",
    ),
)


def build_payload(*, need_id: str, need_text: str, query: str, geography: str, time_range: str) -> dict[str, object]:
    return build_repository_payload(
        CONFIG,
        need_id=need_id,
        need_text=need_text,
        query=query,
        geography=geography,
        time_range=time_range,
    )


def main() -> None:
    run_find_cli(CONFIG, build_payload)


if __name__ == "__main__":
    main()
