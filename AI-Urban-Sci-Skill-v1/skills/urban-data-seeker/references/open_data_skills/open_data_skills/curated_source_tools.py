from __future__ import annotations

import argparse
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any
from urllib.parse import quote

from open_data_skills.generic_resource_tools import run_access_check
from open_data_skills.lint_contract import assert_lint_clean
from open_data_skills.route_bridge import build_dossier_fragment, build_resource_intents
from open_data_skills.tool_contract import (
    build_tool_result,
    fail_closed_result,
    fetch_file_artifact,
    fetch_mode,
    fetch_text_with_live_gate,
    policy_allows,
    policy_reason,
    read_json_file,
    validation_check,
)


@dataclass(frozen=True)
class CandidateTemplate:
    label: str
    url: str
    role: str = "primary"
    access_method: str = "api_or_direct"
    resource_type: str = "landing"
    required_params: tuple[str, ...] = ()
    direct_download: bool = False
    notes: tuple[str, ...] = ()


@dataclass(frozen=True)
class CuratedSourceConfig:
    source_skill_id: str
    source_card_id: str
    publisher: str
    metadata_url: str
    access_status: str
    api_status: str
    authorization_required: bool = False
    not_open_download: bool = False
    credential_label: str = "credential"
    credential_env_var: str = ""
    candidates: tuple[CandidateTemplate, ...] = ()
    expected_suffixes: tuple[str, ...] = ()
    expected_fields: tuple[str, ...] = ()
    validation_notes: tuple[str, ...] = ()
    official_docs_checked: tuple[str, ...] = ()
    used_platform_tools: tuple[str, ...] = ()
    sample_filename: str = "sample.dat"


