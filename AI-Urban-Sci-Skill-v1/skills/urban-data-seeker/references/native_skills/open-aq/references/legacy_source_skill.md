# OpenAQ SourceSkill

## Purpose

Use OpenAQ when a research need asks for ambient air-quality measurements from the OpenAQ API, especially pollutant, station/location, and time-window searches across many providers.

## When To Use

Use this SourceSkill for air-quality observations when the need mentions OpenAQ, pollutant measurements, sensors, stations, locations, or cross-provider air monitoring.

## Do Not Use

Do not use this skill for EPA-only AirData workflows, gridded chemical transport model products, emissions inventories, or meteorological observations.

## Inputs

- `need_id`
- `need_text`
- `pollutant`
- `location`
- `start_date`
- `end_date`

## Tools/Scripts Used

- `scripts/find_open_aq.py` emits not-final OpenAQ API source-prior hints.

## Workflow

1. Identify pollutant, location, and date-window requirements.
2. Emit an OpenAQ measurements API template and resolver/probe hints.
3. Mark incomplete requests as `source_landing`.
4. Pass output to a route runner for validation and final resource decisions.

## Outputs

The script emits a SourceSkill payload with `route_dossier_fragment`, `candidate_resources`, and `resource_intents`. Outputs are not-final source-prior hints.

## Failure Rules

Never create resource plans, approve URLs, write downloaded files, or claim success. If pollutant, location, or dates are missing, emit a source landing hint only.

## Verification

Validate pollutant names, OpenAQ location identity, provider coverage, timestamps, API paging behavior, and schema before acquisition.
