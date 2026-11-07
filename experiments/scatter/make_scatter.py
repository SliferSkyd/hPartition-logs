"""Build 'scattered' partition files in which the sites of every zero-variance subset of an
hPartition scheme are redistributed over the remaining subsets, each site assigned to one of
them uniformly at random.

This is a randomisation control, not a partitioning method: it destroys the grouping of the
invariant sites while leaving every other subset of the scheme untouched. The placement mechanism
coincides with gPartition's (gPartition.py:589-595 also draws randint(0, len(subsetIdx)-1) per
site), but the scope does not -- gPartition disperses every constant site in the alignment, 52% to
71% of these alignments, whereas this disperses only the 3% to 14% of them that form entirely
invariant hPartition subsets. The generator is seeded explicitly, so the schemes are reproducible.

Zero-variance subsets are identified exactly as in ../zerovar/make_merged.py.
"""
import re, sys, os, random

ALNDIR = "/home/diepht/sliferskyd/hPartition-datasets/DNA/empirical"
SCHEME = "/home/diepht/sliferskyd/hPartition/rerun_sim/seedvar/out/{ds}.s0/hPartition/aln.partitions"
DATASETS = ["Arctiina","Calisto","Choreutidae","Coenonymphina",
            "Geometridae","Morpho","Noctuidae","Pieridae"]
SEEDS = [0, 1, 2, 3, 4]

def read_phy(p):
    lines = open(p).read().split("\n")
    seqs = []
    for L in lines[1:]:
        if not L.strip(): continue
        parts = L.split(None, 1)
        if len(parts) == 2: seqs.append(parts[1].replace(" ", ""))
    return seqs

def is_const(col):
    s = {c.upper() for c in col if c.upper() in "ACGT"}
    return len(s) <= 1

def main(outdir):
    os.makedirs(outdir, exist_ok=True)
    summary = []
    for ds in DATASETS:
        seqs = read_phy(f"{ALNDIR}/{ds}.phy")
        cols = list(zip(*seqs))
        const = [is_const(c) for c in cols]
        txt = open(SCHEME.format(ds=ds)).read()
        sets = {}
        for m in re.finditer(r"charset\s+(\S+)\s*=\s*([^;]+);", txt):
            sets[m.group(1)] = [int(x) for x in m.group(2).replace(",", " ").split()]
        nsite_in = sum(len(v) for v in sets.values())
        zv   = [k for k, v in sets.items() if all(const[i-1] for i in v)]
        rest = [k for k in sets if k not in zv]
        if not zv:
            summary.append((ds, len(sets), 0, 0, "-")); continue
        moved = sorted(i for k in zv for i in sets[k])
        for s in SEEDS:
            rng = random.Random(s)
            scattered = {k: list(sets[k]) for k in rest}
            for i in moved:
                scattered[rest[rng.randrange(len(rest))]].append(i)
            assert sum(len(v) for v in scattered.values()) == nsite_in
            assert sorted(i for v in scattered.values() for i in v) == list(range(1, nsite_in+1))
            with open(f"{outdir}/{ds}.s{s}.scatter.nex", "w") as fh:
                fh.write("#nexus\nbegin sets;\n")
                for j, k in enumerate(sorted(scattered, key=lambda x: int(x[1:]))):
                    fh.write(f"charset Q{j} = {','.join(str(x) for x in sorted(scattered[k]))};\n")
                fh.write("end;\n")
        summary.append((ds, len(sets), len(zv), len(moved), f"{len(rest)} hosts"))
    print(f"{'dataset':<15}{'subsets':>8}{'zero-var':>10}{'sites moved':>13}   destination")
    for r in summary:
        print(f"{r[0]:<15}{r[1]:>8}{r[2]:>10}{r[3]:>13}   {r[4]}")

main(sys.argv[1])
