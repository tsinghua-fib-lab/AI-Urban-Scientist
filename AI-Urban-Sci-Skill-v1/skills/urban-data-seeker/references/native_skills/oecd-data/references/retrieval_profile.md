# Retrieval Profile

## One-line capability
OECD statistical indicators across economy, education, labor, regional, and metropolitan dimensions for OECD member and partner countries via SDMX APIs.

## Best for
- Retrieving standardized economic, education, and labor statistics for OECD member countries with comparable methodologies
- Accessing metropolitan-area-level indicators from the OECD Metropolitan Statistics database for cross-country metro comparisons
- Comparing regional development, trade, government spending, and social indicators across advanced economies

## Provides
- Candidate OECD Data Explorer and SDMX API resource hints for indicator, regional, and metropolitan queries
- Metadata evidence for SDMX dataflow, dimension structure, and indicator definitions
- Probe and sample evidence confirming dataflow availability and response structure

## Coverage and constraints
- Geography: OECD member countries (38 members) plus key partners; national and metropolitan/regional levels
- Spatial level: national/global (with metro and regional breakdowns for select indicators)
- Time: annual and sub-annual depending on indicator; most series cover 1960s–present
- Access: open
- Task stage: discover, access_check, probe, fetch_sample

## Not suitable for
- Non-OECD country statistics — use world_bank_indicators or un_sdg_indicators for low-income country coverage
- SDMX-only generic platform queries — use sdmx_platform for mechanics
- Sub-national U.S. demographic data — use census_acs
- Labor statistics specifically from ILO — use ilostat for global labor market indicators
- IMF financial/macro indicators — use imf_data

## Typical user expressions
- 查OECD各国教育支出和PISA成绩数据
- I need OECD metropolitan GDP and population data for comparison across major cities
- 经合组织数据库中有哪些关于劳动力市场和区域经济不平等的指标？

## Nearby alternatives
- world_bank_indicators: when the need covers non-OECD countries or broader development indicators
- ilostat: when the need is specifically labor/employment from ILO rather than OECD
- imf_data: when the need is fiscal, balance-of-payments, or monetary indicators from IMF
- un_sdg_indicators: when the need is official UN SDG indicator series, not OECD-specific

## Retrieval notes
- Positive distinctions: Only skill for OECD Data Explorer SDMX APIs with metro and regional indicator coverage for advanced economies. Evidence: SKILL.md identifies global indicators/economy domain; manifest confirms spatial_granularity national_or_global, platform_dependencies sdmx_platform.
- Negative distinctions: Not U.S. demographics (census_acs), not labor-specific (ilostat), not IMF financial (imf_data), not UN SDG (un_sdg_indicators), not non-OECD (world_bank_indicators).
