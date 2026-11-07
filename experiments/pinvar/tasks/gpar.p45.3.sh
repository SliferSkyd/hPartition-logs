#!/bin/bash
unset LD_LIBRARY_PATH
set -e
rm -rf /home/diepht/sliferskyd/hPartition/rerun_sim/pinvar/out/gpar.p45.3; mkdir -p /home/diepht/sliferskyd/hPartition/rerun_sim/pinvar/out/gpar.p45.3/gPartition /home/diepht/sliferskyd/hPartition/rerun_sim/pinvar/out/gpar.p45.3/partition
cd /home/diepht/sliferskyd/hPartition/gPartition
/usr/bin/time -v -o /home/diepht/sliferskyd/hPartition/rerun_sim/pinvar/out/gpar.p45.3/gPartition/time.txt /home/diepht/anaconda3/bin/python gPartition.py -f /home/diepht/sliferskyd/hPartition/rerun_sim/pinvar/data/p45/3.phy -o /home/diepht/sliferskyd/hPartition/rerun_sim/pinvar/out/gpar.p45.3/gPartition/ > /home/diepht/sliferskyd/hPartition/rerun_sim/pinvar/out/gpar.p45.3/gPartition/cmd.log 2>&1
/home/diepht/sliferskyd/hPartition/rerun_sim/bin/eval_iqtree.sh /home/diepht/sliferskyd/hPartition/rerun_sim/pinvar/data/p45/3.phy /home/diepht/sliferskyd/hPartition/rerun_sim/pinvar/out/gpar.p45.3/gPartition/3.phy.FINAL.nex /home/diepht/sliferskyd/hPartition/rerun_sim/pinvar/out/gpar.p45.3/partition 1
test -s /home/diepht/sliferskyd/hPartition/rerun_sim/pinvar/out/gpar.p45.3/partition/aln.treefile
