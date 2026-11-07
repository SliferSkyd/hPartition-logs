#!/bin/bash
unset LD_LIBRARY_PATH
set -e
rm -rf /home/diepht/sliferskyd/hPartition/rerun_sim/pinvar/out/gpar.p45.2; mkdir -p /home/diepht/sliferskyd/hPartition/rerun_sim/pinvar/out/gpar.p45.2/gPartition /home/diepht/sliferskyd/hPartition/rerun_sim/pinvar/out/gpar.p45.2/partition
cd /home/diepht/sliferskyd/hPartition/gPartition
/usr/bin/time -v -o /home/diepht/sliferskyd/hPartition/rerun_sim/pinvar/out/gpar.p45.2/gPartition/time.txt /home/diepht/anaconda3/bin/python gPartition.py -f /home/diepht/sliferskyd/hPartition/rerun_sim/pinvar/data/p45/2.phy -o /home/diepht/sliferskyd/hPartition/rerun_sim/pinvar/out/gpar.p45.2/gPartition/ > /home/diepht/sliferskyd/hPartition/rerun_sim/pinvar/out/gpar.p45.2/gPartition/cmd.log 2>&1
/home/diepht/sliferskyd/hPartition/rerun_sim/bin/eval_iqtree.sh /home/diepht/sliferskyd/hPartition/rerun_sim/pinvar/data/p45/2.phy /home/diepht/sliferskyd/hPartition/rerun_sim/pinvar/out/gpar.p45.2/gPartition/2.phy.FINAL.nex /home/diepht/sliferskyd/hPartition/rerun_sim/pinvar/out/gpar.p45.2/partition 1
test -s /home/diepht/sliferskyd/hPartition/rerun_sim/pinvar/out/gpar.p45.2/partition/aln.treefile
