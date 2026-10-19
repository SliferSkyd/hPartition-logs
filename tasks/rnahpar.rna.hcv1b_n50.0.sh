set -e
mkdir -p /home/diepht/sliferskyd/hPartition/rerun_sim/out_rna/hPartition/hcv1b_n50/hPartition /home/diepht/sliferskyd/hPartition/rerun_sim/out_rna/hPartition/hcv1b_n50/partition
cd /home/diepht/sliferskyd/hPartition/rerun_sim/out_rna/hPartition/hcv1b_n50/hPartition
/usr/bin/time -v -o /home/diepht/sliferskyd/hPartition/rerun_sim/out_rna/hPartition/hcv1b_n50/hPartition/time.txt /home/diepht/sliferskyd/hPartition/iqtree2/build/iqtree2 -seed 0 -s /home/diepht/sliferskyd/hPartition/rna_datasets/aln/hcv1b_n50.phy -pre /home/diepht/sliferskyd/hPartition/rerun_sim/out_rna/hPartition/hcv1b_n50/hPartition/aln -hPartition -redo -mset JC69,F81,HKY,GTR -T 1 > /home/diepht/sliferskyd/hPartition/rerun_sim/out_rna/hPartition/hcv1b_n50/hPartition/cmd.log 2>&1
/home/diepht/sliferskyd/hPartition/rerun_sim/bin/eval_iqtree.sh /home/diepht/sliferskyd/hPartition/rna_datasets/aln/hcv1b_n50.phy /home/diepht/sliferskyd/hPartition/rerun_sim/out_rna/hPartition/hcv1b_n50/hPartition/aln.partitions /home/diepht/sliferskyd/hPartition/rerun_sim/out_rna/hPartition/hcv1b_n50/partition
test -s /home/diepht/sliferskyd/hPartition/rerun_sim/out_rna/hPartition/hcv1b_n50/partition/aln.treefile
