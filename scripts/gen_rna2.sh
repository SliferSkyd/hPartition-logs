#!/bin/bash
# Append RNA tasks for the given datasets (aln/<ds>.{phy,fasta}) and methods. Same commands as gen_rna.sh, plus
# hPartition-PF (-hPartition-pf). Usage: gen_rna2.sh "hpar hpf gpar psi" ds1 ds2 ...
ROOT=/home/diepht/sliferskyd/hPartition/rerun_sim
ALN=${ALN:-/home/diepht/sliferskyd/hPartition/rna_datasets/aln}
HPAR=/home/diepht/sliferskyd/hPartition/iqtree2/build/iqtree2
GDIR=/home/diepht/sliferskyd/hPartition/gPartition
PY=/home/diepht/miniconda3/envs/PsiPartition/bin/python
NT=${NT:-1}   # IQ-TREE threads (full-size MSAs need more than 1)
MAXH=${MAXH:-}   # optional wall-clock budget for PsiPartition (hours)
methods=$1; shift
add() { grep -qx "$1" $ROOT/tasks/$2.list 2>/dev/null || echo $1 >> $ROOT/tasks/$2.list; mv $ROOT/tasks/$1.sh.tmp $ROOT/tasks/$1.sh; }
for v in "$@"; do
 for m in $methods; do case $m in
  hpar|hpf)
   flag=$([ $m = hpf ] && echo -hPartition-pf || echo -hPartition); M=$([ $m = hpf ] && echo hPartition-PF || echo hPartition)
   t=rna$m.rna.$v.0; o1=$ROOT/out_rna/$M/$v/hPartition; o2=$ROOT/out_rna/$M/$v/partition
   cat > $ROOT/tasks/$t.sh.tmp <<EOT
set -e
mkdir -p $o1 $o2
cd $o1
/usr/bin/time -v -o $o1/time.txt $HPAR -seed 0 -s $ALN/$v.phy -pre $o1/aln $flag -redo -mset JC69,F81,HKY,GTR -T $NT > $o1/cmd.log 2>&1
$ROOT/bin/eval_iqtree.sh $ALN/$v.phy $o1/aln.partitions $o2 $NT
test -s $o2/aln.treefile
EOT
   add $t rna$m ;;
  gpar)
   t=rnagpar.rna.$v.0; o1=$ROOT/out_rna/gPartition/$v/gPartition; o2=$ROOT/out_rna/gPartition/$v/partition
   cat > $ROOT/tasks/$t.sh.tmp <<EOT
set -e
rm -rf $o1 $o2; mkdir -p $o1 $o2
cd $GDIR
/usr/bin/time -v -o $o1/time.txt /home/diepht/anaconda3/bin/python gPartition.py -f $ALN/$v.phy -o $o1/ > $o1/cmd.log 2>&1
$ROOT/bin/eval_iqtree.sh $ALN/$v.phy $o1/$v.phy.FINAL.nex $o2 $NT
test -s $o2/aln.treefile
EOT
   add $t rnagpar ;;
  psi)
   t=rnapsi.rna.$v.0; o=$ROOT/out_rna/PsiPartition/$v
   cat > $ROOT/tasks/$t.sh.tmp <<EOT
set -e
mkdir -p $o; cd $o
[ -e $v.fasta ] || tr a-z A-Z < $ALN/$v.fasta > $v.fasta   # PsiPartition only recognises uppercase ACGT
export PYTHONUNBUFFERED=1 WANDB_MODE=disabled
/usr/bin/time -v -o $o/time.txt $PY -W ignore $ROOT/bin/psi_local.py --msa $o/$v.fasta --format fasta --alphabet dna --max_partitions 30 --n_iter 30 --seed 0 ${MAXH:+--max_hours $MAXH} >> $o/cmd.log 2>&1
test -s $o/final.nwk && test -s $o/last.nwk
EOT
   add $t rnapsi ;;
 esac; done
done
wc -l $ROOT/tasks/rna*.list
