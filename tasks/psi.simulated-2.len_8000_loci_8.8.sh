set -e
mkdir -p /home/diepht/sliferskyd/hPartition/rerun_sim/out/PsiPartition/simulated-2/len_8000_loci_8/8; cd /home/diepht/sliferskyd/hPartition/rerun_sim/out/PsiPartition/simulated-2/len_8000_loci_8/8
[ -e 8.fasta ] || cp /home/diepht/sliferskyd/hPartition-datasets/DNA/simulated-2/len_8000_loci_8/8.fasta 8.fasta
export PYTHONUNBUFFERED=1 WANDB_MODE=disabled
/usr/bin/time -v -o /home/diepht/sliferskyd/hPartition/rerun_sim/out/PsiPartition/simulated-2/len_8000_loci_8/8/time.txt /home/diepht/miniconda3/envs/PsiPartition/bin/python -W ignore /home/diepht/sliferskyd/hPartition/rerun_sim/bin/psi_local.py --msa /home/diepht/sliferskyd/hPartition/rerun_sim/out/PsiPartition/simulated-2/len_8000_loci_8/8/8.fasta --format fasta --alphabet dna --max_partitions 30 --n_iter 30 --seed 0 >> /home/diepht/sliferskyd/hPartition/rerun_sim/out/PsiPartition/simulated-2/len_8000_loci_8/8/cmd.log 2>&1
test -s /home/diepht/sliferskyd/hPartition/rerun_sim/out/PsiPartition/simulated-2/len_8000_loci_8/8/final.nwk && test -s /home/diepht/sliferskyd/hPartition/rerun_sim/out/PsiPartition/simulated-2/len_8000_loci_8/8/last.nwk
