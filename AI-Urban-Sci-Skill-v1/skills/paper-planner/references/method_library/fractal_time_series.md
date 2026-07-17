# Fractal Time Series

Methods for analyzing long-range correlations, fractal properties, and scaling behavior in time series data.

## Food Safety Incident Fractal Analysis

- **Paper**: Food safety incidents in Beijing: occurrence patterns, causes and wider social implications (Humanities and Social Sciences Communications, 2015)
- **DOI**: 10.1057/palcomms.2015.29
- **Domain**: fractal_time_series
- **Study design**: time_series
- **Outcome type**: count
- **Inferential target**: distributional_pattern

### Method specification
- **Method name**: Detrended Fluctuation Analysis (DFA) and Adaptive Fractal Analysis (AFA) for Hurst parameter estimation
- **Hyperparameters**: Hurst parameter H=0.65 (average of DFA and AFA), window sizes for DFA segmentation and AFA trend fitting
- **Required validations**: distributional fit comparison (exponential vs power-law CCDF), DFA/AFA consistency check, trend removal sensitivity (detrended H=0.645 vs original H=0.645)
- **Characteristic outputs**: Hurst parameter H=0.65 indicating persistent long-range correlations, power-law CCDF (R^2=0.985 reported, 0.979 actual), burst-pattern identification in inter-event intervals

### Planning pattern
- **Evidence count**: 4 distinct analytical results
- **Figure count**: 4 main, 0 Extended Data, 0 Supplementary
- **Evidence chain**: incident data collection → distributional analysis (non-Poissonian) → fractal analysis (long-range correlations) → mechanism interpretation
- **Key figures**:
  - F1: establish (1 panel) — Monthly number of food safety incidents over 10-year period
  - F2: reveal (2 panels) — Inter-event interval time series showing burst patterns (reported vs actual)
  - F3: quantify (2 panels) — Log-log CCDF plots confirming power-law behavior
  - F4: validate (2 panels) — DFA and AFA fractal analysis yielding consistent Hurst parameter estimates
- **Narrative arc**: data presentation → distributional characterization → fractal scaling → mechanism scenarios → policy implications
- **Central claim**: Food safety incidents in Beijing occur in bursts with persistent long-range correlations (H=0.65), suggesting systemic rather than stochastic causes linked to government enforcement cycles.
- **Claim strength**: descriptive

### Keywords
fractal analysis, DFA, AFA, Hurst parameter, long-range correlation, time series, inter-event interval, food safety, burst pattern, power law, Poisson process
