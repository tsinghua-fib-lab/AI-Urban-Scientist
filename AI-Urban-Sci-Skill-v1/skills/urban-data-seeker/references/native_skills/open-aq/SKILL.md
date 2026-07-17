---
name: open-aq
description: "Find, query, sample, and validate OpenAQ air-quality measurements and metadata. Use for OpenAQ API, pollutant observations, PM2.5, PM10, NO2, O3, sensors, stations, locations, providers, coordinates, city air monitoring, and cross-provider ambient air-quality requests."
---

<!-- generated-by: migrate_source_skills_to_native.py -->

# OpenAQ

Use this skill to find, access, sample, and validate authoritative data from this source. Treat returned URLs and files as candidates until the source, schema, license, geography, time period, and requested variables are verified.

## When To Use

- Use for OpenAQ measurement, location, sensor, provider, pollutant, and time-window queries.
- Use when cross-provider ambient air-quality observations are acceptable.
- Use when the task needs API pagination, units, coordinates, and provider provenance.
- Use when the user names `open_aq`, `open-aq`, or OpenAQ.

## Do Not Use

- Do not use when the user explicitly needs EPA AQS/AirData only.
- Do not use for emissions inventories, model outputs, weather, or satellite aerosol products.
- Do not mix pollutants or units without explicit normalization.

## Required Inputs

- `pollutant`
- `location_or_bbox`
- `date_range`
- `provider_optional`
- `limit_or_sample_size`

## Workflow

1. Normalize pollutant, geography, date range, and whether station metadata or measurements are needed.
2. Run the find script to choose the relevant OpenAQ API surface.
3. Probe API parameters and pagination before fetching measurements.
4. Fetch a capped sample for schema, units, location, and provider checks.
5. Validate coordinates, datetime fields, pollutant units, provider, sensor/location IDs, and pagination completeness.

## Tools

- `scripts/check_open_aq_access.py`: check access status, authorization requirements, and current availability.
- `scripts/fetch_open_aq_sample.py`: fetch a capped sample or approved resource payload.
- `scripts/find_open_aq.py`: find candidate resources, API endpoints, files, or catalog records.
- `scripts/probe_open_aq_api.py`: probe metadata, schema, variables, or resource headers before download.
- `scripts/validate_open_aq_result.py`: validate returned files, fields, schema, or source suitability.

## References

- `references/source_card.json`: publisher, access status, authoritative URLs, and source-specific validation notes.
- `references/tool_capabilities.json`: available tool actions, access constraints, and download/probe behavior.
- `references/validation_rules.md`: source-specific documentation and validation guidance.
- `references/retrieval_profile.md`: retrieval cues and boundary cases retained from the source package.
- `references/legacy_source_skill.md`: archived pre-migration notes; prefer this SKILL.md for current workflow.

## Official Entrypoints

- OpenAQ API/documentation: https://api.openaq.org/v3/measurements
- OpenAQ API/documentation: https://docs.openaq.org/

## Access And Download Rules

- Current access status from the source card: `key_gated`.
- Authorization required: `true`.
- Probe first when a script supports probe/check mode; do not perform full download as a side effect of search.
- Full download is allowed only after confirming the user intent, source terms, file size, and destination path.
- OpenAQ v3 programmatic API requests require a registered API key sent in the X-API-Key header.
- OpenAQ also documents a full data archive on the Open Data on AWS path; use only official APIs, export functions, or sanctioned archive access.
- Concrete API requests require pollutant, location, and time-window validation.
- Provider coverage and API paging must be checked downstream.

## Validation Focus

- Check pollutant-unit consistency and provider provenance.
- Confirm requested time zone/date semantics and API pagination.
- Report coverage gaps for locations or dates rather than imputing data.

## Output Contract

- Return OpenAQ documentation/API URLs, query parameters, pollutant, geography, date range, and pagination status.
- Report sample row count and whether results are measurements or metadata.
- State unresolved unit, provider, location, or coverage ambiguity.

## Supported Actions

- `find`
- `access_check`
- `probe`
- `fetch_sample`
- `download_link`
- `download`
- `validate`
