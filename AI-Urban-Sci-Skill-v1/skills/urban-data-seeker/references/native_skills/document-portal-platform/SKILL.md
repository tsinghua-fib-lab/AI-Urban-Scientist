---
name: document-portal-platform
description: "Use official HTML/PDF document portal mechanics for planning pages, report landing pages, comprehensive plans, zoning documents, environmental reports, and policy repositories. Use when the selected evidence source is document-backed rather than an API table and official status or version must be verified."
---

# Document Portal Platform

Use this platform skill to narrow an urban data task without pretending that platform or family knowledge is a final dataset. Prefer a concrete source skill whenever the provider or dataset is already known.

## When To Use
- Use when the request, URL, or selected source metadata explicitly contains one of these platform fingerprints: official PDF, planning document, comprehensive plan, zoning report, environmental report.
- Use after source suitability has been narrowed and the remaining work is platform-specific probing or query construction.
- Use to inspect metadata, pagination, filters, fields, assets, or export behavior before acquisition.

## Do Not Use
- Do not treat any search-result PDF as authoritative without publisher and status checks.
- Do not convert narrative documents into structured datasets without caveats.
- Do not use for Legistar records when a Legistar portal is explicit.
- Do not use when planning-document-portal is the concrete source skill matching the request; prefer that source skill for planning documents.
- Do not use for structured tabular datasets; prefer the corresponding data-portal or source skill.

## Required Inputs
- `portal_or_page_url`
- `document_topic`
- `jurisdiction`
- `status_or_date`
- `file_type`

## Workflow
- Confirm the URL, metadata, or user text really contains this platform's fingerprint.
- Inspect platform metadata before constructing queries or export URLs.
- Route back to the concrete source skill when provider suitability, variables, or licensing are the main question.
- Produce a small, reproducible probe plan before suggesting bulk extraction.

## Tools
- `references/platforms/document_portal_platform/scripts/build_document_portal_hints.py`: build platform hints from URL, metadata, and request text.
- `references/platforms/document_portal_platform/references/platform_notes.md`: read only when platform-specific API behavior, limits, or URL patterns are needed.
- `references/platforms/document_portal_platform/retrieval_profile.md`: read only when retrieval signatures or platform routing evidence must be checked.

## References
- `references/source_card.json`: machine-readable identity, role, and candidate coverage for this native meta skill.
- `references/tool_capabilities.json`: machine-readable action contract and access defaults for this native meta skill.
- `references/platforms/document_portal_platform/README.md`: platform package overview.
- `references/platforms/document_portal_platform/retrieval_profile.md`: retrieval profile used by routing experiments.

## Official Entrypoints
- Local platform package: `references/platforms/document_portal_platform/`
- Platform notes: `references/platforms/document_portal_platform/references/platform_notes.md`

## Access And Download Rules
- Probe first: use metadata, landing pages, small API requests, or source-specific probes before any download.
- Full download is allowed only after a concrete source skill or platform probe verifies authority, schema, license, geography, time period, file size, and user intent.
- This meta skill should return candidate sources or platform actions, not unverified bulk data.

## Validation Focus
- Check publisher, adoption/status, date, amendments, appendices, and canonical landing page.
- Keep HTML/PDF evidence linked to official context.
- Document extraction limits when producing structured fields from text.

## Output Contract
- Return `selected_skill_type` as `platform`, `family`, or `discovery`.
- Return `candidate_native_skills` with reasons, required inputs still missing, and validation checks to run next.
- Return `source_priority_rule`: prefer exact source-name matches, then platform URL fingerprints, then source/platform routing.
- Return `download_status`: `not_applicable`, `probe_only`, or `ready_for_source_skill_download`.
