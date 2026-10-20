# hPartition revision — state of work

Snapshot of a Claude Code session running 2026-10-15 to 2026-10-20 on the `fit` cluster.
Written so the work can be picked up elsewhere if this machine is unavailable.

The full transcript is `session-1841f9c7.jsonl.gz` (8,740 messages). Resume it with
`claude --resume 1841f9c7-ff4e-4032-9c4c-3cc4ce587094` from `/home/diepht/sliferskyd/hPartition`,
or read the `.jsonl` directly — one JSON object per line, `type` is `user` or `assistant`.

---

## 1. What this is

Revision of **hPartition** (PeerJ #137879) in response to referee comments, plus a new RNA benchmark
the referee asked for. Two threads:

- **Manuscript** — all 12 referee points addressed. `github.com/SliferSkyd/hPartition-manuscript`
- **Benchmarks** — simulated rerun, RNA datasets, several new experiments. `github.com/SliferSkyd/hPartition-logs`

## 2. Where things are

| | path | remote |
|---|---|---|
| Manuscript | `hPartition/hPartition__PeerJ_/` | `SliferSkyd/hPartition-manuscript` (branch `master` → `main`) |
| Benchmark archive | `hPartition/hPartition-sim-rerun/` | `SliferSkyd/hPartition-logs` (`main`) |
| Live working dir | `hPartition/rerun_sim/` | not a repo; archived via `scripts/sync_archive.sh` and `scripts/sync_rna.sh` |
| RNA datasets | `hPartition/rna_datasets/` | archived into the logs repo under `rna/` |
| Paper's own datasets | `hPartition-datasets/` | `SliferSkyd/hPartition-datasets` |
| hPartition source | `hPartition/iqtree2/` (branch `hPartition`, commit `d5dfc676`) | `SliferSkyd/iqtree2` |

Binaries: hPartition is `iqtree2/build/iqtree2`; evaluation uses stock
`iqtree-2.4.0-Linux-intel/bin/iqtree2`. **Clear `LD_LIBRARY_PATH` before running anything** —
`~/.localnew/lib64` shadows the libstdc++ that libpoppler and pdflatex need.

## 3. Manuscript — done

All 12 referee points. `git diff d9fc732 HEAD` in the manuscript repo shows everything.

| pt | what changed |
|---|---|
| 1 | pseudocode moved to main text as Algorithm 1 (original wording kept; constants in prose above it) |
| 2 | Stage 3 described correctly — one `-m MF -p --fast` call, edge-linked proportional, **not** joint optimisation |
| 3 | merge criterion specified: Pearson corr of flattened Q matrices, ε = 0.9995, nucleotide-only |
| 4 | T is single-pass and **not** used for any reported score; evaluation is an independent IQ-TREE run |
| 5 | worked example as a 7-panel figure (prose section deleted; caption is self-contained) |
| 6 | per-stage complexity section, with provenance of every expression |
| 7 | invariant-site claims softened; measured residuals reported |
| 8 | parity-of-settings paragraph, including two asymmetries that disfavour hPartition |
| 9 | PsiPartition failures identified as memory exhaustion |
| 10 | Figures 3–4 replaced with distribution boxplots; Wilcoxon statistics added |
| 11 | Tables 6/8 kept separate, with cross-references explaining why |
| 12 | Q.insect → Q.plant; Jarvis noted as Q.bird training data |

Building: TeX Live 2020 here lacks `authblk`, `algorithmicx`, `lastpage`, `lipsum`, and `tlmgr` is
blocked by the Fedora wrapper. `BUILD.md` in the manuscript repo has the CTAN workaround. Expected:
26 pages, 0 undefined references, 0 overfull boxes.

## 4. Benchmarks — done

**Simulated (SimDNA1/2, 600 runs).** Reproduces the paper's Figures 2–3. Paired per-alignment:
hPartition better on 56/100 and 70/100 vs gPartition, 66/100 and 85/100 vs PsiPartition;
Wilcoxon p = 1.6×10⁻⁸ … 1.6×10⁻¹⁵.

**RNA benchmark, 53 datasets.** hPartition 51/51, gPartition 51/51, hPartition-PF 48/48 complete;
PsiPartition 35/46 (the rest cancelled on request or failed).

- virus genomes: hPartition beats gPartition 20/29, loses to Psi 7/22
- influenza HA: beats gPartition **17/17**; loses to Psi 0/9
- multi-locus (7 sets): **hPartition 6/7**, gPartition 0/7, Psi 1/7

**Multi-locus final numbers** (BIC, lower better):

| dataset | const% | hPartition | gPartition | Psi | author scheme |
|---|---|---|---|---|---|
| beetle | 28.1% | **768,504** | 776,054 | 825,860 | 825,691 |
| mito | 32.6% | **390,994** | 395,536 | 419,211 | 433,274 |
| hummingbirds | 35.6% | **180,331** | 182,122 | 185,876 | 184,805 |
| midges | 49.6% | **78,503** | 80,212 | 80,030 | — |
| plastome | 57.0% | **1,030,912** | 1,057,690 | — | 1,227,147 |
| barkbeetles | 60.0% | **36,250** | 37,202 | 36,603 | — |
| saxifragales | 73.7% | 81,798 | 81,503 | **76,838** | — |

**PsiPartition reliability:** 958 of 1,177 iterations failed (81%); 951 of those with
`ERROR: Only one state is observed in partition partN`. hPartition never failed.

## 5. Findings that cut against the paper

Recorded because they are easy for a referee to reproduce.

**(a) Invariant-site dispersal costs model fit.** Counterfactual: hPartition's own scheme, with all
invariant sites moved into one subset. Clumping wins on **8/8** datasets, mean −2,453 BIC
(range 621–3,448). So dispersing invariant sites is a trade, not an advantage.
Runs in `rna/runs/stability/`; builder `rerun_sim/bin/make_clumped.py`.

**(b) The stated reason for dispersal is not supported.** The Discussion claims clumping causes
"numerical instabilities and boundary-case parameter estimates". Measured: the all-invariant subset
gets rate multiplier ≈ 0 (0.0000–0.0023 vs 0.66–1.17 for the next-lowest subset) and ModelFinder
selects a parameter-poor model (JC or F81+F). No crashes, no wild estimates. There is no
`MIN_PART_RATE` in the code, so "lower bound of the optimizer" is unsupported.

**(c) Jarvis is not an unseen dataset.** QMaker trained Q.bird on the avian data underlying it, so
the "generalization to unseen data" argument only holds for Ballesteros and Irisarri.

**(d) "Traditional split-then-merge algorithms"** (Discussion) names no real class of method and has
no citation. It describes gPartition's behaviour specifically (`gPartition.py:572, 592-597`).

## 6. Provenance of the RNA datasets

Full detail in `rna_datasets/PROVENANCE.md`. Summary:

- **Authentic PartitionFinder files** — barkbeetles and saxifragales recovered from *deleted git
  history* in `roblanf/BenchmarkAlignments` (commits `ed04781e4c`, `f7908d9d01`; the files are
  `.gitignore`d at HEAD). midges is the TreeBASE original submission, fetched via
  `downloadANexusFile.html;jsessionid=...?id=10378&matrixid=5116` — the `?format=nexus` PhyloWS
  exports omit the SETS block, which is how its charsets were lost originally.
  Sources kept in `rna_datasets/pf/src/`.
- **Reconstructions** — mito (Leavitt et al. 2013 accessions) and beetle (Timmermans et al. 2016
  Table S1). Neither author alignment was deposited, so these are ours, not theirs.
- **Entirely ours** — plastome. Four arbitrary decisions, listed in PROVENANCE.md.

Switching barkbeetles to PartitionFinder's actual 1,897-site file **flipped its result** from
PsiPartition to hPartition. Note PartitionFinder's Table 1 says 1,896 sites; their own file,
charsets and `summary.csv` all say 1,897.

## 7. In flight at snapshot time

**Variant-only seeding experiment.** Tests whether hPartition's much larger candidate-model count
(Table S2) comes from binning *all* sites where gPartition bins only variant ones.

- patched source: `hPartition/iqtree2-novar/` — Stage 2 bins variant sites only, `k₀ = ⌈m/100⌉`
  unchanged, invariant sites scattered at random afterwards
- build: `cd iqtree2-novar/build && make iqtree2 -j6` (**not** `make all` — googletest needs
  `std::u8string` and the local libstdc++ is 7.3.0)
- runs: `rerun_sim/tasks/novar.list`, submit with `sbatch -p short -c 8 bin/worker.sh novar`
- output: `rerun_sim/out_novar/`; compare candidate-model count, final k and BIC against
  Arctiina 32/32/93,223 · Calisto 25/25/77,973 · Choreutidae 40/27/107,071 ·
  Coenonymphina 33/28/118,367 · Geometridae 45/37/357,443 · Morpho 34/34/51,033 ·
  Noctuidae 48/38/188,568 · Pieridae 46/37/251,899

Had not completed at snapshot time; the build failed twice for unrelated reasons.

## 8. Open decisions

1. **How to frame the invariant-dispersal result** (§5a/b). Report the trade openly, or withdraw the
   claim quietly? Affects the abstract, Results and Conclusions.
2. **Rewrite "split-then-merge"** (§5d) to name gPartition and k-means, using references already cited.
3. **Algorithm 1** — main text (where it is now, as the referee asked) or back to the supplement?
4. **Duplicated data** — an `RNA/` tree was pushed to `hPartition-datasets` (commit `fb0fb62`)
   before the correct repos were named; the same material now lives in `hPartition-logs`.
5. **Vietnamese manuscript** `peerj-main-vi.tex` still carries the pre-revision text.
6. **Psi never submitted** for covid_n*, ebov_n20, ebov_n50 — six datasets, so the win/loss tallies
   are drawn from an incomplete set.

## 9. Cluster notes

- Slurm; `short`/`normal`/`long` queues; nodes have 32–36 cores and 63.5 or 112 GB (**not** more —
  the larger QoS figures are aggregate, not per node)
- **Do not run on the login node, and do not disturb other users' jobs**
- Work is dispatched by `rerun_sim/bin/worker.sh <queue>`, which claims tasks atomically with
  `mkdir`. PsiPartition hard-codes `-nt 4`, so any Psi job needs `--export=ALL,LANE_CPUS=4` or it
  oversubscribes
- TreeBASE and NCBI are unreliable from here; ENA works
