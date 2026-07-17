# Landscape Ecology

Entries for papers analyzing the effects of landscape patterns, composition, and configuration on ecological processes such as vegetation growth, habitat quality, or ecosystem services.

---

## landscape_pattern_indirect_effects_BRT

- **Paper**: Indirect non-linear effects of landscape patterns on vegetation growth in Kunming City (npj Urban Sustainability, 2024)
- **DOI**: 10.1038/s42949-024-00165-w
- **Domain**: landscape_ecology
- **Study design**: spatial
- **Outcome type**: continuous
- **Inferential target**: association

### Method specification
- **Method name**: Boosted Regression Tree (BRT) model + cubic polynomial NDVI-UI relationship for Urbanization Indirect Effects on Vegetation Growth (UIE-VG)
- **Hyperparameters**:
  - UIE-VG estimation: cubic polynomial regression (order = 3) between NDVI and urbanization intensity (UI = built-up land percentage); V_nv (nonvegetative NDVI threshold) = 0.05; zero-impact straight line baseline
  - Landscape metrics: 10 metrics at class level — CA (total core area), PLAND (percentage of landscape), AREA_MN (mean patch area), SHAPE_MN (mean shape index), ENN_MN (mean Euclidean nearest neighbor), AI (aggregation index), COHESION (patch cohesion), LPI (large patch index), PD (patch density), ED (edge density); composition metrics (CA, PLAND, AREA_MN) + configuration metrics (remaining 7)
  - Analytical scale: 250 x 250 m grid; elevation filter: +/- 50m from urban core average; farmland units excluded
  - BRT model: "gbm" package in R 4.2.2; land cover maps from Landsat via GEE (2001-2019); random forest classifier in ENVI 5.6 (accuracy > 90% per year); NDVI time-series 8-day composite, 30m, Gap Filling + Savitzky-Golay filtering
  - Statistical tests: Welch t test for mean differences across years; Games-Howell test for pairwise comparison
- **Required validations**: Cubic regression significance (p < 0.05) for each year; Adjusted r² > 0.5 for NDVI-UI model; classification accuracy > 90% (confusion matrix); Games-Howell test significance for year-to-year changes in mean UIE-VG
- **Characteristic outputs**: UIE-VG spatial distributions (omega_i positive/negative) per year; landscape metric contribution rankings via BRT; temporal shifts in dominant landscape drivers (waterbody metrics -> built-up metrics); non-linear relationships between top 3 metrics and UIE-VG per land cover type

### Planning pattern
- **Evidence count**: 4 distinct analytical results
- **Figure count**: 10 main, 0 Extended Data, Supplementary tables/figures present
- **Evidence chain**: NDVI-UI relationship -> spatiotemporal UIE-VG evolution -> landscape metric contributions -> dominant metric non-linear relationships
- **Key figures**:
  - F1: establish (1 panel) — NDVI vs. UI relationship curves (2001, 2010, 2019)
  - F2: reveal (multi-panel) — Spatial distributions of negative indirect effects (omega_i < 0) across Kunming
  - F3: quantify (multi-panel) — Statistical description of omega_i and Games-Howell test results
  - F4: expose_response (multi-panel) — Contributions of landscape composition vs. configuration metrics
  - F5: expose_response (multi-panel) — Contributions of top 10 landscape metrics
  - F6-F9: reveal (multi-panel each) — Non-linear relationships between top 3 metrics and UIE-VG for built-up land, unused land, vegetated areas, and waterbodies
  - F10: establish (1 panel) — Study area location
- **Narrative arc**: Conceptual framework (direct vs. indirect effects) -> NDVI-UI cubic relationship -> Spatiotemporal UIE-VG mapping -> Landscape metric contribution via BRT -> Dominant metric identification -> Non-linear relationship analysis -> Urban greening planning implications
- **Central claim**: Area-related and aggregation-related landscape metrics have greater effects on indirect effects of urbanization on vegetation growth than other metrics, with built-up land metrics becoming dominant over time (from 21.5% to 86.4% contribution), while large aggregated vegetation areas may mitigate negative effects in low urbanization areas.
- **Claim strength**: descriptive

### Keywords
boosted regression tree, landscape metrics, NDVI, urbanization intensity, vegetation growth, indirect effects, landscape composition, landscape configuration, Kunming, GEE, Landsat, urban greening, non-linear effects
