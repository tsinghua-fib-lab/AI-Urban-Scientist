# Machine Learning Prediction with Interpretability

Methods that use machine learning models (tree ensembles, neural networks) for prediction and leverage interpretation techniques (SHAP, PDP, permutation importance) to understand feature effects. Includes XGBoost, Random Forest, GBDT, and Artificial Neural Networks.

---

## XGBoost with SHAP interpretation (built environment and cycling propensity)

- **Paper**: The nonlinear relationship between built environment and cycling propensity for different travel purposes — based on extreme gradient boosting decision tree (Scientific Reports, 2025)
- **DOI**: 10.1038/s41598-025-10788-3
- **Domain**: Urban transportation, travel behavior
- **Study design**: Cross-sectional survey-based prediction with model comparison
- **Outcome type**: Binary cycling choice (1 = bicycle, 0 = otherwise)
- **Inferential target**: Nonlinear relationships and threshold effects between built environment variables and cycling propensity

### Method specification
- **Method name**: XGBoost (Extreme Gradient Boosting Decision Tree) with permutation importance, PDP, and SHAP interpretation
- **Hyperparameters**: Hyperparameter grid search with fivefold cross-validation; compared: Logistic Regression, Random Forest, GBDT, XGBoost; 70/30 train/test split; N=6,231 cycling records from 2018 Daily Trip Survey in Xianyang, China; two models: compulsory trips and discretionary trips
- **Required validations**: Model comparison on accuracy, precision, recall, F1, AUC, ROC curves; VIF multicollinearity test (all VIF < 5); fivefold cross-validation; hyperparameter grid search; two complementary interpretation methods (permutation importance + SHAP) for consistency check
- **Characteristic outputs**: Prediction accuracy (89% compulsory, 80% discretionary); relative importance rankings; partial dependence plots showing nonlinear threshold effects; SHAP value importance rankings; SHAP summary plots (feature value vs SHAP value)

### Planning pattern
- **Evidence count**: 3 distinct analytical results (model comparison, relative importance, nonlinear/SHAP analysis)
- **Figure count**: 13 main figures
- **Evidence chain**: model comparison (4 algorithms) -> feature importance ranking -> nonlinear relationships via PDP (8+ variables) -> SHAP importance -> SHAP summary plots -> policy thresholds
- **Key figures**:
  - F1: Study area and built environment characteristics (4 panels)
  - F2: ROC curve comparison of 4 models
  - F3-F11: Partial dependence plots for 9 key variables (travel distance, population density, POI diversity, distance from center, isolation bar proportion, non-motor lane parking, shopping facilities, bus stops, intersection density)
  - F12-F13: SHAP importance diagrams and SHAP summary plots
- **Narrative arc**: gap (linear models dominate, nonlinear relationships understudied) -> model comparison (XGBoost best) -> feature importance (built environment matters more for compulsory trips) -> nonlinear threshold effects identified -> SHAP confirms importance rankings -> actionable thresholds (e.g., non-motorized lane >80%, parking <25%)
- **Central claim**: The built environment exerts a more substantial impact on cycling for compulsory trips than discretionary trips, with significant nonlinear relationships and threshold effects identified through XGBoost and SHAP analysis.
- **Claim strength**: Descriptive / predictive

### Keywords
XGBoost, SHAP, partial dependence plots, permutation importance, machine learning, cycling propensity, built environment, nonlinear relationship, threshold effect, travel behavior, model comparison, logistic regression, random forest, GBDT

---

## Artificial Neural Networks — Hurricane Impact Level Model

- **Paper**: Spatial and temporal variations in resilience to tropical cyclones along the United States coastline as determined by the multi-hazard hurricane impact level model (Humanities and Social Sciences Communications, 2017)
- **DOI**: 10.1057/s41599-017-0016-1
- **Domain**: Disaster risk, coastal resilience
- **Study design**: Machine learning model trained on historical events, applied to hypothetical scenarios
- **Outcome type**: Hurricane Impact Level (IL 0-5), categorical economic damage classification
- **Inferential target**: Complex nonlinear relationships between multi-hazard meteorological factors, landfall location, and economic damage

### Method specification
- **Method name**: Artificial Neural Networks (ANN) — Hurricane Impact Level (HIL) Model
- **Hyperparameters**: 11 ANNs (designated A through K), each with 20 hidden neurons; maximum 3% error criterion; no false-positive classification; trained on 74 historical tropical cyclone events (1998-2017); 7 events used in testing per network; inputs: maximum wind speed, minimum pressure, maximum storm surge, total precipitation, landfall lat/long (up to 4), population affected
- **Required validations**: Multi-network ensemble approach (11 networks averaged for confidence); testing phase with randomly selected events; hypothetical landfall relocation scenarios; historical event re-simulation with present-day conditions; comparison with population/wealth-only normalization (Pielke et al. 2008); probabilistic distribution fitting with 400 simulations per location
- **Characteristic outputs**: Impact Level predictions (0-5) with confidence scores; Hinton diagrams showing network weights and neuron connections; probability distributions of IL across locations; comparative IL for historical events at actual vs hypothetical locations; historical event IL comparison (then vs now)

### Planning pattern
- **Evidence count**: 3 analytical results (hypothetical scenarios, historical re-simulation, resilience assessment)
- **Figure count**: 3 main figures
- **Evidence chain**: ANN architecture explanation (Hinton diagrams) -> hypothetical landfall relocation (Sandy to Florida, Ike to NC, Andrea to NYC) -> historical event re-simulation (1900 Galveston, 1938 New England, Camille, Andrew) -> resilience assessment over time
- **Key figures**:
  - F1: Hinton diagrams of Networks A and B — excitatory/inhibitory neuron connections
  - F2: Hypothetical scenario comparison — IL probability distributions for relocated storms across locations
  - F3: Historical events timeline — IL at time of occurrence vs if hitting today
- **Narrative arc**: vulnerability question (are East and Gulf coasts equally resilient?) -> ANN model explanation -> hypothetical relocations show Gulf Coast more resilient -> historical events show population growth outweighs infrastructure improvements -> northeastern corridor identified as increasingly vulnerable
- **Central claim**: Even with improved infrastructure and policy over the past century, population growth along the US coastline has counteracted resilience gains, and northeastern coastal communities show lower resilience to hurricanes than southern counterparts.
- **Claim strength**: Descriptive / exploratory

### Keywords
artificial neural network, ANN, Hurricane Impact Level, HIL model, machine learning, tropical cyclone, coastal resilience, multi-hazard, hypothetical scenarios, Hinton diagram, economic damage, building codes, population growth
