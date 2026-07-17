from __future__ import annotations

import sys
from pathlib import Path

OPEN_DATA_SKILLS_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(OPEN_DATA_SKILLS_ROOT))

from open_data_skills.catalog_csv_family import CatalogCsvConfig, build_catalog_csv_payload, run_find_cli


CONFIG = CatalogCsvConfig(
    source_skill_id="microsoft_building_footprints",
    source_card_id="microsoft_global_ml_building_footprints",
    publisher="Microsoft",
    landing_url="https://github.com/microsoft/GlobalMLBuildingFootprints",
    docs_url="https://github.com/microsoft/GlobalMLBuildingFootprints",
    catalog_url="https://minedbuildings.z5.web.core.windows.net/global-buildings/dataset-links.csv",
    source_family="microsoft_global_buildings_csv_catalog",
    resolver_family="microsoft_building_quadkey_catalog_filter",
    entity_label="Microsoft Global ML Building Footprints dataset-links catalog",
    route_description="Microsoft Global ML Building Footprints dataset-links CSV listing current regional/quadkey CSV.GZ resources.",
    sample_filename="microsoft_building_footprints_dataset_links_sample.csv",
    required_columns=("Location", "QuadKey", "Url", "Size", "UploadDate"),
    access_method="dataset_links_csv",
    validation_notes=(
        "The old minedbuildings.blob.core.windows.net URL is no longer public; use the z5.web.core.windows.net hosting listed by the official repository.",
        "Validate region name, quadkey coverage, file size, upload date, schema, confidence fields, and license before downloading large CSV.GZ resources.",
    ),
)


def build_payload(*, need_id: str, need_text: str, query: str, geography: str, time_range: str) -> dict[str, object]:
    return build_catalog_csv_payload(
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
