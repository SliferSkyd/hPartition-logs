#!/bin/bash
# BIC of the hPartition scheme after every zero-variance subset is folded into its
# nearest neighbour. Same evaluation command as every other scheme in the paper.
set -e
/home/diepht/sliferskyd/hPartition/rerun_sim/bin/eval_iqtree.sh \
  /home/diepht/sliferskyd/hPartition-datasets/DNA/empirical/Arctiina.phy \
  /home/diepht/sliferskyd/hPartition/rerun_sim/zerovar/schemes/Arctiina.merged.nex \
  /home/diepht/sliferskyd/hPartition/rerun_sim/zerovar/out/Arctiina 1
