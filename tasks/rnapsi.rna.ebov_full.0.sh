set -e
mkdir -p /home/diepht/sliferskyd/hPartition/rerun_sim/out_rna/PsiPartition/ebov_full; cd /home/diepht/sliferskyd/hPartition/rerun_sim/out_rna/PsiPartition/ebov_full
[ -e ebov_full.fasta ] || tr a-z A-Z < /home/diepht/sliferskyd/hPartition/rna_datasets/full/aln/ebov_full.fasta > ebov_full.fasta   # PsiPartition only recognises uppercase ACGT
export PYTHONUNBUFFERED=1 WANDB_MODE=disabled
/usr/bin/time -v -o /home/diepht/sliferskyd/hPartition/rerun_sim/out_rna/PsiPartition/ebov_full/time.txt /home/diepht/miniconda3/envs/PsiPartition/bin/python -W ignore /home/diepht/sliferskyd/hPartition/rerun_sim/bin/psi_local.py --msa /home/diepht/sliferskyd/hPartition/rerun_sim/out_rna/PsiPartition/ebov_full/ebov_full.fasta --format fasta --alphabet dna --max_partitions 30 --n_iter 30 --seed 0 --max_hours 120 >> /home/diepht/sliferskyd/hPartition/rerun_sim/out_rna/PsiPartition/ebov_full/cmd.log 2>&1
test -s /home/diepht/sliferskyd/hPartition/rerun_sim/out_rna/PsiPartition/ebov_full/final.nwk && test -s /home/diepht/sliferskyd/hPartition/rerun_sim/out_rna/PsiPartition/ebov_full/last.nwk
