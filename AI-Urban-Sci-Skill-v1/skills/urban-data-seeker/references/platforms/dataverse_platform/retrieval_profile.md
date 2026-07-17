# Retrieval Profile

## One-line capability
Emits not-final platform hints for Dataverse persistent-id, dataset, and file-listing mechanics.

## Best for
- Resolving Dataverse dataset URLs into persistent-id and file-listing hints
- Emitting dataset API hints once a Dataverse installation and dataset are identified
- Deriving file-listing mechanics for Dataverse-hosted research datasets

## Provides
- Platform metadata for Dataverse persistent-id resolution and dataset endpoints
- Mechanism hints for file listing within a Dataverse dataset
- Neutral resource hints without research-fit judgment

## Coverage and constraints
- Geography: N/A (any Dataverse installation worldwide)
- Spatial level: N/A
- Time: N/A (mechanics only, no data cadence)
- Access: open
- Task stage: resolve_platform_mechanics

## Not suitable for
- Deciding whether a Dataverse dataset satisfies a research need (source skills do that)
- Socrata, CKAN, ArcGIS, or other platform mechanics (use the relevant platform tool)
- Fetching or validating actual dataset files or checksums (this package emits hints only)

## Typical user expressions
- 我需要解析一个Dataverse数据集的persistent id
- Parse this Dataverse dataset URL into API and file-listing hints
- 帮我了解Dataverse平台的文件列表机制

## Nearby alternatives
- socrata_platform: Pick when the portal is Socrata-based, not Dataverse
- ckan_platform: Pick when the portal is CKAN-based
- zenodo_repository: Pick when the need is Zenodo record/DOI/data availability routing
- osf_repository: Pick when the need is OSF project/component/file metadata

## Retrieval notes
- Positive distinctions: Handles Dataverse-specific persistent-id, dataset API, and file-listing mechanics. Evidence: README.md names Dataverse persistent id/dataset/file-listing mechanics; manifest supported_domains confirms scope.
- Negative distinctions: Exclude socrata_platform for Socrata portals; exclude ckan_platform for CKAN portals; exclude zenodo_repository / osf_repository for non-Dataverse research repositories.
