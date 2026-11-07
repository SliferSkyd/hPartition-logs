"""Build 'merged' partition files in which every zero-variance subset of an hPartition
scheme is folded into the remaining subset with the highest constant-site fraction.
Rule is stated once here and applied identically to every dataset."""
import re, sys, os

ALNDIR = "/home/diepht/sliferskyd/hPartition-datasets/DNA/empirical"
SCHEME = "/home/diepht/sliferskyd/hPartition/rerun_sim/seedvar/out/{ds}.s0/hPartition/aln.partitions"
DATASETS = ["Arctiina","Calisto","Choreutidae","Coenonymphina",
            "Geometridae","Morpho","Noctuidae","Pieridae"]

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
        zv  = [k for k, v in sets.items() if all(const[i-1] for i in v)]
        rest = [k for k in sets if k not in zv]
        if not zv:
            summary.append((ds, len(sets), 0, 0, None)); continue
        # host = remaining subset with the highest constant-site fraction
        host = max(rest, key=lambda k: sum(const[i-1] for i in sets[k]) / len(sets[k]))
        moved = sum(len(sets[k]) for k in zv)
        merged = dict(sets)
        for k in zv:
            merged[host] = merged[host] + merged.pop(k)
        with open(f"{outdir}/{ds}.merged.nex", "w") as fh:
            fh.write("#nexus\nbegin sets;\n")
            for i, k in enumerate(sorted(merged, key=lambda x: int(x[1:]))):
                fh.write(f"charset Q{i} = {','.join(str(x) for x in sorted(merged[k]))};\n")
            fh.write("end;\n")
        frac = sum(const[i-1] for i in sets[host]) / len(sets[host])
        summary.append((ds, len(sets), len(zv), moved, f"{host} ({frac*100:.1f}% const)"))
    print(f"{'dataset':<15}{'subsets':>8}{'zero-var':>10}{'sites moved':>13}   host")
    for r in summary:
        print(f"{r[0]:<15}{r[1]:>8}{r[2]:>10}{r[3]:>13}   {r[4] or '-'}")

main(sys.argv[1])
