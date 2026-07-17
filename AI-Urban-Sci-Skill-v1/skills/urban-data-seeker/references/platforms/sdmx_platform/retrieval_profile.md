# Retrieval Profile

## One-line capability
Emits not-final platform hints for SDMX dataflow, structure, and data-query mechanics.

## Best for
- Resolving SDMX REST URLs into agency, dataflow, and series-key components
- Emitting dataflow metadata and data-query hints for known SDMX endpoints
- Deriving structure and series-key hints once an SDMX agency and dataflow are identified

## Provides
- Platform metadata for SDMX REST base URL and dataflow parsing
- Mechanism hints for dataflow structure, series keys, and data queries
- Neutral resource hints without research-fit judgment

## Coverage and constraints
- Geography: N/A (any SDMX endpoint worldwide)
- Spatial level: N/A
- Time: N/A (mechanics only, no data cadence)
- Access: open
- Task stage: resolve_platform_mechanics

## Not suitable for
- Deciding whether an SDMX series satisfies a research need (source skills do that)
- Socrata, CKAN, ArcGIS, STAC, or other platform mechanics (use the relevant platform tool)
- Fetching or validating actual time-series data (this package emits hints only)

## Typical user expressions
- 我需要解析一个SDMX REST接口的dataflow和series key
- Parse this SDMX URL into agency and dataflow hints
- 帮我了解SDMX平台的dataflow结构和数据查询机制

## Nearby alternatives
- odata_platform: Pick when the service uses OData entity-set mechanics rather than SDMX
- socrata_platform: Pick when the portal is Socrata-based
- ckan_platform: Pick when the portal is CKAN-based
- data_commons: Pick when the need is cross-domain statistical variables from Data Commons

## Retrieval notes
- Positive distinctions: Handles SDMX-specific REST URL parsing (agency, dataflow, series key) and data-query mechanics. Evidence: README.md names SDMX dataflow/structure/data query mechanics; manifest supported_domains confirms scope.
- Negative distinctions: Exclude odata_platform for OData services; exclude socrata_platform for Socrata portals; exclude data_commons for Data Commons knowledge-graph queries.
