set -e
mkdir -p /home/diepht/sliferskyd/hPartition/rerun_sim/out/PsiPartition/simulated-2/len_15000_loci_15/6; cd /home/diepht/sliferskyd/hPartition/rerun_sim/out/PsiPartition/simulated-2/len_15000_loci_15/6
[ -e 6.fasta ] || cp /home/diepht/sliferskyd/hPartition-datasets/DNA/simulated-2/len_15000_loci_15/6.fasta 6.fasta
export PYTHONUNBUFFERED=1 WANDB_MODE=disabled
/usr/bin/time -v -o /home/diepht/sliferskyd/hPartition/rerun_sim/out/PsiPartition/simulated-2/len_15000_loci_15/6/time.txt /home/diepht/miniconda3/envs/PsiPartition/bin/python -W ignore /home/diepht/sliferskyd/hPartition/rerun_sim/bin/psi_local.py --msa /home/diepht/sliferskyd/hPartition/rerun_sim/out/PsiPartition/simulated-2/len_15000_loci_15/6/6.fasta --format fasta --alphabet dna --max_partitions 30 --n_iter 30 --seed 0 >> /home/diepht/sliferskyd/hPartition/rerun_sim/out/PsiPartition/simulated-2/len_15000_loci_15/6/cmd.log 2>&1
test -s /home/diepht/sliferskyd/hPartition/rerun_sim/out/PsiPartition/simulated-2/len_15000_loci_15/6/final.nwk && test -s /home/diepht/sliferskyd/hPartition/rerun_sim/out/PsiPartition/simulated-2/len_15000_loci_15/6/last.nwk
