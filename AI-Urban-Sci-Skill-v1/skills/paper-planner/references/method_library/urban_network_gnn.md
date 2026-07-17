# Urban Network & Graph Neural Networks

Entries on quantifying urban network topology, spatial homogeneity, and intercity similarity using graph neural networks and link prediction.

---

## Spatial Homogeneity Quantification via R-GCN Link Prediction

- **Paper**: Quantifying the spatial homogeneity of urban road networks via graph neural networks (Nature Machine Intelligence, 2022)
- **DOI**: 10.1038/s42256-022-00462-y
- **Domain**: Urban road networks, graph neural networks, spatial homogeneity, transfer learning
- **Study design**: Cross-city comparative analysis across 30 global cities, 11,790 urban road networks (URNs) at 1 km × 1 km resolution
- **Outcome type**: F1 score of link prediction (spatial homogeneity metric); URN type classification; intercity similarity matrix
- **Inferential target**: Relationship between road network spatial homogeneity and socioeconomic development indicators (GDP, population growth, city age)

### Method specification
- **Method name**: Relational Graph Convolutional Network (R-GCN*) + DistMult bilinear scoring + link prediction + K-means URN clustering
- **Hyperparameters**: R-GCN: 3 layers, 50 neurons, learning rate 0.001, 10 epochs; link prediction: 80% links for training, 20% for testing; sigmoid threshold δ = 0.61; positive:negative sample ratio 1:5; K-means: k=4 clusters on 11 network metrics
- **Required validations**: Comparison against 5 other GNN models (node2vec, struc2vec, GraphSAGE, spectral GCN, GAT); centroid shifting robustness test; 30 km × 30 km vs. 20 km × 20 km boundary robustness; feature removal clustering consistency (93.1%-84.4% membership retention)
- **Characteristic outputs**: F1 score distribution per city; URN type composition by city; network irregularity (PC1) vs. F1 correlation; intercity similarity matrix with hierarchical clustering; socioeconomic association regression (15 factors)

### Planning pattern
- **Evidence count**: 5 distinct analytical results
- **Figure count**: 6 main, 0 ED, unspecified Supplementary
- **Evidence chain**: spatial homogeneity definition → intracity link prediction (30 cities) → URN type interpretation → network irregularity correlation → socioeconomic association (GDP, PG, city age) → intercity transfer learning → historical urban insights
- **Key figures**:
  - F1: Spatial homogeneity concept — local vs. entire network similarity, socioeconomic implications
  - F2: URN type interpretation — 4-type centroid coordinates, F1 score distribution, type performance comparison, city type composition
  - F3: Network irregularity vs. F1 — negative correlation scatter + road network visualizations (Chicago, Paris, Singapore)
  - F4: Socioeconomic development — F1 comparison by GDP/PG class across time periods; R² and p-values for 15 regression factors
  - F5: Intercity similarity — average F1 by training/testing city pair; hierarchical clustering dendrogram
  - F6: Historical insights — spatial F1 distribution in Los Angeles showing temporal road network development layers
- **Narrative arc**: Spatial homogeneity defined as local-global network similarity → R-GCN link prediction quantifies homogeneity via F1 → grid-type URNs most predictable → homogeneity negatively correlates with network irregularity → mature cities (high GDP, low PG) have higher homogeneity → intercity transfer reveals development patterns and historical layers
- **Central claim**: Road network spatial homogeneity, quantified as GNN link prediction F1 score, reveals socioeconomic development patterns, with mature cities (high GDP, low population growth) exhibiting more predictable, standardized road networks
- **Claim strength**: Descriptive (observational correlation analysis with ML-derived metric)

### Keywords
urban road network, graph neural network, R-GCN, link prediction, spatial homogeneity, transfer learning, network irregularity, K-means clustering, OpenStreetMap, OSMnx, city comparison, socioeconomic development, population growth, city age, DistMult
