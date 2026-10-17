set -e
mkdir -p /home/diepht/sliferskyd/hPartition/rerun_sim/out_rna/PsiPartition/measles; cd /home/diepht/sliferskyd/hPartition/rerun_sim/out_rna/PsiPartition/measles
[ -e measles.fasta ] || cp /home/diepht/sliferskyd/hPartition/rna_datasets/aln/measles.fasta measles.fasta
export PYTHONUNBUFFERED=1 WANDB_MODE=disabled
/usr/bin/time -v -o /home/diepht/sliferskyd/hPartition/rerun_sim/out_rna/PsiPartition/measles/time.txt /home/diepht/miniconda3/envs/PsiPartition/bin/python -W ignore /home/diepht/sliferskyd/hPartition/rerun_sim/bin/psi_local.py --msa /home/diepht/sliferskyd/hPartition/rerun_sim/out_rna/PsiPartition/measles/measles.fasta --format fasta --alphabet dna --max_partitions 30 --n_iter 30 --seed 0 >> /home/diepht/sliferskyd/hPartition/rerun_sim/out_rna/PsiPartition/measles/cmd.log 2>&1
test -s /home/diepht/sliferskyd/hPartition/rerun_sim/out_rna/PsiPartition/measles/final.nwk && test -s /home/diepht/sliferskyd/hPartition/rerun_sim/out_rna/PsiPartition/measles/last.nwk
