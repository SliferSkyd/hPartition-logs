#!/bin/bash
# Archive the three experiments added during the revision: variant-only seeding (novar),
# seed-variance (seedvar) and the Stage-4 likelihood-matrix replay (diffuse).
# Copies only the files needed to reproduce the reported numbers, not whole run trees.
set -e
SRC=/home/diepht/sliferskyd/hPartition/rerun_sim
DST=/home/diepht/sliferskyd/hPartition/hPartition-sim-rerun/experiments

# novar / seedvar: scheme, ModelFinder report (candidate-model count), evaluated BIC, timings
for exp in novar seedvar; do
  case $exp in
    novar)   root=$SRC/out_novar ;;
    seedvar) root=$SRC/seedvar/out ;;
  esac
  [ -d "$root" ] || continue
  for r in "$root"/*/; do
    n=$(basename "$r"); d=$DST/$exp/$n
    [ -s "$r/partition/aln.iqtree" ] || continue
    mkdir -p "$d/hPartition" "$d/partition"
    for f in hPartition/aln.partitions hPartition/aln.MF.iqtree hPartition/time.txt \
             partition/aln.iqtree partition/time.txt; do
      [ -e "$r/$f" ] && cp -p "$r/$f" "$d/$f"
    done
  done
done

# diffuse: the replayed per-site log-likelihood rows and the model list they came from
if [ -d "$SRC/diffuse" ]; then
  for r in "$SRC"/diffuse/*/; do
    n=$(basename "$r"); mkdir -p "$DST/diffuse/$n"
    cp -p "$r/models.txt" "$DST/diffuse/$n/" 2>/dev/null || true
    tar -C "$r" -czf "$DST/diffuse/$n/rows.tar.gz" $(cd "$r" && ls row*.txt 2>/dev/null) 2>/dev/null || true
  done
fi
echo "experiments archived to $DST"
du -sh "$DST" 2>/dev/null
