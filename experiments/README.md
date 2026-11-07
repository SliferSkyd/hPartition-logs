# Experiments added during the PeerJ revision

Runs that are not part of the original benchmark. Each keeps only the files needed to
reproduce the numbers reported: the scheme, the ModelFinder report, the evaluated `.iqtree`
and timings.

## `novar/` — variant-only seeding (8 alignments)

Tests whether hPartition's larger candidate-model count comes from binning all sites where
gPartition bins only variant ones. Stage 2 was patched to bin variant sites only, with
`k0 = floor(m/100)` unchanged and invariant sites scattered afterwards.

**Result: the hypothesis fails in the opposite direction.** k roughly doubles on all eight
datasets and BIC worsens on seven:

| dataset | k (standard → variant-only) | BIC delta |
|---|---|---|
| Arctiina | 32 → 56 | +953 |
| Calisto | 25 → 45 | +398 |
| Choreutidae | 27 → 60 | +1,815 |
| Coenonymphina | 28 → 40 | +848 |
| Geometridae | 37 → 52 | −1,253 |
| Morpho | 34 → 57 | +1,009 |
| Noctuidae | 38 → 63 | +332 |
| Pieridae | 37 → 55 | +3,897 |

Invariant sites all take rate 0 and so occupy the lowest bin; that bin absorbs 30–60% of the
alignment and the remaining variant sites spread coarsely, so fewer bins survive the `tau = 50`
merge. Removing them lets the variant sites fill the bins evenly and more survive. The Table S2
gap against gPartition therefore comes from the differing bin-count formula
(`floor(m/100)` against gPartition's `max(2T-3,100)/nVar`), not from invariant-site handling.

## `seedvar/` — seed variance (8 alignments x 5 seeds)

hPartition's Stage-4 invariant assignment is stochastic, but every BIC in the paper is from a
single seed. These runs repeat the pipeline at seeds 0–4 with the production binary; the
evaluation is held at `-seed 0` so all variation comes from partitioning.

## `diffuse/` — Stage-4 likelihood matrix (Morpho, Choreutidae)

`calcLH` writes every candidate model's per-site log-likelihoods to the same path, so only the
last survives a normal run. These rows replay the matrix with stock IQ-TREE
(`-m <model> -t <MF tree> -blfix --sitelh`), one model at a time.

Measured on invariant sites: the modal model takes 5.0% (Morpho, 35 models) and 12.8%
(Choreutidae, 44 models) of the sampling probability, against 100% under deterministic
assignment. The effective number of models each site chooses between, `1/sum(p^2)`, is 31.1 and
12.3; the realised allocation of invariant sites across final subsets is 31.2 and 11.9 — close
agreement, consistent with the dispersal being produced by the sampling step itself.

Not used in the manuscript: the invariant-site section there makes an output claim, not a
mechanism claim. Kept as backing in case a referee asks why the clumping does not occur.


---

# Empirical-DNA reruns on the replacement cluster

The cluster that produced the submitted benchmark was decommissioned before the revision, so
every method compared against a revision experiment was rerun here. These directories hold
those runs. Excluded everywhere: `*.sitelh` (11 GB of Stage-4 per-site likelihood matrices,
regenerable from the alignment and seed), `*.ckp.gz`, `*.model.gz`, `*.log`, `*.mldist`, and
the alignments themselves, which live in `hPartition-datasets`.

| directory | what it is | appears in the paper as |
|---|---|---|
| `hparbase/` | hPartition on the large DNA alignments | Tables 5 and 8 |
| `gpar_dna/` | gPartition on the same alignments | Tables 5 and 8 |
| `fullmset/` | hPartition with `-mset` omitted, and gPartition beside it, on 15 of the 17 DNA alignments | **Supplementary Table S5** |
| `memcap/` | peak-RSS measurements | memory discussion |
| `gpar_rep/`, `gpar2/`, `gpar5/` | gPartition replicates and variants | — |
| `scaling/` | runtime against alignment length | — |
| `stability/` | clumped-scheme control | — |
| `datatype/` | binary, codon and morphological runs | data-type claim in the Discussion |

Not in the paper, kept as backing:

| directory | question it answers |
|---|---|
| `pinvar/` | does the proportion of invariant sites change hPartition's standing against PsiPartition? 180 runs over `-i` in {0, .15, .30, .45, .60, .75} |
| `divsweep/` | is the seed-bin divisor of 100 the best choice? 100 and 50 each win 4 of 8 |
| `lhreassign/` | dissolving the zero-variance subsets and reassigning their sites by hPartition's own Stage-5 rule; hPartition keeps the lower BIC in all 25 runs |
| `zerovar/`, `scatter/` | earlier forms of the same question |
| `psimorpho/`, `test_psi/` | PsiPartition behaviour checks |
