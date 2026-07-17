# Retrieval Profile

## One-line capability
Catalog-level discovery of NASA Earth observation collections and granules via the CMR (Common Metadata Repository) search API — spanning MODIS, Landsat, GPM, ICESat, and hundreds of other NASA/Earth-observing satellite missions.

## Best for
- Locating NASA Earth observation datasets (MODIS vegetation indices, GPM precipitation, ICESat elevation, Landsat surface reflectance) for a specific geography and time range
- Identifying collection-level metadata and granule-search leads for NASA Earth science products relevant to remote sensing or climate research
- Finding not-final CMR API leads when the research question points to NASA as a plausible Earth observation data publisher

## Provides
- Candidate resource hints for NASA Earthdata CMR collection and granule search endpoints
- Metadata evidence on publisher, dataset identity, access terms, provenance, and collection identifiers
- Source-landing hints when query parameters are incomplete; no probe or sample fetch available

## Coverage and constraints
- Geography: Global (mission-dependent)
- Spatial level: Varies by mission/product (swath, gridded global, regional)
- Time: Decades-long archive for core missions (MODIS since 1999, Landsat since 1972 via NASA)
- Access: open
- Task stage: discover, access_check

## Not suitable for
- Needs for Copernicus Sentinel data via the Copernicus Data Space ecosystem — use copernicus_dataspace instead
- Needs for STAC-cataloged Earth observation data on Planetary Computer — use planetary_computer instead
- Needs for derived products like land cover classification, urban extent, or building footprints — use nlcd_land_cover, ghsl_urban_extent, or building-footprint skills instead

## Typical user expressions
- 我需要在NASA Earthdata CMR搜索MODIS NDVI时间序列数据
- Search NASA CMR for GPMIMERGHH precipitation granules over East Africa, June 2024
- 想用NASA的遥感数据集做全球气温和植被变化趋势分析

## Nearby alternatives
- copernicus_dataspace: Choose when the need is specifically for Copernicus Sentinel data via STAC, OData, or openEO paths rather than NASA missions
- planetary_computer: Choose when the need is for STAC-cataloged data already hosted on cloud infrastructure with cloud-optimized assets
- nlcd_land_cover: Choose when the need is specifically for U.S. land cover classification products rather than raw satellite collection discovery

## Retrieval notes
- Positive distinctions: Broadest NASA Earth observation catalog; decades of satellite mission data; Evidence: SKILL.md specifies CMR collection/granule search leads for Earth observation products
- Negative distinctions: Discovery-only — no probe or sample fetch; CMR search API requires understanding of collection short names, concept IDs, and granule filters; easily confused with planetary_computer (different catalog/host) and copernicus_dataspace (different mission family); NASA Earthdata Login may be required for granule download
