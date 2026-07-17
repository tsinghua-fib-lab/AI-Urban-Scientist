# Human Mobility

Methods and patterns related to human movement, navigation, and transport infrastructure design.

---

## Scaling Properties of Human Mobility

- **Paper**: Modelling the scaling properties of human mobility (Nature Physics, 2010)
- **DOI**: 10.1038/nphys1760
- **Domain**: human_mobility
- **Study design**: network
- **Outcome type**: flow
- **Inferential target**: distributional_pattern

### Method specification
- **Method name**: Individual-mobility model with exploration and preferential return
- **Hyperparameters**: rho (exploration probability scaling), gamma (exploration decay), alpha=0.55 (preferential return exponent), beta=0.8 (return probability exponent)
- **Required validations**: Scaling law consistency, distributional fit comparison against empirical data, exploration vs return balance validation
- **Characteristic outputs**: Power-law scaling of travel distances, visitation frequency distributions, scaling exponents matching real GPS/mobile phone data

### Planning pattern
- **Evidence count**: 4 distinct analytical results
- **Figure count**: 4 main, 0 Extended Data, 0 Supplementary
- **Evidence chain**: empirical phenomenon -> model formulation -> scaling predictions -> validation against real data
- **Key figures**:
  - F1: establish (multiple panels) - Empirical scaling laws in human mobility data
  - F2: reveal (multiple panels) - Model formulation with exploration and preferential return mechanisms
  - F3: validate (multiple panels) - Model predictions match empirical distributions
  - F4: extend (multiple panels) - Unified framework explaining multiple mobility scaling laws
- **Narrative arc**: empirical observation -> theoretical model -> prediction -> validation -> unification
- **Central claim**: A single individual-mobility model with exploration and preferential return mechanisms reproduces the scaling laws observed across diverse human mobility datasets.
- **Claim strength**: descriptive

### Keywords
human mobility, scaling laws, power law, preferential return, exploration model, individual mobility, movement patterns, spatial dynamics

---

## Evolution of Human Population Distance to Water

- **Paper**: The evolution of human population distance to water in the USA from 1790 to 2010 (Nature Communications, 2019)
- **DOI**: 10.1038/s41467-019-08366-z
- **Domain**: human_mobility
- **Study design**: spatial
- **Outcome type**: continuous
- **Inferential target**: association

### Method specification
- **Method name**: Spatio-temporal overlay analysis with NPD-DMR regression and Pettitt change-point detection
- **Hyperparameters**: Pettitt test parameters, power function fitting parameters
- **Required validations**: Spatial autocorrelation check, boundary sensitivity, scale sensitivity
- **Characteristic outputs**: Population distance to water (PDW) time series, turning point detection, spatial overlay of population density and distance to water sources

### Planning pattern
- **Evidence count**: 4 distinct analytical results
- **Figure count**: 4 main, 0 Extended Data, 0 Supplementary
- **Evidence chain**: historical population distribution -> distance-to-water measurement -> temporal change detection -> spatial pattern attribution
- **Key figures**:
  - F1: establish (multiple panels) - Historical population distribution and water proximity patterns
  - F2: quantify (multiple panels) - Distance-to-water changes over two centuries
  - F3: reveal (multiple panels) - Spatio-temporal overlay analysis results
  - F4: validate (multiple panels) - Change-point detection and power function fitting
- **Narrative arc**: historical baseline -> measurement framework -> temporal analysis -> spatial validation -> interpretation
- **Central claim**: US population has moved progressively closer to water bodies over 220 years, with identifiable turning points in this relationship.
- **Claim strength**: descriptive

### Keywords
population distance to water, spatio-temporal analysis, historical demography, Pettitt test, power function, spatial overlay, water proximity, population distribution

---

## Migratory Response to Hurricanes

- **Paper**: Understanding the migratory response to hurricanes and tropical storms in the USA (Nature Human Behaviour, 2025)
- **DOI**: 10.1038/s41562-025-02281-8
- **Domain**: human_mobility
- **Study design**: panel_longitudinal
- **Outcome type**: flow
- **Inferential target**: causal_effect

