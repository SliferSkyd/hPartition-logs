"""Nested taxon subsets of the pre-aligned SARS-CoV-2 global alignment
(~/diep/diep2026/journal/data_big/covid19.global.fasta, 3685 x 30462).

As for EBOV, the source alignment is used as-is (no realignment); a subset only drops columns that are all-gap
within it. Filters match the other RNA datasets (<0.5% ambiguous characters, identical sequences removed);
sequences are stratified by country|year (parsed from hCoV-19/<country>/<id>/<year> names) and drawn
round-robin with seed 0, so subsets are nested.
NOTE: most names follow the GISAID hCoV-19 convention; these sequences must not be redistributed publicly.
Writes covid/aln/<ds>.{fasta,phy} (uppercase, safe IDs) and <ds>.selected.tsv with the original headers.
"""
import collections
import random
from pathlib import Path

SRC = Path('/work/backup/home/diepht/diep/diep2026/journal/data_big/covid19.global.fasta')
OUT = Path('/home/diepht/sliferskyd/hPartition/rna_datasets/covid')
SIZES = [20, 50, 100, 200, 500]

seqs, name = {}, None
for line in open(SRC):
    line = line.strip()
    if line.startswith('>'):
        name = line[1:].split()[0]
        seqs[name] = []
    elif name:
        seqs[name].append(line.upper())
seqs = {k: ''.join(v) for k, v in seqs.items()}


def group_of(header):
    p = header.split('/')
    return f'{p[1]}|{p[-1]}' if len(p) >= 4 else 'reference|NA'


groups, seen, stats = collections.defaultdict(list), set(), collections.Counter()
for header, s in seqs.items():
    if sum(c not in 'ACGT-' for c in s) > 0.005 * len(s):
        stats['ambiguous'] += 1
        continue
    if s in seen:
        stats['duplicate'] += 1
        continue
    seen.add(s)
    groups[group_of(header)].append((header, s))

rng = random.Random(0)
keys = sorted(groups)
for k in keys:
    rng.shuffle(groups[k])
pool = {k: list(v) for k, v in groups.items()}
order, i = [], 0
while any(pool[k] for k in keys):
    k = keys[i % len(keys)]
    if pool[k]:
        order.append((k,) + pool[k].pop())
    i += 1
print(f'eligible {len(order)} of {len(seqs)}; filtered {dict(stats)}; {len(keys)} country|year groups')

(OUT / 'aln').mkdir(parents=True, exist_ok=True)
for n in SIZES:
    chosen = order[:n]
    cols = list(zip(*[s for _, _, s in chosen]))
    keep = [j for j, c in enumerate(cols) if set(c) != {'-'}]
    ds = f'covid_n{n}'
    subs = [''.join(s[j] for j in keep) for _, _, s in chosen]
    with open(OUT / 'aln' / f'{ds}.fasta', 'w') as fa, open(OUT / 'aln' / f'{ds}.phy', 'w') as ph, \
            open(OUT / 'aln' / f'{ds}.selected.tsv', 'w') as md:
        ph.write(f'{len(chosen)} {len(keep)}\n')
        md.write('id\tgroup\toriginal_header\n')
        for i2, ((grp, header, _), sub) in enumerate(zip(chosen, subs), 1):
            sid = f'S{i2:04d}'
            fa.write(f'>{sid}\n{sub}\n')
            ph.write(f'{sid} {sub}\n')
            md.write(f'{sid}\t{grp}\t{header}\n')
    c2 = list(zip(*subs))
    var = sum(len(set(c) - set('-N?')) > 1 for c in c2)
    pis = sum(sum(1 for b in set(c) - set('-N?') if c.count(b) >= 2) >= 2 for c in c2)
    gaps = sum(c.count('-') for c in c2) / (len(keep) * len(chosen))
    print(f'{ds}: taxa={len(chosen)} sites={len(keep)} variable={var} ({var / len(keep):.1%}) '
          f'PI={pis} ({pis / len(keep):.1%}) gaps={gaps:.2%} groups={len({g for g, *_ in chosen})}')
