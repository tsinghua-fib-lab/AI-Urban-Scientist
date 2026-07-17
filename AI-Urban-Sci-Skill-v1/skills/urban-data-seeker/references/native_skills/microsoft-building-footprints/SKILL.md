---
name: microsoft-building-footprints
description: "Find, download, sample, and validate Microsoft Global ML Building Footprints. Use for open building footprints, ML-derived building polygons, country/regional shard files, geometry quality checks, coverage validation, and large-area building footprint extraction."
---

<!-- generated-by: migrate_source_skills_to_native.py -->

# Microsoft Global ML Building Footprints

Use this skill to find, access, sample, and validate authoritative data from this source. Treat returned URLs and files as candidates until the source, schema, license, geography, time period, and requested variables are verified.

## When To Use

- Use for Microsoft open ML-derived building footprint files and regional shards.
- Use when the task needs building polygons and accepts inferred footprints rather than official building permits.
- Use when file size, shard coverage, geometry quality, and license need validation.
- Use when the user names `microsoft_building_footprints`, `microsoft-building-footprints`, or Microsoft Global ML Building Footprints.

## Do Not Use

- Do not use as official building permit, parcel, address, or occupancy data.
- Do not assume complete coverage or currentness for every region.
- Do not download large shard files without checking size and geography first.

## Required Inputs

- `country_or_region`
- `format`
- `sample_or_full_download`
- `geometry_quality_needs`

## Workflow

1. Identify target country/region and whether ML-derived footprints are acceptable.
2. Run the finder to locate official repository/file-index candidates.
3. Probe file size, shard coverage, update date, format, and license.
4. Fetch a bounded sample before full download.
5. Validate geometry validity, coordinate reference, footprint density, coverage, and attribution.

## Tools

- `scripts/check_microsoft_building_footprints_access.py`: check access status, authorization requirements, and current availability.
- `scripts/fetch_microsoft_building_footprints_sample.py`: fetch a capped sample or approved resource payload.
- `scripts/find_microsoft_building_footprints.py`: find candidate resources, API endpoints, files, or catalog records.
- `scripts/probe_microsoft_building_footprints_api.py`: probe metadata, schema, variables, or resource headers before download.
- `scripts/validate_microsoft_building_footprints_result.py`: validate returned files, fields, schema, or source suitability.

## References

- `references/source_card.json`: publisher, access status, authoritative URLs, and source-specific validation notes.
- `references/tool_capabilities.json`: available tool actions, access constraints, and download/probe behavior.
- `references/validation_rules.md`: source-specific documentation and validation guidance.
- `references/retrieval_profile.md`: retrieval cues and boundary cases retained from the source package.
- `references/legacy_source_skill.md`: archived pre-migration notes; prefer this SKILL.md for current workflow.

## Official Entrypoints

- Microsoft Global ML Building Footprints landing page: https://github.com/microsoft/GlobalMLBuildingFootprints

## Access And Download Rules

- Current access status from the source card: `open`.
- Authorization required: `false`.
- Probe first when a script supports probe/check mode; do not perform full download as a side effect of search.
- Full download is allowed only after confirming the user intent, source terms, file size, and destination path.
- Confirm the source landing page, documentation, and publisher before downstream acquisition.
- Validate requested geography, time range, variables, license, access limits, and provenance.
- Does not validate country shard coverage, freshness, or geometry quality as final.

## Validation Focus

- Check shard coverage and file size.
- Distinguish ML-derived footprints from official records.
- Validate geometry quality and coordinate system.

## Output Contract

- Return official repository/file URLs, region, format, size/status, license, and sample/download status.
- Report unresolved coverage, currentness, or geometry-quality ambiguity.
- Warn when full download is large.

## Supported Actions

- `find`
- `access_check`
- `probe`
- `fetch_sample`
- `download_link`
- `download`
- `validate`
