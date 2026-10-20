set -e
mkdir -p /home/diepht/sliferskyd/hPartition/rerun_sim/out_novar/Calisto/hPartition /home/diepht/sliferskyd/hPartition/rerun_sim/out_novar/Calisto/partition
cd /home/diepht/sliferskyd/hPartition/rerun_sim/out_novar/Calisto/hPartition
/usr/bin/time -v -o /home/diepht/sliferskyd/hPartition/rerun_sim/out_novar/Calisto/hPartition/time.txt /home/diepht/sliferskyd/hPartition/iqtree2-novar-bin \
  -seed 0 -s /home/diepht/sliferskyd/hPartition-datasets/DNA/empirical/Calisto.phy -pre /home/diepht/sliferskyd/hPartition/rerun_sim/out_novar/Calisto/hPartition/aln \
  -hPartition -redo -mset JC69,F81,HKY,GTR -T 1 > /home/diepht/sliferskyd/hPartition/rerun_sim/out_novar/Calisto/hPartition/cmd.log 2>&1
/home/diepht/sliferskyd/hPartition/rerun_sim/bin/eval_iqtree.sh /home/diepht/sliferskyd/hPartition-datasets/DNA/empirical/Calisto.phy /home/diepht/sliferskyd/hPartition/rerun_sim/out_novar/Calisto/hPartition/aln.partitions /home/diepht/sliferskyd/hPartition/rerun_sim/out_novar/Calisto/partition 1
test -s /home/diepht/sliferskyd/hPartition/rerun_sim/out_novar/Calisto/partition/aln.treefile
