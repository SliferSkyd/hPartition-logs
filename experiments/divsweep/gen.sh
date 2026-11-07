#!/bin/bash
# Seed-bin divisor sweep: does the value 100 in k0 = floor(m/divisor) sit near the BIC minimum?
# One job per (dataset, divisor). hPartition is run exactly as in the paper apart from the divisor,
# which the patched binary reads from HPARTITION_BIN_DIVISOR (unset => 100, the released behaviour).
R=/home/diepht/sliferskyd/hPartition
IQ=$R/iqtree2/build/iqtree2
DATA=$R-datasets/DNA/empirical
S=$R/rerun_sim/divsweep
for ds in Arctiina Calisto Choreutidae Coenonymphina Geometridae Morpho Noctuidae Pieridae; do
  for d in 50 100 200 400; do
    O=$S/out/$ds.d$d
    cat > $S/tasks/$ds.d$d.sh <<TASK
#!/bin/bash
unset LD_LIBRARY_PATH
set -e
mkdir -p $O/hPartition $O/partition
export HPARTITION_BIN_DIVISOR=$d
/usr/bin/time -v -o $O/hPartition/time.txt $IQ -seed 0 -s $DATA/$ds.phy \\
  -pre $O/hPartition/aln -hPartition -redo -mset JC69,F81,HKY,GTR -T 1 \\
  > $O/hPartition/cmd.log 2>&1
unset HPARTITION_BIN_DIVISOR
$R/rerun_sim/bin/eval_iqtree.sh $DATA/$ds.phy $O/hPartition/aln.partitions $O/partition 1
TASK
    chmod +x $S/tasks/$ds.d$d.sh
  done
done
echo "generated $(ls $S/tasks | wc -l) task scripts"
