#!/bin/bash
unset LD_LIBRARY_PATH
O=/home/diepht/sliferskyd/hPartition/rerun_sim/memcap/out/psi_stream
/home/diepht/anaconda3/bin/python -I - <<'PY' > $O/psi_stream.txt 2>&1
import os
import numpy as np
from collections import defaultdict

aa_str = "ARNDCQEGHILKMFPSTWYV-"
PHY = "/home/diepht/sliferskyd/hPartition-datasets/Protein/Ran5.phy"
def hwm():
    for l in open("/proc/self/status"):
        if l.startswith("VmHWM"): return int(l.split()[1])/1048576

ls = open(PHY).read().split("\n")
n, M = map(int, ls[0].split())
msa = [l.split()[1] for l in ls[1:n+1]]
m = 400
msa = [s[:m] for s in msa]
print("node:", os.uname().nodename, "| taxa", n, "| sites used", m)

# --- site partitions: PsiPartition_wandb.py:24-33, verbatim ---
sp = []
for s in zip(*msa):
    p = defaultdict(list)
    for i, c in enumerate(s):
        (p[c] if c in aa_str[:-1] else p['-']).append(i)
    sp.append({k: frozenset(v) for k, v in p.items()})

def f(i, j):                       # corr[i,j], lines 36-44 verbatim
    s = 0
    for c2, p2 in sp[j].items():
        for c1, p1 in sp[i].items():
            if p2.issubset(p1):
                s += 1
                break
    return s/len(sp[j]) if s else 0

# --- A: as published, full m x m ---
corr = np.ones((m, m))
for i in range(m):
    for j in range(m):
        if i != j: corr[i, j] = f(i, j)
sort_A = (corr < corr.T).sum(1)

# --- B: same statistic, streaming, no matrix ---
sort_B = np.zeros(m, dtype=int)
for i in range(m):
    for j in range(m):
        if i != j and f(i, j) < f(j, i): sort_B[i] += 1

print("corr symmetric?            ", np.allclose(corr, corr.T))
print("max |corr - corr.T|        : %.4f" % np.abs(corr - corr.T).max())
print("sorting identical?         ", np.array_equal(sort_A, sort_B))
print("first 10 values            :", sort_A[:10].tolist())
print("matrix held by A           : %.4f GiB  (8*m^2, m=%d)" % (8*m*m/2**30, m))
print("state held by B            : %.4f GiB  (8*m)" % (8*m/2**30))
print("at Ran m=432014 -> A: %.1f GiB   B: %.4f GiB" % (8*432014**2/2**30, 8*432014/2**30))
PY
