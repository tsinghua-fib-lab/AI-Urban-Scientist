# Retrieval Profile

## One-line capability
U.S. Census ACS demographic, socioeconomic, and housing tables by tract, block group, county, and other geographies, with annual updates.

## Best for
- Retrieving neighborhood-level (tract/block group) demographic, income, education, and housing composition data for U.S. areas
- Building demographic profiles of counties, places, or metro areas using ACS 1-year or 5-year estimates
- Tracking year-over-year changes in population, race/ethnicity, commute patterns, or poverty at sub-county geographies

## Provides
- Candidate ACS table and API resource hints with variable IDs, geography predicates, and vintage metadata
- Probe and sample evidence confirming table availability, variable definitions, and geography coverage
- Not-final route dossier fragments requiring downstream resolver/probe/download/verifier validation

## Coverage and constraints
- Geography: United States and territories only
- Spatial level: tract, block group, county, place, state, metro — subnational
- Time: annual release cadence; 1-year (pop ≥65k), 5-year (all geographies); vintage-specific
- Access: open
- Task stage: discover, access_check, probe, fetch_sample

## Not suitable for
- Decennial-only redistricting data (PL 94-171) — use census-specific redistricting sources
- TIGER boundary geometry without attribute tables — use us_tiger_boundaries
- LEHD/LODES origin-destination employment flow files — use lehd_lodes
- Non-U.S. demographic data — use un_wpp, world_bank_indicators, or our_world_in_data
- Local administrative records or vital statistics — use cdc_places or cdc_svi

## Typical user expressions
- 帮我查一下某个区县的ACS人口和收入数据，按tract级别
- I need ACS 5-year estimates for median household income by census tract in Cook County
- 想了解某个社区的种族构成和教育水平变化趋势用哪个数据源

## Nearby alternatives
- lehd_lodes: when the need is origin-destination employment flows, not static ACS demographic tables
- cdc_places: when the need is modeled local health indicators, not Census demographics
- census_acs is the correct pick for U.S. sub-national demographic tables; us_tiger_boundaries provides geometry only

## Retrieval notes
- Positive distinctions: Only source for ACS tract/block-group demographic tables with variable-level API access. Evidence: SKILL.md specifies required_params year, survey, geography, variables; manifest lists produces candidate_resource, metadata_evidence, probe_evidence, sample_evidence.
- Negative distinctions: Not a boundary-only tool (us_tiger_boundaries), not employment flows (lehd_lodes), not health indicators (cdc_places), not non-U.S. data (world_bank_indicators, un_wpp).
