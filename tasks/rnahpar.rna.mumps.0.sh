set -e
mkdir -p /home/diepht/sliferskyd/hPartition/rerun_sim/out_rna/hPartition/mumps/hPartition /home/diepht/sliferskyd/hPartition/rerun_sim/out_rna/hPartition/mumps/partition
cd /home/diepht/sliferskyd/hPartition/rerun_sim/out_rna/hPartition/mumps/hPartition
/usr/bin/time -v -o /home/diepht/sliferskyd/hPartition/rerun_sim/out_rna/hPartition/mumps/hPartition/time.txt /home/diepht/sliferskyd/hPartition/iqtree2/build/iqtree2 -seed 0 -s /home/diepht/sliferskyd/hPartition/rna_datasets/aln/mumps.phy -pre /home/diepht/sliferskyd/hPartition/rerun_sim/out_rna/hPartition/mumps/hPartition/aln -hPartition -redo -mset JC69,F81,HKY,GTR -T 1 > /home/diepht/sliferskyd/hPartition/rerun_sim/out_rna/hPartition/mumps/hPartition/cmd.log 2>&1
/home/diepht/sliferskyd/hPartition/rerun_sim/bin/eval_iqtree.sh /home/diepht/sliferskyd/hPartition/rna_datasets/aln/mumps.phy /home/diepht/sliferskyd/hPartition/rerun_sim/out_rna/hPartition/mumps/hPartition/aln.partitions /home/diepht/sliferskyd/hPartition/rerun_sim/out_rna/hPartition/mumps/partition
test -s /home/diepht/sliferskyd/hPartition/rerun_sim/out_rna/hPartition/mumps/partition/aln.treefile
