set -e
mkdir -p /home/diepht/sliferskyd/hPartition/rerun_sim/out_novar/Coenonymphina/hPartition /home/diepht/sliferskyd/hPartition/rerun_sim/out_novar/Coenonymphina/partition
cd /home/diepht/sliferskyd/hPartition/rerun_sim/out_novar/Coenonymphina/hPartition
/usr/bin/time -v -o /home/diepht/sliferskyd/hPartition/rerun_sim/out_novar/Coenonymphina/hPartition/time.txt /home/diepht/sliferskyd/hPartition/iqtree2-novar-bin \
  -seed 0 -s /home/diepht/sliferskyd/hPartition-datasets/DNA/empirical/Coenonymphina.phy -pre /home/diepht/sliferskyd/hPartition/rerun_sim/out_novar/Coenonymphina/hPartition/aln \
  -hPartition -redo -mset JC69,F81,HKY,GTR -T 1 > /home/diepht/sliferskyd/hPartition/rerun_sim/out_novar/Coenonymphina/hPartition/cmd.log 2>&1
/home/diepht/sliferskyd/hPartition/rerun_sim/bin/eval_iqtree.sh /home/diepht/sliferskyd/hPartition-datasets/DNA/empirical/Coenonymphina.phy /home/diepht/sliferskyd/hPartition/rerun_sim/out_novar/Coenonymphina/hPartition/aln.partitions /home/diepht/sliferskyd/hPartition/rerun_sim/out_novar/Coenonymphina/partition 1
test -s /home/diepht/sliferskyd/hPartition/rerun_sim/out_novar/Coenonymphina/partition/aln.treefile