CONFIGS: dict[str, CuratedSourceConfig] = {
    "bea_fred_regional_economics": CuratedSourceConfig(
        source_skill_id="bea_fred_regional_economics",
        source_card_id="bea_fred_regional_economics_source",
        publisher="U.S. Bureau of Economic Analysis / Federal Reserve Bank of St. Louis",
        metadata_url="https://apps.bea.gov/api/signup/",
        access_status="key_gated",
        api_status="public_api_requires_key",
        authorization_required=True,
        credential_label="api_key",
        credential_env_var="BEA_API_KEY or FRED_API_KEY",
        candidates=(
            CandidateTemplate("BEA API dataset list", "https://apps.bea.gov/api/data?UserID={api_key}&method=GETDATASETLIST&ResultFormat=JSON", required_params=("api_key",), resource_type="api_json"),
            CandidateTemplate("BEA regional income", "https://apps.bea.gov/api/data?UserID={api_key}&method=GetData&datasetname=Regional&TableName={table_name}&LineCode={line_code}&GeoFIPS={geo_fips}&Year={year}&ResultFormat=JSON", required_params=("api_key", "table_name", "line_code", "geo_fips", "year"), resource_type="api_json"),
            CandidateTemplate("FRED series search", "https://api.stlouisfed.org/fred/series/search?search_text={query}&api_key={api_key}&file_type=json", required_params=("query", "api_key"), resource_type="api_json"),
        ),
        expected_fields=("BEAAPI", "seriess"),
        validation_notes=("Require BEA or FRED key before live requests.", "Validate series/table identity, geography code, frequency, and units."),
        official_docs_checked=("https://www.bea.gov/news/blog/2015-07-08/beas-api-expands-access-all-regional-data", "https://fred.stlouisfed.org/docs/api/fred/"),
        sample_filename="bea_fred_regional_economics_sample.json",
    ),
    "bikeshare_trip_history": CuratedSourceConfig(
        source_skill_id="bikeshare_trip_history",
        source_card_id="bikeshare_trip_history_source",
        publisher="Bikeshare operators",
        metadata_url="https://citibikenyc.com/system-data",
        access_status="open",
        api_status="bulk_download_only",
        candidates=(
            CandidateTemplate("Citi Bike tripdata index", "https://s3.amazonaws.com/tripdata/index.html", resource_type="html_index"),
            CandidateTemplate("Divvy tripdata index", "https://divvy-tripdata.s3.amazonaws.com/index.html", resource_type="html_index"),
            CandidateTemplate("Capital Bikeshare tripdata index", "https://s3.amazonaws.com/capitalbikeshare-data/index.html", resource_type="html_index"),
        ),
        expected_suffixes=(".zip", ".csv", ".html"),
        validation_notes=("Resolve operator archive month/quarter before download.", "Validate license, schema version, station IDs, timestamps, and privacy-suppressed fields."),
        official_docs_checked=("https://citibikenyc.com/system-data", "https://divvybikes.com/system-data", "https://capitalbikeshare.com/system-data"),
        sample_filename="bikeshare_trip_history_sample.html",
    ),
    "cloud_geospatial_catalogs": CuratedSourceConfig(
        source_skill_id="cloud_geospatial_catalogs",
        source_card_id="cloud_geospatial_catalogs_source",
        publisher="STAC / cloud geospatial catalog providers",
        metadata_url="https://stacspec.org/",
        access_status="open",
        api_status="public_catalog",
        candidates=(
            CandidateTemplate("Microsoft Planetary Computer STAC", "https://planetarycomputer.microsoft.com/api/stac/v1", resource_type="stac_landing"),
            CandidateTemplate("NASA CMR STAC", "https://cmr.earthdata.nasa.gov/stac/", resource_type="stac_landing"),
            CandidateTemplate("AWS Open Data Registry", "https://registry.opendata.aws/", resource_type="html_catalog"),
        ),
        expected_fields=("stac_version", "links", "collections"),
        validation_notes=("Validate catalog provider, collection ID, asset hrefs, license, cloud region, and signed URL requirements."),
        official_docs_checked=("https://stacspec.org/", "https://planetarycomputer.microsoft.com/docs/reference/stac/", "https://cmr.earthdata.nasa.gov/search/site/docs/search/stac", "https://registry.opendata.aws/"),
        sample_filename="cloud_geospatial_catalogs_sample.json",
    ),
    "elevation_lidar_topography": CuratedSourceConfig(
        source_skill_id="elevation_lidar_topography",
        source_card_id="elevation_lidar_topography_source",
        publisher="U.S. Geological Survey / OpenTopography",
        metadata_url="https://tnmaccess.nationalmap.gov/api/v1/docs",
        access_status="open",
        api_status="public_api",
        candidates=(
            CandidateTemplate("USGS TNMAccess elevation products", "https://tnmaccess.nationalmap.gov/api/v1/products?datasets={dataset}&bbox={bbox}&prodFormats={format}&max={max}", required_params=("dataset", "bbox", "format", "max"), resource_type="api_json"),
            CandidateTemplate("USGS LidarExplorer", "https://apps.nationalmap.gov/lidar-explorer/", resource_type="web_app"),
            CandidateTemplate("OpenTopography Global DEM API", "https://portal.opentopography.org/API/globaldem?demtype={demtype}&south={south}&north={north}&west={west}&east={east}&outputFormat=GTiff", required_params=("demtype", "south", "north", "west", "east"), resource_type="file_api", direct_download=True),
        ),
        expected_fields=("items", "downloadURL", "boundingBox"),
        expected_suffixes=(".tif", ".tiff", ".laz", ".las", ".zip", ".json"),
        validation_notes=("Validate vertical datum, resolution, product type, bbox, coordinate reference system, and file size."),
        official_docs_checked=("https://www.usgs.gov/faqs/there-api-accessing-national-map-data", "https://www.usgs.gov/3d-elevation-program", "https://opentopography.org/developers"),
        sample_filename="elevation_lidar_topography_sample.json",
    ),
    "environmental_facilities_compliance": CuratedSourceConfig(
        source_skill_id="environmental_facilities_compliance",
        source_card_id="environmental_facilities_compliance_source",
        publisher="U.S. Environmental Protection Agency",
        metadata_url="https://echo.epa.gov/tools/web-services",
        access_status="open",
        api_status="public_api",
        candidates=(
            CandidateTemplate("EPA ECHO CWA facilities", "https://echodata.epa.gov/echo/cwa_rest_services.get_facilities?output=JSON&p_st={state}&p_act=Y&responseset=1", required_params=("state",), resource_type="api_json"),
            CandidateTemplate("EPA ECHO detailed facility report", "https://echo.epa.gov/detailed-facility-report?fid={facility_id}", required_params=("facility_id",), resource_type="html_report"),
            CandidateTemplate("EPA TRI basic data files", "https://www.epa.gov/toxics-release-inventory-tri-program/tri-basic-data-files-calendar-years-1987-present", resource_type="download_page"),
        ),
        expected_fields=("Results", "RegistryID", "FacName"),
        validation_notes=("Validate facility identifiers, program system, state/county filters, compliance window, and enforcement action fields."),
        official_docs_checked=("https://echo.epa.gov/tools/web-services", "https://echo.epa.gov/tools/data-downloads", "https://www.epa.gov/frs"),
        sample_filename="environmental_facilities_compliance_sample.json",
    ),
    "environmental_justice_screening": CuratedSourceConfig(
        source_skill_id="environmental_justice_screening",
        source_card_id="environmental_justice_screening_source",
        publisher="EPA / OEHHA",
        metadata_url="https://19january2021snapshot.epa.gov/ejscreen/download-ejscreen-data_.html",
        access_status="open",
        api_status="bulk_download_only",
        candidates=(
            CandidateTemplate("EPA archived EJScreen download page", "https://19january2021snapshot.epa.gov/ejscreen/download-ejscreen-data_.html", resource_type="download_page"),
            CandidateTemplate("EPA EJScreen file directory", "https://gaftp.epa.gov/EJScreen/", resource_type="directory_index"),
            CandidateTemplate("CalEnviroScreen", "https://oehha.ca.gov/calenviroscreen", resource_type="download_page"),
        ),
        expected_suffixes=(".zip", ".csv", ".gdb", ".xlsx", ".html"),
        validation_notes=("Validate vintage, geography level, percentile basis, indicator definitions, and archived/current status."),
        official_docs_checked=("https://19january2021snapshot.epa.gov/ejscreen/download-ejscreen-data_.html", "https://oehha.ca.gov/calenviroscreen"),
        sample_filename="environmental_justice_screening_sample.html",
    ),
    "housing_market_data": CuratedSourceConfig(
        source_skill_id="housing_market_data",
        source_card_id="housing_market_data_source",
        publisher="Zillow Research / HUD USER / U.S. Census Bureau",
        metadata_url="https://www.zillow.com/research/data/",
        access_status="open",
        api_status="partial_programmatic_access",
        candidates=(
            CandidateTemplate("Zillow Research data page", "https://www.zillow.com/research/data/", resource_type="download_page"),
            CandidateTemplate("HUD FMR API documentation", "https://www.huduser.gov/portal/dataset/fmr-api.html", resource_type="api_docs"),
            CandidateTemplate("Census Building Permits Survey", "https://www.census.gov/permits", resource_type="download_page"),
        ),
        expected_suffixes=(".csv", ".xlsx", ".json", ".html"),
        validation_notes=("Validate geography level, metric definition, seasonality, housing type, vintage, and provider terms."),
        official_docs_checked=("https://www.zillow.com/research/data/", "https://www.huduser.gov/portal/dataset/fmr-api.html", "https://www.census.gov/permits"),
        sample_filename="housing_market_data_sample.html",
    ),
    "ipums_nhgis": CuratedSourceConfig(
        source_skill_id="ipums_nhgis",
        source_card_id="ipums_nhgis_source",
        publisher="IPUMS NHGIS",
        metadata_url="https://developer.ipums.org/docs/v2/apiprogram/apis/nhgis/",
        access_status="registration_required",
        api_status="public_api_requires_key",
        authorization_required=True,
        credential_label="api_key",
        credential_env_var="IPUMS_API_KEY",
        candidates=(
            CandidateTemplate("NHGIS metadata datasets", "https://api.ipums.org/metadata/nhgis/datasets?version=2", resource_type="api_json"),
            CandidateTemplate("NHGIS data extract API", "https://api.ipums.org/extracts/?collection=nhgis&version=1", resource_type="api_json", required_params=("api_key",)),
            CandidateTemplate("NHGIS GIS files", "https://www.nhgis.org/gis-files", resource_type="download_page"),
        ),
        expected_fields=("data", "datasets", "extracts"),
        validation_notes=("Require IPUMS API key for extract creation/download.", "Validate dataset/table/time series IDs, GIS boundary year, and citation/license requirements."),
        official_docs_checked=("https://developer.ipums.org/docs/v2/apiprogram/apis/nhgis/", "https://developer.ipums.org/docs/v1/reference/nhgis-data-extract/", "https://www.nhgis.org/gis-files"),
        sample_filename="ipums_nhgis_sample.json",
    ),
    "openaddresses_geocoding_base": CuratedSourceConfig(
        source_skill_id="openaddresses_geocoding_base",
        source_card_id="openaddresses_geocoding_base_source",
        publisher="OpenAddresses",
        metadata_url="https://openaddresses.io/",
        access_status="open",
        api_status="public_catalog",
        candidates=(
            CandidateTemplate("OpenAddresses download options", "https://openaddresses.io/", resource_type="download_page"),
            CandidateTemplate("OpenAddresses batch data", "https://batch.openaddresses.io/data", resource_type="web_app_or_api"),
            CandidateTemplate("OpenAddresses source repository", "https://github.com/openaddresses/openaddresses", resource_type="source_catalog"),
        ),
        expected_suffixes=(".zip", ".csv", ".json", ".html"),
        validation_notes=("Validate source license, attribution requirement, country/region source file, and whether batch output is currently accessible."),
        official_docs_checked=("https://openaddresses.io/", "https://github.com/openaddresses/openaddresses", "https://github.com/openaddresses/batch-machine"),
        sample_filename="openaddresses_geocoding_base_sample.html",
    ),
    "osm_geofabrik_extracts": CuratedSourceConfig(
        source_skill_id="osm_geofabrik_extracts",
        source_card_id="osm_geofabrik_extracts_source",
        publisher="Geofabrik / OpenStreetMap",
        metadata_url="https://www.geofabrik.de/data/download.html",
        access_status="open",
        api_status="bulk_download_only",
        candidates=(
            CandidateTemplate("Geofabrik download server", "https://download.geofabrik.de/", resource_type="directory_index"),
            CandidateTemplate("Geofabrik region PBF", "https://download.geofabrik.de/{region_path}-latest.osm.pbf", required_params=("region_path",), resource_type="direct_file", direct_download=True),
            CandidateTemplate("Geofabrik region shapefile", "https://download.geofabrik.de/{region_path}-latest-free.shp.zip", required_params=("region_path",), resource_type="direct_file", direct_download=True),
        ),
        expected_suffixes=(".osm.pbf", ".shp.zip", ".md5", ".html"),
        validation_notes=("Validate region path, ODbL attribution, update date, file size, and whether personal metadata is excluded."),
        official_docs_checked=("https://www.geofabrik.de/data/download.html", "https://download.geofabrik.de/"),
        sample_filename="osm_geofabrik_extracts_sample.html",
    ),
    "parcel_land_use_records": CuratedSourceConfig(
        source_skill_id="parcel_land_use_records",
        source_card_id="parcel_land_use_records_source",
        publisher="Local parcel and planning agencies",
        metadata_url="https://data.cityofnewyork.us/City-Government/Primary-Land-Use-Tax-Lot-Output-PLUTO-/64uk-42ks",
        access_status="open",
        api_status="partial_programmatic_access",
        candidates=(
            CandidateTemplate("NYC PLUTO Socrata API", "https://data.cityofnewyork.us/resource/64uk-42ks.json?$limit={limit}", required_params=("limit",), resource_type="api_json"),
            CandidateTemplate("NYC MapPLUTO Socrata API", "https://data.cityofnewyork.us/resource/f888-ni5f.json?$limit={limit}", required_params=("limit",), resource_type="api_json"),
            CandidateTemplate("NYC DCP PLUTO documentation", "https://www.nyc.gov/content/planning/pages/resources/datasets/mappluto-pluto-change", resource_type="download_page"),
        ),
        expected_fields=("bbl", "borough", "lotarea", "landuse"),
        validation_notes=("Validate jurisdiction, parcel ID, geometry availability, zoning/land-use field definitions, and license constraints."),
        official_docs_checked=("https://www.nyc.gov/content/planning/pages/resources/datasets/mappluto-pluto-change", "https://data.cityofnewyork.us/City-Government/Primary-Land-Use-Tax-Lot-Output-PLUTO-/64uk-42ks"),
        sample_filename="parcel_land_use_records_sample.json",
    ),
    "street_level_imagery": CuratedSourceConfig(
        source_skill_id="street_level_imagery",
        source_card_id="street_level_imagery_source",
        publisher="Mapillary / KartaView",
        metadata_url="https://www.mapillary.com/developer/api-documentation",
        access_status="key_gated",
        api_status="public_api_requires_key",
        authorization_required=True,
        credential_label="access_token",
        credential_env_var="MAPILLARY_ACCESS_TOKEN",
        candidates=(
            CandidateTemplate("Mapillary image search", "https://graph.mapillary.com/images?bbox={bbox}&fields=id,geometry,computed_compass_angle,captured_at&access_token={access_token}", required_params=("bbox", "access_token"), resource_type="api_json"),
            CandidateTemplate("KartaView nearby photos", "https://api.openstreetcam.org/2.0/photo/?lat={lat}&lng={lng}&distance={distance}", required_params=("lat", "lng", "distance"), resource_type="api_json"),
            CandidateTemplate("KartaView photos documentation", "https://kartaview.org/doc/photos", resource_type="api_docs"),
        ),
        expected_fields=("data", "id", "geometry"),
        validation_notes=("Do not bulk-download imagery by default; validate API terms, token scope, geometry, timestamps, and privacy redaction."),
        official_docs_checked=("https://www.mapillary.com/developer/api-documentation", "https://help.mapillary.com/hc/en-us/articles/360010234680-Accessing-imagery-and-data-through-the-Mapillary-API", "https://kartaview.org/doc/photos"),
        sample_filename="street_level_imagery_sample.json",
    ),
    "transit_agency_performance": CuratedSourceConfig(
        source_skill_id="transit_agency_performance",
        source_card_id="transit_agency_performance_source",
        publisher="Federal Transit Administration",
        metadata_url="https://www.transit.dot.gov/ntd",
        access_status="open",
        api_status="public_api",
        candidates=(
            CandidateTemplate("NTD agency metrics Socrata API", "https://data.transportation.gov/resource/g27i-aq2u.json?$limit={limit}", required_params=("limit",), resource_type="api_json"),
            CandidateTemplate("NTD service by agency Socrata API", "https://data.transportation.gov/resource/6y83-7vuw.json?$limit={limit}", required_params=("limit",), resource_type="api_json"),
            CandidateTemplate("FTA NTD data", "https://www.transit.dot.gov/ntd/ntd-data", resource_type="download_page"),
        ),
        expected_fields=("ntd_id", "agency", "report_year"),
        validation_notes=("Validate report year, agency identifier, mode/type of service, annual vs monthly product, and metric definition."),
        official_docs_checked=("https://www.transit.dot.gov/ntd", "https://www.transit.dot.gov/ntd/ntd-data", "https://data.transportation.gov/Public-Transit/NTD-Annual-Data-View-Metrics-by-Agency-/g27i-aq2u"),
        sample_filename="transit_agency_performance_sample.json",
    ),
    "transportation_safety_performance": CuratedSourceConfig(
        source_skill_id="transportation_safety_performance",
        source_card_id="transportation_safety_performance_source",
        publisher="NHTSA / FHWA",
        metadata_url="https://crashviewer.nhtsa.dot.gov/CrashAPI",
        access_status="open",
        api_status="public_api",
        candidates=(
            CandidateTemplate("NHTSA FARS crash API", "https://crashviewer.nhtsa.dot.gov/CrashAPI/crashes/GetCaseList?states={states}&fromYear={from_year}&toYear={to_year}&format=json", required_params=("states", "from_year", "to_year"), resource_type="api_json"),
            CandidateTemplate("NHTSA FARS documentation", "https://www.nhtsa.gov/research-data/fatality-analysis-reporting-system-fars", resource_type="docs"),
            CandidateTemplate("FHWA HPMS", "https://www.fhwa.dot.gov/policyinformation/hpms.cfm", resource_type="download_page"),
        ),
        expected_fields=("Results", "CaseYear", "State"),
        validation_notes=("Validate crash system, year coverage, state codes, fatal/injury definitions, and whether query is initial or final release."),
        official_docs_checked=("https://www.nhtsa.gov/research-data/fatality-analysis-reporting-system-fars", "https://crashviewer.nhtsa.dot.gov/CrashAPI", "https://www.fhwa.dot.gov/policyinformation/hpms.cfm"),
        sample_filename="transportation_safety_performance_sample.json",
    ),
    "urban_traffic_sensors": CuratedSourceConfig(
        source_skill_id="urban_traffic_sensors",
        source_card_id="urban_traffic_sensors_source",
        publisher="State and local transportation agencies",
        metadata_url="https://www.nyc.gov/html/dot/html/about/datafeeds.shtml",
        access_status="registration_required",
        api_status="partial_programmatic_access",
        authorization_required=True,
        credential_label="provider_account_or_token",
        credential_env_var="PEMS_TOKEN or agency-specific credential",
        candidates=(
            CandidateTemplate("NYC DOT Traffic Speeds Socrata API", "https://data.cityofnewyork.us/resource/i4gi-tjb9.json?$limit={limit}", required_params=("limit",), resource_type="api_json"),
            CandidateTemplate("NYC DOT data feeds", "https://www.nyc.gov/html/dot/html/about/datafeeds.shtml", resource_type="download_page"),
            CandidateTemplate("Caltrans PeMS", "https://dot.ca.gov/programs/traffic-operations/mpr/pems-source", resource_type="portal_registration"),
        ),
        expected_fields=("link_id", "speed", "travel_time"),
        validation_notes=("Validate detector/feed owner, timestamp latency, road segment identifier, units, account/license requirements, and historical retention."),
        official_docs_checked=("https://dot.ca.gov/programs/traffic-operations/mpr/pems-source", "https://www.nyc.gov/html/dot/html/about/datafeeds.shtml", "https://data.cityofnewyork.us/Transportation/DOT-Traffic-Speeds/i4gi-tjb9"),
        sample_filename="urban_traffic_sensors_sample.json",
    ),
}


