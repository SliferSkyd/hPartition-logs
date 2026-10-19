set -e
mkdir -p /home/diepht/sliferskyd/hPartition/rerun_sim/stability/out/Pieridae.hpar
/home/diepht/sliferskyd/hPartition/rerun_sim/bin/eval_iqtree.sh /home/diepht/sliferskyd/hPartition-datasets/DNA/empirical/Pieridae.phy /home/diepht/sliferskyd/hPartition-datasets/DNA/empirical/Pieridae.phy.partitions /home/diepht/sliferskyd/hPartition/rerun_sim/stability/out/Pieridae.hpar 1
test -s /home/diepht/sliferskyd/hPartition/rerun_sim/stability/out/Pieridae.hpar/aln.treefile
