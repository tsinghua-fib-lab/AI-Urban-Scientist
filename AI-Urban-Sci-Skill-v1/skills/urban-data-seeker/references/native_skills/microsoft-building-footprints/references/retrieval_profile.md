# Retrieval Profile

## One-line capability
Global ML-derived building footprint polygons from Microsoft, organized by country GeoJSON files, covering 200+ countries and territories.

## Best for
- Obtaining building footprint polygons for any country worldwide where official building data is unavailable
- Estimating urban density, settlement extent, or building counts at national or subnational scale from AI-detected structures
- Assembling a global building-layer dataset for humanitarian mapping, disaster response, or infrastructure gap analysis

## Provides
- Candidate resource hints for Microsoft building-footprint GeoJSON files by country
- Metadata evidence on publisher, coverage, file format, license, and geographic extent
- Probe evidence for file availability and sample footprint fetches to confirm geometry before full download

## Coverage and constraints
- Geography: 200+ countries and territories (global)
- Spatial level: National or global (building-level polygons; aggregated to any boundary)
- Time: Snapshot releases (periodic updates per country); not continuously streamed
- Access: open
- Task stage: discover, access_check, probe, fetch_sample

## Not suitable for
- Needs for Google's building footprints organized by S2 tile IDs — use google_open_buildings instead
- Needs for Overture Maps curated, multi-source building layer with schema-validated attributes — use overture_maps instead
- Needs for official government parcel or cadastral data with legal boundaries — use local cadastral or us_tiger_boundaries sources

## Typical user expressions
- 我需要Microsoft全球建筑足迹数据，获取尼日利亚所有建筑物的GeoJSON文件
- Download Microsoft building footprints for all of Central America for urban density analysis
- 想用Microsoft建筑足迹数据做非洲城市的建成区面积估算

## Nearby alternatives
- google_open_buildings: Choose when the need requires S2-tile-organized CSV with confidence scores, or when Google's ML model coverage is preferred for a specific region
- overture_maps: Choose when the need requires a curated, schema-validated multi-source building layer in GeoParquet format
- ghsl_urban_extent: Choose when the need is for raster built-up surface extent rather than vector building polygons

## Retrieval notes
- Positive distinctions: Broadest single-publisher global building footprint coverage (200+ countries); ML-detected polygons with per-building geometry; Evidence: SKILL.md specifies global ML building-footprint file-index leads; spatial_granularity=national_or_global
- Negative distinctions: Snapshots, not time series; ML-detection errors in dense or informal settlements; easily confused with google_open_buildings which uses a different ML pipeline and S2 tile organization
