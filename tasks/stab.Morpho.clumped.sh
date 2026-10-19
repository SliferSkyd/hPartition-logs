set -e
mkdir -p /home/diepht/sliferskyd/hPartition/rerun_sim/stability/out/Morpho.clumped
/home/diepht/sliferskyd/hPartition/rerun_sim/bin/eval_iqtree.sh /home/diepht/sliferskyd/hPartition-datasets/DNA/empirical/Morpho.phy /home/diepht/sliferskyd/hPartition/rerun_sim/stability/Morpho.clumped.nex /home/diepht/sliferskyd/hPartition/rerun_sim/stability/out/Morpho.clumped 1
test -s /home/diepht/sliferskyd/hPartition/rerun_sim/stability/out/Morpho.clumped/aln.treefile
