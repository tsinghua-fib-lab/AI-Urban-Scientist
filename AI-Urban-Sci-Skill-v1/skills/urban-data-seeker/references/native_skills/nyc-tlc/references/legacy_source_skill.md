# NYC TLC SourceSkill

## Purpose

Use this SourceSkill to identify not-final source evidence and candidate resource leads for NYC Taxi & Limousine Commission trip record data.

## When To Use

- The request is about New York City taxi, yellow taxi, green taxi, FHV, pickup/dropoff, fare, trip record, or TLC trip data.
- The data need expects trip-level or monthly trip-record files.
- The requested geography is New York City or a clearly NYC-specific taxi-zone analysis.

## Do Not Use

- Do not use for public transit schedules, GTFS, subway/bus feeds, bike share, parcel land use, 311, or generic mobility requests.
- Do not use outside New York City unless the request explicitly asks for NYC TLC data as a comparison source.
- Do not treat a landing page, file pattern, or source prior as proof of download success.
- known_source is a legacy source-prior registry, not a SourceSkill.

## Inputs

- Original title, abstract, or user dataset requirement.
- Optional need ids and requested vehicle type.
- Optional requested year and month.
- Optional official TLC HTML fixture or page content.
- Optional prior negative evidence.

## Tools/Scripts Used

- `scripts/find_trip_record_files.py`
- `references/source_card.json`
- `references/official_entrypoints.md`
- `references/validation_rules.md`

## Workflow

1. Preserve the original request context.
2. Check NYC TLC applicability and exclusions.
3. Inspect the official TLC entrypoint or a fixture of that page.
4. Emit matching monthly file candidates as not-final resource intent hints.
5. Emit a project-neutral route dossier fragment with positive and negative evidence.
6. Leave resolver, probe, download, and verifier work to downstream deterministic tools.

## Outputs

- Source evidence JSON.
- Candidate resources with `role`, `access_method`, and `required_validation`.
- Not-final resource intent hints.
- Project-neutral route dossier fragment.
- Negative evidence when no matching monthly file is found.

## Failure Rules

- If no concrete monthly file is found, emit negative evidence, not a guessed URL.
- If only the TLC landing page is available, mark the resource as `landing_page` and `not_final`.
- If a requested month or vehicle type is not present, emit an unresolved question.
- Never create resource plans, approve URLs, write downloaded files, or claim success.

## Verification

- Fixture-backed script tests.
- SourceCard lint.
- Forbidden final-chain field scan.
- Optional live checks must be env-gated and must remain non-download by default.
