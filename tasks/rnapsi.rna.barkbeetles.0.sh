set -e
mkdir -p /home/diepht/sliferskyd/hPartition/rerun_sim/out_rna/PsiPartition/barkbeetles; cd /home/diepht/sliferskyd/hPartition/rerun_sim/out_rna/PsiPartition/barkbeetles
[ -e barkbeetles.fasta ] || tr a-z A-Z < /home/diepht/sliferskyd/hPartition/rna_datasets/pf/aln/barkbeetles.fasta > barkbeetles.fasta   # PsiPartition only recognises uppercase ACGT
export PYTHONUNBUFFERED=1 WANDB_MODE=disabled
/usr/bin/time -v -o /home/diepht/sliferskyd/hPartition/rerun_sim/out_rna/PsiPartition/barkbeetles/time.txt /home/diepht/miniconda3/envs/PsiPartition/bin/python -W ignore /home/diepht/sliferskyd/hPartition/rerun_sim/bin/psi_local.py --msa /home/diepht/sliferskyd/hPartition/rerun_sim/out_rna/PsiPartition/barkbeetles/barkbeetles.fasta --format fasta --alphabet dna --max_partitions 30 --n_iter 30 --seed 0  >> /home/diepht/sliferskyd/hPartition/rerun_sim/out_rna/PsiPartition/barkbeetles/cmd.log 2>&1
test -s /home/diepht/sliferskyd/hPartition/rerun_sim/out_rna/PsiPartition/barkbeetles/final.nwk && test -s /home/diepht/sliferskyd/hPartition/rerun_sim/out_rna/PsiPartition/barkbeetles/last.nwk
