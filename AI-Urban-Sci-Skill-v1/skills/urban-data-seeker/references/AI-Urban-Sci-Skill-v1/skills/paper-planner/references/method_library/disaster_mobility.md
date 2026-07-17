# Disaster Mobility / Digital Trace Data

Methods using GPS mobility data, cell phone telemetry, and other digital trace data sources to study human behavior during and after disasters. Includes stay-point algorithms, kernel density estimation, sampling bias correction, and multi-source community-scale data integration.

---

## GPS mobility data analysis with stay-point algorithm (Hurricane Harvey evacuation disparities)

- **Paper**: High-resolution human mobility data reveal race and wealth disparities in disaster evacuation patterns (Humanities and Social Sciences Communications, 2021)
- **DOI**: 10.1057/s41599-021-00824-8
- **Domain**: Disaster evacuation, social inequality, human mobility
- **Study design**: Observational analysis of anonymized GPS mobility data during Hurricane Harvey
- **Outcome type**: Evacuation status, evacuation distance, destination choice, departure/return timing
- **Inferential target**: Impact of race and wealth on disaster evacuation behavior

### Method specification
- **Method name**: GPS mobility data analysis with stay-point algorithm + KDE + sampling bias correction (weighting + bootstrap)
- **Hyperparameters**: 30 million GPS records, 150,000 users, Greater Houston MSA, July-October 2017; stay-point thresholds: 50 m spatial, 5 min temporal; home detection: weekday evenings 8pm-7am, agglomerative clustering with 50 m max diameter, 5-week cross-validation with 1-week tolerance; evacuation detection: sliding window (5/7 days), >=3 consecutive days departure, 1 km distance threshold; 6 neighborhood types by race (Black/Hispanic/White) and wealth (poor/non-poor, 25% poverty threshold)
- **Required validations**: Sampling bias correction via two strategies: (i) weighting by device-to-population ratio from ACS 2018, (ii) bootstrap resampling with uniform sampling rate (100 iterations); sensitivity analysis with different poverty/race thresholds; user filtering: >=60 unique days, >=100 stay points
- **Characteristic outputs**: Relative evacuation rates by neighborhood type; evacuation distance distribution (truncated power-law fit); origin-destination transition matrices; departure/return kernel density plots; daily disparity rates for wealth and race

### Planning pattern
- **Evidence count**: 3 distinct analytical results (who evacuated, where they went, how long they were gone)
- **Figure count**: 4 main figures, multiple supplementary
- **Evidence chain**: who evacuated (relative rates by neighborhood) -> evacuation distance distribution (universality) -> destination homophily (transition matrices) -> departure/return timing -> temporal disparity rates
- **Key figures**:
  - F1: Geographical and socio-demographic evacuation patterns (6 panels) — net evacuation intensity KDE maps, relative evacuation rates by neighborhood type
  - F2: Evacuation distance distribution and destination transition matrices — truncated power-law fit, socioeconomic homophily in destination choice
  - F3: Race and wealth impacts on evacuation/return times — kernel density of departure/return, duration distributions by income/race
  - F4: Time progression of class and racial disparity — cumulative disparity rates in departure and return over time
- **Narrative arc**: gap (lack of large-scale quantitative research on race/wealth in disaster evacuation) -> data and methods (GPS, stay-point, bias correction) -> who evacuated (non-poor White overrepresented) -> where they went (distance universal, destination homophilous) -> how long gone (disparities in timing) -> policy implications
- **Central claim**: Both race and wealth strongly impact evacuation patterns, with disadvantaged minority populations less likely to evacuate than wealthier white residents, and with considerable discrepancies in departure and return times.
- **Claim strength**: Suggestive

### Keywords
GPS mobility data, stay-point algorithm, kernel density estimation, sampling bias correction, bootstrap, Hurricane Harvey, disaster evacuation, race disparity, wealth disparity, socioeconomic homophily, power-law distribution, census block group, digital trace data

---

## Multi-source community-scale data integration (Winter Storm Uri impact assessment)

- **Paper**: Community-scale big data reveals disparate impacts of the Texas winter storm of 2021 and its managed power outage (Humanities and Social Sciences Communications, 2022)
- **DOI**: 10.1057/s41599-022-01353-8
- **Domain**: Disaster impact assessment, social equity, infrastructure resilience
- **Study design**: Observational multi-source data analysis at census-tract level
- **Outcome type**: Power outage extent/duration (activity density proxy), burst pipe incidence (311 calls), food inaccessibility (POI visit trends)
- **Inferential target**: Disparate impacts of Winter Storm Uri on low-income and racial/ethnic minority subpopulations

### Method specification
- **Method name**: Multi-source community-scale data integration + Kruskal-Wallis + spatial autocorrelation (Moran's I) + agglomerative hierarchical clustering
- **Hyperparameters**: Harris County, Texas, 786 census tracts, January-February 2021; data sources: Mapbox population activity (100m grid, 4h temporal resolution), SafeGraph POI visits (grocery stores NAICS 445110, restaurants NAICS 72251, 1-mile buffer), Houston 311 service helpline (water-related requests), ACS 2019 demographics; minority classification: top/bottom 25% by income, Black ratio, Hispanic ratio
- **Required validations**: Kruskal-Wallis test for nonparametric group comparisons (income, race, ethnicity); Global Moran's I with Monte Carlo simulation (999 permutations, queen contiguity weights); agglomerative hierarchical clustering with Euclidean distance and Ward's linkage for POI visit trend classification; baseline comparison using January 2021 data
- **Characteristic outputs**: Activity density changes and recovery duration distributions by demographic group; 311 call peak normalization (per area per person); POI visit trend clusters (4 classes from most to least impacted); spatial autocorrelation coefficients; statistical test results across 6 demographic pairings

### Planning pattern
- **Evidence count**: 3 impact domains (power outages, burst pipes, food inaccessibility)
- **Figure count**: 10 main figures
- **Evidence chain**: data integration schematic -> demographic group definition -> power outage assessment (activity density) -> burst pipe assessment (311 calls) -> food accessibility (POI clustering) -> disparity analysis across 3 domains
- **Key figures**:
  - F1: Study schematic — multi-source data integration workflow
  - F2: Demographic group maps — high/low income, Black minority, Hispanic minority
  - F3: Activity density time series example — power outage onset and recovery
  - F4: Activity density feature distributions by demographic group
  - F5: Significantly impacted census tracts vs all tracts comparison
  - F6-F8: 311 call analysis — temporal spike, distribution by group, impacted tracts comparison
  - F9: POI visit trend clusters — restaurant and grocery store spatiotemporal patterns
  - F10: Food inaccessibility classes vs demographic groups
- **Narrative arc**: gap (no granular power outage data available, scarce winter storm studies) -> multi-source data as proxy -> power outages disproportionately affect low-income/minority tracts -> burst pipes more severe in same communities -> food inaccessibility clusters reveal secondary impacts -> infrastructure equity implications
- **Central claim**: Low-income and racial/ethnic minority census tracts experienced greater extent and duration of power outages, more burst pipes, and more severe food inaccessibility during Winter Storm Uri, revealing social inequality in managed service disruptions.
- **Claim strength**: Suggestive

### Keywords
community-scale big data, Mapbox activity density, SafeGraph POI visits, 311 service calls, Kruskal-Wallis, spatial autocorrelation, Moran's I, agglomerative hierarchical clustering, Winter Storm Uri, power outage, burst pipes, food inaccessibility, social equity, census tract, digital trace data
