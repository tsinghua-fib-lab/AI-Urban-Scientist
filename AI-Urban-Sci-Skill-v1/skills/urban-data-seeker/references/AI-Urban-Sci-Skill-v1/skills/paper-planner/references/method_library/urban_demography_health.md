# Urban Demography & Health

Methods and patterns for studying relationships between urban demographic change (shrinkage, growth) and public health outcomes.

---

## Urban Shrinkage and COVID-19 Excess Mortality

- **Paper**: Association between urban shrinkage and excess mortality during the COVID-19 pandemic (Nature Cities, 2025)
- **DOI**: 10.1038/s44284-025-00278-y
- **Domain**: urban_demography_health
- **Study design**: observational (county-level panel)
- **Outcome type**: continuous (excess deaths per 100,000) + count (mortality peaks)
- **Inferential target**: association

### Method specification
- **Method name**: Kruskal-Wallis tests + mixed-effects models for urban shrinkage-mortality association
- **Hyperparameters**: Urban shrinkage classification parameters (population CAGR and GRDP CAGR thresholds defining 4 urban types: growing, shrinking, pop-growth/econ-decline, pop-decline/econ-growth), excess death calculation parameters (baseline 2015-2019, pandemic period March 2020-February 2023), mixed-effects random effect structure, peak detection algorithm parameters, Bonferroni post-hoc test parameters
- **Required validations**: Shrinkage classification robustness, excess death baseline period adequacy, mixed-effects model convergence, peak detection algorithm validation, socioeconomic confounder assessment
- **Characteristic outputs**: Four urban type classifications for 1,142 US counties, monthly excess deaths per 100,000 by urban type, mortality peak frequency counts, severity gradient analysis (excess deaths by shrinkage degree), socioeconomic mediator analysis (income, education, unemployment, age structure, race)

### Planning pattern
- **Evidence count**: 4 distinct analytical results
- **Figure count**: 4 main, 2 Extended Data figures, 12 Supplementary tables
- **Evidence chain**: shrinkage classification -> excess mortality comparison -> severity gradient analysis -> socioeconomic mediator assessment
- **Key figures**:
  - F1: establish (multiple panels) - Urban shrinkage classification framework and spatial distribution of four urban types across 1,142 US counties
  - F2: quantify (multiple panels) - Excess mortality comparison: shrinking counties (165% higher) vs growing counties
  - F3: reveal (multiple panels) - Severity gradient: excess deaths increase with degree of demographic and economic contraction
  - F4: extend (multiple panels) - Socioeconomic disadvantages as mediators (income, education, unemployment, age, race)
- **Narrative arc**: classification framework -> outcome comparison -> dose-response gradient -> mediator identification -> policy recommendation
- **Central claim**: Shrinking US counties experienced 165% higher COVID-19 excess deaths and 142% more mortality peaks than growing counties, with severity increasing proportionally with demographic and economic contraction, mediated by socioeconomic disadvantages.
- **Claim strength**: suggestive (observational panel with mixed-effects modeling)

### Keywords
urban shrinkage, excess mortality, COVID-19, Kruskal-Wallis test, mixed-effects model, county-level analysis, US counties, socioeconomic disadvantage, population decline, economic contraction, mortality peaks, place-based health strategy
