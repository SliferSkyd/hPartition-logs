"""Generate SimDNA1-style alignments that differ from SimDNA1 in one parameter only: Seq-Gen's
-i, the proportion of invariable sites.

Everything else follows PsiPartition's gen_fake_dnaseq.py, whose data the manuscript reuses:
Seq-Gen, GTR, -g 4, 49 taxa, 5,000 sites split into 5 loci, each locus with its own GTR rates
and base frequencies. The trees are not resampled -- they are the SimDNA1 loci_5 trees, so the
alignments sit on the same trees as the published simulations.

The per-locus model draws are keyed to the replicate alone, so a given replicate has the same
five models at every level of -i; only the invariable proportion changes between levels.
Level 0.00 therefore reproduces SimDNA1 loci_5 up to the random seed, and serves as the control
that the pipeline is wired correctly.
"""
import os, sys, subprocess, numpy as np

SG   = "/work/diepht/tuank99lhp/hynduf/mpboot/seq-gen/Seq-Gen-1.3.5/source/seq-gen"
TREE = "/home/diepht/sliferskyd/hPartition-datasets/DNA/simulated-1/loci_5/{rep}.tree"
OUT  = "/home/diepht/sliferskyd/hPartition/rerun_sim/pinvar/data"
SEQLEN, NLOCI, NREP = 5000, 5, 10
LEVELS = [0.00, 0.15, 0.30, 0.45, 0.60, 0.75]

def run_locus(rep, j, pinv, rng):
    rr = [f"{x:.3f}" for x in rng.random(6)]
    f  = rng.random(4); f = f/f.sum()
    ff = [f"{x:.3f}" for x in f]
    cmd = [SG, "-r"+rr[0], *rr[1:], "-f"+ff[0], *ff[1:],
           "-m", "GTR", "-g", "4", "-l", str(SEQLEN//NLOCI), "-n", "1",
           "-z", str(rep*1000 + j)]
    if pinv > 0: cmd += ["-i"+str(pinv)]
    r = subprocess.run(cmd, stdin=open(TREE.format(rep=rep)), capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit(f"seq-gen failed rep={rep} locus={j}: {r.stderr[-300:]}")
    seqs, cur = {}, None
    for L in r.stdout.split("\n"):
        L = L.strip()
        if not L: continue
        if L.startswith(">"): cur = L[1:].split()[0]; seqs[cur] = ""
        elif cur: seqs[cur] += L.replace(" ", "")
    if not seqs: sys.exit(f"no sequences rep={rep} locus={j}")
    return seqs

def main():
    summary = []
    for p in LEVELS:
        tag = f"p{int(round(p*100)):02d}"
        d = f"{OUT}/{tag}"; os.makedirs(d, exist_ok=True)
        fracs = []
        for rep in range(NREP):
            rng = np.random.default_rng(rep)          # model draws keyed to the replicate only
            blocks = [run_locus(rep, j, p, rng) for j in range(NLOCI)]
            names = list(blocks[0])
            for b in blocks:
                assert set(b) == set(names), (rep, "taxon sets differ between loci")
            cat = {n: "".join(b[n] for b in blocks) for n in names}
            m = len(cat[names[0]])
            assert m == SEQLEN and all(len(v) == SEQLEN for v in cat.values())
            with open(f"{d}/{rep}.phy", "w") as fh:
                fh.write(f"{len(names)}\t{m}\n")
                for n in names: fh.write(f"{n}\t{cat[n]}\n")
            with open(f"{d}/{rep}.fasta", "w") as fh:
                for n in names: fh.write(f">{n}\n{cat[n]}\n")
            with open(f"{d}/{rep}.true.nex", "w") as fh:
                fh.write("#nexus\nbegin sets;\n")
                for j in range(NLOCI):
                    fh.write(f"charset L{j} = {j*(SEQLEN//NLOCI)+1}-{(j+1)*(SEQLEN//NLOCI)};\n")
                fh.write("end;\n")
            cols = zip(*[cat[n] for n in names])
            c = sum(1 for col in cols
                    if len({x.upper() for x in col if x.upper() in "ACGT"}) <= 1)
            fracs.append(100*c/m)
        summary.append((p, min(fracs), sum(fracs)/len(fracs), max(fracs)))
    print(f"{'-i':>6}{'% const min':>13}{'mean':>8}{'max':>8}")
    for p, lo, mu, hi in summary:
        print(f"{p:>6.2f}{lo:>12.2f}%{mu:>7.2f}%{hi:>7.2f}%")

main()
