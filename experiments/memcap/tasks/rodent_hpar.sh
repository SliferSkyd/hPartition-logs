#!/bin/bash
# Does hPartition on Rodent survive the 10 GB allocation the paper describes?
unset LD_LIBRARY_PATH
set -e
R=/home/diepht/sliferskyd/hPartition
O=$R/rerun_sim/memcap/out/Rodent_hPar
/usr/bin/time -v -o $O/time.txt $R/iqtree2/build/iqtree2 \
  -seed 0 -s /home/diepht/sliferskyd/hPartition-datasets/DNA/empirical/Rodent.phy \
  -pre $O/aln -hPartition -redo -mset JC69,F81,HKY,GTR -T 1 > $O/cmd.log 2>&1
