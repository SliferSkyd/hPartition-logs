set -e
mkdir -p /home/diepht/sliferskyd/hPartition/rerun_sim/out_rna/hPartition/flu_H3N2/hPartition /home/diepht/sliferskyd/hPartition/rerun_sim/out_rna/hPartition/flu_H3N2/partition
cd /home/diepht/sliferskyd/hPartition/rerun_sim/out_rna/hPartition/flu_H3N2/hPartition
/usr/bin/time -v -o /home/diepht/sliferskyd/hPartition/rerun_sim/out_rna/hPartition/flu_H3N2/hPartition/time.txt /home/diepht/sliferskyd/hPartition/iqtree2/build/iqtree2 -seed 0 -s /home/diepht/sliferskyd/hPartition/rna_datasets/flu/aln/flu_H3N2.phy -pre /home/diepht/sliferskyd/hPartition/rerun_sim/out_rna/hPartition/flu_H3N2/hPartition/aln -hPartition -redo -mset JC69,F81,HKY,GTR -T 1 > /home/diepht/sliferskyd/hPartition/rerun_sim/out_rna/hPartition/flu_H3N2/hPartition/cmd.log 2>&1
/home/diepht/sliferskyd/hPartition/rerun_sim/bin/eval_iqtree.sh /home/diepht/sliferskyd/hPartition/rna_datasets/flu/aln/flu_H3N2.phy /home/diepht/sliferskyd/hPartition/rerun_sim/out_rna/hPartition/flu_H3N2/hPartition/aln.partitions /home/diepht/sliferskyd/hPartition/rerun_sim/out_rna/hPartition/flu_H3N2/partition
test -s /home/diepht/sliferskyd/hPartition/rerun_sim/out_rna/hPartition/flu_H3N2/partition/aln.treefile
