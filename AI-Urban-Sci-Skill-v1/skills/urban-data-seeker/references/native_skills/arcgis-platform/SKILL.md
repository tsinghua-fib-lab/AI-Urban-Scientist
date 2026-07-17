---
name: arcgis-platform
description: "Use ArcGIS Hub and ArcGIS REST mechanics for FeatureServer, MapServer, layers, fields, extents, query endpoints, export links, and geospatial open-data services. Use when a URL or metadata explicitly indicates ArcGIS, or when a selected source requires ArcGIS platform probing after source suitability has been decided."
---

# ArcGIS Platform

Use this platform skill to narrow an urban data task without pretending that platform or family knowledge is a final dataset. Prefer a concrete source skill whenever the provider or dataset is already known.

## When To Use
- Use when the request, URL, or selected source metadata explicitly contains one of these platform fingerprints: ArcGIS Hub, FeatureServer, MapServer, services.arcgis.com, arcgis/rest/services.
- Use after source suitability has been narrowed and the remaining work is platform-specific probing or query construction.
- Use to inspect metadata, pagination, filters, fields, assets, or export behavior before acquisition.

## Do Not Use
- Do not use ArcGIS mechanics alone to decide research suitability.
- Do not assume a MapServer visualization layer is downloadable.
- Do not replace a known source skill when the provider is already clear.
- Do not use when fema-flood, hifld-facilities, hifld-utility-networks, usgs-hydro, or another concrete ArcGIS-backed source skill already matches the request.
- Do not use for a generic geospatial question before confirming the host is actually ArcGIS.

## Required Inputs
- `arcgis_url_or_portal`
- `layer_or_service_hint`
- `geometry_needed`
- `fields_needed`
- `bbox_or_filter`

## Workflow
- Confirm the URL, metadata, or user text really contains this platform's fingerprint.
- Inspect platform metadata before constructing queries or export URLs.
- Route back to the concrete source skill when provider suitability, variables, or licensing are the main question.
- Produce a small, reproducible probe plan before suggesting bulk extraction.
- When a layer URL is known, run `scripts/build_arcgis_feature_query.py --service-url {FeatureServer_or_MapServer_url} --layer {id} --where "1=1" --result-record-count 5 --probe`.
- Reject a plain service root, item page, or map visualization as strict success unless a concrete layer `/query` URL or export URL is returned and probed.

## Tools
- `scripts/build_arcgis_feature_query.py`: build and optionally probe a concrete ArcGIS layer `/query` URL with fields, bbox, record count, geometry, and JSON/GeoJSON format.
- `references/platforms/arcgis_platform/scripts/build_arcgis_hints.py`: build platform hints from URL, metadata, and request text.
- `references/platforms/arcgis_platform/references/platform_notes.md`: read only when platform-specific API behavior, limits, or URL patterns are needed.
- `references/platforms/arcgis_platform/retrieval_profile.md`: read only when retrieval signatures or platform routing evidence must be checked.

## References
- `references/source_card.json`: machine-readable identity, role, and candidate coverage for this native meta skill.
- `references/tool_capabilities.json`: machine-readable action contract and access defaults for this native meta skill.
- `references/platforms/arcgis_platform/README.md`: platform package overview.
- `references/platforms/arcgis_platform/retrieval_profile.md`: retrieval profile used by routing experiments.

## Official Entrypoints
- Local platform package: `references/platforms/arcgis_platform/`
- Platform notes: `references/platforms/arcgis_platform/references/platform_notes.md`

## Access And Download Rules
- Probe first: use metadata, landing pages, small API requests, or source-specific probes before any download.
- Full download is allowed only after a concrete source skill or platform probe verifies authority, schema, license, geography, time period, file size, and user intent.
- This meta skill should return candidate sources or platform actions, not unverified bulk data.

## Validation Focus
- Inspect service metadata, layer id, fields, geometry type, extent, max record count, and export support.
- Probe small queries before recommending bulk export.
- Preserve publisher and layer provenance in candidate outputs.
- A successful HTTP 200 is not enough; reject ArcGIS JSON payloads containing an `error` object.
- For strict success, return a layer-level `/query` URL, not only a service URL or ArcGIS Hub item page.
- For full extraction, document pagination with `resultOffset` and `resultRecordCount` according to layer `maxRecordCount`.

## Output Contract
- Return `selected_skill_type` as `platform`, `family`, or `discovery`.
- Return `candidate_native_skills` with reasons, required inputs still missing, and validation checks to run next.
- Return `source_priority_rule`: prefer exact source-name matches, then platform URL fingerprints, then source/platform routing.
- Return `download_status`: `not_applicable`, `probe_only`, or `ready_for_source_skill_download`.
