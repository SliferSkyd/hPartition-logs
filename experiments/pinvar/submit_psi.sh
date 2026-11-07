#!/bin/bash
# PsiPartition only. Its driver hardcodes -nt 4 and IQ-TREE refuses to start when it sees fewer
# cores than threads, so these need four CPUs; hPartition and gPartition ran on one, as the
# benchmark specifies (see rerun_sim/bin/run_mito_pipeline.sh).
P=/home/diepht/sliferskyd/hPartition/rerun_sim/pinvar
MINE=20
mine() { squeue -u $USER -h -o "%j" | grep -c '^pv' ; }
for t in $P/tasks/psi.*.sh; do
  b=$(basename $t .sh); mkdir -p $P/out/$b
  while [ "$(mine)" -ge $MINE ]; do sleep 60; done
  until sbatch --job-name=pv$b --mem=10G --cpus-per-task=4 --time=12:00:00 \
        -o $P/out/$b/slurm.out $t > /dev/null 2>&1; do sleep 60; done
done
echo "psi submitted"
