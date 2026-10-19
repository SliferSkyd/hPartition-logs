"""Convert PartitionFinder's own barkbeetles benchmark alignment to our FASTA/PHYLIP format.

Source: roblanf/BenchmarkAlignments, datasets/Cognato_2001/alignment.nex. The file was removed from the
repository's HEAD ("remove datasets") and the tutorial copies now 404, so it is recovered from git history
at commit ed04781e4c and kept locally in pf/src/. It is 44 taxa x 1,897 nucleotides, matching Table 1 of
Lanfear et al. (2012) exactly, and carries the seven data blocks that table reports: ef1a and COI by codon
position, plus 16S whole.

Underlying study: Cognato AI, Vogler AP (2001) Syst Biol 50(6):758-780; data Dryad 10.5061/dryad.678.
This benchmark copy derives from the deposited phenetic alignment with the 16 morphological characters and
part of the ef1a intron removed.

Writes pf/aln/barkbeetles.{fasta,phy}, .names.tsv and .genes.nex.
"""
import re
from pathlib import Path

SRC = Path('/home/diepht/sliferskyd/hPartition/rna_datasets/pf/src/Cognato_2001.alignment.nex')
OUT = Path('/home/diepht/sliferskyd/hPartition/rna_datasets/pf/aln')

txt = re.sub(r'\[[^\]]*\]', ' ', SRC.read_text(errors='ignore'))
nchar = int(re.search(r'nchar\s*=\s*(\d+)', txt, re.I).group(1))
body = re.search(r'\bmatrix\b(.*?);', txt, re.S | re.I).group(1)

seqs, order = {}, []
for line in body.splitlines():
    p = line.split()
    if len(p) != 2 or not set(p[1].upper()) <= set('ACGTRYSWKMBDHVN-?.'):
        continue
    if p[0] not in seqs:
        seqs[p[0]] = []
        order.append(p[0])
    seqs[p[0]].append(p[1].upper())
seqs = {k: ''.join(v).replace('?', 'N').replace('.', 'N') for k, v in seqs.items()}
bad = {k: len(v) for k, v in seqs.items() if len(v) != nchar}
assert not bad, f'length mismatch: {bad}'

OUT.mkdir(parents=True, exist_ok=True)
ids = [f'S{i:03d}' for i in range(1, len(order) + 1)]
with open(OUT / 'barkbeetles.fasta', 'w') as fa, open(OUT / 'barkbeetles.phy', 'w') as ph, \
        open(OUT / 'barkbeetles.names.tsv', 'w') as nm:
    ph.write(f'{len(order)} {nchar}\n')
    nm.write('id\toriginal_taxon\n')
    for sid, t in zip(ids, order):
        fa.write(f'>{sid}\n{seqs[t]}\n')
        ph.write(f'{sid} {seqs[t]}\n')
        nm.write(f'{sid}\t{t}\n')

cs = re.findall(r'CHARSET\s+(\S+)\s*=\s*([^;]+);', txt, re.I)
with open(OUT / 'barkbeetles.genes.nex', 'w') as f:        # the author's seven data blocks, verbatim
    f.write('#nexus\nbegin sets;\n')
    for n, spec in cs:
        if n.lower() in ('mitochondrial_genome', 'nuclear_genome'):
            continue
        f.write(f'  charset {n} = {spec.strip()};\n')
    f.write('end;\n')

cols = list(zip(*[seqs[t] for t in order]))
con = sum(len(set(c) - set('-N')) <= 1 for c in cols)
print(f'barkbeetles: {len(order)} taxa x {nchar} sites, {len([c for c in cs if c[0].lower() not in ("mitochondrial_genome","nuclear_genome")])} data blocks')
print(f'  constant {con} ({con/nchar:.1%}), variable {nchar-con} ({(nchar-con)/nchar:.1%})')
