#!/bin/bash
# Generate gPartition tasks (old script: gPartition.py then iqtree2 2.4.0 -seed 0 eval)
ROOT=/home/diepht/sliferskyd/hPartition/rerun_sim
DATA=/home/diepht/sliferskyd/hPartition-datasets/DNA
GDIR=/home/diepht/sliferskyd/hPartition/gPartition
IQ=/home/diepht/sliferskyd/hPartition/iqtree-2.4.0-Linux-intel/bin/iqtree2
: > $ROOT/tasks/gpar.list.new
for sim in simulated-1 simulated-2; do
  for f in $DATA/$sim/*/*.phy; do
    cat=$(basename $(dirname $f)); rep=$(basename $f .phy)
    t="gpar.$sim.$cat.$rep"
    o1=$ROOT/out/gPartition/$sim/$cat/$rep/gPartition; o2=$ROOT/out/gPartition/$sim/$cat/$rep/partition
    cat > $ROOT/tasks/$t.sh.tmp <<EOT
set -e
rm -rf $o1 $o2; mkdir -p $o1 $o2
cd $GDIR
/usr/bin/time -v -o $o1/time.txt /home/diepht/anaconda3/bin/python gPartition.py -f $f -o $o1/ > $o1/cmd.log 2>&1
$ROOT/bin/eval_iqtree.sh $f $o1/$rep.phy.FINAL.nex $o2
test -s $o2/aln.treefile
EOT
    mv $ROOT/tasks/$t.sh.tmp $ROOT/tasks/$t.sh
    echo $t >> $ROOT/tasks/gpar.list.new
  done
done
wc -l $ROOT/tasks/gpar.list.new