def run_curated_access_check(*, source_skill_id: str) -> None:
    config = CONFIGS[source_skill_id]
    run_access_check(
        source_skill_id=config.source_skill_id,
        publisher=config.publisher,
        metadata_url=config.metadata_url,
        access_status=config.access_status,
        authorization_required=config.authorization_required,
        not_open_download=config.not_open_download,
        used_platform_tools=list(config.used_platform_tools),
    )


def run_curated_find(*, source_skill_id: str) -> None:
    config = CONFIGS[source_skill_id]
    parser = argparse.ArgumentParser(description=f"Emit source-specific {source_skill_id} candidates.")
    parser.add_argument("--need-id", required=True)
    parser.add_argument("--need-text", required=True)
    parser.add_argument("--query", default="")
    parser.add_argument("--geography", default="")
    parser.add_argument("--time-range", default="")
    parser.add_argument("--params-json", default="")
    args = parser.parse_args()
    params = _load_params(args.params_json)
    params.setdefault("query", args.query)
    payload = build_find_payload(
        config,
        need_id=args.need_id,
        need_text=args.need_text,
        query=args.query,
        geography=args.geography,
        time_range=args.time_range,
        params=params,
    )
    _print(payload)


def run_curated_probe(*, source_skill_id: str) -> None:
    config = CONFIGS[source_skill_id]
    parser = argparse.ArgumentParser(description=f"Probe {source_skill_id} source-specific candidate.")
    parser.add_argument("--policy", default="discovery_only")
    parser.add_argument("--url", default="")
    parser.add_argument("--fixture-response", default="")
    parser.add_argument("--fixture-file", default="")
    args = parser.parse_args()
    input_payload = {
        "url": args.url,
        "fixture_response": bool(args.fixture_response),
        "fixture_file": bool(args.fixture_file),
        "download_mode": fetch_mode(args.policy),
        "authorization_required": config.authorization_required,
    }
    provenance = {"source_url": args.url, "metadata_url": config.metadata_url, "publisher": config.publisher}
    if not policy_allows(args.policy, "probe"):
        _print(fail_closed_result(source_skill_id=config.source_skill_id, tool_type="probe", policy=args.policy, input_payload=input_payload, reason=policy_reason(args.policy, "probe"), provenance=provenance, used_platform_tools=list(config.used_platform_tools)))
        return
    try:
        payload = _load_probe_payload(args.fixture_response, args.fixture_file, args.url)
        checks = _checks(config, payload, args.url or args.fixture_file or args.fixture_response)
        result = {"status": "probe_requestable" if all(check["passed"] for check in checks) else "needs_follow_up"}
    except Exception as exc:
        checks = [validation_check("probe_exception", False, reason=type(exc).__name__)]
        result = {"status": "needs_follow_up", "reason": str(exc)}
    _print(build_tool_result(source_skill_id=config.source_skill_id, tool_type="probe", policy=args.policy, input_payload=input_payload, result=result, provenance=provenance, validation={"checks": checks}, used_platform_tools=list(config.used_platform_tools)))


