# hPartition — simulated-data rerun (SimDNA1 / SimDNA2)

Rerun of the simulated experiments of the hPartition manuscript (PeerJ #137879), done in October 2026 because
the original outputs were lost and a reviewer asked for per-replicate RF distributions rather than only means.
Runs used Slurm on the `fit` cluster. Working directory: `/home/diepht/sliferskyd/hPartition/rerun_sim`. This
repo is a snapshot of it, refreshed with `scripts/sync_archive.sh`.

## Data
`/home/diepht/sliferskyd/hPartition-datasets/DNA/simulated-1` (SimDNA1: 10 loci counts × 10 replicates, 5,000
sites) and `simulated-2` (SimDNA2: 6–15 loci × 1,000 sites, 10 replicates each); 49 taxa; true trees `<rep>.tree`.
These are byte-identical to the PsiPartition authors' `PsiPartition/data/DNA/simulated{,-seqlen}`.

## Methods and exact commands
IQ-TREE 2.4.0 throughout (stock binary `iqtree-2.4.0-Linux-intel/bin/iqtree2`; hPartition = `iqtree2/build/iqtree2`,
a non-MPI 2.4.0 build at commit d5dfc676). One core per run (Psi: 4 threads, as in its code). Seeds as in the old
scripts (`-seed 0`).

| Method | Partitioning | Evaluation (tree compared to truth) |
|---|---|---|
| hPartition | `iqtree2 -seed 0 -s ALN -pre P -hPartition -redo -mset JC69,F81,HKY,GTR -T 1` → `P.partitions` | `iqtree2 -seed 0 -s ALN -p P.partitions -pre E -redo -T 1` → `E.treefile` |
| gPartition | `python gPartition.py -f ALN -o OUT/` → `OUT/<rep>.phy.FINAL.nex` | same evaluation command with that scheme |
| PsiPartition | 30 Bayesian-optimisation iterations, k ∈ 2..30, A/C/G/T/UNK ~ U[0,1], minimise BIC; IQ-TREE `-spp parts -nt 4 -seed 0` per iteration | `final.nwk` = authors' final step (rerun with best-BIC k,w; `comparison/test_PsiPartition.py`); `last.nwk` = last iteration |

RF = ete3 `robinson_foulds(unrooted_trees=True)`, as in the old `summarize.py`.

## Deviations from the old scripts (all agreed with the author)
1. **hPartition uses `-hPartition`**, not `-hPartition-pf` as the old `simulated/hPartition.sh` did.
2. **hPartition output file**: current code writes `<pre>.partitions` (not `<pre>/partitions.nexus`, which was
   pre-commit 6a73a075 behaviour); the evaluation reads that file.
3. **gPartition** patched to call IQ-TREE 2.4.0 (`iqtree` → `iqtree2`, path in `config.py`):
   `patches/gPartition-iqtree2.patch`. gPartition seeds Python's `random` from the clock (unchanged), so its schemes
   are not bit-reproducible.
4. **PsiPartition without a wandb.ai account**: `scripts/psi_local.py` drives the same Bayesian search with wandb's
   open-source `sweeps` engine (wandb 0.16.1 + sweeps 0.2.0; conda env `PsiPartition` in miniconda3) instead of
   the wandb cloud sweep; `np.random.seed(0)` and IQ-TREE `-seed 0` added; IQ-TREE 1.6.12 → 2.4.0. Both the
   last-iteration tree and the authors' final best-config tree are kept.
5. **+R fallback**: if an evaluation aborts on IQ-TREE's FreeRate assertion (`ratefree.cpp: optimizeWithEM`), that
   replicate is rerun with `-mrate E,I,G,I+G` (no +R models); marked by a `NORATE_FALLBACK` file. So far:
   hPartition SimDNA2 10 loci rep 6 only.
6. Psi runs that started before 2026-10-16 02:58 lost `<rep>.last.treefile` to PsiPartition's own
   `remove_caches()`; their trees were rebuilt from the `.iqtree` reports (identical newick; `fixed_from_iqtree=1`
   in `status.txt`).

## Layout
- `results/per_rep.csv` — one row per (dataset, loci, replicate, method): RF, maxRF, nRF, BIC, wall-clock seconds.
- `results/summary.csv` — per loci count: n, mean, SD, median, IQR, min, max of RF.
- `results/psi_orig_per_rep.csv` — RF of the PsiPartition authors' original IQ-TREE 1.6.12 results (all their methods).
- `results/rf_boxplots.{png,pdf}` — per-replicate RF box plots.
- `runs/<method>/<dataset>/<loci>/<rep>/` — essentials of each run: partition scheme, IQ-TREE `.iqtree` report
  and `.log`, trees, `time.txt` (`/usr/bin/time -v`), Psi `<rep>.iters.tsv` (per-iteration k, weights, BIC, timings)
  and `<rep>.csv` (original PsiPartition format), `status.txt`. Bulky intermediates (site likelihoods, checkpoints,
  distance matrices, alignments) are not archived; they remain in `rerun_sim/out/`.
- `scripts/` — task generators (`gen_*.sh`), Slurm worker (`worker.sh`), evaluation wrapper (`eval_iqtree.sh`),
  Psi driver (`psi_local.py`), summaries/plots (`summarize.py`, `psi_orig_rf.py`, `plot_rf.py`).
- `tasks/` — the exact per-run commands that were executed; `logs/` — status markers and Slurm worker logs.

## Regenerating the tables
```
/home/diepht/anaconda3/bin/python scripts/summarize.py      # needs ete3; paths point at rerun_sim/
/home/diepht/anaconda3/bin/python scripts/plot_rf.py
```
