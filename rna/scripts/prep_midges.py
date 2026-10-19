"""Convert the TreeBASE original-submission file for the midges matrix to our FASTA/PHYLIP format.

Source: TreeBASE study 10378, matrix M5116 (Ekrem T., Willassen E. & Stur E. 2010, Mol Phylogenet Evol
57:561-571), original file `Micropsectra_molecular.nex`, written by Mesquite 2.6. Retrieved with
    downloadANexusFile.html;jsessionid=<id>?id=10378&matrixid=5116
after seeding the session from the study's matrices page -- the `?format=nexus` PhyloWS exports, both
study- and matrix-level, omit the SETS block and are what cost us the charsets originally.

The sequence data is identical to the per-matrix export (verified column by column for all 74 taxa), so
this script changes nothing about the alignment; it exists to carry the author's four gene CHARSETs
(COI, COII, 16s, CAD), which PartitionFinder splits by codon position to reach the 10 data blocks its
Table 1 reports.
"""
import re
from pathlib import Path

SRC = Path('/home/diepht/sliferskyd/hPartition/rna_datasets/pf/src/Ekrem_2010.M5116.nexorg')
OUT = Path('/home/diepht/sliferskyd/hPartition/rna_datasets/pf/aln')
IUPAC = {'AG': 'R', 'CT': 'Y', 'CG': 'S', 'AT': 'W', 'GT': 'K', 'AC': 'M',
         'CGT': 'B', 'AGT': 'D', 'ACT': 'H', 'ACG': 'V', 'ACGT': 'N'}

txt = re.sub(r'\[[^\]]*\]', ' ', SRC.read_text(errors='ignore'))
nchar = int(re.search(r'NCHAR\s*=\s*(\d+)', txt, re.I).group(1))
body = re.search(r'^\s*MATRIX\s*$(.*?)^\s*;\s*$', txt, re.S | re.M | re.I).group(1)

seqs, order = {}, []
for line in body.splitlines():
    p = line.split()
    if len(p) != 2:
        continue
    if p[0] not in seqs:
        seqs[p[0]] = []
        order.append(p[0])
    seqs[p[0]].append(p[1])


def collapse(s):
    return re.sub(r'\{([A-Za-z]+)\}',
                  lambda m: IUPAC.get(''.join(sorted(set(m.group(1).upper()))), 'N'), s.upper())


seqs = {k: collapse(''.join(v)).replace('?', 'N').replace('.', 'N') for k, v in seqs.items()}
bad = {k: len(v) for k, v in seqs.items() if len(v) != nchar}
assert not bad, f'length mismatch: {bad}'

ids = [f'S{i:03d}' for i in range(1, len(order) + 1)]
with open(OUT / 'midges.fasta', 'w') as fa, open(OUT / 'midges.phy', 'w') as ph, \
        open(OUT / 'midges.names.tsv', 'w') as nm:
    ph.write(f'{len(order)} {nchar}\n')
    nm.write('id\toriginal_taxon\n')
    for sid, t in zip(ids, order):
        fa.write(f'>{sid}\n{seqs[t]}\n')
        ph.write(f'{sid} {seqs[t]}\n')
        nm.write(f'{sid}\t{t}\n')

cs = re.findall(r'charset\s+(\S+)\s*=\s*(\d+)\s*-\s*(\d+)\s*;', txt, re.I)
with open(OUT / 'midges.genes.nex', 'w') as f:
    f.write('#nexus\nbegin sets;\n')
    for n, a, b in cs:
        f.write(f'  charset {n} = {a}-{b};\n')
    f.write('end;\n')

print(f'midges: {len(order)} taxa x {nchar} sites, {len(cs)} gene charsets')
for n, a, b in cs:
    print(f'  {n:<6} {a}-{b}  ({int(b)-int(a)+1} sites)')
