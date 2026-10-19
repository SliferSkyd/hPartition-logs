set -e
mkdir -p /home/diepht/sliferskyd/hPartition/rerun_sim/out_rna/author_codon/barkbeetles/partition
/home/diepht/sliferskyd/hPartition/rerun_sim/bin/eval_iqtree.sh /home/diepht/sliferskyd/hPartition/rna_datasets/pf/aln/barkbeetles.phy /home/diepht/sliferskyd/hPartition/rna_datasets/pf/aln/barkbeetles.author_codon.nex /home/diepht/sliferskyd/hPartition/rerun_sim/out_rna/author_codon/barkbeetles/partition 1
test -s /home/diepht/sliferskyd/hPartition/rerun_sim/out_rna/author_codon/barkbeetles/partition/aln.treefile
