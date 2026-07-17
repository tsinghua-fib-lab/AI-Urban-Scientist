---
name: us-tiger-boundaries
description: "Find, download, sample, and validate U.S. Census TIGER/Line and cartographic boundary files. Use for Census tract, block group, county, place, state, ZIP/ZCTA, GEOID, shapefile, geodatabase, cartographic boundary, vintage, and official U.S. boundary geometry requests."
---

<!-- generated-by: migrate_source_skills_to_native.py -->

# U.S. Census TIGER/Line Boundaries

Use this skill to find, access, sample, and validate authoritative data from this source. Treat returned URLs and files as candidates until the source, schema, license, geography, time period, and requested variables are verified.

## When To Use

- Use for official U.S. Census boundary geometry and GEOID join keys.
- Use when the task needs tracts, block groups, counties, places, states, ZCTAs, or cartographic boundary files.
- Use when boundary vintage and ACS/decennial attribute joins must be validated.
- Use when the user names `us_tiger_boundaries`, `us-tiger-boundaries`, or U.S. Census TIGER/Line Boundaries.

## Do Not Use

- Do not use for ACS variables without geometry; use Census ACS for attributes.
- Do not use for non-U.S. boundaries.
- Do not mix TIGER/Line and cartographic boundary files without explaining geometry simplification differences.

## Required Inputs

- `vintage`
- `geography_level`
- `state_or_national_scope`
- `boundary_type`
- `format`

## Workflow

1. Identify vintage, geography level, state/national scope, and TIGER versus cartographic boundary need.
2. Run the finder to return official Census boundary file candidates.
3. Probe file URL, size, format, and expected GEOID fields.
4. Fetch a capped sample or approved boundary file.
5. Validate CRS, geometry type, GEOID fields, vintage, and compatibility with target attributes.

## Tools

- `scripts/check_us_tiger_boundaries_access.py`: check access status, authorization requirements, and current availability.
- `scripts/fetch_tiger_boundary_sample.py`: fetch a capped sample or approved resource payload.
- `scripts/find_tiger_boundaries.py`: find candidate resources, API endpoints, files, or catalog records.
- `scripts/probe_tiger_boundary.py`: probe metadata, schema, variables, or resource headers before download.
- `scripts/validate_tiger_boundary_result.py`: validate returned files, fields, schema, or source suitability.

## References

- `references/source_card.json`: publisher, access status, authoritative URLs, and source-specific validation notes.
- `references/tool_capabilities.json`: available tool actions, access constraints, and download/probe behavior.
- `references/validation_rules.md`: source-specific documentation and validation guidance.
- `references/retrieval_profile.md`: retrieval cues and boundary cases retained from the source package.
- `references/legacy_source_skill.md`: archived pre-migration notes; prefer this SKILL.md for current workflow.

## Official Entrypoints

- TIGER/Line shapefiles: https://www.census.gov/geographies/mapping-files/time-series/geo/tiger-line-file.html
- Cartographic boundary files: https://www.census.gov/geographies/mapping-files/time-series/geo/cartographic-boundary.html

## Access And Download Rules

- Current access status from the source card: `open`.
- Authorization required: `false`.
- Probe first when a script supports probe/check mode; do not perform full download as a side effect of search.
- Full download is allowed only after confirming the user intent, source terms, file size, and destination path.
- Census publishes TIGER/Line shapefiles through public web-interface and FTP archive download paths.
- The ACS legacy known_source layer bundled boundary hints; this source card is the boundary-side migration destination.
- Boundary geometry must not be treated as demographic attribute coverage.

## Validation Focus

- Check vintage and summary level before joins.
- Distinguish TIGER/Line detail from cartographic simplification.
- Confirm GEOID field compatibility with ACS or other attributes.

## Output Contract

- Return official Census boundary URL, vintage, geography level, format, scope, and sample/download status.
- Report unresolved vintage, level, state scope, or boundary-type ambiguity.
- Include join-key and CRS notes.

## Supported Actions

- `find`
- `access_check`
- `probe`
- `fetch_sample`
- `download_link`
- `download`
- `validate`
