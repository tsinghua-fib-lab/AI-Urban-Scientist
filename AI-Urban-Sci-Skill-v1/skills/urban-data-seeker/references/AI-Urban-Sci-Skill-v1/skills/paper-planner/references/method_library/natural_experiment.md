# Natural Experiment / Quasi-Experimental Design

Methods that use naturally occurring variation or policy rollouts as quasi-experimental settings to estimate causal effects. Includes difference-in-differences (DID), PSM-DID, DDD, relocation quasi-experiments, and smartphone-accelerometry natural experiments.

---

## Smartphone-accelerometry natural experiment (walkability and physical activity)

- **Paper**: Countrywide natural experiment links built environment to physical activity (Nature, 2025)
- **DOI**: 10.1038/s41586-025-09321-3
- **Domain**: Built environment, public health
- **Study design**: Longitudinal quasi-experiment using residential relocation as natural experiment
- **Outcome type**: Daily step count, MVPA (moderate-to-vigorous physical activity)
- **Inferential target**: Causal effect of walkability changes on physical activity

### Method specification
- **Method name**: Smartphone-accelerometry natural experiment with relocation quasi-experiment
- **Hyperparameters**: Relocation defined as move >100 km, stay >=14 days in each location; 30-day observation windows (±5 days excluded around relocation); Walk Score cut points: -16 to +16 (similar), 16-48 (moderate), 49-80 (large change)
- **Required validations**: Bootstrapped 95% confidence intervals; selection effect tests (no activity change when moving to similar walkability; point-symmetric effect); seasonality adjustment; subgroup analysis across age, gender, BMI; simulation study with post-stratification weights
- **Characteristic outputs**: Change in daily steps per Walk Score point (slope = 16.6); change in weekly MVPA minutes; fraction of population meeting aerobic activity guidelines; demographic subgroup effects

### Planning pattern
- **Evidence count**: 3 distinct analytical results in Results
- **Figure count**: 3 main, 7 Extended Data, multiple Supplementary
- **Evidence chain**: natural experiment setup -> within-person before/after comparison -> symmetric walkability effect -> evidence against residential self-selection -> demographic heterogeneity -> MVPA composition -> population simulation
- **Key figures**:
  - F1: Relocation quasi-experiment illustration (6 panels) — before/after step counts for NYC movers, showing symmetric increase/decrease
  - F2: Aggregated walkability effect and demographic subgroups (2 panels) — linear model across all relocations; step gain per Walk Score point by age/gender/BMI
  - F3: MVPA intensity analysis and population simulation (6 panels) — intensity distribution changes, MVPA minutes vs walkability, guideline compliance simulation
- **Narrative arc**: problem (mixed findings from small/cross-sectional studies) -> natural experiment design (7,447 relocations, 1,609 cities) -> causal effect (walkability increases -> step increases) -> selection bias ruled out -> effects hold across demographics -> MVPA health benefits -> population-level simulation
- **Central claim**: Increases (decreases) in walkability are associated with significant increases (decreases) in physical activity after relocation, predominantly composed of moderate-to-vigorous physical activity.
- **Claim strength**: Quasi-causal

### Keywords
walkability, built environment, physical activity, natural experiment, relocation, smartphone accelerometry, MVPA, Walk Score, quasi-experimental design, public health, urban planning

---

## Difference-in-Differences (EDCS and eco-environmental level)

- **Paper**: Assessing the impact of the eco-environmental damage compensation system (Scientific Reports, 2025)
- **DOI**: 10.1038/s41598-025-12241-x
- **Domain**: Environmental policy, ecological governance
- **Study design**: Panel DID with PSM-DID, DDD, and Double Machine Learning robustness
- **Outcome type**: Eco-environmental level (EEL) composite index, PM2.5 concentration
- **Inferential target**: Causal effect of eco-environmental damage compensation system (EDCS) pilot policy on ecological quality

### Method specification
- **Method name**: Difference-in-Differences (DID)
- **Hyperparameters**: 284 prefecture-level cities, 2009-2017; 7 pilot provinces (treatment=63 cities); EEL index via entropy method (4 indicators across 2 dimensions: ecological resources, environmental quality); controls: GDP, secondary industry proportion, industrial electricity, urban park green space
- **Required validations**: Parallel trend test (event study); placebo test (1000 random assignments of 63 treatment cities); PSM-DID (propensity score matching + DID); DDD (triple difference using resource/provincial-capital/key city groupings); robustness with PM2.5 substitution; robustness with adjusted policy timing; additional control variables (merchandise exports, fiscal expenditures); Double Machine Learning (DML) with 1:2 sample split
- **Characteristic outputs**: DID coefficient on Treat*Post; parallel trend event-study plot; placebo kernel density; heterogeneity by resource vs non-resource cities; mechanism analysis (industrial structure upgrading, technological innovation) with marginal effect plots

