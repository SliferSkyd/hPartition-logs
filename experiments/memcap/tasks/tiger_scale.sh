#!/bin/bash
unset LD_LIBRARY_PATH
O=/home/diepht/sliferskyd/hPartition/rerun_sim/memcap/out/tiger_scale
/home/diepht/anaconda3/bin/python -I - <<'PY' > $O/tiger_scale.txt 2>&1
import os, re, time
NEX = "/home/diepht/sliferskyd/hPartition-datasets/Protein/Ran.nex"
UNKNOWN = ["?", "-", "X", "x"]

def hwm():
    for l in open("/proc/self/status"):
        if l.startswith("VmHWM"): return int(l.split()[1]) / 1048576

# --- read the matrix ---
seqs, inmat = {}, False
for l in open(NEX):
    s = l.strip()
    if s.lower().startswith("matrix"): inmat = True; continue
    if not inmat: continue
    if s.startswith(";") or s.lower().startswith("end"): break
    p = s.split()
    if len(p) == 2: seqs[p[0]] = seqs.get(p[0], "") + p[1]
names = sorted(seqs)
M = len(seqs[names[0]])
print("node:", os.uname().nodename)
print("taxa %d  sites %d  (alignment in RAM: %.3f GiB)" % (len(names), M, hwm()))

# --- tiger_fns_102.py, verbatim logic ---
def getPattern(site):
    considered, pattern = [], []
    for x in range(len(site)):
        if site[x] not in UNKNOWN:
            if site[x] in considered:
                pattern[considered.index(site[x])].append(str(x))
            else:
                considered.append(site[x]); pattern.append([str(x)])
    return "|".join([",".join(g) for g in pattern])

def scoreConflict(indA, patA, patterns):
    dividand = 0; pg = patA.split("|"); score = 0.0
    pats2 = patterns[:]            # full copy, every call
    del pats2[indA]
    for patB in pats2:
        if re.search(r"\|", patB):
            dividand += 1
            compB = patB.split("|"); scB = 0.0
            for group in compB:
                cont = 1; tax = group.split(","); ch1 = tax[0]
                for gp in pg:
                    if ch1 in gp:
                        for ch2 in tax[1:]:
                            if ch2 not in gp and cont:
                                scB += 1.0; cont = 0
            score += (scB / len(compB))
    return score / dividand if dividand else 0.0

print("\n%8s %10s %12s %12s %10s" % ("m", "|comp|", "dedup (s)", "score (s)", "VmHWM GiB"))
res = []
for m in (250, 500, 1000, 2000):
    sub = [seqs[n][:m] for n in names]
    t0 = time.time()
    patterns, comp = [], []
    for i in range(m):
        site = "".join(j[i] for j in sub)
        patterns.append(getPattern(site))
        if patterns[-1] not in comp:      # linear scan per site
            comp.append(patterns[-1])
    t1 = time.time()
    for aa, patA in enumerate(comp):
        if re.search(r"\|", patA): scoreConflict(aa, patA, patterns)
    t2 = time.time()
    res.append((m, len(comp), t1 - t0, t2 - t1))
    print("%8d %10d %12.2f %12.2f %10.3f" % (m, len(comp), t1-t0, t2-t1, hwm()))

m0, c0, d0, s0 = res[-1]
tot = d0 + s0
print("\nquadratic fit from m=%d:" % m0)
for m, c, d, s in res:
    print("  m=%-6d total %8.2f s   t/m^2 = %.3e" % (m, d+s, (d+s)/m**2))
print("\nextrapolation to Ran (m=%d):" % M)
print("  time  : %.1f days   (t/m^2 x m^2, from m=%d)" % (tot/m0**2*M**2/86400, m0))
print("  memory: alignment %.3f GiB + patterns ~%.3f GiB (O(n.m), no m^2 array)"
      % (len(names)*M/1073741824, M*2*len(names)*60/1073741824))
PY
