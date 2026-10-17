set -e
mkdir -p /home/diepht/sliferskyd/hPartition/rerun_sim/out_rna/PsiPartition/rabies; cd /home/diepht/sliferskyd/hPartition/rerun_sim/out_rna/PsiPartition/rabies
[ -e rabies.fasta ] || cp /home/diepht/sliferskyd/hPartition/rna_datasets/aln/rabies.fasta rabies.fasta
export PYTHONUNBUFFERED=1 WANDB_MODE=disabled
/usr/bin/time -v -o /home/diepht/sliferskyd/hPartition/rerun_sim/out_rna/PsiPartition/rabies/time.txt /home/diepht/miniconda3/envs/PsiPartition/bin/python -W ignore /home/diepht/sliferskyd/hPartition/rerun_sim/bin/psi_local.py --msa /home/diepht/sliferskyd/hPartition/rerun_sim/out_rna/PsiPartition/rabies/rabies.fasta --format fasta --alphabet dna --max_partitions 30 --n_iter 30 --seed 0 >> /home/diepht/sliferskyd/hPartition/rerun_sim/out_rna/PsiPartition/rabies/cmd.log 2>&1
test -s /home/diepht/sliferskyd/hPartition/rerun_sim/out_rna/PsiPartition/rabies/final.nwk && test -s /home/diepht/sliferskyd/hPartition/rerun_sim/out_rna/PsiPartition/rabies/last.nwk
