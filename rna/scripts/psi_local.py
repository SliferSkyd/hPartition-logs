"""Run PsiPartition (PsiPartition_wandb.py) without a wandb.ai account.

Same search space / objective / per-iteration body as PsiPartition_wandb.py; the wandb cloud sweep
controller is replaced by the open-source wandb `sweeps` engine (same Bayesian algorithm) driven locally.
Changes vs. original (agreed with user): IQ-TREE 2.4.0 binary, `-seed 0` added to IQ-TREE, np.random
seeded for the Bayesian search. Outputs: <stem>.last.* = what the last iteration leaves on disk;
<stem>.final.* = the authors' final step (rerun with best-BIC k,w from the csv, as in comparison/test_PsiPartition.py). Per-iteration timings go to <stem>.iters.tsv; resumes from it if interrupted.
"""
import argparse
import random
import shutil
import sys
import time
from pathlib import Path

import numpy as np

PSI_DIR = '/home/diepht/sliferskyd/hPartition/PsiPartition'
IQTREE = '/home/diepht/sliferskyd/hPartition/iqtree-2.4.0-Linux-intel/bin/iqtree2'
sys.path.insert(0, PSI_DIR)

import subprocess  # noqa: E402

import sweeps  # noqa: E402
from sweeps import RunState, SweepRun  # noqa: E402

import utils  # noqa: E402
from PsiPartition_wandb import calculate_sorting  # noqa: E402
from utils import dna_str, extract_stat, remove_caches, write_part_file  # noqa: E402


def default_iqtree(options, log_file):
    rc = subprocess.call([IQTREE, '-redo', '-safe', '-seed', '0', *options],
                         stderr=log_file, stdout=log_file)
    pre = Path(options[options.index('-pre') + 1])
    log = pre.with_suffix('.log')
    if rc != 0 and log.exists() and 'optimizeWithEM' in log.read_text(errors='ignore'):
        # known IQ-TREE FreeRate EM assertion: rerun without +R models (agreed with user), and record it
        with open(pre.parent / 'NORATE_FALLBACK', 'a') as f:
            f.write(f'{time.ctime()}: FreeRate EM assertion; reran with -mrate E,I,G,I+G\n')
        subprocess.call([IQTREE, '-redo', '-safe', '-seed', '0', *options, '-mrate', 'E,I,G,I+G'],
                        stderr=log_file, stdout=log_file)


utils.default_iqtree = default_iqtree


def write_nwk(iqtree_report, out):
    """Copy the ML tree ('Tree in newick format:' section) of an IQ-TREE .iqtree report to `out`."""
    lines = Path(iqtree_report).read_text().splitlines()
    i = lines.index('Tree in newick format:')
    tree = next(line for line in lines[i + 1:] if line.strip())
    Path(out).write_text(tree.strip() + '\n')


def psi_partition(msa, fmt, alphabet, k, w, timing):
    t0 = time.time()
    _, sorting = calculate_sorting(msa, fmt, alphabet, w)
    timing['sort'] = time.time() - t0
    indices = np.digitize(sorting, np.linspace(sorting.min(), sorting.max(), k))
    write_part_file(Path(msa).with_suffix('.parts'), indices)
    t0 = time.time()
    with open(Path(msa).with_suffix('.log'), 'w') as log_file:
        remove_caches(Path(msa))
        Path(msa).with_suffix('.iqtree').unlink(missing_ok=True)  # remove_caches() keeps it; avoid stale BIC
        default_iqtree(['-s', msa, '-pre', Path(msa).with_suffix(''),
                        '-spp', Path(msa).with_suffix('.parts'), '-nt', '4'], log_file)
    timing['iqtree'] = time.time() - t0
    if not Path(msa).with_suffix('.iqtree').exists():
        log = Path(msa).with_suffix('.log')
        raise IterationFailed(log.read_text(errors='ignore') if log.exists() else '')
    return extract_stat(Path(msa).with_suffix('.iqtree'))


