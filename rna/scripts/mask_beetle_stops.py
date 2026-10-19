"""Mask the gene regions whose translations contain internal stop codons.

Five (taxon, gene) sequences translate with internal stops under genetic code 5, which means the deposited
annotation's reading frame is wrong, the record has sequencing errors, or the copy is a pseudogene. The rest of
each taxon's 37 genes are fine, so only the offending gene's columns are set to gaps rather than dropping the
taxon.
"""
import re
from pathlib import Path

D = Path('/home/diepht/sliferskyd/hPartition/rna_datasets/beetle/aln')
MASK = [('JX412852', 'cox1'), ('JX412759', 'cox1'), ('JX412798', 'cox1'),
        ('JX412839', 'cox1'), ('JX412729', 'nad5')]

cs = {m[0]: (int(m[1]), int(m[2])) for m in
      re.findall(r'charset (\S+) = (\d+)-(\d+);', (D / 'beetle.genes.nex').read_text())}

seqs, order, cur = {}, [], None
for line in (D / 'beetle.unmasked.fasta').read_text().splitlines():
    if line.startswith('>'):
        cur = line[1:].strip(); order.append(cur); seqs[cur] = ''
    elif cur:
        seqs[cur] += line.strip()

log = []
for taxon, gene in MASK:
    a, b = cs[gene]
    s = seqs[taxon]
    nong = len(s[a - 1:b]) - s[a - 1:b].count('-')
    seqs[taxon] = s[:a - 1] + '-' * (b - a + 1) + s[b:]
    log.append(f'{taxon}\t{gene}\t{a}-{b}\t{nong} non-gap sites masked')

L = len(seqs[order[0]])
assert all(len(s) == L for s in seqs.values())
(D / 'beetle.fasta').write_text(''.join(f'>{t}\n{seqs[t]}\n' for t in order))
with open(D / 'beetle.phy', 'w') as f:
    f.write(f'{len(order)} {L}\n')
    for t in order:
        f.write(f'{t} {seqs[t]}\n')
(D / 'beetle.masked.tsv').write_text('taxon\tgene\tcolumns\tnote\n' + '\n'.join(log) + '\n')
print('\n'.join(log))
print(f'\n{len(order)} taxa x {L} sites')
