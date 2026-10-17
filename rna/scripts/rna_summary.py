"""RNA-virus benchmark summary -> results/rna/rna_results.csv (one row per dataset x method).
BIC/AICc/lnL from the evaluation IQ-TREE 2.4.0 report (hPartition, hPartition-PF, gPartition) or from Psi's
final best-config rerun. For Psi also: valid iterations out of 30, and the share of sites placed in partitions
whose sites are all invariant (the GC-only / AT-only binning artifact) and the number of 1-site partitions."""
import csv
import re
from pathlib import Path

ROOT = Path('/home/diepht/sliferskyd/hPartition/rerun_sim')
ALN = Path('/home/diepht/sliferskyd/hPartition/rna_datasets/aln')
DATASETS = ['measles', 'measles_n50', 'measles_n100', 'mumps', 'mumps_n50', 'mumps_n100', 'rabies', 'rabies_n50',
            'rabies_n100', 'denv1', 'denv1_n50', 'denv1_n100', 'zika']
METHODS = ['hPartition', 'hPartition-PF', 'gPartition', 'PsiPartition']


def grab(txt, pat):
    m = re.search(pat, txt)
    return float(m.group(1)) if m else None


def wall(p):
    try:
        m = re.search(r'Elapsed \(wall clock\) time.*: (\S+)', p.read_text())
    except OSError:
        return None
    if not m:
        return None
    return sum(float(v) * 60 ** i for i, v in enumerate(reversed(m.group(1).split(':'))))


def columns(ds):
    seqs, name = {}, None
    for line in open(ALN / f'{ds}.fasta'):
        line = line.strip()
        if line.startswith('>'):
            name = line[1:]
            seqs[name] = []
        elif name:
            seqs[name].append(line.upper())
    return list(zip(*[''.join(v) for v in seqs.values()]))


rows = []
for ds in DATASETS:
    taxa = int(ds.split('_n')[1]) if '_n' in ds else (26 if ds == 'rabies' else 20)
    cols = columns(ds)
    for m in METHODS:
        r = dict(dataset=ds, virus=ds.split('_')[0], taxa=taxa, sites=len(cols), method=m)
        if m == 'PsiPartition':
            o = ROOT / 'out_rna' / m / ds
            its = [l.split('\t') for l in (o / f'{ds}.iters.tsv').read_text().splitlines()[1:]]
            r['psi_valid_iters'] = sum(i[7] != 'NA' for i in its)
            if (o / 'NO_VALID_SCHEME').exists():
                r['status'] = 'no valid scheme'
                rows.append(r)
                continue
            rep, parts = (o / f'{ds}.final.iqtree').read_text(), (o / f'{ds}.final.parts').read_text()
            t = wall(o / 'time.txt')
            sets = [[int(x) - 1 for x in s.split()] for s in re.findall(r'charset \S+ = ([^;]+);', parts)]
            inv = lambda i: len(set(cols[i]) - set('-N')) <= 1  # noqa: E731
            r['psi_sites_in_all_invariant_parts'] = sum(len(s) for s in sets if all(inv(i) for i in s)) / len(cols)
            r['psi_one_site_parts'] = sum(len(s) == 1 for s in sets)
        else:
            o = ROOT / 'out_rna' / m / ds
            rep = (o / 'partition' / 'aln.iqtree').read_text()
            pfile = o / ('gPartition/' + f'{ds}.phy.FINAL.nex' if m == 'gPartition' else 'hPartition/aln.partitions')
            sets = re.findall(r'charset', pfile.read_text(), flags=re.I)
            t1 = wall(o / ('gPartition' if m == 'gPartition' else 'hPartition') / 'time.txt')
            t = (t1 or 0) + (wall(o / 'partition' / 'time.txt') or 0)
            r['partition_step_s'] = t1
            r['fallback_noR'] = (o / 'partition' / 'NORATE_FALLBACK').exists()
        r.update(status='ok', k=len(sets), BIC=grab(rep, r'BIC\) score: (\S+)'),
                 AICc=grab(rep, r'AICc\) score: (\S+)'), lnL=grab(rep, r'Log-likelihood of the tree: (\S+)'),
                 total_wall_s=t)
        rows.append(r)

out = ROOT / 'results' / 'rna'
out.mkdir(parents=True, exist_ok=True)
keys = ['dataset', 'virus', 'taxa', 'sites', 'method', 'status', 'k', 'BIC', 'AICc', 'lnL', 'partition_step_s',
        'total_wall_s', 'fallback_noR', 'psi_valid_iters', 'psi_sites_in_all_invariant_parts', 'psi_one_site_parts']
with open(out / 'rna_results.csv', 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=keys)
    w.writeheader()
    w.writerows(rows)
print(f'{len(rows)} rows -> {out}/rna_results.csv')
