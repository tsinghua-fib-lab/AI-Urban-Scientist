# Retrieval Profile

## One-line capability
STAC-cataloged Earth observation collections and cloud-hosted raster assets on Microsoft Planetary Computer, spanning Landsat, Sentinel, MODIS-derived, terrain, weather, and environmental monitoring datasets.

## Best for
- Discovering pre-registered STAC collections for satellite imagery, terrain models, or environmental rasters with cloud-optimized access
- Locating Earth observation data that is already hosted on Azure cloud storage with STAC metadata for programmatic querying
- Finding not-final collection, item, and asset leads for remote sensing and cloud geospatial analysis workflows

## Provides
- Candidate resource hints for Planetary Computer STAC collection, item, and asset endpoints
- Metadata evidence on publisher, dataset identity, access terms, and STAC platform dependencies
- Probe evidence for API availability and sample asset fetches to confirm collection accessibility before full download

## Coverage and constraints
- Geography: Global (collection-dependent)
- Spatial level: Varies by collection (satellite swath, gridded raster, global mosaic)
- Time: Varies by collection (daily satellite overpasses to decadal composites)
- Access: open
- Task stage: discover, access_check, probe, fetch_sample

## Not suitable for
- Needs for Copernicus-specific API paths (OData, openEO, Sentinel Hub) — use copernicus_dataspace instead
- Needs for NASA Earth observation collections searched via CMR — use nasa_earthdata_cmr instead
- Needs for derived products like land cover, building footprints, or urban extent — use nlcd_land_cover, microsoft_building_footprints, or ghsl_urban_extent instead

## Typical user expressions
- 我需要在Planetary Computer上查找Landsat 8 Collection 2的STAC数据
- Search Planetary Computer STAC for Sentinel-2 L2A items over the Mekong Delta, 2024
- 想用Planetary Computer的cloud-optimized遥感数据做东南亚的森林覆盖变化分析

## Nearby alternatives
- copernicus_dataspace: Choose when the need is specifically for Copernicus Sentinel data via the Copernicus Data Space ecosystem (OData, openEO, Sentinel Hub paths)
- nasa_earthdata_cmr: Choose when the need is specifically for NASA Earth observation products via the CMR search API
- nlcd_land_cover: Choose when the need is specifically for U.S. land cover classification rather than raw satellite imagery discovery

## Retrieval notes
- Positive distinctions: Cloud-hosted STAC catalog with pre-registered collections; probe and fetch_sample capabilities; Evidence: SKILL.md specifies stac_platform as platform dependency; probe and fetch_sample scripts available
- Negative distinctions: Collection-dependent coverage — not all Earth observation data is hosted here; easily confused with copernicus_dataspace (different API ecosystem) and nasa_earthdata_cmr (NASA-specific catalog); requires STAC-aware tooling for efficient use
