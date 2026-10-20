"""Measure how diffuse the Stage-4 sampling distribution is for invariant sites.

For each site i, hPartition samples subset j with probability proportional to exp(L[i][j]).
This reads the replayed L matrix and reports, separately for invariant and variant sites:
  max_j P(i->j)      how much mass the best model takes (1.0 = argmax; 1/n = flat)
  n_eff = 1/sum P^2  how many models the site effectively chooses between
"""
import sys, re, math, glob, os
import statistics as st

R = '/home/diepht/sliferskyd/hPartition/rerun_sim'
D = '/home/diepht/sliferskyd/hPartition-datasets/DNA/empirical'

def invariant_mask(phy):
    seqs = []
    for ln in open(phy).read().split('\n')[1:]:
        p = ln.split(None, 1)
        if len(p) == 2:
            seqs.append(p[1].replace(' ', '').upper())
    return [len(set(c for c in col if c in 'ACGT')) <= 1 for col in zip(*seqs)]

def load_rows(d):
    rows = []
    for f in sorted(glob.glob(f'{d}/row*.txt'), key=lambda x: int(re.search(r'row(\d+)', x).group(1))):
        txt = open(f).read().split('\n')
        vals = txt[1].split()[1:] if len(txt) > 1 else []
        if vals:
            rows.append([float(v) for v in vals])
    return rows

def stats(L, idx):
    """L is n_models x n_sites; idx selects sites."""
    mx, ne = [], []
    n = len(L)
    for i in idx:
        col = [L[j][i] for j in range(n)]
        m = max(col)
        w = [math.exp(v - m) for v in col]          # stable softmax
        s = sum(w)
        p = [x / s for x in w]
        mx.append(max(p))
        ne.append(1.0 / sum(x * x for x in p))
    return mx, ne

for ds in sys.argv[1:]:
    d = f'{R}/diffuse/{ds}'
    L = load_rows(d)
    if not L:
        print(f'{ds}: no rows yet'); continue
    inv = invariant_mask(f'{D}/{ds}.phy')
    m = min(len(L[0]), len(inv))
    I = [i for i in range(m) if inv[i]]
    V = [i for i in range(m) if not inv[i]]
    print(f'\n=== {ds}: {len(L)} models x {m} sites  ({len(I)} invariant, {len(V)} variant)')
    print(f'  {"":12}{"max P  median":>16}{"mean":>9}{"   |":>4}{"n_eff  median":>16}{"mean":>9}')
    for name, idx in (('invariant', I), ('variant', V)):
        if not idx: continue
        mx, ne = stats(L, idx)
        print(f'  {name:12}{st.median(mx):>16.3f}{st.mean(mx):>9.3f}{"   |":>4}'
              f'{st.median(ne):>16.1f}{st.mean(ne):>9.1f}')
    print(f'  (flat distribution over {len(L)} models would give max P = {1/len(L):.3f}, n_eff = {len(L)})')
