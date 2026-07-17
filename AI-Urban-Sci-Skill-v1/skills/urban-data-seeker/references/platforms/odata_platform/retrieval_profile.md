# Retrieval Profile

## One-line capability
Not-final platform hints for OData service document, metadata document, and entity-query mechanics.

## Best for
- Resolving OData service roots into metadata document and entity-set components
- Emitting entity-query hints for known OData endpoints
- Deriving capped query templates once an OData service root and entity set are identified

## Provides
- Platform metadata for OData service document and metadata document parsing
- Mechanism hints for entity sets and query templates
- Neutral resource hints without research-fit judgment

## Coverage and constraints
- Geography: N/A (any OData service worldwide)
- Spatial level: N/A
- Time: N/A (mechanics only, no data cadence)
- Access: open
- Task stage: resolve_platform_mechanics

## Not suitable for
- Deciding whether an OData entity set satisfies a research need (source skills do that)
- SDMX dataflow or structure mechanics (use sdmx_platform for that)
- Socrata, CKAN, ArcGIS, STAC, or other data-portal mechanics (use the relevant platform tool)
- Fetching or validating actual entity rows (this package emits hints only)

## Typical user expressions
- 我需要解析一个OData服务的entity set和metadata文档
- Parse this OData service root into metadata and entity-set hints
- 帮我了解OData平台的entity查询和服务文档机制

## Nearby alternatives
- sdmx_platform: Pick when the service uses SDMX dataflow mechanics rather than OData
- socrata_platform: Pick when the portal is Socrata-based rather than OData
- stac_platform: Pick when the service uses STAC catalog/item mechanics
- copernicus_dataspace: Pick when the need is Copernicus Sentinel data (which may use OData underneath)

## Retrieval notes
- Positive distinctions: Handles OData-specific service document, metadata document, and entity-query mechanics. Evidence: README.md names OData service document/metadata/entity query mechanics; manifest supported_domains confirms scope.
- Negative distinctions: Exclude sdmx_platform for SDMX services; exclude socrata_platform for Socrata portals; exclude stac_platform for STAC catalogs; exclude dataverse_platform for Dataverse dataset mechanics.
