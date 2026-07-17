# Retrieval Profile

## One-line capability
Identifies public GTFS static feed leads for transit schedule, route, stop, and trip research by agency name or known feed URL.

## Best for
- Finding official GTFS static feeds for a transit agency's schedules, routes, stops, and service calendars
- Validating that a candidate GTFS zip URL contains the required stops.txt, routes.txt, and trips.txt members
- Obtaining feed leads for headway, trip, and service-calendar analysis for a known transit operator

## Provides
- Candidate GTFS feed resource hints (agency, feed name, or supplied URL) marked not-final
- Not-final route dossier and resource intent fragments with ambiguity around agency identity and feed freshness
- Verification notes requiring downstream GTFS zip content validation (stops.txt/routes.txt/trips.txt)

## Coverage and constraints
- Geography: Global — any transit agency publishing a GTFS static feed
- Spatial level: point (stop-level) and route-level
- Time: Scheduled service calendars and timetables; feed versions reflect publisher update cadence
- Access: open
- Task stage: discover, access_check, probe, fetch_sample

## Not suitable for
- Real-time vehicle positions unless the request explicitly asks for GTFS-Realtime — this skill targets static feeds
- Ride-hailing or taxi trip records — use nyc_tlc or commercial mobility providers
- Transit performance dashboards without feed identity — need a specific agency or feed first
- Bikeshare station or vehicle feeds — use gbfs_bikeshare instead
- Generic city open-data portal searches without a transit-feed context — use socrata_platform or ckan_platform

## Typical user expressions
- 我想查某个城市公交机构的GTFS静态数据，包括线路、站点和时刻表
- "Find the GTFS feed for Chicago Transit Authority bus routes and schedules"
- "I need a static GTFS zip for a transit agency to analyze stop coverage and service frequency"

## Nearby alternatives
- transitland: Pick when the need is to discover transit feeds via API search by query or bounding box rather than a known agency/feed URL
- mobility_database: Pick when the need is catalog-level discovery of GTFS and GBFS datasets by country or feed type
- gbfs_bikeshare: Pick when the need is about bikeshare availability rather than transit schedules

## Retrieval notes
- Positive distinctions: GTFS static feed identification with agency/feed-name matching; zip content verification requirements (stops.txt/routes.txt/trips.txt); Evidence: SKILL.md When To Use lists schedule, routes, stops, trips, headways, service calendars signals; manifest source_family = public_transit_schedule_feeds
- Negative distinctions: Not for real-time vehicle positions without explicit GTFS-RT request; not for taxi/ride-hailing (→ nyc_tlc); not for bikeshare (→ gbfs_bikeshare); not for feed discovery by bbox/query without known agency (→ transitland, mobility_database)
