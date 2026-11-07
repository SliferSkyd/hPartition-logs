"""Full read of the pinvar sweep.

BIC comes from the common scoring run (bin/eval_iqtree.sh) so the three methods are on one
footing; RF to the true tree uses ete3 robinson_foulds(unrooted_trees=True), the metric the
manuscript's simulated benchmark uses (rerun_sim/bin/summarize.py).
"""
import os, re, statistics as st
from ete3 import Tree

P = "/home/diepht/sliferskyd/hPartition/rerun_sim/pinvar"
TRUE = "/home/diepht/sliferskyd/hPartition-datasets/DNA/simulated-1/loci_5/{r}.tree"
LV = [("p00",0.0),("p15",0.15),("p30",0.30),("p45",0.45),("p60",0.60),("p75",0.75)]
MET = {"hpar":"hPartition","gpar":"gPartition","psi":"PsiPartition"}

def bic(p):
    if not os.path.exists(p): return None
    for l in open(p):
        if "Bayesian information criterion (BIC) score:" in l: return float(l.split()[-1])

def rf(inferred, r):
    if not os.path.exists(inferred): return None, None
    a = Tree(open(inferred).read().strip())
    b = Tree(open(TRUE.format(r=r)).read().strip())
    d, mx, *_ = a.robinson_foulds(b, unrooted_trees=True)
    return d, mx

def ksub(m, lv, r):
    f = {"hpar": f"{P}/out/hpar.{lv}.{r}/hPartition/aln.partitions",
         "gpar": f"{P}/out/gpar.{lv}.{r}/gPartition/{r}.phy.FINAL.nex",
         "psi":  f"{P}/out/psi.{lv}.{r}/PsiPartition/{r}.final.parts"}[m]
    if not os.path.exists(f): return None
    return sum(1 for l in open(f) if l.strip().lower().startswith("charset"))

rows = {}
for lv, p in LV:
    for m in MET:
        for r in range(10):
            b = bic(f"{P}/out/{m}.{lv}.{r}/partition/aln.iqtree")
            d, mx = rf(f"{P}/out/{m}.{lv}.{r}/partition/aln.treefile", r)
            rows[(lv, m, r)] = (b, d, mx, ksub(m, lv, r))

print("BIC relative to hPartition (positive = hPartition better), and RF to the true tree")
print(f"{'level':>6}{'(Psi-h)/h':>11}{'sd':>7}{'h<Psi':>7}"
      f"{'(g-h)/h':>10}{'sd':>7}{'h<g':>6}"
      f"{'RF h':>7}{'RF g':>7}{'RF Psi':>8}{'maxRF':>7}"
      f"{'k h':>6}{'k g':>6}{'k Psi':>7}")
for lv, p in LV:
    h  = [rows[(lv,'hpar',r)] for r in range(10)]
    g  = [rows[(lv,'gpar',r)] for r in range(10)]
    s  = [rows[(lv,'psi', r)] for r in range(10)]
    dp = [100*(s[r][0]-h[r][0])/h[r][0] for r in range(10) if h[r][0] and s[r][0]]
    dg = [100*(g[r][0]-h[r][0])/h[r][0] for r in range(10) if h[r][0] and g[r][0]]
    wp = sum(1 for r in range(10) if h[r][0] and s[r][0] and h[r][0] < s[r][0])
    wg = sum(1 for r in range(10) if h[r][0] and g[r][0] and h[r][0] < g[r][0])
    mean = lambda v: st.mean([x for x in v if x is not None]) if any(x is not None for x in v) else float('nan')
    print(f"{lv:>6}{st.mean(dp):>10.2f}%{st.stdev(dp):>7.2f}{str(wp)+'/10':>7}"
          f"{st.mean(dg):>9.2f}%{st.stdev(dg):>7.2f}{str(wg)+'/10':>6}"
          f"{mean([x[1] for x in h]):>7.1f}{mean([x[1] for x in g]):>7.1f}{mean([x[1] for x in s]):>8.1f}"
          f"{mean([x[2] for x in h]):>7.0f}"
          f"{mean([x[3] for x in h]):>6.1f}{mean([x[3] for x in g]):>6.1f}{mean([x[3] for x in s]):>7.1f}")
