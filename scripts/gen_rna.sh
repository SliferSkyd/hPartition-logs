#!/bin/bash
# RNA-virus empirical datasets (Nextstrain genomes, MAFFT G-INS-1 + trimAl): same protocol as the simulated runs.
ROOT=/home/diepht/sliferskyd/hPartition/rerun_sim
ALN=/home/diepht/sliferskyd/hPartition/rna_datasets/aln
HPAR=/home/diepht/sliferskyd/hPartition/iqtree2/build/iqtree2
GDIR=/home/diepht/sliferskyd/hPartition/gPartition
PY=/home/diepht/miniconda3/envs/PsiPartition/bin/python
: > $ROOT/tasks/rnahpar.list; : > $ROOT/tasks/rnagpar.list; : > $ROOT/tasks/rnapsi.list
for v in measles mumps rabies denv1 zika; do
  # hPartition
  t=rnahpar.rna.$v.0; o1=$ROOT/out_rna/hPartition/$v/hPartition; o2=$ROOT/out_rna/hPartition/$v/partition
  cat > $ROOT/tasks/$t.sh.tmp <<EOT
set -e
mkdir -p $o1 $o2
cd $o1
/usr/bin/time -v -o $o1/time.txt $HPAR -seed 0 -s $ALN/$v.phy -pre $o1/aln -hPartition -redo -mset JC69,F81,HKY,GTR -T 1 > $o1/cmd.log 2>&1
$ROOT/bin/eval_iqtree.sh $ALN/$v.phy $o1/aln.partitions $o2
test -s $o2/aln.treefile
EOT
  mv $ROOT/tasks/$t.sh.tmp $ROOT/tasks/$t.sh; echo $t >> $ROOT/tasks/rnahpar.list
  # gPartition
  t=rnagpar.rna.$v.0; o1=$ROOT/out_rna/gPartition/$v/gPartition; o2=$ROOT/out_rna/gPartition/$v/partition
  cat > $ROOT/tasks/$t.sh.tmp <<EOT
set -e
rm -rf $o1 $o2; mkdir -p $o1 $o2
cd $GDIR
/usr/bin/time -v -o $o1/time.txt /home/diepht/anaconda3/bin/python gPartition.py -f $ALN/$v.phy -o $o1/ > $o1/cmd.log 2>&1
$ROOT/bin/eval_iqtree.sh $ALN/$v.phy $o1/$v.phy.FINAL.nex $o2
test -s $o2/aln.treefile
EOT
  mv $ROOT/tasks/$t.sh.tmp $ROOT/tasks/$t.sh; echo $t >> $ROOT/tasks/rnagpar.list
  # PsiPartition (30 iters, k<=30, -nt 4, seed 0)
  t=rnapsi.rna.$v.0; o=$ROOT/out_rna/PsiPartition/$v
  cat > $ROOT/tasks/$t.sh.tmp <<EOT
set -e
mkdir -p $o; cd $o
[ -e $v.fasta ] || cp $ALN/$v.fasta $v.fasta
export PYTHONUNBUFFERED=1 WANDB_MODE=disabled
/usr/bin/time -v -o $o/time.txt $PY -W ignore $ROOT/bin/psi_local.py --msa $o/$v.fasta --format fasta --alphabet dna --max_partitions 30 --n_iter 30 --seed 0 >> $o/cmd.log 2>&1
test -s $o/final.nwk && test -s $o/last.nwk
EOT
  mv $ROOT/tasks/$t.sh.tmp $ROOT/tasks/$t.sh; echo $t >> $ROOT/tasks/rnapsi.list
done
wc -l $ROOT/tasks/rna*.list
