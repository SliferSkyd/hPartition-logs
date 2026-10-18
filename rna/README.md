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

## Additional dataset families (added later)

**PartitionFinder benchmark alignments** (`datasets/{saxifragales,midges,hummingbirds,barkbeetles}.*`).
Multi-locus alignments containing rRNA/tRNA, from the ten datasets used to validate PartitionFinder
(Lanfear et al. 2012, MBE 29:1695). These answer the reviewer in the idiom of the partitioning literature:
rRNA genes appear in 4 of PartitionFinder's 10 benchmark datasets, but always embedded in multi-locus
alignments rather than as standalone RNA data.

| dataset | taxa | sites | RNA component | invariant | source |
|---|---|---|---|---|---|
| saxifragales | 40 | 9,006 | 18S + 26S (57% of sites) | 74% | Fishbein et al. 2001, Dryad 10.5061/dryad.684 |
| midges | 74 | 2,701 | 16S | 50% | Ekrem et al. 2010, TreeBASE study 10378 matrix M5116 |
| hummingbirds | 164 | 3,821 | tRNA (210 sites) | 36% | McGuire et al. 2007, TreeBASE matrix M3354 |
| barkbeetles | 44 | 2,083 | 16S | 64% | Cognato & Vogler 2001, Dryad 10.5061/dryad.678 (Ips.poy.g2.nexus) |

Conversion notes (`scripts/prep_pf.py`, `scripts/prep_nexorg.py`):
- saxifragales: NEXUS uses GAP=':'; only the five gene CHARSETs are kept (9,006 of 9,237 columns), which is
  the subset PartitionFinder Table 1 reports.
- hummingbirds: the .nexorg EXSET excludes 301 of 4,122 columns, giving exactly the 3,821 of Table 1.
- midges: NEXUS ambiguity braces ({AG}) converted to IUPAC letters; the per-matrix TreeBASE download has no
  SETS block, so this is the one dataset without an author partition.
- barkbeetles: the Dryad package holds four alignments and none has Table 1's 1,896 sites; Ips.poy.g2.nexus
  (2,083 sites) is used because it alone matches the stated seven data blocks (16S + COI and EF1a codon
  positions) and contains no morphological characters.
- `<ds>.genes.nex` holds the author-defined gene/codon partition remapped onto the retained columns.

**Epidemic-scale alignment** (`datasets/ebov_full.*`): EBOV Makona, 1,610 taxa x 18,996 sites, from
Dudas et al. 2017 Nature 544:309 (github.com/ebov/space-time, CC-BY-SA-4.0). hPartition and gPartition only;
PsiPartition and the COVID runs were cancelled as too costly for the information they returned.

**Not redistributed here**: the influenza alignments that contain GISAID sequences, and the local SARS-CoV-2
alignment (GISAID-style names). Their results are in `results/rna_results.csv`; the alignments are not included.

`results/rna_results.csv` has one row per dataset x method, with status `ok`, `no valid scheme`
(PsiPartition produced none in 30 iterations) or `not run / cancelled`.
