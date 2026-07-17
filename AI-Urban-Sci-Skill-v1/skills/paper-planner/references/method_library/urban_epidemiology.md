# Urban Epidemiology

Methods and patterns for studying environmental health risks, disease transmission, and pollution-mortality associations in urban settings.

---

## Malaria Importation and Transmission Modeling

- **Paper**: Travel risk, malaria importation and malaria transmission in Zanzibar (Scientific Reports, 2011)
- **DOI**: 10.1038/srep00093
- **Domain**: urban_epidemiology
- **Study design**: spatial_modeling (mobile phone data + mathematical modeling)
- **Outcome type**: count (malaria cases, importation events)
- **Inferential target**: association

### Method specification
- **Method name**: Mobile phone data-based travel pattern analysis + modified Ross-Macdonald malaria transmission model
- **Hyperparameters**: Mobile phone call detail record (CDR) aggregation parameters, travel volume estimation parameters, Ross-Macdonald model parameters (vector biting rate, mosquito mortality, parasite development rate), spatial transmission kernel parameters
- **Required validations**: Mobile phone data representativeness assessment, cross-validation between mobile-phone-derived travel volumes and malaria importation estimates, transmission model parameter sensitivity analysis
- **Characteristic outputs**: Travel volume maps from mobile phone data, malaria importation risk estimates by region, reproduction number (R0) spatial distribution, cross-validation metrics between travel-based and transmission-based models

### Planning pattern
- **Evidence count**: 5 distinct analytical results
- **Figure count**: 5 main, 0 Extended Data, Supplementary present
- **Evidence chain**: travel pattern quantification -> importation risk estimation -> transmission modeling -> cross-validation -> spatial risk mapping
- **Key figures**:
  - F1: establish (multiple panels) - Travel patterns and volumes from mobile phone data
  - F2: quantify (multiple panels) - Malaria importation risk by travel route
  - F3: reveal (multiple panels) - Modified Ross-Macdonald transmission model outputs
  - F4: validate (multiple panels) - Cross-validation between mobile phone and transmission models
  - F5: synthesize (multiple panels) - Spatial risk mapping and policy implications
- **Narrative arc**: data source description -> travel pattern analysis -> importation estimation -> mechanistic transmission modeling -> convergent validation -> risk mapping
- **Central claim**: Mobile phone data can quantify human travel patterns and malaria importation risk, providing complementary estimates to traditional transmission modeling approaches for guiding targeted malaria control interventions.
- **Claim strength**: suggestive (observational travel data + mechanistic model cross-validation)

### Keywords
malaria importation, mobile phone data, Ross-Macdonald model, travel risk, Zanzibar, disease transmission, spatial epidemiology, call detail records, importation modeling, malaria control

---

## NO2 Cardiovascular Mortality Spatial Heterogeneity

- **Paper**: Acute Effects of Nitrogen Dioxide on Cardiovascular Mortality in Beijing (Scientific Reports, 2016)
- **DOI**: 10.1038/srep38328
- **Domain**: urban_epidemiology
- **Study design**: multilevel_time_stratified_case_crossover
- **Outcome type**: binary (mortality event)
- **Inferential target**: causal_effect

### Method specification
- **Method name**: Multilevel time-stratified case-crossover design + mixed Cox model + robust regression
- **Hyperparameters**: Time-stratification window parameters, lag structure for NO2 exposure (same-day and lag days), spatial resolution for exposure assignment (monitor-level to community-level), mixed effects random effect structure, robust regression tuning parameters
- **Required validations**: Spatial heterogeneity assessment, model fit diagnostics, sensitivity to exposure lag specification, robustness to unmeasured confounding assessment, cross-validation of spatial risk patterns
- **Characteristic outputs**: Community-level NO2-mortality risk estimates, spatial heterogeneity maps, effect modification by socioeconomic and environmental factors, lag-response curves

