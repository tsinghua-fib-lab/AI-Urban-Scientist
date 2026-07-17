# Retrieval Profile

## One-line capability
Emits not-final platform hints for STAC catalog, collection, and item-search mechanics.

## Best for
- Resolving STAC API roots into catalog, collection, and item-search parameters
- Emitting collection and search hints for known STAC endpoints
- Deriving bbox, datetime, and query-parameter hints for STAC item searches

## Provides
- Platform metadata for STAC catalog and collection parsing
- Mechanism hints for item-search endpoints (bbox, datetime, query parameters)
- Neutral resource hints without research-fit judgment

## Coverage and constraints
- Geography: N/A (any STAC catalog worldwide)
- Spatial level: N/A
- Time: N/A (mechanics only, no data cadence)
- Access: open
- Task stage: resolve_platform_mechanics

## Not suitable for
- Deciding whether a STAC collection or item satisfies a research need (source skills do that)
- Socrata, CKAN, ArcGIS, OData, or other platform mechanics (use the relevant platform tool)
- Fetching or validating actual imagery or raster assets (this package emits hints only)

## Typical user expressions
- 我需要解析一个STAC catalog的collection和item-search参数
- Parse this STAC API URL into collection and item-search hints
- 帮我了解STAC平台的collection查询和bbox机制

## Nearby alternatives
- arcgis_platform: Pick when the service is an ArcGIS FeatureServer/MapServer
- odata_platform: Pick when the service uses OData entity-set mechanics
- copernicus_dataspace: Pick when the need is Copernicus Sentinel remote-sensing data (which may use STAC underneath)

## Retrieval notes
- Positive distinctions: Handles STAC-specific catalog/collection/item-search mechanics including bbox and datetime parameters. Evidence: README.md names STAC catalog/collection/item-search mechanics; manifest supported_domains confirms scope.
- Negative distinctions: Exclude arcgis_platform for ArcGIS services; exclude odata_platform for OData services; exclude copernicus_dataspace for Copernicus-specific remote-sensing needs.
