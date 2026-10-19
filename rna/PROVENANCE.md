# Provenance of the multi-locus RNA-benchmark datasets

Three tiers, by how much of the dataset comes from the source publication.

## Tier 1 — published and deposited; used as the authors released it

### barkbeetles — 44 taxa × 2,083 sites, 9 charsets
- **Study:** Cognato AI, Vogler AP (2001). *Exploring data interaction and nucleotide alignment in a
  multiple gene analysis of* Ips *(Coleoptera: Scolytinae).* Systematic Biology 50(6):758–780.
- **Deposit:** Dryad `doi:10.5061/dryad.678`, local copy in
  `hPartition/doi_10_5061_dryad_678__v20090630/`
- **File used:** `Ips.poy.g2.nexus` (the POY gap-cost g2 alignment), NTAX=44 NCHAR=2083.
  Verified: its nine CHARSETs are byte-identical to our `pf/aln/barkbeetles.genes.nex`.
- **Genes:** 16S (1–525), EF1a (526–1314), COI (1315–2083), with codon-position charsets for both
  coding genes. EF1a's codon charsets cover only 526–1136; the remaining 1137–1314 is the **intron**,
  which has no reading frame.
- **Note:** this is *not* the alignment used in the PartitionFinder tutorial. That one is a different
  alignment of the same study — 1,897 sites, blocks ef1a 1–649 / COI 650–1415 / 16S 1416–1897, no
  intron — distributed via `roblanf/BenchmarkAlignments/datasets/Cognato_2001/alignment.nex`. Ours is
  the authors' own Dryad deposit.

### saxifragales — 40 taxa × 9,006 sites, 5 charsets
- **Study:** Fishbein M et al. (2001). Systematic Biology 50:817–847.
- **Deposit:** Dryad `doi:10.5061/dryad.684`.
- **Genes:** atpB, 18S, rbcL, matK, 26S. These five CHARSETs span 9,006 of the file's 9,237 columns,
  which is the subset PartitionFinder Table 1 reports; only those columns are kept.
- NEXUS uses `GAP=':'`, `MISSING='N'`.

### hummingbirds — 164 taxa × 3,821 sites, 11 charsets
- **Study:** McGuire et al. (2007).
- **Deposit:** TreeBASE matrix **M3354**, downloaded as `.nexorg` (the original submitted NEXUS, which
  retains the SETS block).
- NCHAR=4122; the author's EXSET removes 301 sites, giving the 3,821 columns PartitionFinder Table 1
  reports.
- **Genes:** ND2 and ND4 with codon positions, AK1, bfib, tRNA.

### midges — 74 taxa × 2,701 sites, **charsets not recovered**
- **Study:** Ekrem, Willassen & Stur (2010).
- **Deposit:** TreeBASE study **10378**, matrix 5116; original file name `Micropsectra_molecular.nex`.
- **Genes:** COI, COII, CAD, 16S *according to the publication* — we could not verify this against the
  file, because the TreeBASE **per-matrix** download strips the SETS block. The copy we hold contains
  only TAXA and CHARACTERS blocks: no CHARSET, no gene names.
- **To fix:** download the `.nexorg` for study 10378 and run `scripts/prep_nexorg.py`, as was done for
  hummingbirds. TreeBASE is unreachable from this cluster.

## Tier 2 — published taxon set and canonical gene set; alignment reconstructed by us

### mito — 33 taxa × 15,490 sites, 37 loci
- **Study:** Leavitt JR et al. (2013). Molecular Phylogenetics and Evolution 67:494–508, who analysed
  34 grasshopper mitogenomes.
- **What is theirs:** the GenBank accessions listed in their Table 1, and the per-gene alignment protocol.
- **What is ours:** the alignment itself. Their alignment was never deposited, so this is a
  reconstruction, not their file. The 37-gene metazoan mitochondrial set is fixed by biology, so the
  gene content is not a choice we made; the alignment procedure is.

### beetle — 52 taxa × 16,318 sites, 37 loci
- **Study:** Timmermans MJTN et al. (2016). Genome Biology and Evolution 8:161.
- **What is theirs:** the accessions in Table S1 (243 records).
- **What is ours:** record filtering (175 have ≥12 of 13 protein-coding genes; 52 of those also have
  both rRNA genes annotated) and the alignment. See `rerun_sim/results/beetle_pipeline.png`.
- **Masking:** five gene copies translate with internal stop codons under genetic code 5 and are
  masked to gaps — JX412852/cox1, JX412759/cox1, JX412798/cox1, JX412839/cox1, JX412729/nad5.
  Recorded in `beetle/aln/beetle.masked.tsv`; unmasked alignment kept as `beetle.unmasked.fasta`.

## Tier 3 — built entirely by us

### plastome — 33 taxa × 84,209 sites, 110 loci
- **No source publication.** Taxon set, gene set and alignment are all ours, assembled from annotated
  ENA plastid genome records.
- Four decisions are arbitrary and would need defending: the taxon selection, the `MIN_FRAC=0.8`
  gene-presence threshold, skipping the trans-spliced `rps12`, and keeping only the first copy of each
  inverted-repeat gene.
- Validation performed: 0 internal stop codons across 2,483 plastid CDS; six known angiosperm clades
  recovered (Poaceae, monocots, Fagales, Melastomataceae, Brassicaceae, Brassicales).
