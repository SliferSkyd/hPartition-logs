#!/bin/bash
# BIC of the hPartition scheme after its entirely invariant subsets are dissolved and their sites
# re-placed by hPartition's own rule for a dissolved subset (probability proportional to
# exp(lnL - minLH)). Same evaluation command as every other scheme in the paper.
set -e
/home/diepht/sliferskyd/hPartition/rerun_sim/bin/eval_iqtree.sh \
  /home/diepht/sliferskyd/hPartition-datasets/DNA/empirical/Arctiina.phy \
  /home/diepht/sliferskyd/hPartition/rerun_sim/lhreassign/schemes/Arctiina.s4.lhre.nex \
  /home/diepht/sliferskyd/hPartition/rerun_sim/lhreassign/out/Arctiina.s4 1
