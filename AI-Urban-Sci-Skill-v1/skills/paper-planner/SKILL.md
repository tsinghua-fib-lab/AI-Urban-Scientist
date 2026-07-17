---
name: paper-planner
description: "Create a single-file, human-reviewable research paper execution plan from an article, research idea, dataset, result sketch, or early analysis concept. Use when Codex needs a research plan with central claim, research questions, evidence chain, data plan, method-library calibration, analysis execution DAG, figures/tables, robustness checks, risks, interpretation framework, and agent-ready tasks."
---

# Paper Planner

Use this skill to turn a paper idea or existing article into a **research execution plan**. The plan should be strong enough to guide a researcher or coding agent through the work, while remaining compact enough to review in one sitting.

## Output Package

Create or update exactly this folder unless the user gives another target:

```text
plans/paper-plan/
```

Create exactly one default output file:

```text
paper_plan.md
```

This file is the human review document and must contain all plan sections. Do not split the plan across multiple files unless the user explicitly asks. If the user asks for a machine-readable plan, additionally create `agent_plan.json`; otherwise do not create JSON.

Do not write into `.claude/skills` or install the skill unless the user explicitly asks.

Use `references/output_templates.md` for compact file templates when useful.

## Planning Standard

A good plan must answer five questions:

1. **What is the paper claiming?** Central claim, claim strength, subclaims, falsification conditions.
2. **How would the research be executed?** Data, variables, identification/model strategy, analysis tasks, dependencies, acceptance criteria.
3. **What evidence would persuade a skeptical reviewer?** Evidence chain, figures, tables, validation, robustness, alternative explanations.
4. **What could go wrong?** Data gaps, measurement risks, identification threats, model limitations, scope limits.
5. **How should different result patterns be interpreted?** Primary, null, heterogeneous, mechanism-only, and fragile/sensitivity-dependent outcomes.

## Workflow

This skill runs as a **staged planning pipeline**: eight sequential transformation stages turn a polymorphic source into an executable plan, a ninth gate stage closes a quality feedback loop, and a domain knowledge base feeds the calibration stage on demand. The eleven steps below are the detailed specification of those stages.

```text
SOURCE (article · idea · dataset · result draft)
   │
   ▼
① INGEST     (Step 1)      raw source  → typed seed facts
② FRAME      (Step 2)      facts       → central claim · RQs · subclaims
        └─[branch] select profile by contribution type ─▶ parameterizes ④ ⑤ ⑦
③ GROUND     (Step 3)      argument    → datasets · variable construction
        └─[checkpoint] data sufficiency ─────────────fail─▶ ③ GROUND
④ CALIBRATE  (Steps 4–5)  quantities  → method match · strategy   ⇄ Method Library
        └─[checkpoint] claim–design fit ─────────────fail─▶ ② FRAME / ④ CALIBRATE
⑤ ARCHITECT  (Steps 6–7)  method      → evidence chain · analyses · task DAG
        └─[checkpoint] execution readiness · evidence coverage · mechanism discipline
                                                     fail─▶ ⑤ ARCHITECT  (mechanism → ② FRAME)
⑥ RENDER     (Step 8)      results     → figures · tables · visual-design spec
        └─[checkpoint] figure economy · visual design ─fail─▶ ⑥ RENDER
⑦ STRESS     (Step 9)      claim       → robustness · risks · reviewer defense
        └─[checkpoint] robustness adequacy ──────────fail─▶ ⑦ STRESS
⑧ INTERPRET  (Step 10)     one result  → five result-pattern contingencies
   │
   ▼
⑨ GATE       (Step 11)     draft plan  → re-confirm all checkpoints + no-invention
   │
   ├── pass ─▶ paper_plan.md  (+ optional agent_plan.json)
   └── fail ─▶ return to the stage named by the failed gate (typed back-edge; see Step 11)
```

Architectural invariants to honor while executing the steps:

- **Polymorphic ingestion** — INGEST normalizes every input type into the same seed facts, so all later stages stay input-agnostic.
- **Knowledge-base sidecar** — domain expertise lives in the Method Library, retrieved lazily at CALIBRATE; the pipeline itself stays generic.
- **Shift-left, fail-fast** — each gate is checked at the earliest stage where its inputs exist (the in-stage checkpoints above), not only at the end. Resolve a failed checkpoint before spending downstream stages; do not push a known-broken plan forward.
- **Typed back-edges** — a failed gate routes to the specific stage that owns the defect (named in Step 11), not a blanket restart. The terminal GATE re-confirms every checkpoint before emitting the plan; never emit a plan that fails GATE, downgrade the claim honestly instead.

