# Osm Geofabrik Extracts SourceSkill

## Purpose

Regional OpenStreetMap PBF and derived vector extracts from Geofabrik.

## When To Use

Use this SourceSkill when the request matches this source family, names the platform, or needs its official API/download workflow rather than a generic web search.

## Do Not Use

Do not treat returned candidates as final until source, schema, license, geography, time period, and requested variables are validated. Do not bypass credentials, provider terms, rate limits, or explicit full-download authorization.

## Inputs

- `need_id`
- `need_text`
- `query`
- `geography`
- `time_range`
- `params_json` for source-specific parameters such as bbox, year, state, region path, API key placeholders, or limit.

## Tools/Scripts Used

- `scripts/check_osm_geofabrik_extracts_access.py` reports access, authorization, and policy constraints.
- `scripts/find_osm_geofabrik_extracts.py` emits source-specific candidate URLs and required validation notes.
- `scripts/probe_osm_geofabrik_extracts_metadata.py` probes fixture or live responses under `probe_allowed`.
- `scripts/fetch_osm_geofabrik_extracts_sample.py` writes capped fixture or live samples under `fetch_sample_allowed`; full fetch requires explicit approval and policy.
- `scripts/validate_osm_geofabrik_extracts_result.py` validates returned samples against source-specific field, suffix, and provenance expectations.

## Official Candidate Entrypoints

- Geofabrik download server: `https://download.geofabrik.de/`
- Geofabrik region PBF: `https://download.geofabrik.de/{region_path}-latest.osm.pbf`
- Geofabrik region shapefile: `https://download.geofabrik.de/{region_path}-latest-free.shp.zip`

## Access And Download Rules

- Access status: `open`.
- API status: `bulk_download_only`.
- Authorization required: `false`.
- This source can be probed without credentials, but full downloads still require terms, size, and destination checks.
- Probe first; full download is never a side effect of search.

## Validation Focus

- Validate region path, ODbL attribution, update date, file size, and whether personal metadata is excluded.

## Workflow

1. Resolve source-specific parameters and emit candidate resources with `find`.
2. Run `check` and `probe` before acquisition.
3. Fetch only a capped sample unless explicit full-fetch policy is approved.
4. Validate schema, geography, time period, license, and provider-specific caveats before passing the result downstream.

## Failure Rules

Never claim acquisition success from candidate URLs alone. Return unresolved parameters, credential gaps, unavailable endpoints, or license restrictions as follow-up requirements.
