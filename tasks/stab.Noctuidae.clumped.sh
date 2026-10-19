set -e
mkdir -p /home/diepht/sliferskyd/hPartition/rerun_sim/stability/out/Noctuidae.clumped
/home/diepht/sliferskyd/hPartition/rerun_sim/bin/eval_iqtree.sh /home/diepht/sliferskyd/hPartition-datasets/DNA/empirical/Noctuidae.phy /home/diepht/sliferskyd/hPartition/rerun_sim/stability/Noctuidae.clumped.nex /home/diepht/sliferskyd/hPartition/rerun_sim/stability/out/Noctuidae.clumped 1
test -s /home/diepht/sliferskyd/hPartition/rerun_sim/stability/out/Noctuidae.clumped/aln.treefile
