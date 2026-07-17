# Satellite Emission Monitoring

Methods for detecting and quantifying greenhouse gas emissions using satellite remote sensing, plume detection, and inverse modeling.

## Landfill Methane Emission Satellite Monitoring

- **Paper**: Reduction of methane emissions through improved landfill management (Nature Climate Change, 2025)
- **DOI**: 10.1038/s41558-025-02391-1
- **Domain**: satellite_emission_monitoring
- **Study design**: observational_cohort
- **Outcome type**: rate
- **Inferential target**: association

### Method specification
- **Method name**: Satellite plume detection (TROPOMI, PRISMA) with methane emission quantification and inventory comparison
- **Hyperparameters**: 5 years of satellite observations, 102 high-emitting landfills worldwide, EDGAR v8.0 inventory comparison baseline
- **Required validations**: cross-validation with airborne measurements (AVIRIS-NG, Carbon Mapper), comparison with US EPA GHGRP inventory, BAAQMD validation, spatial plume clustering for emission event identification
- **Characteristic outputs**: methane plume spatial distributions from hyperspectral remote sensing, emission rates per landfill, open dump vs sanitary landfill comparison (5.3x underestimation in EDGAR), mitigation potential estimates (80% reduction, 760 Mt CO2e annually)

### Planning pattern
- **Evidence count**: 4 distinct analytical results
- **Figure count**: 4 main, 5 Extended Data, 0 Supplementary
- **Evidence chain**: satellite detection → emission quantification → inventory comparison → mitigation potential estimation
- **Key figures**:
  - F1: establish (multiple panels) — Global distribution of 102 monitored landfills and detection methodology
  - F2: quantify (multiple panels) — Methane emission rates from satellite plume detection
  - F3: reveal (multiple panels) — Comparison between satellite measurements and inventory estimates
  - F4: extend (multiple panels) — Mitigation potential under improved waste management scenarios
- **Narrative arc**: detection framework → quantification results → inventory validation → mitigation pathways → policy implications
- **Central claim**: Open dumpsite methane emissions are underestimated by 5.3x in current inventories, and transforming open dumpsites to sanitary landfills with organic waste diversion can reduce emissions by 80%, offering 760 Mt CO2e annual mitigation potential.
- **Claim strength**: suggestive

### Keywords
satellite remote sensing, methane emission, TROPOMI, PRISMA, plume detection, landfill, EDGAR inventory, inverse modeling, emission quantification, waste management mitigation
