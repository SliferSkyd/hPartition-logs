#!/bin/bash
# Taxon-scaling sets: MAFFT G-INS-1 + trimAl -gappyout (same as align.sh), multi-threaded; PHYLIP in "N L"/"name seq" form
B=/home/diepht/miniconda3/envs/rnaaln/bin
cd /home/diepht/sliferskyd/hPartition/rna_datasets
T=${SLURM_CPUS_PER_TASK:-1}
for v in ${SETS:-mumps_n50 measles_n50 mumps_n100 measles_n100}; do
  s=$(date +%s)
  $B/mafft --globalpair --thread $T --quiet sel/$v.fasta > aln/$v.mafft.fasta 2> logs/$v.mafft.log
  $B/trimal -in aln/$v.mafft.fasta -out aln/$v.fasta -gappyout -fasta
  /home/diepht/anaconda3/bin/python -I -c "
import sys
s={};n=None
for l in open('aln/$v.fasta'):
    l=l.strip()
    if l.startswith('>'): n=l[1:].split()[0]; s[n]=[]
    elif n: s[n].append(l)
s={k:''.join(x) for k,x in s.items()}; L={len(x) for x in s.values()}; assert len(L)==1
open('aln/$v.phy','w').write(f'{len(s)} {L.pop()}\n'+''.join(f'{k} {x}\n' for k,x in s.items()))"
  echo "$v done in $(( $(date +%s)-s ))s"
done
