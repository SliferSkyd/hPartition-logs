#!/bin/bash
# Submit the sweep, respecting the per-user queue limit.
S=/home/diepht/sliferskyd/hPartition/rerun_sim/divsweep
for t in $S/tasks/*.sh; do
  b=$(basename $t .sh)
  case $b in Morpho.d50|Morpho.d100) continue;; esac
  mkdir -p $S/out/$b
  until sbatch --job-name=dv$b --mem=10G --cpus-per-task=1 --time=06:00:00 \
        -o $S/out/$b/slurm.out $t > /dev/null 2>&1; do sleep 45; done
done
echo "all submitted"
