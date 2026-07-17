# Environmental Survey / Questionnaire-Based Assessment

Methods using questionnaire-based surveys and established emission/conversion factors to quantify environmental impacts of human activities at population scale. Includes nonparametric statistical testing and national extrapolation.

---

## Questionnaire-based survey + DEFRA GHG conversion factors (spectator travel to football)

- **Paper**: Greenhouse gas emissions as a result of spectators travelling to football in England (Scientific Reports, 2017)
- **DOI**: 10.1038/s41598-017-06141-y
- **Domain**: Sports environmental impact, transport emissions
- **Study design**: Cross-sectional questionnaire survey with national extrapolation
- **Outcome type**: Greenhouse gas emissions (kgCO2e per spectator)
- **Inferential target**: Differences in travel-related GHG emissions across football tiers and between home/away spectators

### Method specification
- **Method name**: Questionnaire-based survey + DEFRA GHG conversion factors
- **Hyperparameters**: N=1,649 participants across 8 football tiers (tiers 3-10) in Essex, England; survey period: February 2012 to March 2013; DEFRA 2012 conversion factors for CO2, CH4, N2O (converted to CO2e using GWP); travel modes: walking, cycling, car, bus, train, taxi; power analysis: GPower 3.1, one-way ANOVA, 8 groups, medium effect size, 95% power -> required N=360
- **Required validations**: Normality test (failed, leading to nonparametric tests); Kruskal-Wallis test for 8-tier comparison; Mann-Whitney U test for home vs away comparison; pairwise comparisons with adjusted p-values; statistical power verification (achieved N=1,649 provides 100% power)
- **Characteristic outputs**: Mean GHG emissions per spectator overall and by tier; tier-by-tier Kruskal-Wallis results; home vs away comparison; national extrapolation (linear) to 56,237 tonnes CO2e; travel mode distribution

### Planning pattern
- **Evidence count**: 3 analytical results (tier comparison, home vs away, national extrapolation)
- **Figure count**: 3 main figures
- **Evidence chain**: survey design and participant characterization -> distance/mode characterization -> tier comparison (Kruskal-Wallis) -> home vs away (Mann-Whitney U) -> national extrapolation
- **Key figures**:
  - F1: Travel mode distribution across football tiers — stacked bar chart showing car dominance (67.5%)
  - F2: Mean GHG emissions per spectator across 8 tiers with error bars
  - F3: League vs non-league GHG emission comparison
- **Narrative arc**: gap (lower-echelon football GHG emissions unstudied) -> survey methodology (1,649 participants, 8 tiers) -> travel mode characterization (car-dominated) -> significant tier differences -> away fans emit more than home fans -> national extrapolation (56,237 tonnes CO2e, <0.05% of transport) -> policy recommendations
- **Central claim**: Significant differences exist in travel-related GHG emissions across football tiers, with league-level emissions approximately four times higher than non-league, and away fans emitting significantly more than home fans; the extrapolated annual total is 56,237 tonnes CO2e.
- **Claim strength**: Descriptive

### Keywords
questionnaire survey, DEFRA conversion factors, GHG emissions, CO2e, Kruskal-Wallis, Mann-Whitney U, football spectators, travel emissions, national extrapolation, nonparametric tests, sports environmental impact, transport behavior
