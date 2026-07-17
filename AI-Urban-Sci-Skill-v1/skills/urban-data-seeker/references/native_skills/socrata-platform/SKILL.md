---
name: socrata-platform
description: "Use Socrata-powered open-data portal and SODA API mechanics for tabular city, county, state, or federal datasets. Use when a URL contains a Socrata domain or four-by-four view id, or when a selected source requires Socrata metadata, SoQL, pagination, export, or schema probing."
---

# Socrata Platform

Use this platform skill to narrow an urban data task without pretending that platform or family knowledge is a final dataset. Prefer a concrete source skill whenever the provider or dataset is already known.

## When To Use
- Use when the request, URL, or selected source metadata explicitly contains one of these platform fingerprints: Socrata, SODA, SoQL, four-by-four view id, data.cityof.
- Use after source suitability has been narrowed and the remaining work is platform-specific probing or query construction.
- Use to inspect metadata, pagination, filters, fields, assets, or export behavior before acquisition.

## Do Not Use
- Do not infer data quality from portal rank or title alone.
- Do not use Socrata mechanics for non-tabular repositories, imagery, or statistical APIs.
- Do not treat CSV export availability as final acquisition.
- Do not use when a concrete Socrata-backed portal skill already matches the request; prefer chicago-open-data for Chicago-specific tables, or the corresponding city portal skill when the city is named.
- Do not use for a known non-Socrata URL even if the data looks tabular; check for CKAN, ArcGIS, or OData fingerprints first.

## Required Inputs
- `socrata_domain_or_view`
- `fields_needed`
- `filters`
- `row_limit`
- `download_required`

## Workflow
- Confirm the URL, metadata, or user text really contains this platform's fingerprint.
- Inspect platform metadata before constructing queries or export URLs.
- Route back to the concrete source skill when provider suitability, variables, or licensing are the main question.
- Produce a small, reproducible probe plan before suggesting bulk extraction.
- When a view ID is known, run `scripts/build_socrata_direct_url.py` to produce metadata, rows export, and resource API URLs. Use `--full-export` only after metadata confirms the selected table is semantically correct.

## Tools
- `scripts/build_socrata_direct_url.py`: construct metadata, bounded sample, full export, and resource API URLs from a verified domain and view ID.
- `references/platforms/socrata_platform/scripts/build_socrata_hints.py`: build platform hints from URL, metadata, and request text.
- `references/platforms/socrata_platform/references/platform_notes.md`: read only when platform-specific API behavior, limits, or URL patterns are needed.
- `references/platforms/socrata_platform/retrieval_profile.md`: read only when retrieval signatures or platform routing evidence must be checked.

## References
- `references/source_card.json`: machine-readable identity, role, and candidate coverage for this native meta skill.
- `references/tool_capabilities.json`: machine-readable action contract and access defaults for this native meta skill.
- `references/platforms/socrata_platform/README.md`: platform package overview.
- `references/platforms/socrata_platform/retrieval_profile.md`: retrieval profile used by routing experiments.
- `references/query_patterns.md`: SoQL/app-token/export/probing patterns, and common Socrata failure modes.

## Official Entrypoints
- Local platform package: `references/platforms/socrata_platform/`
- Platform notes: `references/platforms/socrata_platform/references/platform_notes.md`

## Direct Export Workflow
- Verify metadata at `https://{domain}/api/views/{view_id}.json`.
- Build a bounded probe with `python scripts/build_socrata_direct_url.py --domain {domain} --view-id {view_id} --format json --limit 5`.
- For final direct export after metadata/field checks, build `python scripts/build_socrata_direct_url.py --domain {domain} --view-id {view_id} --format csv --full-export` and return either the unbounded `.csv` resource URL, `rows.csv?accessType=DOWNLOAD`, or a filtered URL that covers the requested date/geography.
- If a platform-mechanics task names Chicago but supplies no view ID or data topic, use the public Building Permits view `ydr8-5enu` only as a smoke test of Socrata export mechanics: `https://data.cityofchicago.org/resource/ydr8-5enu.csv?%24limit=1`. State that it is a mechanics example, not an inferred user dataset.
- Public datasets normally allow unauthenticated reads. App tokens improve quotas but are not universally mandatory; do not infer `AUTH_REQUIRED` from a single `403` without an explicit token error.
- Shell-quote URLs containing `$limit`, `$where`, or `$select`; otherwise the shell can remove parameter names and create a misleading `400`.
- Do not return a `$limit=1` or `$limit=5` sample URL as `DIRECT_PASS`; samples are probes, not final retrieval.
- Return `DIRECT_PASS` only when the export/API URL covers the requested dataset scope and a bounded probe confirms CSV/JSON/GeoJSON data bytes. Metadata and catalog URLs are not final assets.

## Access And Download Rules
- Probe first: use metadata, landing pages, small API requests, or source-specific probes before any download.
- Full download is allowed only after a concrete source skill or platform probe verifies authority, schema, license, geography, time period, file size, and user intent.
- This meta skill should return candidate sources or platform actions, not unverified bulk data.

## Validation Focus
- Check metadata, field names/types, row count, update frequency, license, publisher, and API limits.
- Probe with small SoQL queries before bulk export.
- Return landing page, API endpoint, and query parameters.
- Treat HTTP 200 Socrata error JSON, missing view IDs, shell-stripped `$` parameters, and stale portal pages as failures until repaired.

## Output Contract
- Return `selected_skill_type` as `platform`, `family`, or `discovery`.
- Return `candidate_native_skills` with reasons, required inputs still missing, and validation checks to run next.
- Return `source_priority_rule`: prefer exact source-name matches, then platform URL fingerprints, then source/platform routing.
- Return `download_status`: `not_applicable`, `probe_only`, or `ready_for_source_skill_download`.
