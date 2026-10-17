"""Select n complete genomes per RNA virus from Nextstrain open data (raw/<virus>.{sequences.fasta,metadata.tsv}).

Rules (fixed, seed 0):
  * complete: ungapped length >= 95% of the reference genome length; non-ACGT characters < 0.5%
  * data use: if a dataUseTerms column exists (Pathoplexus-sourced measles), keep only OPEN records with an
    INSDC (GenBank/ENA) accession
  * identical sequences removed (first accession kept)
  * genotype-stratified: shuffle each genotype group (seed 0) and pick round-robin across groups until n, so
    the set spans the virus's diversity instead of n near-identical recent genomes
Taxon counts follow Patino-Galindo et al. 2018 (GBE 10:657) Table 1 where the virus is in that study.
Writes sel/<virus>.fasta (headers = INSDC accession) and sel/<virus>.selected.tsv.
With command-line taxon counts (e.g. `select_genomes.py 50 100`), writes sel/<virus>_n<N>.* instead, for
measles, mumps, rabies and denv1 (taxon-count scaling experiment).
"""
import csv
import random
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path('/home/diepht/sliferskyd/hPartition/rna_datasets')
VIRUSES = {  # name: (reference genome length, n taxa, genotype column)
    'measles': (15894, 20, 'genotype_ppx'),
    'mumps': (15384, 20, 'MuV_genotype'),
    'rabies': (11932, 26, 'host_group'),     # no genotype column; stratify by host group
    'denv1': (10735, 20, 'genotype_nextclade'),
    'zika': (10807, 20, 'region'),           # no genotype column; stratify by region
}
csv.field_size_limit(sys.maxsize)


def read_fasta(p):
    seqs, name, buf = {}, None, []
    for line in open(p):
        line = line.rstrip()
        if line.startswith('>'):
            if name:
                seqs[name] = ''.join(buf)
            name, buf = line[1:].split()[0], []
        else:
            buf.append(line)
    if name:
        seqs[name] = ''.join(buf)
    return seqs


out = ROOT / 'sel'
out.mkdir(exist_ok=True)
SIZES = [int(x) for x in sys.argv[1:]]
jobs = [(v, n, '') for v, (_, n, _) in VIRUSES.items()] if not SIZES else \
       [(v, n, f'_n{n}') for v in ['measles', 'mumps', 'rabies', 'denv1'] for n in SIZES]
for virus, n, suffix in jobs:
    ref_len, _, gcol = VIRUSES[virus]
    seqs = read_fasta(ROOT / 'raw' / f'{virus}.sequences.fasta')
    meta = list(csv.DictReader(open(ROOT / 'raw' / f'{virus}.metadata.tsv'), delimiter='\t'))
    groups, seen, stats = defaultdict(list), set(), defaultdict(int)
    for m in meta:
        acc = m['accession']
        s = seqs.get(acc, '').upper().replace('-', '')
        if not s:
            stats['no_seq'] += 1
            continue
        if 'dataUseTerms' in m:
            if m['dataUseTerms'] != 'OPEN' or not m.get('INSDC_accession'):
                stats['not_open_or_no_insdc'] += 1
                continue
            acc = m['INSDC_accession']
        if len(s) < 0.95 * ref_len:
            stats['incomplete'] += 1
            continue
        if sum(c not in 'ACGTU' for c in s) > 0.005 * len(s):
            stats['ambiguous'] += 1
            continue
        if s in seen:
            stats['duplicate'] += 1
            continue
        seen.add(s)
        g = (m.get(gcol) or 'NA').strip() or 'NA'
        groups[g].append((acc, s.replace('U', 'T'), m))
    rng = random.Random(0)
    keys = sorted(groups)
    for k in keys:
        rng.shuffle(groups[k])
    chosen, i = [], 0
    while len(chosen) < n and any(groups[k] for k in keys):
        k = keys[i % len(keys)]
        if groups[k]:
            chosen.append((k,) + groups[k].pop())
        i += 1
    eligible = sum(len(v) for v in groups.values()) + len(chosen)
    with open(out / f'{virus}{suffix}.fasta', 'w') as f:
        for g, acc, s, m in chosen:
            f.write(f'>{acc}\n{s}\n')
    with open(out / f'{virus}{suffix}.selected.tsv', 'w') as f:
        f.write(f'accession\t{gcol}\tdate\tcountry\tlength\n')
        for g, acc, s, m in chosen:
            f.write(f'{acc}\t{g}\t{m.get("date", "")}\t{m.get("country", "")}\t{len(s)}\n')
    print(f'{virus}{suffix}: {len(seqs)} genomes, eligible {eligible}, groups {len(keys)}, chosen {len(chosen)} '
          f'from {len({c[0] for c in chosen})} {gcol} groups; filtered {dict(stats)}')
