#!/bin/bash
# Does gPartition on Neoaves survive the 10 GB allocation the paper describes?
set -e
R=/home/diepht/sliferskyd/hPartition
O=$R/rerun_sim/memcap/out/Neoaves_gPar
cd $R/gPartition
/usr/bin/time -v -o $O/time.txt /home/diepht/anaconda3/bin/python gPartition.py \
  -f /home/diepht/sliferskyd/hPartition-datasets/DNA/empirical/Neoaves.phy \
  -o $O/ > $O/cmd.log 2>&1
