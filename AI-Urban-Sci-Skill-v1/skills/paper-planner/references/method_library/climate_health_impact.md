# Climate & Health Impact

Entries on modeling health and climate impacts of transportation emissions, air quality, and pollution using integrated modeling systems, chemical transport models, and economic valuation.

---

## Integrated Freight Emission-Health-Climate Modeling with InMAP

- **Paper**: Health and climate impacts of future United States land freight modelled with global-to-urban models (Nature Sustainability, 2019)
- **DOI**: 10.1038/s41893-019-0224-3
- **Domain**: Freight transport, air quality, health impact, climate forcing
- **Study design**: Scenario-based projection modeling (2010-2050) across baseline and 3 mitigation scenarios
- **Outcome type**: PM2.5-related mortalities, short-lived and long-lived radiative forcing (TW-yr), pollutant emissions
- **Inferential target**: Emission, health, and climate impacts of US freight truck and rail transport under policy scenarios

### Method specification
- **Method name**: Integrated system of systems: asymptotic vehicle routing model + SPEW-Trend fleet emission model + InMAP reduced-form air quality model + health impact function + radiative forcing analysis
- **Hyperparameters**: InMAP: variable resolution grid (1-48 km); health impact: RR=1.06 per 10 µg/m³ PM2.5; carbon tax and technology slip scenarios; urban spatial form scenarios (trend, polycentric, compact)
- **Required validations**: Cross-model comparison with COBRA, APEEP/AP2, EASIUR reduced-form models; EMFAC2014 baseline validation for truck mileages
- **Characteristic outputs**: Projected emissions by pollutant and freight category; spatial PM2.5 distribution maps; mortality estimates per scenario; marginal health impact per ktonne of emissions reduced; short- and long-lived radiative forcing trajectories

### Planning pattern
- **Evidence count**: 6 distinct analytical results
- **Figure count**: 5 main, 0 ED, unspecified Supplementary
- **Evidence chain**: system-of-systems model design → freight activity & emission projections → spatial PM2.5 distribution → mortality estimation → marginal impact by species & category → scenario comparison (triple-impact: mortality, short-lived forcing, long-lived forcing)
- **Key figures**:
  - F1: System of systems schematic — integrated model flow from freight activity to emissions to impacts
  - F2: Short-haul freight activity, fuel, emissions 2010-2050 across urban form scenarios
  - F3: Spatial PM2.5 distribution maps (2010 vs 2050 baseline)
  - F4: Total PM2.5-related mortalities by scenario
  - F5: Triple-impact trajectories (mortality, short-lived forcing, long-lived forcing) across scenarios
- **Narrative arc**: Integrated modeling system → emission trajectories show early decline then rise → urban form reduces freight distances → policy scenarios (carbon tax, technology slip, urban form) compared → health benefits quantified at species level → climate tradeoffs assessed
- **Central claim**: Air pollutant emissions and health impacts from US freight will decline through 2030 due to emission standards, but long-term climate forcing increases unless additional policies (carbon tax, electrification) are implemented
- **Claim strength**: Descriptive (scenario-based projection modeling)

### Keywords
freight transport, emission modeling, InMAP, health impact assessment, climate forcing, PM2.5 mortality, radiative forcing, vehicle routing, fleet model, carbon tax, urban spatial form, technology slip, scenario analysis, reduced-form air quality model

---

## Neighborhood-Scale Air Quality & Equity Analysis of HDV Electrification

- **Paper**: Air quality, health and equity implications of electrifying heavy-duty vehicles (Nature Sustainability, 2023)
- **DOI**: 10.1038/s41893-023-01219-0
- **Domain**: Air quality, environmental justice, vehicle electrification
- **Study design**: Chemical transport model simulation (WRF-CMAQ) comparing baseline vs. 30% eHDV adoption scenario across 4 meteorological seasons
- **Outcome type**: NO2, MDA8O3, PM2.5 concentration changes; attributable premature deaths; racial/ethnic distribution of health benefits
- **Inferential target**: Air quality, health, and equity implications of heavy-duty vehicle electrification at neighborhood scale

