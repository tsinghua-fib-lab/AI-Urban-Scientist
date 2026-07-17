# World Bank Indicators SourceSkill

## Purpose

Emit not-final source-prior hints for World Bank indicator API calls by country, indicator code, and time range.

## When To Use

Use when the need asks for country-level development indicators from World Bank DataBank or the World Bank Indicators API.

## Do Not Use

Do not use for city microdata, World Bank project documents, SDMX-only providers, or non-World-Bank publisher-native APIs. Never create resource plans, approve URLs, write downloaded files, or claim success.

All emitted payloads must keep `finality=not_final` and `consumer_authority=none`.

## Inputs

- `need_id`
- `need_text`
- `country`
- `indicator`
- `start_year`
- `end_year`

## Tools/Scripts Used

- `scripts/find_world_bank_indicators.py` emits not-final World Bank REST API hints.

This uses the official World Bank Indicators API, not a generic platform tool.

## Workflow

1. Resolve country code and indicator code from source evidence.
2. Emit an API URL when country and indicator are known.
3. Preserve year-range ambiguity and indicator-definition ambiguity.
4. Pass the hint to downstream resolver, probe, acquisition, and verifier stages.

## Outputs

SourceSkill payload with not-final API candidate resources and route/resource intent fragments.

## Failure Rules

If `country` or `indicator` is missing, emit a source landing hint only. Do not invent indicator codes or countries.

## Verification

Validate country code, indicator metadata, date coverage, paging, units, aggregation method, and license before acquisition.
