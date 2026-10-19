set -e
mkdir -p /home/diepht/sliferskyd/hPartition/rerun_sim/stability/out/Geometridae.hpar
/home/diepht/sliferskyd/hPartition/rerun_sim/bin/eval_iqtree.sh /home/diepht/sliferskyd/hPartition-datasets/DNA/empirical/Geometridae.phy /home/diepht/sliferskyd/hPartition-datasets/DNA/empirical/Geometridae.phy.partitions /home/diepht/sliferskyd/hPartition/rerun_sim/stability/out/Geometridae.hpar 1
test -s /home/diepht/sliferskyd/hPartition/rerun_sim/stability/out/Geometridae.hpar/aln.treefile
