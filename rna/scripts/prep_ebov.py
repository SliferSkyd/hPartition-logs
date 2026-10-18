"""Nested taxon subsets of the published EBOV Makona alignment (Dudas et al. 2017, Nature 544:309-315;
github.com/ebov/space-time, Data/Makona_1610_genomes_2016-06-23.fasta, CC-BY-SA-4.0).

The source is already aligned, so no realignment is done: the authors' columns are preserved and a subset only
drops columns that are all-gap within that subset. Filters match the other RNA datasets (<0.5% ambiguous
characters, identical sequences removed); sequences are stratified by country|district and drawn round-robin
with seed 0, so subsets are nested (20 subset of 50 subset of 100 ...).
Sequences are renamed to their GenBank accession (suffixed when an accession repeats); the original FASTA
headers are kept in <ds>.names.tsv. Writes ebov/aln/<ds>.{fasta,phy} (uppercase) and <ds>.selected.tsv.
"""
import collections
import random
from pathlib import Path

SRC = Path('/tmp/claude-10030/-work-backup-home-diepht-sliferskyd-hPartition/'
           '1841f9c7-ff4e-4032-9c4c-3cc4ce587094/scratchpad/ebov/Makona.fasta')
OUT = Path('/home/diepht/sliferskyd/hPartition/rna_datasets/ebov')
SIZES = [20, 50, 100, 200, 500]

seqs, name = {}, None
for line in open(SRC):
    line = line.strip()
    if line.startswith('>'):
        name = line[1:]
        seqs[name] = []
    elif name:
        seqs[name].append(line.upper())
seqs = {k: ''.join(v) for k, v in seqs.items()}

groups, seen, stats = collections.defaultdict(list), set(), collections.Counter()
for header, s in seqs.items():
    _, _, acc, country, district, date = header.split('|')
    if sum(c not in 'ACGT-' for c in s) > 0.005 * len(s):
        stats['ambiguous'] += 1
        continue
    if s in seen:
        stats['duplicate'] += 1
        continue
    seen.add(s)
    groups[f'{country}|{district}'].append((acc, header, s, country, district, date))

rng = random.Random(0)
keys = sorted(groups)
for k in keys:
    rng.shuffle(groups[k])
pool = {k: list(v) for k, v in groups.items()}
order, i = [], 0
while any(pool[k] for k in keys):
    k = keys[i % len(keys)]
    if pool[k]:
        order.append(pool[k].pop())
    i += 1
print(f'eligible {len(order)} of {len(seqs)}; filtered {dict(stats)}; {len(keys)} country|district groups')

(OUT / 'aln').mkdir(parents=True, exist_ok=True)
for n in SIZES:
    chosen = order[:n]
    cols = list(zip(*[s for _, _, s, *_ in chosen]))
    keep = [j for j, c in enumerate(cols) if set(c) != {'-'}]
    ids, used = [], collections.Counter()
    for acc, *_ in chosen:
        used[acc] += 1
        ids.append(acc if used[acc] == 1 else f'{acc}_{used[acc]}')
    ds = f'ebov_n{n}'
    with open(OUT / 'aln' / f'{ds}.fasta', 'w') as fa, open(OUT / 'aln' / f'{ds}.phy', 'w') as ph, \
            open(OUT / 'aln' / f'{ds}.selected.tsv', 'w') as md:
        ph.write(f'{len(chosen)} {len(keep)}\n')
        md.write('id\taccession\tcountry\tdistrict\tdate\toriginal_header\n')
        for sid, (acc, header, s, country, district, date) in zip(ids, chosen):
            sub = ''.join(s[j] for j in keep)
            fa.write(f'>{sid}\n{sub}\n')
            ph.write(f'{sid} {sub}\n')
            md.write(f'{sid}\t{acc}\t{country}\t{district}\t{date}\t{header}\n')
    sub_cols = [tuple(c[j] for c in [tuple(s) for _, _, s, *_ in chosen]) for j in []]  # placeholder
    cols2 = list(zip(*[''.join(s[j] for j in keep) for _, _, s, *_ in chosen]))
    var = sum(len(set(c) - set('-N?')) > 1 for c in cols2)
    gaps = sum(c.count('-') for c in cols2) / (len(keep) * len(chosen))
    print(f'{ds}: taxa={len(chosen)} sites={len(keep)} variable={var} ({var / len(keep):.1%}) '
          f'gaps={gaps:.2%} groups={len({c for _, _, _, c, *_ in chosen})}')
