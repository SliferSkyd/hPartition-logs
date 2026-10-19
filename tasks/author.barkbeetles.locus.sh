set -e
mkdir -p /home/diepht/sliferskyd/hPartition/rerun_sim/out_rna/author_locus/barkbeetles/partition
/home/diepht/sliferskyd/hPartition/rerun_sim/bin/eval_iqtree.sh /home/diepht/sliferskyd/hPartition/rna_datasets/pf/aln/barkbeetles.phy /home/diepht/sliferskyd/hPartition/rna_datasets/pf/aln/barkbeetles.author_locus.nex /home/diepht/sliferskyd/hPartition/rerun_sim/out_rna/author_locus/barkbeetles/partition 1
test -s /home/diepht/sliferskyd/hPartition/rerun_sim/out_rna/author_locus/barkbeetles/partition/aln.treefile
