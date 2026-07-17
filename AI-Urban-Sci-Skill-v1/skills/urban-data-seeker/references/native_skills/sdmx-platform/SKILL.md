---
name: sdmx-platform
description: "Use SDMX statistical API mechanics for dataflows, dimensions, codelists, series keys, frequencies, and official indicator data services. Use when a selected provider exposes SDMX REST patterns and the task requires metadata-driven series construction."
---

# SDMX Platform

Use this platform skill to narrow an urban data task without pretending that platform or family knowledge is a final dataset. Prefer a concrete source skill whenever the provider or dataset is already known.

## When To Use
- Use when the request, URL, or selected source metadata explicitly contains one of these platform fingerprints: SDMX, dataflow, codelist, series key, dimensions.
- Use after source suitability has been narrowed and the remaining work is platform-specific probing or query construction.
- Use to inspect metadata, pagination, filters, fields, assets, or export behavior before acquisition.

## Do Not Use
- Do not guess dimension order, keys, codelist values, or frequencies.
- Do not mix vintages or frequencies silently.
- Do not use SDMX platform mechanics instead of selecting the authoritative provider first.
- Do not use when a concrete official-statistical provider skill (world-bank-indicators, oecd-data, imf-data, ilostat, un-sdg-indicators, etc.) is the actual target; prefer that concrete skill.
- Do not use SDMX mechanics for non-SDMX indicator APIs; check for OData or provider-specific REST patterns first.

## Required Inputs
- `sdmx_base_url`
- `dataflow`
- `dimensions`
- `codelists`
- `time_range`

## Workflow
- Confirm the URL, metadata, or user text really contains this platform's fingerprint.
- Inspect platform metadata before constructing queries or export URLs.
- Route back to the concrete source skill when provider suitability, variables, or licensing are the main question.
- Produce a small, reproducible probe plan before suggesting bulk extraction.

## Tools
- `scripts/build_sdmx_endpoint_templates.py`: no-network helper that returns dataflow, datastructure, and bounded data-query URL templates for a provider SDMX base URL.
  Fast path: `python scripts/build_sdmx_endpoint_templates.py --base-url https://sdmx.oecd.org/public/rest/v1`
- `references/platforms/sdmx_platform/scripts/build_sdmx_hints.py`: build platform hints from URL, metadata, and request text.
- `references/platforms/sdmx_platform/references/platform_notes.md`: read only when platform-specific API behavior, limits, or URL patterns are needed.
- `references/platforms/sdmx_platform/retrieval_profile.md`: read only when retrieval signatures or platform routing evidence must be checked.

## References
- `references/source_card.json`: machine-readable identity, role, and candidate coverage for this native meta skill.
- `references/tool_capabilities.json`: machine-readable action contract and access defaults for this native meta skill.
- `references/platforms/sdmx_platform/README.md`: platform package overview.
- `references/platforms/sdmx_platform/retrieval_profile.md`: retrieval profile used by routing experiments.

## Official Entrypoints
- Local platform package: `references/platforms/sdmx_platform/`
- Platform notes: `references/platforms/sdmx_platform/references/platform_notes.md`

## Direct-URL Evaluation Boundary

For a platform-only direct-URL evaluation, do not infer a city-specific indicator, provider, dataflow, or SDMX series key from scratch. This skill is being tested for SDMX mechanics, not provider selection.

If the request or selected source provides an SDMX `base_url`, construct and probe:

`{base_url}/dataflow/{agency}/{dataflow}/latest`

Use `agency=all` and `dataflow=all` only when no narrower provider dataflow is already known. If no provider base URL is supplied in the prompt, scripts, or references, use the bundled script default only as a public smoke-test example, not as proof that OECD is the user's intended data source:

`python scripts/build_sdmx_endpoint_templates.py`

Expected evidence:
- HTTP status `200`
- SDMX XML/JSON content type or a parseable SDMX structure/data response
- response evidence showing `dataflow`, `datastructure`, `codelist`, or SDMX structure metadata

Use the verified metadata/query endpoint as `api_url`; leave `direct_download_url` empty. Do not use `Range` headers on SDMX metadata endpoints, and do not spend time enumerating all flows, dimensions, codelists, or city-specific series unless a concrete provider/dataflow is already selected.

## Official SDMX Path Templates (Universal)

- Dataflow 元数据（最短）：
  - `{base_url}/dataflow/{agency}/{dataflow}/latest`
  - 可选：`{base_url}/dataflow/{agency}/{dataflow}/latest?references=all`
- Datastructure 元数据：
  - `{base_url}/datastructure/{agency}/{dataflow}/latest?references=all&detail=allstubs`
- 数据查询：
  - `{base_url}/data/{flow_ref}/{key}`
  - 常用时间窗参数：`startPeriod=YYYY`、`endPeriod=YYYY`

`base_url` should come from the selected official provider. Examples include OECD, IMF, ILO, ECB, Eurostat, or national statistical SDMX REST services; do not assume one provider is correct when the user has not selected it.

### Minimal Probe

1. 先用 provider base + `/dataflow/all/all/latest` 验证 SDMX 入口是否可用。Use a normal small `GET`; do not send `Range` to SDMX metadata endpoints because some valid services return `416`.
2. 对候选 `agency`+`dataflow` 做 `/dataflow/{agency}/{dataflow}/latest`，拿到可用维度信息与版本。
3. 再做一次 datastructure 引用探测 `/datastructure/{agency}/{dataflow}/latest?references=all&detail=allstubs`，确认 key 顺序后再进行小范围数据探测。
4. 数据探测示例：`{base_url}/data/{flow_ref}/all?startPeriod=2024&endPeriod=2024&dimensionAtObservation=AllDimensions`（如需可改 `AllDimensions` 或 `TIME_PERIOD`）。

## Access And Download Rules
- Probe first: use metadata, landing pages, small API requests, or source-specific probes before any download.
- Full download is allowed only after a concrete source skill or platform probe verifies authority, schema, license, geography, time period, file size, and user intent.
- This meta skill should return candidate sources or platform actions, not unverified bulk data.
- This platform skill can return a directly queryable metadata API endpoint as `API_PASS`; it should not return a bulk data file unless a concrete provider/dataflow/key has already been selected.

## Validation Focus
- Inspect dataflows, dimensions, codelists, frequencies, and unit metadata.
- Validate series keys before requesting data values.
- Record provider, flow, key, and query URL.

## Output Contract
- Return `selected_skill_type` as `platform`, `family`, or `discovery`.
- Return `candidate_native_skills` with reasons, required inputs still missing, and validation checks to run next.
- Return `source_priority_rule`: prefer exact source-name matches, then platform URL fingerprints, then source/platform routing.
- Return `download_status`: `not_applicable`, `probe_only`, or `ready_for_source_skill_download`.
- For direct-URL evaluation, return `API_PASS` with a verified dataflow/datastructure API URL if no concrete provider series key is known. Do not time out trying to infer all dimensions from a platform-only prompt.
