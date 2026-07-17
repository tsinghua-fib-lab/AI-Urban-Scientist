# NOAA Weather SourceSkill

## Purpose

Identify NOAA weather, climate, precipitation, temperature, station, and time-range source leads. This skill emits not-final source evidence and resource intent hints for downstream resolver/probe/download/verifier stages.

## When To Use

Use this skill when a request asks for weather observations, climate normals, daily precipitation, daily temperature, NOAA station data, GHCN, NCEI, CDO, or time-ranged meteorological records.

## Do Not Use

Do not use this skill for air quality, hydrology-only stream gauges, satellite imagery, forecast products, or local weather dashboards unless the NOAA dataset family is explicitly needed. Do not treat a station id or dataset endpoint as sufficient without checking variables and time coverage.

## Inputs

- Original title, abstract, or user dataset requirement.
- Data need id.
- NOAA dataset family or search target.
- Optional station id.
- Optional variable list.
- Optional start and end dates.

## Tools/Scripts Used

- `scripts/find_noaa_weather.py`
- `open_data_skills.route_bridge`

## Workflow

1. Preserve the need text and requested time range.
2. Match weather, precipitation, temperature, station, and NOAA signals.
3. Emit NOAA/NCEI or CDO search/API entrypoints as not-final resource hints.
4. Record station/time/variable ambiguity explicitly.
5. Hand off validation to resolver, probe, download, and verifier stages.

## Outputs

- Source evidence JSON.
- Not-final route dossier fragment.
- Candidate NOAA search or API resource hints.
- Resource intent hints requiring downstream validation.
- Ambiguity notes for station, time range, and variable coverage.

## Failure Rules

- If station, time range, or variables are missing, emit ambiguity evidence instead of guessing.
- If only a NOAA search page is available, keep it as a source-prior lead.
- If an API endpoint is suggested, do not claim it covers the requested variables or dates until validated.
- Never create resource plans, approve URLs, write downloaded files, or claim success.

## Verification

- Fixture-free CLI tests for not-final output shape.
- SourceCard lint.
- Forbidden final-chain field scan.
- Optional future live smoke must be env-gated and must not require credentials by default.

known_source is a legacy source-prior registry, not a SourceSkill.
