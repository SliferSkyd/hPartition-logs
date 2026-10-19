"""Convert PartitionFinder's own saxifragales benchmark alignment to our FASTA/PHYLIP format.

Source: roblanf/BenchmarkAlignments, datasets/Fishbein_2001/alignment.nex, recovered from git history at
commit f7908d9d01 (the directory was later removed) and kept in pf/src/. The file is the full deposited
matrix, 40 taxa x 9,237 columns; the eleven CHARSETs cover 9,005 of them, which is the figure Table 1 of
Lanfear et al. (2012) reports, and only those columns are kept.

Note the atpB block begins at column 58, not 57 as the Dryad file's own `atpB` charset has it: PartitionFinder
starts at the first codon position. That one column is the whole difference between 9,005 and 9,006.

Underlying study: Fishbein M et al. (2001) Syst Biol 50:817-847; data Dryad 10.5061/dryad.684.
Writes pf/aln/saxifragales.{fasta,phy}, .names.tsv and .genes.nex (the eleven data blocks).
"""
import re
from pathlib import Path

SRC = Path('/home/diepht/sliferskyd/hPartition/rna_datasets/pf/src/Fishbein_2001.alignment.nex')
OUT = Path('/home/diepht/sliferskyd/hPartition/rna_datasets/pf/aln')
SKIP = {'mitochondrial_genome', 'nuclear_genome', 'chloroplast_genome'}


def expand(spec):
    spec = re.sub(r'(?<=\d)\s*-\s*(?=\d)', ' - ', spec).replace('\\', ' \\ ')
    t = spec.replace(',', ' ').split(); out = set(); i = 0
    while i < len(t):
        if not t[i].isdigit():
            i += 1; continue
        a = int(t[i]); b = a; st = 1; j = i + 1
        if j < len(t) and t[j] == '-': b = int(t[j + 1]); j += 2
        if j < len(t) and t[j] == '\\': st = int(t[j + 1]); j += 2
        out |= set(range(a, b + 1, st)); i = j
    return out


txt = re.sub(r'\[[^\]]*\]', ' ', SRC.read_text(errors='ignore'))
nchar = int(re.search(r'nchar\s*=\s*(\d+)', txt, re.I).group(1))
body = re.search(r'\bmatrix\b(.*?);', txt, re.S | re.I).group(1)

seqs, order = {}, []
for line in body.splitlines():
    p = line.split()
    if len(p) != 2 or not set(p[1].upper()) <= set('ACGTRYSWKMBDHVN-?.:'):
        continue
    if p[0] not in seqs:
        seqs[p[0]] = []; order.append(p[0])
    seqs[p[0]].append(p[1].upper())
seqs = {k: ''.join(v) for k, v in seqs.items()}
bad = {k: len(v) for k, v in seqs.items() if len(v) != nchar}
assert not bad, f'length mismatch: {bad}'

cs = [(n, expand(s)) for n, s in re.findall(r'CHARSET\s+(\S+)\s*=\s*([^;]+);', txt, re.I)
      if n.lower() not in SKIP]
keep = sorted(set().union(*[v for _, v in cs]))
pos = {j: i + 1 for i, j in enumerate(keep)}
sub = {k: ''.join(v[j - 1] for j in keep).replace('?', 'N').replace('.', 'N').replace(':', '-')
       for k, v in seqs.items()}

OUT.mkdir(parents=True, exist_ok=True)
ids = [f'S{i:03d}' for i in range(1, len(order) + 1)]
with open(OUT / 'saxifragales.fasta', 'w') as fa, open(OUT / 'saxifragales.phy', 'w') as ph, \
        open(OUT / 'saxifragales.names.tsv', 'w') as nm:
    ph.write(f'{len(order)} {len(keep)}\n')
    nm.write('id\toriginal_taxon\n')
    for sid, t in zip(ids, order):
        fa.write(f'>{sid}\n{sub[t]}\n')
        ph.write(f'{sid} {sub[t]}\n')
        nm.write(f'{sid}\t{t}\n')


def ranges(xs):
    xs = sorted(xs); out = []; a = p = xs[0]
    for x in xs[1:]:
        if x == p + 1: p = x
        else: out.append((a, p)); a = p = x
    out.append((a, p))
    return ' '.join(f'{u}-{v}' if u != v else str(u) for u, v in out)


with open(OUT / 'saxifragales.genes.nex', 'w') as f:
    f.write('#nexus\nbegin sets;\n')
    for n, v in cs:
        f.write(f'  charset {n} = {ranges([pos[j] for j in sorted(v)])};\n')
    f.write('end;\n')

cols = list(zip(*[sub[t] for t in order]))
con = sum(len(set(c) - set('-N')) <= 1 for c in cols)
print(f'saxifragales: {len(order)} taxa x {len(keep)} sites (from NCHAR {nchar}), {len(cs)} data blocks')
print(f'  constant {con} ({con/len(keep):.1%})')
