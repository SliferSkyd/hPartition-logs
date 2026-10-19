set -e
mkdir -p /home/diepht/sliferskyd/hPartition/rerun_sim/stability/out/Pieridae.clumped
/home/diepht/sliferskyd/hPartition/rerun_sim/bin/eval_iqtree.sh /home/diepht/sliferskyd/hPartition-datasets/DNA/empirical/Pieridae.phy /home/diepht/sliferskyd/hPartition/rerun_sim/stability/Pieridae.clumped.nex /home/diepht/sliferskyd/hPartition/rerun_sim/stability/out/Pieridae.clumped 1
test -s /home/diepht/sliferskyd/hPartition/rerun_sim/stability/out/Pieridae.clumped/aln.treefile