### Pipeline Branch Profiles

The pipeline is not one fixed line. Right after FRAME, the **contribution type** (set during INGEST) selects a *branch profile* that parameterizes three downstream stages: which strategy family CALIBRATE must use, which evaluation task ARCHITECT must include, which checks STRESS must run, and the highest claim strength the branch may assert. Pick exactly one branch (or compose for mixed) before entering CALIBRATE, and apply it consistently through STRESS.

| Branch | Contribution types | CALIBRATE — strategy family | ARCHITECT — mandatory task | STRESS — mandatory checks | Claim ceiling |
| --- | --- | --- | --- | --- | --- |
| **Causal** | causal, quasi-causal | identification design (RCT, DiD, IV, RDD, matching, event study) | an identifying-assumption test task | balance, pre-/parallel-trends, placebo/negative control, sensitivity to unobserved confounding (Rosenbaum / E-value) | causal only if assumptions hold; else quasi-causal / suggestive |
| **Predictive** | predictive | supervised/ML model with a clean train/validation/test split | held-out evaluation + calibration task | cross-validation, calibration, external/temporal validation, ablation, leakage audit, baseline comparison | predictive performance only; no causal language |
| **Descriptive** | descriptive, measurement | estimator + explicit uncertainty quantification | validation-against-reference + coverage task | sampling/coverage sensitivity, reliability/repeatability, measurement-error sensitivity | descriptive; correlations are not framed as effects |
| **Mechanistic** | mechanistic | mediation, decomposition, perturbation, pathway analysis | mediator-validity + temporal-ordering task | alternative-pathway tests, mediator measurement error, ordering checks | mechanism only with mechanism evidence; else stated as hypothesis |
| **Simulation** | simulation, policy/scenario | IAM, LCA, Earth-system, agent-based, counterfactual scenario | calibration-to-baseline + uncertainty-propagation task | parameter uncertainty, scenario sensitivity, validation against observations | conditional on stated model assumptions and scenarios |
| **Mixed** | mixed | compose the relevant branches | each part's mandatory task | each part's mandatory checks | the weakest ceiling among composed branches; name the boundary between parts |

The branch is a routing decision, not a relabeling: CALIBRATE, ARCHITECT, and STRESS must actually contain the branch's required strategy, task, and checks, and the GATE will fail a plan whose claim exceeds its branch ceiling.

### Step 1: Ingest The Source

Identify the input type:

- Existing article or article JSON: preserve the article's actual title, data modalities, methods, and contribution.
- Research idea or dataset sketch: mark unknown details explicitly and propose the smallest credible data/method choices.
- Result sketch or early analysis: separate observed results from planned or hypothetical results.

Extract these seed facts before planning:

- working title
- domain and study design family
- unit of observation
- outcome, exposure/treatment, mediators/moderators, controls
- temporal and spatial coverage
- available datasets and missing datasets
- reported or intended methods
- main contribution type: causal, quasi-causal, descriptive, predictive, mechanistic, measurement, simulation, policy/scenario, or mixed

If an existing article is provided, avoid inventing analyses that contradict the source. Recommended extensions may be included, but label them as extensions.

### Step 2: Claim And Research Questions

Write one central claim with:

- `claim_text`: one sentence
- `claim_strength`: causal, quasi-causal, suggestive, descriptive, predictive, mechanistic, simulation, or exploratory
- `inferential_target`: population, process, relationship, mechanism, or policy quantity
- `falsification_condition`: concrete observation that would undermine the claim

Then write 3-6 research questions and 3-6 subclaims. Each subclaim must include:

- observable implication
- minimum evidence required
- primary analysis needed
- main alternative explanation
- result pattern that would weaken or revise the claim

Do not overstate causality. If identification is weak, downgrade claim strength and make the design honest.

### Step 3: Data And Measurement Plan

For every dataset, specify:

- name and role
- unit of observation
- time and spatial coverage
- key variables
- linkage keys
- preprocessing steps
- measurement limitations
- access or reproducibility constraints

For every core variable, specify:

