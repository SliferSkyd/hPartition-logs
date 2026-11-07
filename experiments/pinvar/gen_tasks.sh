#!/bin/bash
# One task per (level, replicate, method). Each runs the method, then scores the resulting
# scheme with bin/eval_iqtree.sh -- the same command used for every other scheme in the paper,
# so the three methods are compared on equal footing rather than on their own internal scoring.
P=/home/diepht/sliferskyd/hPartition/rerun_sim/pinvar
R=/home/diepht/sliferskyd/hPartition/rerun_sim
HPAR=/home/diepht/sliferskyd/hPartition/iqtree2/build/iqtree2
GDIR=/home/diepht/sliferskyd/hPartition/gPartition
PY=/home/diepht/miniconda3/envs/PsiPartition/bin/python
rm -f $P/tasks/*.sh
for d in $P/data/p*; do
  tag=$(basename $d)
  for rep in $(seq 0 9); do
    aln=$d/$rep.phy; fa=$d/$rep.fasta

    o=$P/out/hpar.$tag.$rep
    cat > $P/tasks/hpar.$tag.$rep.sh <<EOT
#!/bin/bash
unset LD_LIBRARY_PATH
set -e
mkdir -p $o/hPartition $o/partition
cd $o/hPartition
/usr/bin/time -v -o $o/hPartition/time.txt $HPAR -seed 0 -s $aln -pre $o/hPartition/aln -hPartition -redo -mset JC69,F81,HKY,GTR -T 1 > $o/hPartition/cmd.log 2>&1
$R/bin/eval_iqtree.sh $aln $o/hPartition/aln.partitions $o/partition 1
test -s $o/partition/aln.treefile
EOT

    o=$P/out/gpar.$tag.$rep
    cat > $P/tasks/gpar.$tag.$rep.sh <<EOT
#!/bin/bash
unset LD_LIBRARY_PATH
set -e
rm -rf $o; mkdir -p $o/gPartition $o/partition
cd $GDIR
/usr/bin/time -v -o $o/gPartition/time.txt /home/diepht/anaconda3/bin/python gPartition.py -f $aln -o $o/gPartition/ > $o/gPartition/cmd.log 2>&1
$R/bin/eval_iqtree.sh $aln $o/gPartition/$rep.phy.FINAL.nex $o/partition 1
test -s $o/partition/aln.treefile
EOT

    o=$P/out/psi.$tag.$rep
    cat > $P/tasks/psi.$tag.$rep.sh <<EOT
#!/bin/bash
unset LD_LIBRARY_PATH
set -e
mkdir -p $o/PsiPartition $o/partition
cd $o/PsiPartition
[ -e $rep.fasta ] || cp $fa $rep.fasta
export PYTHONUNBUFFERED=1 WANDB_MODE=disabled
/usr/bin/time -v -o $o/PsiPartition/time.txt $PY -W ignore $R/bin/psi_local.py --msa $o/PsiPartition/$rep.fasta --format fasta --alphabet dna --max_partitions 30 --n_iter 30 --seed 0 >> $o/PsiPartition/cmd.log 2>&1
$R/bin/eval_iqtree.sh $aln $o/PsiPartition/$rep.final.parts $o/partition 1
test -s $o/partition/aln.treefile
EOT
  done
done
chmod +x $P/tasks/*.sh
ls $P/tasks/*.sh | wc -l
