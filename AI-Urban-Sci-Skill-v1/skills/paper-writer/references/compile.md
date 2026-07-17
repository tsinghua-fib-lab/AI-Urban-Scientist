# Compile LaTeX to PDF — Self-Contained Reference

This file replaces the `/paper-compile` skill dependency. Follow every step here without calling any external skill.

## Constants

- **COMPILER**: `latexmk`
- **ENGINE**: `pdflatex` (use `xelatex` only for CJK/custom fonts)
- **MAX_ATTEMPTS**: 3
- **PAPER_DIR**: `paper/` (relative to the job's output directory)

---

## Step 1: Verify Prerequisites

```bash
which pdflatex && which latexmk && which bibtex
# If missing on Ubuntu: sudo apt-get install -y texlive-full
# macOS: brew install --cask mactex-no-gui
```

Verify required files:
```bash
ls paper/main.tex
ls paper/references.bib 2>/dev/null || echo "WARNING: no references.bib"
```

---

## Step 2: First Compilation

```bash
cd paper/
# Clean all stale artifacts first
latexmk -C
# Full build: pdflatex + bibtex + pdflatex × 2
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex 2>&1 | tee compile.log
```

---

## Step 3: Error Diagnosis

Read `compile.log` and match against this table:

| Error pattern | Fix |
|--------------|-----|
| `File 'somepackage.sty' not found` | `tlmgr install somepackage` or remove `\usepackage` |
| `Reference 'fig:xyz' undefined` | Verify `\label{fig:xyz}` exists in correct figure env |
| `File 'figures/fig1.pdf' not found` | Check extension (.pdf vs .png), fix `\includegraphics` path |
| `Citation 'key' undefined` | Add entry to `references.bib` or fix key spelling |
| `I was expecting a ',' or a '}'` | Fix BibTeX syntax in `references.bib` |
| `Overfull \hbox (>20pt)` | Rephrase text or adjust figure width; ignore if ≤20pt |
| `\crefname undefined` | Add `\crefname{...}` after `\newtheorem` in preamble |
| `[VERIFY]` markers in source | Search for correct information or mark as TODO |

---

## Step 4: Iterative Fix Loop

```
for attempt in 1..3:
    compile()
    if success: break
    parse compile.log for errors
    apply fixes from Step 3 table
    clean aux files: latexmk -C
```

After each fix, always clean aux files before recompiling.

---

## Step 5: Post-Compilation Checks

```bash
# PDF exists and non-empty
ls -la paper/main.pdf
pdfinfo paper/main.pdf | grep Pages

# Undefined references/citations
grep -c "LaTeX Warning.*undefined" paper/compile.log
grep -c "Citation.*undefined" paper/compile.log
```

Checklist:
- [ ] `main.pdf` exists and is > 100 KB
- [ ] No `??` in PDF (undefined references)
- [ ] No `[?]` in PDF (undefined citations)
- [ ] All figures rendered (no missing image placeholders)

Visual scan (read PDF directly if possible):
- Figures readable, labels legible
- No orphaned section headers
- Tables aligned, consistent decimal precision

---

## Step 6: Page Count Verification

**Nature / urban science style (this pipeline)**: no strict page cap — verify the PDF is 12–20 pages and appears complete.

**ML conference page counting** (if ever used for conference submission):
- ICLR/NeurIPS/ICML: main body = title through end of Conclusion; references and appendix excluded
- ICLR=9, NeurIPS=9, ICML=8

**IEEE**: total pages including references count toward limit.

```bash
pdftotext paper/main.pdf - | python3 -c "
import sys
text = sys.stdin.read()
pages = text.split('\f')
for i, page in enumerate(pages):
    if 'Conclusion' in page:
        print(f'Conclusion on page {i+1}')
    if any(w in page for w in ['References', 'Bibliography']):
        lines = [l for l in page.split('\n') if l.strip()]
        for l in lines[:3]:
            if 'References' in l or 'Bibliography' in l:
                print(f'References start on page {i+1}')
                break
"
```

---

## Step 7: Stale File Detection

```bash
for f in paper/sections/*.tex 2>/dev/null; do
    base=$(basename "$f")
    grep -q "$base" paper/main.tex || echo "WARNING: $f not referenced by main.tex"
done
```

---

## Step 8: Output Summary

Report:
```
Compilation: SUCCESS | FAILED
PDF: paper-output/<idea-stem>/paper/main.pdf
Pages: X
PDF size: Y KB
Undefined references: N
Undefined citations: N
Figures embedded: M/M
```

---

## Key Rules

- Never delete source files — only modify to fix errors
- Keep `compile.log` — useful for debugging
- Do not suppress warnings — report but do not block
- Font embedding: `pdffonts main.pdf | grep -v "yes"` should return nothing
- Clean ALL aux files before every recompile attempt
