"""Worked-example figure: a 6-taxon, 17-site alignment traced through all six stages.

Panels A-B are in alignment order; from panel C the sites are sorted by rate, so each seed subset, and then
each model, is a consecutive block that can be followed down the figure. Rates and log-likelihoods are
computed with the same formulae and binary used for the benchmarks; the invariant draw uses seed 0.
"""
import math
import random
from itertools import combinations
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyArrowPatch

OUT = Path('/home/diepht/sliferskyd/hPartition/hPartition__PeerJ_')
TAXA = ['t1', 't2', 't3', 't4', 't5', 't6']
# alignment order is deliberately mixed so that the Stage-2 sort has visible work to do
COLS = ['ACGTAC', 'AAAAAA', 'AACCAA', 'CGTACG', 'AAAAAG', 'GGGGGG', 'GGTTGG', 'GTACGT', 'CCCCCT',
        'ACGAAC', 'AAGGAA', 'TACGTA', 'CCCCCC', 'GGGGGA', 'CCTTCC', 'ACGTAC', 'CGTACG']
m = len(COLS)
ALN = {t: ''.join(c[i] for c in COLS) for i, t in enumerate(TAXA)}
MODELS = ['JC', 'F81', 'HKY', 'GTR']
# per-site log-likelihoods, IQ-TREE on the fixed tree (t1,t2,(t3,t4),(t5,t6)), reindexed to COLS order
_L = {'JC':  [-4.14, -4.14, -4.14, -6.78, -6.78, -6.78, -4.76, -4.76, -4.76, -4.76, -9.07, -9.07, -9.07, -9.07, -9.07, -9.07, -9.07],
      'F81': [-3.77, -4.02, -4.11, -6.28, -7.30, -6.49, -4.25, -5.43, -4.29, -5.37, -8.01, -8.91, -9.01, -9.09, -9.80, -8.91, -9.01],
      'HKY': [-3.56, -4.19, -3.83, -6.57, -7.88, -6.70, -4.11, -5.20, -4.32, -5.59, -8.33, -8.60, -8.65, -8.76, -9.45, -8.60, -8.65],
      'GTR': [-3.42, -3.69, -3.79, -6.45, -7.18, -6.66, -4.07, -5.31, -4.38, -5.68, -8.79, -8.46, -8.84, -8.16, -9.58, -8.46, -8.84]}
CANON = ['AAAAAA', 'CCCCCC', 'GGGGGG', 'AAAAAG', 'CCCCCT', 'GGGGGA', 'AACCAA', 'GGTTGG', 'AAGGAA',
         'CCTTCC', 'ACGAAC', 'ACGTAC', 'CGTACG', 'GTACGT', 'TACGTA', 'ACGTAC', 'CGTACG']
used = [False] * m
idx = []
for c in COLS:
    for j, d in enumerate(CANON):
        if d == c and not used[j]:
            used[j] = True; idx.append(j); break
L = {k: [v[j] for j in idx] for k, v in _L.items()}

MC = {'JC': '#9aa0a6', 'F81': '#1baf7a', 'HKY': '#eda100', 'GTR': '#2a78d6'}
BASE = {'A': '#2a78d6', 'C': '#eb6834', 'G': '#1baf7a', 'T': '#eda100'}
SC = {1: '#9aa0a6', 2: '#1baf7a', 3: '#eda100', 4: '#2a78d6'}
INK, INK2, GRID, SURF, RED = '#1f1f1e', '#5f5e5a', '#e4e3df', '#ffffff', '#c0392b'
plt.rcParams.update({'font.size': 12, 'text.color': INK, 'xtick.color': INK2,
                     'ytick.color': INK2, 'axes.edgecolor': INK2})
TAU = 3

