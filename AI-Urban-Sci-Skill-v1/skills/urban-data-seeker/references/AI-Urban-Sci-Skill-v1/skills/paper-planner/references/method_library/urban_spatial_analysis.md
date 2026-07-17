# Urban Spatial Analysis

Entries for papers using satellite imagery, remote sensing, computer vision, and spatial classification to analyze urban form, land use, and settlement patterns.

---

## underload_city_LCC_assessment

- **Paper**: Underload city conceptual approach extending ghost city studies (npj Urban Sustainability, 2022)
- **DOI**: 10.1038/s42949-022-00057-x
- **Domain**: urban_spatial_analysis
- **Study design**: cross_sectional
- **Outcome type**: rate
- **Inferential target**: distributional_pattern

### Method specification
- **Method name**: Land Carrying Capacity (LCC) estimation via Stacked Auto-Encoder (SAE) + Ordinary Least Squares (OLS)
- **Hyperparameters**:
  - Multilevel semantic segmentation (MSS): segmentation scale = 50; DenseNet + 4 dilated convolutions (kernels: 1x1, 3x3, 3x3, 3x3; dilated rates: 1, 6, 12, 18); Adam optimizer, learning rate = 2e-4; L2 regularization; cross entropy loss; 50,000 training iterations; patch size 512x512; 70/30 train-test split (84,730 labeled samples)
  - SAE: 3 hidden layers (dimensions 32, 16, 8); batch size = 16; each AE trained 150 iterations; fine-tuning 500 iterations; sigmoid activation; reduces 64 LFS indices to 8 dimensions
  - Density Peaks Clustering Algorithm (DPCA): cluster center selection criteria rho >= 7, delta >= 0.5; Euclidean distance in combined functional/structural/thematic index space
- **Required validations**: Pixel-wise confusion matrix (OA = 85.0%, Kappa = 0.82 on 25,419 test samples); DPCA cluster center detection via rho-delta decision plot; comparison of LCC-based classification vs. population-density-based ghost city identification
- **Characteristic outputs**: 12-class land functional zone maps at 2.4 m resolution; 6 LFS city types; LCC estimates for population and GDP per city; Land Carrying Rate (LCR) classification (underload/slightly underload/well-balanced/slightly overload/overload)

### Planning pattern
- **Evidence count**: 4 distinct analytical results
- **Figure count**: 6 main, 0 Extended Data, ~7 Supplementary
- **Evidence chain**: phenomenon (imbalanced growth) -> method (VHR mapping + LFS indexing) -> quantification (LCC estimation) -> classification (underload identification) -> comparison (vs. ghost city concept)
- **Key figures**:
  - F1: establish (1 panel) — Land functional zone maps of 81 Chinese cities at VHR
  - F2: reveal (1 panel) — Six LFS-based city clusters
  - F3: quantify (3 panels) — LCC computations: SLC and LCR for 81 cities
  - F4: reveal (1 panel) — City distribution in LCR feature space
  - F5: classify (1 panel) — Five-type classification (underload to overload)
  - F6: validate (1 panel) — LCR vs. population density comparison, underload vs. ghost city differences
- **Narrative arc**: Problem framing -> VHR satellite mapping -> LFS characterization and clustering -> LCC estimation via SAE+OLS -> Underload city identification -> Conceptual contribution
- **Central claim**: Cities carrying fewer people and lower economic strength than their land carrying capacity constitute "underload cities," a broader and more accurate concept than "ghost cities" that accounts for spatial heterogeneity of land carrying capacities.
- **Claim strength**: descriptive

### Keywords
land carrying capacity, ghost city, satellite imagery, semantic segmentation, stacked auto-encoder, density peaks clustering, urban land use, sustainable development, China cities, VHR remote sensing

---

## ger_settlement_detection_unet

- **Paper**: Machine learning-based detection of informal ger settlements in Mongolia using satellite imagery (npj Urban Sustainability, 2025)
- **DOI**: 10.1038/s42949-025-00273-1
- **Domain**: urban_spatial_analysis
- **Study design**: time_series
- **Outcome type**: count
- **Inferential target**: distributional_pattern

### Method specification
- **Method name**: U-Net-based computer vision algorithm for circular dwelling (ger) detection from VHR satellite imagery
- **Hyperparameters**: U-Net architecture (encoder-decoder with skip connections); input: RGB satellite imagery from World Imagery dataset (Maxar/GeoEye-1, WorldView-2, WorldView-3); 8 temporal snapshots (2015 Jul, 2016 Aug, 2019 May, 2020 May, 2021 Apr, 2022 Apr, 2023 Jun, 2025 May); grid-level analysis at zoom level 15 (0.67 km² per grid); manual annotation for training labels
- **Required validations**: Correlation with World Bank district-level poverty data (r = 0.85); visual inspection of predicted vs. manual labels; temporal consistency check across 8 time periods
- **Characteristic outputs**: Individual ger detections per time period; ger count time series (2015-2025); grid-level change maps; ger household ratio estimates; extrapolation to nationwide slum population trends

### Planning pattern
- **Evidence count**: 3 distinct analytical results
- **Figure count**: 6 main, 0 Extended Data, Supplementary figures present
- **Evidence chain**: concept definition (ger as slum) -> detection (U-Net on satellite imagery) -> temporal analysis (2015-2025 trends) -> validation (poverty correlation) -> implication (SDG monitoring gap)
- **Key figures**:
  - F1: establish (2 panels) — Detected gers in Ulaanbaatar 2025 + zoomed settlement layout
  - F2: quantify (multi-panel) — Ger count changes over decade showing three trends (decline, sporadic increase, stability)
  - F3: reveal (1 panel) — Grid-level ger relocation from center to periphery
  - F4: validate (1 panel) — Slum population (% urban) comparison with official projections
  - F5: establish (1 panel) — Satellite image coverage and administrative boundaries
  - F6: validate (multi-panel) — Input images, manual labels, and U-Net predictions
- **Narrative arc**: Slum definition rationale -> U-Net detection -> Temporal trend analysis -> Periphery extension -> Validation against poverty data -> SDG monitoring implications
- **Central claim**: U-Net-based detection of circular ger settlements from VHR satellite imagery reveals that housing improvements in Mongolian informal settlements have fallen short of official projections by 2.8% since the pandemic, demonstrating the value of ML on satellite data for SDG monitoring.
- **Claim strength**: suggestive

### Keywords
U-Net, computer vision, satellite imagery, informal settlement, slum detection, ger, Mongolia, urbanization, SDG monitoring, time series, VHR, remote sensing
