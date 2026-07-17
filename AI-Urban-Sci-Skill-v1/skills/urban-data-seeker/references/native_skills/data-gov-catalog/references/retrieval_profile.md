# Retrieval Profile

## One-line capability
Not-final hints for U.S. federal open-data catalog leads from data.gov; resource files still need source-specific validation.

## Best for
- Finding U.S. federal open-data catalog leads across agencies and topics
- Resolving data.gov dataset landing pages and API endpoints
- Probing federal dataset availability and sampling records for downstream acquisition

## Provides
- Candidate-resource hints for U.S. federal open-data catalog entries
- Metadata evidence including publisher agency, endpoint, license, and access constraints
- Probe and sample evidence for dataset schema, pagination, and field identity

## Coverage and constraints
- Geography: United States (federal agencies)
- Spatial level: N/A (varies by dataset; may include national, subnational, or point)
- Time: Varies by dataset; user-supplied time_range
- Access: open
- Task stage: discover, access_check, probe, fetch_sample

## Not suitable for
- Non-U.S. government catalogs (use hdx_catalog for global humanitarian data)
- U.S. city or state open-data portals (use chicago_open_data or other city-specific skills)
- Generic CKAN platform mechanics without a U.S. federal topic (delegate to ckan_platform)
- Research datasets in academic repositories (use zenodo_repository, figshare_repository, or dryad_repository)

## Typical user expressions
- 我需要查找美国联邦政府公开数据集
- Find U.S. federal open data leads for my research topic
- 帮我从data.gov获取候选资源和元数据证据

## Nearby alternatives
- hdx_catalog: Pick when the need is global humanitarian data rather than U.S. federal data
- chicago_open_data: Pick when the need is Chicago city data rather than federal data
- ckan_platform: Pick when only CKAN platform mechanics are needed after a concrete dataset is identified

## Retrieval notes
- Positive distinctions: U.S. federal open-data catalog with cross-domain coverage; platform mechanics delegated to ckan_platform. Evidence: SKILL.md names U.S. federal open-data catalog leads; manifest supported_domains: government data/catalog; platform_dependencies: ckan_platform.
- Negative distinctions: Exclude hdx_catalog for humanitarian data; exclude chicago_open_data for city-level data; exclude ckan_platform when catalog discovery (not platform mechanics) is the primary need; exclude research repository skills for academic datasets.
