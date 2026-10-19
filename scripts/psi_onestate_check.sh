#!/bin/bash
unset LD_LIBRARY_PATH
cd /home/diepht/sliferskyd/hPartition/rerun_sim
PY=/home/diepht/miniconda3/envs/PsiPartition/bin/python
U=/tmp/psi_check_$SLURM_JOB_ID; mkdir -p $U
for v in ${CHECK_SETS:-measles mumps rabies denv1 zika rabies_n50 denv1_n50 rabies_n100 denv1_n100}; do
  tr a-z A-Z < ${CHECK_ALN:-/home/diepht/sliferskyd/hPartition/rna_datasets/aln}/$v.fasta > $U/$v.fasta; echo $v
done | xargs -P ${SLURM_CPUS_PER_TASK:-1} -I{} sh -c "$PY -W ignore bin/psi_onestate_check.py $U/{}.fasta 2>/dev/null > results/rna/onestate_{}.tsv"
rm -rf $U
