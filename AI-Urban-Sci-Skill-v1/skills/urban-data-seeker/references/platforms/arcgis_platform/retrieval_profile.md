# Retrieval Profile

## One-line capability
Emits not-final platform hints for ArcGIS REST FeatureServer/MapServer service, layer, and portal mechanics.

## Best for
- Resolving ArcGIS REST URLs into service, layer, and portal components
- Emitting query and metadata hints for known ArcGIS FeatureServer or MapServer endpoints
- Deriving layer-id and service-name hints once an ArcGIS service is identified

## Provides
- Platform metadata for ArcGIS REST service parsing (FeatureServer, MapServer)
- Mechanism hints for layer ids, service names, and query endpoints
- Neutral resource hints without research-fit judgment

## Coverage and constraints
- Geography: N/A (any ArcGIS portal worldwide)
- Spatial level: N/A
- Time: N/A (mechanics only, no data cadence)
- Access: open
- Task stage: resolve_platform_mechanics

## Not suitable for
- Deciding whether an ArcGIS layer satisfies a research need (source skills do that)
- Socrata, CKAN, Dataverse, STAC, or other platform mechanics (use the relevant platform tool)
- Fetching or validating actual feature geometries or rows (this package emits hints only)

## Typical user expressions
- 我需要解析一个ArcGIS FeatureServer的URL
- Parse this ArcGIS MapServer URL into layer and service hints
- 帮我了解ArcGIS REST服务的layer查询机制

## Nearby alternatives
- socrata_platform: Pick when the portal is Socrata-based, not ArcGIS
- ckan_platform: Pick when the portal is CKAN-based
- stac_platform: Pick when the service uses STAC catalog/item mechanics
- fema_flood: Pick when the need is FEMA NFHL flood data (which uses ArcGIS mechanics underneath)

## Retrieval notes
- Positive distinctions: Handles ArcGIS REST FeatureServer/MapServer URL parsing, layer ids, and service names. Evidence: README.md names ArcGIS service/item/layer/portal mechanics; manifest supported_domains confirms scope.
- Negative distinctions: Exclude socrata_platform for Socrata portals; exclude ckan_platform for CKAN portals; exclude stac_platform for STAC catalogs.