### Method specification
- **Method name**: WRF-CMAQ coupled CTM at 1.3 km resolution + MOVES emission factors + SMOKE processing + census tract health impact estimation + equity decile analysis
- **Hyperparameters**: 30% eHDV adoption; CMAQ v5.2, WRF v3.8; 4-season simulation (Aug/Oct 2018, Jan/Apr 2019); RR for NO2=1.04 per 10 µg/m³, O3=1.02 per 10 ppb, PM2.5=1.03 per 5 µg/m³; EGU emission remapping via vehicle-to-EGU algorithm
- **Required validations**: WRF-CMAQ performance metrics per season (Supplementary Table 1); sensitivity to EGU emission-free scenario
- **Characteristic outputs**: Emission change maps; NO2/O3/PM2.5 concentration difference maps; MDA8O3 exceedance days; census tract mortality estimates; racial/ethnic composition by concentration and mortality change deciles

### Planning pattern
- **Evidence count**: 5 distinct analytical results
- **Figure count**: 5 main, 0 ED, unspecified Supplementary
- **Evidence chain**: emission changes (on-road vs. EGU) → NO2 and O3 concentration changes → O3 regime explanation (VOC/NOx ratio) → PM2.5 changes → health benefits & tradeoffs → equity analysis by race/ethnicity
- **Key figures**:
  - F1: Emission changes — on-road and EGU NOx; EGU generation increase by fuel type
  - F2: NO2 and MDA8O3 baseline concentrations and differences
  - F3: MDA8O3 exceedance days above WHO 50 ppb threshold by county
  - F4: PM2.5 baseline and difference maps
  - F5: Equity implications — racial/ethnic fraction by NO2 concentration and mortality change deciles (domain and Chicago)
- **Narrative arc**: 30% eHDV reduces on-road emissions but increases EGU emissions → NO2 decreases substantially but O3 increases in VOC-limited urban areas → PM2.5 decreases → net health benefit despite O3 penalty → largest NO2 reductions benefit Black, Asian, Hispanic communities → equity analysis reveals distributional patterns
- **Central claim**: 30% HDV electrification reduces NO2 and PM2.5 with substantial health benefits that disproportionately benefit communities of color, but creates O3 increases in VOC-limited urban environments
- **Claim strength**: Suggestive (scenario-based CTM simulation with 4-month averaging)

### Keywords
heavy-duty vehicle electrification, WRF-CMAQ, air quality, environmental justice, equity analysis, NO2, ozone, PM2.5, neighborhood scale, health impact, census tract, MOVES, SMOKE, VOC-limited regime, racial disparity

---

## Age-Stratified PM2.5 Health Cost & Healthcare Mismatch Assessment

- **Paper**: Rising socio-economic costs of PM2.5 pollution and medical service mismatching (Nature Sustainability, 2025)
- **DOI**: 10.1038/s41893-025-01509-9
- **Domain**: Air pollution, public health, aging, healthcare resource allocation
- **Study design**: Spatial-temporal observational analysis across 47 Japanese prefectures, 2001-2019
- **Outcome type**: PM2.5-attributable deaths by age segment; age-adjusted value of statistical life (AVSL); relative economic cost (EC/GDP); disease burden by medical department
- **Inferential target**: Socio-economic costs of PM2.5 exposure stratified by age and region, and spatial mismatch with healthcare resources

### Method specification
- **Method name**: Global Exposure Mortality Model (GEMM) + Age-adjusted Value of Statistical Life (AVSL) + Age-adjusted VSLY (AVSLY) + Disease burden mapping
- **Hyperparameters**: GEMM: 17 age segments (5-year intervals), 5 diseases (COPD, IHD, LRI, LC, stroke), counterfactual PM2.5 = 2.4 µg/m³; AVSLY: VSL baseline = US$3.54M, income elasticity = 0.8, discount rate = 4%; disease burden: 170,000 medical-clinic records mapped to 5 diseases × relevant departments
- **Required validations**: None explicitly reported; relies on established GEMM and VSL methodologies
- **Characteristic outputs**: Age-stratified premature death maps and time series; AVSL distribution by age and prefecture; relative economic cost maps (EC/GDP); disease burden maps by medical department; metropolitan vs. non-metropolitan gap analysis

