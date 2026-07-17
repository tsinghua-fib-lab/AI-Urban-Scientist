# Urban Mobility & Accessibility

Entries on quantifying urban accessibility, mobility patterns, and mobility inequality using mobility data, counterfausal methods, and network embeddings.

---

## CRANE — Counterfactual Random-walk-based Network Embedding for Accessibility Gaps

- **Paper**: Counterfactual mobility network embedding reveals prevalent accessibility gaps in U.S. cities (Humanities and Social Sciences Communications, 2024)
- **DOI**: 10.1057/s41599-023-02570-5
- **Domain**: Urban mobility, accessibility inequality, causal inference
- **Study design**: Observational, quasi-experimental causal inference across 6 U.S. MSAs
- **Outcome type**: Mobility frequency, mobility reduction, urban facility accessibility by POI category
- **Inferential target**: Causal effect of neighborhood demographics (income, race, education, disability) on urban mobility patterns

### Method specification
- **Method name**: CRANE (Counterfactual RANdom-walks-based Embedding) + Propensity Score Matching (PSM)
- **Hyperparameters**: PSM: 5 treatment-level bins, ordinal regression for propensity scores; CRANE: 200,000 random walks per category, embedding dimension not explicitly stated in methods
- **Required validations**: Consistency check between CRANE embedding proximities and PSM treatment effects; within-city 80/20 train-test prediction of neighborhood accessibility
- **Characteristic outputs**: Treatment effect estimates per demographic feature per MSA; neighborhood-level embedding vectors; accessibility prediction models; POI category-demographic proximity visualization

### Planning pattern
- **Evidence count**: 6 distinct analytical results
- **Figure count**: 6 main, 0 ED, unspecified Supplementary
- **Evidence chain**: phenomenon detection (correlation) → confounding concern → causal identification (PSM) → counterfausal embedding (CRANE) → validation & prediction → spatial query application
- **Key figures**:
  - F1: PSM method schematic (3 panels) — treatment stratification, propensity score estimation, matching distance
  - F2: Counterfactual random walk illustration — POI sampling, neighborhood sampling, alternative outcome
  - F3: Treatment effects on mobility frequency & COVID reduction (multi-panel bar charts across 6 MSAs)
  - F4: Treatment effects on POI category accessibility (4 categories × 6 MSAs)
  - F5: CRANE convergence & embedding proximity visualization (2 panels)
  - F6: Spatial POI query application in Houston — income-based accessibility gap mapping
- **Narrative arc**: Correlation reveals potential inequality → confounding motivates causal method → PSM disentangles effects → CRANE scales PSM to network level → embeddings validate and predict → embeddings enable policy-relevant spatial queries
- **Central claim**: Prevalent accessibility gaps exist across income, race, and education dimensions in U.S. cities, measurable through counterfactual mobility network embeddings that disentangle confounding effects
- **Claim strength**: Quasi-causal

### Keywords
urban mobility, accessibility gap, propensity score matching, counterfactual, network embedding, causal inference, SafeGraph, neighborhood demographics, COVID-19 mobility reduction, POI accessibility, CRANE method, income inequality, racial gap
