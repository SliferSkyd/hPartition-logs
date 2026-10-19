set -e
mkdir -p /home/diepht/sliferskyd/hPartition/rerun_sim/out_rna/hPartition/mito/hPartition /home/diepht/sliferskyd/hPartition/rerun_sim/out_rna/hPartition/mito/partition
cd /home/diepht/sliferskyd/hPartition/rerun_sim/out_rna/hPartition/mito/hPartition
/usr/bin/time -v -o /home/diepht/sliferskyd/hPartition/rerun_sim/out_rna/hPartition/mito/hPartition/time.txt /home/diepht/sliferskyd/hPartition/iqtree2/build/iqtree2 -seed 0 -s /home/diepht/sliferskyd/hPartition/rna_datasets/mito/aln/mito.phy -pre /home/diepht/sliferskyd/hPartition/rerun_sim/out_rna/hPartition/mito/hPartition/aln -hPartition -redo -mset JC69,F81,HKY,GTR -T 1 > /home/diepht/sliferskyd/hPartition/rerun_sim/out_rna/hPartition/mito/hPartition/cmd.log 2>&1
/home/diepht/sliferskyd/hPartition/rerun_sim/bin/eval_iqtree.sh /home/diepht/sliferskyd/hPartition/rna_datasets/mito/aln/mito.phy /home/diepht/sliferskyd/hPartition/rerun_sim/out_rna/hPartition/mito/hPartition/aln.partitions /home/diepht/sliferskyd/hPartition/rerun_sim/out_rna/hPartition/mito/partition 1
test -s /home/diepht/sliferskyd/hPartition/rerun_sim/out_rna/hPartition/mito/partition/aln.treefile
