#!/bin/bash
unset LD_LIBRARY_PATH
set -e
rm -rf /home/diepht/sliferskyd/hPartition/rerun_sim/pinvar/out/gpar.p60.7; mkdir -p /home/diepht/sliferskyd/hPartition/rerun_sim/pinvar/out/gpar.p60.7/gPartition /home/diepht/sliferskyd/hPartition/rerun_sim/pinvar/out/gpar.p60.7/partition
cd /home/diepht/sliferskyd/hPartition/gPartition
/usr/bin/time -v -o /home/diepht/sliferskyd/hPartition/rerun_sim/pinvar/out/gpar.p60.7/gPartition/time.txt /home/diepht/anaconda3/bin/python gPartition.py -f /home/diepht/sliferskyd/hPartition/rerun_sim/pinvar/data/p60/7.phy -o /home/diepht/sliferskyd/hPartition/rerun_sim/pinvar/out/gpar.p60.7/gPartition/ > /home/diepht/sliferskyd/hPartition/rerun_sim/pinvar/out/gpar.p60.7/gPartition/cmd.log 2>&1
/home/diepht/sliferskyd/hPartition/rerun_sim/bin/eval_iqtree.sh /home/diepht/sliferskyd/hPartition/rerun_sim/pinvar/data/p60/7.phy /home/diepht/sliferskyd/hPartition/rerun_sim/pinvar/out/gpar.p60.7/gPartition/7.phy.FINAL.nex /home/diepht/sliferskyd/hPartition/rerun_sim/pinvar/out/gpar.p60.7/partition 1
test -s /home/diepht/sliferskyd/hPartition/rerun_sim/pinvar/out/gpar.p60.7/partition/aln.treefile
