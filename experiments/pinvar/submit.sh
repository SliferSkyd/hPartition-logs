#!/bin/bash
# Submit the pinvar sweep. Keeps at most MINE jobs of our own in the queue, so the user's
# other work still fits under the per-user QOS limit.
P=/home/diepht/sliferskyd/hPartition/rerun_sim/pinvar
MINE=20
mine() { squeue -u $USER -h -o "%j" | grep -c '^pv' ; }
sub() {
  for t in "$@"; do
    b=$(basename $t .sh); mkdir -p $P/out/$b
    while [ "$(mine)" -ge $MINE ]; do sleep 60; done
    until sbatch --job-name=pv$b --mem=10G --cpus-per-task=1 --time=12:00:00 \
          -o $P/out/$b/slurm.out $t > /dev/null 2>&1; do sleep 60; done
  done
}
sub $P/tasks/hpar.*.sh $P/tasks/gpar.*.sh     # minutes each
echo "short jobs submitted"
sub $P/tasks/psi.*.sh                          # 2-3 h each, the long pole
echo "all submitted"