def run_curated_fetch(*, source_skill_id: str) -> None:
    config = CONFIGS[source_skill_id]
    parser = argparse.ArgumentParser(description=f"Fetch a policy-gated {source_skill_id} sample.")
    parser.add_argument("--policy", default="discovery_only")
    parser.add_argument("--url", default="")
    parser.add_argument("--fixture-file", default="")
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--max-bytes", type=int, default=1_000_000)
    args = parser.parse_args()
    input_payload = {
        "url": args.url,
        "fixture_file": bool(args.fixture_file),
        "max_bytes": args.max_bytes,
        "download_mode": fetch_mode(args.policy),
        "authorization_required": config.authorization_required,
    }
    provenance = {"source_url": args.url, "metadata_url": config.metadata_url, "publisher": config.publisher}
    if not policy_allows(args.policy, "fetch"):
        _print(fail_closed_result(source_skill_id=config.source_skill_id, tool_type="fetch", policy=args.policy, input_payload=input_payload, reason=policy_reason(args.policy, "fetch"), provenance=provenance, used_platform_tools=list(config.used_platform_tools)))
        return
    if not args.url and not args.fixture_file:
        _print(fail_closed_result(source_skill_id=config.source_skill_id, tool_type="fetch", policy=args.policy, input_payload=input_payload, reason="url_or_fixture_file_required", provenance=provenance, used_platform_tools=list(config.used_platform_tools)))
        return
    try:
        target = Path(args.output_dir) / config.sample_filename
        artifact = fetch_file_artifact(fixture_file=args.fixture_file or None, url=args.url, target=target, policy=args.policy, max_bytes=args.max_bytes)
        checks = [
            validation_check("sample_written", True),
            validation_check("source_specific_fetcher", True),
            validation_check("fetch_scope", True, download_mode=fetch_mode(args.policy), max_bytes=args.max_bytes),
        ]
        result = {"status": "fetched", "size_bytes": Path(artifact["path"]).stat().st_size}
        artifacts = [artifact]
    except Exception as exc:
        checks = [validation_check("fetch_exception", False, reason=type(exc).__name__)]
        result = {"status": "needs_follow_up", "reason": str(exc)}
        artifacts = []
    _print(build_tool_result(source_skill_id=config.source_skill_id, tool_type="fetch", policy=args.policy, input_payload=input_payload, result=result, provenance=provenance, artifacts=artifacts, validation={"checks": checks}, used_platform_tools=list(config.used_platform_tools)))