### Planning pattern
- **Evidence count**: 5 main analytical sections (benchmark, robustness, heterogeneity, mechanism, conclusion)
- **Figure count**: 5 main figures, multiple tables
- **Evidence chain**: policy background and theoretical model -> DID benchmark regression -> parallel trend validation -> robustness suite (PM2.5, placebo, PSM-DID, DDD, timing) -> heterogeneity (resource vs non-resource) -> mechanism (industrial structure, innovation)
- **Key figures**:
  - F1: Theoretical mechanism diagram — EDCS impact pathway
  - F2: Parallel trend test — event study showing pre-policy equivalence and post-policy divergence
  - F3: Placebo test — kernel density of 1000 random coefficient estimates
  - F4: Marginal effect plots for industrial structure thresholds
  - F5: Marginal effect plot for technological innovation threshold
- **Narrative arc**: policy problem -> theoretical model (utility maximization with EDCS) -> DID identification -> robustness battery -> heterogeneity discovery (resource cities benefit more) -> mechanism channels (industrial upgrading, innovation) -> policy recommendations
- **Central claim**: The EDCS significantly improves the eco-environmental level in pilot provinces, with effects mediated by industrial structure upgrading and technological innovation, and concentrated in resource-based cities.
- **Claim strength**: Quasi-causal

### Keywords
difference-in-differences, DID, PSM-DID, DDD, double machine learning, environmental policy, eco-environmental damage compensation, entropy method, placebo test, parallel trend, resource-based cities, industrial structure, technological innovation

---

## Difference-in-Differences (green finance and air quality)

- **Paper**: Has the establishment of green finance reform and innovation pilot zones improved air quality? Evidence from China (Humanities and Social Sciences Communications, 2023)
- **DOI**: 10.1057/s41599-023-01773-0
- **Domain**: Green finance, environmental economics
- **Study design**: Quasi-natural experiment using DID with PSM-DID robustness
- **Outcome type**: Air Quality Index (AQI), PM2.5, PM10, SO2, CO, NO2, O3 concentrations
- **Inferential target**: Causal effect of Green Finance Reform and Innovation Pilot Zones (GFRIs) on urban air quality

### Method specification
- **Method name**: Difference-in-Differences (DID) with mediating effect models
- **Hyperparameters**: 146 prefecture-level cities, 2015-2019 (monthly panel); 8 pilot zones in 5 provinces (treatment cities: Quzhou, Huzhou, Guangzhou, Karamay, Changji, Hami, Gui'an/Guiyang+Anshun, Ganjiang/Nanchang+Jiujiang); AQI as primary outcome; controls: temperature, lngdp, lngdp^2, green coverage rate, population growth rate, FDI
- **Required validations**: Parallel trend test (60-month event plot); PSM-DID (one-to-one nearest-neighbor + kernel density matching); placebo test (advance policy timing by 4 months and 1 year); explained variable substitution (PM2.5, PM10, SO2, CO, NO2, O3); Bootstrap mediation test for industrial structure upgrading
- **Characteristic outputs**: DID coefficient on Treat*Post; parallel trend plot; PSM balance table and kernel density plots; placebo coefficients; mediating effect proportions; heterogeneity by region (Qinling-Huaihe line), city size, AQI level, financial development scale, fiscal expenditure

### Planning pattern
- **Evidence count**: 3 main results (DID benchmark, robustness, mechanism/heterogeneity)
- **Figure count**: 3 main figures, multiple tables
- **Evidence chain**: DID benchmark -> parallel trend validation -> PSM-DID robustness -> placebo test -> variable substitution -> mechanism (Bootstrap mediation: industrial structure upgrading, green total factor productivity) -> heterogeneity (regional, city scale, financial development)
- **Key figures**:
  - F1: Parallel trend — 60-month AQI trajectories for treatment vs control
  - F2: Kernel density plots before and after PSM matching
  - F3: Qinling-Huaihe line regional division map
- **Narrative arc**: green finance policy context -> DID identification -> robustness suite (parallel trend, PSM-DID, placebo, substitution) -> mechanism channels (industrial upgrading, green innovation via SBM-GML) -> heterogeneous effects (south vs north, large vs small cities, financial development)
- **Central claim**: The establishment of GFRIs significantly reduces AQI and improves air quality through industrial structure upgrading and green innovation, with stronger effects in southern, larger, and financially developed cities.
- **Claim strength**: Quasi-causal

### Keywords
difference-in-differences, DID, PSM-DID, green finance, air quality, AQI, quasi-natural experiment, mediating effect, Bootstrap, industrial structure upgrading, green total factor productivity, SBM-GML, heterogeneity analysis
