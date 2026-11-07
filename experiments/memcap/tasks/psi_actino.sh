#!/bin/bash
# Reproduce PsiPartition's failure on the smallest alignment it failed on (Actinopterygii,
# 149,366 sites) under the 10 GB allocation the paper describes. The question is not WHETHER
# it fails but HOW: a numpy MemoryError (a software error, with a traceback) or an OOM kill.
unset LD_LIBRARY_PATH
R=/home/diepht/sliferskyd/hPartition
O=$R/rerun_sim/memcap/out/Actinopterygii_Psi
PY=/home/diepht/miniconda3/envs/PsiPartition/bin/python
cd $O
$PY -c "
from Bio import AlignIO
AlignIO.convert('/home/diepht/sliferskyd/hPartition-datasets/DNA/empirical/Actinopterygii.phy',
                'phylip-relaxed', '$O/Actinopterygii.fasta', 'fasta')
print('converted ok')
" > $O/convert.log 2>&1
echo "--- vm.overcommit_memory = $(cat /proc/sys/vm/overcommit_memory) ---" > $O/cmd.log
echo "--- node: $(hostname), MemTotal $(awk '/MemTotal/{print $2}' /proc/meminfo) kB ---" >> $O/cmd.log
export PYTHONUNBUFFERED=1 WANDB_MODE=disabled
/usr/bin/time -v -o $O/time.txt $PY -W ignore $R/rerun_sim/bin/psi_local.py \
  --msa $O/Actinopterygii.fasta --format fasta --alphabet dna \
  --max_partitions 30 --n_iter 30 --seed 0 >> $O/cmd.log 2>&1
echo "python exit=$?" >> $O/cmd.log
