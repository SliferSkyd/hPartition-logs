"""Does each scheme capture the true rate structure?

Seq-Gen assigns every site one of four discrete gamma classes, or rate 0 if invariable. We score
each scheme against those classes over the sites that are genuinely variable (true rate > 0),
two ways: the adjusted Rand index against the class labels, and eta squared, the share of the
variance in true log rate that subset membership explains.
"""
import os, re, statistics as st
import numpy as np
from sklearn.metrics import adjusted_rand_score

P="/home/diepht/sliferskyd/hPartition/rerun_sim/pinvar"
LV=["p00","p15","p30","p45","p60","p75"]
FILES={
 "hPar seed":    lambda lv,r: f"{P}/out/hpar.{lv}.{r}/hPartition/aln.MF.best_scheme.nex",
 "hPar final":   lambda lv,r: f"{P}/out/hpar.{lv}.{r}/hPartition/aln.partitions",
 "gPartition":   lambda lv,r: f"{P}/out/gpar.{lv}.{r}/gPartition/{r}.phy.FINAL.nex",
 "PsiPartition": lambda lv,r: f"{P}/out/psi.{lv}.{r}/PsiPartition/{r}.final.parts"}

def labels(nex,m):
    lab=[-1]*m
    for i,mt in enumerate(re.finditer(r"charset\s+(\S+)\s*=\s*([^;]+);",open(nex).read(),re.I)):
        for tok in mt.group(2).replace(","," ").split():
            if "-" in tok:
                a,b=tok.split("-")
                for s in range(int(a),int(b)+1): lab[s-1]=i
            else: lab[int(tok)-1]=i
    return lab

def eta2(y,g):
    y=np.asarray(y,float); g=np.asarray(g)
    gm=y.mean(); sst=((y-gm)**2).sum()
    ssb=sum(len(y[g==k])*(y[g==k].mean()-gm)**2 for k in np.unique(g))
    return ssb/sst if sst>0 else float('nan')

for metric in ("ARI","eta2"):
    print(f"\n=== {metric} vs true rate class, variable sites only ===")
    print(f"{'level':>6}"+"".join(f"{k:>14}" for k in FILES))
    for lv in LV:
        out={k:[] for k in FILES}
        for r in range(10):
            rt=[float(l.split("\t")[1]) for l in open(f"{P}/rates/{lv}/{r}.rates")]
            m=len(rt); keep=[i for i in range(m) if rt[i]>0]
            truth=[rt[i] for i in keep]
            for k,f in FILES.items():
                p=f(lv,r)
                if not os.path.exists(p): continue
                lab=labels(p,m); pv=[lab[i] for i in keep]
                if -1 in pv: continue
                out[k].append(adjusted_rand_score(truth,pv) if metric=="ARI"
                              else eta2(np.log(truth),np.array(pv)))
        print(f"{lv:>6}"+"".join(f"{st.mean(v):>14.3f}" if v else f"{'-':>14}" for v in out.values()))
