# Census ACS SourceSkill

## Purpose

Identify U.S. Census American Community Survey (ACS) table/API source leads for demographic, socioeconomic, geography, tract, block group, and variable-specific data needs. This skill emits not-final source evidence and resource intent hints only.

## When To Use

Use this skill when the request asks for ACS, Census demographics, tract or block group variables, population, income, housing, race/ethnicity, commute, education, or other ACS table fields.

## Do Not Use

Do not use this skill for decennial-only redistricting data, TIGER boundary files without attributes, local administrative records, LEHD/LODES employment data, or non-U.S. geographies. Do not treat a Census API endpoint as sufficient until variables, geography, vintage, and predicates are validated.

## Inputs

- Original title, abstract, or user dataset requirement.
- Data need id.
- ACS year and survey.
- Geography such as tract, block group, county, or place.
- ACS variable ids or table ids.

## Tools/Scripts Used

- `scripts/find_acs_tables.py`
- `open_data_skills.route_bridge`

## Workflow

1. Preserve the need text and requested variables.
2. Match ACS/Census demographic signals and requested geography.
3. Emit Census API/table entrypoints as not-final resource hints.
4. Record variable/geography/year ambiguity explicitly.
5. Hand off validation to resolver, probe, download, and verifier stages.

## Outputs

- Source evidence JSON.
- Not-final route dossier fragment.
- Candidate Census/ACS API or table resource hints.
- Resource intent hints requiring downstream validation.
- Ambiguity notes for variables, geography, and year.

## Failure Rules

- If variables, geography, or year are missing, emit ambiguity evidence instead of guessing.
- If only a table family is known, keep it as a source-prior lead.
- If an API endpoint is suggested, do not claim it contains the requested variables or geographies until validated.
- Never create resource plans, approve URLs, write downloaded files, or claim success.

## Verification

- Fixture-free CLI tests for not-final output shape.
- SourceCard lint.
- Forbidden final-chain field scan.
- Optional future live smoke must be env-gated and must not require API keys by default.

known_source is a legacy source-prior registry, not a SourceSkill.
