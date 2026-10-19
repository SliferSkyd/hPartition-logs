"""Worked-example figure. Panels A-B are in input site order; from panel C onward the sites are reordered by
rate, so each seed subset -- and then each model -- is a consecutive block and can be followed down the figure.

Every rate and likelihood shown is computed with the same formulae and binary used for the benchmarks.
"""
import math
from itertools import combinations
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyArrowPatch

OUT = Path('/home/diepht/sliferskyd/hPartition/hPartition__PeerJ_')
TAXA = ['t1', 't2', 't3', 't4', 't5', 't6']
ALN = {'t1': 'ACGTAC' 'AAACC' 'ACGTA', 't2': 'ACGTAC' 'AAACC' 'CGTAC',
       't3': 'ACGTAC' 'AAGCC' 'GTACG', 't4': 'ACGTAC' 'AGACC' 'TACGT',
       't5': 'ACGTAC' 'AAACT' 'ACGTA', 't6': 'ACGTAC' 'AAACT' 'CGTAC'}
m = len(ALN['t1'])
JC = [-3.1164]*7 + [-4.93429, -4.93935, -3.1164, -6.92306] + [-10.0331]*5
HKY = [-2.48074, -2.83614, -4.11082, -4.07658, -2.48074, -2.83614, -2.48074, -4.67827,
       -4.56048, -2.83614, -7.03696, -9.73302, -9.9343, -10.6255, -10.6037, -9.73302]

BASE = {'A': '#2a78d6', 'C': '#eb6834', 'G': '#1baf7a', 'T': '#eda100'}
S = {1: '#9aa0a6', 2: '#1baf7a', 3: '#eda100', 4: '#eb6834'}
JCC, HKYC = '#9aa0a6', '#2a78d6'
INK, INK2, GRID, SURF, RED = '#1f1f1e', '#5f5e5a', '#e4e3df', '#ffffff', '#c0392b'
plt.rcParams.update({'font.size': 10, 'text.color': INK, 'xtick.color': INK2,
                     'ytick.color': INK2, 'axes.edgecolor': INK2})

sim = {(x, y): sum(a == b for a, b in zip(ALN[x], ALN[y])) for x, y in combinations(TAXA, 2)}
den = sum(sim.values())
rates = [1 - sum(s for (x, y), s in sim.items() if ALN[x][i] == ALN[y][i]) / den for i in range(m)]
k0 = 4
lo, hi = min(rates), max(rates)
w = (hi - lo) / k0
binof = [min(k0, int((r - lo) / w) + 1) for r in rates]

order = sorted(range(m), key=lambda i: (binof[i], i))      # reorder by rate from panel C on
pJC = []
for i in range(m):
    mn = min(JC[i], HKY[i]); a, b = math.exp(JC[i] - mn), math.exp(HKY[i] - mn)
    pJC.append(a / (a + b))
# model per seed: S1 -> JC, the rest -> HKY (S3 already merged into S4)
mdl = {i: ('JC' if binof[i] == 1 else 'HKY') for i in range(m)}

fig = plt.figure(figsize=(13.0, 12.4), facecolor=SURF)
gs = fig.add_gridspec(7, 1, height_ratios=[1.25, 0.76, 0.42, 0.42, 0.66, 0.82, 0.50], hspace=1.40,
                      left=0.165, right=0.905, top=0.960, bottom=0.050)
TITLE = dict(loc='left', fontsize=12, pad=9, color=INK)


def rowaxis(ax, label):
    ax.set_xlim(0, m); ax.set_ylim(0, 1); ax.set_xticks([]); ax.set_yticks([])
    for s_ in ax.spines.values(): s_.set_visible(False)
    ax.text(-0.012, .5, label, transform=ax.transAxes, ha='right', va='center',
            fontsize=10.5, color=INK)


def groupbrackets(ax, y, labels=True):
    """Draw a bracket under each consecutive seed block of the reordered axis."""
    start = 0
    for j in range(1, k0 + 1):
        n = sum(1 for i in order if binof[i] == j)
        if not n:
            continue
        ax.annotate('', xy=(start + .08, y), xytext=(start + n - .08, y), annotation_clip=False,
                    arrowprops=dict(arrowstyle='-', color=S[j], lw=2.2))
        if labels:
            ax.text(start + n / 2, y - .22, f'$S_{j}$  ($n={n}$)', ha='center', va='top',
                    fontsize=10, color=S[j], clip_on=False)
        start += n


