set -e
mkdir -p /home/diepht/sliferskyd/hPartition/rerun_sim/stability/out/Calisto.clumped
/home/diepht/sliferskyd/hPartition/rerun_sim/bin/eval_iqtree.sh /home/diepht/sliferskyd/hPartition-datasets/DNA/empirical/Calisto.phy /home/diepht/sliferskyd/hPartition/rerun_sim/stability/Calisto.clumped.nex /home/diepht/sliferskyd/hPartition/rerun_sim/stability/out/Calisto.clumped 1
test -s /home/diepht/sliferskyd/hPartition/rerun_sim/stability/out/Calisto.clumped/aln.treefile