def run_curated_validate(*, source_skill_id: str) -> None:
    config = CONFIGS[source_skill_id]
    parser = argparse.ArgumentParser(description=f"Validate a {source_skill_id} sample.")
    parser.add_argument("--policy", default="discovery_only")
    parser.add_argument("--input-file", required=True)
    args = parser.parse_args()
    input_payload = {"input_file": args.input_file}
    provenance = {"source_url": "", "metadata_url": config.metadata_url, "publisher": config.publisher}
    if not policy_allows(args.policy, "validate"):
        _print(fail_closed_result(source_skill_id=config.source_skill_id, tool_type="validate", policy=args.policy, input_payload=input_payload, reason=policy_reason(args.policy, "validate"), provenance=provenance, used_platform_tools=list(config.used_platform_tools)))
        return
    try:
        payload = _load_input_file(args.input_file)
        checks = _checks(config, payload, args.input_file)
        result = {"status": "validation_passed" if all(check["passed"] for check in checks) else "validation_failed"}
    except Exception as exc:
        checks = [validation_check("validate_exception", False, reason=type(exc).__name__)]
        result = {"status": "validation_failed", "reason": str(exc)}
    _print(build_tool_result(source_skill_id=config.source_skill_id, tool_type="validate", policy=args.policy, input_payload=input_payload, result=result, provenance=provenance, validation={"checks": checks}, used_platform_tools=list(config.used_platform_tools)))