# ---- A: alignment, input order ----------------------------------------
ax = fig.add_subplot(gs[0])
for r, t in enumerate(TAXA):
    for c in range(m):
        b = ALN[t][c]
        ax.add_patch(Rectangle((c, len(TAXA)-1-r), 1, 1, fc=BASE[b]+'44', ec='white', lw=1.1))
        ax.text(c+.5, len(TAXA)-.5-r, b, ha='center', va='center', fontsize=9, color=INK)
ax.set_xlim(0, m); ax.set_ylim(0, len(TAXA))
ax.set_yticks([len(TAXA)-.5-i for i in range(len(TAXA))]); ax.set_yticklabels(TAXA, fontsize=10)
ax.set_xticks([c+.5 for c in range(m)]); ax.set_xticklabels(range(1, m+1), fontsize=9.5)
ax.tick_params(length=0, pad=3)
for s_ in ax.spines.values(): s_.set_visible(False)
ax.set_title('A   Input: 6 taxa $\\times$ 16 sites, in alignment order', **TITLE)

# ---- B: Stage 1, input order ------------------------------------------
ax = fig.add_subplot(gs[1])
cols = [S[1] if r == 0 else HKYC for r in rates]
ax.bar([c+.5 for c in range(m)], rates, width=.7, color=[c+'77' for c in cols],
       edgecolor=cols, linewidth=1.3)
for c, r in enumerate(rates):
    ax.text(c+.5, r+.05, f'{r:.2f}', ha='center', fontsize=8.6, color=INK2)
for j in range(1, k0):
    ax.axhline(lo+j*w, color=INK2, lw=.9, ls=':')
ax.set_xlim(0, m); ax.set_ylim(0, hi*1.3); ax.set_xticks([])
ax.set_ylabel('rate $r_i$', fontsize=10.5); ax.tick_params(axis='y', labelsize=9.5)
ax.yaxis.grid(True, color=GRID, lw=.8); ax.set_axisbelow(True)
for s_ in ('top', 'right'): ax.spines[s_].set_visible(False)
ax.set_title('B   Stage 1 — site rates.  All eight invariant columns get rate exactly 0 (grey); '
             'dotted lines are the bin edges', **TITLE)

# ---- C: Stage 2, reordered --------------------------------------------
ax = fig.add_subplot(gs[2]); rowaxis(ax, 'sites, sorted\nby rate')
for pos, i in enumerate(order):
    j = binof[i]
    ax.add_patch(Rectangle((pos+.06, .30), .88, .62, fc=S[j]+'55', ec=S[j], lw=1.3))
    ax.text(pos+.5, .61, str(i+1), ha='center', va='center', fontsize=9, color=INK)
groupbrackets(ax, .16)
ax.text(8.6, -.88, '$S_3$ holds 1 site $<\\tau$ → merged into $S_4$', ha='left', va='center',
        fontsize=10, color=RED, clip_on=False)

ax.set_title('C   Stage 2 — sites sorted by rate fall into consecutive equal-width bins; '
             'all invariant sites form one block', **TITLE)

# ---- D: Stage 3, same order -------------------------------------------
ax = fig.add_subplot(gs[3]); rowaxis(ax, 'fitted model')
start = 0
for j in [1, 2, 4]:
    n = sum(1 for i in order if binof[i] in ([3, 4] if j == 4 else [j]))
    col = JCC if j == 1 else HKYC
    nm = 'JC' if j == 1 else 'HKY'
    ax.add_patch(Rectangle((start+.06, .30), n-.12, .62, fc=col+'55', ec=col, lw=1.6))
    ax.text(start+n/2, .61, nm, ha='center', va='center', fontsize=11, color=INK)
    start += n
ax.annotate('', xy=(8.3, .10), xytext=(15.9, .10), annotation_clip=False,
            arrowprops=dict(arrowstyle='-', color=RED, lw=1.8))
ax.text(12.1, -.18, 'near-identical $Q$ (corr $>\\epsilon$) → united into $S_{\\mathrm{HKY}}$',
        ha='center', va='top', fontsize=10, color=RED, clip_on=False)
ax.set_title('D   Stage 3 — one ModelFinder call fits a model per seed; each block is now one model',
             **TITLE)

# ---- E: per-site likelihoods ------------------------------------------
ax = fig.add_subplot(gs[4]); rowaxis(ax, '')
vals = [JC, HKY]
vmin, vmax = min(min(JC), min(HKY)), max(max(JC), max(HKY))
for row, (nm, v, col) in enumerate([('$S_{\\mathrm{JC}}$', JC, JCC), ('$S_{\\mathrm{HKY}}$', HKY, HKYC)]):
    for pos, i in enumerate(order):
        f = (v[i] - vmin) / (vmax - vmin)
        ax.add_patch(Rectangle((pos+.06, .52-row*.46), .88, .40,
                               fc=col + f'{int(25+200*f):02x}', ec='white', lw=.9))
        best = (v[i] >= max(JC[i], HKY[i]))
        ax.text(pos+.5, .72-row*.46, f'{v[i]:.1f}', ha='center', va='center',
                fontsize=7.6, color=INK, fontweight='bold' if best else 'normal')
        if best:
            ax.add_patch(Rectangle((pos+.06, .52-row*.46), .88, .40, fc='none', ec=INK, lw=1.5))
    ax.text(-0.012, .72-row*.46, nm, transform=ax.transAxes, ha='right', va='center',
            fontsize=11, color=INK)
