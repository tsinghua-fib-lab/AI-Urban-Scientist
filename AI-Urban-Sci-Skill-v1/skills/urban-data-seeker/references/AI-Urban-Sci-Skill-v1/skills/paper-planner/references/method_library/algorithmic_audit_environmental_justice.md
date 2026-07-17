# Algorithmic Audit & Environmental Justice

Entries on auditing, sensitivity analysis, and mitigation of algorithmic decision-making tools for environmental justice and resource allocation.

---

## CalEnviroScreen Algorithmic Audit: Sensitivity, Tradeoffs, and Adversarial Manipulability

- **Paper**: Mitigating allocative tradeoffs and harms in an environmental justice data tool (Nature Machine Intelligence, 2024)
- **DOI**: 10.1038/s42256-024-00793-y
- **Domain**: Algorithmic auditing, environmental justice, policy algorithm, fairness
- **Study design**: Algorithmic reproduction + sensitivity analysis + causal inference (regression discontinuity) + adversarial optimization
- **Outcome type**: Tract designation change percentage; funding impact (USD); racial/poverty composition shifts; adversarial optimization results by political party
- **Inferential target**: Sensitivity of CalEnviroScreen to subjective model specifications and consequences for funding allocation and subpopulation representation

### Method specification
- **Method name**: Full algorithm reproduction + alternative model specification grid (pre-processing × aggregation × health metrics) + sharp regression discontinuity design + Hooke-Jeeves adversarial optimization
- **Hyperparameters**: 8 alternative models varying: pre-processing (percentile ranking vs. z-score), aggregation (multiplication vs. arithmetic mean), health metrics (additional: survey asthma, COPD, chronic kidney disease, cancer); RD: Imbens-Kalyanaraman bandwidth selection, local linear regression; adversarial optimization: weights constrained [0.1, 0.9], optimizing demographic representation
- **Required validations**: RD robustness checks: varying bandwidths, functional forms, covariate adjustments, dataset configurations; propensity score matching; causal forest; reproduction validation against existing CalEnviroScreen data
- **Characteristic outputs**: Sensitivity range per tract (min/max percentile across models); funding impact estimates with 95% CI; racial composition shift tables; adversarial optimization flow diagrams; multi-model union sensitivity reduction percentages

### Planning pattern
- **Evidence count**: 4 distinct analytical results
- **Figure count**: 4 main, 0 ED, unspecified Supplementary
- **Evidence chain**: model reproduction → sensitivity analysis across specifications → causal funding impact estimation → allocative tradeoff analysis (race/poverty) → adversarial manipulability assessment → mitigation proposals
- **Key figures**:
  - F1: Model sensitivity — tract percentile ranges across alternative specifications with uncertainty bars at threshold
  - F2: Funding by CalEnviroScreen percentile — California Climate Investments 2017-2021, earmarked vs. non-earmarked
  - F3: Allocative tradeoffs — racial/poverty composition shift between current and alternative model among tracts changing designation
  - F4: Adversarial optimization — tract distribution by political party under optimized vs. baseline model
- **Narrative arc**: CalEnviroScreen reproduced → 16.1% of tracts could change designation from small model changes → designation confers $2.08B in additional funding → alternative model increases designation for minoritized populations in poverty but decreases overall minoritized representation → adversarial optimization shows 39% swing possible → mitigation: multi-model union reduces sensitivity 40.7%, three-model union 71%
- **Central claim**: Environmental justice screening algorithms are highly sensitive to subjective design choices, making them vulnerable to allocative harm and adversarial manipulation, but multi-model ensemble approaches can substantially reduce sensitivity
- **Claim strength**: Quasi-causal (regression discontinuity design for funding impact; observational for sensitivity analysis)

### Keywords
algorithmic audit, environmental justice, CalEnviroScreen, sensitivity analysis, regression discontinuity, adversarial optimization, allocative harm, model manipulability, composite indicator, environmental burden, census tract, disadvantaged community, California Climate Investments, fairness, policy algorithm
