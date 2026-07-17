# Climate Health Attribution

Methods for attributing health outcomes to climate change, combining temperature-mortality modeling with attribution frameworks.

## Mortality Attribution from Extreme Temperatures

- **Paper**: Attributing mortality from extreme temperatures to climate change in Stockholm, Sweden (Nature Climate Change, 2013)
- **DOI**: 10.1038/nclimate2022
- **Domain**: climate_health_attribution
- **Study design**: time_series
- **Outcome type**: count
- **Inferential target**: causal_effect

### Method specification
- **Method name**: Overdispersed Poisson GLM with smooth time trends and attribution formula
- **Hyperparameters**: smooth time trend with 120 degrees of freedom (4 df per year), cold threshold = 2nd percentile of 26-day moving average (lag0-25), heat threshold = 98th percentile of 2-day moving average (lag0-1)
- **Required validations**: decade-by-decade RR stability test, adaptation assessment (RR vs number of extremes regression), lag sensitivity analysis
- **Characteristic outputs**: relative risks of mortality from cold (5.6%, 95% CI: 2.9%, 8.2%) and heat (4.6%, 95% CI: 2.6%, 6.7%) extremes, attributed mortality counts (288 heat-attributable deaths, 95% CI: 161, 417)

### Planning pattern
- **Evidence count**: 4 distinct analytical results
- **Figure count**: 4 main, 0 Extended Data, 0 Supplementary
- **Evidence chain**: temperature distribution shift → mortality risk estimation → adaptation assessment → mortality attribution
- **Key figures**:
  - F1: establish (1 panel) — Winter temperature distribution shift between 1900-1929 and 1980-2009
  - F2: reveal (1 panel) — Summer temperature distribution shift showing more heat extremes
  - F3: quantify (1 panel) — Number of cold/heat extremes per decade over the century
  - F4: validate (1 panel) — Mortality relative risks by temperature extreme and age group
- **Narrative arc**: climate context → temperature evidence → risk quantification → adaptation check → attribution calculation
- **Central claim**: Mortality from heat extremes in Stockholm during 1980-2009 was double what would have occurred without climate change, with 288 excess deaths attributable to increased heat extreme frequency.
- **Claim strength**: quasi_causal

### Keywords
climate attribution, temperature mortality, extreme heat, extreme cold, Poisson regression, attributable mortality, adaptation assessment, urban heat island, Stockholm
