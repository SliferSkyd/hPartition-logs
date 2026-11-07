#!/bin/bash
# BIC of the hPartition scheme after its entirely invariant subsets are dissolved and their sites
# re-placed by hPartition's own rule for a dissolved subset (probability proportional to
# exp(lnL - minLH)). Same evaluation command as every other scheme in the paper.
set -e
/home/diepht/sliferskyd/hPartition/rerun_sim/bin/eval_iqtree.sh \
  /home/diepht/sliferskyd/hPartition-datasets/DNA/empirical/Calisto.phy \
  /home/diepht/sliferskyd/hPartition/rerun_sim/lhreassign/schemes/Calisto.s3.lhre.nex \
  /home/diepht/sliferskyd/hPartition/rerun_sim/lhreassign/out/Calisto.s3 1
