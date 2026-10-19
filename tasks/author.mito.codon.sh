set -e
mkdir -p /home/diepht/sliferskyd/hPartition/rerun_sim/out_rna/author_codon/mito/partition
/home/diepht/sliferskyd/hPartition/rerun_sim/bin/eval_iqtree.sh /home/diepht/sliferskyd/hPartition/rna_datasets/mito/aln/mito.phy /home/diepht/sliferskyd/hPartition/rna_datasets/mito/aln/mito.author_codon.nex /home/diepht/sliferskyd/hPartition/rerun_sim/out_rna/author_codon/mito/partition 1
test -s /home/diepht/sliferskyd/hPartition/rerun_sim/out_rna/author_codon/mito/partition/aln.treefile
