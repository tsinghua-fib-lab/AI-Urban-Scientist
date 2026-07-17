# Environmental Epidemiology

Entries for papers examining associations between environmental exposures (greenness, air quality, temperature, etc.) and health outcomes using cohort studies, multi-state models, and survival analysis.

---

## greenness_cardiometabolic_multimorbidity_multistate

- **Paper**: Residential greenness and trajectories of cardiometabolic multimorbidity: a prospective cohort study (npj Urban Sustainability, 2025)
- **DOI**: 10.1038/s42949-025-00201-3
- **Domain**: environmental_epidemiology
- **Study design**: observational_cohort
- **Outcome type**: time_to_event
- **Inferential target**: association

### Method specification
- **Method name**: Multi-state Cox proportional hazard models + restricted cubic splines (RCS) for exposure-response curves
- **Hyperparameters**:
  - Cohort: UK Biobank; 454,777 participants aged 40-69 at baseline (2006-2010); median follow-up 12.1 years; exclusions: incomplete greenspace data (n=5,152), prevalent CMDs at baseline (T2D: 13,417; IHD: 23,402; stroke: 5,732)
  - Exposure: NDVI from MODIS 16-day, 250m resolution; summer images 2006-2010 (cloud/snow removed); NDVI restricted to > 0; averaged within 300m, 500m, 1000m, 1500m buffers around registered addresses
  - Multi-state model states: Baseline (healthy) -> First CMD (FCMD: T2D/IHD/stroke) -> Cardiometabolic Multimorbidity (CMM: >= 2 CMDs) -> Death
  - Transitions modeled: Baseline->FCMD, Baseline->Death, FCMD->CMM, FCMD->Death, CMM->Death, and disease-specific transitions (e.g., T2D->CMM, IHD->CMM, IHD->Death)
  - Covariates: age, gender, ethnicity, employment status, education, income, urban/rural residence, healthy diet score (0-7), alcohol, smoking; confounder selection via DAGitty directed acyclic graphs
  - RCS: restricted cubic splines for monotonic exposure-response curves
  - Sensitivity analyses: multiple alternative model specifications (Tables S5-S10)
  - Subgroup analyses: by gender, urban/rural residence
- **Required validations**: Proportional hazards assumption; DAG-based confounder identification; sensitivity analyses with alternative specifications; subgroup analysis for effect modification; multi-buffer consistency (300m-1500m)
- **Characteristic outputs**: Hazard ratios per IQR NDVI increment for each transition; disease-specific transition HRs (T2D, IHD, stroke); exposure-response curves (RCS); subgroup-stratified estimates; sensitivity analysis results

### Planning pattern
- **Evidence count**: 4 distinct analytical results
- **Figure count**: 4 main, 0 Extended Data, Supplementary figures/tables present
- **Evidence chain**: cohort description -> conventional Cox -> multi-state analysis -> disease-specific transitions -> sensitivity/subgroup validation
- **Key figures**:
  - F1: establish (1 panel) — Multi-state model diagram and participant flow (baseline -> FCMD -> CMM -> death)
  - F2: quantify (1 panel) — Disease-specific transition counts (T2D, IHD, stroke pathways)
  - F3: expose_response (multi-panel) — Exposure-response curves (RCS) between greenness and diverse transitions
  - F4: quantify (multi-panel) — Associations of greenness with transitions from baseline to single CMD, CMM, and all-cause death
- **Narrative arc**: Cohort description -> Descriptive statistics -> Conventional Cox (greenness vs. FCMD/CMM/death) -> Multi-state model (transition-specific HRs) -> RCS exposure-response curves -> Disease-specific transitions -> Subgroup analyses -> Sensitivity analyses -> Conclusion
- **Central claim**: Residential greenness is significantly associated with transitions from healthy to first cardiometabolic disease, from FCMD to CMM, and from both states to death, with effects varying across disease-specific pathways (strongest for T2D transitions and IHD-to-CMM/death), suggesting greenness impacts CMM occurrence, progression, and prognosis.
- **Claim strength**: suggestive

### Keywords
greenness, NDVI, cardiometabolic multimorbidity, multi-state model, Cox regression, restricted cubic splines, UK Biobank, prospective cohort, T2D, IHD, stroke, exposure-response, DAG, survival analysis
