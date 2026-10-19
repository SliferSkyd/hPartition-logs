set -e
mkdir -p /home/diepht/sliferskyd/hPartition/rerun_sim/stability/out/Calisto.hpar
/home/diepht/sliferskyd/hPartition/rerun_sim/bin/eval_iqtree.sh /home/diepht/sliferskyd/hPartition-datasets/DNA/empirical/Calisto.phy /home/diepht/sliferskyd/hPartition-datasets/DNA/empirical/Calisto.phy.partitions /home/diepht/sliferskyd/hPartition/rerun_sim/stability/out/Calisto.hpar 1
test -s /home/diepht/sliferskyd/hPartition/rerun_sim/stability/out/Calisto.hpar/aln.treefile