- construct definition
- raw source field(s)
- transformation or normalization
- expected scale/unit
- missingness handling
- validation check

The plan should let an analyst know what table to build before choosing models.

> **Checkpoint — data sufficiency.** Before leaving GROUND, confirm the datasets and variables can support every subclaim. If not, stay in GROUND (add a dataset, redefine a variable, or narrow the subclaim) before advancing to CALIBRATE.

### Step 4: Method Library Calibration

Before finalizing the strategy, check the method library:

```text
references/method_library/
```

Use it this way:

1. Read `references/method_library/INDEX.md`.
2. Match the project by domain, method, outcome type, exposure/treatment, data modality, population, or keywords.
3. Open only the most relevant category files.
4. Search for entries with similar study design, variables, and evidence architecture.
5. Use matching entries to calibrate method choice, validations, evidence chain, figure architecture, and claim strength.
6. If no entry fits, use the strategy guide in the next step and mark method-library calibration as "no close match".

When adapting a method-library entry:

- Preserve the current project's own claim, data, and constraints.
- Borrow method patterns, validation expectations, and figure logic only when they fit.
- Do not copy another paper's results, effect sizes, or conclusions.
- If the project spans multiple domains, combine patterns explicitly and name the boundary between them.

### Step 5: Identification Or Modeling Strategy

Apply the branch profile selected after FRAME: the strategy you choose here must come from that branch's required strategy family. Choose a strategy that matches the claim:

| Claim need | Strategy examples | Required checks |
| --- | --- | --- |
| Causal effect | RCT, natural experiment, DiD, IV, RDD, matching, event study | balance, pre-trends, placebo, exclusion/continuity, sensitivity |
| Association/risk | GLM/GAM, mixed model, Cox, DLNM, Bayesian hierarchical model | residuals, functional form, lag/spline sensitivity, confounding control |
| Prediction/classification | gradient boosting, random forest, neural model, calibrated regression | cross-validation, calibration, external validation, ablation |
| Spatial process | spatial error/lag, GWR, CAR/BYM, spatial ML | spatial autocorrelation, scale sensitivity, boundary sensitivity |
| Network/diffusion | ERGM, exposure mapping, graph model, cascade analysis | null networks, edge-definition sensitivity, degree/confounding checks |
| Simulation/scenario | IAM, LCA, Earth-system, agent-based, counterfactual scenario | parameter uncertainty, scenario sensitivity, validation against observations |
| Mechanism | mediation, decomposition, feature attribution, perturbation, pathway analysis | mediator validity, temporal ordering, alternative pathway tests |

Write the primary model in prose or formula form. Include inputs, outputs, assumptions, and what would make the model unsuitable.

> **Checkpoint — claim–design fit.** Before leaving CALIBRATE, confirm the chosen strategy can actually deliver the claim's strength. If it cannot, route back: either downgrade the claim (return to FRAME) or change the strategy (stay in CALIBRATE). Do not carry an over-strong claim into ARCHITECT.

### Step 6: Evidence Chain And Main Analyses

Build an evidence chain before designing figures:

```text
context/measurement -> primary test -> mechanism or decomposition -> heterogeneity/generalization -> robustness/implication
```

Create 5-10 evidence items. For each:

- evidence ID
- linked subclaim(s)
- evidence type: estimate, contrast, map, prediction, diagnostic, mechanism, heterogeneity, robustness, table, qualitative synthesis
- datasets and variables
- analysis task(s)
- decision rule
- validity threat
- placement: main figure, table, text, extended/supporting, or omitted

Then define 5-10 main analyses. One of them must be the branch profile's mandatory task (e.g. a held-out evaluation for Predictive, an identifying-assumption test for Causal, a mediator-validity test for Mechanistic). Each analysis must include:

- purpose
- model or procedure
- exact input data
- output artifact
- acceptance criteria
- failure action if assumptions or diagnostics fail

### Step 7: Analysis Execution DAG

Write a task DAG, not just a list. Each task needs:

- stable task ID
- dependencies
- inputs
- method/model
- implementation notes
- outputs
- validation/diagnostics
- acceptance criteria
- downstream consumers

Use concrete outputs such as `tables/model_primary.csv`, `figures/F2_data.csv`, or `models/event_study_primary.rds` when appropriate. If file names are speculative, mark them as proposed.

