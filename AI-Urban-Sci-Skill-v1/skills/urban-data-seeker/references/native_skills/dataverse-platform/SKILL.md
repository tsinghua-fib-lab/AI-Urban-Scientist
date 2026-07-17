---
name: dataverse-platform
description: "Use Dataverse repository mechanics for dataset pages, persistent identifiers, versions, file metadata, citations, terms, and file-access APIs. Use when a URL or landing page explicitly indicates a Dataverse installation, dataset.xhtml, persistentId, or Dataverse API path."
---

# Dataverse Platform

Use this platform skill to narrow an urban data task without pretending that platform or family knowledge is a final dataset. Prefer a concrete source skill whenever the provider or dataset is already known.

## When To Use
- Use when the request, URL, or selected source metadata explicitly contains one of these platform fingerprints: Dataverse, dataset.xhtml, persistentId, /api/datasets/, /api/access/datafile/.
- Use after source suitability has been narrowed and the remaining work is platform-specific probing or query construction.
- Use to inspect metadata, pagination, filters, fields, assets, or export behavior before acquisition.

## Do Not Use
- Do not trigger on DOI or Handle alone unless the landing page is Dataverse.
- Do not assume all files are public or current.
- Do not bypass restricted files, terms, or embargoes.
- Do not use when zenodo-repository, figshare-repository, dryad-repository, or osf-repository is the actual host; prefer those concrete repository skills instead.
- Do not use for general repository or dataset-DOI questions before confirming the host is Dataverse.

## Required Inputs
- `dataverse_url_or_pid`
- `dataset_version`
- `file_role_or_format`
- `download_required`
- `license_or_terms_required`

## Workflow
- Confirm the URL, metadata, or user text really contains this platform's fingerprint.
- Inspect platform metadata before constructing queries or export URLs.
- Route back to the concrete source skill when provider suitability, variables, or licensing are the main question.
- Produce a small, reproducible probe plan before suggesting bulk extraction.
- If the supplied URL does not expose Dataverse fingerprints, stop and report platform mismatch instead of fabricating a Dataverse API URL.

## Tools
- `references/platforms/dataverse_platform/scripts/build_dataverse_hints.py`: build platform hints from URL, metadata, and request text.
- `references/platforms/dataverse_platform/references/platform_notes.md`: read only when platform-specific API behavior, limits, or URL patterns are needed.
- `references/platforms/dataverse_platform/retrieval_profile.md`: read only when retrieval signatures or platform routing evidence must be checked.

## References
- `references/source_card.json`: machine-readable identity, role, and candidate coverage for this native meta skill.
- `references/tool_capabilities.json`: machine-readable action contract and access defaults for this native meta skill.
- `references/platforms/dataverse_platform/README.md`: platform package overview.
- `references/platforms/dataverse_platform/retrieval_profile.md`: retrieval profile used by routing experiments.
- `references/version_file_rules.md`: persistentId/version/file-id rules and restricted-file validation points.

## Official Entrypoints
- Local platform package: `references/platforms/dataverse_platform/`
- Platform notes: `references/platforms/dataverse_platform/references/platform_notes.md`
- Dataverse native API docs: https://guides.dataverse.org/en/latest/api/native-api.html
- Dataverse data access API docs: https://guides.dataverse.org/en/latest/api/dataaccess.html

## Direct API Resolution
- Valid Dataverse dataset pages usually contain `dataset.xhtml`, `persistentId=`, `/api/datasets/:persistentId`, or Dataverse installation UI/API fingerprints.
- From a real Dataverse installation, resolve dataset metadata with `/api/datasets/:persistentId/?persistentId={PID}` or version metadata with `/api/datasets/:persistentId/versions/{version}?persistentId={PID}`.
- Choose a file from the returned file metadata by filename, MIME type, description, tabular tags, and restricted/embargo status.
- Return `/api/access/datafile/{file_id}` or `/api/access/datafile/:persistentId?persistentId={file_pid}` as `direct_download_url` only after the file id or file persistent id exists in metadata.
- Never substitute a non-Dataverse catalog URL into Dataverse placeholder syntax. URLs containing literal `:persistentId` with no real identifier are invalid and should be rejected.
- If the host is Socrata, ArcGIS, CKAN, OSF, Zenodo, or another repository, return `RESOLVABLE_PASS` with `platform_mismatch` and name the correct skill to use.

## Access And Download Rules
- Probe first: use metadata, landing pages, small API requests, or source-specific probes before any download.
- Full download is allowed only after a concrete source skill or platform probe verifies authority, schema, license, geography, time period, file size, and user intent.
- This meta skill should return candidate sources or platform actions, not unverified bulk data.

## Validation Focus
- Check dataset version, file metadata, terms, restrictions, citation, and file role.
- Separate metadata-only DOI resolution from file acquisition.
- Use version-specific APIs when reproducibility matters.

## Output Contract
- Return `selected_skill_type` as `platform`, `family`, or `discovery`.
- Return `candidate_native_skills` with reasons, required inputs still missing, and validation checks to run next.
- Return `source_priority_rule`: prefer exact source-name matches, then platform URL fingerprints, then source/platform routing.
- Return `download_status`: `not_applicable`, `probe_only`, or `ready_for_source_skill_download`.
