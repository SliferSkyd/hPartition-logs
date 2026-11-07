"""Write, per dataset, the model string of every subset of the hPartition seed-0 scheme that is
not entirely invariant. Model strings are taken fitted (with parameters in braces) from the
scoring run, so the subsets are evaluated exactly as they stand in the scheme being perturbed."""
import re, os
ALN="/home/diepht/sliferskyd/hPartition-datasets/DNA/empirical/{ds}.phy"
SCH="/home/diepht/sliferskyd/hPartition/rerun_sim/seedvar/out/{ds}.s0/hPartition/aln.partitions"
BM ="/home/diepht/sliferskyd/hPartition/rerun_sim/seedvar/out/{ds}.s0/partition/aln.best_model.nex"
DS=["Arctiina","Calisto","Choreutidae","Morpho","Pieridae"]
def read_phy(p):
    out=[]
    for L in open(p).read().split("\n")[1:]:
        q=L.split(None,1)
        if len(q)==2: out.append(q[1].replace(" ",""))
    return out
def isc(c):
    s={x.upper() for x in c if x.upper() in "ACGT"}
    return len(s)<=1
for ds in DS:
    cols=list(zip(*read_phy(ALN.format(ds=ds))))
    const=[isc(c) for c in cols]
    sets={m.group(1):[int(x) for x in m.group(2).replace(","," ").split()]
          for m in re.finditer(r"charset\s+(\S+)\s*=\s*([^;]+);",open(SCH.format(ds=ds)).read())}
    zv=[k for k,v in sets.items() if all(const[i-1] for i in v)]
    rest=sorted((k for k in sets if k not in zv), key=lambda x:int(x[1:]))
    txt=open(BM.format(ds=ds)).read()
    mod={}
    for L in txt.split("\n"):
        m=re.match(r"\s*(.+?):\s*(P\d+)\{[0-9.eE+-]+\}\s*[,;]?\s*$", L)
        if m:
            mdl=m.group(1).strip()
            # Both methods drop +ASC before computing site likelihoods, because the model is
            # evaluated over the whole alignment, which has constant sites even when the subset
            # it was fitted to does not (gPartition.py:771, phyloanalysis.cpp:4611-4616).
            mdl=mdl.replace("+ASC","")
            mod[m.group(2)]=mdl
    missing=[k for k in rest if k not in mod]
    assert not missing, (ds, missing[:5])
    with open(f"models/{ds}.txt","w") as fh:
        for k in rest: fh.write(f"{k}\t{mod[k]}\n")
    with open(f"models/{ds}.moved.txt","w") as fh:
        for i in sorted(i for k in zv for i in sets[k]): fh.write(f"{i}\n")
    print(f"{ds:<13} remaining={len(rest):>3}  dissolved={len(zv)}  sites moved={sum(len(sets[k]) for k in zv)}")
