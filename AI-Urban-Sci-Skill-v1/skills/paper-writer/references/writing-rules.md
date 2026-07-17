# Writing Rules — Nature Style

## Language Calibration by Support Status

| `support_status` | Allowed phrases | Avoid |
|-----------------|----------------|-------|
| `supported` | "We find that...", "X increases Y by Z%", "Our results demonstrate..." | Hedging |
| `partially_supported` | "Our data suggest...", "There is preliminary evidence...", "We observe a trend..." | Strong causal claims |
| `unsupported` | "We speculate that...", "This remains to be tested...", "Future work should..." | Presenting as finding |
| `contradicted` | "Contrary to our hypothesis...", "We find no evidence for...", "Unexpectedly..." | Hiding the contradiction |

Every Results paragraph that references evidence **must** identify its subclaim ID (in comments or implicitly) and use language matching that subclaim's `support_status`.

## Structural Rules

**Abstract** (self-contained, ~150 words):
> Context → Problem/gap → Approach or dataset → Main finding (number) → Mechanism or validation → Implication with explicit scope limit

**Introduction** (no `\section` header):
1. Broad context and real-world motivation (1–2 paragraphs)
2. Knowledge gap (1 paragraph)
3. One-sentence contribution matching the central claim
4. Bullet contributions (3–4 items, each falsifiable)
5. Results preview (1 paragraph)

**Results**:
- Each `\section` or `\subsection` maps to one or more subclaim IDs from the plan
- Every paragraph references a figure panel: "(Fig. 1a)" or "as shown in Fig. 2b"
- Include a limitation paragraph where `interpretation_boundary` is defined in the plan

**Methods** (last section before addendum):
- List actual filenames from `data/` — not hypothetical dataset names
- Reproducibility: describe what can be reproduced; **do NOT write a GitHub URL**
- If data is synthetic: "As no empirical dataset was available, we constructed a synthetic dataset calibrated to published literature values."

## Forbidden Words (AI-isms)

Do not use: `delve`, `pivotal`, `landscape`, `tapestry`, `underscore`, `noteworthy`, `crucial`, `robust` (as generic filler), `showcase`, `leverage` (as verb).

## Claim Integrity Rules

- Every quantitative claim must trace to a file in `results/`
- Do not over-claim: match language exactly to `support_status`
- Do not present synthetic data as survey or observational data in Abstract or Introduction
- Do not fabricate URLs, repository links, or data availability statements
- Author line: always `\author{AI Urban Scientist}` — never invent names or affiliations
