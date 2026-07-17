# Retrieval Profile

## One-line capability
Cross-provider ambient air-quality measurements — pollutant concentrations, monitoring stations, and time-window searches aggregated through the OpenAQ API / 通过OpenAQ API聚合多国多网络环境空气质量观测数据。

## Best for
- Finding ambient pollutant measurements (PM2.5, ozone, NO2, etc.) from many contributing networks worldwide through one API
- Locating monitoring stations by geography and checking time coverage for a specific pollutant
- Aggregating air-quality data across government, research, and community providers for cross-border or global studies

## Provides
- Ambient air-quality observation records (pollutant concentration, station/location, timestamp)
- Cross-provider station and location metadata with pollutant parameter coverage
- Source-landing, probe, and sample hints for OpenAQ API queries over pollutant × location × time windows

## Coverage and constraints
- Geography: Global — aggregates measurements from many national, subnational, and community providers
- Spatial level: Point (station-level)
- Time: Varies by station and provider; typically hourly or daily; user must specify start and end dates
- Access: open
- Task stage: discover, access_check, probe, fetch_sample

## Not suitable for
- EPA-only U.S. regulatory AirData workflows or EPA parameter-code-specific queries (use epa_air_quality)
- Gridded chemical transport model products, emissions inventories, or modeled exposure surfaces
- Meteorological and weather observations such as temperature, precipitation, or wind (use noaa_weather or era5_cds)
- Use cases requiring U.S.-only monitor certification and regulatory parameter codes

## Typical user expressions
- "查一下全球PM2.5的监测站数据，按污染物和时间段筛选"
- "Search OpenAQ for NO2 measurements near industrial zones in 2023"
- "需要跨越多个国家网络的空气质量传感器观测，按城市和时间窗口"

## Nearby alternatives
- epa_air_quality: Pick when the focus is U.S. EPA regulatory monitors, AQI, and EPA parameter codes
- noaa_weather: Pick for weather and meteorological variables, not pollutant concentrations
- era5_cds: Pick for gridded reanalysis weather fields rather than in-situ pollutant measurements

## Retrieval notes
- Positive distinctions: Multi-provider aggregation (Evidence: SKILL.md Purpose — "ambient air-quality measurements from the OpenAQ API, especially pollutant, station/location, and time-window searches across many providers"); explicit cross-border scope versus U.S.-only EPA skill; probe and fetch_sample scripts available in manifest.
- Negative distinctions: Not a U.S. regulatory source (use epa_air_quality for EPA AirData); not a weather or reanalysis source (use noaa_weather / era5_cds); not an emissions-inventory or CTM product.
