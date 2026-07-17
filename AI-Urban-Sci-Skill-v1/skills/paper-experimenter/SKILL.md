---
name: paper-experimenter
description: "Paper Experimenter. Executes the experiment phase of a research plan: reads plan-output/PAPER_PLAN.md, audits available data, runs experiments, generates figures and tables, and produces a narrative report mapping results to subclaims. Use when user says /paper-experimenter, wants to run experiments from a plan, or the pipeline calls this step after /paper-planner."
---

# Paper Experimenter

Pipeline: `PAPER_PLAN.md` → experiments → figures → tables → `NARRATIVE_REPORT.md`.

**Self-contained**: do NOT call any external experiment or figure skill. All logic is defined in this file and `references/`.

## Usage

```
/paper-experimenter                # auto-detect latest plan-output/ subfolder
/paper-experimenter <subfolder>   # use plan-output/<subfolder>/
```

## References (load when needed)

| File | Load when |
|------|-----------|
| `references/figure-style.md` | Step 5 — generating figures and tables |

---

## Workflow

### Step 1: Locate the Plan

Auto-detect: pick the most recently modified subfolder in `plan-output/`.  
Manual: use `plan-output/<subfolder>/` if the user specified one.

Read `PAPER_PLAN.md` from that subfolder. **If it does not exist, report error and stop — do not improvise.**

Also read `data/DATA_SEEKER_REPORT.md` to understand available datasets.

### Step 2: Create Output Directory (idempotent)

Create `paper-output/<idea-stem>/` and its subdirectories **only if they do not already exist**. If the directory exists from a prior run, preserve its contents — Step 3 will detect what can be reused.

```
paper-output/<idea-stem>/
├── exp/        # experiment scripts
├── results/    # experiment outputs (CSV, JSON)
├── figures/    # generated figures (PDF, SVG, PNG)
├── tables/     # generated LaTeX tables
└── paper/      # placeholder — paper-writer fills this later
```

### Step 3: Data and Results Audit

- List all files in `data/`, cross-reference with data-seeker report
- Scan `exp/`, `results/`, `figures/` for already-completed work
- Record: what exists (consume directly) vs what needs to be created (run/generate)

### Step 4: Experiment Execution

For each analysis task in the plan's DAG:

```
result already in results/?  → skip (consume directly)
input data in data/?         → write exp/<task_id>.py and run
input data missing?          → apply fallback (proxy variable, skip with docs,
                               or synthetic data as last resort)
```

**Script requirements:**
- Load real data from `data/` — synthetic only when `data/` is empty or all files unusable
- Begin with a comment block listing which files it reads and why any were skipped
- Normalize features; set random seeds; import all modules at top level
- Target variable must not be tautologically derived from input features
- Use `df.rename(columns={...})` not `df.columns = [...]`
- Write output to `results/<task_id>_results.csv` or `.json`

### Step 5: Generate Figures and Tables

Read `references/figure-style.md` for style constants, output format commands, and script patterns.

```
figure exists in figures/?     → use existing
results/<task_id> exists?      → write plotting script, generate figure
results missing?               → run Step 4 first, or document as placeholder
```

Generate each figure in three formats: PDF (for LaTeX), SVG (editable), PNG (preview).  
Save source data CSV alongside each figure.  
Generate LaTeX tables to `tables/`.

### Step 6: Narrative Report

Create `results/NARRATIVE_REPORT.md` and `results/narrative_report.json`.

Structure: for each subclaim in the plan:
- Claim ID and statement
- `support_status`: `supported | partially_supported | unsupported | contradicted`
- Key numerical results (from `results/` files)
- Figure panel references
- Interpretation and boundary

### Step 7: Summary Report

```
Experiment phase complete: <idea-title>

Plan:  plan-output/<name>/PAPER_PLAN.md
Tasks: N planned | X executed | Y consumed | Z blocked
Figures: N planned | M generated

Output: paper-output/<idea-stem>/
  exp/              — experiment scripts
  results/          — experiment outputs (CSV, JSON)
    └── NARRATIVE_REPORT.md / narrative_report.json
  figures/          — PDF, SVG, PNG per figure + source data CSV
  tables/           — LaTeX tables

Status:  READY_FOR_WRITING  |  BLOCKED (see details)
Next step:  run /paper-writer to produce the full paper
```

---

## Core Rules

**Real data first**: scripts MUST load `data/` files when they exist. Synthetic data requires explicit disclosure in the narrative report.

**Consume before creating**: check `results/` and `figures/` before running anything. Never re-run completed work.

**No user interaction**: never ask a question or wait for input. If blocked, apply fallback and continue.

**No fabrication**: no invented numbers, no synthetic data presented as survey data. All results must trace to `results/` files.

**Hand off cleanly to paper-writer**: the narrative report is the contract — paper-writer reads it and PAPER_PLAN.md to write the paper. Every quantitative claim it makes must trace to a file in `results/`.
