# Retrieval Profile

## One-line capability
Discovers General Bikeshare Feed Specification (GBFS) feeds for real-time station availability, vehicle status, and bikeshare system metadata worldwide.

## Best for
- Finding live bikeshare station information, station status, and free-bike availability for a specific city or system
- Identifying GBFS discovery endpoints and feed structure for a known bikeshare operator
- Assessing whether a GBFS system provides real-time versus historical data suitable for analysis

## Provides
- GBFS discovery URL hints and system catalog leads by system name and region
- Candidate resource hints marked not-final requiring resolver, probe, download, and verifier steps
- Ambiguity notes distinguishing real-time feed suitability from historical trip-data needs

## Coverage and constraints
- Geography: Global — any GBFS-compatible bikeshare system
- Spatial level: point (station-level)
- Time: Real-time / near-real-time station and vehicle status; not designed for long-term trip histories unless publisher provides separate archives
- Access: open
- Task stage: discover, access_check, probe, fetch_sample

## Not suitable for
- Long-term historical bikeshare trip records unless the publisher explicitly exposes historical GBFS archives — most GBFS feeds are real-time only
- Public transit schedules, routes, or stops — use gtfs_feed or transitland instead
- Taxi or ride-hailing trip data — use nyc_tlc or a commercial mobility provider
- Generic open-data portal searches without a bikeshare context — use socrata_platform or ckan_platform

## Typical user expressions
- 我想查某个城市的共享单车站点实时状态和可用车辆数据
- "Find GBFS feed for Bay Wheels bike-share station availability in San Francisco"
- "I need real-time bikeshare station status and free-bike data for a Citi Bike analysis"

## Nearby alternatives
- gtfs_feed: Pick when the need is about transit schedules/routes/stops rather than bikeshare availability
- mobility_database: Pick when the need is to discover both GTFS and GBFS systems via a unified catalog rather than a specific known system
- transitland: Pick when the need is about transit feed/operator/route discovery rather than bikeshare

## Retrieval notes
- Positive distinctions: GBFS-specific feed discovery with system name and region matching; real-time vs. historical ambiguity flagging; Evidence: SKILL.md When To Use lists bikeshare availability, station status, vehicle status, system metadata, feed-discovery signals; manifest source_family = mobility_realtime_feeds
- Negative distinctions: Not for transit schedules (→ gtfs_feed, transitland); not for catalog-level GTFS/GBFS discovery (→ mobility_database); not for historical trip histories without publisher proof of archives
