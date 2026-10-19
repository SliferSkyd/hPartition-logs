set -e
mkdir -p /home/diepht/sliferskyd/hPartition/rerun_sim/out_rna/hPartition-noMset/zika/hPartition /home/diepht/sliferskyd/hPartition/rerun_sim/out_rna/hPartition-noMset/zika/partition
cd /home/diepht/sliferskyd/hPartition/rerun_sim/out_rna/hPartition-noMset/zika/hPartition
/usr/bin/time -v -o /home/diepht/sliferskyd/hPartition/rerun_sim/out_rna/hPartition-noMset/zika/hPartition/time.txt /home/diepht/sliferskyd/hPartition/iqtree2/build/iqtree2 -seed 0 -s /home/diepht/sliferskyd/hPartition/rerun_sim/../rna_datasets/aln/zika.phy -pre /home/diepht/sliferskyd/hPartition/rerun_sim/out_rna/hPartition-noMset/zika/hPartition/aln -hPartition -redo -T 1 > /home/diepht/sliferskyd/hPartition/rerun_sim/out_rna/hPartition-noMset/zika/hPartition/cmd.log 2>&1
/home/diepht/sliferskyd/hPartition/rerun_sim/bin/eval_iqtree.sh /home/diepht/sliferskyd/hPartition/rerun_sim/../rna_datasets/aln/zika.phy /home/diepht/sliferskyd/hPartition/rerun_sim/out_rna/hPartition-noMset/zika/hPartition/aln.partitions /home/diepht/sliferskyd/hPartition/rerun_sim/out_rna/hPartition-noMset/zika/partition 1
test -s /home/diepht/sliferskyd/hPartition/rerun_sim/out_rna/hPartition-noMset/zika/partition/aln.treefile
