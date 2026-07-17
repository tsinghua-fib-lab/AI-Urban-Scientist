# Spatial Analysis / Geostatistical Methods

Methods for analyzing spatial patterns, spatial autocorrelation, and spatially varying relationships. Includes exploratory spatial data analysis (Moran's I, LISA), Geographically Weighted Regression (GWR), and kernel density estimation.

---

## Exploratory spatial data analysis + Geographically Weighted Regression (carbon emissions in resource-based cities)

- **Paper**: Determinants and their spatial heterogeneity of carbon emissions in resource-based cities, China (Scientific Reports, 2024)
- **DOI**: 10.1038/s41598-024-56434-2
- **Domain**: Carbon emissions, urban geography
- **Study design**: Cross-sectional spatial analysis with temporal comparison (2003-2017)
- **Outcome type**: City-level carbon emissions (from CEADs database)
- **Inferential target**: Spatial patterns and heterogeneous effects of population, economy, technology, and industry on carbon emissions

### Method specification
- **Method name**: Exploratory spatial data analysis (Moran's I) + Geographically Weighted Regression (GWR)
- **Hyperparameters**: 113 prefecture-level resource-based cities in China, 2003-2017; 4 predictors: permanent population, per capita GDP, proportion of resource-based industries (mining workers / total workers), carbon abatement technology (carbon intensity); adaptive spatial kernel with Gaussian model; AICc for optimal bandwidth selection
- **Required validations**: GWR vs OLS model comparison (AICc, adjusted R2); global Moran's I for spatial autocorrelation; local Moran's I and LISA agglomeration for local clustering; Mann-Kendall trend test for peak carbon detection; Theil indices for spatial disparities
- **Characteristic outputs**: Global Moran's I values (declining from 0.409 to 0.389); LISA clustering maps (high-high, low-low); GWR regression coefficient maps for each predictor across 4 time points; model fit comparison tables (GWR superior to OLS on AICc and adjusted R2)

### Planning pattern
- **Evidence count**: 4 analytical results in empirical analysis
- **Figure count**: 12 main figures
- **Evidence chain**: temporal trends (emissions growth, plateau since 2011) -> spatial patterns (northeast high, southwest low) -> spatial autocorrelation (global + local Moran's I, LISA) -> GWR vs OLS comparison -> factor-specific spatial coefficient maps (population, economy, technology, industry) -> summary
- **Key figures**:
  - F1: Study area map (113 resource-based cities)
  - F2-F6: Temporal characteristics — emissions trends, RBC vs non-RBC comparison, regional shares, city-type shares, Mann-Kendall test
  - F7-F8: Spatial distribution maps and LISA agglomeration / Moran scatter plots
  - F9-F12: GWR regression coefficient maps for each of the 4 predictors across 4 years
- **Narrative arc**: gap (resource-based cities overlooked in climate policy) -> temporal analysis (emissions growing, not yet peaked) -> spatial pattern (northeast high, southwest low) -> spatial autocorrelation confirmed -> GWR shows spatial heterogeneity -> four factor analyses with maps -> policy implications for differentiated approaches
- **Central claim**: Population size, economic development level, carbon abatement technology, and proportion of resource-based industries all contribute to carbon emissions in resource-based cities, with carbon abatement technology playing the predominant role and effects showing significant spatial heterogeneity.
- **Claim strength**: Descriptive / suggestive

### Keywords
Geographically Weighted Regression, GWR, Moran's I, LISA, spatial autocorrelation, carbon emissions, resource-based cities, spatial heterogeneity, exploratory spatial data analysis, OLS comparison, AICc, Theil index, Mann-Kendall test
