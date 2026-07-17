# Urban & Regional Planning

Methods and patterns for city-region delineation, urban activity classification, and spatial planning analysis.

---

## Multi-tier City-Region Delineation

- **Paper**: Worldwide delineation of multi-tier city-regions (Nature Cities, 2024)
- **DOI**: 10.1038/s44284-024-00083-z
- **Domain**: urban_regional_planning
- **Study design**: spatial (global)
- **Outcome type**: categorical (city-region tier classification)
- **Inferential target**: classification

### Method specification
- **Method name**: Travel-time catchment area method for city-region delineation
- **Hyperparameters**: Travel-time threshold parameters, catchment area boundary definitions, population threshold for urban center identification (50,000+), tier classification criteria (4 tiers), spatial resolution of travel-time surface
- **Required validations**: Catchment area boundary sensitivity, travel-time surface accuracy, tier classification robustness, cross-validation of urban center identification, global coverage completeness assessment
- **Characteristic outputs**: 30,079 urban centers classified into 4 tiers, global city-region boundary maps, catchment area population estimates, tier distribution statistics

### Planning pattern
- **Evidence count**: 4 distinct analytical results
- **Figure count**: 4 main, Extended Data present, Supplementary present
- **Evidence chain**: urban center identification -> travel-time catchment computation -> tier classification -> global pattern analysis
- **Key figures**:
  - F1: establish (multiple panels) - Global distribution of urban centers and methodology overview
  - F2: quantify (multiple panels) - Travel-time catchment area delineation method and results
  - F3: reveal (multiple panels) - Four-tier city-region classification and global distribution
  - F4: synthesize (multiple panels) - Cross-tier comparisons and planning implications
- **Narrative arc**: method development -> global application -> tier classification -> comparative analysis -> planning relevance
- **Central claim**: A travel-time catchment area method produces a globally consistent delineation of 30,079 urban centers into four tiers of city-regions, revealing the hierarchical structure of urban systems worldwide.
- **Claim strength**: descriptive

### Keywords
city-region delineation, travel-time catchment, urban centers, multi-tier classification, global urban system, spatial planning, urban hierarchy, catchment area, 30079 urban centers, four-tier classification

---

## Activity Typology over a Century of Urban Growth

- **Paper**: A typology of activities over a century of urban growth (Nature Cities, 2024)
- **DOI**: 10.1038/s44284-024-00108-7
- **Domain**: urban_regional_planning
- **Study design**: geohistorical (longitudinal)
- **Outcome type**: categorical (activity type) + count (establishment counts)
- **Inferential target**: association

### Method specification
- **Method name**: Geohistorical directory analysis with population scaling regression (linear, sublinear, superlinear)
- **Hyperparameters**: NAICS-inspired activity categorization parameters, population scaling exponent fitting parameters, time-window aggregation parameters (1829-1907, Paris), historical perturbation identification parameters
- **Required validations**: Directory data completeness assessment, categorization consistency over time, scaling law fit quality, historical perturbation attribution robustness
- **Characteristic outputs**: Activity scaling exponents (linear, sublinear, superlinear), activity type classification by scaling behavior, temporal activity dynamics over ~80 years, perturbation sensitivity analysis

### Planning pattern
- **Evidence count**: 3 distinct analytical results
- **Figure count**: 3 main, 0 Extended Data, 10 Supplementary figures, 4 Supplementary tables
- **Evidence chain**: geohistorical database construction -> activity scaling analysis -> typology classification -> perturbation sensitivity
- **Key figures**:
  - F1: establish (multiple panels) - Geohistorical database construction and Paris activity landscape 1829-1907
  - F2: quantify (multiple panels) - Population scaling relationships: linear, sublinear, superlinear activity categories
  - F3: reveal (multiple panels) - Activity dynamics sensitivity to historical perturbations (public works, political conflicts)
- **Narrative arc**: data construction -> scaling analysis -> typology discovery -> historical perturbation analysis -> urban growth theory
- **Central claim**: Urban activities can be classified into three scaling categories with population: linear (everyday needs), sublinear (public services), and superlinear (specialization/passing fads), and these dynamics are sensitive to historical perturbations such as large-scale public works or political conflicts.
- **Claim strength**: descriptive

### Keywords
activity typology, urban scaling, geohistorical data, historical directories, Paris 1829-1907, population scaling, superlinear, sublinear, linear scaling, urban growth, NAICS classification, historical perturbation

---

## Sustainable Dining Accessibility in Tokyo

- **Paper**: Disparities in access to sustainable dining options across the Tokyo Metropolis (Nature Cities, 2025)
- **DOI**: 10.1038/s44284-025-00235-9
- **Domain**: urban_regional_planning
- **Study design**: cross-sectional (spatial analysis)
- **Outcome type**: composite index (sustainable dining accessibility)
- **Inferential target**: association

### Method specification
- **Method name**: Integrated multi-dimensional sustainability assessment framework (economic preferences + environmental supply-chain impacts + nutritional quality) + spatial accessibility analysis
- **Hyperparameters**: 3,649 menu item classification parameters, 112,892 restaurant geocoding parameters, railway station buffer distance parameters, 3EID embodied energy/emission intensity parameters, nutritional scoring parameters, economic preference weighting parameters, Gini/inequality index parameters
- **Required validations**: Restaurant clustering validation around railway stations, sustainability dimension weighting sensitivity, spatial accessibility measure robustness, inequality metric validation, ward-level aggregation accuracy
- **Characteristic outputs**: Restaurant spatial clustering patterns around transit nodes, multi-dimensional sustainability scores by restaurant, accessibility inequality maps across station vicinities/railway lines/administrative wards, passenger exposure estimates (up to 9 million daily passengers)

### Planning pattern
- **Evidence count**: 5 distinct analytical results
- **Figure count**: 5 main (plus Figure 6 in source data), Extended Data present, 13 Supplementary figures, 8 Supplementary tables
- **Evidence chain**: transit-oriented restaurant clustering -> multi-dimensional sustainability scoring -> spatial accessibility mapping -> inequality quantification -> targeted intervention proposal
- **Key figures**:
  - F1: establish (multiple panels) - Restaurant distribution and clustering around railway stations in Tokyo
  - F2: quantify (multiple panels) - Multi-dimensional sustainability assessment framework (economic, environmental, nutritional)
  - F3: reveal (multiple panels) - Sustainable dining accessibility patterns across station vicinities
  - F4: compare (multiple panels) - Inequality across railway lines and administrative wards
  - F5: synthesize (multiple panels) - Population exposure to unsustainable dining environments and intervention scenarios
- **Narrative arc**: spatial pattern discovery -> sustainability framework construction -> accessibility assessment -> inequality quantification -> intervention design
- **Central claim**: Severe inequalities exist in sustainable dining accessibility across Tokyo's station vicinities, railway lines, and administrative wards, with up to 9 million daily passengers exposed to unsustainable dining environments, requiring targeted spatial distribution interventions.
- **Claim strength**: descriptive

### Keywords
sustainable dining, food accessibility, transit-oriented development, Tokyo, restaurant clustering, multi-dimensional sustainability, supply-chain emissions, nutritional quality, spatial inequality, railway stations, 3EID database, urban food systems
