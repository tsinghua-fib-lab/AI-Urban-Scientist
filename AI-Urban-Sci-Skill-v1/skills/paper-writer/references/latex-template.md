# LaTeX Template — Nature Style

## Preamble

```latex
\documentclass{nature}

\usepackage[utf8]{inputenc}
\usepackage{graphicx}
\usepackage{amsmath}
\usepackage{amssymb}
\usepackage{booktabs}
\usepackage{multirow}
\usepackage{longtable}
\usepackage{hyperref}   % must be loaded last

% FIX 1: nature.cls disables \includegraphics — restore it
\let\realincludegraphics\includegraphics
\AtBeginDocument{\let\includegraphics\realincludegraphics}

% FIX 2: nature.cls defers figure captions to end — restore standard float
\makeatletter
\renewenvironment{figure}{\@float{figure}}{\end@float}
\makeatother
```

## Document Structure

```latex
\begin{document}

\title{<Working title from PAPER_PLAN.md, refined on actual results>}
\author{AI Urban Scientist}   % NEVER invent names or affiliations

\maketitle

% Abstract: Context → Gap → Approach/dataset → Main finding → Mechanism → Implication+scope
\begin{abstract}
...
\end{abstract}

% Introduction (no \section header — flows directly from abstract)
% 1. Broad context and motivation
% 2. Knowledge gap
% 3. One-sentence contribution (from central claim)
% 4. Contributions (3-4 bullets, each falsifiable)
% 5. Results preview

% Results sections — driven by evidence chain in PAPER_PLAN.md
% Each \section supports one or more subclaims
% Every paragraph references figure panels: "Fig. 1a shows..."

% Discussion
% 1. Broader implications, policy relevance
% 2. Limitations (honest, transparent)
% 3. Future directions

% Methods
% 1. Data sources (list actual files from data/)
% 2. Analysis models
% 3. Statistics
% 4. Software and packages
% 5. Reproducibility: describe what can be reproduced — DO NOT fabricate a GitHub URL
% 6. Data availability: if synthetic, state plainly

\begin{addendum}
\item[Competing interests] The authors declare no competing interests.
\end{addendum}

\bibliographystyle{naturemag}
\bibliography{references}

\end{document}
```

## Figure Inclusion

Figure paths are relative to `paper/` directory:
```latex
\begin{figure}
\includegraphics[width=\textwidth]{../figures/fig1.pdf}
\caption{Caption text. \textbf{a,} Panel description. \textbf{b,} Panel description.}
\label{fig:fig1}
\end{figure}
```

Standard widths:
- Single column: `width=0.48\textwidth` (3.4 inches)
- Double column: `width=\textwidth` (6.8 inches)

## BibTeX Rules

Allowed entry types: `@article`, `@book`, `@inproceedings`, `@misc`, `@phdthesis`

**Do NOT use `@report`** — not defined in `naturemag.bst`. Use `@book` for technical reports.

Fetch real BibTeX:
```bash
# Via DBLP (title + author search)
curl -s "https://dblp.org/search/publ/api?q=TITLE+AUTHOR&format=json&h=3"

# Via DOI
curl -sLH "Accept: application/x-bibtex" "https://doi.org/{doi}"
```

Mark unverifiable entries with `% [VERIFY]` — never fabricate.

## Critical Fixes Summary

1. `\includegraphics` disabled by `nature.cls` → restore with `\AtBeginDocument`
2. Figure captions deferred to end by `nature.cls` → restore standard `\@float`
3. `@report` not in `naturemag.bst` → use `@book`
4. All `\makeatletter`/`\makeatother` must wrap @-commands
5. Figure paths: `../figures/` relative to `paper/`
6. Clean ALL aux files before recompile: `latexmk -C`
