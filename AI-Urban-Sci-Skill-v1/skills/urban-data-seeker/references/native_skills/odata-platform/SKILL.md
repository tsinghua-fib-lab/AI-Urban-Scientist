---
name: odata-platform
description: "Use OData REST mechanics for service roots, metadata documents, entity sets, selected fields, filters, pagination, and JSON payloads. Use when an official API explicitly exposes OData paths such as WHO GHO-style services, $metadata endpoints, or entity-set URLs."
---

# OData Platform

Use this platform skill to narrow an urban data task without pretending that platform or family knowledge is a final dataset. Prefer a concrete source skill whenever the provider or dataset is already known.

## When To Use
- Use when the request, URL, or selected source metadata explicitly contains one of these platform fingerprints: OData, $metadata, $filter, $select, $top, $skip.
- Use after source suitability has been narrowed and the remaining work is platform-specific probing or query construction.
- Use to inspect metadata, pagination, filters, fields, assets, or export behavior before acquisition.

## Do Not Use
- Do not infer filter values or entity semantics without metadata.
- Do not ignore pagination or server-side limits.
- Do not treat an entity-set listing as the final indicator table.
- Do not use when who-gho is the concrete source skill matching the request; prefer that source skill for WHO indicators.
- Do not use for generic REST APIs that do not expose OData metadata; check for Socrata, CKAN, or SDMX fingerprints first.
- Do not classify a non-OData source as `AUTH_REQUIRED` just because an OData probe fails. If fingerprints show Socrata/CKAN/ArcGIS/SDMX instead, return `RESOLVABLE_PASS` with the detected platform mismatch and the correct platform family.

## Required Inputs
- `odata_service_root`
- `entity_set`
- `filters`
- `fields`
- `pagination_limit`

## Workflow
- Confirm the URL, metadata, or user text really contains this platform's fingerprint.
- Inspect platform metadata before constructing queries or export URLs.
- Route back to the concrete source skill when provider suitability, variables, or licensing are the main question.
- Produce a small, reproducible probe plan before suggesting bulk extraction.
- If the service root does not expose OData metadata or OData syntax, do not force OData parameters onto it; report the detected platform mismatch.

## Tools
- `references/platforms/odata_platform/scripts/build_odata_hints.py`: build platform hints from URL, metadata, and request text.
- `references/platforms/odata_platform/references/platform_notes.md`: read only when platform-specific API behavior, limits, or URL patterns are needed.
- `references/platforms/odata_platform/retrieval_profile.md`: read only when retrieval signatures or platform routing evidence must be checked.

## References
- `references/source_card.json`: machine-readable identity, role, and candidate coverage for this native meta skill.
- `references/tool_capabilities.json`: machine-readable action contract and access defaults for this native meta skill.
- `references/platforms/odata_platform/README.md`: platform package overview.
- `references/platforms/odata_platform/retrieval_profile.md`: retrieval profile used by routing experiments.

## Official Entrypoints
- Local platform package: `references/platforms/odata_platform/`
- Platform notes: `references/platforms/odata_platform/references/platform_notes.md`
- OData documentation: https://www.odata.org/documentation/

## Direct Query Construction
- Start with the service root and fetch `$metadata` or the service document to confirm entity set names and property names.
- Use OData parameter names exactly: `$select`, `$filter`, `$orderby`, `$top`, `$skip`, and `$format` when supported by that service.
- Encode query parameters but keep the final URL human-auditable. Example pattern: `{service_root}/{entity_set}?$select=a,b&$orderby=date desc&$top=10&$skip=0`.
- Do not call Socrata SoQL, CKAN, ArcGIS REST, or plain JSON APIs OData. Socrata uses `$select`, `$order`, `$limit`, and `$offset`, but it is not OData and should route to Socrata/source-specific mechanics.
- If entity set or field names are unknown, return the `$metadata` URL as the next required API step, not a fabricated entity query.
- Return `OPEN_API_PASS` only when the entity set and fields are confirmed and a small query URL is valid.

## Access And Download Rules
- Probe first: use metadata, landing pages, small API requests, or source-specific probes before any download.
- Full download is allowed only after a concrete source skill or platform probe verifies authority, schema, license, geography, time period, file size, and user intent.
- This meta skill should return candidate sources or platform actions, not unverified bulk data.
- A `$metadata` failure on a Socrata or other non-OData service is a platform mismatch, not an authorization boundary.

## Validation Focus
- Inspect $metadata, entity fields, key fields, filter support, and pagination behavior.
- Probe small requests before exporting rows.
- Record exact query URL and parameters.

## Output Contract
- Return `selected_skill_type` as `platform`, `family`, or `discovery`.
- Return `candidate_native_skills` with reasons, required inputs still missing, and validation checks to run next.
- Return `source_priority_rule`: prefer exact source-name matches, then platform URL fingerprints, then source/platform routing.
- Return `download_status`: `not_applicable`, `probe_only`, or `ready_for_source_skill_download`.
