---
name: hdx-catalog
description: "Find, inspect, and validate Humanitarian Data Exchange datasets. Use for HDX, humanitarian open data, crisis, disaster, population, admin boundaries, food security, health, vulnerability, resource downloads, organization metadata, licenses, and country-level humanitarian dataset discovery."
---

<!-- generated-by: migrate_source_skills_to_native.py -->

# Humanitarian Data Exchange

Use this skill to find, access, sample, and validate authoritative data from this source. Treat returned URLs and files as candidates until the source, schema, license, geography, time period, and requested variables are verified.

## When To Use

- Use for humanitarian datasets published through HDX by country, crisis, organization, or theme.
- Use when the task names HDX, UNOCHA, humanitarian data, crisis data, or disaster response datasets.
- Use when resources, licenses, update dates, and organization provenance must be checked.
- Use when the user names `hdx_catalog`, `hdx-catalog`, or Humanitarian Data Exchange.

## Do Not Use

- Do not treat HDX catalog presence as proof of official national statistics.
- Do not use for non-humanitarian city open data when a local portal is more authoritative.
- Do not download sensitive or restricted data without checking HDX terms and resource restrictions.

## Required Inputs

- `country_or_crisis`
- `theme`
- `time_range_optional`
- `organization_optional`
- `format_optional`

## Workflow

1. Clarify country/crisis, theme, time coverage, organization, and required format.
2. Run the finder or HDX catalog query to retrieve candidate packages.
3. Inspect package metadata, resource list, organization, license, and update date.
4. Probe resource URLs for format, schema, and access status before fetching.
5. Validate humanitarian context, geographic coverage, temporal coverage, and sensitivity/terms.

## Tools

- `scripts/check_hdx_catalog_access.py`: check access status, authorization requirements, and current availability.
- `scripts/fetch_hdx_catalog_sample.py`: fetch a capped sample or approved resource payload.
- `scripts/find_hdx_catalog.py`: find candidate resources, API endpoints, files, or catalog records.
- `scripts/probe_hdx_catalog_api.py`: probe metadata, schema, variables, or resource headers before download.
- `scripts/validate_hdx_catalog_result.py`: validate returned files, fields, schema, or source suitability.

## References

- `references/source_card.json`: publisher, access status, authoritative URLs, and source-specific validation notes.
- `references/tool_capabilities.json`: available tool actions, access constraints, and download/probe behavior.
- `references/validation_rules.md`: source-specific documentation and validation guidance.
- `references/retrieval_profile.md`: retrieval cues and boundary cases retained from the source package.
- `references/legacy_source_skill.md`: archived pre-migration notes; prefer this SKILL.md for current workflow.

## Official Entrypoints

- Humanitarian Data Exchange landing page: https://data.humdata.org/
- Humanitarian Data Exchange documentation: https://docs.humdata.org/

## Access And Download Rules

- Current access status from the source card: `open`.
- Authorization required: `false`.
- Probe first when a script supports probe/check mode; do not perform full download as a side effect of search.
- Full download is allowed only after confirming the user intent, source terms, file size, and destination path.
- Confirm the source landing page, documentation, and publisher before downstream acquisition.
- Validate requested geography, time range, variables, license, access limits, and provenance.
- Does not select crisis-specific files or validate humanitarian data recency.

## Validation Focus

- Check organization authority and dataset update date.
- Validate country/crisis coverage and resource-level license.
- Flag sensitive, restricted, or personally risky resources.

## Output Contract

- Return HDX package URL, organization, resource URLs, formats, license, update date, and validation status.
- Report unresolved country, crisis, theme, or organization ambiguity.
- State whether resources are metadata-only, probed, sampled, or approved for download.

## Supported Actions

- `find`
- `access_check`
- `probe`
- `fetch_sample`
- `download_link`
- `download`
- `validate`
