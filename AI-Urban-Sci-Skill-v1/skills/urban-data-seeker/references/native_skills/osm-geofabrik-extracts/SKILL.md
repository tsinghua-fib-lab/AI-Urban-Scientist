---
name: osm-geofabrik-extracts
description: "Find, access-check, probe, validate, and return candidate Geofabrik OpenStreetMap regional extract links. Use for bulk OSM PBF, shapefile, regional extracts, country/state/city downloads, planet-derived files, and large-area OpenStreetMap feature extraction workflows."
---

<!-- generated-by: migrate_source_skills_to_native.py -->

# Geofabrik OSM Extracts

Use this skill to find, access, sample, and validate authoritative data from this source. Treat returned URLs and files as candidates until the source, schema, license, geography, time period, and requested variables are verified.

## When To Use

- Use for bulk regional OSM extract downloads from Geofabrik.
- Use when Overpass is too small or unstable for the requested geography.
- Use when the task needs reproducible PBF/shapefile source URLs and extract metadata.
- Use when the user names `osm_geofabrik_extracts`, `osm-geofabrik-extracts`, or Geofabrik OSM Extracts.

## Do Not Use

- Do not use for small tag-only interactive queries where OSM features or Overpass is sufficient.
- Do not use for official government roads, parcels, addresses, or zoning unless OSM is acceptable.
- Do not download very large extracts without explicit user approval and destination path.

## Required Inputs

- `region`
- `format`
- `feature_needs`
- `download_or_metadata_only`

## Workflow

1. Identify the smallest Geofabrik region that covers the study area.
2. Run `scripts/resolve_geofabrik_region.py --region "{place}" --format pbf --probe` before considering broader country extracts.
3. Probe file availability, size, timestamp, and format before download.
4. Do not claim a small derived sample from the bundled static fetch script; return metadata and candidate file links until a source-specific sampler is implemented.
5. Validate region coverage, ODbL attribution, file date, format, and downstream filtering plan.

## Tools

- `scripts/check_osm_geofabrik_extracts_access.py`: check access status, authorization requirements, and current availability.
- `scripts/fetch_osm_geofabrik_extracts_sample.py`: fetch a capped sample or approved resource payload.
- `scripts/find_osm_geofabrik_extracts.py`: find candidate resources, API endpoints, files, or catalog records.
- `scripts/resolve_geofabrik_region.py`: search official `index-v1.json`, choose the smallest matching extract, and return direct PBF/shapefile URLs with optional HEAD probe.
- `scripts/probe_osm_geofabrik_extracts_metadata.py`: probe metadata, schema, variables, or resource headers before download.
- `scripts/validate_osm_geofabrik_extracts_result.py`: validate returned files, fields, schema, or source suitability.

## References

- `references/source_card.json`: publisher, access status, authoritative URLs, and source-specific validation notes.
- `references/tool_capabilities.json`: available tool actions, access constraints, and download/probe behavior.
- `references/retrieval_profile.md`: retrieval cues and boundary cases retained from the source package.
- `references/legacy_source_skill.md`: archived pre-migration notes; prefer this SKILL.md for current workflow.

## Official Entrypoints

- Geofabrik download server: https://download.geofabrik.de/
- Geofabrik region PBF: https://download.geofabrik.de/{region_path}-latest.osm.pbf
- Geofabrik region shapefile: https://download.geofabrik.de/{region_path}-latest-free.shp.zip

## Access And Download Rules

- Current access status from the source card: `open`.
- Authorization required: `false`.
- Probe first when a script supports probe/check mode; do not perform full download as a side effect of search.
- Full download is allowed only after confirming the user intent, source terms, file size, and destination path.
- This initial source package exposes official entrypoints and conservative source hints only.

## Validation Focus

- Prefer the smallest adequate extract to reduce cost.
- Never claim no city/regional extract exists until `index-v1.json` has been searched. For London, prefer `greater-london-latest.osm.pbf` over Great Britain or England extracts when the task asks for London.
- Check file size and timestamp before full download.
- Preserve OSM license and attribution notes.

## Output Contract

- Return Geofabrik region page, direct file URLs, format, timestamp, and size when available.
- State whether the output is metadata-only, candidate download link, probed file, or approved full download.
- Report if the requested city is not directly available and a larger region is required.

## Supported Actions

- `find`
- `access_check`
- `probe`
- `fetch_sample`
- `download_link`
- `validate`
