set -e
mkdir -p /home/diepht/sliferskyd/hPartition/rerun_sim/stability/out/Geometridae.clumped
/home/diepht/sliferskyd/hPartition/rerun_sim/bin/eval_iqtree.sh /home/diepht/sliferskyd/hPartition-datasets/DNA/empirical/Geometridae.phy /home/diepht/sliferskyd/hPartition/rerun_sim/stability/Geometridae.clumped.nex /home/diepht/sliferskyd/hPartition/rerun_sim/stability/out/Geometridae.clumped 1
test -s /home/diepht/sliferskyd/hPartition/rerun_sim/stability/out/Geometridae.clumped/aln.treefile
