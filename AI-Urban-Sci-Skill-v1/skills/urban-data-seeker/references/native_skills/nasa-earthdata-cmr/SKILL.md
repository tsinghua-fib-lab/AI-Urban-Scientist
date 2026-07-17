---
name: nasa-earthdata-cmr
description: "Find, query, sample, and validate NASA Earthdata CMR collections and granules. Use for NASA Earthdata, CMR search, satellite products, collections, granules, bounding boxes, temporal filters, DAAC data, remote sensing, Earth observation metadata, and NASA download access checks."
---

<!-- generated-by: migrate_source_skills_to_native.py -->

# NASA Earthdata CMR

Use this skill to find, access, sample, and validate authoritative data from this source. Treat returned URLs and files as candidates until the source, schema, license, geography, time period, and requested variables are verified.

## When To Use

- Use for NASA Earthdata collection or granule discovery through CMR.
- Use when DAAC, product short name, version, bbox, temporal range, or granule links must be validated.
- Use when Earthdata login, access constraints, or large remote-sensing downloads need explicit handling.
- Use when the user names `nasa_earthdata_cmr`, `nasa-earthdata-cmr`, or NASA Earthdata CMR.

## Do Not Use

- Do not use for non-NASA STAC catalogs unless NASA CMR is explicitly involved.
- Do not download large granules without user approval, size checks, and authentication status.
- Do not treat collection metadata as proof that a granule covers the exact study area/date.
- Do not use for generic STAC catalog mechanics; prefer stac-platform when the URL is a STAC API without NASA-specific context.
- Do not use as a general remote-sensing router; prefer remote-sensing-earth-observation when the product family is still unresolved.
- Do not use for Sentinel or Landsat assets hosted on Planetary Computer or Copernicus Data Space; prefer planetary-computer or copernicus-dataspace.
- Do not use for climate reanalysis variables; prefer era5-cds.

## Required Inputs

- `product_or_collection`
- `bbox_or_geometry`
- `date_range`
- `granule_or_collection_search`
- `download_intent`

## Workflow

1. Clarify product, collection, version, bbox/geometry, date range, and whether collection or granule search is needed.
2. Run the finder to return candidate CMR collection or granule queries.
3. Probe metadata for DAAC, version, temporal coverage, spatial coverage, links, and access constraints.
4. Fetch metadata or a capped granule sample before any full download.
5. Validate granule coverage, product version, file links, Earthdata authentication, license, and size.

## Tools

- `scripts/check_nasa_earthdata_cmr_access.py`: check access status, authorization requirements, and current availability.
- `scripts/fetch_nasa_earthdata_cmr_sample.py`: fetch a capped sample or approved resource payload.
- `scripts/find_nasa_earthdata_cmr.py`: find candidate resources, API endpoints, files, or catalog records.
- `scripts/probe_nasa_earthdata_cmr_api.py`: probe metadata, schema, variables, or resource headers before download.
- `scripts/validate_nasa_earthdata_cmr_result.py`: validate returned files, fields, schema, or source suitability.

## References

- `references/source_card.json`: publisher, access status, authoritative URLs, and source-specific validation notes.
- `references/tool_capabilities.json`: available tool actions, access constraints, and download/probe behavior.
- `references/validation_rules.md`: source-specific documentation and validation guidance.
- `references/retrieval_profile.md`: retrieval cues and boundary cases retained from the source package.
- `references/legacy_source_skill.md`: archived pre-migration notes; prefer this SKILL.md for current workflow.

## Official Entrypoints

- NASA Earthdata CMR landing page: https://www.earthdata.nasa.gov/
- NASA Earthdata CMR documentation: https://cmr.earthdata.nasa.gov/search/site/docs/search/api
- NASA Earthdata CMR API endpoint: https://cmr.earthdata.nasa.gov/search

## Access And Download Rules

- Current access status from the source card: `registration_required`.
- Authorization required: `true`.
- Probe first when a script supports probe/check mode; do not perform full download as a side effect of search.
- Full download is allowed only after confirming the user intent, source terms, file size, and destination path.
- This source is not treated as open bulk-download data; return access instructions or metadata instead of files.
- Confirm the source landing page, documentation, and publisher before downstream acquisition.
- Validate requested geography, time range, variables, license, access limits, and provenance.
- Does not bypass Earthdata Login, EULA, product version, or large-file policy.

## Validation Focus

- Check collection short name, version, DAAC, spatial/temporal intersection, and access constraints before granule fetch.
- Separate collection discovery from granule availability.
- Report Earthdata authentication requirements and large-file risks.

## Output Contract

- Return CMR query URL, collection/granule IDs, DAAC, version, bbox/date filters, and access status.
- State whether output is metadata, candidate granule links, sampled metadata, or approved download.
- List missing product, version, bbox, date, or login ambiguity.

## Supported Actions

- `find`
- `access_check`
- `probe`
- `fetch_sample`
- `download_link`
- `download`
- `validate`
