set -e
mkdir -p /home/diepht/sliferskyd/hPartition/rerun_sim/stability/out/Noctuidae.hpar
/home/diepht/sliferskyd/hPartition/rerun_sim/bin/eval_iqtree.sh /home/diepht/sliferskyd/hPartition-datasets/DNA/empirical/Noctuidae.phy /home/diepht/sliferskyd/hPartition-datasets/DNA/empirical/Noctuidae.phy.partitions /home/diepht/sliferskyd/hPartition/rerun_sim/stability/out/Noctuidae.hpar 1
test -s /home/diepht/sliferskyd/hPartition/rerun_sim/stability/out/Noctuidae.hpar/aln.treefile
