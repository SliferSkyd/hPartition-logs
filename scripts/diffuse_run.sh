#!/bin/bash
# Rebuild the Stage-4 per-site log-likelihood matrix L[model][site] for one dataset by
# replaying exactly what calcLH() does: stock IQ-TREE, one candidate model at a time,
# on the fixed ModelFinder tree with -blfix --sitelh.
set -e
ds=$1
R=/home/diepht/sliferskyd/hPartition/rerun_sim
IQ=/home/diepht/sliferskyd/hPartition/iqtree-2.4.0-Linux-intel/bin/iqtree2
ALN=/home/diepht/sliferskyd/hPartition-datasets/DNA/empirical/$ds.phy
SRC=$R/seedvar/out/$ds.s0/hPartition
OUT=$R/diffuse/$ds
unset LD_LIBRARY_PATH
mkdir -p $OUT
# candidate models = Parameters column of the MF report (same regex as getCandidateModels)
awk '/SUBSTITUTION PROCESS/{f=1} f&&/TREE USED/{exit} f' $SRC/aln.MF.iqtree \
  | sed -nE 's/^[[:space:]]*[0-9]+[[:space:]]+[^[:space:]]+[[:space:]]+[0-9.]+[[:space:]]+(.+)$/\1/p' \
  | sed 's/+ASC//' > $OUT/models.txt
n=$(wc -l < $OUT/models.txt)
echo "$ds: $n candidate models"
i=0
while IFS= read -r m; do
  i=$((i+1))
  [ -s $OUT/m$i.sitelh ] && continue
  $IQ -seed 0 -s $ALN -m "$m" -t $SRC/aln.MF.treefile -pre $OUT/m$i \
      -keep-ident --safe --sitelh -blfix --fast -T 1 -redo > $OUT/m$i.log 2>&1
  # keep only the per-site row; drop the rest
  mv $OUT/m$i.sitelh $OUT/row$i.txt 2>/dev/null || true
  rm -f $OUT/m$i.ckp.gz $OUT/m$i.treefile $OUT/m$i.iqtree $OUT/m$i.log
done < $OUT/models.txt
echo "$ds: done, $(ls $OUT/row*.txt 2>/dev/null | wc -l) rows"
