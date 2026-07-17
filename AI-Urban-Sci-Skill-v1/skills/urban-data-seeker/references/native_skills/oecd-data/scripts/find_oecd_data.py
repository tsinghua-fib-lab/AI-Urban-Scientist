from __future__ import annotations

import sys
from pathlib import Path

OPEN_DATA_SKILLS_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(OPEN_DATA_SKILLS_ROOT))

from open_data_skills.repository_metadata_family import RepositoryMetadataConfig, build_repository_payload, run_find_cli


CONFIG = RepositoryMetadataConfig(
    source_skill_id="oecd_data",
    source_card_id="oecd_data_explorer_sdmx",
    publisher="OECD",
    landing_url="https://www.oecd.org/en/data.html",
    docs_url="https://www.oecd.org/en/data/insights/data-explainers/2024/09/api.html",
    search_url="https://sdmx.oecd.org/public/rest/dataflow/all/all/latest",
    source_family="oecd_data_explorer_sdmx",
    resolver_family="oecd_sdmx_dataflow_metadata",
    entity_label="OECD SDMX dataflow metadata",
    route_description="OECD SDMX dataflow metadata leads for resolving official indicator datasets before building data queries.",
    result_path=("value",),
    required_item_keys=("id", "name"),
    sample_filename="oecd_data_sample.xml",
    access_method="sdmx_dataflow_metadata",
    used_platform_tools=("sdmx_platform",),
    required_inputs=("query",),
    validation_notes=(
        "Validate the target dataflow, agency, version, and dimension key structure before issuing SDMX data requests.",
        "Dataflow metadata is discovery evidence and does not by itself choose the final dataset key or period filters.",
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