sim = {(x, y): sum(a == b for a, b in zip(ALN[x], ALN[y])) for x, y in combinations(TAXA, 2)}
den = sum(sim.values())
rates = [1 - sum(s for (x, y), s in sim.items() if ALN[x][i] == ALN[y][i]) / den for i in range(m)]
k0 = 6
lo, hi = min(rates), max(rates)
w = (hi - lo) / k0
raw = [min(k0, int((r - lo) / w) + 1) for r in rates]
seedof = {b: j + 1 for j, b in enumerate(sorted(set(raw)))}          # relabel non-empty bins S1..S4
binof = [seedof[b] for b in raw]
order = sorted(range(m), key=lambda i: (binof[i], i))
seedmodel = {1: 'JC', 2: 'F81', 3: 'HKY', 4: 'GTR'}
inv = [i for i in range(m) if rates[i] == 0]

rng = random.Random(0)
assign, prob = {}, {}
for i in range(m):
    v = [L[x][i] for x in MODELS]
    if i in inv:
        mn = min(v); wt = [math.exp(x - mn) for x in v]; tot = sum(wt)
        prob[i] = [x / tot for x in wt]
        r = rng.random() * tot; c = 0
        for k, x in enumerate(wt):
            c += x
            if r < c: assign[i] = MODELS[k]; break
    else:
        assign[i] = MODELS[v.index(max(v))]
size = {x: sum(1 for i in assign if assign[i] == x) for x in MODELS}
small = [x for x in MODELS if size[x] < TAU]
moved = {}
for s in small:
    for i in [k for k, v in assign.items() if v == s]:
        alt = {x: L[x][i] for x in MODELS if x != s}
        moved[i] = max(alt, key=alt.get); assign[i] = moved[i]
final = {x: sum(1 for i in assign if assign[i] == x) for x in MODELS if size[x] >= TAU}

fig = plt.figure(figsize=(14.2, 14.4), facecolor=SURF)
gs = fig.add_gridspec(7, 1, height_ratios=[1.18, 0.72, 0.40, 0.40, 0.90, 0.78, 0.62], hspace=1.40,
                      left=0.160, right=0.912, top=0.964, bottom=0.085)
TITLE = dict(loc='left', fontsize=14, pad=10, color=INK)


def rowaxis(ax, label):
    ax.set_xlim(0, m); ax.set_ylim(0, 1); ax.set_xticks([]); ax.set_yticks([])
    for s_ in ax.spines.values(): s_.set_visible(False)
    ax.text(-0.010, .5, label, transform=ax.transAxes, ha='right', va='center',
            fontsize=12.5, color=INK)


# ---- A ----------------------------------------------------------------
ax = fig.add_subplot(gs[0])
for r, t in enumerate(TAXA):
    for c in range(m):
        b = ALN[t][c]
        ax.add_patch(Rectangle((c, len(TAXA)-1-r), 1, 1, fc=BASE[b]+'44', ec='white', lw=1.0))
        ax.text(c+.5, len(TAXA)-.5-r, b, ha='center', va='center', fontsize=10.2, color=INK)
ax.set_xlim(0, m); ax.set_ylim(0, len(TAXA))
ax.set_yticks([len(TAXA)-.5-i for i in range(len(TAXA))]); ax.set_yticklabels(TAXA, fontsize=12)
ax.set_xticks([c+.5 for c in range(m)]); ax.set_xticklabels(range(1, m+1), fontsize=10.5)
ax.tick_params(length=0, pad=3)
for s_ in ax.spines.values(): s_.set_visible(False)
ax.set_title('A   Input: 6 taxa $\\times$ 17 sites, in alignment order', **TITLE)

# ---- B ----------------------------------------------------------------
ax = fig.add_subplot(gs[1])
cols = [SC[1] if r == 0 else MC['GTR'] for r in rates]
ax.bar([c+.5 for c in range(m)], rates, width=.7, color=[c+'77' for c in cols],
       edgecolor=cols, linewidth=1.3)
for c, r in enumerate(rates):
    ax.text(c+.5, r+.045, f'{r:.2f}', ha='center', fontsize=9.6, color=INK2)