def build_find_payload(
    config: CuratedSourceConfig,
    *,
    need_id: str,
    need_text: str,
    query: str,
    geography: str,
    time_range: str,
    params: dict[str, str],
) -> dict[str, Any]:
    resources = []
    for template in config.candidates:
        missing = [param for param in template.required_params if not params.get(param)]
        url = _format_url(template.url, params)
        resources.append(
            {
                "url": url,
                "role": template.role,
                "label": template.label,
                "access_method": template.access_method,
                "source_skill_id": config.source_skill_id,
                "source_card_id": config.source_card_id,
                "need_ids": [need_id],
                "publisher": config.publisher,
                "resource_type": template.resource_type,
                "executability_hint": "resolvable_resource" if not missing else "source_landing",
                "required_params": list(template.required_params),
                "missing_params": missing,
                "download_candidate": {
                    "url": url,
                    "is_direct_download_candidate": bool(template.direct_download and not missing),
                    "reason": "source_specific_candidate_requires_probe_before_fetch",
                },
                "required_validation": ["source", "access", "schema", "geography", "time_period", "license"],
                "validation_notes": _as_list(config.validation_notes) + _as_list(template.notes),
            }
        )
    fragment = build_dossier_fragment(
        source_skill_id=config.source_skill_id,
        source_card_id=config.source_card_id,
        need_ids=[need_id],
        route_goal=need_text,
        candidate_resources=resources,
        positive_evidence=[{"type": "source_specific_tooling", "message": f"{config.source_skill_id} emits source-specific candidates rather than generic source-prior hints."}],
        negative_evidence=[],
    )
    fragment["ambiguities"] = [{"type": "source_parameters", "message": "Resolve missing source-specific parameters before approving download."}]
    fragment["verification_notes"] = _as_list(config.validation_notes)
    fragment["executability_hint"] = "resolvable_resource" if any(not r["missing_params"] for r in resources) else "source_landing"
    payload = {
        "source_skill_id": config.source_skill_id,
        "source_card_id": config.source_card_id,
        "finality": "not_final",
        "consumer_authority": "none",
        "query": {
            "need_id": need_id,
            "need_text": need_text,
            "query": query,
            "geography": geography,
            "time_range": time_range,
            "params": params,
        },
        "candidate_resources": resources,
        "route_dossier_fragment": fragment,
        "resource_intents": build_resource_intents(fragment),
    }
    assert_lint_clean(payload)
    return payload


