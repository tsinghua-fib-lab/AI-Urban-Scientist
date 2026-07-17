# Figure Style — Nature Publication Quality

## Style Constants

```python
# figures/paper_plot_style.py
import matplotlib as mpl
import matplotlib.pyplot as plt

COLORS = ['#2166ac', '#b2182b', '#33a02c', '#f46d43', '#663399', '#ff7f00']
WIDTH_SINGLE = 3.4   # inches, single column
WIDTH_DOUBLE = 6.8   # inches, double column

def apply_nature_style():
    mpl.rcParams.update({
        'font.family':       'serif',
        'font.size':         8,
        'axes.linewidth':    0.8,
        'axes.labelsize':    8,
        'xtick.labelsize':   7,
        'ytick.labelsize':   7,
        'legend.fontsize':   7,
        'figure.dpi':        150,
        'savefig.dpi':       150,
        'savefig.bbox':      'tight',
        'savefig.pad_inches': 0.05,
    })
```

## Output Formats

For every figure, generate three files:

```python
import matplotlib.pyplot as plt

def save_figure(fig, figure_id, figures_dir):
    base = f"{figures_dir}/{figure_id}"
    fig.savefig(f"{base}.pdf")          # vector — for LaTeX embedding
    fig.savefig(f"{base}.svg")          # vector editable
    fig.savefig(f"{base}.png", dpi=150) # preview
    # also save source data
    # df.to_csv(f"{base}_source_data.csv", index=False)
```

## Decision Tree

```
figure <id> needed?
├── file exists in figures/?  → use existing, skip generation
├── results/<task_id>_results.csv exists? → write plotting script, generate
└── results missing?
    ├── run analysis first (Step 4), then generate
    └── or document as placeholder with caption
```

## Script Pattern

```python
#!/usr/bin/env python3
# Data source: results/<task_id>_results.csv
# Skipped files: none

import sys
import pandas as pd
import matplotlib.pyplot as plt
sys.path.insert(0, 'figures/')
from paper_plot_style import apply_nature_style, COLORS, WIDTH_SINGLE

apply_nature_style()

df = pd.read_csv('results/<task_id>_results.csv')

fig, axes = plt.subplots(1, 2, figsize=(WIDTH_DOUBLE, 2.5))

# panel a
ax = axes[0]
ax.plot(df['x'], df['y'], color=COLORS[0])
ax.set_xlabel('X label')
ax.set_ylabel('Y label')
ax.text(-0.15, 1.05, 'a', transform=ax.transAxes,
        fontsize=9, fontweight='bold', va='top')

# panel b
# ...

plt.tight_layout()
save_figure(fig, 'fig1', 'figures/')
plt.close()
```

## LaTeX Tables

Save to `tables/` as `.tex` files, then `\input{../tables/tab_main.tex}` in `main.tex`.

```python
# Example: main results table
latex_table = df.to_latex(
    index=False,
    float_format='%.3f',
    booktabs=True,
    caption='Main results.',
    label='tab:main',
)
with open('tables/tab_main.tex', 'w') as f:
    f.write(latex_table)
```
