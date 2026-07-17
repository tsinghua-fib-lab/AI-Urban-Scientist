# Retrieval Profile

## One-line capability
NOAA/NCEI weather, climate, precipitation, and temperature station observations — GHCN, CDO, and climate normals / NOAA美国国家气候数据中心气象站观测数据。

## Best for
- Retrieving daily precipitation and temperature records from NOAA/NCEI weather stations
- Looking up GHCN station metadata and time coverage for climate and weather analysis
- Building station-level weather observation time series for climate normals, trends, and historical studies

## Provides
- NOAA weather and climate station observation records (precipitation, temperature, and related variables)
- Station identity, variable list, and time-range metadata
- Source-landing, probe, and sample hints for NOAA/NCEI and CDO search/API entrypoints

## Coverage and constraints
- Geography: Global (GHCN network), with strong U.S. coverage via NCEI/CDO
- Spatial level: Point (station-level)
- Time: Daily observations; long historical record; user supplies station, start_date, end_date, and variables
- Access: open
- Task stage: discover, access_check, probe, fetch_sample

## Not suitable for
- Air-quality pollutant data (use open_aq or epa_air_quality)
- Gridded reanalysis products (use era5_cds for ERA5/ERA5-Land)
- Hydrology-only stream gauges, satellite imagery, or local weather dashboards
- Forecast products rather than historical observations

## Typical user expressions
- "查NOAA某站过去30年逐日降水和温度数据"
- "Get GHCN daily temperature records for station USW00014739, 1990–2020"
- "NCEI CDO气象站温度和降水观测，按变量和日期范围"

## Nearby alternatives
- era5_cds: Pick for gridded reanalysis weather fields rather than station observations
- epa_air_quality / open_aq: Pick for air-quality pollutant measurements, not meteorological variables
- usgs_hydro: Pick for streamflow and hydrology gauges, not weather stations

## Retrieval notes
- Positive distinctions: Station-level daily weather observations with long historical coverage (Evidence: manifest spatial_granularity "point", temporal_granularity "daily"; SKILL.md — "weather observations, climate normals, daily precipitation, daily temperature, NOAA station data, GHCN, NCEI, CDO"); probe and fetch_sample scripts available.
- Negative distinctions: Not a reanalysis grid source (use era5_cds); not air-quality (use open_aq / epa_air_quality); not hydrology (use usgs_hydro for stream gauges).
