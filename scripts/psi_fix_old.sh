#!/bin/bash
# Psi runs started before the tree-naming fix end with a .fail marker because remove_caches() deleted
# <rep>.last.treefile. If the run is otherwise complete (30 iterations + final rerun, python exit 0),
# rebuild last.nwk / final.nwk from the surviving .iqtree reports and mark the task ok.
ROOT=/home/diepht/sliferskyd/hPartition/rerun_sim
PY=/home/diepht/miniconda3/envs/PsiPartition/bin/python
for f in $ROOT/done/psi.*.fail; do
  [ -e "$f" ] || continue
  t=$(basename $f .fail); IFS=. read -r _ s cat rep <<<"$t"; o=$ROOT/out/PsiPartition/$s/$cat/$rep
  n=$(( $(wc -l < $o/$rep.iters.tsv) - 1 ))
  if [ "$n" -ge 30 ] && [ -s $o/$rep.last.iqtree ] && [ -s $o/$rep.final.iqtree ] && grep -q "Exit status: 0" $o/time.txt; then
    $PY -c "import sys; sys.path.insert(0,'$ROOT/bin'); from psi_local import write_nwk; write_nwk('$o/$rep.last.iqtree','$o/last.nwk'); write_nwk('$o/$rep.final.iqtree','$o/final.nwk')" 2>/dev/null \
      && { echo "$(cat $f) fixed_from_iqtree=1" > $ROOT/done/$t.ok; rm -f $f; rm -rf $ROOT/claims/$t; echo "fixed $t"; }
  else
    echo "REAL FAIL $t (iters=$n)"
  fi
done
