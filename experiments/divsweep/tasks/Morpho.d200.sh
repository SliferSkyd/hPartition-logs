#!/bin/bash
unset LD_LIBRARY_PATH
set -e
mkdir -p /home/diepht/sliferskyd/hPartition/rerun_sim/divsweep/out/Morpho.d200/hPartition /home/diepht/sliferskyd/hPartition/rerun_sim/divsweep/out/Morpho.d200/partition
export HPARTITION_BIN_DIVISOR=200
/usr/bin/time -v -o /home/diepht/sliferskyd/hPartition/rerun_sim/divsweep/out/Morpho.d200/hPartition/time.txt /home/diepht/sliferskyd/hPartition/iqtree2/build/iqtree2 -seed 0 -s /home/diepht/sliferskyd/hPartition-datasets/DNA/empirical/Morpho.phy \
  -pre /home/diepht/sliferskyd/hPartition/rerun_sim/divsweep/out/Morpho.d200/hPartition/aln -hPartition -redo -mset JC69,F81,HKY,GTR -T 1 \
  > /home/diepht/sliferskyd/hPartition/rerun_sim/divsweep/out/Morpho.d200/hPartition/cmd.log 2>&1
unset HPARTITION_BIN_DIVISOR
/home/diepht/sliferskyd/hPartition/rerun_sim/bin/eval_iqtree.sh /home/diepht/sliferskyd/hPartition-datasets/DNA/empirical/Morpho.phy /home/diepht/sliferskyd/hPartition/rerun_sim/divsweep/out/Morpho.d200/hPartition/aln.partitions /home/diepht/sliferskyd/hPartition/rerun_sim/divsweep/out/Morpho.d200/partition 1
