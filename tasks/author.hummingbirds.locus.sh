set -e
mkdir -p /home/diepht/sliferskyd/hPartition/rerun_sim/out_rna/author_locus/hummingbirds/partition
/home/diepht/sliferskyd/hPartition/rerun_sim/bin/eval_iqtree.sh /home/diepht/sliferskyd/hPartition/rna_datasets/pf/aln/hummingbirds.phy /home/diepht/sliferskyd/hPartition/rna_datasets/pf/aln/hummingbirds.author_locus.nex /home/diepht/sliferskyd/hPartition/rerun_sim/out_rna/author_locus/hummingbirds/partition 1
test -s /home/diepht/sliferskyd/hPartition/rerun_sim/out_rna/author_locus/hummingbirds/partition/aln.treefile