def _load_params(value: str) -> dict[str, str]:
    if not value:
        return {}
    payload = json.loads(value)
    if not isinstance(payload, dict):
        raise ValueError("--params-json must be a JSON object")
    return {str(k): str(v) for k, v in payload.items() if v is not None}


def _format_url(template: str, params: dict[str, str]) -> str:
    safe_params = {key: _safe_value(params.get(key, "{" + key + "}")) for key in _field_names(template)}
    return template.format(**safe_params)


def _field_names(template: str) -> list[str]:
    names: list[str] = []
    start = 0
    while True:
        left = template.find("{", start)
        if left == -1:
            return names
        right = template.find("}", left)
        if right == -1:
            return names
        names.append(template[left + 1 : right])
        start = right + 1


def _safe_value(value: str) -> str:
    if value.startswith("{") and value.endswith("}"):
        return value
    return quote(value, safe="/:,{}$.-_")


def _as_list(value: Any) -> list[str]:
    if value in (None, ""):
        return []
    if isinstance(value, str):
        return [value]
    return [str(item) for item in value]


def _load_probe_payload(fixture_response: str, fixture_file: str, url: str) -> Any:
    if fixture_response:
        return read_json_file(fixture_response)
    if fixture_file:
        return _load_input_file(fixture_file)
    if not url:
        return {"candidate_url_present": False}
    text = fetch_text_with_live_gate(url, max_bytes=512_000)
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return {"text_sample": text[:10000], "content_kind": "text"}


