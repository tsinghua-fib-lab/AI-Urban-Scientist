# Urban Soil & Carbon

Methods and patterns for studying urban soil properties, carbon dynamics, and land-cover change impacts on soil ecology.

---

## Impervious Surface Impacts on Soil Organic Carbon

- **Paper**: Impacts of impervious surface expansion on soil organic carbon (Scientific Reports, 2015)
- **DOI**: 10.1038/srep17905
- **Domain**: urban_soil_carbon
- **Study design**: field_sampling (spatial)
- **Outcome type**: continuous (SOC concentration)
- **Inferential target**: association

### Method specification
- **Method name**: Field soil pit sampling + Landsat TM Linear Spectral Mixture Analysis (LSMA) impervious surface classification
- **Hyperparameters**: Soil pit sampling grid parameters, LSMA endmember selection and unmixing parameters, impervious surface fraction classification thresholds, spatial resolution parameters
- **Required validations**: LSMA classification accuracy assessment, soil sampling representativeness, SOC measurement quality control, spatial interpolation validation
- **Characteristic outputs**: Impervious surface fraction maps, soil organic carbon (SOC) concentration by impervious surface coverage level, SOC depletion estimates associated with urbanization

### Planning pattern
- **Evidence count**: 3 distinct analytical results
- **Figure count**: 3 main, 0 Extended Data, Supplementary present
- **Evidence chain**: impervious surface mapping -> field soil sampling -> SOC-impervious surface association quantification
- **Key figures**:
  - F1: establish (multiple panels) - Impervious surface classification and spatial distribution from Landsat TM LSMA
  - F2: quantify (multiple panels) - Field soil pit sampling design and SOC measurements
  - F3: reveal (multiple panels) - SOC concentration patterns by impervious surface coverage level
- **Narrative arc**: remote sensing classification -> field validation sampling -> association analysis -> urbanization impact quantification
- **Central claim**: Impervious surface expansion associated with urbanization significantly affects soil organic carbon concentrations, with measurable depletion patterns linked to increasing surface sealing.
- **Claim strength**: suggestive (observational field sampling with remote sensing classification)

### Keywords
soil organic carbon, impervious surface, LSMA, linear spectral mixture analysis, Landsat TM, soil pit sampling, urbanization impact, soil carbon depletion, land-cover change, remote sensing
