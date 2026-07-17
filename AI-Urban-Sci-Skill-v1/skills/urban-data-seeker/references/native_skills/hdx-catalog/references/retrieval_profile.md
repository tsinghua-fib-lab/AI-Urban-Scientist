# Retrieval Profile

## One-line capability
Not-final hints for HDX humanitarian catalog and HAPI leads for crisis, population, boundary, and response data worldwide.

## Best for
- Finding humanitarian datasets for crisis-affected countries (conflict, disaster, epidemic)
- Locating population statistics, administrative boundaries, and response indicators from HDX
- Discovering HAPI (Humanitarian API) data leads for food security, displacement, and aid operations

## Provides
- Candidate-resource hints for HDX catalog datasets and HAPI endpoints
- Metadata evidence including publisher, organization, license, geography, and topic tags
- Probe and sample evidence for CKAN dataset structure, resource formats, and HAPI query parameters

## Coverage and constraints
- Geography: Global (covers all countries and territories in the HDX catalog)
- Spatial level: N/A (varies by dataset; can include national, subnational, or point)
- Time: Varies by dataset; many are updated frequently during active crises — user-supplied time_range
- Access: open
- Task stage: discover, access_check, probe, fetch_sample

## Not suitable for
- U.S. federal open data (use data_gov_catalog for domestic U.S. government datasets)
- Academic research datasets in Zenodo, Figshare, Dryad, or OSF (use the matching repository skill)
- Global development indicators unrelated to crisis/humanitarian topics (use gapminder or world_bank_indicators)
- Generic CKAN platform mechanics without a humanitarian topic (delegate to ckan_platform)

## Typical user expressions
- 我需要查找人道主义数据交换平台的危机或人口数据
- Find HDX catalog datasets for population displacement in a crisis-affected country
- 帮我查找HAPI中关于人道主义援助指标的候选资源

## Nearby alternatives
- data_gov_catalog: Pick when the need is U.S. federal open data rather than global humanitarian data
- gapminder: Pick when the need is global development indicators rather than crisis/humanitarian data
- ckan_platform: Pick when only CKAN platform mechanics are needed after a concrete dataset is identified

## Retrieval notes
- Positive distinctions: HDX-specific humanitarian catalog and HAPI integration for crisis/population/boundary/response data across all affected countries; platform mechanics delegated to ckan_platform. Evidence: SKILL.md names HDX humanitarian catalog and HAPI leads; manifest source_family: hdx_ckan_hapi_catalog; supported_domains: humanitarian/risk/population; platform_dependencies: ckan_platform.
- Negative distinctions: Exclude data_gov_catalog when the need is humanitarian/global rather than U.S. federal; exclude gapminder for development indicators; exclude research repository skills when the need is for operational humanitarian data rather than academic datasets.
