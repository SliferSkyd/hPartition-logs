"""How well does each scheme recover the generating locus structure?

Each alignment was built from five 1,000-site loci, each with its own GTR matrix and base
frequencies, so locus membership is the generative grouping. We score agreement with the
adjusted Rand index over the variable sites only: invariable sites carry no locus signal and
every method disperses them deliberately, so including them measures dispersal, not grouping.

hPartition is scored twice: at its seed scheme (aln.MF.best_scheme.nex, the direct product of
rate binning in Stage 2) and at its final scheme, which isolates the binning step from the
likelihood reassignment that follows it.
"""
import os, re, statistics as st
from sklearn.metrics import adjusted_rand_score

P = "/home/diepht/sliferskyd/hPartition/rerun_sim/pinvar"
LV = ["p00","p15","p30","p45","p60","p75"]

def var_mask(phy):
    seqs=[]
    for L in open(phy).read().split("\n")[1:]:
        q=L.split(None,1)
        if len(q)==2: seqs.append(q[1].replace(" ",""))
    return [len({x.upper() for x in col if x.upper() in "ACGT"})>1 for col in zip(*seqs)]

def labels(nexus, m):
    lab=[-1]*m
    txt=open(nexus).read()
    for i,mt in enumerate(re.finditer(r"charset\s+(\S+)\s*=\s*([^;]+);", txt, re.I)):
        for tok in mt.group(2).replace(","," ").split():
            if "-" in tok:
                a,b=tok.split("-"); 
                for s in range(int(a),int(b)+1): lab[s-1]=i
            else: lab[int(tok)-1]=i
    return lab

FILES = {
 "hPar seed": lambda lv,r: f"{P}/out/hpar.{lv}.{r}/hPartition/aln.MF.best_scheme.nex",
 "hPar final": lambda lv,r: f"{P}/out/hpar.{lv}.{r}/hPartition/aln.partitions",
 "gPartition": lambda lv,r: f"{P}/out/gpar.{lv}.{r}/gPartition/{r}.phy.FINAL.nex",
 "PsiPartition": lambda lv,r: f"{P}/out/psi.{lv}.{r}/PsiPartition/{r}.final.parts",
}
print(f"{'level':>6}" + "".join(f"{k:>14}" for k in FILES))
for lv in LV:
    out={k:[] for k in FILES}
    for r in range(10):
        vm = var_mask(f"{P}/data/{lv}/{r}.phy"); m=len(vm)
        truth=[i//1000 for i in range(m)]
        tv=[t for t,v in zip(truth,vm) if v]
        for k,f in FILES.items():
            p=f(lv,r)
            if not os.path.exists(p): continue
            lab=labels(p,m)
            pv=[l for l,v in zip(lab,vm) if v]
            if len(set(pv))<1 or -1 in pv: continue
            out[k].append(adjusted_rand_score(tv,pv))
    print(f"{lv:>6}" + "".join(f"{st.mean(v):>14.3f}" if v else f"{'-':>14}" for v in out.values()))
