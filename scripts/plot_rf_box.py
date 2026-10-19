"""Replacement for Figures 2 and 3: RF distance distributions, not averages.

The reviewer asked whether hPartition's advantage is consistent across replicates or driven by a few
alignments, so each locus count is shown as a box over its 10 replicate alignments (median, IQR, 1.5*IQR
whiskers). No individual points are drawn, and the figure carries no title: the caption supplies it.
The paired per-alignment statistics are reported in the Results text instead of a second panel.
"""
import csv
import collections
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

R = Path('/home/diepht/sliferskyd/hPartition/rerun_sim')
OUT = Path('/home/diepht/sliferskyd/hPartition/hPartition__PeerJ_')
METHODS = ['hPartition', 'gPartition', 'PsiPartition']
BLUE, ORANGE, AQUA = '#2a78d6', '#eb6834', '#1baf7a'
COL = dict(zip(METHODS, [BLUE, ORANGE, AQUA]))
INK, INK2, GRID = '#1f1f1e', '#5f5e5a', '#e4e3df'
plt.rcParams.update({'font.size': 9, 'font.family': 'DejaVu Sans', 'text.color': INK,
                     'axes.labelcolor': INK, 'xtick.color': INK2, 'ytick.color': INK2,
                     'axes.edgecolor': INK2, 'axes.linewidth': 0.8})

rows = [r for r in csv.DictReader(open(R / 'results' / 'per_rep.csv')) if r['method'] in METHODS]
data = collections.defaultdict(list)          # (dataset, loci, method) -> [RF]
paired = collections.defaultdict(dict)        # (dataset, loci, rep) -> {method: RF}
for r in rows:
    key = (r['dataset'], int(r['loci']))
    data[key + (r['method'],)].append(int(r['RF']))
    paired[(r['dataset'], int(r['loci']), r['rep'])][r['method']] = int(r['RF'])


def style(bp, colour):
    for b in bp['boxes']:
        b.set(facecolor=colour + '55', edgecolor=colour, linewidth=1.1)
    for w in bp['whiskers'] + bp['caps']:
        w.set(color=colour, linewidth=1.0)
    for med in bp['medians']:
        med.set(color=INK, linewidth=1.6)


def panel(ax, ds, loci):
    W = 0.26
    for mi, m in enumerate(METHODS):
        off = (mi - 1) * W
        vals = [data[(ds, L, m)] for L in loci]
        bp = ax.boxplot(vals, positions=[i + off for i in range(len(loci))], widths=W * 0.86,
                        patch_artist=True, showfliers=False, showcaps=True, whis=1.5, zorder=3)
        style(bp, COL[m])
    ax.set_xticks(range(len(loci)))
    ax.set_xticklabels(loci)
    ax.set_xlim(-0.6, len(loci) - 0.4)
    ax.yaxis.grid(True, color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)
    for s in ('top', 'right'):
        ax.spines[s].set_visible(False)


def diff_panel(ax, ds, loci):
    """Paired per-alignment difference: competitor RF minus hPartition RF. >0 means hPartition is closer."""
    W = 0.34
    for mi, m in enumerate([x for x in METHODS if x != 'hPartition']):
        off = (mi - 0.5) * W
        vals = []
        for L in loci:
            d = [p[m] - p['hPartition'] for k, p in paired.items()
                 if k[0] == ds and k[1] == L and m in p and 'hPartition' in p]
            vals.append(d)
        bp = ax.boxplot(vals, positions=[i + off for i in range(len(loci))], widths=W * 0.86,
                        patch_artist=True, showfliers=False, whis=1.5, zorder=3)
        style(bp, COL[m])
    ax.axhline(0, color=INK, linewidth=1.0, zorder=4)
    ax.set_xticks(range(len(loci)))
    ax.set_xticklabels(loci)
    ax.set_xlim(-0.6, len(loci) - 0.4)
    ax.yaxis.grid(True, color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)
    for s in ('top', 'right'):
        ax.spines[s].set_visible(False)


for ds, fname in [('SimDNA1', 'fig2-Simulated_DNA1.png'), ('SimDNA2', 'fig3-Simulated_DNA2.png')]:
    loci = sorted({L for (d, L, m) in data if d == ds})
    fig, ax = plt.subplots(figsize=(11.0, 5.0))
    fig.patch.set_facecolor('white')
    panel(ax, ds, loci)
    ax.set_ylabel('RF distance to true tree', fontsize=15)
    ax.set_xlabel('number of loci', fontsize=15)
    ax.tick_params(axis='both', labelsize=13)
    handles = [Patch(facecolor=COL[m] + '55', edgecolor=COL[m], linewidth=1.6, label=m) for m in METHODS]
    ax.legend(handles=handles, loc='upper left', frameon=False, ncol=3, fontsize=16,
              handlelength=2.2, handleheight=1.5, columnspacing=2.4, borderaxespad=0.2,
              handletextpad=0.7)
    ax.set_ylim(bottom=-1, top=max(max(v) for k, v in data.items() if k[0] == ds) * 1.16)
    fig.tight_layout()
    for q in (OUT / fname, R / 'results' / fname.replace('.png', '.pdf')):
        fig.savefig(q, dpi=300, facecolor='white')
    print('wrote', OUT / fname)
