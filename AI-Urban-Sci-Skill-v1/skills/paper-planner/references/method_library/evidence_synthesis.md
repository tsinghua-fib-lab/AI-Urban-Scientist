# Evidence Synthesis

Methods and patterns for systematic literature mapping, evidence gap identification, and AI-assisted evidence synthesis.

---

## Systematic Global Stocktake of Urban Climate Studies

- **Paper**: Systematic global stocktake of over 50,000 urban climate change studies (Nature Cities, 2025)
- **DOI**: 10.1038/s44284-025-00260-8
- **Domain**: evidence_synthesis
- **Study design**: systematic_mapping (AI-enhanced)
- **Outcome type**: categorical (topic classification) + count (study counts)
- **Inferential target**: mapping

### Method specification
- **Method name**: AI-enhanced systematic evidence mapping pipeline: XGBoost supervised classifier + Mordecai geoparser + structural topic modeling (STM) + fuzzy-reference matching
- **Hyperparameters**: XGBoost classifier hyperparameters (tree depth, learning rate, loss reduction, minimal node size, sample size, number of randomly sampled predictors at each split, number of trees, iterations without improvement until stop, prediction probability threshold), nested cross-validation with 5 outer and 5 inner folds, topic model with 220 topics, keyword query parameters for OpenAlex database, geoparser validation parameters (600-article ground truth sample), city name keyword match from GHSL-UCDB (>13,000 city names), review identification keyword parameters
- **Required validations**: Classifier performance (F1=0.952 out-of-sample), geoparser accuracy (recall=0.85, precision=0.74, F1=0.79 for combined approach), topic model granularity assessment, IPCC reference fuzzy-match accuracy (OpenAlex coverage of 92.6% of IPCC references), review coverage estimation accuracy
- **Characteristic outputs**: 53,295 classified urban climate studies database, 19,733 spatially specific city case studies, 33,562 generic urban climate studies, 220 structural topics grouped into WG themes, geographic bias maps, IPCC coverage analysis (2,421 urban studies in AR6 = 4.6% of landscape)

### Planning pattern
- **Evidence count**: 5 distinct analytical results
- **Figure count**: 5 main, 7 Extended Data figures, Supplementary present
- **Evidence chain**: literature identification and classification -> spatial case study extraction -> geographic bias quantification -> topic modeling -> IPCC coverage comparison
- **Key figures**:
  - F1: establish (multiple panels) - Growth and volume of urban climate change literature (53,295 studies)
  - F2: quantify (multiple panels) - Global spatial distribution of city case studies and geographic bias patterns
  - F3: reveal (multiple panels) - Topic modeling results: thematic coverage across IPCC WG domains
  - F4: compare (multiple panels) - IPCC AR6 coverage vs wider literature (4.6% direct, 2.1% second-order)
  - F5: synthesize (multiple panels) - Review coverage relationships and IPCC uptake patterns
- **Narrative arc**: database construction -> scale revelation -> geographic bias discovery -> thematic richness -> assessment gap identification -> synthesis recommendation
- **Central claim**: A systematic AI-enhanced stocktake identifies 53,295 urban climate studies revealing rapid growth, severe geographic bias toward the Global North and large cities, and limited IPCC coverage (4.6%), requiring coordinated evidence synthesis efforts.
- **Claim strength**: descriptive

### Keywords
systematic mapping, evidence synthesis, XGBoost classifier, structural topic modeling, geoparsing, Mordecai, OpenAlex, urban climate change, IPCC coverage, evidence gap, AI-assisted screening, living database, Global South bias, case study synthesis, 53295 studies
