set -e
mkdir -p /home/diepht/sliferskyd/hPartition/rerun_sim/out_rna/PsiPartition/flu_B_Victoria; cd /home/diepht/sliferskyd/hPartition/rerun_sim/out_rna/PsiPartition/flu_B_Victoria
[ -e flu_B_Victoria.fasta ] || tr a-z A-Z < /home/diepht/sliferskyd/hPartition/rna_datasets/flu/aln/flu_B_Victoria.fasta > flu_B_Victoria.fasta   # PsiPartition only recognises uppercase ACGT
export PYTHONUNBUFFERED=1 WANDB_MODE=disabled
/usr/bin/time -v -o /home/diepht/sliferskyd/hPartition/rerun_sim/out_rna/PsiPartition/flu_B_Victoria/time.txt /home/diepht/miniconda3/envs/PsiPartition/bin/python -W ignore /home/diepht/sliferskyd/hPartition/rerun_sim/bin/psi_local.py --msa /home/diepht/sliferskyd/hPartition/rerun_sim/out_rna/PsiPartition/flu_B_Victoria/flu_B_Victoria.fasta --format fasta --alphabet dna --max_partitions 30 --n_iter 30 --seed 0 >> /home/diepht/sliferskyd/hPartition/rerun_sim/out_rna/PsiPartition/flu_B_Victoria/cmd.log 2>&1
test -s /home/diepht/sliferskyd/hPartition/rerun_sim/out_rna/PsiPartition/flu_B_Victoria/final.nwk && test -s /home/diepht/sliferskyd/hPartition/rerun_sim/out_rna/PsiPartition/flu_B_Victoria/last.nwk
