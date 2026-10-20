set -e
mkdir -p /home/diepht/sliferskyd/hPartition/rerun_sim/seedvar/out/Coenonymphina.s0/hPartition /home/diepht/sliferskyd/hPartition/rerun_sim/seedvar/out/Coenonymphina.s0/partition
cd /home/diepht/sliferskyd/hPartition/rerun_sim/seedvar/out/Coenonymphina.s0/hPartition
/usr/bin/time -v -o /home/diepht/sliferskyd/hPartition/rerun_sim/seedvar/out/Coenonymphina.s0/hPartition/time.txt /home/diepht/sliferskyd/hPartition/iqtree2/build/iqtree2 \
  -seed 0 -s /home/diepht/sliferskyd/hPartition-datasets/DNA/empirical/Coenonymphina.phy -pre /home/diepht/sliferskyd/hPartition/rerun_sim/seedvar/out/Coenonymphina.s0/hPartition/aln \
  -hPartition -redo -mset JC69,F81,HKY,GTR -T 1 > /home/diepht/sliferskyd/hPartition/rerun_sim/seedvar/out/Coenonymphina.s0/hPartition/cmd.log 2>&1
/home/diepht/sliferskyd/hPartition/rerun_sim/bin/eval_iqtree.sh /home/diepht/sliferskyd/hPartition-datasets/DNA/empirical/Coenonymphina.phy /home/diepht/sliferskyd/hPartition/rerun_sim/seedvar/out/Coenonymphina.s0/hPartition/aln.partitions /home/diepht/sliferskyd/hPartition/rerun_sim/seedvar/out/Coenonymphina.s0/partition 1
test -s /home/diepht/sliferskyd/hPartition/rerun_sim/seedvar/out/Coenonymphina.s0/partition/aln.treefile
