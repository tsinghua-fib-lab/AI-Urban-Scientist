---
name: legistar-platform
description: "Use Granicus Legistar portal mechanics for municipal legislation, ordinances, resolutions, agendas, meetings, votes, files, attachments, and legislative history. Use when a URL or source page is a Legistar portal, or after a Legistar source skill has selected a legislative record to probe."
---

# Legistar Platform

Use this platform skill to narrow an urban data task without pretending that platform or family knowledge is a final dataset. Prefer a concrete source skill whenever the provider or dataset is already known.

## When To Use
- Use when the request, URL, or selected source metadata explicitly contains one of these platform fingerprints: Legistar, LegislationDetail, Calendar.aspx, Granicus, Matter, File ID.
- Use after source suitability has been narrowed and the remaining work is platform-specific probing or query construction.
- Use to inspect metadata, pagination, filters, fields, assets, or export behavior before acquisition.

## Do Not Use
- Do not trigger on general policy-document requests unless Legistar is explicit.
- Do not treat introduced bills as enacted policy.
- Do not ignore amendments, substitutes, attachments, votes, or meeting history.
- Do not use when legistar-legislation is the concrete source skill matching the request; prefer that source skill for legislative records.
- Do not use for planning documents; prefer planning-document-portal or document-portal-platform.

## Required Inputs
- `legistar_url_or_portal`
- `matter_or_file_id`
- `jurisdiction`
- `record_type`
- `status_or_date`

## Workflow
- Confirm the URL, metadata, or user text really contains this platform's fingerprint.
- Inspect platform metadata before constructing queries or export URLs.
- Route back to the concrete source skill when provider suitability, variables, or licensing are the main question.
- Produce a small, reproducible probe plan before suggesting bulk extraction.
- For Granicus Legistar, use `scripts/resolve_legistar_api.py --system legistar --client {client} --query "{topic}" --probe` when a public client API is available.
- For Chicago eLMS, use `scripts/resolve_legistar_api.py --system chicago-elms --query "{topic}" --probe` and validate against the official swagger endpoint.
- A generic `Legislation.aspx` page is a resolver only, not strict success.

## Tools
- `scripts/resolve_legistar_api.py`: build and optionally probe Granicus Legistar Web API or Chicago eLMS search API URLs for legislative records.
- `references/platforms/legistar_platform/scripts/build_legistar_hints.py`: build platform hints from URL, metadata, and request text.
- `references/platforms/legistar_platform/references/platform_notes.md`: read only when platform-specific API behavior, limits, or URL patterns are needed.
- `references/platforms/legistar_platform/retrieval_profile.md`: read only when retrieval signatures or platform routing evidence must be checked.

## References
- `references/source_card.json`: machine-readable identity, role, and candidate coverage for this native meta skill.
- `references/tool_capabilities.json`: machine-readable action contract and access defaults for this native meta skill.
- `references/platforms/legistar_platform/README.md`: platform package overview.
- `references/platforms/legistar_platform/retrieval_profile.md`: retrieval profile used by routing experiments.

## Official Entrypoints
- Local platform package: `references/platforms/legistar_platform/`
- Platform notes: `references/platforms/legistar_platform/references/platform_notes.md`
- Granicus Legistar Web API: https://webapi.legistar.com/
- Chicago eLMS API swagger: https://api.chicityclerkelms.chicago.gov/swagger.json

## Access And Download Rules
- Probe first: use metadata, landing pages, small API requests, or source-specific probes before any download.
- Full download is allowed only after a concrete source skill or platform probe verifies authority, schema, license, geography, time period, file size, and user intent.
- This meta skill should return candidate sources or platform actions, not unverified bulk data.

## Validation Focus
- Check record status, dates, sponsors, votes, attachments, meetings, and official city context.
- Separate legislative history from adopted policy claims.
- Return stable record URLs and attachment candidates.
- For strict success, return a working API search/detail URL or specific record URL with fields for title, status, dates, sponsor/body, and attachment/text path.
- Some Legistar clients require tokens. If a token error is returned, classify as access boundary instead of fabricating a portal-only success.

## Output Contract
- Return `selected_skill_type` as `platform`, `family`, or `discovery`.
- Return `candidate_native_skills` with reasons, required inputs still missing, and validation checks to run next.
- Return `source_priority_rule`: prefer exact source-name matches, then platform URL fingerprints, then source/platform routing.
- Return `download_status`: `not_applicable`, `probe_only`, or `ready_for_source_skill_download`.
