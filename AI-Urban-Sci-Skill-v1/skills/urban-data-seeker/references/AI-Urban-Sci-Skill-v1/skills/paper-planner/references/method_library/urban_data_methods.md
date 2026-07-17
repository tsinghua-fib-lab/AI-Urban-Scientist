# Urban Data Methods

Computational methods for urban data quality assessment, crowdsourcing analytics, and urban sensing.

---

## Crowdsourcing Under-reporting Delay Estimation

- **Paper**: Quantifying spatial under-reporting disparities in resident crowdsourcing (Nature Computational Science, 2023)
- **DOI**: 10.1038/s43588-023-00572-6
- **Domain**: urban_data_methods
- **Study design**: observational (crowdsourced data analysis)
- **Outcome type**: count (report events, delay time)
- **Inferential target**: association

### Method specification
- **Method name**: Zero-inflated Bayesian Poisson regression + duplicate report analysis method for reporting delay estimation
- **Hyperparameters**: Zero-inflation parameters, Poisson regression rate parameters, Bayesian prior specifications, duplicate detection time-window parameters, spatial resolution parameters
- **Required validations**: Duplicate identification accuracy, zero-inflation model fit assessment, spatial autocorrelation check, reporting delay distribution validation, sensitivity to duplicate detection threshold
- **Characteristic outputs**: Spatial maps of under-reporting disparities, reporting delay distributions by area, zero-inflation rate estimates, duplicate report frequency patterns

### Planning pattern
- **Evidence count**: 3 distinct analytical results
- **Figure count**: 3 main, 0 Extended Data, Supplementary present
- **Evidence chain**: reporting pattern characterization -> duplicate-based delay estimation -> spatial disparity mapping
- **Key figures**:
  - F1: establish (multiple panels) - Crowdsourced reporting patterns and spatial distribution
  - F2: quantify (multiple panels) - Duplicate report analysis and delay estimation methodology
  - F3: reveal (multiple panels) - Spatial under-reporting disparities and their correlates
- **Narrative arc**: data characterization -> methodological innovation (duplicate-based delay estimation) -> spatial disparity discovery -> equity implication
- **Central claim**: Duplicate report analysis reveals systematic spatial disparities in crowdsourced reporting delays, with under-reporting concentrated in specific areas, indicating inequities in civic data quality.
- **Claim strength**: suggestive (observational crowdsourced data with novel duplicate-based method)

### Keywords
crowdsourcing, under-reporting, reporting delay, zero-inflated Poisson, Bayesian regression, duplicate analysis, civic data, spatial disparity, urban sensing, data quality
