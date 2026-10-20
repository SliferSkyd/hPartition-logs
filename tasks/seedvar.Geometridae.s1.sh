set -e
mkdir -p /home/diepht/sliferskyd/hPartition/rerun_sim/seedvar/out/Geometridae.s1/hPartition /home/diepht/sliferskyd/hPartition/rerun_sim/seedvar/out/Geometridae.s1/partition
cd /home/diepht/sliferskyd/hPartition/rerun_sim/seedvar/out/Geometridae.s1/hPartition
/usr/bin/time -v -o /home/diepht/sliferskyd/hPartition/rerun_sim/seedvar/out/Geometridae.s1/hPartition/time.txt /home/diepht/sliferskyd/hPartition/iqtree2/build/iqtree2 \
  -seed 1 -s /home/diepht/sliferskyd/hPartition-datasets/DNA/empirical/Geometridae.phy -pre /home/diepht/sliferskyd/hPartition/rerun_sim/seedvar/out/Geometridae.s1/hPartition/aln \
  -hPartition -redo -mset JC69,F81,HKY,GTR -T 1 > /home/diepht/sliferskyd/hPartition/rerun_sim/seedvar/out/Geometridae.s1/hPartition/cmd.log 2>&1
/home/diepht/sliferskyd/hPartition/rerun_sim/bin/eval_iqtree.sh /home/diepht/sliferskyd/hPartition-datasets/DNA/empirical/Geometridae.phy /home/diepht/sliferskyd/hPartition/rerun_sim/seedvar/out/Geometridae.s1/hPartition/aln.partitions /home/diepht/sliferskyd/hPartition/rerun_sim/seedvar/out/Geometridae.s1/partition 1
test -s /home/diepht/sliferskyd/hPartition/rerun_sim/seedvar/out/Geometridae.s1/partition/aln.treefile
