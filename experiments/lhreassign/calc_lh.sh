#!/bin/bash
# Site log-likelihoods of every site under each surviving subset's model, computed with the exact
# invocation hPartition's Stage 4 uses (phyloanalysis.cpp:4429-4452, calcLH): fixed tree, fixed
# branch lengths, --sitelh, --fast.
unset LD_LIBRARY_PATH
set -e
ds=$1
R=/home/diepht/sliferskyd/hPartition/rerun_sim
L=$R/lhreassign
IQ=/home/diepht/sliferskyd/hPartition/iqtree2/build/iqtree2
ALN=/home/diepht/sliferskyd/hPartition-datasets/DNA/empirical/$ds.phy
TREE=$R/seedvar/out/$ds.s0/partition/aln.treefile
mkdir -p $L/lh/$ds
while IFS=$'\t' read -r name model; do
  $IQ -s $ALN -m "$model" -t $TREE -pre $L/lh/$ds/$name \
      -keep-ident --safe --sitelh -blfix --fast -T 1 -redo -seed 0 > $L/lh/$ds/$name.log 2>&1
  rm -f $L/lh/$ds/$name.{ckp.gz,iqtree,log,treefile,model.gz,bionj,mldist,best_model.nex}
done < $L/models/$ds.txt
echo "done $ds: $(ls $L/lh/$ds/*.sitelh | wc -l) sitelh files"
