# Remote Sensing & Socioeconomics

Entries on inferring socioeconomic indicators from satellite/aerial imagery using deep learning with model interpretability methods.

---

## Interpretable SES Inference from Aerial Imagery via EfficientNet + Grad-CAM

- **Paper**: Interpretable socioeconomic status inference from aerial imagery through urban patterns (Nature Machine Intelligence, 2020)
- **DOI**: 10.1038/s42256-020-00243-5
- **Domain**: Remote sensing, socioeconomic inference, model interpretability, urban analytics
- **Study design**: Supervised learning with transfer learning across 5 French cities, fivefold cross-validation
- **Outcome type**: 5-class SES prediction (income quantiles) at 200m × 200m resolution; urban class activation maps
- **Inferential target**: Correlation between CNN activation patterns and urban land-use topology for SES prediction

### Method specification
- **Method name**: EfficientNetB0 (transfer learning from ImageNet) + binomial ordinal layer + guided Grad-CAM + activation ratio metric
- **Hyperparameters**: Input: 800 × 800 × 3 aerial tiles (20 cm/pixel); learning rate: 8×10⁻⁵, decayed 90% every 3 epochs; max 30 epochs; 2,500 samples/epoch; 5-fold CV (80/20 split, inner 75/25 train/val); data augmentation: random horizontal/vertical flip
- **Required validations**: Fivefold cross-validation per city; performance comparison against VGGs and ResNets (Supplementary Table 1); overfitting risk assessment (Supplementary Fig. 6)
- **Characteristic outputs**: Confusion matrices with Pearson r, MAE, accuracy, accuracy(±1); SES prediction maps; guided Grad-CAM activation maps; activation ratio per urban class; coactivation/co-appearance gain heatmaps

### Planning pattern
- **Evidence count**: 4 distinct analytical results
- **Figure count**: 6 main, 0 ED, unspecified Supplementary
- **Evidence chain**: dataset combination (aerial + socioeconomic + land-use) → SES inference model training → spatial prediction maps → Grad-CAM interpretability → activation ratio to urban topology correlation → coactivation analysis
- **Key figures**:
  - F1: Overlaid datasets (Paris) — aerial tile, income distribution, land cover map
  - F2: SES prediction confusion matrices across 5 French cities with r, MAE, Acc, Acc(±1)
  - F3: Observed vs. predicted income maps (Paris) — 200m × 200m pixel-level prediction
  - F4: Guided Grad-CAM activation maps for poorest and wealthiest classes overlaid on land-use polygons
  - F5: Correlation between urban topology and SES — mean activation rate per urban class with 95% CI
  - F6: Low/high SES coactivation and co-appearance gain heatmap — spatial neighborhood relationships
- **Narrative arc**: Aerial imagery + census income + land-use data combined → EfficientNet predicts SES at fine resolution → predictions recover spatial income patterns → Grad-CAM reveals which urban features drive predictions → activation ratios quantify land-use-SES correlations → coactivation maps show neighborhood effects
- **Central claim**: EfficientNet trained on aerial imagery can predict neighborhood-level SES with r = 0.65-0.71, and guided Grad-CAM reveals that specific urban patterns (e.g., green space, building density) are the visual features the model uses for inference
- **Claim strength**: Descriptive (supervised learning with interpretability analysis)

### Keywords
socioeconomic status, aerial imagery, satellite image, EfficientNet, transfer learning, Grad-CAM, interpretability, urban topology, land use, income prediction, CNN, activation map, French cities, remote sensing, urban pattern
