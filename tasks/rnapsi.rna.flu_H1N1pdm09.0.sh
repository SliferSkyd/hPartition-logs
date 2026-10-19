set -e
mkdir -p /home/diepht/sliferskyd/hPartition/rerun_sim/out_rna/PsiPartition/flu_H1N1pdm09; cd /home/diepht/sliferskyd/hPartition/rerun_sim/out_rna/PsiPartition/flu_H1N1pdm09
[ -e flu_H1N1pdm09.fasta ] || tr a-z A-Z < /home/diepht/sliferskyd/hPartition/rna_datasets/flu/aln/flu_H1N1pdm09.fasta > flu_H1N1pdm09.fasta   # PsiPartition only recognises uppercase ACGT
export PYTHONUNBUFFERED=1 WANDB_MODE=disabled
/usr/bin/time -v -o /home/diepht/sliferskyd/hPartition/rerun_sim/out_rna/PsiPartition/flu_H1N1pdm09/time.txt /home/diepht/miniconda3/envs/PsiPartition/bin/python -W ignore /home/diepht/sliferskyd/hPartition/rerun_sim/bin/psi_local.py --msa /home/diepht/sliferskyd/hPartition/rerun_sim/out_rna/PsiPartition/flu_H1N1pdm09/flu_H1N1pdm09.fasta --format fasta --alphabet dna --max_partitions 30 --n_iter 30 --seed 0 >> /home/diepht/sliferskyd/hPartition/rerun_sim/out_rna/PsiPartition/flu_H1N1pdm09/cmd.log 2>&1
test -s /home/diepht/sliferskyd/hPartition/rerun_sim/out_rna/PsiPartition/flu_H1N1pdm09/final.nwk && test -s /home/diepht/sliferskyd/hPartition/rerun_sim/out_rna/PsiPartition/flu_H1N1pdm09/last.nwk
