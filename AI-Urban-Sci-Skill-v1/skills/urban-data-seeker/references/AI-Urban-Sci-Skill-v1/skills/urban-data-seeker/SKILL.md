---
name: urban-data-seeker
description: "Find, route, probe, sample, validate, and conditionally download authoritative urban datasets using a curated bundle of 25 high-utility platform and concrete source skills. Use when Codex needs urban, city, mobility, demographics, geospatial, environmental, public-document, legislation, repository, statistical API, transit, weather, remote-sensing, building-footprint, or open-data portal datasets and must choose the right source/API/platform mechanics, access boundary, schema, license, geography, and time coverage before acquisition."
---

# Urban Data Seeker

Use this skill as the only top-level router for urban dataset discovery and acquisition. Route by data type first, then choose the most specific source skill. If no bundled source skill covers the data type, use platform skills as fallback discovery entrypoints.

## Core Rule

Classify the request into a data type before opening downstream skills. Prefer source skills when the data type maps cleanly to one. Use platform skills as both technical adapters and fallback discovery entrypoints when the source is unknown, missing from this bundle, or provided only as a portal/protocol clue.

## Workflow

1. Parse the request into `data_type`, `source_name`, `url_or_domain`, `geography`, `time_range`, `granularity`, `format`, `action`, and `access_preference`.
2. If the request names a bundled source, route directly to that source skill.
3. If the request supplies a URL or explicit protocol fingerprint, route to the matching platform skill when the source itself is not already clear.
4. Otherwise select the source skill from the Data-Type Routing Matrix below.
5. Run the deterministic router as a sanity check or tie-breaker, not as the primary conceptual router:
   - `python3 scripts/route_data_request.py --query "{user_request}" --top-k 5`
   - Add `--url "{url}"` when the user supplies a URL.
6. Prefer final route types in this order: exact source alias, data-type source match, URL/domain fingerprint, platform fingerprint.
7. Open only the top 1-3 selected source/platform `skill_path` values.
8. Resolve `references/...` inside a selected downstream skill relative to that selected skill directory. Resolve `references/platforms/...` relative to this `urban-data-seeker` skill root.
9. Probe before fetching data. Validate source authority, schema, license, geography, time coverage, format, file size, and access terms before full download.
10. If no bundled source route is viable, select a platform fallback from the Platform Fallback Rules below. Report `external_candidate_required` only when no source, platform, catalog, document, repository, or protocol route can be justified.

## Data-Type Routing Matrix

Use this matrix before relying on generic text similarity. When multiple sources match, choose by geography, granularity, authority, access, and requested output format.

### 1. Social And Economic Baselines

#### Population And Demographics

- Use `census-acs` for U.S. ACS demographic, socioeconomic, housing, commute, education, income, race, tract, block-group, county, place, ACS table, variable, estimate, or margin-of-error requests.
- Use `us-tiger-boundaries` alongside `census-acs` only when the user needs official Census geometry to join with ACS attributes.
- If the geography is outside the U.S. and the request asks for country-level indicators, prefer `world-bank-indicators`, `oecd-data`, or `who-gho` depending on the measure.

#### Economy And Labor

- Use `world-bank-indicators` for global or country-year development indicators such as GDP, poverty, population, urbanization, health, education, and broad economic series.
- Use `oecd-data` for OECD countries, regions, metro areas, SDMX dataflows, labor, education, economy, environment, regional, or city statistics.
- Use `sdmx-platform` only when the source is already known to expose SDMX mechanics and the task is about dataflows, codelists, dimensions, or series keys.

#### Health And Social Conditions

- Use `who-gho` for WHO Global Health Observatory indicators, mortality, disease burden, health systems, SDG health indicators, OData entity sets, country/year/dimension combinations.
- Use `odata-platform` only when the request or selected source explicitly exposes OData mechanics such as `$metadata`, `$filter`, `$select`, `$top`, or `$skip`.

### 2. Environment And Natural Resources

#### Weather And Climate

- Use `noaa-weather` for NOAA/NCEI/CDO weather and climate station observations, daily summaries, hourly LCD, station inventories, temperature, precipitation, wind, and U.S. or global station data.

#### Air Quality

