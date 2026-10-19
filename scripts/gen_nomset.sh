#!/bin/bash
# hPartition WITHOUT -mset: lets hPartition's internal candidate-model search use ModelFinder's full default
# DNA model set instead of JC69,F81,HKY,GTR. Evaluation step is unchanged (it never used -mset), so BIC stays
# comparable with the main runs. Output goes to out_rna/hPartition-noMset/ so nothing is overwritten.
ROOT=/home/diepht/sliferskyd/hPartition/rerun_sim
HPAR=/home/diepht/sliferskyd/hPartition/iqtree2/build/iqtree2
: > $ROOT/tasks/nomset.list
for v in "$@"; do
  for d in $ROOT/../rna_datasets/pf/aln $ROOT/../rna_datasets/aln $ROOT/../rna_datasets/flu/aln $ROOT/../rna_datasets/full/aln; do
    [ -e $d/$v.phy ] && ALN=$d && break
  done
  t=nomset.rna.$v.0; o1=$ROOT/out_rna/hPartition-noMset/$v/hPartition; o2=$ROOT/out_rna/hPartition-noMset/$v/partition
  cat > $ROOT/tasks/$t.sh.tmp <<EOT
set -e
mkdir -p $o1 $o2
cd $o1
/usr/bin/time -v -o $o1/time.txt $HPAR -seed 0 -s $ALN/$v.phy -pre $o1/aln -hPartition -redo -T 1 > $o1/cmd.log 2>&1
$ROOT/bin/eval_iqtree.sh $ALN/$v.phy $o1/aln.partitions $o2 1
test -s $o2/aln.treefile
EOT
  mv $ROOT/tasks/$t.sh.tmp $ROOT/tasks/$t.sh; echo $t >> $ROOT/tasks/nomset.list
done
wc -l < $ROOT/tasks/nomset.list
