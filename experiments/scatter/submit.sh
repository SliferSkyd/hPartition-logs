#!/bin/bash
# Submit the scatter control, respecting the per-user queue limit.
S=/home/diepht/sliferskyd/hPartition/rerun_sim/scatter
for t in $S/tasks/*.sh; do
  b=$(basename $t .sh)
  mkdir -p $S/out/$b
  until sbatch --job-name=sc$b --mem=10G --cpus-per-task=1 --time=06:00:00 \
        -o $S/out/$b/slurm.out $t > /dev/null 2>&1; do sleep 45; done
done
echo "all submitted"
