"""Convert the two rRNA-containing PartitionFinder benchmark alignments to our FASTA/PHYLIP format.

  saxifragales  Fishbein et al. 2001, Syst Biol 50:817-847 (Dryad 10.5061/dryad.684)
                40 taxa; the five CHARSETs (atpB, 18S, rbcL, matK, 26S) span 9,006 of the file's
                9,237 columns, which is the subset PartitionFinder Table 1 reports; only those are kept.
                NEXUS uses GAP=':' and MISSING='N'.
  midges        Ekrem, Willassen & Stur 2010 (TreeBASE study 10378, matrix 5116)
                74 taxa x 2,701 sites, COI/COII/CAD/16S. NEXUS uses GAP='-' and MISSING='?'.

Both are nucleotide, interleaved. Output: pf/aln/<ds>.{fasta,phy} (uppercase, '-' gaps, 'N' missing,
safe IDs) plus <ds>.names.tsv and, where the source defines them, <ds>.genes.nex with the gene CHARSETs
remapped to the retained columns (a reference partition to compare the methods against).
"""
import re
from pathlib import Path

OUT = Path('/home/diepht/sliferskyd/hPartition/rna_datasets/pf')
SRC = {
    'saxifragales': ('/home/diepht/sliferskyd/hPartition/Fishbein.nexus', ':', 'N'),
    'midges': ('/tmp/claude-10030/-work-backup-home-diepht-sliferskyd-hPartition/'
               '1841f9c7-ff4e-4032-9c4c-3cc4ce587094/scratchpad/tb/midges.nex', '-', '?'),
}


IUPAC = {'AG': 'R', 'CT': 'Y', 'CG': 'S', 'AT': 'W', 'GT': 'K', 'AC': 'M',
         'CGT': 'B', 'AGT': 'D', 'ACT': 'H', 'ACG': 'V', 'ACGT': 'N'}


def collapse_ambiguity(s):
    """NEXUS writes ambiguity as a brace set, e.g. {AG}; IQ-TREE wants the IUPAC letter."""
    return re.sub(r'\{([A-Za-z]+)\}',
                  lambda m: IUPAC.get(''.join(sorted(set(m.group(1).upper()))), 'N'), s)


def read_nexus(path, gap, missing):
    txt = Path(path).read_text(errors='ignore')
    # MATRIX must be its own line: the word also occurs in TreeBASE's TITLE 'Matrix in file ...' line
    m = re.search(r'^[ \t]*MATRIX[ \t]*$(.*?)(?:^\s*;\s*$)', txt, re.S | re.I | re.M)
    body = m.group(1)
    seqs, order = {}, []
    for line in body.splitlines():
        line = re.sub(r'\[[^\]]*\]', '', line).strip()   # drop [ ... ] comments / rulers
        if not line:
            continue
        parts = line.split(None, 1)
        if len(parts) != 2:
            continue
        name, s = parts[0], collapse_ambiguity(re.sub(r'\s', '', parts[1]).upper())
        if not s or not re.fullmatch(r'[A-Za-z?:\-.]+', s):
            continue
        if name not in seqs:
            seqs[name] = []
            order.append(name)
        seqs[name].append(s)
    seqs = {k: ''.join(v).upper().replace(gap, '-').replace(missing.upper(), 'N') for k, v in seqs.items()}
    charsets = [(n, int(a), int(b)) for n, a, b in
                re.findall(r'CHARSET\s+(\S+)\s*=\s*(\d+)\s*-\s*(\d+)\s*;', txt, re.I)]
    return order, seqs, charsets


(OUT / 'aln').mkdir(parents=True, exist_ok=True)
for ds, (path, gap, missing) in SRC.items():
    order, seqs, charsets = read_nexus(path, gap, missing)
    L = {len(s) for s in seqs.values()}
    assert len(L) == 1, (ds, sorted(L)[:4])
    L = L.pop()
    if charsets:                       # keep only the columns the gene CHARSETs cover
        keep, remap, pos = [], [], 0
        for name, a, b in charsets:
            keep += list(range(a - 1, b))
            remap.append((name, pos + 1, pos + b - a + 1))
            pos += b - a + 1
    else:
        keep, remap = list(range(L)), []
    ids = [f'S{i:03d}' for i in range(1, len(order) + 1)]
    with open(OUT / 'aln' / f'{ds}.fasta', 'w') as fa, open(OUT / 'aln' / f'{ds}.phy', 'w') as ph, \
            open(OUT / 'aln' / f'{ds}.names.tsv', 'w') as nm:
        ph.write(f'{len(order)} {len(keep)}\n')
        nm.write('id\toriginal_taxon\n')
        for sid, name in zip(ids, order):
            sub = ''.join(seqs[name][j] for j in keep)
            fa.write(f'>{sid}\n{sub}\n')
            ph.write(f'{sid} {sub}\n')
            nm.write(f'{sid}\t{name}\n')
    if remap:
        with open(OUT / 'aln' / f'{ds}.genes.nex', 'w') as f:
            f.write('#nexus\nbegin sets;\n')
            for name, a, b in remap:
                f.write(f'  charset {name} = {a}-{b};\n')
            f.write('end;\n')
    cols = list(zip(*[''.join(seqs[n][j] for j in keep) for n in order]))
    var = sum(len(set(c) - set('-N?')) > 1 for c in cols)
    gaps = sum(c.count('-') for c in cols) / (len(keep) * len(order))
    print(f'{ds}: {len(order)} taxa x {len(keep)} sites (source {L}), variable {var} ({var/len(keep):.1%}), '
          f'gaps {gaps:.1%}, genes {[n for n, _, _ in remap] or "none in file"}')
