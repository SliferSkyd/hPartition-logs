set -e
mkdir -p /home/diepht/sliferskyd/hPartition/rerun_sim/out_novar/Geometridae/hPartition /home/diepht/sliferskyd/hPartition/rerun_sim/out_novar/Geometridae/partition
cd /home/diepht/sliferskyd/hPartition/rerun_sim/out_novar/Geometridae/hPartition
/usr/bin/time -v -o /home/diepht/sliferskyd/hPartition/rerun_sim/out_novar/Geometridae/hPartition/time.txt /home/diepht/sliferskyd/hPartition/iqtree2-novar-bin \
  -seed 0 -s /home/diepht/sliferskyd/hPartition-datasets/DNA/empirical/Geometridae.phy -pre /home/diepht/sliferskyd/hPartition/rerun_sim/out_novar/Geometridae/hPartition/aln \
  -hPartition -redo -mset JC69,F81,HKY,GTR -T 1 > /home/diepht/sliferskyd/hPartition/rerun_sim/out_novar/Geometridae/hPartition/cmd.log 2>&1
/home/diepht/sliferskyd/hPartition/rerun_sim/bin/eval_iqtree.sh /home/diepht/sliferskyd/hPartition-datasets/DNA/empirical/Geometridae.phy /home/diepht/sliferskyd/hPartition/rerun_sim/out_novar/Geometridae/hPartition/aln.partitions /home/diepht/sliferskyd/hPartition/rerun_sim/out_novar/Geometridae/partition 1
test -s /home/diepht/sliferskyd/hPartition/rerun_sim/out_novar/Geometridae/partition/aln.treefile
