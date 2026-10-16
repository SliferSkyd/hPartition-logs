"""RF of the PsiPartition authors' original results (IQ-TREE 1.6.12, PsiPartition/data/DNA) vs true trees
-> results/psi_orig_per_rep.csv"""
import csv
from pathlib import Path
from ete3 import Tree
P = Path('/home/diepht/sliferskyd/hPartition/PsiPartition/data/DNA')
sets = {'SimDNA1': ('simulated', {'PsiPartition': 'SortPartition', 'PsiPartitionFast': 'SortPartitionFast'}),
        'SimDNA2': ('simulated-seqlen', {'PsiPartition': 'PsiPartition', 'PsiPartitionFast': 'PsiPartitionFast'})}
rows = []
for ds, (d, ren) in sets.items():
    for cat in sorted((P / d).glob('l*_loci_*')) + sorted((P / d).glob('loci_*')):
        for true in cat.glob('*.tree'):
            rep = true.stem; t = Tree(str(true))
            for m in ['PsiPartition', 'PsiPartitionFast', 'mPartition', 'noPartition', 'RatePartition-4', 'RatePartition-5']:
                tf = P / d / ren.get(m, m) / cat.name / (f'par.{rep}.treefile' if m == 'mPartition' else f'{rep}.treefile')
                if not tf.exists():
                    continue
                rf, mx, *_ = t.robinson_foulds(Tree(str(tf)), unrooted_trees=True)
                rows.append(dict(dataset=ds, loci=int(cat.name.split('_')[-1]), rep=int(rep), method=m + '(iq1.6)', RF=rf, maxRF=mx))
with open('results/psi_orig_per_rep.csv', 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
print(len(rows), 'rows')
