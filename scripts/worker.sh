#!/bin/bash
# Slurm worker: runs $SLURM_CPUS_PER_TASK single-core lanes; each lane claims tasks
# from tasks/<queue>.list atomically (mkdir) and runs them. Usage: sbatch ... worker.sh <queue> [<queue> ...]
ROOT=/home/diepht/sliferskyd/hPartition/rerun_sim
unset LD_LIBRARY_PATH
export OMP_NUM_THREADS=1
NL=$(( ${SLURM_CPUS_PER_TASK:-1} / ${LANE_CPUS:-1} ))
lane() {
  for q in "$@"; do
    while read -r t; do
      [ -z "$t" ] && continue
      [ -e "$ROOT/done/$t.ok" ] && continue
      mkdir "$ROOT/claims/$t" 2>/dev/null || continue
      echo "$SLURM_JOB_ID $(hostname) $(date +%s)" > "$ROOT/claims/$t/owner"
      start=$(date +%s)
      bash "$ROOT/tasks/$t.sh" > "$ROOT/logs/$t.log" 2>&1
      rc=$?
      echo "rc=$rc wall=$(( $(date +%s)-start )) job=$SLURM_JOB_ID host=$(hostname)" > "$ROOT/done/$t.$( [ $rc = 0 ] && echo ok || echo fail )"
      [ $rc = 0 ] && rm -rf "$ROOT/claims/$t"
    done < "$ROOT/tasks/$q.list"
  done
}
for i in $(seq 1 $NL); do lane "$@" & done
wait