> **Checkpoint — execution readiness · evidence coverage · mechanism discipline.** Before leaving ARCHITECT, confirm: every task has inputs, outputs, dependencies, validations, and acceptance criteria; every subclaim has primary evidence plus at least one validation/robustness path; and any mechanism claim has mechanism evidence. If a task is underspecified or a subclaim is uncovered, stay in ARCHITECT. If a mechanism lacks evidence, return to FRAME and reframe it as a hypothesis.

### Step 8: Figures And Tables

Design figures as arguments, not galleries.

Main figures should emphasize:

- primary claim tests
- central mechanism/decomposition
- key heterogeneity or generalization
- decisive validation or implication

Tables should hold:

- variable definitions
- sample construction
- dense model coefficients
- robustness matrix
- top-ranked entities or cases

For each figure/table, specify:

- narrative role
- linked evidence
- panels or columns
- visual/table type
- key comparison
- expected reader takeaway
- reason it belongs in main text, table, or supporting material

Keep main figures to 4-7 unless the claim genuinely needs a different figure budget.

#### Visual Design And Aesthetics

A figure plan is not finished until it specifies how the figure should *look*. Aim for the visual standard of Nature / Science / PNAS, not default `matplotlib`/`ggplot` output. Each figure (and the figure set as a whole) must define a deliberate visual design, not leave it to library defaults.

**Color is encoding, not decoration.** Choose the palette type by what the data means, and never use a rainbow/jet colormap:

- Sequential (single ordered quantity, e.g. density, magnitude): perceptually-uniform ramps such as `viridis`, `magma`, `cividis`, or ColorBrewer `Blues`/`YlGnBu`. Light = low, dark = high.
- Diverging (signed deviation from a meaningful midpoint, e.g. effect direction, anomaly): `RdBu`, `BrBG`, `PuOr`, or `coolwarm`, with a neutral, near-white midpoint pinned to zero.
- Categorical (unordered groups, ≤7 classes): a curated qualitative set such as Okabe–Ito (colorblind-safe), ColorBrewer `Set2`/`Dark2`, or Tableau 10. If groups exceed ~7, redesign (facet, group, or rank) rather than adding more hues.

**Accessibility and reproducibility are requirements, not nice-to-haves:**

- Colorblind-safe by default (prefer Okabe–Ito or `viridis` family); state that the palette survives deuteranopia/protanopia simulation.
- Do not rely on color alone — pair color with shape, line style, direct labels, or texture so the figure reads in grayscale and for color-blind readers.
- Define exact hex codes (or a named palette + version) so figures are reproducible and consistent across panels.
- Ensure sufficient contrast against the background and adequate luminance separation between adjacent categories.

**Composition and typographic discipline (apply across the whole figure set):**

- One consistent palette, font family, and sizing scheme across all figures so the paper reads as a designed set, not a collage.
- Maximize data-ink: remove chartjunk, heavy gridlines, 3D effects, redundant legends, and boxed frames; keep only marks that carry information.
- Direct-label series where feasible instead of forcing legend lookups; place legends inside dead space.
- Typography legible at final print column width (single ≈ 89 mm, double ≈ 183 mm): readable axis/tick labels, units on every axis, no clipped text, consistent decimal precision.
- Show uncertainty explicitly (CI bands, error bars, distributions) rather than point estimates alone.
- Vector format (PDF/SVG) for line art; ≥300 dpi for raster; specify target width and aspect ratio.

For each main figure, the plan must state: palette type and named palette + hex/version, colorblind-safety note, the redundant (non-color) encoding channel, font/size scheme, format + dpi + target width, and any uncertainty representation. Capture these in the figure design spec rows of the template.

> **Checkpoint — figure economy · visual design.** Before leaving RENDER, confirm main figures carry T1/T2 evidence (not just descriptive context) and that every main figure has a deliberate, colorblind-safe design spec. If a figure is decorative or under-specified, stay in RENDER and redesign before advancing to STRESS.

### Step 9: Robustness, Risks, And Reviewer Defense

Create a robustness matrix with:

- base checks: alternative model, alternative variable definition, sample restriction, placebo/negative control, multiple testing or uncertainty correction, missingness/sampling sensitivity
- design-specific checks: the branch profile's mandatory checks plus design specifics, e.g. pre-trends for DiD, bandwidth for RDD, lag structure for DLNM, edge definition for networks, spatial weights for spatial models
- context-specific checks tied to the actual domain

