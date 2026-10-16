#!/bin/bash
# Generate PsiPartition tasks (local sweeps driver; 30 iters, k<=30, -nt 4, seed 0). Largest alignments first.
ROOT=/home/diepht/sliferskyd/hPartition/rerun_sim
DATA=/home/diepht/sliferskyd/hPartition-datasets/DNA
PY=/home/diepht/miniconda3/envs/PsiPartition/bin/python
: > $ROOT/tasks/psi.list.new
for f in $(ls -d $DATA/simulated-2/len_*/*.fasta | sort -t_ -k2,2nr) $(ls -d $DATA/simulated-1/loci_*/*.fasta | sort -t_ -k2,2nr); do
  sim=$(basename $(dirname $(dirname $f))); cat=$(basename $(dirname $f)); rep=$(basename $f .fasta)
  t="psi.$sim.$cat.$rep"; o=$ROOT/out/PsiPartition/$sim/$cat/$rep
  cat > $ROOT/tasks/$t.sh.tmp <<EOT
set -e
mkdir -p $o; cd $o
[ -e $rep.fasta ] || cp $f $rep.fasta
export PYTHONUNBUFFERED=1 WANDB_MODE=disabled
/usr/bin/time -v -o $o/time.txt $PY -W ignore $ROOT/bin/psi_local.py --msa $o/$rep.fasta --format fasta --alphabet dna --max_partitions 30 --n_iter 30 --seed 0 >> $o/cmd.log 2>&1
test -s $o/final.nwk && test -s $o/last.nwk
EOT
  mv $ROOT/tasks/$t.sh.tmp $ROOT/tasks/$t.sh
  echo $t >> $ROOT/tasks/psi.list.new
done
wc -l $ROOT/tasks/psi.list.new; head -2 $ROOT/tasks/psi.list.new; tail -1 $ROOT/tasks/psi.list.new
