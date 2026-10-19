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
            'rabies_n100', 'denv1', 'denv1_n50', 'denv1_n100', 'zika', 'rubella', 'rubella_n50', 'rubella_n100',
            'hcv1b', 'hcv1b_n50', 'hcv1b_n100', 'hiv1b', 'hiv1b_n50', 'hiv1b_n100']
BASE_TAXA = {'rabies': 26, 'rubella': 35, 'hiv1b': 33}
FLU = Path('/home/diepht/sliferskyd/hPartition/rna_datasets/flu/aln')
PF = Path('/home/diepht/sliferskyd/hPartition/rna_datasets/pf/aln')      # PartitionFinder benchmark sets
FULL = Path('/home/diepht/sliferskyd/hPartition/rna_datasets/full/aln')  # epidemic-scale full alignments
DATASETS += sorted(p.stem for p in FLU.glob('flu_*.phy'))  # influenza HA sets (Qiu & Bahl BEAST XMLs)
DATASETS += ['saxifragales', 'midges', 'hummingbirds', 'barkbeetles', 'ebov_full']


def aln_dir(ds):
    for d in (PF, FLU, FULL, ALN):
        if (d / f'{ds}.fasta').exists():
            return d
    return ALN
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
    for line in open(aln_dir(ds) / f'{ds}.fasta'):
        line = line.strip()
        if line.startswith('>'):
            name = line[1:]
            seqs[name] = []
        elif name:
            seqs[name].append(line.upper())
    return list(zip(*[''.join(v) for v in seqs.values()]))


rows = []
for ds in DATASETS:
    cols = columns(ds)
    taxa = len(cols[0])
    for m in METHODS:
        r = dict(dataset=ds, virus=ds.split('_')[0], taxa=taxa, sites=len(cols), method=m)
        tag = {'hPartition': 'rnahpar', 'hPartition-PF': 'rnahpf',
               'gPartition': 'rnagpar', 'PsiPartition': 'rnapsi'}[m]
        if not (ROOT / 'done' / f'{tag}.rna.{ds}.0.ok').exists() \
                and not (ROOT / 'out_rna' / m / ds / 'NO_VALID_SCHEME').exists():
            r['status'] = 'not run / cancelled'
            rows.append(r)
            continue
        if m == 'PsiPartition':
            o = ROOT / 'out_rna' / m / ds
            itf = o / f'{ds}.iters.tsv'
            its = [l.split('\t') for l in itf.read_text().splitlines()[1:]] if itf.exists() else []
            r['psi_valid_iters'] = sum(i[7] != 'NA' for i in its)
            if (o / 'NO_VALID_SCHEME').exists() or not (o / 'final.nwk').exists():
                r['status'] = 'no valid scheme' if (o / 'NO_VALID_SCHEME').exists() else f'running ({len(its)}/30)'
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
