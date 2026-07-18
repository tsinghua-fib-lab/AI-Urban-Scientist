from __future__ import annotations

from .repository_metadata_family import RepositoryMetadataConfig


GEOSPATIAL_JSON_CONFIGS: dict[str, RepositoryMetadataConfig] = {
    "planetary_computer": RepositoryMetadataConfig(
        source_skill_id="planetary_computer",
        source_card_id="planetary_computer_stac",
        publisher="Microsoft",
        landing_url="https://planetarycomputer.microsoft.com/catalog",
        docs_url="https://planetarycomputer.microsoft.com/docs/quickstarts/reading-stac/",
        search_url="https://planetarycomputer.microsoft.com/api/stac/v1/collections",
        source_family="stac_api",
        resolver_family="planetary_computer_stac_collections",
        entity_label="Microsoft Planetary Computer STAC catalog",
        route_description="Planetary Computer STAC collections endpoint for discovering cloud-native geospatial collections.",
        result_path=("collections",),
        required_item_keys=("id", "type"),
        sample_filename="planetary_computer_stac_collections_sample.json",
        access_method="stac_collections_api",
        required_inputs=(),
        validation_notes=(
            "Validate collection license, asset roles, temporal coverage, item search constraints, and signed asset requirements before download.",
            "Many assets require Planetary Computer SAS signing rather than direct anonymous blob access.",
        ),
    ),
    "nasa_earthdata_cmr": RepositoryMetadataConfig(
        source_skill_id="nasa_earthdata_cmr",
        source_card_id="nasa_earthdata_cmr_api",
        publisher="NASA",
        landing_url="https://www.earthdata.nasa.gov/",
        docs_url="https://cmr.earthdata.nasa.gov/search/site/docs/search/api.html",
        search_url="https://cmr.earthdata.nasa.gov/search/collections.json",
        source_family="nasa_cmr_api",
        resolver_family="nasa_cmr_collection_search",
        entity_label="NASA Earthdata CMR collections",
        route_description="NASA CMR collection search API for Earthdata dataset discovery.",
        result_path=("feed", "entry"),
        required_item_keys=("id", "title"),
        sample_filename="nasa_earthdata_cmr_collections_sample.json",
        access_method="cmr_collection_search_api",
        query_params=(("keyword", "{query}"), ("page_size", "10")),
        validation_notes=(
            "Validate Earthdata Login requirements, data center, processing level, temporal/spatial coverage, and granule download policy.",
            "Collection discovery does not prove granule files are immediately downloadable.",
        ),
    ),
    "copernicus_dataspace": RepositoryMetadataConfig(
        source_skill_id="copernicus_dataspace",
        source_card_id="copernicus_dataspace_stac",
        publisher="European Space Agency / Copernicus Data Space Ecosystem",
        landing_url="https://dataspace.copernicus.eu/",
        docs_url="https://documentation.dataspace.copernicus.eu/APIs/STAC.html",
        search_url="https://catalogue.dataspace.copernicus.eu/stac/collections",
        source_family="stac_api",
        resolver_family="copernicus_dataspace_stac_collections",
        entity_label="Copernicus Data Space STAC catalog",
        route_description="Copernicus Data Space STAC collections endpoint for Sentinel and contributing-mission discovery.",
        result_path=("collections",),
        required_item_keys=("id", "type"),
        sample_filename="copernicus_dataspace_stac_collections_sample.json",
        access_method="stac_collections_api",
        required_inputs=(),
        validation_notes=(
            "Validate collection license, authentication need, cloud cover/geometry constraints, and product download policy.",
            "Some Copernicus downloads require account tokens even when STAC metadata is public.",
        ),
    ),
    "google_open_buildings": RepositoryMetadataConfig(
        source_skill_id="google_open_buildings",
        source_card_id="google_open_buildings_hdx_catalog",
        publisher="Google Research / HDX",
        landing_url="https://sites.research.google/gr/open-buildings/",
        docs_url="https://data.humdata.org/organization/google-open-buildings",
        search_url="https://data.humdata.org/api/3/action/package_search",
        source_family="hdx_ckan_catalog_api",
        resolver_family="google_open_buildings_hdx_package_search",
        entity_label="Google Open Buildings HDX catalog",
        route_description="HDX CKAN package search constrained to the Google Open Buildings organization.",
        result_path=("result", "results"),
        required_item_keys=("id", "name", "title"),
        sample_filename="google_open_buildings_hdx_catalog_sample.json",
        access_method="ckan_package_search",
        query_params=(("fq", "organization:google-open-buildings"), ("rows", "10")),
        required_inputs=(),
        validation_notes=(
            "Validate whether the selected HDX package represents V3 polygons, 2.5D temporal data, or country/region extracts.",
            "Preserve Google Open Buildings license, caveats, confidence scores, and coverage limitations.",
        ),
    ),
}


def get_geospatial_json_config(source_skill_id: str) -> RepositoryMetadataConfig:
    return GEOSPATIAL_JSON_CONFIGS[source_skill_id]