### Method specification
- **Method name**: County-level panel analysis with storm path data
- **Hyperparameters**: null - underspecified in paper
- **Required validations**: Confounding assessment, placebo or negative control, sensitivity to unmeasured confounding when possible
- **Characteristic outputs**: Population-weighted exposure estimates, county-level migration flows in response to storm events

### Planning pattern
- **Evidence count**: 4 distinct analytical results
- **Figure count**: 4 main, 0 Extended Data, 0 Supplementary
- **Evidence chain**: storm exposure identification -> population displacement measurement -> spatial migration patterns -> differential response by storm characteristics
- **Key figures**:
  - F1: establish (multiple panels) - Storm path and exposure mapping
  - F2: quantify (multiple panels) - Migration flow quantification by exposure level
  - F3: reveal (multiple panels) - Spatial patterns of population displacement
  - F4: extend (multiple panels) - Differential response by storm severity and county characteristics
- **Narrative arc**: exposure definition -> displacement measurement -> pattern identification -> causal attribution
- **Central claim**: Hurricanes and tropical storms trigger measurable county-to-county migration in the USA, with population displacement patterns varying by storm intensity and geographic location.
- **Claim strength**: quasi_causal

### Keywords
hurricane migration, climate migration, panel analysis, county-level analysis, storm exposure, population displacement, natural disaster migration, climate mobility

---

## Vector-based Pedestrian Navigation

- **Paper**: Vector-based pedestrian navigation in cities (Nature Computational Science, 2021)
- **DOI**: 10.1038/s43588-021-00130-y
- **Domain**: human_mobility
- **Study design**: observational (GPS trajectory analysis)
- **Outcome type**: flow
- **Inferential target**: association

### Method specification
- **Method name**: Vector-based navigation model ("pointiest paths") with stochastic distance minimization baseline
- **Hyperparameters**: Street network graph parameters (Boston and San Francisco pedestrian networks), GPS trace sampling and filtering parameters, asymmetry testing procedure parameters
- **Required validations**: Cross-city generalization (Boston vs San Francisco), O-D swap asymmetry test, statistical comparison against shortest-path baseline, model fit to empirical GPS traces
- **Characteristic outputs**: Deviation-from-shortest-path curves by trip distance, O-D swap asymmetry metrics, pointiest-path vs human-path statistical fit comparison

### Planning pattern
- **Evidence count**: 4 distinct analytical results
- **Figure count**: 4 main, 0 Extended Data, 8 Supplementary figures, 3 Supplementary tables
- **Evidence chain**: phenomenon (GPS path deviations) -> O-D asymmetry discovery -> vector-based model formulation -> cross-city validation
- **Key figures**:
  - F1: establish (multiple panels) - Statistical features of pedestrian path choice from GPS traces
  - F2: reveal (multiple panels) - O-D swap asymmetry in chosen paths
  - F3: validate (multiple panels) - Vector-based navigation model ("pointiest paths") vs human trajectories
  - F4: extend (4 panels) - Cross-city generalization across different street network topologies
- **Narrative arc**: empirical observation -> anomaly discovery (asymmetry) -> cognitive model (vector-based navigation) -> cross-city validation -> universal property claim
- **Central claim**: Direction to goal is a main driver of pedestrian path planning, and vector-based navigation ("pointiest paths") is a statistically better predictor of human paths than distance minimization with stochastic effects, generalizing across cities with different street networks.
- **Claim strength**: descriptive

### Keywords
pedestrian navigation, GPS trajectories, path planning, vector-based navigation, pointiest paths, O-D asymmetry, stochastic distance minimization, urban street networks, Boston, San Francisco, cognitive navigation

---

## Demand-driven Bicycle Infrastructure Network Design

- **Paper**: Demand-driven design of bicycle infrastructure networks for improved urban bikeability (Nature Computational Science, 2022)
- **DOI**: 10.1038/s43588-022-00318-w
- **Domain**: human_mobility
- **Study design**: computational modeling (inverse percolation)
- **Outcome type**: network
- **Inferential target**: counterfactual_simulation

### Method specification
- **Method name**: Demand-driven inverse percolation framework for bike path network design
- **Hyperparameters**: Cycling demand distribution (from bike-sharing trip records), route choice safety preference parameters, iterative edge removal scheduling parameters
- **Required validations**: Comparison against homogenized-demand baseline, multi-city applicability test (Hamburg and Dresden), network efficiency metrics across removal iterations
- **Characteristic outputs**: Sequence of progressively reduced bike path networks adapted to cycling demand, network efficiency curves, demand-distribution importance quantification

