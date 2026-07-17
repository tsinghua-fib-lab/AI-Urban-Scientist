# Paper Experimenter

A Claude Code skill that runs the **experiment phase** of a research plan — from data audit through experiment execution to a structured narrative report ready for paper writing.

## What It Produces

```
paper-output/<idea-stem>/
├── exp/                             # experiment scripts (.py)
├── results/                         # experiment outputs (CSV, JSON)
│   ├── <task_id>_results.csv        # per-task result files
│   ├── NARRATIVE_REPORT.md          # human-readable evidence report
│   └── narrative_report.json        # machine-readable claim-to-evidence map
├── figures/                         # publication-quality figures
│   ├── fig1.pdf / .svg / .png       # 3 formats per figure
│   └── fig1_source_data.csv         # source data for reproducibility
├── tables/                          # LaTeX tables (.tex)
└── paper/                           # placeholder for paper-writer
```

## How It Works

1. **Locate the plan** — reads `PAPER_PLAN.md` and `DATA_SEEKER_REPORT.md`
2. **Audit existing work** — checks what already exists, never re-runs
3. **Execute experiments** — writes and runs `exp/<task_id>.py` scripts from the plan's analysis DAG
4. **Generate figures & tables** — publication-grade (Nature/PNAS standard), colorblind-safe, 3 formats each
5. **Write narrative report** — maps every subclaim to its `support_status` (supported / partially_supported / unsupported / contradicted) with numerical evidence

## How To Use

```text
/paper-experimenter                  # auto-detect latest plan
/paper-experimenter <subfolder>     # use plan-output/<subfolder>/
```

## Dependencies

- **Upstream**: `paper-planner` (produces `PAPER_PLAN.md`) + `urban-data-seeker` (provides `data/`)
- **Downstream**: `paper-writer` (consumes `NARRATIVE_REPORT.md` + figures to write the paper)

## Core Rules

- **Real data first** — synthetic data only as last resort, explicitly disclosed
- **Consume before creating** — never re-run completed work
- **No user interaction** — fully autonomous
- **No fabrication** — all numbers trace to `results/` files
- **Clean handoff** — narrative report is the contract with `paper-writer`

## Files

```text
paper-experimenter/
├── SKILL.md                     # Full skill definition (7-step workflow)
├── README.md                    # This file
└── references/
    └── figure-style.md          # Figure style constants, output formats, script patterns
```
