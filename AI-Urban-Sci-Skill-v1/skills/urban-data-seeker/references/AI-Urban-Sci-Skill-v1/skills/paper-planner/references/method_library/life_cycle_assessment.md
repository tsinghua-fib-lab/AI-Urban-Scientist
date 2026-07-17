# Life Cycle Assessment

Methods for assessing life-cycle environmental impacts, energy use, and greenhouse gas emissions of technologies and systems.

## Drone Delivery Life Cycle Assessment

- **Paper**: Energy use and life cycle greenhouse gas emissions of drones for commercial package delivery (Nature Communications, 2018)
- **DOI**: 10.1038/s41467-017-02411-5
- **Domain**: life_cycle_assessment
- **Study design**: observational_cohort
- **Outcome type**: continuous
- **Inferential target**: distributional_pattern

### Method specification
- **Method name**: Analytical drone energy model (conservation of momentum) calibrated to flight data, with life-cycle GHG assessment using GREET model
- **Hyperparameters**: power efficiency eta=0.70 (high speed), eta=0.53 (low speed), CD_body=1.5, battery energy density 540 kJ/kg (LiPo), travel velocity 10 m/s, warehouse energy multiplier 2x base case
- **Required validations**: flight test calibration (1073 flight segments), sensitivity analysis across electricity carbon intensities, warehouse energy assumptions, package-per-km delivery rates, comparison across drone sizes (quadcopter vs octocopter)
- **Characteristic outputs**: energy use per distance (J/m), delivery range (~3.5 km quadcopter, ~4.2 km octocopter), life-cycle GHG emissions per package across delivery modes, sensitivity tornado diagrams

### Planning pattern
- **Evidence count**: 6 distinct analytical results
- **Figure count**: 6 main, 0 Extended Data, 0 Supplementary
- **Evidence chain**: energy model development → range estimation → energy comparison → emissions comparison → sensitivity analysis → policy implications
- **Key figures**:
  - F1: establish (2 panels) — Measured vs modeled energy use per distance at various velocities
  - F2: reveal (2 panels) — Range and energy use as function of battery size
  - F3: quantify (2 panels) — Hypothetical warehouse coverage maps for drone delivery
  - F4: reveal (1 panel) — Energy per km comparison across delivery vehicles
  - F5: quantify (1 panel) — Life-cycle GHG emissions per package across all delivery pathways
  - F6: validate (1 panel) — Sensitivity analysis tornado diagram
- **Narrative arc**: model formulation → empirical calibration → performance prediction → comparative assessment → sensitivity exploration → policy guidance
- **Central claim**: Small electric drones have lower life-cycle GHG emissions than conventional delivery trucks in most US regions, but additional warehousing requirements and electricity carbon intensity are critical determinants of environmental benefit.
- **Claim strength**: descriptive

### Keywords
life cycle assessment, drone delivery, energy model, greenhouse gas emissions, GREET, conservation of momentum, warehouse energy, package delivery, comparative LCA, sensitivity analysis
