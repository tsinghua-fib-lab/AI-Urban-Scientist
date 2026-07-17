# Urban Carbon Modeling

Entries for papers quantifying urban carbon emissions at building or city scale using life cycle assessment, archetype modeling, and simulation frameworks.

---

## urban_embodied_carbon_LCA_simulation

- **Paper**: A systematic framework to reduce urban embodied carbon emissions using urban scale simulation (npj Urban Sustainability, 2025)
- **DOI**: 10.1038/s42949-025-00196-x
- **Domain**: urban_carbon_modeling
- **Study design**: cross_sectional
- **Outcome type**: continuous
- **Inferential target**: distributional_pattern

### Method specification
- **Method name**: Bottom-up urban life cycle assessment (LCA) via building archetypes + Monte Carlo simulation
- **Hyperparameters**:
  - Building stock dataset: National Structure Inventory (NSI) + Cook County Open Data merged by geocoordinates; 1,010,840 buildings; variables: structure type, foundation type, square footage, floors, wall materials, roof materials, HVAC systems, geocoordinates, year built
  - Archetype creation: 157 archetypes (S-F-WW-RR naming: structure-foundation-wall-roof combinations) representing 1M+ buildings; each archetype modeled as 1000 SQF, single-story in Athena
  - LCA: Athena Impact Estimator v5.5; cradle-to-grave boundary (stages A-C, excluding operational carbon stage B); outputs: GWP (kg CO2 eq/m²), acidification (kg SO2 eq/m²), eutrophication (kg PO4 eq/m²), HH particulate (PM2.5 eq/m²), ozone depletion (CFC eq/m²), smog formation (kg O3 eq/m²)
  - Simulation: 350,000 iterations; lifespan range 50-80 years (4 thresholds: 50, 60, 70, 80); area change scenarios; 50,000 building sample for computation efficiency (actual city values ~20x stated numbers); uniform distribution across scenario variables
  - Scaling: Athena results scaled per 1000 SQF to match individual building floor area and story count
- **Required validations**: Uniform distribution verification (mean of each variable at midpoint of range); iteration count per lifespan threshold (~87,500 each); comparison of new construction vs. renovation emissions (7,500x difference)
- **Characteristic outputs**: Per-building embodied carbon estimates; emission statistics by building characteristics; scenario-based emission change distributions; lifespan-emission trade-off analysis; renovation vs. new construction emission comparison; demolition scenario turnover analysis

### Planning pattern
- **Evidence count**: 4 distinct analytical results
- **Figure count**: 8 main, 0 Extended Data, Supplementary tables/figures present
- **Evidence chain**: dataset creation -> archetype LCA -> scenario simulation -> policy recommendation
- **Key figures**:
  - F1: establish (multi-panel) — Chicago building stock status: land coverage, year built, floors, structure type, envelope type
  - F2: quantify (multi-panel) — Simulation results: emission distributions across 350,000 iterations
  - F3: reveal (multi-panel) — Lifespan-emission relationship and turnover analysis
  - F4: quantify (multi-panel) — Area change scenarios and emission impact
  - F5: expose_response (multi-panel) — Turnover average changes per lifespan and area changes for demolition scenarios
  - F6-F8: reveal/extend (multi-panel each) — Additional scenario analyses and sensitivity results
- **Narrative arc**: Building stock dataset creation -> Archetype definition (157 types) -> Athena LCA per archetype -> Geo-assignment to Chicago buildings -> 350,000-iteration simulation -> Lifespan and area sensitivity -> Policy recommendation (renovation over new construction)
- **Central claim**: Buildings with 50-year lifespans emit 3x more CO2 than those lasting 80 years, and a 20% change in building area can negate longevity benefits, demonstrating that renovation strategies to extend building lifespans should be prioritized over new construction for urban embodied carbon reduction.
- **Claim strength**: quasi_causal (simulation-based counterfactual)

### Keywords
life cycle assessment, embodied carbon, building archetypes, Athena Impact Estimator, Monte Carlo simulation, urban carbon, bottom-up approach, building stock, renovation, lifespan, Chicago, construction policy, GWP
