"""Build a massive multi-locus chloroplast-genome alignment from annotated ENA records.

Same per-gene protocol as the mitogenome set (scripts/prep_mito.py): protein-coding genes are aligned in
translation space (plastid/bacterial code, table 11) and back-translated so reading frame is preserved;
rRNA and tRNA genes are aligned as nucleotides; genes are then concatenated.

Plastome specifics: the inverted repeat duplicates ~20 genes (including all four rRNAs), so only the first
copy of each gene per taxon is kept; gene content varies between taxa, so only genes present in at least
MIN_FRAC of taxa are used; the trans-spliced rps12 is skipped.
Writes plastome/aln/plastome.{fasta,phy}, .names.tsv and .genes.nex (per-gene, codon-position, rRNA and tRNA sets).
"""
import re
import subprocess
from collections import defaultdict
from pathlib import Path

from Bio import SeqIO
from Bio.Seq import Seq

D = Path('/home/diepht/sliferskyd/hPartition/rna_datasets/plastome')
MAFFT = '/home/diepht/miniconda3/envs/rnaaln/bin/mafft'
PLASTID_CODE = 11
MIN_FRAC = 0.8
SKIP = {'rps12'}            # trans-spliced: its exons are on separate strands


AA1 = {'ala':'A','arg':'R','asn':'N','asp':'D','cys':'C','gln':'Q','glu':'E','gly':'G','his':'H',
       'ile':'I','leu':'L','lys':'K','met':'M','phe':'F','pro':'P','ser':'S','thr':'T','trp':'W',
       'tyr':'Y','val':'V','fmet':'fM'}


def norm(name, ftype, anticodon=None):
    """Plastid submissions name the same gene several ways: rrn16 / rrn16S / '16S ribosomal RNA', and
    trnV-GAC / trnV / tRNA-Val. Normalise so homologous genes group across taxa."""
    n = name.strip()
    if ftype == 'rRNA':
        m = re.search(r'(4\.5|16|23|5)(?!\d)', n)
        return f'rrn{m.group(1)}' if m else None
    if ftype == 'tRNA':
        m = re.search(r'trn([A-Za-z]{1,4})[-_ ]?([ACGTU]{3})?', n, re.I)
        if m:
            aa, ac = m.group(1), m.group(2)
        else:
            m = re.search(r'tRNA[-_ ]([A-Za-z]{3})', n, re.I)
            if not m:
                return None
            aa, ac = AA1.get(m.group(1).lower()), None
        if aa and len(aa) > 2:
            aa = AA1.get(aa.lower(), aa)
        ac = (ac or anticodon or '').upper().replace('T', 'U')
        return f'trn{aa}-{ac}' if ac else (f'trn{aa}' if aa else None)
    n = re.sub(r'[^A-Za-z0-9.\-_]', '', n)
    return n.lower() or None


def anticodon_of(feat, rec):
    q = feat.qualifiers.get('anticodon', [''])[0]
    m = re.search(r'pos:\s*(?:complement\()?(\d+)\.\.(\d+)', q)
    if not m:
        m2 = re.search(r'aa:[A-Za-z]+,\s*seq:([acgtu]{3})', q, re.I)
        return m2.group(1).upper().replace('T', 'U') if m2 else None
    a, b = int(m.group(1)), int(m.group(2))
    sub = rec.seq[a - 1:b]
    if feat.location.strand == -1 or 'complement' in q:
        sub = sub.reverse_complement()
    return str(sub).upper().replace('T', 'U')


genes_nt, gene_type, taxa = defaultdict(dict), {}, []
for f in sorted((D / 'embl').glob('*.embl')):
    rec = next(SeqIO.parse(f, 'embl'))
    acc = f.stem
    taxa.append(acc)
    for feat in rec.features:
        if feat.type not in ('CDS', 'rRNA', 'tRNA'):
            continue
        q = feat.qualifiers
        g = norm(q.get('gene', q.get('product', ['']))[0], feat.type, anticodon_of(feat, rec))
        if not g or g in SKIP:
            continue
        try:
            seq = str(feat.extract(rec.seq)).upper()
        except Exception:
            continue
        if len(seq) < 60 or len(seq) > 20000:
            continue
        if acc in genes_nt[g]:          # inverted-repeat duplicate: keep the first copy only
            continue
        genes_nt[g][acc] = seq
        gene_type[g] = feat.type