### Planning pattern
- **Evidence count**: 3 distinct analytical results
- **Figure count**: 3 main, 0 ED, unspecified Supplementary
- **Evidence chain**: age-stratified PM2.5 mortality → economic cost by age and region (AVSL) → healthcare resource mismatch mapping
- **Key figures**:
  - F1: Age-stratified AVSL and PM2.5 premature deaths by prefecture (5 age groups) — maps + time series
  - F2: Monetized health impacts — EC/GDP map with contribution decomposition by prefecture and age segment
  - F3: Disease burden map — spatial mismatch between PM2.5-related disease burden and healthcare resource availability by department
- **Narrative arc**: PM2.5 deaths increase despite concentration decline due to aging → economic burden highest in Baby Boomer generation (40-59) and oldest elderly (80+) → West Japan bears disproportionate relative cost → healthcare resources concentrated in metros while disease burden highest in non-metropolitan West Japan
- **Central claim**: PM2.5-related socio-economic costs in Japan are rising due to demographic aging, with disproportionate burden on West Japan's less-developed regions that also face healthcare resource mismatch
- **Claim strength**: Descriptive (observational economic and health cost estimation)

### Keywords
PM2.5, aging population, GEMM, AVSL, VSLY, healthcare mismatch, disease burden, Japan, economic cost, Baby Boomer, spatial inequality, medical resource allocation, elderly health, West Japan

---

## Housing Exchange Framework for Commuting Emission Reduction

- **Paper**: Housing exchange framework to reduce carbon emissions from commuting (Nature Sustainability, 2025)
- **DOI**: 10.1038/s41893-025-01658-x
- **Domain**: Urban transport, housing, commuting, carbon emissions
- **Study design**: Cross-city comparative analysis using household survey data from Beijing (n=2,032), Munich (n=3,131), Singapore (n=7,418)
- **Outcome type**: Commuting distance reduction, CO2/CO/NOx/PM2.5 emission reduction, utility gains
- **Inferential target**: Potential emission reduction from information-enabled housing exchange that optimizes commuting distance

### Method specification
- **Method name**: Utility-based housing exchange matching algorithm + Discrete Choice Model (DCM) for mode switching + Minimum-weight matching optimization
- **Hyperparameters**: Utility = WTP for amenities + generalized commuting cost + expected capital gains; budget = 2 years after-tax income minus essential living; amenity tolerance α = 0.9 (10% max deterioration); time span = 5 years; solved via Google OR-tools
- **Required validations**: Sensitivity tests on WTP, value of time, amenity tolerance, capital gain assumptions, time span (3, 5, 8 years), revealed preference constraints (±30% on community income, CBD distance, POI count); random vs. targeted participant selection
- **Characteristic outputs**: Commuting pattern flow maps (current vs. optimal); distance distribution comparisons; emission reduction percentages; sensitivity analysis tornado plots; network effect curves; targeted selection efficiency curves

### Planning pattern
- **Evidence count**: 4 distinct analytical results
- **Figure count**: 6 main, 0 ED, unspecified Supplementary
- **Evidence chain**: current commuting patterns → housing exchange optimization → scenario comparison (near-optimal vs. optimal) → sensitivity analysis → targeted vs. random selection efficiency
- **Key figures**:
  - F1: Housing exchange conceptual illustration — current vs. utility-maximizing exchange
  - F2: Commuting patterns and distance distributions (current vs. optimal) for 3 cities
  - F3: Average commuting distance and emissions under 3 scenarios (current, near-optimal, optimal)
  - F4: Sensitivity analysis — % change in distance and emissions across parameters
  - F5: Random vs. targeted selection — total and average emission reduction curves
  - F6: Commuting reduction and utility gains under constraints (relocation cost, targeted % thresholds)
- **Narrative arc**: Spatial mismatch documented → housing exchange framework formulated with utility + constraints → optimization reduces commuting 10-13% across cities → near-optimal (no capital gains) performs similarly → top 5% targeted relocations capture >50% of potential → network effect with more participants
- **Central claim**: An information-enabled housing exchange framework can reduce commuting-related CO2 emissions by 11-13% across diverse cities, with the top 5% of targeted relocations capturing over half the total reduction potential
- **Claim strength**: Suggestive (counterfactual optimization based on survey data, not implemented policy)

### Keywords
housing exchange, commuting emissions, utility maximization, matching algorithm, discrete choice model, carbon reduction, Beijing, Munich, Singapore, optimization, OR-tools, network effect, targeted relocation, willingness to pay, generalized commuting cost
