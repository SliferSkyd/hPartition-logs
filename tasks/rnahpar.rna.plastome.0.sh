set -e
mkdir -p /home/diepht/sliferskyd/hPartition/rerun_sim/out_rna/hPartition/plastome/hPartition /home/diepht/sliferskyd/hPartition/rerun_sim/out_rna/hPartition/plastome/partition
cd /home/diepht/sliferskyd/hPartition/rerun_sim/out_rna/hPartition/plastome/hPartition
/usr/bin/time -v -o /home/diepht/sliferskyd/hPartition/rerun_sim/out_rna/hPartition/plastome/hPartition/time.txt /home/diepht/sliferskyd/hPartition/iqtree2/build/iqtree2 -seed 0 -s /home/diepht/sliferskyd/hPartition/rna_datasets/plastome/aln/plastome.phy -pre /home/diepht/sliferskyd/hPartition/rerun_sim/out_rna/hPartition/plastome/hPartition/aln -hPartition -redo -mset JC69,F81,HKY,GTR -T 8 > /home/diepht/sliferskyd/hPartition/rerun_sim/out_rna/hPartition/plastome/hPartition/cmd.log 2>&1
/home/diepht/sliferskyd/hPartition/rerun_sim/bin/eval_iqtree.sh /home/diepht/sliferskyd/hPartition/rna_datasets/plastome/aln/plastome.phy /home/diepht/sliferskyd/hPartition/rerun_sim/out_rna/hPartition/plastome/hPartition/aln.partitions /home/diepht/sliferskyd/hPartition/rerun_sim/out_rna/hPartition/plastome/partition 8
test -s /home/diepht/sliferskyd/hPartition/rerun_sim/out_rna/hPartition/plastome/partition/aln.treefile
