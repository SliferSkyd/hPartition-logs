"""Write the biologists' own partition schemes as IQ-TREE partition files, to score alongside the methods.

The *.genes.nex files hold overlapping alternatives (a gene charset and that gene's codon-position charsets
both cover the same columns), which IQ-TREE's -p will not accept. Two non-overlapping schemes are emitted:
  <ds>.author_locus.nex   one subset per locus (gene)
  <ds>.author_codon.nex   protein-coding loci split by codon position; rRNA/tRNA loci left whole
"""
import re
from pathlib import Path

B = Path('/home/diepht/sliferskyd/hPartition/rna_datasets')


def expand(spec):
    spec = re.sub(r'(?<=\d)\s*-\s*(?=\d)', ' - ', spec).replace('\\', ' \\ ')
    toks = spec.replace(',', ' ').split()
    out, i = set(), 0
    while i < len(toks):
        if not toks[i].isdigit():
            i += 1; continue
        a = int(toks[i]); b = a; st = 1; j = i + 1
        if j < len(toks) and toks[j] == '-': b = int(toks[j + 1]); j += 2
        if j < len(toks) and toks[j] == '\\': st = int(toks[j + 1]); j += 2
        out |= set(range(a, b + 1, st)); i = j
    return out


def ranges(xs):
    xs = sorted(xs); out = []; a = p = xs[0]
    for x in xs[1:]:
        if x == p + 1: p = x
        else: out.append((a, p)); a = p = x
    out.append((a, p))
    return ' '.join(f'{u}-{v}' if u != v else str(u) for u, v in out)


def write(path, parts, L):
    cov = set()
    for v in parts.values(): cov |= v
    assert len(cov) == L, f'{path}: covers {len(cov)} of {L}'
    tot = sum(len(v) for v in parts.values())
    assert tot == L, f'{path}: {tot - L} overlapping positions'
    with open(path, 'w') as f:
        f.write('#nexus\nbegin sets;\n')
        for n, v in parts.items():
            f.write(f'  charset {n} = {ranges(v)};\n')
        f.write('end;\n')
    print(f'  {path.name}: {len(parts)} subsets, {L} sites')


PCG13 = ['atp6','atp8','cox1','cox2','cox3','cob','nad1','nad2','nad3','nad4','nad4l','nad5','nad6']
JOBS = [('hummingbirds', B/'pf/aln'), ('barkbeetles', B/'pf/aln'), ('saxifragales', B/'pf/aln'),
        ('mito', B/'mito/aln'), ('beetle', B/'beetle/aln'), ('plastome', B/'plastome/aln')]

for ds, d in JOBS:
    gx = d / f'{ds}.genes.nex'
    if not gx.exists():
        print(f'{ds}: no genes.nex, skipped'); continue
    L = int(open(d / f'{ds}.phy').readline().split()[1])
    cs = {n: expand(s) for n, s in re.findall(r'charset (\S+) = ([^;]+);', gx.read_text())}
    print(f'{ds}:')
    def with_rest(loci, children):
        """locus -> its codon charsets; any columns a locus' codon charsets do not cover (e.g. the EF1a
        intron in barkbeetles, which has no reading frame) become a '<locus>_rest' subset."""
        out = {}
        for g, v in loci.items():
            # name per locus: the mito/plastome codon charsets are pooled across all genes, so the
            # raw charset name is the same for every locus and would collide
            kids = {f'{g}_p{i}': cs[k] & v for i, k in enumerate(children.get(g, []), 1) if k in cs}
            kids = {k: x for k, x in kids.items() if x}
            if not kids:
                out[g] = v; continue
            out.update(kids)
            rest = v - set().union(*kids.values())
            if rest: out[f'{g}_rest'] = rest
        return out

    if ds == 'hummingbirds':
        locus = {k: cs[k] for k in ['tRNA', 'ND2', 'ND4', 'AK1', 'bfib']}
        codon = with_rest(locus, {'ND2': ['ND2pos1', 'ND2pos2', 'ND2pos3'],
                                  'ND4': ['ND4pos1', 'ND4pos2', 'ND4pos3']})
    elif ds == 'barkbeetles':
        locus = {k: cs[k] for k in ['16s', 'EF1a', 'COI']}
        codon = with_rest(locus, {'COI': ['1st', '2nd', '3rd'], 'EF1a': ['1ef', '2ef', '3ef']})
    elif ds == 'saxifragales':
        locus = {k: cs[k] for k in ['atpB', '18S', 'rbcL', 'matK', '26S']}
        codon = None
    else:   # mito, beetle, plastome: gene charsets + pooled codon1/2/3 + rRNA + tRNA
        locus = {k: v for k, v in cs.items() if k not in ('codon1', 'codon2', 'codon3', 'rRNA', 'tRNA')}
        codon = with_rest(locus, {g: ['codon1', 'codon2', 'codon3'] for g in locus})
    write(d / f'{ds}.author_locus.nex', locus, L)
    if codon: write(d / f'{ds}.author_codon.nex', codon, L)