for j in range(1, k0):
    ax.axhline(lo+j*w, color=INK2, lw=.9, ls=':')
ax.set_xlim(0, m); ax.set_ylim(0, hi*1.30); ax.set_xticks([])
ax.set_ylabel('rate $r_i$', fontsize=12.5); ax.tick_params(axis='y', labelsize=11)
ax.yaxis.grid(True, color=GRID, lw=.8); ax.set_axisbelow(True)
for s_ in ('top', 'right'): ax.spines[s_].set_visible(False)
ax.set_title('B   Stage 1 — site rates.  The three invariant columns get rate exactly 0 (grey); '
             'dotted lines are the bin edges', **TITLE)

# ---- C ----------------------------------------------------------------
ax = fig.add_subplot(gs[2]); rowaxis(ax, 'sites, sorted\nby rate')
for pos, i in enumerate(order):
    j = binof[i]
    ax.add_patch(Rectangle((pos+.06, .32), .88, .60, fc=SC[j]+'55', ec=SC[j], lw=1.3))
    ax.text(pos+.5, .62, str(i+1), ha='center', va='center', fontsize=10.4, color=INK)
start = 0
for j in sorted(SC):
    n = sum(1 for i in order if binof[i] == j)
    ax.annotate('', xy=(start+.08, .18), xytext=(start+n-.08, .18), annotation_clip=False,
                arrowprops=dict(arrowstyle='-', color=SC[j], lw=2.2))
    ax.text(start+n/2, -.06, f'$S_{j}$ ($n={n}$)', ha='center', va='top', fontsize=11.5,
            color=SC[j], clip_on=False)
    start += n
ax.set_title('C   Stage 2 — sorted by rate, the sites fall into four non-empty equal-width bins',
             **TITLE)

# ---- D ----------------------------------------------------------------
ax = fig.add_subplot(gs[3]); rowaxis(ax, 'fitted model')
start = 0
for j in sorted(SC):
    n = sum(1 for i in order if binof[i] == j)
    nm = seedmodel[j]
    ax.add_patch(Rectangle((start+.06, .32), n-.12, .60, fc=MC[nm]+'55', ec=MC[nm], lw=1.6))
    ax.text(start+n/2, .62, nm, ha='center', va='center', fontsize=13, color=INK)
    start += n
ax.text(m/2, -.10, 'no two fitted matrices are near-identical here, so nothing is merged at this stage',
        ha='center', va='top', fontsize=11.3, color=INK2, clip_on=False)
ax.set_title('D   Stage 3 — one ModelFinder call fits a model per seed; four candidate models remain',
             **TITLE)

# ---- E ----------------------------------------------------------------
ax = fig.add_subplot(gs[4]); rowaxis(ax, '')
vmin = min(min(v) for v in L.values()); vmax = max(max(v) for v in L.values())
for row, nm in enumerate(MODELS):
    y = .80 - row*.235
    for pos, i in enumerate(order):
        f = (L[nm][i]-vmin)/(vmax-vmin)
        ax.add_patch(Rectangle((pos+.06, y-.10), .88, .20,
                               fc=MC[nm] + f'{int(22+205*f):02x}', ec='white', lw=.8))
        best = L[nm][i] >= max(L[x][i] for x in MODELS)
        ax.text(pos+.5, y, f'{L[nm][i]:.1f}', ha='center', va='center', fontsize=8.3,
                color=INK, fontweight='bold' if best else 'normal')
        if best:
            ax.add_patch(Rectangle((pos+.06, y-.10), .88, .20, fc='none', ec=INK, lw=1.4))
    ax.text(-0.010, y, '$S_{\\mathrm{%s}}$' % nm, transform=ax.transAxes, ha='right',
            va='center', fontsize=12.5, color=INK)
ax.set_title('E   Stage 4a — per-site log-likelihood under each candidate model, on the fixed tree $T$ '
             '(outlined = highest)', **TITLE)

