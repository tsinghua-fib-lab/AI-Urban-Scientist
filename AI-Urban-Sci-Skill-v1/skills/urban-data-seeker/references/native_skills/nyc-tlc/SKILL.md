---
name: nyc-tlc
description: "Find, download, sample, and validate NYC Taxi and Limousine Commission trip record data. Use for yellow taxi, green taxi, FHV, high-volume FHV, taxi zones, pickup/dropoff, fares, monthly Parquet/CSV files, and New York City trip-level mobility analysis."
---

<!-- generated-by: migrate_source_skills_to_native.py -->

# NYC TLC Trip Record Data

Use this skill to find, access, sample, and validate authoritative data from this source. Treat returned URLs and files as candidates until the source, schema, license, geography, time period, and requested variables are verified.

## When To Use

- Use for New York City taxi, FHV, yellow taxi, green taxi, pickup/dropoff, fare, and trip record questions.
- Use when the request needs monthly trip-record files or schema-aware samples.
- Use for taxi-zone based urban mobility analysis in NYC.
- Use when the user names `nyc_tlc`, `nyc-tlc`, or NYC TLC Trip Record Data.

## Do Not Use

- Do not use for cities outside New York City.
- Do not use for GTFS transit schedules, bike share trips, traffic sensors, or generic ride-hailing data.
- Do not assume old CSV schemas and newer Parquet schemas are identical.

## Required Inputs

- `vehicle_type`
- `year`
- `month`
- `sample_or_full_download`
- `needed_columns`

## Workflow

1. Identify vehicle type, month range, file format, and whether taxi zone lookup data is needed.
2. Run the file finder to construct candidate official monthly file URLs.
3. Probe candidate files for availability, size, format, and schema before downloading.
4. Fetch a capped sample first for schema checks unless full download is explicitly requested.
5. Validate pickup/dropoff timestamps, location IDs, fare fields, trip distance, passenger count, and known schema changes.

## Tools

- `scripts/check_nyc_tlc_access.py`: check access status, authorization requirements, and current availability.
- `scripts/fetch_trip_record_sample.py`: fetch a capped sample or approved resource payload.
- `scripts/find_trip_record_files.py`: find candidate resources, API endpoints, files, or catalog records.
- `scripts/probe_trip_record_file.py`: probe metadata, schema, variables, or resource headers before download.
- `scripts/validate_trip_record_schema.py`: validate returned files, fields, schema, or source suitability.

## References

- `references/official_entrypoints.md`: source-specific documentation and validation guidance.
- `references/source_card.json`: publisher, access status, authoritative URLs, and source-specific validation notes.
- `references/tool_capabilities.json`: available tool actions, access constraints, and download/probe behavior.
- `references/validation_rules.md`: source-specific documentation and validation guidance.
- `references/retrieval_profile.md`: retrieval cues and boundary cases retained from the source package.
- `references/legacy_source_skill.md`: archived pre-migration notes; prefer this SKILL.md for current workflow.

## Official Entrypoints

- NYC TLC Trip Record Data landing page: https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page
- NYC Open Data TLC datasets: https://data.cityofnewyork.us/browse?q=Taxi%20and%20Limousine%20Commission

## Access And Download Rules

- Current access status from the source card: `open`.
- Authorization required: `false`.
- Probe first when a script supports probe/check mode; do not perform full download as a side effect of search.
- Full download is allowed only after confirming the user intent, source terms, file size, and destination path.
- NYC TLC publishes monthly trip records as public Parquet files and links NYC Open Data export options.
- Legacy known_source compatibility remains source only.
- Monthly file patterns must be resolved and probed before route acceptance.

## Validation Focus

- Check monthly file existence and schema version.
- Confirm taxi zone lookup compatibility when mapping pickup/dropoff IDs.
- Flag unrealistic trips, null zones, and format changes as data quality issues.

## Output Contract

- Return official TLC landing page, selected monthly file URLs, vehicle type, file format, and schema status.
- Report whether files were only found, probed, sampled, or fully downloaded.
- Include taxi-zone lookup requirements when spatial analysis is requested.

## Supported Actions

- `find`
- `access_check`
- `probe`
- `fetch_sample`
- `download_link`
- `download`
- `validate`
