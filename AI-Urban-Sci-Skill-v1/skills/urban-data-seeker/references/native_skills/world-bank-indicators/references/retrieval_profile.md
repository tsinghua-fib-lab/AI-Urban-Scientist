# Retrieval Profile

## One-line capability
Country-level development indicators from the World Bank Indicators API covering economy, health, education, infrastructure, and governance across 200+ economies.

## Best for
- Retrieving standardized cross-country development indicators (GDP per capita, life expectancy, school enrollment) for macro-level comparisons
- Building time-series panels of World Bank indicator codes across multiple countries and years
- Accessing official World Bank DataBank metrics for research on global development, poverty, or economic growth

## Provides
- Candidate World Bank REST API resource hints with country code, indicator code, and time range
- Metadata evidence for indicator definitions, units, aggregation methods, and date coverage
- Probe and sample evidence confirming indicator availability and response structure

## Coverage and constraints
- Geography: Global — 200+ economies and country groups; national-level only
- Spatial level: national/global
- Time: annual indicators; most series cover 1960–present with varying start dates per indicator
- Access: open
- Task stage: discover, access_check, probe, fetch_sample

## Not suitable for
- City-level or sub-national microdata — use census_acs, oecd_data (metro), or city-specific skills
- World Bank project documents or procurement data — not indicator API
- Poverty headcount or inequality-specific metrics — use world_bank_pip for harmonized household survey poverty/inequality
- SDMX-only provider workflows where another publisher is the native source — use ilostat, imf_data, or oecd_data

## Typical user expressions
- 我想查世界银行关于各国GDP和预期寿命的数据，按年份
- I need World Bank indicator SP.POP.TOTL for Brazil, India, and China from 2000 to 2023
- 哪个数据源能比较不同国家的高等教育入学率？

## Nearby alternatives
- world_bank_pip: when the need is poverty headcount or inequality measures from harmonized household surveys
- oecd_data: when the need is OECD-member-specific indicators with richer sub-national/metro breakdowns
- our_world_in_data: when the user wants curated chart-ready historical data with upstream-source citations
- imf_data: when the need is macroeconomic/financial indicators (balance of payments, fiscal) from IMF

## Retrieval notes
- Positive distinctions: Direct access to 18,000+ World Bank indicator codes via official REST API with country/time/indicator resolution. Evidence: SKILL.md specifies required_params country, indicator; manifest confirms produces candidate_resource, metadata_evidence, probe_evidence, sample_evidence.
- Negative distinctions: Not household-survey poverty/inequality (world_bank_pip), not city-level (census_acs), not curated chart data (our_world_in_data), not IMF financial data (imf_data).
