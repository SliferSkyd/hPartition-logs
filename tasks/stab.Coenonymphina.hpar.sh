set -e
mkdir -p /home/diepht/sliferskyd/hPartition/rerun_sim/stability/out/Coenonymphina.hpar
/home/diepht/sliferskyd/hPartition/rerun_sim/bin/eval_iqtree.sh /home/diepht/sliferskyd/hPartition-datasets/DNA/empirical/Coenonymphina.phy /home/diepht/sliferskyd/hPartition-datasets/DNA/empirical/Coenonymphina.phy.partitions /home/diepht/sliferskyd/hPartition/rerun_sim/stability/out/Coenonymphina.hpar 1
test -s /home/diepht/sliferskyd/hPartition/rerun_sim/stability/out/Coenonymphina.hpar/aln.treefile
