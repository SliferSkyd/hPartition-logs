#!/bin/bash
# BIC of the hPartition scheme after the sites of every zero-variance subset are scattered
# uniformly at random over the remaining subsets. This is a randomisation control, not gPartition's
# Same evaluation command as every other scheme in the paper.
set -e
/home/diepht/sliferskyd/hPartition/rerun_sim/bin/eval_iqtree.sh \
  /home/diepht/sliferskyd/hPartition-datasets/DNA/empirical/Choreutidae.phy \
  /home/diepht/sliferskyd/hPartition/rerun_sim/scatter/schemes/Choreutidae.s0.scatter.nex \
  /home/diepht/sliferskyd/hPartition/rerun_sim/scatter/out/Choreutidae.s0 1
