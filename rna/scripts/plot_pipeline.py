"""Figure documenting how the beetle mitogenome dataset was prepared: the record-filtering funnel,
the per-gene assembly pipeline, and the composition of the resulting alignment."""
import re
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Rectangle

D = Path('/home/diepht/sliferskyd/hPartition/rna_datasets/beetle')
BLUE, ORANGE, AQUA, YELLOW = '#2a78d6', '#eb6834', '#1baf7a', '#eda100'
INK, INK2, GRID, SURF = '#1f1f1e', '#5f5e5a', '#e4e3df', '#fcfcfb'
plt.rcParams.update({'font.size': 9, 'text.color': INK, 'axes.labelcolor': INK,
                     'xtick.color': INK2, 'ytick.color': INK2, 'axes.edgecolor': INK2})

rows = [tuple(map(int, l.split())) for l in open(D / 'counts.txt')]
ge12 = [r for r in rows if r[0] >= 12]
funnel = [('Accessions in Timmermans et al.\nTable S1, fetched from ENA', len(rows), BLUE),
          ('Have >=12 of 13 protein-coding genes', len(ge12), BLUE),
          ('...and both rRNA genes annotated\n(dataset used)', sum(1 for r in ge12 if r[1] >= 2), AQUA)]
losses = [('no annotation at all', sum(1 for r in rows if r[0] == 0)),
          ('<12 protein-coding genes', sum(1 for r in rows if 0 < r[0] < 12)),
          ('rRNA genes not annotated', sum(1 for r in ge12 if r[1] == 0)),
          ('only 1 rRNA gene annotated', sum(1 for r in ge12 if r[1] == 1))]

fig = plt.figure(figsize=(11.5, 7.2), facecolor=SURF)
gs = fig.add_gridspec(2, 2, height_ratios=[1, 1.05], width_ratios=[1.25, 1],
                      hspace=0.5, wspace=0.3, left=0.26, right=0.97)

# --- A: filtering funnel -------------------------------------------------
ax = fig.add_subplot(gs[0, :]); ax.set_facecolor(SURF)
for i, (lab, n, c) in enumerate(funnel):
    ax.barh(i, n, height=0.52, color=c + '55', edgecolor=c, linewidth=1.2)
    ax.text(n + 4, i, f'{n}', va='center', ha='left', fontweight='bold', color=INK)
    ax.text(-6, i, lab, va='center', ha='right', fontsize=8.5, color=INK)
ax.set_yticks([]); ax.set_ylim(2.6, -0.6); ax.set_xlim(0, 390)
ax.set_xlabel('records')
ax.set_title('A  Which published accessions could be used, and why most could not',
             loc='left', fontsize=10.5, color=INK, pad=8)
for s in ('top', 'right', 'left'):
    ax.spines[s].set_visible(False)
ax.xaxis.grid(True, color=GRID, linewidth=0.8); ax.set_axisbelow(True)
txt = '\n'.join(f'  -{n:>4}   {lab}' for lab, n in losses)
ax.text(0.70, 0.50, 'records excluded:\n' + txt, transform=ax.transAxes, fontsize=8.3,
        va='center', family='monospace', color=INK2,
        bbox=dict(boxstyle='round,pad=0.6', fc='white', ec=GRID))

# --- B: pipeline ---------------------------------------------------------
ax = fig.add_subplot(gs[1, 0]); ax.set_facecolor(SURF); ax.axis('off')
ax.set_title('B  Per-gene assembly pipeline', loc='left', fontsize=10.5, color=INK, pad=6)
steps = [('ENA records (EMBL, annotated)', BLUE),
         ('extract CDS / rRNA / tRNA features', BLUE),
         ('normalise gene names;\nsplit duplicate Leu & Ser tRNAs by anticodon', BLUE),
         ('CDS: translate (code 5) -> MAFFT -> back-translate\nrRNA & tRNA: MAFFT on nucleotides', ORANGE),
         ('mask 5 gene copies that translate with internal stops\n(4x cox1, 1x nad5; 3,615 sites -> gaps)', YELLOW),
         ('concatenate 37 genes; write charsets\n(per gene, per codon position, rRNA, tRNA)', AQUA)]
for i, (lab, c) in enumerate(steps):
    y = 1 - i * 0.172
    ax.add_patch(Rectangle((0.02, y - 0.079), 0.96, 0.113, transform=ax.transAxes,
                           fc=c + '22', ec=c, lw=1.1, zorder=1))
    ax.text(0.5, y - 0.023, lab, transform=ax.transAxes, ha='center', va='center',
            fontsize=8.2, color=INK, zorder=2)
    if i < len(steps) - 1:
        ax.add_patch(FancyArrowPatch((0.5, y - 0.082), (0.5, y - 0.138), transform=ax.transAxes,
                                     arrowstyle='-|>', mutation_scale=9, color=INK2, lw=1))
ax.text(0.02, -0.08, 'no trimming applied; no alignment columns removed', transform=ax.transAxes,
        fontsize=8, style='italic', color=INK2)

# --- C: composition ------------------------------------------------------
ax = fig.add_subplot(gs[1, 1]); ax.set_facecolor(SURF)
cs = dict((m[0], (int(m[1]), int(m[2]))) for m in
          re.findall(r'charset (\S+) = (\d+)-(\d+);', (D / 'aln' / 'beetle.genes.nex').read_text()))
PCG = ['atp6', 'atp8', 'cox1', 'cox2', 'cox3', 'cob', 'nad1', 'nad2', 'nad3', 'nad4', 'nad4l', 'nad5', 'nad6']
pcg = sum(b - a + 1 for g, (a, b) in cs.items() if g in PCG)
rrna = sum(b - a + 1 for g, (a, b) in cs.items() if g.startswith('rrn'))
trna = sum(b - a + 1 for g, (a, b) in cs.items() if g.startswith('trn'))
tot = pcg + rrna + trna
left = 0
for lab, v, c in [(f'13 protein-coding\n{pcg:,} sites', pcg, BLUE),
                  (f'2 rRNA\n{rrna:,}', rrna, ORANGE),
                  (f'22 tRNA\n{trna:,}', trna, AQUA)]:
    ax.barh(0, v, left=left, height=0.42, color=c + '55', edgecolor=c, linewidth=1.2)
    ax.text(left + v / 2, 0, lab, ha='center', va='center', fontsize=8.2, color=INK)
    left += v
ax.barh(-0.55, rrna + trna, left=pcg, height=0.2, color=YELLOW + '55', edgecolor=YELLOW, linewidth=1.2)
ax.text(pcg + (rrna + trna) / 2, -0.85, f'structural RNA  {(rrna+trna)/tot:.1%}', ha='center', va='center',
        fontsize=8.4, color=INK)
ax.set_xlim(0, tot); ax.set_ylim(-1.2, 0.5); ax.set_yticks([])
ax.set_xlabel('alignment position')
ax.set_title(f'C  Composition: 52 taxa x {tot:,} sites, 37 loci', loc='left', fontsize=10.5, color=INK, pad=6)
for s in ('top', 'right', 'left'):
    ax.spines[s].set_visible(False)

fig.text(0.012, 0.985, 'Preparation of the beetle mitogenome dataset '
         '(accessions from Timmermans et al. 2016, Genome Biol Evol 8:161)',
         fontsize=11, va='top', color=INK)

out = Path('/home/diepht/sliferskyd/hPartition/rerun_sim/results')
for ext in ('png', 'pdf'):
    fig.savefig(out / f'beetle_pipeline.{ext}', dpi=200, facecolor=SURF)
print('saved', out / 'beetle_pipeline.png')
