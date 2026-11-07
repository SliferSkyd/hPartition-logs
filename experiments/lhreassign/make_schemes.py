"""Dissolve the entirely invariant subsets of an hPartition scheme and re-place their sites over
the surviving subsets by hPartition's own rule for a dissolved subset: a constant site is sampled
with probability proportional to exp(lnL - minLH) across the candidate subsets
(phyloanalysis.cpp:4405-4427 getPartitionIdx with stg=1, applied at 4868-4885).

Site log-likelihoods come from lh/<ds>/<subset>.sitelh, computed with the invocation of
phyloanalysis.cpp:4429-4452. Sampling is stochastic, so five independent assignments are written
per alignment.
"""
import re, os, sys, math, random
from collections import Counter

ALN="/home/diepht/sliferskyd/hPartition-datasets/DNA/empirical/{ds}.phy"
SCH="/home/diepht/sliferskyd/hPartition/rerun_sim/seedvar/out/{ds}.s0/hPartition/aln.partitions"
DS=["Arctiina","Calisto","Choreutidae","Morpho","Pieridae"]
SEEDS=[0,1,2,3,4]

def read_sitelh(p):
    with open(p) as fh:
        fh.readline()                      # "1 <nsite>"
        parts = fh.readline().split()
        assert parts[0].startswith("Site_Lh"), p
        return [float(x) for x in parts[1:]]

def read_phy(p):
    out=[]
    for L in open(p).read().split("\n")[1:]:
        q=L.split(None,1)
        if len(q)==2: out.append(q[1].replace(" ",""))
    return out

def isc(c):
    s={x.upper() for x in c if x.upper() in "ACGT"}
    return len(s)<=1

def pick(lhs, rng):
    """Exactly getPartitionIdx(lh, 1)."""
    minLH = min(lhs)
    eps = [math.exp(x - minLH) for x in lhs]
    total = sum(eps)
    r = rng.random()
    for i, e in enumerate(eps):
        if r < e/total: return i
        r -= e/total
    return len(eps)-1                      # only reachable through float rounding

def main(outdir):
    os.makedirs(outdir, exist_ok=True)
    print(f"{'dataset':<13}{'moved':>7}{'targets':>9}{'distinct dest':>15}{'top dest share':>16}")
    for ds in DS:
        names=[L.split("\t")[0] for L in open(f"models/{ds}.txt").read().strip().split("\n")]
        lh=[read_sitelh(f"lh/{ds}/{n}.sitelh") for n in names]
        nsite=len(lh[0]); assert all(len(x)==nsite for x in lh), ds
        moved=[int(x) for x in open(f"models/{ds}.moved.txt").read().split()]
        cols=list(zip(*read_phy(ALN.format(ds=ds))))
        const=[isc(c) for c in cols]
        sets={m.group(1):[int(x) for x in m.group(2).replace(","," ").split()]
              for m in re.finditer(r"charset\s+(\S+)\s*=\s*([^;]+);",open(SCH.format(ds=ds)).read())}
        assert sorted(moved)==sorted(i for k,v in sets.items()
                                     if all(const[j-1] for j in v) for i in v), ds
        tally=Counter()
        for s in SEEDS:
            rng=random.Random(s)
            out={n:list(sets[n]) for n in names}
            for i in moved:
                j=pick([lh[k][i-1] for k in range(len(names))], rng)
                out[names[j]].append(i)
                if s==0: tally[names[j]]+=1
            tot=sum(len(v) for v in out.values())
            assert tot==nsite and sorted(i for v in out.values() for i in v)==list(range(1,nsite+1)), ds
            with open(f"{outdir}/{ds}.s{s}.lhre.nex","w") as fh:
                fh.write("#nexus\nbegin sets;\n")
                for q,n in enumerate(names):
                    fh.write(f"charset Q{q} = {','.join(str(x) for x in sorted(out[n]))};\n")
                fh.write("end;\n")
        top=tally.most_common(1)[0]
        print(f"{ds:<13}{len(moved):>7}{len(names):>9}{len(tally):>15}{top[0]+' '+format(100*top[1]/len(moved),'.1f')+'%':>16}")

main(sys.argv[1] if len(sys.argv)>1 else "schemes")
