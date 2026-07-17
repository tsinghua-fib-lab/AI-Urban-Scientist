# Retrieval Profile

## One-line capability
WHO Global Health Observatory health indicators covering disease burden, health systems, nutrition, and risk factors across 194 member states via OData API.

## Best for
- Retrieving official WHO health indicators such as disease incidence, mortality, vaccination coverage, and health workforce metrics by country
- Comparing global health outcomes (maternal mortality, HIV prevalence, TB rates) across WHO member states over time
- Accessing standardized health-system performance indicators and risk-factor data from the WHO official statistics program

## Provides
- Candidate WHO GHO OData API resource hints for health indicator queries by geography and time range
- Metadata evidence for indicator definitions, measurement methods, and reporting completeness
- Probe and sample evidence confirming OData endpoint availability and response structure

## Coverage and constraints
- Geography: Global — 194 WHO member states; national-level with some sub-national and regional aggregates
- Spatial level: national/global
- Time: annual and multi-year; varies by indicator and country reporting; many series from 1990s–present
- Access: open
- Task stage: discover, access_check, probe, fetch_sample

## Not suitable for
- U.S. local health indicators or modeled small-area estimates — use cdc_places
- Individual patient records, hospital data, or vital statistics microdata — use source-specific health systems
- Environmental health or air-quality exposure data — use epa_air_quality or open_aq
- Non-health global indicators (economy, education, poverty) — use world_bank_indicators or un_sdg_indicators
- Global health data from non-WHO publishers — use our_world_in_data for curated multi-source health charts

## Typical user expressions
- 查WHO全球卫生观察站关于某国的传染病发病率和疫苗接种率数据
- I need WHO GHO data on maternal mortality ratio and antenatal care coverage for Southeast Asian countries
- 世界卫生组织数据库中有哪些关于非传染性疾病和危险因素的可比指标？

## Nearby alternatives
- cdc_places: when the need is U.S. local modeled health indicators, not WHO global data
- open_aq: when the need is ambient air-quality measurements, not WHO health outcome indicators
- our_world_in_data: when the user wants OWID's curated health charts with upstream-source lineage
- un_sdg_indicators: when the need is official SDG health indicators (SDG 3) from UN rather than WHO GHO directly

## Retrieval notes
- Positive distinctions: Only skill for WHO GHO OData API — the official WHO health statistics repository with standardized indicator definitions across 194 countries. Evidence: SKILL.md identifies health/global indicators domain; manifest confirms spatial_granularity national_or_global, platform_dependencies odata_platform.
- Negative distinctions: Not U.S. local health (cdc_places), not air quality (open_aq), not curated multi-source (our_world_in_data), not SDG-specific framing (un_sdg_indicators).