ax.set_title('E   Stage 4a — per-site log-likelihood under every candidate model, on the fixed tree $T$ '
             '(outlined cell = higher)', **TITLE)

# ---- F: assignment ----------------------------------------------------
ax = fig.add_subplot(gs[5])
ax.set_xlim(0, m); ax.set_ylim(0, 1)
for pos, i in enumerate(order):
    if rates[i] == 0:
        ax.add_patch(Rectangle((pos+.06, 0), .88, pJC[i], fc=JCC+'99', ec=JCC, lw=1.3, ls='--'))
        ax.add_patch(Rectangle((pos+.06, pJC[i]), .88, 1-pJC[i], fc=HKYC+'44', ec=HKYC, lw=1.3, ls='--'))
        ax.text(pos+.5, pJC[i]/2, f'{pJC[i]:.2f}', ha='center', va='center', fontsize=8, color=INK)
        ax.text(pos+.5, pJC[i]+(1-pJC[i])/2, f'{1-pJC[i]:.2f}', ha='center', va='center',
                fontsize=8, color=INK)
    else:
        win = JCC if JC[i] > HKY[i] else HKYC
        lab = 'JC' if JC[i] > HKY[i] else 'HKY'
        ax.add_patch(Rectangle((pos+.06, 0), .88, 1, fc=win+'cc', ec=win, lw=1.5))
        ax.text(pos+.5, .5, lab, ha='center', va='center', fontsize=8.6, color='white',
                fontweight='bold', rotation=90)
ax.set_xticks([p+.5 for p in range(m)]); ax.set_xticklabels([i+1 for i in order], fontsize=9.5)
ax.set_yticks([0, .5, 1]); ax.set_yticklabels(['0', '0.5', '1'], fontsize=9.5)
ax.set_ylabel('assignment', fontsize=10.5); ax.set_xlabel('site (sorted by rate)', fontsize=10.5)
ax.tick_params(length=0)
for s_ in ('top', 'right'): ax.spines[s_].set_visible(False)
ax.set_title('F   Stage 4b — variant sites take the higher-likelihood model outright; invariant sites are '
             'sampled, breaking up the $S_1$ block', **TITLE)

# ---- G: stages 5-6 ----------------------------------------------------
ax = fig.add_subplot(gs[6]); ax.axis('off')
inv = [i for i in range(m) if rates[i] == 0]
nJC = sum(pJC[i] for i in inv) + sum(1 for i in range(m) if rates[i] > 0 and JC[i] > HKY[i])
ax.add_patch(Rectangle((0.000, .70), .014, .22, transform=ax.transAxes, fc=HKYC+'cc', ec=HKYC,
                       lw=1.4, clip_on=False))
ax.text(0.022, .81, 'variant site: solid bar, assigned by $\\arg\\max$', transform=ax.transAxes,
        va='center', fontsize=10.5, color=INK)
ax.add_patch(Rectangle((0.420, .70), .014, .22, transform=ax.transAxes, fc=JCC+'99', ec=JCC,
                       lw=1.4, ls='--', clip_on=False))
ax.text(0.442, .81, 'invariant site: dashed bar, split by sampling probability',
        transform=ax.transAxes, va='center', fontsize=10.5, color=INK)
ax.text(0, .40, f'Stage 5 — both subsets hold more than $\\tau$ sites '
        f'($\\approx${nJC:.0f} and $\\approx${m-nJC:.0f}), so nothing is dissolved.',
        transform=ax.transAxes, fontsize=10.8, va='top', color=INK)
ax.text(0, .04, 'Stage 6 (optional, -hPartition-pf) — the one available merge is tested and kept only if '
        'it lowers the criterion.', transform=ax.transAxes, fontsize=10.8, va='top', color=INK)
ax.set_title('G   Stages 5 and 6 — cleanup and optional merging', **TITLE)

for ext in ('png', 'pdf'):
    fig.savefig(OUT / f'fig-worked-example.{ext}', dpi=300, facecolor=SURF)
print('wrote', OUT / 'fig-worked-example.png')