- Use `open-aq` for OpenAQ air-quality measurements, sensors, stations, PM2.5, PM10, NO2, O3, SO2, CO, provider aggregation, hourly observations, API queries, and bounded samples.

#### Energy, Hydrology, And Hazards

- This bundle has no dedicated source skill for energy, hydrology, or disasters. Use platform fallback before declaring a gap: `data-gov-catalog` or `ckan-platform` for official catalog search, `arcgis-platform` for geospatial layers, `hdx-catalog` for humanitarian/disaster data, and `socrata-platform` for city open-data portals.

### 3. Remote Sensing And Geospatial Data

#### Remote Sensing And Earth Observation

- Use `nasa-earthdata-cmr` for NASA Earthdata CMR collection/granule discovery, MODIS, Landsat, SRTM, NASA products, keyword, short_name, bbox, temporal filters, and Earthdata Login boundaries.
- Use `planetary-computer` for Microsoft Planetary Computer STAC collections, Sentinel-2, Landsat, NAIP, cloud-hosted rasters, signed asset URLs, and asset-level STAC access.
- Use `stac-platform` for generic STAC endpoints when the host is not specifically Planetary Computer or NASA CMR.

#### Land Cover, Built Form, And Open Geospatial Features

- Use `microsoft-building-footprints` for global ML building footprints, country shards, building polygons, built-environment density, and urban morphology analysis.
- Use `osm-geofabrik-extracts` for OpenStreetMap regional extracts, PBF, shapefiles, roads, buildings, POIs, land use, and large-area OSM downloads.

#### Administrative Boundaries And Geography

- Use `us-tiger-boundaries` for U.S. Census TIGER/Line and cartographic boundary files, tract, block group, county, place, ZCTA, shapefile, geodatabase, and GEOID joins.
- Use `arcgis-platform`, `ckan-platform`, or `data-gov-catalog` only when an official boundary dataset is supplied through that platform and no more specific bundled source applies.

### 4. Transport And Mobility

- Use `gtfs-feed` for static transit schedules, GTFS routes, stops, trips, stop_times, calendar, shapes, agency feeds, and accessibility or network modeling.
- Use `gbfs-bikeshare` for GBFS bikeshare or micromobility station status, station information, vehicle availability, docks, and near-real-time feed queries.
- Use `nyc-tlc` for New York City yellow taxi, green taxi, FHV, trip records, monthly Parquet files, pickup/dropoff zones, fares, timestamps, and taxi mobility analysis.

### 5. Governance, Portals, Documents, And Research Repositories

- Use `data-gov-catalog` for U.S. Data.gov federal catalog records, CKAN-backed package search, agency datasets, and resource URL resolution.
- Use `hdx-catalog` for Humanitarian Data Exchange datasets, disaster, conflict, humanitarian operations, administrative boundaries, food security, refugees, health, and country-level humanitarian open data.
- Use `document-portal-platform` for official HTML/PDF document portals, planning documents, comprehensive plans, zoning texts, environmental reports, and versioned municipal documents.
- Use `legistar-platform` for Legistar/Granicus municipal legislation, ordinances, resolutions, agendas, meeting minutes, votes, matter IDs, file IDs, and attachments.
- Use `dataverse-platform` when a repository page is Dataverse, `dataset.xhtml`, `persistentId`, `/api/datasets/`, or `/api/access/datafile/`.

### 6. Platform Technical Adapters

Use these after source/protocol evidence exists, or as fallback discovery entrypoints when the data type is covered only by portals/catalogs in this bundle:

- `socrata-platform`: SODA/SoQL, Socrata catalog/view metadata, CSV/JSON/GeoJSON exports, app-token/quota behavior.
- `arcgis-platform`: ArcGIS REST FeatureServer/MapServer, layer metadata, fields, extent, `/query`, bbox, outFields.
- `ckan-platform`: CKAN Action API, `package_search`, `package_show`, `resources[].url`, HEAD probes.
- `dataverse-platform`: Dataverse persistent IDs, dataset versions, file metadata, restricted files, `/api/access/datafile/`.
- `stac-platform`: STAC `/collections`, item search, assets, bbox, datetime, cloud-cover filters.
- `sdmx-platform`: SDMX dataflows, dimensions, codelists, series keys, time series.
- `odata-platform`: OData `$metadata`, entity sets, `$filter`, `$select`, `$top`, `$skip`.
- `document-portal-platform`: official HTML/PDF landing pages, document discovery, file/version validation.
- `legistar-platform`: Legistar/Granicus matter/file ID resolution, agenda, vote, attachment metadata.

