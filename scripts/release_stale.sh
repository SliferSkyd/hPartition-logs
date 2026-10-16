#!/bin/bash
# Release claims whose owning Slurm job is no longer running (cancelled/timed out), and failed tasks if --fails.
ROOT=/home/diepht/sliferskyd/hPartition/rerun_sim
live=$(squeue -u $USER -h -t R -o %i)
n=0
for c in $ROOT/claims/*; do
  [ -d "$c" ] || continue
  j=$(awk '{print $1}' "$c/owner" 2>/dev/null)
  [[ "$j" =~ ^[0-9]+$ ]] || continue  # skip manual RETRY claims
  if ! grep -qx "$j" <<<"$live"; then rm -rf "$c"; rm -f $ROOT/done/$(basename $c).fail; n=$((n+1)); fi
done
echo "released $n stale claims"
