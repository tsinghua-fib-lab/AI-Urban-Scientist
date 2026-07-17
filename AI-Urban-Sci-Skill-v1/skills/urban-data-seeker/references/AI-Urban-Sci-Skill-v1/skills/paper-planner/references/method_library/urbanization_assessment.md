# Urbanization Assessment

Entries for papers evaluating multidimensional urbanization progress using indicator systems, coordination indices, and multi-scale statistical comparison of population, land, and people-centered urbanization dimensions.

---

## people_oriented_urbanization_multidimensional

- **Paper**: People-oriented urbanization lags behind population and land urbanization in China (npj Urban Sustainability, 2025)
- **DOI**: 10.1038/s42949-025-00251-7
- **Domain**: urbanization_assessment
- **Study design**: panel_longitudinal
- **Outcome type**: continuous
- **Inferential target**: association

### Method specification
- **Method name**: Multidimensional indicator system + paired t-test + 45-degree linear analysis + evenness index (modified radar chart method)
- **Hyperparameters**:
  - Sample: 283 prefecture-level cities in mainland China; time period 2005-2020 (4 time points)
  - Urbanization dimensions:
    - Population urbanization: proportion of permanent urban residents (0-100%)
    - Land urbanization: total urban built-up area (km²)
    - People-oriented urbanization: 16 indicators across 4 sub-dimensions:
      - Economic (e.g., GDPP, AW, CEP, AD, FAI, R&DEP)
      - Social (e.g., PP, EEP, NHTR)
      - Environmental (e.g., PM2.5, SDE, GSP)
      - Social equity (e.g., Gini, URIR, UPR, HPIR)
  - Statistical methods:
    - Paired t-test: dimensional differences between population/land and people-oriented urbanization
    - 45-degree linear analysis: lagging vs. leading characteristics identification
    - Multivariate fitting analysis: relational pattern examination
    - Evenness index: modified radar chart method for coordinated development assessment
  - Multi-scale classification: 4 geographical regions (eastern, central, western, northeastern); 3 city sizes (large > 5M, medium 1-5M, small < 1M); urban agglomeration vs. non-urban agglomeration
  - Data preprocessing: spatial overlay consistency verification (e.g., PM2.5 raster with city statistics); exclusion of cities with incomplete data
- **Required validations**: Paired t-test significance for dimensional differences; evenness index temporal trend consistency (U-shaped pattern verification); cross-scale pattern robustness (regional, size, agglomeration)
- **Characteristic outputs**: Base-period growth rates for 18 indicators (2005-2020); east-west gradient analysis; city size comparison patterns; urban agglomeration vs. non-agglomeration differences; evenness index time series; base-period growth rate evenness trends

### Planning pattern
- **Evidence count**: 5 distinct analytical results
- **Figure count**: 9 main, 0 Extended Data, Supplementary tables present
- **Evidence chain**: indicator framework -> temporal trends -> regional differences -> population/land correlation -> coordination assessment
- **Key figures**:
  - F1: reveal (multi-panel) — Spatio-temporal patterns of 18 urbanization indicators across Chinese cities (2005-2020)
  - F2: compare (multi-panel) — Multiscale distribution across 4 Chinese regions
  - F3-F4: expose_response (multi-panel each) — Relationships between population/land urbanization and people-oriented indicators
  - F5: quantify (1 panel) — U-shaped evenness index change pattern (2005-2020)
  - F6-F7: reveal (multi-panel each) — Spatiotemporal evenness trends at multiple scales (evenness index and base-period growth rate evenness)
  - F8-F9: establish (1 panel each) — Study area map and research framework diagram
- **Narrative arc**: Framework development -> Overall temporal trends (18 indicators) -> Regional gradient analysis (east-west) -> City size and agglomeration comparisons -> Population/land vs. people-oriented correlation analysis -> Evenness index coordination assessment -> U-shaped pattern discovery -> Policy recommendations
- **Central claim**: Between 2005-2020, China's economic and social people-oriented urbanization indicators lagged behind land and population urbanization, while environmental indicators caught up, and the evenness index showed a U-shaped pattern indicating convergence after the 2014 new-type urbanization plan implementation.
- **Claim strength**: descriptive

### Keywords
people-oriented urbanization, evenness index, paired t-test, radar chart method, multidimensional indicators, China, prefecture-level cities, population urbanization, land urbanization, coordination assessment, SDG11, new-type urbanization
