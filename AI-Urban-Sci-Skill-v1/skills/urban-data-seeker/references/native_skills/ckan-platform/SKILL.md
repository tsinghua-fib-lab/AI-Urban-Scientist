---
name: ckan-platform
description: "Use CKAN catalog mechanics for package search, package metadata, organizations, groups, tags, and resource files. Use when a selected portal exposes CKAN APIs or resource metadata, including government, humanitarian, institutional, and city catalogs, after source suitability has been narrowed."
---

# CKAN Platform

Use this platform skill to narrow an urban data task without pretending that platform or family knowledge is a final dataset. Prefer a concrete source skill whenever the provider or dataset is already known.

## When To Use
- Use when the request, URL, or selected source metadata explicitly contains one of these platform fingerprints: CKAN, package_search, package_show, /api/3/action/, resource metadata.
- Use after source suitability has been narrowed and the remaining work is platform-specific probing or query construction.
- Use to inspect metadata, pagination, filters, fields, assets, or export behavior before acquisition.

## Do Not Use
- Do not rank a CKAN package as final because it matches keywords.
- Do not choose the first resource automatically.
- Do not use CKAN when a concrete source skill already provides a better official endpoint.
- Do not use when hdx-catalog, data-gov-catalog, or a concrete CKAN-backed portal skill already matches the request.
- Do not use for non-CKAN government or institutional catalogs; check for Socrata, ArcGIS, or OData fingerprints first.

## Required Inputs
- `ckan_base_url`
- `query_or_package_id`
- `organization_or_group`
- `resource_format`
- `time_or_update_filter`

## Workflow
- Confirm the URL, metadata, or user text really contains this platform's fingerprint.
- Inspect platform metadata before constructing queries or export URLs.
- Route back to the concrete source skill when provider suitability, variables, or licensing are the main question.
- Produce a small, reproducible probe plan before suggesting bulk extraction.
- Resolve package metadata into concrete resource URLs with `scripts/resolve_ckan_resources.py --domain {domain} --package-id {package}` or `--query {query}`.
- Do not stop at `package_search`; choose and probe an actual `resources[].url`.

## Tools
- `scripts/resolve_ckan_resources.py`: call CKAN `package_show` or `package_search`, extract resource URLs, filter by format, and optionally HEAD-probe candidate files.
- `references/platforms/ckan_platform/scripts/build_ckan_hints.py`: build platform hints from URL, metadata, and request text.
- `references/platforms/ckan_platform/references/platform_notes.md`: read only when platform-specific API behavior, limits, or URL patterns are needed.
- `references/platforms/ckan_platform/retrieval_profile.md`: read only when retrieval signatures or platform routing evidence must be checked.

## References
- `references/source_card.json`: machine-readable identity, role, and candidate coverage for this native meta skill.
- `references/tool_capabilities.json`: machine-readable action contract and access defaults for this native meta skill.
- `references/platforms/ckan_platform/README.md`: platform package overview.
- `references/platforms/ckan_platform/retrieval_profile.md`: retrieval profile used by routing experiments.

## Official Entrypoints
- Local platform package: `references/platforms/ckan_platform/`
- Platform notes: `references/platforms/ckan_platform/references/platform_notes.md`

## Access And Download Rules
- Probe first: use metadata, landing pages, small API requests, or source-specific probes before any download.
- Full download is allowed only after a concrete source skill or platform probe verifies authority, schema, license, geography, time period, file size, and user intent.
- This meta skill should return candidate sources or platform actions, not unverified bulk data.

## Validation Focus
- Check package title, publisher, resource role, format, URL status, license, update date, and schema.
- Prefer direct resource URLs only after landing-page and metadata validation.
- Record API action and parameters used for reproducibility.
- `package_search` and catalog pages are discovery only. Strict success requires a selected package resource URL that probes as data or a documented access boundary.

## Output Contract
- Return `selected_skill_type` as `platform`, `family`, or `discovery`.
- Return `candidate_native_skills` with reasons, required inputs still missing, and validation checks to run next.
- Return `source_priority_rule`: prefer exact source-name matches, then platform URL fingerprints, then source/platform routing.
- Return `download_status`: `not_applicable`, `probe_only`, or `ready_for_source_skill_download`.
