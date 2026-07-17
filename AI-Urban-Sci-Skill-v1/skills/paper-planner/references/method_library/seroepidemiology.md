# Seroepidemiology

Methods for using serological data to estimate infection and vaccination patterns, often with dual-assay approaches and Bayesian modeling.

## SARS-CoV-2 Vaccination and Infection Disparities

- **Paper**: Using sero-epidemiology to monitor disparities in vaccination and infection with SARS-CoV-2 (Nature Communications, 2022)
- **DOI**: 10.1038/s41467-022-30051-x
- **Domain**: seroepidemiology
- **Study design**: cross_sectional
- **Outcome type**: binary
- **Inferential target**: association

### Method specification
- **Method name**: Bayesian binomial models with dual-assay serology (Vitros spike, Roche nucleocapsid) and hypergeometric priors
- **Hyperparameters**: Stan version 2.21.2, 4 chains with 2000 iterations (1000 burn-in), Vitros specificity 100%, sensitivity 83.8%, Roche specificity 99.80%, sensitivity 90.0%
- **Required validations**: R-hat convergence diagnostic, assay performance adjustment (manufacturer specificity, in-house sensitivity), bivariate dual-assay cross-validation, hypergeometric prior construction from population vaccination data
- **Characteristic outputs**: stratified probabilities of infection Pr(inf) and vaccination Pr(vacc) by age, race/ethnicity, and zipcode, infection-to-vaccination ratios by demographic group, geographic disparity maps

### Planning pattern
- **Evidence count**: 5 distinct analytical results
- **Figure count**: 5 main, 0 Extended Data, 0 Supplementary
- **Evidence chain**: sample characterization → assay result distribution → geographic disparity mapping → demographic stratification → vaccination-infection ratio analysis
- **Key figures**:
  - F1: establish (2 panels) — Sample age distribution and geographic representativeness by zipcode
  - F2: reveal (1 panel) — Schematic of parameters estimated using dual-assay serology
  - F3: quantify (2 panels) — Geographic maps of infection probability and vaccination probability by zipcode
  - F4: reveal (4 panels) — Stratified seroprevalence by assay and demographic group
  - F5: extend (2 panels) — Relationship between vaccination and infection probability by race/ethnicity with infographic
- **Narrative arc**: platform description → serology results → spatial disparities → demographic disparities → double-burden synthesis
- **Central claim**: During early vaccine roll-out in San Francisco, Hispanic/Latinx residents faced 5.3x higher infection risk than White residents, while White residents over 65 were twice as likely to be vaccinated as Black/African American residents, creating a double burden of disparities.
- **Claim strength**: suggestive

### Keywords
seroepidemiology, dual assay, Bayesian estimation, vaccination disparity, infection disparity, SARS-CoV-2, spike protein, nucleocapsid, Stan, hypergeometric prior, health equity
