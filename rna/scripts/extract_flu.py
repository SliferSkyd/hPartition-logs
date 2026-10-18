"""Extract the nucleotide alignments embedded in the BEAST XMLs of github.com/XuetingQiu/FluPartitioningModels
(Qiu & Bahl, bioRxiv 10.1101/228692). One dataset per folder (the -c/-p/-pc/-hky XMLs share one alignment; this
is checked). Sequences are renamed S0001.. (original BEAST taxon IDs contain '|' and '/'); mapping in <ds>.names.tsv.
Writes flu/aln/<ds>.{fasta,phy} (uppercase; PHYLIP as "N L" / "name seq")."""
import collections
import hashlib
import re
from pathlib import Path

R = Path('/home/diepht/sliferskyd/hPartition/rna_datasets/flu')
groups = collections.defaultdict(list)
for f in sorted((R / 'xml').glob('*.xml')):
    groups[f.name.rsplit('__', 1)[0] if '__' in f.name else f.stem].append(f)
for ds, files in groups.items():
    alns = {}
    for f in files:
        t = f.read_text(errors='ignore')
        seqs = re.findall(r'<sequence>\s*<taxon idref="([^"]+)"\s*/>\s*([A-Za-z\-\?\s]+?)\s*</sequence>', t)
        seqs = [(n, re.sub(r'\s', '', s).upper()) for n, s in seqs]
        alns[f.name] = seqs
    h = {hashlib.md5(repr(v).encode()).hexdigest() for v in alns.values()}
    seqs = next(iter(alns.values()))
    name = 'flu_' + re.sub(r'[^A-Za-z0-9]+', '_', ds).strip('_')
    L = {len(s) for _, s in seqs}
    assert len(L) == 1
    L = L.pop()
    with open(R / 'aln' / f'{name}.fasta', 'w') as fa, open(R / 'aln' / f'{name}.phy', 'w') as ph, \
            open(R / 'aln' / f'{name}.names.tsv', 'w') as nm:
        ph.write(f'{len(seqs)} {L}\n')
        nm.write('id\toriginal_beast_taxon\n')
        for i, (n, s) in enumerate(seqs, 1):
            sid = f'S{i:04d}'
            fa.write(f'>{sid}\n{s}\n')
            ph.write(f'{sid} {s}\n')
            nm.write(f'{sid}\t{n}\n')
    cols = list(zip(*[s for _, s in seqs]))
    var = sum(len(set(c) - set('-N?')) > 1 for c in cols)
    gis = sum(n.startswith('EPI') for n, _ in seqs)
    print(f'{name:42} xmls={len(files)} identical_alignments={len(h) == 1} taxa={len(seqs)} sites={L} '
          f'variable={var / L:.0%} GISAID_ids={gis}')
