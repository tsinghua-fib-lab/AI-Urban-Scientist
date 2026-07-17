# Causal Inference Frameworks

Methods grounded in formal causal inference theory, particularly the Rubin Causal Model (potential outcomes framework), propensity score matching for design-stage covariate balance, and Bayesian imputation of missing potential outcomes.

---

## Rubin Causal Model with propensity score matching (weather and crime in Boston)

- **Paper**: Comparing apples to apples: an environmental criminology analysis of the effects of heat and rain on violent crimes in Boston (Humanities and Social Sciences Communications, 2018)
- **DOI**: 10.1057/s41599-018-0188-3
- **Domain**: Environmental criminology, public health
- **Study design**: Observational study reconstructed as four hypothetical randomized experiments via design-stage matching
- **Outcome type**: Daily violent crime counts, aggravated assault counts, larceny counts
- **Inferential target**: Average exposure effect (AEE) of heat index levels and rainfall occurrence on daily crime counts

### Method specification
- **Method name**: Rubin Causal Model (RCM) with propensity score matching + Bayesian negative-binomial imputation
- **Hyperparameters**: 4 hypothetical experiments (Negative HI: extremely cold vs very cold; Mild HI: cold vs temperate; High HI: very hot vs extremely hot; Precipitation: rainy vs dry); one-to-one matching with caliper on estimated propensity score; 20,000 MCMC iterations with 10,000 burn-in; Negative-Binomial distribution for potential outcomes; weakly informative priors (Half-Cauchy(0,5) for dispersion, N(0,5) for intercept, N(0,2.5) for slopes)
- **Required validations**: Propensity score estimation via logistic regression with AIC stepwise selection; overlap assessment in propensity score distributions (outlying days discarded); covariate balance diagnostic (Love plots, standardized mean differences); empirical distribution comparison before/after matching; SUTVA assumption; exploratory analysis in Los Angeles for comparison
- **Characteristic outputs**: Average exposure effect (AEE) with 95% posterior intervals for each experiment; covariate balance diagnostics; spatial mapping of crime counts by zip code across exposure levels

### Planning pattern
- **Evidence count**: 3 distinct results (primary, exploratory, spatial)
- **Figure count**: 5 main figures, multiple supplementary
- **Evidence chain**: design stage (propensity score estimation, overlap assessment, matching) -> analytic stage (Bayesian NB imputation) -> primary results (4 AEE estimates) -> exploratory (aggravated assault, larceny) -> spatial description (zip-code variation)
- **Key figures**:
  - F1: Crime count distributions by exposure level after matching (heat index categories, dry vs rainy)
  - F2: AEE estimates with posterior intervals across 4 experiments
  - F3: Spatial map of average daily violent crimes by zip code
  - F4: Spatial maps by exposure level across experiments
  - F5: Smooth LOESS curves for heat index experiments
- **Narrative arc**: problem (associational models cannot quantify causal weather-crime effects) -> RCM framework -> 4 design stages reconstructing hypothetical experiments -> primary causal estimates -> exploratory crime types -> spatial heterogeneity -> comparison with LA -> policy implications
- **Central claim**: On average, more violent crimes occur on temperate days compared to extremely cold days, and on dry days compared to rainy days in Boston, but no significant difference is found between extremely hot and less warm days.
- **Claim strength**: Quasi-causal

### Keywords
Rubin Causal Model, RCM, propensity score matching, potential outcomes, Bayesian imputation, negative-binomial, weather-crime relationship, heat index, rainfall, violent crime, causal inference, design stage, covariate balance, MCMC
