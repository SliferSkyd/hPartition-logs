set -e
mkdir -p /home/diepht/sliferskyd/hPartition/rerun_sim/out/PsiPartition/simulated-2/len_10000_loci_10/5; cd /home/diepht/sliferskyd/hPartition/rerun_sim/out/PsiPartition/simulated-2/len_10000_loci_10/5
[ -e 5.fasta ] || cp /home/diepht/sliferskyd/hPartition-datasets/DNA/simulated-2/len_10000_loci_10/5.fasta 5.fasta
export PYTHONUNBUFFERED=1 WANDB_MODE=disabled
/usr/bin/time -v -o /home/diepht/sliferskyd/hPartition/rerun_sim/out/PsiPartition/simulated-2/len_10000_loci_10/5/time.txt /home/diepht/miniconda3/envs/PsiPartition/bin/python -W ignore /home/diepht/sliferskyd/hPartition/rerun_sim/bin/psi_local.py --msa /home/diepht/sliferskyd/hPartition/rerun_sim/out/PsiPartition/simulated-2/len_10000_loci_10/5/5.fasta --format fasta --alphabet dna --max_partitions 30 --n_iter 30 --seed 0 >> /home/diepht/sliferskyd/hPartition/rerun_sim/out/PsiPartition/simulated-2/len_10000_loci_10/5/cmd.log 2>&1
test -s /home/diepht/sliferskyd/hPartition/rerun_sim/out/PsiPartition/simulated-2/len_10000_loci_10/5/final.nwk && test -s /home/diepht/sliferskyd/hPartition/rerun_sim/out/PsiPartition/simulated-2/len_10000_loci_10/5/last.nwk