# ---- F ----------------------------------------------------------------
ax = fig.add_subplot(gs[5])
ax.set_xlim(0, m); ax.set_ylim(0, 1)
for pos, i in enumerate(order):
    if i in inv:
        y = 0
        for k, nm in enumerate(MODELS):
            h = prob[i][k]
            ax.add_patch(Rectangle((pos+.06, y), .88, h, fc=MC[nm]+'77', ec=MC[nm], lw=1.0, ls='--'))
            if h > .19:
                ax.text(pos+.5, y+h/2, f'{h:.2f}', ha='center', va='center', fontsize=8.2, color=INK)
            y += h
    else:
        nm = assign[i] if i not in moved else [x for x in MODELS if L[x][i] == max(L[y][i] for y in MODELS)][0]
        ax.add_patch(Rectangle((pos+.06, 0), .88, 1, fc=MC[nm]+'cc', ec=MC[nm], lw=1.4))
        ax.text(pos+.5, .5, nm, ha='center', va='center', fontsize=9.4, color='white',
                fontweight='bold', rotation=90)
ax.set_xticks([p+.5 for p in range(m)]); ax.set_xticklabels([i+1 for i in order], fontsize=10.5)
ax.set_yticks([0, .5, 1]); ax.set_yticklabels(['0', '0.5', '1'], fontsize=11)
ax.set_ylabel('assignment', fontsize=12.5); ax.set_xlabel('site (sorted by rate)', fontsize=12.5)
ax.tick_params(length=0)
for s_ in ('top', 'right'): ax.spines[s_].set_visible(False)
ax.set_title('F   Stage 4b — variant sites take the best model outright (solid); '
             'invariant sites are sampled (dashed)', **TITLE)

# ---- G ----------------------------------------------------------------
ax = fig.add_subplot(gs[6]); rowaxis(ax, 'subsets after\nStage 4')
x = 0
for nm in MODELS:
    n = size[nm]
    bad = nm in small
    ax.add_patch(Rectangle((x+.06, .52), n-.12, .40, fc=MC[nm]+('33' if bad else '77'),
                           ec=RED if bad else MC[nm], lw=2.0 if bad else 1.4,
                           ls='--' if bad else '-'))
    ax.text(x+n/2, .72, f'$S_{{\\mathrm{{{nm}}}}}$  $n={n}$', ha='center', va='center',
            fontsize=11.4, color=RED if bad else INK)
    x += n
ax.text(sum(size[x_] for x_ in MODELS[:2])+size['HKY']/2 + 0.2, .34,
        f'$n<\\tau$ → dissolved; sites {", ".join(str(i+1) for i in sorted(moved))} go to their next-best model',
        ha='center', va='top', fontsize=11.4, color=RED, clip_on=False)
x = 0
for nm in [k for k in MODELS if k not in small]:
    n = final[nm]
    ax.add_patch(Rectangle((x+.06, -.30), n-.12, .36, fc=MC[nm]+'99', ec=MC[nm], lw=1.6))
    ax.text(x+n/2, -.12, f'$S_{{\\mathrm{{{nm}}}}}$  $n={n}$', ha='center', va='center',
            fontsize=11.4, color=INK)
    x += n
ax.text(-0.010, -.12, 'final scheme', transform=ax.transAxes, ha='right', va='center',
        fontsize=12.5, color=INK)
ax.text(0, -.74, f'Stage 6 (optional, -hPartition-pf) — the remaining {len(final)} subsets are tested '
        'pairwise and merged only where that lowers the criterion.',
        transform=ax.transAxes, fontsize=12, va='top', color=INK)
ax.set_title('G   Stage 5 — subsets below the minimum size are dissolved and their sites redistributed',
             **TITLE)

for ext in ('png', 'pdf'):
    fig.savefig(OUT / f'fig-worked-example.{ext}', dpi=300, facecolor=SURF)
print('wrote', OUT / 'fig-worked-example.png')
print(f'  seeds {len(SC)}; after Stage 4 {size}; dissolved {small}; final {final}')
