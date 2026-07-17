---
name: stac-platform
description: "Use SpatioTemporal Asset Catalog mechanics for collection, item, asset, bbox, datetime, cloud-cover, platform, and product-level filtering. Use when a selected remote-sensing or geospatial source exposes a STAC catalog/API, or when a URL is explicitly STAC."
---

# STAC Platform

Use this platform skill to narrow an urban data task without pretending that platform or family knowledge is a final dataset. Prefer a concrete source skill whenever the provider or dataset is already known.

## When To Use
- Use when the request, URL, or selected source metadata explicitly contains one of these platform fingerprints: STAC, collections, items, assets, bbox, datetime.
- Use after source suitability has been narrowed and the remaining work is platform-specific probing or query construction.
- Use to inspect metadata, pagination, filters, fields, assets, or export behavior before acquisition.

## Do Not Use
- Do not use STAC mechanics alone to decide scientific product suitability.
- Do not ignore cloud cover, product level, bands/assets, or signing requirements.
- Do not treat cloud-object links as local acquisition.
- Do not use when nasa-earthdata-cmr, planetary-computer, or copernicus-dataspace is the actual target; prefer those concrete source skills when the product is named.
- Do not use for non-STAC raster catalogs or product-specific APIs that do not expose STAC.

## Required Inputs
- `stac_url`
- `collection`
- `bbox`
- `datetime`
- `asset_or_band`

## Workflow
- Confirm the URL, metadata, or user text really contains this platform's fingerprint.
- Inspect platform metadata before constructing queries or export URLs.
- Route back to the concrete source skill when provider suitability, variables, or licensing are the main question.
- Produce a small, reproducible probe plan before suggesting bulk extraction.
- When collection, bbox, and date are known, run `scripts/probe_stac_search.py --catalog-url {catalog} --collection {collection} --bbox {bbox} --datetime {range}` to return item assets.
- Do not call `/collections/{id}/items` or `/search` a direct download unless the returned item asset `href` is selected and validated.

## Tools
- `scripts/probe_stac_search.py`: execute a bounded STAC item search and return candidate item asset hrefs; optionally HEAD-probe HTTP assets.
- `references/platforms/stac_platform/scripts/build_stac_hints.py`: build platform hints from URL, metadata, and request text.
- `references/platforms/stac_platform/references/platform_notes.md`: read only when platform-specific API behavior, limits, or URL patterns are needed.
- `references/platforms/stac_platform/retrieval_profile.md`: read only when retrieval signatures or platform routing evidence must be checked.

## References
- `references/source_card.json`: machine-readable identity, role, and candidate coverage for this native meta skill.
- `references/tool_capabilities.json`: machine-readable action contract and access defaults for this native meta skill.
- `references/platforms/stac_platform/README.md`: platform package overview.
- `references/platforms/stac_platform/retrieval_profile.md`: retrieval profile used by routing experiments.
- `references/stac_query_patterns.md`: STAC collection/item-search/asset query and paging patterns plus common failure modes.

## Official Entrypoints
- Local platform package: `references/platforms/stac_platform/`
- Platform notes: `references/platforms/stac_platform/references/platform_notes.md`

## Access And Download Rules
- Probe first: use metadata, landing pages, small API requests, or source-specific probes before any download.
- Full download is allowed only after a concrete source skill or platform probe verifies authority, schema, license, geography, time period, file size, and user intent.
- This meta skill should return candidate sources or platform actions, not unverified bulk data.

## Validation Focus
- Check collection metadata, item search support, asset roles, bands, CRS, cloud cover, and access signing.
- Probe a small item/asset sample before download.
- Record STAC query parameters and selected assets.
- For strict success, return either a concrete asset URL or an executable item-search API URL plus item/asset evidence; a collection landing page is only a resolver.
- State if asset URLs require signing, requester-pays cloud access, OAuth, or provider-specific tokens.

## Output Contract
- Return `selected_skill_type` as `platform`, `family`, or `discovery`.
- Return `candidate_native_skills` with reasons, required inputs still missing, and validation checks to run next.
- Return `source_priority_rule`: prefer exact source-name matches, then platform URL fingerprints, then source/platform routing.
- Return `download_status`: `not_applicable`, `probe_only`, or `ready_for_source_skill_download`.
