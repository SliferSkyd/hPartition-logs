"""Box plots of per-replicate RF distance to the true tree, per #loci, for SimDNA1 and SimDNA2.
Reads results/per_rep.csv; writes results/rf_boxplots.{png,pdf}. Methods present in the csv are plotted
(PsiPartition appears automatically once its runs finish). Colour follows the method, never its rank."""
import csv
from collections import defaultdict
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path('/home/diepht/sliferskyd/hPartition/rerun_sim')
ORDER = ['PsiPartition', 'gPartition', 'hPartition']
COLOR = {'PsiPartition': '#2a78d6', 'gPartition': '#eb6834', 'hPartition': '#1baf7a'}
INK, INK2, GRID, SURF = '#1f1f1e', '#5f5e5a', '#e4e3df', '#fcfcfb'

data = defaultdict(list)
for r in csv.DictReader(open(ROOT / 'results' / 'per_rep.csv')):
    data[(r['dataset'], int(r['loci']), r['method'])].append(int(r['RF']))
methods = [m for m in ORDER if any(k[2] == m for k in data)]

plt.rcParams.update({'font.size': 9, 'axes.edgecolor': INK2, 'axes.labelcolor': INK, 'xtick.color': INK2,
                     'ytick.color': INK2, 'text.color': INK})
fig, axes = plt.subplots(2, 1, figsize=(7.2, 6.4), facecolor=SURF)
rng = np.random.default_rng(0)
w = 0.8 / len(methods)
for ax, (ds, loci) in zip(axes, [('SimDNA1', range(1, 11)), ('SimDNA2', range(6, 16))]):
    ax.set_facecolor(SURF)
    for i, l in enumerate(loci):
        for j, m in enumerate(methods):
            v = data.get((ds, l, m))
            if not v:
                continue
            x = i + (j - (len(methods) - 1) / 2) * w
            ax.boxplot(v, positions=[x], widths=w * 0.82, patch_artist=True, showfliers=False,
                       boxprops=dict(facecolor=COLOR[m] + '40', edgecolor=COLOR[m], linewidth=1),
                       medianprops=dict(color=COLOR[m], linewidth=2), whiskerprops=dict(color=COLOR[m], linewidth=1),
                       capprops=dict(color=COLOR[m], linewidth=1))
            ax.scatter(x + rng.uniform(-w * 0.25, w * 0.25, len(v)), v, s=9, color=COLOR[m], alpha=0.75,
                       edgecolors=SURF, linewidths=0.5, zorder=3)
            ax.scatter([x], [np.mean(v)], marker='D', s=14, color=SURF, edgecolors=INK, linewidths=0.8, zorder=4)
    ax.set_xticks(range(len(loci)), [str(l) for l in loci])
    ax.set_xlim(-0.6, len(loci) - 0.4)
    ax.set_ylim(bottom=-1)
    ax.set_ylabel('RF distance to true tree')
    ax.set_title(f'{ds}' + ('  (5,000 sites)' if ds == 'SimDNA1' else '  (1,000 sites per locus)'),
                 loc='left', fontsize=10, color=INK)
    ax.yaxis.grid(True, color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)
    for s in ['top', 'right']:
        ax.spines[s].set_visible(False)
axes[1].set_xlabel('Number of loci')
handles = [plt.Line2D([], [], color=COLOR[m], marker='s', linestyle='', markersize=8, label=m) for m in methods]
handles.append(plt.Line2D([], [], color=INK, marker='D', markerfacecolor=SURF, linestyle='', markersize=5, label='mean'))
fig.legend(handles=handles, loc='upper left', ncol=len(handles), frameon=False, bbox_to_anchor=(0.0, 0.965))
fig.text(0.01, 0.985, 'Topological accuracy per replicate (n = 10 per box; lower is better)', fontsize=10, va='top')
fig.tight_layout(rect=(0, 0, 1, 0.92))
for ext in ['png', 'pdf']:
    fig.savefig(ROOT / 'results' / f'rf_boxplots.{ext}', dpi=200, facecolor=SURF)
print('saved', ROOT / 'results' / 'rf_boxplots.png', 'methods:', methods)
