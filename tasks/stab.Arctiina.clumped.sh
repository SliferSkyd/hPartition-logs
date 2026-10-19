set -e
mkdir -p /home/diepht/sliferskyd/hPartition/rerun_sim/stability/out/Arctiina.clumped
/home/diepht/sliferskyd/hPartition/rerun_sim/bin/eval_iqtree.sh /home/diepht/sliferskyd/hPartition-datasets/DNA/empirical/Arctiina.phy /home/diepht/sliferskyd/hPartition/rerun_sim/stability/Arctiina.clumped.nex /home/diepht/sliferskyd/hPartition/rerun_sim/stability/out/Arctiina.clumped 1
test -s /home/diepht/sliferskyd/hPartition/rerun_sim/stability/out/Arctiina.clumped/aln.treefile
