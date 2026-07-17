---
name: who-gho
description: "Find, query, sample, and validate WHO Global Health Observatory data. Use for WHO GHO, OData API, health indicators, countries, regions, dimensions, diseases, mortality, health systems, SDG health metrics, code lists, and global public-health time series."
---

<!-- generated-by: migrate_source_skills_to_native.py -->

# WHO Global Health Observatory

Use this skill to find, access, sample, and validate authoritative data from this source. Treat returned URLs and files as candidates until the source, schema, license, geography, time period, and requested variables are verified.

## When To Use

- Use for WHO GHO health indicator queries and OData API metadata.
- Use when the task names WHO, GHO, global health indicators, health dimensions, or country health time series.
- Use when indicator codes, dimensions, countries, years, and units must be validated.
- Use when the user names `who_gho`, `who-gho`, or WHO Global Health Observatory.

## Do Not Use

- Do not use for patient records, hospital encounter microdata, or local clinic data.
- Do not guess indicator codes or dimensions from broad health concepts.
- Do not substitute CDC/US-specific sources when the user needs U.S. local health indicators.
- Do not use for non-health official indicators; prefer the concept-appropriate source skill (world-bank-indicators, oecd-data, ilo-stat, etc.).
- Do not use for subnational city health data; prefer cdc-places or the relevant city portal when applicable.

## Required Inputs

- `indicator_or_concept`
- `country_or_region`
- `time_range`
- `dimensions_optional`

## Workflow

1. Map the concept to candidate WHO GHO indicators and dimensions.
2. Run the finder to return official GHO/OData candidates.
3. Probe indicator metadata, dimensions, codes, units, and country/year availability.
4. Fetch a capped sample or approved series query.
5. Validate indicator definition, unit, dimensions, country codes, years, and missing values.

## Tools

- `scripts/check_who_gho_access.py`: check access status, authorization requirements, and current availability.
- `scripts/fetch_who_gho_sample.py`: fetch a capped sample or approved resource payload.
- `scripts/find_who_gho.py`: find candidate resources, API endpoints, files, or catalog records.
- `scripts/probe_who_gho_api.py`: probe metadata, schema, variables, or resource headers before download.
- `scripts/validate_who_gho_result.py`: validate returned files, fields, schema, or source suitability.

## References

- `references/source_card.json`: publisher, access status, authoritative URLs, and source-specific validation notes.
- `references/tool_capabilities.json`: available tool actions, access constraints, and download/probe behavior.
- `references/validation_rules.md`: source-specific documentation and validation guidance.
- `references/retrieval_profile.md`: retrieval cues and boundary cases retained from the source package.
- `references/legacy_source_skill.md`: archived pre-migration notes; prefer this SKILL.md for current workflow.

## Official Entrypoints

- WHO Global Health Observatory landing page: https://www.who.int/data/gho
- WHO Global Health Observatory documentation: https://www.who.int/data/gho/info/gho-odata-api
- WHO Global Health Observatory API endpoint: https://ghoapi.azureedge.net/api

## Access And Download Rules

- Current access status from the source card: `open`.
- Authorization required: `false`.
- Probe first when a script supports probe/check mode; do not perform full download as a side effect of search.
- Full download is allowed only after confirming the user intent, source terms, file size, and destination path.
- Confirm the source landing page, documentation, and publisher before downstream acquisition.
- Validate requested geography, time range, variables, license, access limits, and provenance.
- Does not choose WHO entity sets, filters, disaggregations, or units as final.

## Validation Focus

- Check GHO indicator code and dimensions before fetching values.
- Confirm country/region and year coverage.
- Keep global indicators separate from local modeled health datasets.
- Check indicator code, dimension values, disaggregation, and OData entity-set schema.

## Output Contract

- Return GHO API URL, indicator code, dimensions, countries, years, units, and sample/full status.
- Report unresolved concept-to-indicator or dimension ambiguity.
- State whether output is metadata-only, probed, sampled, or fetched.

## Supported Actions

- `find`
- `access_check`
- `probe`
- `fetch_sample`
- `download_link`
- `download`
- `validate`
