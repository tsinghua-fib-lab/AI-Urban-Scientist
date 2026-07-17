---
name: planetary-computer
description: "Find, query, sample, and validate Microsoft Planetary Computer geospatial assets. Use for STAC collections, satellite imagery, raster assets, cloud-hosted geospatial data, Sentinel, Landsat, NAIP, weather/climate rasters, signed asset URLs, bounding boxes, dates, and cloud-native spatial workflows."
---

<!-- generated-by: migrate_source_skills_to_native.py -->

# Microsoft Planetary Computer

Use this skill to find, access, sample, and validate authoritative data from this source. Treat returned URLs and files as candidates until the source, schema, license, geography, time period, and requested variables are verified.

## When To Use

- Use for Microsoft Planetary Computer STAC collections and cloud-hosted geospatial assets.
- Use when the task needs bbox/date/collection/asset filtering before downloading imagery or rasters.
- Use when signed asset URLs, item metadata, and cloud-native access should be checked.
- Use when the user names `planetary_computer`, `planetary-computer`, or Microsoft Planetary Computer.

## Do Not Use

- Do not use for generic web maps or local files when no Planetary Computer collection is involved.
- Do not download large rasters without bounding, asset selection, and user approval.
- Do not assume every asset is analysis-ready for the requested CRS, resolution, or date.
- Do not use for generic STAC catalog mechanics; prefer stac-platform when the URL is a STAC API without Planetary-Computer-specific context.
- Do not use as a general remote-sensing router; prefer remote-sensing-earth-observation when the product family is still unresolved.
- Do not use for NASA DAAC-specific products; prefer nasa-earthdata-cmr.
- Do not use for Copernicus-only products that are not mirrored on Planetary Computer; prefer copernicus-dataspace.

## Required Inputs

- `collection`
- `bbox_or_geometry`
- `date_range`
- `asset_type`
- `sample_or_full_download`

## Workflow

1. Identify collection, bbox/geometry, date range, asset type, and resolution requirements.
2. Run the finder to choose candidate STAC collections or items.
3. Probe item metadata, assets, license, CRS, resolution, and signing requirements.
4. Fetch metadata or a small spatial/temporal sample before any large download.
5. Validate item coverage, cloud/quality flags when relevant, asset URLs, and geospatial metadata.

## Tools

- `scripts/check_planetary_computer_access.py`: check access status, authorization requirements, and current availability.
- `scripts/fetch_planetary_computer_sample.py`: fetch a capped sample or approved resource payload.
- `scripts/find_planetary_computer.py`: find candidate resources, API endpoints, files, or catalog records.
- `scripts/probe_planetary_computer_api.py`: probe metadata, schema, variables, or resource headers before download.
- `scripts/validate_planetary_computer_result.py`: validate returned files, fields, schema, or source suitability.

## References

- `references/source_card.json`: publisher, access status, authoritative URLs, and source-specific validation notes.
- `references/tool_capabilities.json`: available tool actions, access constraints, and download/probe behavior.
- `references/validation_rules.md`: source-specific documentation and validation guidance.
- `references/retrieval_profile.md`: retrieval cues and boundary cases retained from the source package.
- `references/legacy_source_skill.md`: archived pre-migration notes; prefer this SKILL.md for current workflow.

## Official Entrypoints

- Microsoft Planetary Computer landing page: https://planetarycomputer.microsoft.com/
- Microsoft Planetary Computer documentation: https://planetarycomputer.microsoft.com/docs/
- Microsoft Planetary Computer API endpoint: https://planetarycomputer.microsoft.com/api/stac/v1

## Access And Download Rules

- Current access status from the source card: `open`.
- Authorization required: `false`.
- Probe first when a script supports probe/check mode; do not perform full download as a side effect of search.
- Full download is allowed only after confirming the user intent, source terms, file size, and destination path.
- Confirm the source landing page, documentation, and publisher before downstream acquisition.
- Validate requested geography, time range, variables, license, access limits, and provenance.
- Does not sign assets, choose item assets, or perform cloud raster sampling as final.

## Validation Focus

- Check STAC collection, item date, bbox intersection, asset roles, signed URL requirements, CRS, resolution, and nodata.
- Confirm quality/cloud fields when needed.
- Keep metadata search separate from raster download.

## Output Contract

- Return STAC collection/item URLs, asset names, bbox/date filters, signing status, and sample/download status.
- Report unresolved collection, asset, CRS, or coverage ambiguity.
- Warn when full download would be large or unnecessary.

## Supported Actions

- `find`
- `access_check`
- `probe`
- `fetch_sample`
- `download_link`
- `download`
- `validate`
