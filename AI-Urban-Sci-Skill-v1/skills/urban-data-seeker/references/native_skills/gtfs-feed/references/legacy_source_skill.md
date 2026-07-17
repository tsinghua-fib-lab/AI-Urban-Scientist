# GTFS Feed SourceSkill

## Purpose

Identify public General Transit Feed Specification (GTFS) feed leads for transit schedule, route, stop, and trip research needs. This skill emits not-final source-prior evidence and resource intent hints only.

## When To Use

Use this skill when the request asks for transit schedules, public transport routes, stops, trips, headways, service calendars, or agency GTFS/static feed data. It is appropriate when a transit agency, region, or feed URL is supplied or can be treated as an official source-prior hint.

## Do Not Use

Do not use this skill for real-time vehicle positions unless the request explicitly asks for GTFS-Realtime. Do not use it for ride-hailing trips, taxi records, transit performance dashboards without feed identity, or generic city open-data portal searches. Do not treat a feed URL as validated just because it ends with `.zip`.

## Inputs

- Original title, abstract, or user dataset requirement.
- Data need id.
- Transit agency or feed name.
- Optional official GTFS feed URL.
- Optional prior negative evidence.

## Tools/Scripts Used

- `scripts/find_gtfs_feed.py`
- `open_data_skills.route_bridge`

## Workflow

1. Preserve the original need text and need id.
2. Check for GTFS/transit-feed signals such as schedule, routes, stops, trips, or agency feed.
3. Emit official or user-supplied feed URLs as not-final candidate resources.
4. Record ambiguity around agency/feed identity and feed freshness.
5. State that future GTFS zip validation requires `stops.txt/routes.txt/trips.txt`.
6. Hand off required validation to resolver, probe, download, and verifier stages.

## Outputs

- Source evidence JSON.
- Not-final route dossier fragment.
- Candidate GTFS feed resource hints.
- Resource intent hints requiring downstream validation.
- Ambiguity and verification notes.

## Failure Rules

- If no feed URL is supplied, emit negative evidence rather than inventing a URL.
- If only an agency page is known, mark it as a landing-page/source-prior lead.
- If a `.zip` URL is supplied, keep it not-final until GTFS contents are verified.
- Never create resource plans, approve URLs, write downloaded files, or claim success.

## Verification

- Fixture-free CLI tests for not-final output shape.
- SourceCard lint.
- Forbidden final-chain field scan.
- Future live or fixture validation should inspect GTFS zip members and require `stops.txt/routes.txt/trips.txt`.

known_source is a legacy source-prior registry, not a SourceSkill.
