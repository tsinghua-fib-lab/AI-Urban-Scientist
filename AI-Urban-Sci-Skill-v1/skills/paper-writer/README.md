# Paper Writer

A Claude Code skill that writes and compiles a **submission-ready paper** from experiment results — LaTeX with Nature template, quality gate verification, and PDF compilation.

## What It Produces

```
paper-output/<idea-stem>/paper/
├── main.tex                      # monolithic LaTeX source (Nature \documentclass)
├── main.pdf                      # compiled, submission-ready PDF
├── references.bib                # bibliography
├── quality_gate_check.md         # subclaim-evidence traceability report
└── compile.log                   # full compilation log
```

## How It Works

1. **Verify prerequisites** — ensures `NARRATIVE_REPORT.md` and all figures exist (hard stop if missing)
2. **Write LaTeX paper** — single monolithic `main.tex` with Nature template, claim-calibrated language
3. **Quality gate** — traces every subclaim to evidence, checks citations, verifies figures
4. **Compile to PDF** — `latexmk` + `pdflatex` with automatic error diagnosis and fix loop (max 3 attempts)
5. **Summary report** — compilation status, page count, figure/citation resolution stats

## How To Use

```text
/paper-writer                          # auto-detect latest paper-output/
/paper-writer <paper-output-subfolder> # use specific output dir
```

## Prerequisites

**Must be run after `/paper-experimenter`** — requires:
- `paper-output/<idea-stem>/results/NARRATIVE_REPORT.md`
- `paper-output/<idea-stem>/results/narrative_report.json`
- `paper-output/<idea-stem>/figures/` (≥1 figure)
- `plan-output/<name>/PAPER_PLAN.md`

If any are missing, stops with an error — does NOT write a paper without results.

## Dependencies

- **Upstream**: `paper-experimenter` (produces figures, tables, and narrative report)
- **Requires**: LaTeX distribution with `pdflatex` and `latexmk`

## Core Rules

- **Results-first** — never write without experiment results
- **Claim-calibrated language** — claim strength language matched to `support_status`
- **No fabrication** — no invented URLs, BibTeX, or citations
- **No user interaction** — fully autonomous
- **No external skill calls** — self-contained compile logic

## Files

```text
paper-writer/
├── SKILL.md                     # Full skill definition (5-step workflow)
├── README.md                    # This file
└── references/
    ├── latex-template.md        # Nature \documentclass preamble + document structure
    ├── writing-rules.md         # Language calibration, structural rules, forbidden words
    └── compile.md               # LaTeX → PDF compilation with error diagnosis & fix loop
```
