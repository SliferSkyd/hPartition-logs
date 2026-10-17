set -e
mkdir -p /home/diepht/sliferskyd/hPartition/rerun_sim/out_rna/PsiPartition/mumps; cd /home/diepht/sliferskyd/hPartition/rerun_sim/out_rna/PsiPartition/mumps
[ -e mumps.fasta ] || cp /home/diepht/sliferskyd/hPartition/rna_datasets/aln/mumps.fasta mumps.fasta
export PYTHONUNBUFFERED=1 WANDB_MODE=disabled
/usr/bin/time -v -o /home/diepht/sliferskyd/hPartition/rerun_sim/out_rna/PsiPartition/mumps/time.txt /home/diepht/miniconda3/envs/PsiPartition/bin/python -W ignore /home/diepht/sliferskyd/hPartition/rerun_sim/bin/psi_local.py --msa /home/diepht/sliferskyd/hPartition/rerun_sim/out_rna/PsiPartition/mumps/mumps.fasta --format fasta --alphabet dna --max_partitions 30 --n_iter 30 --seed 0 >> /home/diepht/sliferskyd/hPartition/rerun_sim/out_rna/PsiPartition/mumps/cmd.log 2>&1
test -s /home/diepht/sliferskyd/hPartition/rerun_sim/out_rna/PsiPartition/mumps/final.nwk && test -s /home/diepht/sliferskyd/hPartition/rerun_sim/out_rna/PsiPartition/mumps/last.nwk
