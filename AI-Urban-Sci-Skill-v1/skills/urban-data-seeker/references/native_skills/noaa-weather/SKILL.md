---
name: noaa-weather
description: "Find, query, sample, and validate NOAA weather and climate data. Use for NOAA CDO, NCEI, stations, daily summaries, hourly observations, precipitation, temperature, weather stations, climate normals, station metadata, and U.S. or global weather time-series requests."
---

<!-- generated-by: migrate_source_skills_to_native.py -->

# NOAA Weather and Climate Data

Use this skill to find, access, sample, and validate authoritative data from this source. Treat returned URLs and files as candidates until the source, schema, license, geography, time period, and requested variables are verified.

## When To Use

- Use for NOAA station observations, climate summaries, precipitation, temperature, normals, and station metadata.
- Use when dataset ID, station ID, datatype, date range, or bounding box must be selected.
- Use when official NOAA/NCEI provenance is required.
- Use when the user names `noaa_weather`, `noaa-weather`, or NOAA Weather and Climate Data.

## Do Not Use

- Do not use for air-quality monitors, satellite imagery, hydrology gauges, or model reanalysis unless NOAA is the requested source.
- Do not guess station coverage or datatype availability.
- Do not ignore API token, rate limit, or date-range constraints.

## Required Inputs

- `dataset`
- `station_or_bbox`
- `datatype`
- `date_range`
- `units`

## Workflow

1. Determine the NOAA dataset family, geography/station, datatype, dates, and units.
2. Run the finder to identify candidate NOAA/NCEI endpoints or datasets.
3. Probe station and datatype availability before fetching observations.
4. Fetch a capped sample or approved response for schema and unit checks.
5. Validate station metadata, coordinates, datatype, units, date coverage, and missing-value flags.

## Tools

- `scripts/check_noaa_weather_access.py`: check access status, authorization requirements, and current availability.
- `scripts/fetch_noaa_sample.py`: fetch a capped sample or approved resource payload.
- `scripts/find_noaa_weather.py`: find candidate resources, API endpoints, files, or catalog records.
- `scripts/probe_noaa_api.py`: probe metadata, schema, variables, or resource headers before download.
- `scripts/resolve_noaa_lcd_hourly.py`: generate executable NOAA NCEI Local Climatological Data hourly observation URLs with station metadata; supports Chicago station presets and custom station IDs, with optional bounded live probe.
- `scripts/validate_noaa_result.py`: validate returned files, fields, schema, or source suitability.

## References

- `references/source_card.json`: publisher, access status, authoritative URLs, and source-specific validation notes.
- `references/tool_capabilities.json`: available tool actions, access constraints, and download/probe behavior.
- `references/validation_rules.md`: source-specific documentation and validation guidance.
- `references/retrieval_profile.md`: retrieval cues and boundary cases retained from the source package.
- `references/legacy_source_skill.md`: archived pre-migration notes; prefer this SKILL.md for current workflow.

## Official Entrypoints

- NOAA NCEI Climate Data Online search: https://www.ncei.noaa.gov/cdo-web/search
- NOAA NCEI access services: https://www.ncei.noaa.gov/access

## Access And Download Rules

- Current access status from the source card: `open_public_use_with_restricted_follow_up_available`.
- Authorization required: `true`.
- Probe first when a script supports probe/check mode; do not perform full download as a side effect of search.
- Full download is allowed only after confirming the user intent, source terms, file size, and destination path.
- NOAA NCEI Data Access offers direct downloads and cloud-ready APIs for many data products.
- NOAA NCEI Data Access `local-climatological-data` can return station-level hourly observations without a CDO token through `https://www.ncei.noaa.gov/access/services/data/v1` when station IDs and dates are known. Use `scripts/resolve_noaa_lcd_hourly.py` for heat, humidity, wind, and precipitation station time-series needs before falling back to token-gated CDO APIs.
- NOAA Climate Data Online web services require an assigned token in the request header.
- The current sample-fetch configuration uses a no-token National Weather Service-style JSON payload; CDO/NCEI full API access still needs explicit token support.
- Legacy NOAA CDO known_source entries remain source compatibility hints.
- NOAA search/API entrypoints may require token, station, variable, and date validation.

## Validation Focus

- Check station coverage for the requested dates.
- Confirm datatype names and units.
- Report API token or rate-limit requirements clearly.

## Output Contract

- Return NOAA dataset, endpoint, station/geography, datatype, date range, unit, and access status.
- For hourly urban station-observation tasks, return the NCEI Data Access API URL or CSV URL plus the station IDs, station metadata fields, requested date range, and probe evidence.
- Report whether data was found, probed, sampled, or downloaded.
- List station/date/datatype gaps instead of silently substituting another station.

## Supported Actions

- `find`
- `access_check`
- `probe`
- `fetch_sample`
- `download_link`
- `download`
- `validate`
