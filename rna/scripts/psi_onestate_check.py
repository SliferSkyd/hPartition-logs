"""For one alignment: does any PsiPartition configuration avoid IQ-TREE's 'Only one state is observed in
partition' error? The site order (sorting) depends only on the weights w, so compute it once per w and test
every k in 2..30 with PsiPartition's own binning (np.digitize over linspace(min, max, k), as in
PsiPartition_wandb.py). A bin fails when all its sites together show <= 1 nucleotide state.
Usage: psi_onestate_check.py ALN.fasta  -> one TSV line per (w, k) on stdout."""
import sys

import numpy as np

sys.path.insert(0, '/home/diepht/sliferskyd/hPartition/PsiPartition')
from Bio import AlignIO  # noqa: E402

from PsiPartition_wandb import calculate_sorting  # noqa: E402

aln = sys.argv[1]
cols = list(zip(*[str(r.seq) for r in AlignIO.read(aln, 'fasta')]))
inv = sum(len(set(c) - set('-N')) <= 1 for c in cols) / len(cols)
rng = np.random.default_rng(0)
weights = {'equal': [0.2] * 5}
for i in range(2):
    weights[f'random{i}'] = list(rng.uniform(0, 1, 5))
for name, ws in weights.items():
    w = dict(zip('ACGT-', np.array(ws) / sum(ws)))
    _, sorting = calculate_sorting(aln, 'fasta', 'dna', w)
    for k in range(2, 31):
        idx = np.digitize(sorting, np.linspace(sorting.min(), sorting.max(), k))
        bad = 0
        for b in np.unique(idx):
            states = set()
            for j in np.where(idx == b)[0]:
                states |= set(cols[j]) - set('-N')
            bad += len(states) <= 1
        print(f'{aln.split("/")[-1][:-6]}\t{inv:.3f}\t{name}\t{k}\t{len(np.unique(idx))}\t{bad}', flush=True)
