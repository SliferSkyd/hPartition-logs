set -e
mkdir -p /home/diepht/sliferskyd/hPartition/rerun_sim/stability/out/Choreutidae.hpar
/home/diepht/sliferskyd/hPartition/rerun_sim/bin/eval_iqtree.sh /home/diepht/sliferskyd/hPartition-datasets/DNA/empirical/Choreutidae.phy /home/diepht/sliferskyd/hPartition-datasets/DNA/empirical/Choreutidae.phy.partitions /home/diepht/sliferskyd/hPartition/rerun_sim/stability/out/Choreutidae.hpar 1
test -s /home/diepht/sliferskyd/hPartition/rerun_sim/stability/out/Choreutidae.hpar/aln.treefile
