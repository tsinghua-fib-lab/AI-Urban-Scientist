# Climate Impact & Crime

Entries on quantifying climate and weather effects on crime patterns using interpretable machine learning, regression decomposition, and social cost assessment.

---

## IML-MLR Crime Determinant Decomposition with VSLY Social Cost

- **Paper**: The impact of weather patterns on increasing violent crime and social cost in South Africa (Humanities and Social Sciences Communications, 2025)
- **DOI**: 10.1057/s41599-025-05460-0
- **Domain**: Climate impact, criminology, social cost, interpretable ML
- **Study design**: Multi-region observational analysis (South Africa, Mexico, Chicago USA) with ML decomposition
- **Outcome type**: Crime frequency by type (violent, violent-related, property, other); intentional homicide rate; social cost in USD
- **Inferential target**: Meteorological vs. anthropogenic contribution to crime trends; temperature and precipitation effects on violent crime

### Method specification
- **Method name**: Interpretable Machine Learning (IML) with SHAP + Multiple Linear Regression (MLR) decomposition + Adjusted Value of Statistical Life Year (VSLY)
- **Hyperparameters**: ML models tested: ANN, MLP, DT, GBM, XGBoost (XGBoost selected: R²=0.96); SHAP: tree-SHAP variant for XGBoost; MLR: seasonal dummy variables; Poisson regression with holiday controls
- **Required validations**: Cross-region generalization (Mexico, Chicago); Global and Local Moran's I spatial autocorrelation; LSDV model for cross-region heterogeneity; Granger causality test; ADF stationarity test
- **Characteristic outputs**: Meteorological vs. anthropogenic decomposition percentages; SHAP feature importance rankings; partial dependence plots; VSLY social cost estimates; spatial crime clustering maps; cross-region comparison tables

### Planning pattern
- **Evidence count**: 7 distinct analytical results
- **Figure count**: 5 main, 0 ED, unspecified Supplementary
- **Evidence chain**: crime pattern description → MLR decomposition (meteorological vs. anthropogenic) → temperature/precipitation effects → SHAP-driven IML for homicide → social cost estimation → cross-region generalization → spatial autocorrelation analysis
- **Key figures**:
  - F1: Spatiotemporal crime patterns — total crimes by province, quarterly trends by crime type
  - F2: IML study framework — data flow through DT/ANN/MLP/GBM/XGBoost → SHAP → contribution assessment
  - F3: SHAP values of crime drivers — summary plot + partial dependence for pGDP, PM2.5, education, temperature
  - F4: International homicide rate & social cost world map
  - F5: Chicago crime distribution & Moran's I cluster analysis (160m grid)
- **Narrative arc**: Crime seasonality observed → MLR attributes 64% of violent crime to weather → temperature and precipitation quantify → SHAP/XGBoost identifies multi-driver homicide model → VSLY quantifies social cost → method generalizes to Mexico and Chicago → spatial clustering reveals hotspots
- **Central claim**: Meteorological factors account for 64% of violent crime contribution in South Africa, with temperature and precipitation as primary drivers, and this decomposition approach generalizes across regions
- **Claim strength**: Suggestive (observational decomposition with cross-region validation)

### Keywords
climate impact, violent crime, interpretable machine learning, SHAP, XGBoost, multiple linear regression, VSLY, social cost, temperature effect, precipitation, South Africa, spatial autocorrelation, Moran's I, crime decomposition, Poisson regression
