"""Build the 'clumped' counterfactual scheme used to test the effect of isolating invariant sites.

Scheme A is hPartition's own scheme. Scheme B keeps every variant site where hPartition put it but moves
all invariant sites into one dedicated subset, reproducing what rate-clustering methods do when every
invariant site receives rate 0 and is left in the lowest bin. Subsets left with fewer than 50 sites are
folded into the nearest remaining subset so that the two schemes differ only in the treatment of
invariant sites, not in minimum-subset policy.
"""
import re, sys
from pathlib import Path

D = Path('/home/diepht/sliferskyd/hPartition-datasets/DNA/empirical')
OUT = Path('/home/diepht/sliferskyd/hPartition/rerun_sim/stability')


def read_phy(p):
    rows = []
    for l in open(p).read().split('\n')[1:]:
        q = l.split(None, 1)
        if len(q) == 2:
            rows.append(q[1].replace(' ', '').upper())
    return rows


def expand(s):
    s = re.sub(r'(?<=\d)\s*-\s*(?=\d)', ' - ', s).replace('\\', ' \\ ')
    t = s.replace(',', ' ').split(); o = set(); i = 0
    while i < len(t):
        if not t[i].isdigit():
            i += 1; continue
        a = int(t[i]); b = a; st = 1; j = i + 1
        if j < len(t) and t[j] == '-': b = int(t[j + 1]); j += 2
        if j < len(t) and t[j] == '\\': st = int(t[j + 1]); j += 2
        o |= set(range(a, b + 1, st)); i = j
    return o


def ranges(xs):
    xs = sorted(xs); out = []; a = p = xs[0]
    for x in xs[1:]:
        if x == p + 1: p = x
        else: out.append((a, p)); a = p = x
    out.append((a, p))
    return ' '.join(f'{u}-{v}' if u != v else str(u) for u, v in out)


OUT.mkdir(exist_ok=True)
ds = sys.argv[1]
rows = read_phy(D / f'{ds}.phy')
cols = list(zip(*rows))
con = [len(set(c) - set('-N?')) <= 1 for c in cols]
P = {n: expand(s) for n, s in re.findall(r'charset (\S+) = ([^;]+);', (D / f'{ds}.phy.partitions').read_text())}

variant_only = {n: {i for i in v if not con[i - 1]} for n, v in P.items()}
inv = {i for i, c in enumerate(con, 1) if c}
parts = {n: v for n, v in variant_only.items() if len(v) >= 50}
orphan = set().union(*[v for n, v in variant_only.items() if len(v) < 50]) if any(len(v) < 50 for v in variant_only.values()) else set()
if orphan:                       # fold leftovers into the largest subset
    big = max(parts, key=lambda n: len(parts[n]))
    parts[big] |= orphan
parts['INVARIANT'] = inv

with open(OUT / f'{ds}.clumped.nex', 'w') as f:
    f.write('#nexus\nbegin sets;\n')
    for n, v in parts.items():
        if v: f.write(f'  charset {n} = {ranges(v)};\n')
    f.write('end;\n')
cov = set().union(*parts.values())
assert len(cov) == len(cols) and sum(len(v) for v in parts.values()) == len(cols), f'{ds}: bad cover'
print(f'{ds}: hPartition k={len(P)} -> clumped k={len([v for v in parts.values() if v])} '
      f'(invariant subset {len(inv)} sites = {len(inv)/len(cols):.1%})')
