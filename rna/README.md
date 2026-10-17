# RNA-virus empirical benchmark (reviewer request)

13 datasets from Nextstrain open data (GenBank genomes): measles, mumps, rabies, dengue-1 at 20(26)/50/100 taxa
(nested, genotype-stratified, seed 0) and Zika at 20 taxa. Design follows Patino-Galindo et al. 2018 (GBE 10:657,
doi:10.1093/gbe/evx273): complete genomes, MAFFT G-INS-1 (`--globalpair`), trimAl (`-gappyout`), uppercased.
Selection rules: `scripts/select_genomes.py`; accessions per dataset: `datasets/*.selected.tsv`.

Methods (IQ-TREE 2.4.0, seed 0, 1 thread; Psi -nt 4): hPartition (`-hPartition -mset JC69,F81,HKY,GTR`),
hPartition-PF (`-hPartition-pf`), gPartition, each evaluated with `iqtree2 -p <scheme>`; PsiPartition (30
Bayesian-optimisation iterations, k<=30; BIC from the authors' final best-configuration rerun).

Notes:
- PsiPartition iterations whose scheme contains a single-state partition make IQ-TREE abort ("Only one state is
  observed in partition"); they are recorded as failed runs, as in the original wandb sweep (`*.iters.tsv`, BIC NA).
  Mumps (20 taxa): all 30 failed -> `NO_VALID_SCHEME`. `results/onestate_all.tsv`: with equal base weights every
  k works on every dataset; with random weights 85-88% of configurations fail.
- PsiPartition's valid schemes put 47-81% of sites into partitions made only of invariant sites, split by base
  (GC-only / AT-only), which inflates likelihood (see `psi_sites_in_all_invariant_parts` in `results/rna_results.csv`).
