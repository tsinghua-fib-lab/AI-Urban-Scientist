---
name: oecd-data
description: "Find, query, sample, and validate OECD Data Explorer statistics. Use for OECD indicators, SDMX dataflows, countries, regions, metropolitan statistics, economy, labor, education, environment, dimensions, codelists, time series, and international comparison requests."
---

<!-- generated-by: migrate_source_skills_to_native.py -->

# OECD Data Explorer

Use this skill to find, access, sample, and validate authoritative data from this source. Treat returned URLs and files as candidates until the source, schema, license, geography, time period, and requested variables are verified.

## When To Use

- Use for OECD indicator series, regional statistics, metropolitan data, and SDMX dataflows.
- Use when the request names OECD Data Explorer, OECD API, SDMX, codelists, dimensions, or international indicators.
- Use when dimension keys, units, frequency, and country/region coverage must be verified.
- Use when the user names `oecd_data`, `oecd-data`, or OECD Data Explorer.

## Do Not Use

- Do not use for city microdata or local administrative records not published by OECD.
- Do not guess SDMX dataflow IDs, dimension order, or codelist values.
- Do not mix countries, regions, and metro areas without checking geography semantics.
- Do not use for IMF, World Bank, WHO, FAO, ILO, or UN indicator data; prefer the corresponding source skill.

## Required Inputs

- `indicator_or_concept`
- `geography`
- `time_range`
- `frequency_optional`
- `dimensions_optional`

## Workflow

1. Map the concept to candidate OECD dataflows, dimensions, and codelists.
2. Run the finder to return official OECD Data Explorer/API candidates.
3. Probe dataflow metadata, dimension order, units, frequency, and geography coverage.
4. Fetch a capped sample or approved series query.
5. Validate series keys, units, time coverage, missing values, and regional/geographic definitions.

## Tools

- `scripts/check_oecd_data_access.py`: check access status, authorization requirements, and current availability.
- `scripts/fetch_oecd_data_sample.py`: fetch a capped sample or approved resource payload.
- `scripts/find_oecd_data.py`: find candidate resources, API endpoints, files, or catalog records.
- `scripts/probe_oecd_data_api.py`: probe metadata, schema, variables, or resource headers before download.
- `scripts/validate_oecd_data_result.py`: validate returned files, fields, schema, or source suitability.

## References

- `references/source_card.json`: publisher, access status, authoritative URLs, and source-specific validation notes.
- `references/tool_capabilities.json`: available tool actions, access constraints, and download/probe behavior.
- `references/validation_rules.md`: source-specific documentation and validation guidance.
- `references/retrieval_profile.md`: retrieval cues and boundary cases retained from the source package.
- `references/legacy_source_skill.md`: archived pre-migration notes; prefer this SKILL.md for current workflow.

## Official Entrypoints

- OECD Data Explorer landing page: https://www.oecd.org/en/data.html
- OECD Data Explorer documentation: https://www.oecd.org/en/data/insights/data-explainers/2024/09/api.html
- OECD Data Explorer API endpoint: https://sdmx.oecd.org/public/rest/v1

## Access And Download Rules

- Current access status from the source card: `open`.
- Authorization required: `false`.
- Probe first when a script supports probe/check mode; do not perform full download as a side effect of search.
- Full download is allowed only after confirming the user intent, source terms, file size, and destination path.
- Confirm the source landing page, documentation, and publisher before downstream acquisition.
- Validate requested geography, time range, variables, license, access limits, and provenance.
- Does not resolve SDMX dataflow dimensions or codelists as final.

## Validation Focus

- Check SDMX dataflow ID, dimensions, codelists, and key order.
- Confirm unit, frequency, and geographic level.
- Report concept-to-indicator ambiguity and missing observations.

## Output Contract

- Return OECD dataflow/API URL, dimensions, selected codes, geography, time range, units, and sample/full status.
- Report unresolved dataflow, dimension, codelist, or geography ambiguity.
- State whether output is metadata-only, probed, sampled, or fetched.

## Supported Actions

- `find`
- `access_check`
- `probe`
- `fetch_sample`
- `download_link`
- `download`
- `validate`