keep = [g for g in genes_nt if len(genes_nt[g]) >= MIN_FRAC * len(taxa)]
order = ([g for g in sorted(keep) if gene_type[g] == 'CDS']
         + [g for g in sorted(keep) if gene_type[g] == 'rRNA']
         + [g for g in sorted(keep) if gene_type[g] == 'tRNA'])
print(f'{len(taxa)} taxa; {len(genes_nt)} gene names seen; {len(order)} kept (present in >={MIN_FRAC:.0%} of taxa): '
      f"{sum(gene_type[g]=='CDS' for g in order)} CDS, {sum(gene_type[g]=='rRNA' for g in order)} rRNA, "
      f"{sum(gene_type[g]=='tRNA' for g in order)} tRNA")

(D / 'genes').mkdir(exist_ok=True)
(D / 'aln').mkdir(exist_ok=True)


def mafft(path):
    out = subprocess.run([MAFFT, '--auto', '--quiet', str(path)], capture_output=True, text=True).stdout
    res, cur = {}, None
    for line in out.splitlines():
        if line.startswith('>'):
            cur = line[1:].strip(); res[cur] = []
        elif cur:
            res[cur].append(line.strip())
    return {k: ''.join(v).upper() for k, v in res.items()}


aligned = {}
for g in order:
    fn = D / 'genes' / f'{g}.fa'
    if gene_type[g] == 'CDS':
        pep = {}
        for a, s in genes_nt[g].items():
            s2 = s[:len(s) // 3 * 3]
            pep[a] = str(Seq(s2).translate(table=PLASTID_CODE)).rstrip('*').replace('*', 'X')
        fn.write_text(''.join(f'>{a}\n{p}\n' for a, p in pep.items()))
        ap = mafft(fn)
        res = {}
        for a, p in ap.items():
            nt = genes_nt[g][a]; nt = nt[:len(nt) // 3 * 3]
            i, buf = 0, []
            for ch in p:
                if ch == '-':
                    buf.append('---')
                else:
                    buf.append(nt[i * 3:i * 3 + 3].ljust(3, '-')); i += 1
            res[a] = ''.join(buf)
    else:
        fn.write_text(''.join(f'>{a}\n{s}\n' for a, s in genes_nt[g].items()))
        res = mafft(fn)
    L = max(len(v) for v in res.values())
    res = {a: v.ljust(L, '-') for a, v in res.items()}
    aligned[g] = {a: res.get(a, '-' * L) for a in taxa}

cat = {a: [] for a in taxa}
charsets, pos = [], 0
for g in order:
    L = len(next(iter(aligned[g].values())))
    for a in taxa:
        cat[a].append(aligned[g][a])
    charsets.append((g, pos + 1, pos + L)); pos += L
cat = {a: ''.join(v) for a, v in cat.items()}

(D / 'aln' / 'plastome.fasta').write_text(''.join(f'>{a}\n{cat[a]}\n' for a in taxa))
with open(D / 'aln' / 'plastome.phy', 'w') as f:
    f.write(f'{len(taxa)} {pos}\n')
    for a in taxa:
        f.write(f'{a} {cat[a]}\n')
with open(D / 'aln' / 'plastome.genes.nex', 'w') as f:
    f.write('#nexus\nbegin sets;\n')
    for g, a, b in charsets:
        f.write(f'  charset {re.sub(chr(45), "_", g)} = {a}-{b};\n')
    for i in (1, 2, 3):
        spec = ' '.join(f'{a + i - 1}-{b}\\3' for g, a, b in charsets if gene_type[g] == 'CDS')
        f.write(f'  charset codon{i} = {spec};\n')
    for t, lab in (('rRNA', 'rRNA'), ('tRNA', 'tRNA')):
        spec = ' '.join(f'{a}-{b}' for g, a, b in charsets if gene_type[g] == t)
        if spec:
            f.write(f'  charset {lab} = {spec};\n')
    f.write('end;\n')
cols = list(zip(*cat.values()))
var = sum(len(set(c) - set('-N')) > 1 for c in cols)
rna = sum(b - a + 1 for g, a, b in charsets if gene_type[g] in ('rRNA', 'tRNA'))
print(f'plastome: {len(taxa)} taxa x {pos} sites, {len(order)} loci, variable {var} ({var/pos:.1%}), '
      f'gaps {sum(c.count("-") for c in cols)/(pos*len(taxa)):.1%}, RNA sites {rna} ({rna/pos:.1%})')
