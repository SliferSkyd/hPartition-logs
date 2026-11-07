"""Recover the true per-site rate class of every generated alignment.

Re-runs Seq-Gen with exactly the arguments gen.py used, adding only -wr, which writes the rate
class of each site to stderr. The regenerated sequences are compared byte for byte against the
alignment actually analysed; if they differ the rates would not belong to that alignment, so
the run aborts rather than write them.
"""
import os, sys, subprocess, numpy as np
SG   = "/work/diepht/tuank99lhp/hynduf/mpboot/seq-gen/Seq-Gen-1.3.5/source/seq-gen"
TREE = "/home/diepht/sliferskyd/hPartition-datasets/DNA/simulated-1/loci_5/{rep}.tree"
P    = "/home/diepht/sliferskyd/hPartition/rerun_sim/pinvar"
SEQLEN, NLOCI, NREP = 5000, 5, 10
LEVELS = [(0.00,"p00"),(0.15,"p15"),(0.30,"p30"),(0.45,"p45"),(0.60,"p60"),(0.75,"p75")]

def locus(rep, j, pinv, rng):
    rr=[f"{x:.3f}" for x in rng.random(6)]
    f=rng.random(4); f=f/f.sum(); ff=[f"{x:.3f}" for x in f]
    cmd=[SG,"-r"+rr[0],*rr[1:],"-f"+ff[0],*ff[1:],
         "-m","GTR","-g","4","-l",str(SEQLEN//NLOCI),"-n","1","-z",str(rep*1000+j)]
    if pinv>0: cmd+=["-i"+str(pinv)]
    cmd+=["-wr"]
    r=subprocess.run(cmd,stdin=open(TREE.format(rep=rep)),capture_output=True,text=True)
    if r.returncode!=0: sys.exit(f"seq-gen failed rep={rep} locus={j}")
    seqs,cur={},None
    for L in r.stdout.split("\n"):
        L=L.strip()
        if not L: continue
        if L.startswith(">"): cur=L[1:].split()[0]; seqs[cur]=""
        elif cur: seqs[cur]+=L.replace(" ","")
    rates=[]
    for L in r.stderr.split("\n"):
        p=L.split("\t")
        if len(p)==2 and p[0].strip().isdigit():
            rates.append(float(p[1]))
    assert len(rates)==SEQLEN//NLOCI, (rep,j,len(rates))
    return seqs, rates

def main():
    os.makedirs(f"{P}/rates", exist_ok=True)
    for pinv,tag in LEVELS:
        os.makedirs(f"{P}/rates/{tag}", exist_ok=True)
        for rep in range(NREP):
            rng=np.random.default_rng(rep)
            blocks=[]; rates=[]
            for j in range(NLOCI):
                s,rt=locus(rep,j,pinv,rng); blocks.append(s); rates+=rt
            names=list(blocks[0])
            cat={n:"".join(b[n] for b in blocks) for n in names}
            # the alignment that was actually analysed
            have={}
            for L in open(f"{P}/data/{tag}/{rep}.phy").read().split("\n")[1:]:
                q=L.split(None,1)
                if len(q)==2: have[q[0]]=q[1].replace(" ","")
            if have!=cat:
                sys.exit(f"MISMATCH {tag}/{rep}: regenerated sequences differ from the analysed alignment")
            with open(f"{P}/rates/{tag}/{rep}.rates","w") as fh:
                fh.write("\n".join(f"{i+1}\t{r}" for i,r in enumerate(rates))+"\n")
        print(f"{tag}: 10/10 verified identical")
main()
