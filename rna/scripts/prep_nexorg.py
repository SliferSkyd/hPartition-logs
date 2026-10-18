"""Convert a TreeBASE .nexorg (original submitted NEXUS) to our FASTA/PHYLIP format.

Unlike the per-matrix download, a .nexorg keeps the author's SETS block, so the gene/codon CHARSETs and any
EXSET of excluded sites survive. Both matter: for McGuire et al. 2007 (hummingbirds, M3354) the file is
NCHAR=4122 and the EXSET removes 301 sites, giving the 3,821 columns PartitionFinder Table 1 reports.

Handles: files written with tabs and no newlines; CHARSETs with several ranges and a stride (`a - b \\ 3`,
used for codon positions); EXSET exclusions; NEXUS ambiguity braces ({AG} -> R).
Usage: prep_nexorg.py <file.nexorg> <output-name>
Writes pf/aln/<name>.{fasta,phy}, <name>.names.tsv and <name>.genes.nex (CHARSETs remapped to kept columns).
"""
import re
import sys
from pathlib import Path

OUT = Path('/home/diepht/sliferskyd/hPartition/rna_datasets/pf/aln')
IUPAC = {'AG': 'R', 'CT': 'Y', 'CG': 'S', 'AT': 'W', 'GT': 'K', 'AC': 'M',
         'CGT': 'B', 'AGT': 'D', 'ACT': 'H', 'ACG': 'V', 'ACGT': 'N'}
DNA = set('ACGTURYSWKMBDHVN-?.')


def expand(spec):
    """'1 - 6 1048 - 1074' or '7 - 1045 \\ 3' -> set of 0-based column indices."""
    spec = re.sub(r'(?<=\d)\s*-\s*(?=\d)', ' - ', spec)   # '1-525' and '1 - 525' both occur
    spec = spec.replace('\\', ' \\ ')
    toks = spec.split()
    out, i = set(), 0
    while i < len(toks):
        if not toks[i].lstrip('-').isdigit():
            i += 1
            continue
        a = int(toks[i])
        b, step, j = a, 1, i + 1
        if j < len(toks) and toks[j] == '-':
            b = int(toks[j + 1])
            j += 2
        if j < len(toks) and toks[j] == '\\':
            step = int(toks[j + 1])
            j += 2
        out |= set(range(a - 1, b, step))
        i = j
    return out


src, name = sys.argv[1], sys.argv[2]
txt = Path(src).read_text(errors='ignore')
txt = re.sub(r'\[[^\]]*\]', ' ', txt)   # strip NEXUS comments first: the header holds "[Matrix accession#: ...]"
nchar = int(re.search(r'NCHAR\s*=\s*(\d+)', txt, re.I).group(1))

# sequences: in the MATRIX block, tokens alternate taxon / sequence (works interleaved or not)
mat = re.search(r'\bMATRIX\b(.*?);', txt, re.S | re.I).group(1)
toks = mat.split()
seqs, order, k = {}, [], 0
while k + 1 < len(toks):
    taxon, s = toks[k], re.sub(r'\{([A-Za-z]+)\}',
                               lambda m: IUPAC.get(''.join(sorted(set(m.group(1).upper()))), 'N'),
                               toks[k + 1].upper())
    if set(s) <= DNA and len(s) > 1:
        if taxon not in seqs:
            seqs[taxon] = []
            order.append(taxon)
        seqs[taxon].append(s)
        k += 2
    else:
        k += 1
seqs = {t: ''.join(v).upper().replace('?', 'N').replace('.', 'N') for t, v in seqs.items()}

charsets = [(n, expand(r)) for n, r in re.findall(r'CHARSET\s+(\S+)\s*=\s*([^;]+);', txt, re.I)]
exset = set()
for r in re.findall(r'EXSET\s+\S+\s*=\s*([^;]+);', txt, re.I):
    exset |= expand(r)
keep = [j for j in range(nchar) if j not in exset]
pos = {j: i for i, j in enumerate(keep)}

OUT.mkdir(parents=True, exist_ok=True)
ids = [f'S{i:03d}' for i in range(1, len(order) + 1)]
with open(OUT / f'{name}.fasta', 'w') as fa, open(OUT / f'{name}.phy', 'w') as ph, \
        open(OUT / f'{name}.names.tsv', 'w') as nm:
    ph.write(f'{len(order)} {len(keep)}\n')
    nm.write('id\toriginal_taxon\n')
    for sid, t in zip(ids, order):
        sub = ''.join(seqs[t][j] for j in keep)
        fa.write(f'>{sid}\n{sub}\n')
        ph.write(f'{sid} {sub}\n')
        nm.write(f'{sid}\t{t}\n')

with open(OUT / f'{name}.genes.nex', 'w') as f:   # author partition, remapped onto the kept columns
    f.write('#nexus\nbegin sets;\n')
    for cn, cols in charsets:
        v = sorted(pos[j] + 1 for j in cols if j in pos)
        if v:
            f.write(f'  charset {cn} = {" ".join(map(str, v))};\n')
    f.write('end;\n')

cols = list(zip(*[''.join(seqs[t][j] for j in keep) for t in order]))
var = sum(len(set(c) - set('-N')) > 1 for c in cols)
gaps = sum(c.count('-') for c in cols) / (len(keep) * len(order))
print(f'{name}: {len(order)} taxa x {len(keep)} sites (NCHAR {nchar}, excluded {len(exset)}), '
      f'variable {var} ({var/len(keep):.1%}), gaps {gaps:.1%}')
print(f'  charsets: {", ".join(f"{n}({len([j for j in c if j in pos])})" for n, c in charsets)}')