### Planning pattern
- **Evidence count**: 6 distinct analytical results
- **Figure count**: 6 main, 0 Extended Data, 3 Supplementary figures
- **Evidence chain**: network formulation -> demand estimation -> inverse percolation algorithm -> efficiency evaluation -> demand-distribution comparison -> cross-city generalization
- **Key figures**:
  - F1: establish (multiple panels) - Conceptual framework for demand-driven bike network design
  - F2: quantify (multiple panels) - Cycling demand distribution from bike-sharing data
  - F3: reveal (multiple panels) - Inverse percolation: iterative network reduction with updated route choices
  - F4: compare (multiple panels) - Demand-driven vs homogenized-demand network comparison
  - F5: validate (multiple panels) - Network efficiency metrics across removal iterations
  - F6: extend (multiple panels) - Cross-city application (Hamburg and Dresden)
- **Narrative arc**: problem formulation -> data-driven demand modeling -> algorithmic network design -> quantitative evaluation -> counterfactual comparison -> generalization
- **Central claim**: A demand-driven inverse percolation approach generates families of efficient bike path networks that explicitly account for cyclist demand distribution and safety-based route choices, outperforming homogenized-demand alternatives.
- **Claim strength**: quasi_causal (simulation-based counterfactual)

### Keywords
bicycle infrastructure, network design, inverse percolation, demand-driven planning, bike-sharing data, route choice, safety preferences, urban bikeability, complex networks, Hamburg, Dresden

---

## urban_heat_trap_mobility_network

- **Paper**: The emergence of urban heat traps and human mobility in 20 US cities (npj Urban Sustainability, 2024)
- **DOI**: 10.1038/s42949-024-00142-3
- **Domain**: human_mobility
- **Study design**: cross_sectional
- **Outcome type**: rate
- **Inferential target**: association

### Method specification
- **Method name**: Mobility network construction + urban heat trap/escalate/escape ratio analysis
- **Hyperparameters**:
  - Mobility data: Spectus (Cuebiq) location-based data, February 2020 (pre-pandemic); ~15 million daily active US users; device-level home tract identification via dwell times; monthly aggregation of origin-destination trip counts at census tract level
  - Heat exposure: US Surface Urban Heat Island (SUHI) database; annual mean LST from MODIS + GMTED; 55,871 census tracts in 497 urbanized areas; quantile breaks into 3 clusters (low/median/high UHI)
  - Network: nodes = census tracts, edges = number of trips between tract pairs; intra-county only (no cross-county trips captured)
  - Classification: Urban heat trap = high-to-high trips; urban heat escalate = low-to-high trips; urban heat escape = high-to-low trips; metropolitan area classification based on relative percentages of the three trip types
- **Required validations**: Comparison across 20 metropolitan areas; consistency check (total high-origin trips to low + high destinations = same origin set); cross-city pattern comparison (e.g., LA dispersed vs. Chicago clustered traps)
- **Characteristic outputs**: Per-city heat trap/escalate/escape ratios; tract-level trip ratio maps; metropolitan area typology based on mobility-heat interaction; identification of priority cities for intervention (e.g., LA, Boston, Chicago)

### Planning pattern
- **Evidence count**: 3 distinct analytical results
- **Figure count**: 7 main, 0 Extended Data, Supplementary tables/figures present
- **Evidence chain**: data construction (mobility + SUHI) -> network analysis -> trap identification -> city-level comparison -> implication for urban design
- **Key figures**:
  - F1: establish (1 panel) — Heat level classification for study areas
  - F2-F7: reveal (4 panels each) — Per-city heat trap maps: UH level map, low-to-high ratio, high-to-high ratio, high-to-low ratio; detailed case studies for LA, Chicago, Boston, Atlanta, Minneapolis, Dallas
