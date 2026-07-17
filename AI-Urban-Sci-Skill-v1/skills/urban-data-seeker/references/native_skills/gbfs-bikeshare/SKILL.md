---
name: gbfs-bikeshare
description: "Find, access, sample, and validate GBFS bikeshare feeds. Use for station_status, station_information, free_bike_status, system_information, vehicle availability, dock availability, bikeshare station networks, shared micromobility feeds, and realtime or near-realtime GBFS API requests."
---

<!-- generated-by: migrate_source_skills_to_native.py -->

# GBFS Bikeshare Feeds

Use this skill to find, access, sample, and validate authoritative data from this source. Treat returned URLs and files as candidates until the source, schema, license, geography, time period, and requested variables are verified.

## When To Use

- Use for bikeshare or micromobility GBFS feeds and station/vehicle availability.
- Use when the request names GBFS, station_status, station_information, free_bike_status, or a bikeshare system.
- Use when the task needs feed discovery through a systems catalog or operator endpoint.
- Use when the user names `gbfs_bikeshare`, `gbfs-bikeshare`, or GBFS Bikeshare Feeds.

## Do Not Use

- Do not use for historical trip records unless a separate trip-history archive is requested.
- Do not use for GTFS transit schedules, taxi data, or traffic sensors.
- Do not treat realtime snapshots as historical demand without repeated collection.

## Required Inputs

- `system_or_city`
- `feed_url_optional`
- `gbfs_version_optional`
- `endpoint`
- `snapshot_time`

## Workflow

1. Identify the bikeshare system, city, and required GBFS endpoint.
2. Run the finder to locate official GBFS discovery URLs or catalog records.
3. Probe gbfs.json, language feeds, version, TTL, and required endpoint availability.
4. Fetch a capped snapshot for station or vehicle schema checks.
5. Validate station IDs, coordinates, bike/dock availability, timestamps, TTL, and license terms.

## Tools

- `scripts/check_gbfs_bikeshare_access.py`: check access status, authorization requirements, and current availability.
- `scripts/fetch_gbfs_sample.py`: fetch a capped sample or approved resource payload.
- `scripts/find_gbfs_feed.py`: find candidate resources, API endpoints, files, or catalog records.
- `scripts/probe_gbfs_feed.py`: probe metadata, schema, variables, or resource headers before download.
- `scripts/validate_gbfs_result.py`: validate returned files, fields, schema, or source suitability.

## References

- `references/source_card.json`: publisher, access status, authoritative URLs, and source-specific validation notes.
- `references/tool_capabilities.json`: available tool actions, access constraints, and download/probe behavior.
- `references/validation_rules.md`: source-specific documentation and validation guidance.
- `references/retrieval_profile.md`: retrieval cues and boundary cases retained from the source package.
- `references/legacy_source_skill.md`: archived pre-migration notes; prefer this SKILL.md for current workflow.

## Official Entrypoints

- GBFS specification: https://github.com/MobilityData/gbfs
- GBFS systems catalog: https://github.com/MobilityData/gbfs/blob/master/systems.csv

## Access And Download Rules

- Current access status from the source card: `open`.
- Authorization required: `false`.
- Probe first when a script supports probe/check mode; do not perform full download as a side effect of search.
- Full download is allowed only after confirming the user intent, source terms, file size, and destination path.
- GBFS is an open data standard for public shared-mobility availability feeds.
- Concrete system feeds still require discovery URL, version, freshness, and schema validation.

## Validation Focus

- Check GBFS version, TTL, last_updated, and endpoint presence.
- Distinguish station-based and free-floating systems.
- State that one snapshot is not a historical time series.

## Output Contract

- Return discovery URL, selected endpoint URLs, GBFS version, timestamp, and snapshot status.
- Report whether output is metadata, a live sample, or a repeated-collection requirement.
- Flag missing endpoints or stale feeds.

## Supported Actions

- `find`
- `access_check`
- `probe`
- `fetch_sample`
- `download_link`
- `download`
- `validate`
