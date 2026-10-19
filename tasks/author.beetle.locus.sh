set -e
mkdir -p /home/diepht/sliferskyd/hPartition/rerun_sim/out_rna/author_locus/beetle/partition
/home/diepht/sliferskyd/hPartition/rerun_sim/bin/eval_iqtree.sh /home/diepht/sliferskyd/hPartition/rna_datasets/beetle/aln/beetle.phy /home/diepht/sliferskyd/hPartition/rna_datasets/beetle/aln/beetle.author_locus.nex /home/diepht/sliferskyd/hPartition/rerun_sim/out_rna/author_locus/beetle/partition 1
test -s /home/diepht/sliferskyd/hPartition/rerun_sim/out_rna/author_locus/beetle/partition/aln.treefile
