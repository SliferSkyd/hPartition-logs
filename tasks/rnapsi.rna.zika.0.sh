set -e
mkdir -p /home/diepht/sliferskyd/hPartition/rerun_sim/out_rna/PsiPartition/zika; cd /home/diepht/sliferskyd/hPartition/rerun_sim/out_rna/PsiPartition/zika
[ -e zika.fasta ] || cp /home/diepht/sliferskyd/hPartition/rna_datasets/aln/zika.fasta zika.fasta
export PYTHONUNBUFFERED=1 WANDB_MODE=disabled
/usr/bin/time -v -o /home/diepht/sliferskyd/hPartition/rerun_sim/out_rna/PsiPartition/zika/time.txt /home/diepht/miniconda3/envs/PsiPartition/bin/python -W ignore /home/diepht/sliferskyd/hPartition/rerun_sim/bin/psi_local.py --msa /home/diepht/sliferskyd/hPartition/rerun_sim/out_rna/PsiPartition/zika/zika.fasta --format fasta --alphabet dna --max_partitions 30 --n_iter 30 --seed 0 >> /home/diepht/sliferskyd/hPartition/rerun_sim/out_rna/PsiPartition/zika/cmd.log 2>&1
test -s /home/diepht/sliferskyd/hPartition/rerun_sim/out_rna/PsiPartition/zika/final.nwk && test -s /home/diepht/sliferskyd/hPartition/rerun_sim/out_rna/PsiPartition/zika/last.nwk
