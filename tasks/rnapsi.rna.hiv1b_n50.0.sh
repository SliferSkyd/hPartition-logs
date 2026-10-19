set -e
mkdir -p /home/diepht/sliferskyd/hPartition/rerun_sim/out_rna/PsiPartition/hiv1b_n50; cd /home/diepht/sliferskyd/hPartition/rerun_sim/out_rna/PsiPartition/hiv1b_n50
[ -e hiv1b_n50.fasta ] || tr a-z A-Z < /home/diepht/sliferskyd/hPartition/rna_datasets/aln/hiv1b_n50.fasta > hiv1b_n50.fasta   # PsiPartition only recognises uppercase ACGT
export PYTHONUNBUFFERED=1 WANDB_MODE=disabled
/usr/bin/time -v -o /home/diepht/sliferskyd/hPartition/rerun_sim/out_rna/PsiPartition/hiv1b_n50/time.txt /home/diepht/miniconda3/envs/PsiPartition/bin/python -W ignore /home/diepht/sliferskyd/hPartition/rerun_sim/bin/psi_local.py --msa /home/diepht/sliferskyd/hPartition/rerun_sim/out_rna/PsiPartition/hiv1b_n50/hiv1b_n50.fasta --format fasta --alphabet dna --max_partitions 30 --n_iter 30 --seed 0 >> /home/diepht/sliferskyd/hPartition/rerun_sim/out_rna/PsiPartition/hiv1b_n50/cmd.log 2>&1
test -s /home/diepht/sliferskyd/hPartition/rerun_sim/out_rna/PsiPartition/hiv1b_n50/final.nwk && test -s /home/diepht/sliferskyd/hPartition/rerun_sim/out_rna/PsiPartition/hiv1b_n50/last.nwk
