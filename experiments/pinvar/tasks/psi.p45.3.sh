#!/bin/bash
unset LD_LIBRARY_PATH
set -e
mkdir -p /home/diepht/sliferskyd/hPartition/rerun_sim/pinvar/out/psi.p45.3/PsiPartition /home/diepht/sliferskyd/hPartition/rerun_sim/pinvar/out/psi.p45.3/partition
cd /home/diepht/sliferskyd/hPartition/rerun_sim/pinvar/out/psi.p45.3/PsiPartition
[ -e 3.fasta ] || cp /home/diepht/sliferskyd/hPartition/rerun_sim/pinvar/data/p45/3.fasta 3.fasta
export PYTHONUNBUFFERED=1 WANDB_MODE=disabled
/usr/bin/time -v -o /home/diepht/sliferskyd/hPartition/rerun_sim/pinvar/out/psi.p45.3/PsiPartition/time.txt /home/diepht/miniconda3/envs/PsiPartition/bin/python -W ignore /home/diepht/sliferskyd/hPartition/rerun_sim/bin/psi_local.py --msa /home/diepht/sliferskyd/hPartition/rerun_sim/pinvar/out/psi.p45.3/PsiPartition/3.fasta --format fasta --alphabet dna --max_partitions 30 --n_iter 30 --seed 0 >> /home/diepht/sliferskyd/hPartition/rerun_sim/pinvar/out/psi.p45.3/PsiPartition/cmd.log 2>&1
/home/diepht/sliferskyd/hPartition/rerun_sim/bin/eval_iqtree.sh /home/diepht/sliferskyd/hPartition/rerun_sim/pinvar/data/p45/3.phy /home/diepht/sliferskyd/hPartition/rerun_sim/pinvar/out/psi.p45.3/PsiPartition/3.final.parts /home/diepht/sliferskyd/hPartition/rerun_sim/pinvar/out/psi.p45.3/partition 1
test -s /home/diepht/sliferskyd/hPartition/rerun_sim/pinvar/out/psi.p45.3/partition/aln.treefile
