# Retrieval Profile

## One-line capability
Identifies NYC Taxi & Limousine Commission trip record file leads by vehicle type, year, and month for taxi-zone and ride-level mobility research.

## Best for
- Studying ride-hailing and taxi trip volumes, fares, and pickup/dropoff patterns within New York City
- Building origin-destination flow analyses specific to NYC taxi zones over monthly periods
- Obtaining TLC trip-level microdata for yellow taxi, green taxi, and for-hire vehicles

## Provides
- Monthly trip-record file candidates keyed by vehicle type (yellow, green, FHV), year, and month
- Candidate resource leads with role, access method, and required validation metadata
- Project-neutral route dossier fragments with positive and negative evidence

## Coverage and constraints
- Geography: New York City five boroughs and NYC taxi zones
- Spatial level: city, point
- Time: Monthly files; temporal_granularity = monthly
- Access: open
- Task stage: discover, access_check, probe, fetch_sample

## Not suitable for
- Public transit schedules, GTFS feeds, or subway/bus route data — use gtfs_feed or transitland instead
- Bikeshare station availability or GBFS feeds — use gbfs_bikeshare instead
- Commute flows, employment origin-destination, or census-derived mobility — use lehd_lodes instead
- Any geography outside New York City unless TLC is explicitly requested as a comparison source

## Typical user expressions
- 我想查纽约出租车的载客记录，按月份和车型获取trip record文件
- "NYC yellow taxi pickup dropoff trip data 2023"
- "I need TLC for-hire vehicle trip records for a ride-hailing demand study in Manhattan"

## Nearby alternatives
- gtfs_feed: Pick when the need is about transit schedules/routes/stops rather than taxi trip records
- lehd_lodes: Pick when the need is about commute or employment origin-destination flows rather than individual ride records
- socrata_platform: Pick when the need is about general NYC open data hosted on Socrata rather than TLC-specific trip records

## Retrieval notes
- Positive distinctions: NYC-specific taxi trip records at monthly granularity; vehicle-type filtering (yellow/green/FHV); Evidence: SKILL.md When To Use lists taxi, yellow taxi, green taxi, FHV, pickup/dropoff, fare, trip record signals; manifest spatial_granularity = city/point, temporal_granularity = monthly
- Negative distinctions: Not for GTFS/transit schedules (→ gtfs_feed); not for bikeshare (→ gbfs_bikeshare); not for employment OD flows (→ lehd_lodes); not for generic NYC open data without taxi context (→ socrata_platform)
