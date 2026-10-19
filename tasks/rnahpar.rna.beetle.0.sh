set -e
mkdir -p /home/diepht/sliferskyd/hPartition/rerun_sim/out_rna/hPartition/beetle/hPartition /home/diepht/sliferskyd/hPartition/rerun_sim/out_rna/hPartition/beetle/partition
cd /home/diepht/sliferskyd/hPartition/rerun_sim/out_rna/hPartition/beetle/hPartition
/usr/bin/time -v -o /home/diepht/sliferskyd/hPartition/rerun_sim/out_rna/hPartition/beetle/hPartition/time.txt /home/diepht/sliferskyd/hPartition/iqtree2/build/iqtree2 -seed 0 -s /home/diepht/sliferskyd/hPartition/rna_datasets/beetle/aln/beetle.phy -pre /home/diepht/sliferskyd/hPartition/rerun_sim/out_rna/hPartition/beetle/hPartition/aln -hPartition -redo -mset JC69,F81,HKY,GTR -T 1 > /home/diepht/sliferskyd/hPartition/rerun_sim/out_rna/hPartition/beetle/hPartition/cmd.log 2>&1
/home/diepht/sliferskyd/hPartition/rerun_sim/bin/eval_iqtree.sh /home/diepht/sliferskyd/hPartition/rna_datasets/beetle/aln/beetle.phy /home/diepht/sliferskyd/hPartition/rerun_sim/out_rna/hPartition/beetle/hPartition/aln.partitions /home/diepht/sliferskyd/hPartition/rerun_sim/out_rna/hPartition/beetle/partition 1
test -s /home/diepht/sliferskyd/hPartition/rerun_sim/out_rna/hPartition/beetle/partition/aln.treefile
