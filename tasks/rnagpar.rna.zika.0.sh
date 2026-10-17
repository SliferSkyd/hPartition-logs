set -e
rm -rf /home/diepht/sliferskyd/hPartition/rerun_sim/out_rna/gPartition/zika/gPartition /home/diepht/sliferskyd/hPartition/rerun_sim/out_rna/gPartition/zika/partition; mkdir -p /home/diepht/sliferskyd/hPartition/rerun_sim/out_rna/gPartition/zika/gPartition /home/diepht/sliferskyd/hPartition/rerun_sim/out_rna/gPartition/zika/partition
cd /home/diepht/sliferskyd/hPartition/gPartition
/usr/bin/time -v -o /home/diepht/sliferskyd/hPartition/rerun_sim/out_rna/gPartition/zika/gPartition/time.txt /home/diepht/anaconda3/bin/python gPartition.py -f /home/diepht/sliferskyd/hPartition/rna_datasets/aln/zika.phy -o /home/diepht/sliferskyd/hPartition/rerun_sim/out_rna/gPartition/zika/gPartition/ > /home/diepht/sliferskyd/hPartition/rerun_sim/out_rna/gPartition/zika/gPartition/cmd.log 2>&1
/home/diepht/sliferskyd/hPartition/rerun_sim/bin/eval_iqtree.sh /home/diepht/sliferskyd/hPartition/rna_datasets/aln/zika.phy /home/diepht/sliferskyd/hPartition/rerun_sim/out_rna/gPartition/zika/gPartition/zika.phy.FINAL.nex /home/diepht/sliferskyd/hPartition/rerun_sim/out_rna/gPartition/zika/partition
test -s /home/diepht/sliferskyd/hPartition/rerun_sim/out_rna/gPartition/zika/partition/aln.treefile
