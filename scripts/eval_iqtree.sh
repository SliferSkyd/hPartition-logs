#!/bin/bash
# Evaluation run with stock IQ-TREE 2.4.0. If it aborts on the known FreeRate EM assertion
# (ratefree.cpp: optimizeWithEM), rerun the same replicate excluding +R models (-mrate E,I,G,I+G),
# as agreed with the user, and leave a NORATE_FALLBACK marker. Usage: eval_iqtree.sh ALN PARTFILE OUTDIR
IQ=/home/diepht/sliferskyd/hPartition/iqtree-2.4.0-Linux-intel/bin/iqtree2
aln=$1; part=$2; o=$3; NT=${4:-1}
cd $o
/usr/bin/time -v -o $o/time.txt $IQ -seed 0 -s $aln -p $part -pre $o/aln -redo -T $NT > $o/cmd.log 2>&1 && exit 0
if grep -q "ratefree.cpp.*optimizeWithEM" $o/aln.log; then
  mkdir -p $o/crashed_with_R; mv $o/aln.log $o/cmd.log $o/time.txt $o/crashed_with_R/ 2>/dev/null
  echo "FreeRate EM assertion with default model set; reran with -mrate E,I,G,I+G" > $o/NORATE_FALLBACK
  /usr/bin/time -v -o $o/time.txt $IQ -seed 0 -s $aln -p $part -pre $o/aln -redo -T $NT -mrate E,I,G,I+G > $o/cmd.log 2>&1
else
  exit 1
fi
