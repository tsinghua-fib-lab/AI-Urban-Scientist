# Urban Climate & Heat

Methods and patterns related to urban heat exposure, heat-mortality relationships, and climate adaptation/mitigation in cities.

---

## Heat Exposure Decrease through Adaptation and Mitigation

- **Paper**: Quantifying the decrease in heat exposure through adaptation and mitigation (Nature Cities, 2023)
- **DOI**: 10.1038/s44284-023-00001-9
- **Domain**: urban_climate
- **Study design**: regional_climate_modeling
- **Outcome type**: continuous (temperature, heat index)
- **Inferential target**: counterfactual_simulation

### Method specification
- **Method name**: WRF (Weather Research and Forecasting) regional climate modeling with urban adaptation/mitigation scenarios
- **Hyperparameters**: 1.5 km spatial resolution grid over CONUS, urban parameterization scheme parameters, adaptation scenario definitions (albedo modification, green infrastructure), mitigation scenario definitions
- **Required validations**: Model validation against observational temperature data, sensitivity analysis across urban parameterizations, spatial resolution adequacy assessment
- **Characteristic outputs**: Temperature and heat index spatial distributions, population-weighted heat exposure changes under adaptation vs mitigation scenarios, spatial maps of exposure reduction

### Planning pattern
- **Evidence count**: 6 distinct analytical results
- **Figure count**: 6 main, Extended Data present, Supplementary present
- **Evidence chain**: baseline urban heat mapping -> adaptation scenario simulation -> mitigation scenario simulation -> population exposure quantification -> spatial attribution -> policy implication
- **Key figures**:
  - F1: establish (multiple panels) - Baseline urban heat patterns across CONUS
  - F2: quantify (multiple panels) - Heat exposure decrease under adaptation strategies
  - F3: reveal (multiple panels) - Heat exposure decrease under mitigation strategies
  - F4: compare (multiple panels) - Adaptation vs mitigation effectiveness comparison
  - F5: extend (multiple panels) - Population-weighted exposure reduction by region
  - F6: synthesize (multiple panels) - Spatial distribution of exposure changes and implications
- **Narrative arc**: phenomenon quantification -> adaptation modeling -> mitigation modeling -> comparative evaluation -> population impact -> policy implication
- **Central claim**: Urban heat adaptation and mitigation strategies can substantially reduce population heat exposure, with effectiveness varying by strategy type and geographic region.
- **Claim strength**: causal (modeling-based counterfactual)

### Keywords
heat exposure, urban climate, WRF modeling, regional climate model, adaptation, mitigation, albedo, green infrastructure, heat index, population exposure, CONUS, urban parameterization

---

## Heat-mortality Temporal Variation

- **Paper**: High temperatures-related elderly mortality varied greatly from year to year (Scientific Reports, 2012)
- **DOI**: 10.1038/srep00830
- **Domain**: urban_climate
- **Study design**: time_series (multi-city)
- **Outcome type**: count (mortality)
- **Inferential target**: association

### Method specification
- **Method name**: Distributed Lag Non-linear Model (DLNM) + Bayesian hierarchical model
- **Hyperparameters**: Lag structure parameters (lag days for temperature effect), spline degrees of freedom for temperature-response relationship, Bayesian prior specifications, hierarchical model variance components
- **Required validations**: Model convergence diagnostics, lag structure sensitivity, between-city heterogeneity assessment, temporal stability check
- **Characteristic outputs**: City-specific temperature-mortality exposure-response curves, lag-effect distributions, year-to-year variability estimates, pooled multi-city relative risk estimates

### Planning pattern
- **Evidence count**: 3 distinct analytical results
- **Figure count**: 3 main, 0 Extended Data, Supplementary present
- **Evidence chain**: temperature-mortality association estimation -> year-to-year variability quantification -> elderly vulnerability characterization
- **Key figures**:
  - F1: establish (multiple panels) - Temperature-mortality exposure-response relationships across 83 US cities
  - F2: reveal (multiple panels) - Year-to-year variability in heat-mortality associations over 14 years
  - F3: extend (multiple panels) - Age-specific patterns (elderly vulnerability)
- **Narrative arc**: multi-city association estimation -> temporal variability discovery -> vulnerable population identification
- **Central claim**: The association between high temperatures and elderly mortality varies substantially from year to year across US cities, highlighting the need to account for temporal instability in heat-health impact assessments.
- **Claim strength**: suggestive (observational time-series with multi-city pooling)

### Keywords
heat mortality, DLNM, distributed lag non-linear model, Bayesian hierarchical model, elderly mortality, temporal variability, multi-city study, temperature-mortality, US cities, time-series epidemiology
