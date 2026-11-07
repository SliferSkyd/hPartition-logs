#!/bin/bash
# RF distance of each inferred tree to the true tree, the metric the manuscript uses for the
# simulated benchmark (hPartition-sim-rerun/scripts/plot_rf.py reads per-replicate RF).
unset LD_LIBRARY_PATH
set -e
P=/home/diepht/sliferskyd/hPartition/rerun_sim/pinvar
IQ=/home/diepht/sliferskyd/hPartition/iqtree-2.4.0-Linux-intel/bin/iqtree2
TRUE=/home/diepht/sliferskyd/hPartition-datasets/DNA/simulated-1/loci_5
mkdir -p $P/rf; : > $P/rf/rf.tsv
for lv in p00 p15 p30 p45 p60 p75; do
  for m in hpar gpar psi; do
    for r in $(seq 0 9); do
      t=$P/out/$m.$lv.$r/partition/aln.treefile
      [ -s "$t" ] || { echo -e "$lv\t$m\t$r\tNA" >> $P/rf/rf.tsv; continue; }
      w=$P/rf/$m.$lv.$r; mkdir -p $w
      cat $t $TRUE/$r.tree > $w/pair.tre
      $IQ -rf_all $w/pair.tre -pre $w/x -redo -quiet > /dev/null 2>&1 || true
      v=$(awk 'NR==2{print $3}' $w/x.rfdist 2>/dev/null)
      echo -e "$lv\t$m\t$r\t${v:-NA}" >> $P/rf/rf.tsv
    done
  done
done
wc -l < $P/rf/rf.tsv
