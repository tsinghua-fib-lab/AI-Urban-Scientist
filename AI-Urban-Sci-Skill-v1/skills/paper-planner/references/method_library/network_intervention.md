# Network Intervention

Methods for designing and evaluating interventions targeting social networks, measuring direct and spillover effects using network structure and causal inference.

## Gun Violence Network Intervention

- **Paper**: Reducing gunshot victimization in high-risk social networks through direct and spillover effects (Nature Human Behaviour, 2019)
- **DOI**: 10.1038/s41562-019-0688-1
- **Domain**: network_intervention
- **Study design**: natural_experiment
- **Outcome type**: binary
- **Inferential target**: causal_effect

### Method specification
- **Method name**: Quasi-experimental design with co-arrest network analysis, BART-based causal effect estimation for direct and spillover effects
- **Hyperparameters**: BART default priors (ntree=200, nu=3, alpha=0.95 for tree depth), 2,349 participants (seeds), 6,132 non-participant peers, 3-year co-arrest network construction window, 2-year post-intervention follow-up
- **Required validations**: posterior predictive checks, variable importance, comparison with difference-in-means estimator, entropy balancing (EBAL) robustness check, logistic regression sensitivity
- **Characteristic outputs**: CATE distributions via BART heterogeneity analysis, compliance effect (-3.2 percentage points), spillover effect (-1.5 percentage points), counterfactual victimization estimates (98 fewer victimizations)

### Planning pattern
- **Evidence count**: 4 distinct analytical results
- **Figure count**: 3 main, 0 Extended Data, 0 Supplementary
- **Evidence chain**: network construction → compliance effect estimation → spillover effect estimation → heterogeneity analysis
- **Key figures**:
  - F1: establish (multiple panels) — Research design illustration showing seed/peer identification and comparison groups
  - F2: quantify (multiple panels) — Compliance and spillover effect estimates with BART posterior distributions
  - F3: reveal (2 panels) — Heterogeneity of compliance and spillover effects across covariate profiles
- **Narrative arc**: network logic → intervention design → causal identification → direct effect → spillover effect → heterogeneity → counterfactual synthesis
- **Central claim**: A desistance-based gun violence intervention reduced two-year gunshot victimization by 3.2 percentage points among participants and by 1.5 percentage points among their network peers, demonstrating measurable spillover effects through co-arrest social networks.
- **Claim strength**: quasi_causal

### Keywords
network intervention, spillover effect, BART, co-arrest network, quasi-experimental, gun violence, desistance, peer influence, causal inference, treatment effect heterogeneity, Chicago
