---
name: gtfs-feed
description: "Find, access, sample, and validate GTFS static schedule feeds. Use for transit routes, stops, trips, stop_times, calendars, service dates, shapes, agency feeds, schedule archives, GTFS zip files, and public transportation network or accessibility analysis."
---

<!-- generated-by: migrate_source_skills_to_native.py -->

# GTFS Schedule Feeds

Use this skill to find, access, sample, and validate authoritative data from this source. Treat returned URLs and files as candidates until the source, schema, license, geography, time period, and requested variables are verified.

## When To Use

- Use for static GTFS schedule feeds, route/stop/trip tables, calendars, and shapes.
- Use when the task needs transit service geometry, stop locations, headways, or schedule-derived accessibility.
- Use for agency feed discovery before running a GTFS validator or parser.
- Use when the user names `gtfs_feed`, `gtfs-feed`, or GTFS Schedule Feeds.

## Do Not Use

- Do not use for realtime vehicle positions unless a GTFS-Realtime source is separately identified.
- Do not use for bikeshare GBFS, taxi trips, traffic sensors, or fare transaction data.
- Do not assume a feed is current without checking feed_info, calendar, and agency publication date.

## Required Inputs

- `agency_or_region`
- `service_date_or_date_range`
- `needed_tables`
- `current_or_archive`

## Workflow

1. Identify the transit agency, region, target service dates, and static GTFS tables needed.
2. Run the feed finder to locate official or cataloged GTFS zip candidates.
3. Probe the feed URL for availability, file size, zip contents, and feed_info dates.
4. Fetch a capped or approved feed sample before parsing large archives.
5. Validate required tables, calendar coverage, stop coordinates, route/trip relationships, and shape availability.

## Tools

- `scripts/check_gtfs_feed_access.py`: check access status, authorization requirements, and current availability.
- `scripts/fetch_gtfs_feed.py`: fetch a capped sample or approved resource payload.
- `scripts/find_gtfs_feed.py`: find candidate resources, API endpoints, files, or catalog records.
- `scripts/probe_gtfs_feed.py`: probe metadata, schema, variables, or resource headers before download.
- `scripts/resolve_transit_equity_bundle.py`: return verified city presets for GTFS schedule feeds plus Census TIGER/ACS companion resources for accessibility or equity analysis; supports `nyc` and `chicago`.
- `scripts/validate_gtfs_feed.py`: validate returned files, fields, schema, or source suitability.

## References

- `references/source_card.json`: publisher, access status, authoritative URLs, and source-specific validation notes.
- `references/tool_capabilities.json`: available tool actions, access constraints, and download/probe behavior.
- `references/validation_rules.md`: source-specific documentation and validation guidance.
- `references/retrieval_profile.md`: retrieval cues and boundary cases retained from the source package.
- `references/legacy_source_skill.md`: archived pre-migration notes; prefer this SKILL.md for current workflow.

## Official Entrypoints

- GTFS static reference: https://gtfs.org/schedule/reference/
- Transit agency developer or open data feed page: agency-specific

## Access And Download Rules

- Current access status from the source card: `open_public_use_with_restricted_follow_up_available`.
- Authorization required: `false`.
- Probe first when a script supports probe/check mode; do not perform full download as a side effect of search.
- Full download is allowed only after confirming the user intent, source terms, file size, and destination path.
- GTFS Schedule is a public file-format standard; actual feed access depends on each transit agency's published feed URL and terms.
- MTA and King County Metro legacy known_source entries remain compatibility hints only.
- For New York subway schedule tasks, `scripts/resolve_transit_equity_bundle.py --city nyc` returns the MTA GTFS static zip and companion TIGER/ACS tract resources. Use the direct GTFS URL before searching generic transit catalogs.
- For Chicago CTA tasks, the official GTFS URL is known, but direct automated probing may return Cloudflare 403 from this environment; report that boundary honestly and use the official CTA entrypoint rather than mirrors.
- A feed URL or agency page is not sufficient until GTFS zip contents are validated.

## Validation Focus

- Check feed freshness and service date coverage.
- Confirm required GTFS tables and IDs exist.
- Flag unofficial mirrors unless the agency or trusted catalog is clear.

## Output Contract

- Return GTFS feed URL, publisher, agency, service date coverage, required tables, and validation status.
- For accessibility/equity tasks, return the GTFS zip together with the tract boundary ZIP and ACS API template needed for downstream joins.
- Report whether the feed is candidate, probed, sampled, downloaded, or parsed.
- Call out missing calendar, shapes, or stop_times when relevant.

## Supported Actions

- `find`
- `access_check`
- `probe`
- `fetch_sample`
- `download_link`
- `download`
- `validate`
