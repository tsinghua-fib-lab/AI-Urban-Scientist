# Climate Risk Assessment

Entries for papers projecting future climate-related exposure, vulnerability, and risk using climate model ensembles, scenario analysis, and spatiotemporal trend estimation.

---

## heatwave_exposure_ageing_projection

- **Paper**: Rising vulnerability of compound risk inequality to ageing and extreme heatwave exposure in global cities (npj Urban Sustainability, 2023)
- **DOI**: 10.1038/s42949-023-00118-9
- **Domain**: climate_risk_assessment
- **Study design**: time_series
- **Outcome type**: rate
- **Inferential target**: association

### Method specification
- **Method name**: Multi-model ensemble (MME) climate projection + heatwave exposure risk quantification + decomposition analysis
- **Hyperparameters**:
  - CMIP6: 27 high-resolution GCMs; SSP2-4.5 (moderate mitigation) and SSP5-8.5 (fossil fuel development) scenarios; historical period 1950-2014, projection 2020-2100; 0.25-degree grid, daily Tmax
  - Heatwave definition: consecutive >= 3 days with daily Tmax above 95th percentile (reference 1950-2014, 5-day moving window, summer season); heatwave duration (HWD) and heatwave average intensity (HWI)
  - Population projections: 0.125-degree resolution, 10-year intervals 2010-2100 (SSP database, IIASA); ageing rate from national-level SSP data
  - Exposure risk = HWD x HWI x Population; elderly = population >= 65 years
  - Trend analysis: Mann-Kendall (MK) test + Sen's slope estimator; OLS linear regression per city (2020s-2090s); significance threshold p < 0.05
  - Resampling: nearest neighbor interpolation to 0.0125 degrees
- **Required validations**: MK significance test (p < 0.05) for all urban settlements with positive trends; MME mean composite projections; sensitivity across two SSP scenarios
- **Characteristic outputs**: Spatiotemporal trend maps of HWD/HWI; exposure risk projections by city; elderly-specific exposure risk; income-group and city-size stratified analysis; factor decomposition (climate effects vs. ageing effects contribution percentages)

### Planning pattern
- **Evidence count**: 5 distinct analytical results
- **Figure count**: 7 main, 0 Extended Data, Supplementary figures present
- **Evidence chain**: scenario setup (CMIP6 + SSP) -> heatwave characterization -> exposure risk quantification -> elderly vulnerability -> inequality decomposition -> policy implication
- **Key figures**:
  - F1: establish (multi-panel) — Spatiotemporal variation in exposure risk trend projections under SSP2-4.5 and SSP5-8.5
  - F2: quantify (multi-panel) — Elderly exposure risk projections
  - F3: compare (multi-panel) — Continental evolution of exposure risk
  - F4: reveal (multi-panel) — Relationship between initial scale and growth trend
  - F5: expose_response (multi-panel) — Uneven distribution across income groups
  - F6: compare (multi-panel) — Proportional patterns by income group and city size
  - F7: mechanism (multi-panel) — Decomposition of driving factors (climate vs. ageing effects)
- **Narrative arc**: Climate scenario setup -> Heatwave characteristic trends -> Urban exposure risk quantification -> Elderly compound risk -> Geographic and income inequality -> Factor decomposition -> Adaptation implications
- **Central claim**: Urban heatwave exposure risk increases by 619-1740% globally by 2090, with elderly risk rising 1642-5529%, and 69% of elderly exposure concentrated in middle-income countries, revealing a disproportionately higher heat-related burden that demands targeted adaptation strategies.
- **Claim strength**: suggestive

### Keywords
CMIP6, SSP scenarios, heatwave exposure, ageing, global cities, climate risk, vulnerability, inequality, multi-model ensemble, Sen's slope, Mann-Kendall, factor decomposition, elderly population
