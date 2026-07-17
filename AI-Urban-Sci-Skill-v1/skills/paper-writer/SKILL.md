---
name: paper-writer
description: "Paper Writer. Writes and compiles a submission-ready paper from experiment results: reads results/NARRATIVE_REPORT.md and plan-output/PAPER_PLAN.md, writes LaTeX paper with Nature template, runs quality gate, and compiles to PDF. Use when user says /paper-writer, wants to write a paper from experiment results, or the pipeline calls this step after /paper-experimenter."
---

# Paper Writer

Pipeline: `NARRATIVE_REPORT.md` + `PAPER_PLAN.md` → LaTeX → quality gate → `main.pdf`.

**Self-contained**: do NOT call `/paper-compile` or any other external skill. All compile logic is in `references/compile.md`.

**Prerequisite**: `paper-experimenter` must have completed successfully, producing `results/NARRATIVE_REPORT.md`, figures, and tables. If these are missing, report error and stop — do not write a paper without results.

## Usage

```
/paper-writer                          # auto-detect latest paper-output/ subfolder
/paper-writer <paper-output-subfolder> # use specific paper-output/<subfolder>/
```

## References (load when needed)

| File | Load when |
|------|-----------|
| `references/latex-template.md` | Step 2 — writing main.tex |
| `references/writing-rules.md` | Step 2 — writing Results, Discussion, Methods |
| `references/compile.md` | Step 4 — compiling LaTeX to PDF |

---

## Workflow

### Step 1: Verify Prerequisites

Locate the experiment output directory — auto-detect most recent `paper-output/<idea-stem>/` or use the one specified by the user.

Verify these files exist. **If any is missing, report error and stop — do not improvise.**

```
paper-output/<idea-stem>/results/NARRATIVE_REPORT.md      # REQUIRED
paper-output/<idea-stem>/results/narrative_report.json     # REQUIRED
paper-output/<idea-stem>/figures/                          # REQUIRED (≥1 figure)
paper-output/<idea-stem>/tables/                           # optional
plan-output/<name>/PAPER_PLAN.md                          # REQUIRED
```

Also verify `data/DATA_SEEKER_REPORT.md` exists for Methods section dataset references.

### Step 2: Write LaTeX Paper

Read `references/latex-template.md` for the full preamble, document structure, and BibTeX rules.  
Read `references/writing-rules.md` for language calibration, structural rules, and forbidden words.

Inputs:
- `results/NARRATIVE_REPORT.md` and `results/narrative_report.json` — actual results
- `PAPER_PLAN.md` — claim structure, evidence chain, figure design

Write `paper/main.tex` as a single monolithic file using `\documentclass{nature}`.

Paper sections: Abstract → Introduction → Results (subclaim-driven) → Discussion → Methods → Addendum → Bibliography.

### Step 3: Quality Gate

Before compiling, write `paper/quality_gate_check.md`:

- [ ] Each subclaim has ≥1 supporting evidence item in `results/`
- [ ] All planned figure files exist in `figures/`
- [ ] All `\cite{}` keys exist in `references.bib`
- [ ] Written claim language matches `support_status` in `narrative_report.json`
- [ ] All numerical results trace back to `results/` files
- [ ] Paper references actual downloaded files from `data/`, not hypothetical datasets

### Step 4: Compile to PDF

Read `references/compile.md` and follow its full workflow.  
Do NOT call `/paper-compile`.

### Step 5: Summary Report

```
Paper writing complete: <idea-title>

Plan:  plan-output/<name>/PAPER_PLAN.md
Results:  paper-output/<idea-stem>/

Output: paper-output/<idea-stem>/
  paper/main.pdf    — compiled Nature-style PDF
  paper/main.tex    — LaTeX source
  paper/quality_gate_check.md
  paper/compile.log

Compilation:  SUCCESS | FAILED
PDF pages:    X
PDF size:     Y KB
Figures:      M/M embedded
Citations:    X/X resolved
Quality gate: PASSED | ISSUES (see quality_gate_check.md)
```

---

## Core Rules

**Results-first**: never write a paper without experiment results. If `results/NARRATIVE_REPORT.md` is missing, stop and tell the user to run `/paper-experimenter` first.

**No fabrication**: no invented GitHub URLs, no fabricated BibTeX, no synthetic data presented as survey data.

**No user interaction**: never ask a question or wait for input. If blocked, apply fallback and continue (except for missing prerequisites — those are hard stops).

**No external skill calls**: compile logic lives in `references/compile.md` — use it directly.

**Claim integrity**: every quantitative claim must trace to a file in `results/`. Match language exactly to `support_status`. Author line: always `\author{AI Urban Scientist}` — never invent names or affiliations.
