---
name: data-gov-catalog
description: "Find, inspect, and validate U.S. Data.gov catalog records and CKAN resources. Use for federal open data discovery, agency datasets, package_search, resource metadata, CSV/GeoJSON/API links, publisher provenance, license checks, and U.S. government dataset leads."
---

<!-- generated-by: migrate_source_skills_to_native.py -->

# Data.gov Catalog

Use this skill to find, access, sample, and validate authoritative data from this source. Treat returned URLs and files as candidates until the source, schema, license, geography, time period, and requested variables are verified.

## When To Use

- Use for broad U.S. federal or multi-agency open-data discovery when the exact source is not yet known.
- Use when the user names Data.gov, catalog.data.gov, CKAN package search, agency datasets, or federal open data.
- Use to find candidate dataset pages and resource files before source-specific validation.
- Use when the user names `data_gov_catalog`, `data-gov-catalog`, or Data.gov Catalog.

## Do Not Use

- Do not treat catalog search ranking as proof that a dataset satisfies the research need.
- Do not download resource files until publisher, license, variables, geography, and time coverage are checked.
- Do not use when a more specific source skill already matches the requested agency or dataset.
- Do not use for city-specific datasets when an official city portal (chicago-open-data, london-datastore, etc.) publishes them directly.
- Do not use Data.gov catalog rank as a proxy for dataset quality or authority.

## Required Inputs

- `query`
- `geography_optional`
- `time_range_optional`
- `agency_optional`
- `format_optional`

## Workflow

1. Translate the need into catalog search terms, geography, time, agency, and expected file/API format.
2. Run the finder or CKAN catalog query to retrieve candidate packages.
3. Inspect package metadata, organization, license, update date, and resource list before choosing a file.
4. Probe candidate resource URLs for format, size, schema, and availability.
5. Validate publisher authority, variables, geography, time range, and license before acquisition.

## Tools

- `scripts/check_data_gov_catalog_access.py`: check access status, authorization requirements, and current availability.
- `scripts/fetch_data_gov_catalog_sample.py`: fetch a capped sample or approved resource payload.
- `scripts/find_data_gov_catalog.py`: find candidate resources, API endpoints, files, or catalog records.
- `scripts/probe_data_gov_catalog_api.py`: probe metadata, schema, variables, or resource headers before download.
- `scripts/validate_data_gov_catalog_result.py`: validate returned files, fields, schema, or source suitability.

## References

- `references/source_card.json`: publisher, access status, authoritative URLs, and source-specific validation notes.
- `references/tool_capabilities.json`: available tool actions, access constraints, and download/probe behavior.
- `references/validation_rules.md`: source-specific documentation and validation guidance.
- `references/retrieval_profile.md`: retrieval cues and boundary cases retained from the source package.
- `references/legacy_source_skill.md`: archived pre-migration notes; prefer this SKILL.md for current workflow.

## Official Entrypoints

- Data.gov Catalog landing page: https://data.gov/
- Data.gov Catalog documentation: https://catalog.data.gov/dataset/data-gov-ckan-api
- Data.gov Catalog API endpoint: https://catalog.data.gov/api/3/action/package_search

## Access And Download Rules

- Current access status from the source card: `open`.
- Authorization required: `false`.
- Probe first when a script supports probe/check mode; do not perform full download as a side effect of search.
- Full download is allowed only after confirming the user intent, source terms, file size, and destination path.
- Confirm the source landing page, documentation, and publisher before downstream acquisition.
- Validate requested geography, time range, variables, license, access limits, and provenance.
- Does not choose a CKAN resource or claim publisher fitness as final.

## Validation Focus

- Check organization/publisher and source landing page.
- Validate each resource separately; package metadata alone is insufficient.
- Record license, update date, format, and access restrictions.
- Check publisher, resource format, landing page, license, and update date before returning a resource URL.

## Output Contract

- Return catalog package URL, publisher, selected resource URLs, formats, license, and validation status.
- Report candidate packages rejected because of geography, time, variables, access, or provenance.
- State whether each resource is metadata-only, probed, sampled, or approved for download.

## Supported Actions

- `find`
- `access_check`
- `probe`
- `fetch_sample`
- `download_link`
- `download`
- `validate`
