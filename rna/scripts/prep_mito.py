"""Build a multi-locus mitogenome alignment from annotated ENA records.

Follows the protocol of Leavitt et al. 2013 (Mol Phylogenet Evol 67:494-508), who analysed 34 grasshopper
mitogenomes: each gene is aligned separately and the genes are concatenated. Protein-coding genes are aligned
in translation space and back-translated, so reading frame (and therefore the codon-position charsets) is
preserved; rRNA and tRNA genes are aligned as nucleotides. Their alignment was never deposited, so this is a
reconstruction from the GenBank accessions listed in their Table 1, not their file.

Gene names vary between submissions (nad2/ND2, cob/cytb, trnI-gau/tRNA-Ile, rrnS/12S), so names are normalised
to the standard 37-gene metazoan mitochondrial set before grouping.
Outputs mito/aln/mito.{fasta,phy}, mito.names.tsv and the author-style partition schemes in mito.genes.nex.
"""
import re
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

from Bio import SeqIO
from Bio.Seq import Seq

import os
D = Path(os.environ.get('MITO_DIR', '/home/diepht/sliferskyd/hPartition/rna_datasets/mito'))
NAME = os.environ.get('MITO_NAME', 'mito')
MAFFT = '/home/diepht/miniconda3/envs/rnaaln/bin/mafft'
MITO_CODE = 5                      # invertebrate mitochondrial genetic code
PCG = ['atp6', 'atp8', 'cox1', 'cox2', 'cox3', 'cob', 'nad1', 'nad2', 'nad3', 'nad4', 'nad4l', 'nad5', 'nad6']
RRNA = ['rrnS', 'rrnL']
AA3 = ['Ala', 'Arg', 'Asn', 'Asp', 'Cys', 'Gln', 'Glu', 'Gly', 'His', 'Ile', 'Leu1', 'Leu2', 'Lys', 'Met',
       'Phe', 'Pro', 'Ser1', 'Ser2', 'Thr', 'Trp', 'Tyr', 'Val']
ONE2THREE = {'A': 'Ala', 'R': 'Arg', 'N': 'Asn', 'D': 'Asp', 'C': 'Cys', 'Q': 'Gln', 'E': 'Glu', 'G': 'Gly',
             'H': 'His', 'I': 'Ile', 'L': 'Leu', 'K': 'Lys', 'M': 'Met', 'F': 'Phe', 'P': 'Pro', 'S': 'Ser',
             'T': 'Thr', 'W': 'Trp', 'Y': 'Tyr', 'V': 'Val'}


def norm_pcg(name):
    n = re.sub(r'[^a-z0-9]', '', name.lower())
    alias = {'cytb': 'cob', 'cytochromeb': 'cob', 'coi': 'cox1', 'coii': 'cox2', 'coiii': 'cox3',
             'co1': 'cox1', 'co2': 'cox2', 'co3': 'cox3', 'nd1': 'nad1', 'nd2': 'nad2', 'nd3': 'nad3',
             'nd4': 'nad4', 'nd4l': 'nad4l', 'nd5': 'nad5', 'nd6': 'nad6', 'atpase6': 'atp6',
             'atpase8': 'atp8'}
    n = alias.get(n, n)
    return n if n in PCG else None


def norm_rrna(name):
    n = name.lower()
    if 's-rrna' in n or 'rrns' in n or '12s' in n or 'small subunit' in n:
        return 'rrnS'
    if 'l-rrna' in n or 'rrnl' in n or '16s' in n or 'large subunit' in n:
        return 'rrnL'
    return None


def norm_trna(name):
    """tRNA-Leu / trnI-gau -> 'Leu' / 'Ile'. Leu and Ser occur twice and are resolved later by anticodon."""
    m = re.search(r'(?:trn|tRNA[-_])([A-Za-z]{1,3})', name)
    if not m:
        return None
    tag = m.group(1)
    if len(tag) == 1:
        return ONE2THREE.get(tag.upper())
    return tag.capitalize() if tag.capitalize() in ONE2THREE.values() else ONE2THREE.get(tag[0].upper())


def anticodon_of(feat, rec):
    """Read the /anticodon qualifier's pos: range off the genome (reverse-complemented on the minus strand)."""
    q = feat.qualifiers.get('anticodon', [''])[0]
    m = re.search(r'pos:\s*(?:complement\()?(\d+)\.\.(\d+)', q)
    if not m:
        return None
    a, b = int(m.group(1)), int(m.group(2))
    sub = rec.seq[a - 1:b]
    if feat.location.strand == -1 or 'complement' in q:
        sub = sub.reverse_complement()
    return str(sub).upper().replace('T', 'U')


# Leu and Ser each have two mitochondrial copies, distinguished by anticodon:
#   Leu1 = UAG (CUN codons), Leu2 = UAA (UUR);  Ser1 = GCU (AGN), Ser2 = UGA (UCN)
DUP_AC = {('Leu', 'UAG'): 'Leu1', ('Leu', 'UAA'): 'Leu2',
          ('Ser', 'GCU'): 'Ser1', ('Ser', 'UGA'): 'Ser2'}

