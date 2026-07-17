# Cultural Geography & Migration

Entries on measuring cultural similarity, cultural factors in migration, and gravity-model-based migration analysis.

---

## Religious Cultural Similarity Index (RCS) for Migration Analysis

- **Paper**: Impact of religious cultural similarity on internal migration: a regional perspective in contemporary China (Humanities and Social Sciences Communications, 2025)
- **DOI**: 10.1057/s41599-025-05272-2
- **Domain**: Cultural geography, internal migration, regional analysis
- **Study design**: Panel regression with origin-destination fixed effects across 339 Chinese cities, 2019-2022
- **Outcome type**: Migration Index (MI) proxy for migration stock, derived from Spring Festival Baidu LBS data
- **Inferential target**: Effect of religious cultural similarity between city pairs on intercity migration flows

### Method specification
- **Method name**: Religious Cultural Similarity (RCS) index + gravity model panel regression
- **Hyperparameters**: RCS: cosine similarity of 4-dimensional religious building vectors, rescaled 0-100; gravity model: origin + destination fixed effects, 1-year lag on independent variables; religious entropy K-means clustering with 5 centroids
- **Required validations**: Alternative RCS (Herfindahl Similarity Index); instrumental variable approach; Poisson pseudo-maximum likelihood estimator with three-way fixed effects; cross-sectional OLS by year; spatial lag model; 2-year lag robustness; alternative migration data (Census province-level stocks); net flow as alternative DV
- **Characteristic outputs**: RCS coefficients on migration; interaction effects by religious culture type; religious entropy clustering (5 types: equilibrium, TTT, Christian, ancestor worship, Islamic); robustness test coefficient tables

### Planning pattern
- **Evidence count**: 5 distinct analytical results
- **Figure count**: 3 main, 0 ED, unspecified Supplementary
- **Evidence chain**: cultural landscape description → RCS index construction → gravity model estimation → heterogeneity by religious type → robustness & endogeneity tests
- **Key figures**:
  - F1: City religious culture vectorization approach — 4D vector construction, cosine similarity matrix
  - F2: Religious entropy workflow — Shannon entropy calculation, K-means centroid selection, 5-type classification
  - F3: Spatiotemporal distribution of five religious cultures — geographic map + temporal trends 2016-2022
- **Narrative arc**: Religious culture diversity in China → operationalize as RCS index → gravity model shows RCS promotes migration → effect varies by religious type → extensive robustness confirms findings
- **Central claim**: Religious cultural similarity between cities significantly promotes internal migration in China, with effects varying by regional religious setting
- **Claim strength**: Suggestive (observational with extensive robustness checks and IV approach)

### Keywords
religious culture, migration, gravity model, cultural similarity, China, cosine similarity, Shannon entropy, K-means clustering, Baidu migration index, fixed effects, instrumental variable, regional perspective, internal migration stock, Spring Festival
