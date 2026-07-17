# Retrieval Profile

## One-line capability
Emits not-final platform hints for CKAN package search and package metadata mechanics.

## Best for
- Resolving CKAN portal URLs into package-search and package-show hints
- Emitting package metadata hints once a CKAN portal and dataset slug are known
- Delegating CKAN-specific endpoint mechanics from a source skill that has already judged fit

## Provides
- Platform metadata for CKAN package search and package show endpoints
- Mechanism hints for dataset resource listings within a CKAN catalog
- Neutral resource hints without research-fit judgment

## Coverage and constraints
- Geography: N/A (any CKAN portal worldwide)
- Spatial level: N/A
- Time: N/A (mechanics only, no data cadence)
- Access: open
- Task stage: resolve_platform_mechanics

## Not suitable for
- Deciding whether a CKAN dataset satisfies a research need (source skills do that)
- Socrata, Dataverse, ArcGIS, or other platform mechanics (use socrata_platform, dataverse_platform, arcgis_platform)
- Fetching or validating actual resource files (this package emits hints only)

## Typical user expressions
- 我需要解析一个CKAN门户的package search接口
- Parse this CKAN dataset URL into package-search hints
- 帮我了解CKAN平台的package metadata机制

## Nearby alternatives
- socrata_platform: Pick when the portal is Socrata-based, not CKAN
- dataverse_platform: Pick when the portal is Dataverse-hosted
- data_gov_catalog: Pick when the need is U.S. federal data discovery (which uses CKAN mechanics underneath)
- hdx_catalog: Pick when the need is humanitarian data (which uses CKAN mechanics underneath)

## Retrieval notes
- Positive distinctions: Handles CKAN-specific package search and package show mechanics. Evidence: README.md names CKAN package search and package metadata mechanics; manifest supported_domains confirms scope.
- Negative distinctions: Exclude socrata_platform for Socrata portals; exclude dataverse_platform for Dataverse; exclude arcgis_platform for ArcGIS services.
