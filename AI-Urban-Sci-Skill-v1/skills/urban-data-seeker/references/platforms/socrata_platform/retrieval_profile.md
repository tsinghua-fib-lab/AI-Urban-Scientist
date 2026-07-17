# Retrieval Profile

## One-line capability
Emits not-final platform hints for Socrata domain, view id, catalog, metadata, and rows-export mechanics.

## Best for
- Resolving Socrata dataset URLs into domain and view-id components
- Emitting catalog and metadata hints for a known Socrata dataset
- Deriving rows-export and search endpoint hints once a Socrata view id is known

## Provides
- Platform metadata for Socrata domain and view-id parsing
- Mechanism hints for catalog, metadata, and rows-export endpoints
- Neutral resource hints without research-fit judgment

## Coverage and constraints
- Geography: N/A (any Socrata domain worldwide)
- Spatial level: N/A
- Time: N/A (mechanics only, no data cadence)
- Access: open
- Task stage: resolve_platform_mechanics

## Not suitable for
- Deciding whether a Socrata dataset satisfies a research need (source skills do that)
- CKAN, Dataverse, ArcGIS, or other platform mechanics (use ckan_platform, dataverse_platform, arcgis_platform)
- Fetching or validating actual dataset rows (this package emits hints only)

## Typical user expressions
- 我需要解析一个Socrata数据集的domain和view id
- Parse this Socrata dataset URL into platform hints
- 帮我了解Socrata平台的catalog和rows导出机制

## Nearby alternatives
- ckan_platform: Pick when the portal is CKAN-based, not Socrata
- arcgis_platform: Pick when the service is an ArcGIS FeatureServer/MapServer
- chicago_open_data: Pick when the need is Chicago-specific city data rather than generic Socrata mechanics

## Retrieval notes
- Positive distinctions: Handles Socrata-specific URL parsing (domain, view id, catalog, metadata, rows export). Evidence: README.md names Socrata domain/view id/catalog/metadata/rows export mechanics; manifest supported_domains confirms scope.
- Negative distinctions: Exclude ckan_platform for CKAN portals; exclude arcgis_platform for FeatureServer/MapServer; exclude source skills that delegate platform mechanics here after deciding a Socrata dataset is relevant.
