set -e
mkdir -p /home/diepht/sliferskyd/hPartition/rerun_sim/stability/out/Morpho.hpar
/home/diepht/sliferskyd/hPartition/rerun_sim/bin/eval_iqtree.sh /home/diepht/sliferskyd/hPartition-datasets/DNA/empirical/Morpho.phy /home/diepht/sliferskyd/hPartition-datasets/DNA/empirical/Morpho.phy.partitions /home/diepht/sliferskyd/hPartition/rerun_sim/stability/out/Morpho.hpar 1
test -s /home/diepht/sliferskyd/hPartition/rerun_sim/stability/out/Morpho.hpar/aln.treefile
