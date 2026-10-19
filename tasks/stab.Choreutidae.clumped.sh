set -e
mkdir -p /home/diepht/sliferskyd/hPartition/rerun_sim/stability/out/Choreutidae.clumped
/home/diepht/sliferskyd/hPartition/rerun_sim/bin/eval_iqtree.sh /home/diepht/sliferskyd/hPartition-datasets/DNA/empirical/Choreutidae.phy /home/diepht/sliferskyd/hPartition/rerun_sim/stability/Choreutidae.clumped.nex /home/diepht/sliferskyd/hPartition/rerun_sim/stability/out/Choreutidae.clumped 1
test -s /home/diepht/sliferskyd/hPartition/rerun_sim/stability/out/Choreutidae.clumped/aln.treefile
