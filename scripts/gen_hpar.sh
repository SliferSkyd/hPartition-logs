#!/bin/bash
# Generate hPartition tasks (plain -hPartition, seed 0, as requested by user)
ROOT=/home/diepht/sliferskyd/hPartition/rerun_sim
DATA=/home/diepht/sliferskyd/hPartition-datasets/DNA
HPAR=/home/diepht/sliferskyd/hPartition/iqtree2/build/iqtree2
IQ=/home/diepht/sliferskyd/hPartition/iqtree-2.4.0-Linux-intel/bin/iqtree2
: > $ROOT/tasks/hpar.list.new
for sim in simulated-1 simulated-2; do
  for f in $DATA/$sim/*/*.phy; do
    cat=$(basename $(dirname $f)); rep=$(basename $f .phy)
    t="hpar.$sim.$cat.$rep"
    o1=$ROOT/out/hPartition/$sim/$cat/$rep/hPartition; o2=$ROOT/out/hPartition/$sim/$cat/$rep/partition
    cat > $ROOT/tasks/$t.sh.tmp <<EOT
set -e
mkdir -p $o1 $o2
cd $o1
/usr/bin/time -v -o $o1/time.txt $HPAR -seed 0 -s $f -pre $o1/aln -hPartition -redo -mset JC69,F81,HKY,GTR -T 1 > $o1/cmd.log 2>&1
$ROOT/bin/eval_iqtree.sh $f $o1/aln.partitions $o2
test -s $o2/aln.treefile
EOT
    mv $ROOT/tasks/$t.sh.tmp $ROOT/tasks/$t.sh
    echo $t >> $ROOT/tasks/hpar.list.new
  done
done
wc -l $ROOT/tasks/hpar.list.new