class IterationFailed(Exception):
    """IQ-TREE produced no report for this (k, w), e.g. 'Only one state is observed in partition'."""


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--msa', required=True)
    p.add_argument('--format', default='fasta')
    p.add_argument('--alphabet', default='dna')
    p.add_argument('--max_partitions', type=int, default=30)
    p.add_argument('--n_iter', type=int, default=30)
    p.add_argument('--seed', type=int, default=0)
    args = p.parse_args()
    assert args.alphabet == 'dna'

    params = {c: {'min': 0, 'max': 1, 'distribution': 'uniform'} for c in ['A', 'C', 'G', 'T', 'UNK']}
    sweep_config = {
        "method": "bayes", "name": "PsiPartition",
        "metric": {"goal": "minimize", "name": "BIC"},
        "parameters": {"k": {"values": list(range(2, args.max_partitions + 1))}, **params},
    }
    np.random.seed(args.seed)
    random.seed(args.seed)

    msa = args.msa
    iters_file = Path(msa).with_suffix('.iters.tsv')
    runs = []
    if iters_file.exists():  # resume
        for line in iters_file.read_text().splitlines()[1:]:
            f = line.split('\t')
            cfg = {'k': int(f[1]), 'A': float(f[2]), 'C': float(f[3]), 'G': float(f[4]),
                   'T': float(f[5]), 'UNK': float(f[6])}
            ok = f[7] != 'NA'
            runs.append(SweepRun(name=f'r{f[0]}', state=RunState.finished if ok else RunState.failed,
                                 config={a: {'value': v} for a, v in cfg.items()},
                                 summary_metrics={'BIC': float(f[7])} if ok else {}))
    else:
        iters_file.write_text('iter\tk\tA\tC\tG\tT\tUNK\tBIC\tAICc\tlogL\tnum_params\tsort_s\tiqtree_s\n')

    while len(runs) < args.n_iter:
        it = len(runs)
        suggestion = sweeps.next_run(sweep_config, runs)
        cfg = {a: v['value'] for a, v in suggestion.config.items()}
        k = int(cfg['k'])
        w = {'A': cfg['A'], 'C': cfg['C'], 'G': cfg['G'], 'T': cfg['T'], '-': cfg['UNK']}
        s = sum(w.values())
        w = {c: v / s for c, v in w.items()}
        timing = {}
        try:
            stat = psi_partition(msa, args.format, args.alphabet, k, w, timing)
        except IterationFailed as e:
            # In the original wandb sweep an exception marks the run failed and the agent continues; the run
            # counts toward --n_iter and logs no BIC. Reproduce that; no csv row (as in the original).
            err = next((l for l in str(e).splitlines() if l.startswith('ERROR')), 'ERROR: no .iqtree')
            with open(iters_file, 'a') as f:
                f.write(f'{it}\t{k}\t{cfg["A"]}\t{cfg["C"]}\t{cfg["G"]}\t{cfg["T"]}\t{cfg["UNK"]}\tNA\tNA\tNA\tNA\t'
                        f'{timing["sort"]:.1f}\t{timing.get("iqtree", 0):.1f}\n')
            runs.append(SweepRun(name=f'r{it}', state=RunState.failed, config=suggestion.config, summary_metrics={}))
            print(f'iter {it} k={k} FAILED ({err.strip()})', flush=True)
            continue
        for ext in ['iqtree', 'parts']:  # last successful iteration (.treefile would be wiped by remove_caches)
            shutil.copy(f'{Path(msa).with_suffix("")}.{ext}', f'{Path(msa).with_suffix("")}.lastok.{ext}')
        # same csv row as the original opt_func
        with open(Path(msa).with_suffix('.csv'), 'a') as f:
            f.write(f'{k},{stat["BIC"]},{stat["AICc"]},{stat["log-likelihood"]},{stat["num_params"]},')
            f.write(','.join([f'{w[c]}' for c in dna_str]))
            f.write('\n')
        with open(iters_file, 'a') as f:
            f.write(f'{it}\t{k}\t{cfg["A"]}\t{cfg["C"]}\t{cfg["G"]}\t{cfg["T"]}\t{cfg["UNK"]}\t'
                    f'{stat["BIC"]}\t{stat["AICc"]}\t{stat["log-likelihood"]}\t{stat["num_params"]}\t'
                    f'{timing["sort"]:.1f}\t{timing["iqtree"]:.1f}\n')
        runs.append(SweepRun(name=f'r{it}', state=RunState.finished, config=suggestion.config,
                             summary_metrics={'BIC': stat['BIC']}))
        print(f'iter {it} k={k} BIC={stat["BIC"]} sort={timing["sort"]:.0f}s iqtree={timing["iqtree"]:.0f}s',
              flush=True)

    # Keep what the last iteration left on disk as <stem>.last.*
    stem = Path(msa).with_suffix('')
    # NB: PsiPartition's remove_caches() deletes '<stem>.*.treefile' before every IQ-TREE call, so trees are
    # kept as last.nwk / final.nwk (names outside its glob), extracted from the .iqtree reports.
    if not Path(f'{stem}.last.iqtree').exists():
        for ext in ['iqtree', 'parts']:
            shutil.copy(f'{stem}.lastok.{ext}', f'{stem}.last.{ext}')
    write_nwk(f'{stem}.last.iqtree', Path(msa).parent / 'last.nwk')
    # Final step of the authors' pipeline (comparison/test_PsiPartition.py): take the best-BIC (k, w)
    # from the csv and run PsiPartition + IQ-TREE once more; its outputs are kept as <stem>.final.*
    if not Path(f'{stem}.final.iqtree').exists():
        rows = [line.split(',') for line in Path(msa).with_suffix('.csv').read_text().splitlines()]
        best = min(rows, key=lambda r: float(r[1]))
        k = int(best[0])
        w = dict(zip(dna_str, (float(x) for x in best[5:10])))
        s = sum(w.values())
        w = {c: v / s for c, v in w.items()}
        timing = {}
        stat = psi_partition(msa, args.format, args.alphabet, k, w, timing)
        for ext in ['treefile', 'iqtree', 'parts']:
            shutil.copy(f'{stem}.{ext}', f'{stem}.final.{ext}')
        print(f'final k={k} BIC={stat["BIC"]} (best iter BIC={best[1]}) sort={timing["sort"]:.0f}s '
              f'iqtree={timing["iqtree"]:.0f}s', flush=True)
    write_nwk(f'{stem}.final.iqtree', Path(msa).parent / 'final.nwk')


if __name__ == '__main__':
    main()
