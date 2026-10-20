set -e
mkdir -p /home/diepht/sliferskyd/hPartition/rerun_sim/out_novar/Choreutidae/hPartition /home/diepht/sliferskyd/hPartition/rerun_sim/out_novar/Choreutidae/partition
cd /home/diepht/sliferskyd/hPartition/rerun_sim/out_novar/Choreutidae/hPartition
/usr/bin/time -v -o /home/diepht/sliferskyd/hPartition/rerun_sim/out_novar/Choreutidae/hPartition/time.txt /home/diepht/sliferskyd/hPartition/iqtree2-novar-bin \
  -seed 0 -s /home/diepht/sliferskyd/hPartition-datasets/DNA/empirical/Choreutidae.phy -pre /home/diepht/sliferskyd/hPartition/rerun_sim/out_novar/Choreutidae/hPartition/aln \
  -hPartition -redo -mset JC69,F81,HKY,GTR -T 1 > /home/diepht/sliferskyd/hPartition/rerun_sim/out_novar/Choreutidae/hPartition/cmd.log 2>&1
/home/diepht/sliferskyd/hPartition/rerun_sim/bin/eval_iqtree.sh /home/diepht/sliferskyd/hPartition-datasets/DNA/empirical/Choreutidae.phy /home/diepht/sliferskyd/hPartition/rerun_sim/out_novar/Choreutidae/hPartition/aln.partitions /home/diepht/sliferskyd/hPartition/rerun_sim/out_novar/Choreutidae/partition 1
test -s /home/diepht/sliferskyd/hPartition/rerun_sim/out_novar/Choreutidae/partition/aln.treefile
