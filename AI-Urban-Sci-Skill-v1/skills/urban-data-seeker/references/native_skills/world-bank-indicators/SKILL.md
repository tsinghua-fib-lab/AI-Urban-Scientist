---
name: world-bank-indicators
description: "Find, query, sample, and validate World Bank indicator data. Use for World Bank Data API, country indicators, income, poverty, GDP, population, urbanization, health, education, environment, indicator codes, country codes, time series, and international development comparisons."
---

<!-- generated-by: migrate_source_skills_to_native.py -->

# World Bank Indicators

Use this skill to find, access, sample, and validate authoritative data from this source. Treat returned URLs and files as candidates until the source, schema, license, geography, time period, and requested variables are verified.

## When To Use

- Use for World Bank indicator series by country, economy, region, and year.
- Use when the request mentions World Bank, indicator code, WDI, country time series, or development indicators.
- Use when indicator definitions, units, source notes, and country coverage must be checked.
- Use when the user names `world_bank_indicators`, `world-bank-indicators`, or World Bank Indicators.

## Do Not Use

- Do not use for subnational city data unless the World Bank source explicitly provides it.
- Do not guess indicator codes from plain-language concepts without checking metadata.
- Do not mix current and historical country codes without noting implications.
- Do not use for World Bank Poverty and Inequality Platform microdata; prefer world-bank-pip.
- Do not use for IMF, OECD, WHO, FAO, ILO, or UN data; prefer the corresponding source skill.

## Required Inputs

- `indicator_or_concept`
- `country_or_region`
- `year_range`
- `frequency_optional`

## Workflow

1. Map the concept to candidate World Bank indicator codes and country/economy codes.
2. Run the finder to return API or metadata candidates.
3. Probe indicator metadata, unit, source note, and country coverage before fetching values.
4. Fetch a capped sample or approved time series.
5. Validate indicator definition, unit, source organization, year coverage, missing values, and country code semantics.

## Tools

- `scripts/check_world_bank_indicators_access.py`: check access status, authorization requirements, and current availability.
- `scripts/fetch_world_bank_indicators_sample.py`: fetch a capped sample or approved resource payload.
- `scripts/find_world_bank_indicators.py`: find candidate resources, API endpoints, files, or catalog records.
- `scripts/probe_world_bank_indicators_api.py`: probe metadata, schema, variables, or resource headers before download.
- `scripts/validate_world_bank_indicators_result.py`: validate returned files, fields, schema, or source suitability.

## References

- `references/source_card.json`: publisher, access status, authoritative URLs, and source-specific validation notes.
- `references/tool_capabilities.json`: available tool actions, access constraints, and download/probe behavior.
- `references/validation_rules.md`: source-specific documentation and validation guidance.
- `references/retrieval_profile.md`: retrieval cues and boundary cases retained from the source package.
- `references/legacy_source_skill.md`: archived pre-migration notes; prefer this SKILL.md for current workflow.

## Official Entrypoints

- World Bank Data portal: https://data.worldbank.org/
- World Bank API documentation: https://datahelpdesk.worldbank.org/knowledgebase/articles/889392

## Access And Download Rules

- Current access status from the source card: `open`.
- Authorization required: `false`.
- Probe first when a script supports probe/check mode; do not perform full download as a side effect of search.
- Full download is allowed only after confirming the user intent, source terms, file size, and destination path.

## Validation Focus

- Check indicator code, definition, unit, and source note.
- Confirm country/economy codes and year availability.
- Report missing values and aggregation limitations.

## Output Contract

- Return indicator code, country codes, API URL, years, unit, and metadata source note.
- Report whether values are metadata-only, sample, or full approved series.
- State unresolved concept-to-indicator ambiguity.

## Supported Actions

- `find`
- `access_check`
- `probe`
- `fetch_sample`
- `download_link`
- `download`
- `validate`