genes = defaultdict(dict)      # gene -> {accession: nucleotide seq}
taxa = []
for f in sorted((D / 'embl').glob('*.embl')):
    rec = next(SeqIO.parse(f, 'embl'))
    acc = f.stem
    taxa.append(acc)
    dup = defaultdict(list)    # (Leu|Ser) -> [(start, seq, anticodon)] resolved after the feature pass
    for feat in rec.features:
        q = feat.qualifiers
        name = (q.get('gene', q.get('product', ['']))[0])
        seq = str(feat.extract(rec.seq)).upper()
        if len(seq) < 30:
            continue
        if feat.type == 'CDS':
            g = norm_pcg(name)
        elif feat.type == 'rRNA':
            g = norm_rrna(name) or norm_rrna(q.get('product', [''])[0])
        elif feat.type == 'tRNA':
            aa = norm_trna(name)
            if aa in ('Leu', 'Ser'):
                dup[aa].append((int(feat.location.start), seq, anticodon_of(feat, rec)))
                continue
            g = f'trn{aa}' if aa else None
        else:
            continue
        if g and acc not in genes[g]:
            genes[g][acc] = seq
    for aa, copies in dup.items():
        copies.sort(key=lambda x: x[0])            # genomic order is the fallback when no anticodon is given
        for i, (_, seq, ac) in enumerate(copies[:2]):
            lab = DUP_AC.get((aa, ac)) if ac else None
            if lab is None:
                lab = f'{aa}{i + 1}'
            if acc not in genes[f'trn{lab}']:
                genes[f'trn{lab}'][acc] = seq

order = PCG + RRNA + [f'trn{a}' for a in AA3]
missing = [g for g in order if g not in genes]
print(f'{len(taxa)} taxa; genes found {len(genes)}; expected {len(order)}; missing {missing}')
for g in sorted(genes, key=lambda x: order.index(x) if x in order else 99):
    if g not in order:
        print(f'  (unrecognised gene name kept out: {g})')

(D / 'genes').mkdir(exist_ok=True)
(D / 'aln').mkdir(exist_ok=True)
aligned = {}
for g in order:
    if g not in genes or len(genes[g]) < 4:
        print(f'  skip {g}: present in {len(genes.get(g, {}))} taxa')
        continue
    raw, prot = D / 'genes' / f'{g}.fasta', D / 'genes' / f'{g}.pep'
    if g in PCG:                                  # translate -> align -> back-translate
        pep = {}
        for a, s in genes[g].items():
            s = s[:len(s) // 3 * 3]
            pep[a] = str(Seq(s).translate(table=MITO_CODE)).rstrip('*').replace('*', 'X')
        prot.write_text(''.join(f'>{a}\n{p}\n' for a, p in pep.items()))
        out = subprocess.run([MAFFT, '--auto', '--quiet', str(prot)], capture_output=True, text=True).stdout
        ap, cur = {}, None
        for line in out.splitlines():
            if line.startswith('>'):
                cur = line[1:].strip(); ap[cur] = []
            elif cur:
                ap[cur].append(line.strip())
        ap = {k: ''.join(v) for k, v in ap.items()}
        res = {}
        for a, p in ap.items():
            nt, i, buf = genes[g][a], 0, []
            nt = nt[:len(nt) // 3 * 3]
            for ch in p:
                if ch == '-':
                    buf.append('---')
                else:
                    buf.append(nt[i * 3:i * 3 + 3].ljust(3, '-')); i += 1
            res[a] = ''.join(buf)
    else:                                          # rRNA / tRNA: align nucleotides
        raw.write_text(''.join(f'>{a}\n{s}\n' for a, s in genes[g].items()))
        out = subprocess.run([MAFFT, '--auto', '--quiet', str(raw)], capture_output=True, text=True).stdout
        res, cur = {}, None
        for line in out.splitlines():
            if line.startswith('>'):
                cur = line[1:].strip(); res[cur] = []
            elif cur:
                res[cur].append(line.strip())
        res = {k: ''.join(v).upper() for k, v in res.items()}
    L = len(next(iter(res.values())))
    aligned[g] = {a: res.get(a, '-' * L) for a in taxa}
    print(f'  {g}: {len(res)}/{len(taxa)} taxa, {L} aligned sites')

# concatenate, record charsets
cat = {a: '' for a in taxa}
charsets, pos = [], 0
for g in order:
    if g not in aligned:
        continue
    L = len(next(iter(aligned[g].values())))
    for a in taxa:
        cat[a] += aligned[g][a]
    charsets.append((g, pos + 1, pos + L)); pos += L

(D / 'aln' / f'{NAME}.fasta').write_text(''.join(f'>{a}\n{cat[a]}\n' for a in taxa))
with open(D / 'aln' / f'{NAME}.phy', 'w') as f:
    f.write(f'{len(taxa)} {pos}\n')
    for a in taxa:
        f.write(f'{a} {cat[a]}\n')
with open(D / 'aln' / f'{NAME}.genes.nex', 'w') as f:
    f.write('#nexus\nbegin sets;\n')
    for g, a, b in charsets:
        f.write(f'  charset {g} = {a}-{b};\n')
    for i in (1, 2, 3):                            # codon positions pooled across the 13 PCGs
        spec = ' '.join(f'{a + i - 1}-{b}\\3' for g, a, b in charsets if g in PCG)
        f.write(f'  charset codon{i} = {spec};\n')
    f.write('  charset rRNA = ' + ' '.join(f'{a}-{b}' for g, a, b in charsets if g in RRNA) + ';\n')
    f.write('  charset tRNA = ' + ' '.join(f'{a}-{b}' for g, a, b in charsets if g.startswith('trn')) + ';\n')
    f.write('end;\n')
cols = list(zip(*cat.values()))
var = sum(len(set(c) - set('-N')) > 1 for c in cols)
print(f'\n{NAME}: {len(taxa)} taxa x {pos} sites, {len(charsets)} loci, variable {var} ({var/pos:.1%}), '
      f'gaps {sum(c.count("-") for c in cols)/(pos*len(taxa)):.1%}')
