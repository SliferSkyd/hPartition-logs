"""Per-replicate RF distances (vs. true tree), BIC and wall time for all methods -> results/per_rep.csv,
plus per-category summary (mean/sd/median/IQR/min/max) -> results/summary.csv.
RF as in the old summarize.py: ete3 robinson_foulds(unrooted_trees=True)."""
import csv
import os
import re
import statistics as st
from pathlib import Path

from ete3 import Tree

ROOT = Path('/home/diepht/sliferskyd/hPartition/rerun_sim')
DATA = Path('/home/diepht/sliferskyd/hPartition-datasets/DNA')


def wall(p):
    """Elapsed wall-clock seconds from /usr/bin/time -v output."""
    try:
        m = re.search(r'Elapsed \(wall clock\) time.*: (\S+)', p.read_text())
    except OSError:
        return None
    if not m:
        return None
    parts = [float(x) for x in m.group(1).split(':')]
    return sum(v * 60 ** i for i, v in enumerate(reversed(parts)))


def bic(p):
    try:
        m = re.search(r'Bayesian information criterion \(BIC\) score: (\S+)', p.read_text())
        return float(m.group(1)) if m else None
    except OSError:
        return None


def files(method, sim, cat, rep):
    o = ROOT / 'out' / method / sim / cat / rep
    if method.startswith('PsiPartition'):
        o = ROOT / 'out' / 'PsiPartition' / sim / cat / rep
        v = 'last' if method == 'PsiPartition-last' else 'final'  # final = authors' best-config rerun
        return o / f'{v}.nwk', o / f'{rep}.{v}.iqtree', [o / 'time.txt']
    pre = 'hPartition' if method == 'hPartition' else 'gPartition'
    return (o / 'partition' / 'aln.treefile', o / 'partition' / 'aln.iqtree',
            [o / pre / 'time.txt', o / 'partition' / 'time.txt'])


def nloci(cat):
    return int(cat.split('_')[-1])


rows = []
for sim in ['simulated-1', 'simulated-2']:
    for catdir in sorted((DATA / sim).iterdir(), key=lambda d: nloci(d.name)):
        for true in sorted(catdir.glob('*.tree'), key=lambda p: int(p.stem)):
            rep = true.stem
            t_true = Tree(str(true))
            for method in ['hPartition', 'gPartition', 'PsiPartition', 'PsiPartition-last']:
                tf, iq, tms = files(method, sim, catdir.name, rep)
                tag = {'hPartition': 'hpar', 'gPartition': 'gpar'}.get(method, 'psi')
                if not (ROOT / 'done' / f'{tag}.{sim}.{catdir.name}.{rep}.ok').exists():
                    continue  # unfinished: IQ-TREE writes intermediate .treefile during search
                rf, max_rf, *_ = t_true.robinson_foulds(Tree(str(tf)), unrooted_trees=True)
                ws = [wall(t) for t in tms]
                rows.append(dict(dataset='SimDNA1' if sim == 'simulated-1' else 'SimDNA2', loci=nloci(catdir.name),
                                 rep=int(rep), method=method, RF=rf, maxRF=max_rf, nRF=rf / max_rf,
                                 BIC=bic(iq), wall_s=sum(w for w in ws if w) if all(ws) else None))

out = ROOT / 'results'
out.mkdir(exist_ok=True)
with open(out / 'per_rep.csv', 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys()) if rows else ['dataset'])
    w.writeheader()
    w.writerows(rows)

groups = {}
for r in rows:
    groups.setdefault((r['dataset'], r['loci'], r['method']), []).append(r['RF'])
with open(out / 'summary.csv', 'w', newline='') as f:
    w = csv.writer(f)
    w.writerow(['dataset', 'loci', 'method', 'n', 'mean_RF', 'sd_RF', 'median_RF', 'q1', 'q3', 'min', 'max'])
    for (d, l, m), v in sorted(groups.items()):
        q = st.quantiles(v, n=4) if len(v) > 1 else [v[0]] * 3
        w.writerow([d, l, m, len(v), f'{st.mean(v):.2f}', f'{st.stdev(v):.2f}' if len(v) > 1 else '',
                    st.median(v), q[0], q[2], min(v), max(v)])
print(f'{len(rows)} rows -> {out}/per_rep.csv, summary.csv')