def _load_input_file(path: str) -> Any:
    target = Path(path)
    if target.suffix.lower() == ".json":
        return read_json_file(target)
    data = target.read_bytes()
    try:
        return {"text_sample": data[:20000].decode("utf-8", errors="replace"), "size_bytes": target.stat().st_size}
    except Exception:
        return {"binary_sample": True, "size_bytes": target.stat().st_size}


def _checks(config: CuratedSourceConfig, payload: Any, target: str) -> list[dict[str, Any]]:
    checks = [
        validation_check("source_specific_config", True),
        validation_check("target_present", bool(target)),
    ]
    if config.expected_suffixes and target:
        checks.append(validation_check("expected_suffix_or_probeable_url", _suffix_ok(target, config.expected_suffixes) or target.startswith("http"), expected_suffixes=list(config.expected_suffixes)))
    if isinstance(payload, dict):
        checks.append(validation_check("payload_shape", True))
        if config.expected_fields:
            checks.append(validation_check("expected_field_hint", any(_field_present(payload, field) for field in config.expected_fields), expected_fields=list(config.expected_fields)))
        else:
            checks.append(validation_check("payload_nonempty", bool(payload)))
    elif isinstance(payload, list):
        checks.append(validation_check("payload_shape", True))
        checks.append(validation_check("payload_nonempty", bool(payload)))
    else:
        checks.append(validation_check("payload_shape", False))
    return checks


def _suffix_ok(target: str, suffixes: tuple[str, ...]) -> bool:
    lowered = target.lower()
    return any(lowered.endswith(suffix.lower()) for suffix in suffixes)


def _field_present(payload: Any, field: str) -> bool:
    if isinstance(payload, dict):
        if field in payload:
            return True
        return any(_field_present(value, field) for value in payload.values() if isinstance(value, (dict, list)))
    if isinstance(payload, list):
        return any(_field_present(item, field) for item in payload[:20])
    return False


def _print(payload: dict[str, Any]) -> None:
    print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
