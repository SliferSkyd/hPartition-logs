#!/bin/bash
unset LD_LIBRARY_PATH
set -e
mkdir -p /home/diepht/sliferskyd/hPartition/rerun_sim/pinvar/out/hpar.p00.0/hPartition /home/diepht/sliferskyd/hPartition/rerun_sim/pinvar/out/hpar.p00.0/partition
cd /home/diepht/sliferskyd/hPartition/rerun_sim/pinvar/out/hpar.p00.0/hPartition
/usr/bin/time -v -o /home/diepht/sliferskyd/hPartition/rerun_sim/pinvar/out/hpar.p00.0/hPartition/time.txt /home/diepht/sliferskyd/hPartition/iqtree2/build/iqtree2 -seed 0 -s /home/diepht/sliferskyd/hPartition/rerun_sim/pinvar/data/p00/0.phy -pre /home/diepht/sliferskyd/hPartition/rerun_sim/pinvar/out/hpar.p00.0/hPartition/aln -hPartition -redo -mset JC69,F81,HKY,GTR -T 1 > /home/diepht/sliferskyd/hPartition/rerun_sim/pinvar/out/hpar.p00.0/hPartition/cmd.log 2>&1
/home/diepht/sliferskyd/hPartition/rerun_sim/bin/eval_iqtree.sh /home/diepht/sliferskyd/hPartition/rerun_sim/pinvar/data/p00/0.phy /home/diepht/sliferskyd/hPartition/rerun_sim/pinvar/out/hpar.p00.0/hPartition/aln.partitions /home/diepht/sliferskyd/hPartition/rerun_sim/pinvar/out/hpar.p00.0/partition 1
test -s /home/diepht/sliferskyd/hPartition/rerun_sim/pinvar/out/hpar.p00.0/partition/aln.treefile