- **Narrative arc**: Data and network construction -> City-level patterns overview -> Detailed case studies of high-trap cities -> Heat escalation and escape quantification -> Urban planning implications
- **Central claim**: Urban heat traps exist in most studied US metropolitan areas, wherein populations residing in high-heat exposure areas primarily visit other high-heat exposure zones, with LA, Boston, and Chicago particularly pronounced, revealing that human mobility exacerbates rather than alleviates heat exposure inequality.
- **Claim strength**: descriptive

### Keywords
human mobility, mobility network, urban heat island, heat trap, location-based data, census tract, Spectus, SUHI, LST, network analysis, urban planning, environmental justice

---

## covid_mobility_manifold_learning

- **Paper**: Manifold learning reveals geographic and socioeconomic patterns in COVID-19 mobility behavior (Nature Computational Science, 2021)
- **DOI**: 10.1038/s43588-021-00125-9
- **Domain**: human_mobility
- **Study design**: panel_longitudinal
- **Outcome type**: continuous
- **Inferential target**: association

### Method specification
- **Method name**: Laplacian Eigenmaps (nonlinear manifold learning) + Gaussian Mixture Model (GMM) clustering on stay-at-home time series
- **Hyperparameters**:
  - Mobility data: SafeGraph v2.0/v2.1; 117 days (23 Feb 2020 onward); census block group (CBG) level; stay-at-home fraction = completely_home_device_count / device_count; home defined as most frequent nighttime location (18:00-07:00) over 6-week window at Geohash-7 (~153m x 153m)
  - Laplacian Eigenmaps: 50 neighbors (n_neighbors); optimal embedding dimension = 14 (determined by trustworthiness metric); tested alternative methods (diffusion maps with fixed/variable-bandwidth kernels)
  - GMM clustering: 5 clusters (selected via BIC knee-point detection); cluster assignments robust to initialization; low uncertainty values
  - States analyzed: California, Georgia, Texas, Washington
  - Covariates: 2018 ACS data (population, age, income, college enrollment, renter/owner, geographic mobility); COVID-19 case data by zip code (Washington State WDRS)
- **Required validations**: Cross-state consistency (embedding structure similar across 4 states); trustworthiness metric for embedding dimension selection; BIC knee-point for cluster count; cluster assignment robustness to initialization; comparison with linear dimensionality reduction (showed high uncertainty); linkage to COVID-19 case counts
- **Characteristic outputs**: 14-dimensional embedding of CBG mobility behavior; 5 mobility behavior clusters per state; cluster-geography correspondence (urban/peri-urban/rural); socioeconomic stratification by cluster; population turnover detection; cluster-COVID case association

### Planning pattern
- **Evidence count**: 5 distinct analytical results
- **Figure count**: 6 main, 0 Extended Data, ~20 Supplementary
- **Evidence chain**: data workflow -> manifold learning -> clustering -> geographic correspondence -> socioeconomic correlates -> epidemiological linkage
- **Key figures**:
  - F1: establish (multi-panel) — Analysis workflow overview, example CBG time series, data matrix construction, embedding visualization, cluster assignment
  - F2: reveal (multi-panel) — Cross-state clustering consistency across CA, GA, TX, WA; embedding + average time series per cluster
  - F3: reveal (multi-panel) — Metropolitan area mobility cluster maps (Seattle and other cities)
  - F4: expose_response (multi-panel) — CBG population characteristics by cluster (income, density, renter, college enrollment, geographic mobility)
  - F5: reveal (multi-panel) — Fraction of devices only away from home per day
  - F6: validate (multi-panel) — COVID-19 cases by zip code mapped to mobility cluster
- **Narrative arc**: Data aggregation -> Nonlinear dimensionality reduction -> GMM clustering -> Geographic patterns -> Socioeconomic correlates -> Population turnover detection -> COVID-19 case linkage -> Epidemiological framework
- **Central claim**: A low-dimensional manifold embedding of CBG-level stay-at-home time series reveals mobility behavior patterns that align with stay-at-home orders, correlate with socioeconomic factors, cluster geographically, and link to COVID-19 case counts, providing a framework for local epidemiologists to interpret mobility data.
- **Claim strength**: quasi_causal

### Keywords
manifold learning, Laplacian eigenmaps, Gaussian mixture model, COVID-19, mobility data, SafeGraph, stay-at-home behavior, socioeconomic factors, dimensionality reduction, clustering, census block group, epidemiology