## Platform Fallback Rules

When no bundled source skill directly covers the data type, do not stop. Select a platform fallback:

- Local tabular city datasets, permits, inspections, 311, crashes, facilities, code enforcement: prefer `socrata-platform`, then `ckan-platform`.
- Official U.S. federal or cross-agency datasets: prefer `data-gov-catalog`, then `ckan-platform`.
- Humanitarian, disaster, refugee, food-security, crisis, or country operations data: prefer `hdx-catalog`, then `ckan-platform`.
- Geospatial layers, parcels, land use, utilities, hazards, flood maps, public facilities, zoning layers: prefer `arcgis-platform`, then `ckan-platform` or `data-gov-catalog`.
- Remote-sensing catalogs not clearly NASA CMR or Planetary Computer: prefer `stac-platform`.
- Indicator APIs without a selected provider but with SDMX clues: prefer `sdmx-platform`.
- Indicator APIs with OData clues: prefer `odata-platform`.
- Planning, zoning, environmental review, policy, or report PDFs/HTML: prefer `document-portal-platform`.
- Ordinances, agendas, votes, resolutions, meeting minutes, or municipal legislation: prefer `legistar-platform`.
- Repository pages with Dataverse fingerprints: prefer `dataverse-platform`.

For fallback routes, return `route_type: platform_fallback`, make the next step a catalog/search/probe action, and state what concrete source/dataset still needs to be selected.

## Residual Gaps

Use `external_candidate_required` only after platform fallback fails or is clearly inappropriate. Common cases include requests for a named provider not bundled here, commercial or restricted mobility/location products, source-specific APIs outside these platform patterns, or domains requiring a dedicated source skill for licensing/schema semantics.

## Bundled Resources

- `references/route_index.compact.jsonl`: compact deterministic routing index for the 25 selected skills.
- `references/selected_skills.json`: selected skill inventory, selection rationale, and route metadata.
- `references/routing_rules.md`: scoring rules, priority order, and access-boundary conventions.
- `references/native_skills/`: the 25 selected downstream skill directories.
- `references/platforms/`: copied platform packages needed by platform skills.

## Scripts

- `scripts/route_data_request.py`: score the compact index and return ranked candidate skills.
- `scripts/inspect_skill.py`: print a selected skill's key files, sections, and available scripts.
- `scripts/validate_data_seeker_bundle.py`: validate the integrated bundle after edits.

## Selected Skill Set

Keep only platform and concrete source skills in this bundle. The data-type matrix above decides which of these to open.

- Platform: `socrata-platform`, `arcgis-platform`, `ckan-platform`, `dataverse-platform`, `stac-platform`, `sdmx-platform`, `odata-platform`, `document-portal-platform`, `legistar-platform`.
- Concrete high-frequency sources: `census-acs`, `us-tiger-boundaries`, `osm-geofabrik-extracts`, `open-aq`, `nyc-tlc`, `data-gov-catalog`, `hdx-catalog`, `world-bank-indicators`, `oecd-data`, `who-gho`, `noaa-weather`, `gtfs-feed`, `gbfs-bikeshare`, `nasa-earthdata-cmr`, `planetary-computer`, `microsoft-building-footprints`.

## Output Contract

Return:

- `selected_skill`: chosen downstream skill name.
- `route_type`: `exact_source`, `data_type_source`, `url_domain`, `platform_fingerprint`, `source_topic`, or `platform_fallback`.
- `confidence`: high, medium, or low.
- `why`: concise routing evidence.
- `next_probe`: exact metadata/API/catalog probe to run next.
- `access_boundary`: `none`, `api_key_optional`, `api_key_required`, `login_required`, `restricted`, `paywalled`, `browser_or_waf`, `interactive_selection_required`, `platform_fallback_dataset_selection_required`, or `external_candidate_required`.
- `download_status`: `not_ready`, `probe_only`, `sample_ready`, or `full_download_ready`.

Never present a homepage-only result as a validated dataset. Never perform full download as a side effect of routing.
