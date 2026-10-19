set -e
mkdir -p /home/diepht/sliferskyd/hPartition/rerun_sim/stability/out/Arctiina.hpar
/home/diepht/sliferskyd/hPartition/rerun_sim/bin/eval_iqtree.sh /home/diepht/sliferskyd/hPartition-datasets/DNA/empirical/Arctiina.phy /home/diepht/sliferskyd/hPartition-datasets/DNA/empirical/Arctiina.phy.partitions /home/diepht/sliferskyd/hPartition/rerun_sim/stability/out/Arctiina.hpar 1
test -s /home/diepht/sliferskyd/hPartition/rerun_sim/stability/out/Arctiina.hpar/aln.treefile
