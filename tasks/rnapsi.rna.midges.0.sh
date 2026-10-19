set -e
mkdir -p /home/diepht/sliferskyd/hPartition/rerun_sim/out_rna/PsiPartition/midges; cd /home/diepht/sliferskyd/hPartition/rerun_sim/out_rna/PsiPartition/midges
[ -e midges.fasta ] || tr a-z A-Z < /home/diepht/sliferskyd/hPartition/rna_datasets/pf/aln/midges.fasta > midges.fasta   # PsiPartition only recognises uppercase ACGT
export PYTHONUNBUFFERED=1 WANDB_MODE=disabled
/usr/bin/time -v -o /home/diepht/sliferskyd/hPartition/rerun_sim/out_rna/PsiPartition/midges/time.txt /home/diepht/miniconda3/envs/PsiPartition/bin/python -W ignore /home/diepht/sliferskyd/hPartition/rerun_sim/bin/psi_local.py --msa /home/diepht/sliferskyd/hPartition/rerun_sim/out_rna/PsiPartition/midges/midges.fasta --format fasta --alphabet dna --max_partitions 30 --n_iter 30 --seed 0  >> /home/diepht/sliferskyd/hPartition/rerun_sim/out_rna/PsiPartition/midges/cmd.log 2>&1
test -s /home/diepht/sliferskyd/hPartition/rerun_sim/out_rna/PsiPartition/midges/final.nwk && test -s /home/diepht/sliferskyd/hPartition/rerun_sim/out_rna/PsiPartition/midges/last.nwk