### Planning pattern
- **Evidence count**: 6 distinct analytical results
- **Figure count**: 6 main, 0 Extended Data, Supplementary present
- **Evidence chain**: overall NO2-mortality association -> spatial heterogeneity identification -> effect modification analysis -> vulnerable population characterization -> spatial risk mapping -> policy implication
- **Key figures**:
  - F1: establish (multiple panels) - Overall NO2-cardiovascular mortality association in Beijing
  - F2: quantify (multiple panels) - Spatial distribution of NO2 monitoring and exposure
  - F3: reveal (multiple panels) - Spatial heterogeneity in NO2-mortality effects across communities
  - F4: compare (multiple panels) - Effect modification by socioeconomic and environmental factors
  - F5: extend (multiple panels) - Lag-response relationships and sensitivity analyses
  - F6: synthesize (multiple panels) - Spatial risk maps and policy-targeted recommendations
- **Narrative arc**: population-level association -> spatial disaggregation -> heterogeneity discovery -> modifier identification -> spatial mapping -> targeted intervention
- **Central claim**: The acute effects of NO2 on cardiovascular mortality exhibit significant spatial heterogeneity across Beijing communities, with effect modification by local socioeconomic and environmental characteristics.
- **Claim strength**: quasi_causal (case-crossover design with multilevel spatial modeling)

### Keywords
NO2 mortality, nitrogen dioxide, cardiovascular mortality, case-crossover, mixed Cox model, spatial heterogeneity, Beijing, air pollution, robust regression, multilevel model, environmental epidemiology

---

## Heat-related Road Traffic Deaths in Latin America

- **Paper**: Individual and city-level variations in heat-related road traffic deaths in Latin America (Nature Cities, 2025)
- **DOI**: 10.1038/s44284-025-00279-x
- **Domain**: urban_epidemiology
- **Study design**: time_stratified_case_crossover (multi-city)
- **Outcome type**: count (road traffic mortality)
- **Inferential target**: causal_effect

### Method specification
- **Method name**: Time-stratified case-crossover design with multi-city conditional logistic regression and city-level effect modification analysis
- **Hyperparameters**: Temperature percentile thresholds (95th, 99th), time-stratification window, lag structure for temperature exposure, city-level covariate parameters (commute duration, street segment length, climate zone clustering), individual-level covariate parameters (age groups, sex, road user type)
- **Required validations**: Case-crossover design assumptions check, temperature cluster analysis validation, effect modification robustness, cross-city heterogeneity assessment
- **Characteristic outputs**: Temperature-mortality exposure-response curves by city, relative risk estimates at extreme temperature percentiles, effect modification by individual characteristics (age, sex, road user type) and city characteristics (climate, commute, street structure)

### Planning pattern
- **Evidence count**: 4 distinct analytical results
- **Figure count**: 4 main, 2 Extended Data figures, 1 Supplementary figure
- **Evidence chain**: temperature-traffic mortality association -> extreme heat risk quantification -> individual-level vulnerability -> city-level effect modification
- **Key figures**:
  - F1: establish (multiple panels) - Study area, temperature and mortality characteristics across 272 Latin American cities
  - F2: quantify (multiple panels) - Temperature-road traffic mortality exposure-response relationships
  - F3: reveal (multiple panels) - Individual-level vulnerability (age, sex, road user type)
  - F4: extend (multiple panels) - City-level effect modification (climate, commute, urban form)
- **Narrative arc**: multi-city data assembly -> association estimation -> vulnerable subgroup identification -> contextual effect modification -> policy recommendation
- **Central claim**: Road traffic mortality risk increases with temperature in a monotonic pattern across 272 Latin American cities, with significantly elevated risk on extremely hot days, particularly among younger individuals, males, motorcyclists, bicyclists, and in cities with hotter climates and longer commutes.
- **Claim strength**: quasi_causal (time-stratified case-crossover design)

### Keywords
heat mortality, road traffic deaths, case-crossover, Latin America, temperature mortality, vulnerable road users, motorcyclists, cyclists, urban form, commute exposure, SALURBAL, multi-city study
