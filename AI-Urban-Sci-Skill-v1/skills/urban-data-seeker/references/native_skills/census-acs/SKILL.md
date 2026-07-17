---
name: census-acs
description: "Find, query, sample, and validate U.S. Census American Community Survey data. Use for ACS 1-year or 5-year demographic, socioeconomic, housing, commute, education, race, income, tract, block group, county, place, table, variable, API, and margin-of-error requests."
---

<!-- generated-by: migrate_source_skills_to_native.py -->

# U.S. Census American Community Survey

Use this skill to find, access, sample, and validate authoritative data from this source. Treat returned URLs and files as candidates until the source, schema, license, geography, time period, and requested variables are verified.

## When To Use

- Use for U.S. demographic or socioeconomic indicators from ACS tables or variables.
- Use when the request names ACS, American Community Survey, Census API, tract, block group, county, place, table IDs, variable IDs, estimates, or margins of error.
- Use when the task needs attributes that can later be joined to TIGER/Line or other boundary geometry.
- Use when the user names `census_acs`, `census-acs`, or U.S. Census American Community Survey.

## Do Not Use

- Do not use for LEHD/LODES workplace flows, decennial-only redistricting files, or non-U.S. geographies.
- Do not treat TIGER boundaries as ACS attributes; handle geometry and ACS tables as separate resources.
- Do not guess variable IDs, summary levels, or 1-year versus 5-year survey availability.

## Required Inputs

- `survey`
- `year`
- `geography`
- `variables_or_tables`
- `state_or_place_filter`

## Workflow

1. Identify the ACS vintage, survey type, geography level, and variables or table IDs before constructing a URL.
2. Run the find script to surface relevant ACS table/API leads and ambiguity notes.
3. Run `scripts/resolve_acs_tiger_urls.py` when the task needs both ACS attributes and tract/block-group geometry; this emits ACS API, variable metadata, and TIGER/Line boundary ZIP URLs.
4. Probe the Census API with the requested geography predicates and variables before claiming coverage.
5. Fetch a capped table sample or approved full table only after variable and geography validation passes.
6. Validate estimate columns, margin-of-error columns, geography identifiers, table universe, and vintage.

## Tools

- `scripts/check_census_acs_access.py`: check access status, authorization requirements, and current availability.
- `scripts/fetch_acs_table.py`: fetch a capped sample or approved resource payload.
- `scripts/find_acs_tables.py`: find candidate resources, API endpoints, files, or catalog records.
- `scripts/resolve_acs_tiger_urls.py`: build paired ACS API and TIGER/Line geometry URLs for concrete state/county/geography inputs.
- `scripts/probe_acs_query.py`: probe metadata, schema, variables, or resource headers before download.
- `scripts/validate_acs_result.py`: validate returned files, fields, schema, or source suitability.

## References

- `references/source_card.json`: publisher, access status, authoritative URLs, and source-specific validation notes.
- `references/tool_capabilities.json`: available tool actions, access constraints, and download/probe behavior.
- `references/validation_rules.md`: source-specific documentation and validation guidance.
- `references/retrieval_profile.md`: retrieval cues and boundary cases retained from the source package.
- `references/legacy_source_skill.md`: archived pre-migration notes; prefer this SKILL.md for current workflow.

## Official Entrypoints

- Census Data API: https://api.census.gov/data.html
- ACS program page: https://www.census.gov/programs-surveys/acs

## Access And Download Rules

- Current access status from the source card: `open`.
- Authorization required: `false`.
- Probe first when a script supports probe/check mode; do not perform full download as a side effect of search.
- Full download is allowed only after confirming the user intent, source terms, file size, and destination path.
- Census Data API metadata and TIGER/Line files are public. In this environment, ACS data-row requests currently redirect to a Missing Key page unless a valid Census API key is supplied; report this as an API-key boundary rather than claiming a successful attribute query.
- Legacy ACS known_source entries remain source compatibility hints.
- ACS attributes and TIGER boundaries are separate verification concerns.

## Validation Focus

- Check that every requested variable exists in the selected vintage and survey.
- Preserve estimate and margin-of-error pairing.
- Confirm summary level, state/county/place filters, and GEOID compatibility with any boundary file.
- Do not return `https://api.census.gov/data/{year}/acs5` as a final URL; the executable path is `https://api.census.gov/data/{year}/acs/{acs5|acs1}` with `get`, `for`, `in`, and often `key` parameters.

## Output Contract

- Return Census API dataset URL, variables, predicates, geography level, vintage, and any required key status.
- Report unresolved variable, table, survey, or geography ambiguity.
- State whether the result is only a candidate query, a probed query, a sample, or an approved full fetch.

## Supported Actions

- `find`
- `access_check`
- `probe`
- `fetch_sample`
- `download_link`
- `download`
- `validate`
