# GBFS Bikeshare SourceSkill

## Purpose

Emit not-final source-prior hints for General Bikeshare Feed Specification feeds, including station information, station status, free-bike status, and related bikeshare metadata.

## When To Use

Use when a data need asks for bikeshare availability, station status, vehicle status, system metadata, or feed-discovery hints for a GBFS-compatible system.

## Do Not Use

Do not use for long-term trip histories unless the publisher explicitly provides historical GBFS archives or separate trip-data products. Never create resource plans, approve URLs, write downloaded files, or claim success.

## Inputs

- `need_id`: Route-agent need identifier.
- `need_text`: User-facing data need text.
- `system_name`: Bikeshare system name.
- `region`: City, region, or operating market.
- `feed_url`: Optional known GBFS discovery URL.

## Tools/Scripts Used

- `scripts/find_gbfs_feed.py`: Emits GBFS source-prior feed hints and ambiguity notes.
- Future platform tools may inspect GBFS discovery JSON and versioned endpoint availability.

## Workflow

1. Match the need to a GBFS system and region.
2. Emit a provided GBFS discovery URL, or a public GBFS systems catalog lead when no feed URL is known.
3. Preserve system, endpoint, freshness, and history ambiguity.
4. Return RouteDossier and RouteResourceIntent fragments marked `not-final`.

## Outputs

- SourceSkill payload with `finality=not_final` and `consumer_authority=none`.
- Candidate resource hints that require resolver, probe, download, and verifier steps.
- Ambiguity notes for real-time versus historical suitability.

## Failure Rules

- If no feed URL is known, emit a catalog/search hint instead of fabricating a system URL.
- If the need asks for historical trips, require separate proof that the publisher exposes history.
- Do not treat a live GBFS endpoint as sufficient for retrospective analysis without verifier evidence.

## Verification

Future verification must confirm GBFS discovery JSON, system identity, endpoint list, feed freshness, language/version fields, and whether the requested analysis needs real-time versus historical data.
