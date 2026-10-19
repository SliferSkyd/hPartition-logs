set -e
mkdir -p /home/diepht/sliferskyd/hPartition/rerun_sim/out_rna/author_locus/plastome/partition
/home/diepht/sliferskyd/hPartition/rerun_sim/bin/eval_iqtree.sh /home/diepht/sliferskyd/hPartition/rna_datasets/plastome/aln/plastome.phy /home/diepht/sliferskyd/hPartition/rna_datasets/plastome/aln/plastome.author_locus.nex /home/diepht/sliferskyd/hPartition/rerun_sim/out_rna/author_locus/plastome/partition 1
test -s /home/diepht/sliferskyd/hPartition/rerun_sim/out_rna/author_locus/plastome/partition/aln.treefile