Create a risk register:

- data risk
- measurement risk
- identification/model risk
- mechanism risk
- generalizability risk
- ethics/policy misuse risk when relevant

For each risk, include likelihood, impact, affected claim, mitigation, and how to phrase the limitation if unresolved.

> **Checkpoint — robustness adequacy.** Before leaving STRESS, confirm the checks address the main alternative explanations for each subclaim, not just generic sensitivity. If a primary threat is unaddressed, stay in STRESS and add the targeted check.

### Step 10: Interpretation Framework

Write interpretations for at least five result patterns:

- **Primary pattern**: main claim supported
- **Null pattern**: primary estimate weak or absent
- **Heterogeneous pattern**: effect appears only in some groups/regions/time periods
- **Mechanism pattern**: primary effect exists but mechanism evidence is weak, or mechanism appears without primary effect
- **Fragile pattern**: result depends on specification, sample, model, or measurement choice

For each pattern, say how the central claim, title, figures, and discussion should change.

### Step 11: Quality Gates

Most gates are first checked at an in-stage **checkpoint** (shift-left, fail-fast) so defects are caught before downstream stages are spent. The terminal GATE **re-confirms every gate** on the assembled plan and adds the two whole-plan gates (`no-invention`, and a final pass of `claim-design fit`). Record each gate as pass / caution / fail.

When a gate fails, follow its **typed back-edge** — return to the stage that owns the defect, fix, and re-run from there. Do not blanket-restart, and do not emit a plan with an unresolved fail; if a defect cannot be fixed, downgrade the claim honestly and record the limitation.

| Gate | First checked at | On fail → return to | Verifies |
| --- | --- | --- | --- |
| Data sufficiency | ③ GROUND checkpoint | ③ GROUND | datasets and variables can support each subclaim |
| Claim-design fit | ④ CALIBRATE checkpoint | ② FRAME (downgrade) or ④ CALIBRATE (re-strategize) | claim strength matches the strategy and does not exceed the branch profile's claim ceiling |
| Execution readiness | ⑤ ARCHITECT checkpoint | ⑤ ARCHITECT | tasks have inputs, outputs, dependencies, validations, acceptance criteria |
| Evidence coverage | ⑤ ARCHITECT checkpoint | ⑤ ARCHITECT | every subclaim has primary evidence + ≥1 validation/robustness path |
| Mechanism discipline | ⑤ ARCHITECT checkpoint | ② FRAME (reframe as hypothesis) | mechanism claims have mechanism evidence |
| Figure economy | ⑥ RENDER checkpoint | ⑥ RENDER | main figures carry T1/T2 evidence, not descriptive filler |
| Visual design | ⑥ RENDER checkpoint | ⑥ RENDER | colorblind-safe palette, redundant encoding, consistent typography, uncertainty, print-grade format; no rainbow maps/defaults |
| Robustness adequacy | ⑦ STRESS checkpoint | ⑦ STRESS | checks address the main alternative explanations, not generic sensitivity |
| No invention | ⑨ GATE (terminal) | offending stage | unknown facts stay marked unknown; extensions labeled |

## Optional Agent Plan JSON Contract

Create `agent_plan.json` only when the user explicitly asks for a machine-readable or agent-executable JSON plan. When created, it should include:

- `metadata`
- `central_claim`
- `research_questions`
- `subclaims`
- `datasets`
- `variables`
- `method_library_calibration`
- `identification_or_modeling_strategy`
- `evidence_items`
- `analysis_tasks`
- `figure_style_guide`
- `figures`
- `tables`
- `robustness_checks`
- `risk_register`
- `interpretation_framework`
- `quality_gates`

Keep JSON concise. Put long prose in `paper_plan.md`.

## Common Failure Modes

- Producing only a claim/evidence/figure summary with no execution DAG.
- Listing methods without variable construction or acceptance criteria.
- Treating robustness as generic rather than tied to the design's main threats.
- Calling an association a mechanism without mediator, pathway, perturbation, or decomposition evidence.
- Adding ambitious extensions to an existing article without marking them as extensions.
- Splitting the human review plan across multiple files without being asked.
- Inventing effect sizes, p-values, sample sizes, or findings not present in the source.
