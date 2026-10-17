set -e
mkdir -p /home/diepht/sliferskyd/hPartition/rerun_sim/out_rna/hPartition/rabies/hPartition /home/diepht/sliferskyd/hPartition/rerun_sim/out_rna/hPartition/rabies/partition
cd /home/diepht/sliferskyd/hPartition/rerun_sim/out_rna/hPartition/rabies/hPartition
/usr/bin/time -v -o /home/diepht/sliferskyd/hPartition/rerun_sim/out_rna/hPartition/rabies/hPartition/time.txt /home/diepht/sliferskyd/hPartition/iqtree2/build/iqtree2 -seed 0 -s /home/diepht/sliferskyd/hPartition/rna_datasets/aln/rabies.phy -pre /home/diepht/sliferskyd/hPartition/rerun_sim/out_rna/hPartition/rabies/hPartition/aln -hPartition -redo -mset JC69,F81,HKY,GTR -T 1 > /home/diepht/sliferskyd/hPartition/rerun_sim/out_rna/hPartition/rabies/hPartition/cmd.log 2>&1
/home/diepht/sliferskyd/hPartition/rerun_sim/bin/eval_iqtree.sh /home/diepht/sliferskyd/hPartition/rna_datasets/aln/rabies.phy /home/diepht/sliferskyd/hPartition/rerun_sim/out_rna/hPartition/rabies/hPartition/aln.partitions /home/diepht/sliferskyd/hPartition/rerun_sim/out_rna/hPartition/rabies/partition
test -s /home/diepht/sliferskyd/hPartition/rerun_sim/out_rna/hPartition/rabies/partition/aln.treefile
