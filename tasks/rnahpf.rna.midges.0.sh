set -e
mkdir -p /home/diepht/sliferskyd/hPartition/rerun_sim/out_rna/hPartition-PF/midges/hPartition /home/diepht/sliferskyd/hPartition/rerun_sim/out_rna/hPartition-PF/midges/partition
cd /home/diepht/sliferskyd/hPartition/rerun_sim/out_rna/hPartition-PF/midges/hPartition
/usr/bin/time -v -o /home/diepht/sliferskyd/hPartition/rerun_sim/out_rna/hPartition-PF/midges/hPartition/time.txt /home/diepht/sliferskyd/hPartition/iqtree2/build/iqtree2 -seed 0 -s /home/diepht/sliferskyd/hPartition/rna_datasets/pf/aln/midges.phy -pre /home/diepht/sliferskyd/hPartition/rerun_sim/out_rna/hPartition-PF/midges/hPartition/aln -hPartition-pf -redo -mset JC69,F81,HKY,GTR -T 1 > /home/diepht/sliferskyd/hPartition/rerun_sim/out_rna/hPartition-PF/midges/hPartition/cmd.log 2>&1
/home/diepht/sliferskyd/hPartition/rerun_sim/bin/eval_iqtree.sh /home/diepht/sliferskyd/hPartition/rna_datasets/pf/aln/midges.phy /home/diepht/sliferskyd/hPartition/rerun_sim/out_rna/hPartition-PF/midges/hPartition/aln.partitions /home/diepht/sliferskyd/hPartition/rerun_sim/out_rna/hPartition-PF/midges/partition 1
test -s /home/diepht/sliferskyd/hPartition/rerun_sim/out_rna/hPartition-PF/midges/partition/aln.treefile
