#!/bin/bash
# Rubella / HCV-1b / HIV-1B: select (base, 50, 100 genomes), MAFFT G-INS-1, trimAl -gappyout, UPPERCASE, PHYLIP
set -e
B=/home/diepht/miniconda3/envs/rnaaln/bin
cd /home/diepht/sliferskyd/hPartition/rna_datasets
VIRUSES=rubella,hcv1b,hiv1b /home/diepht/anaconda3/bin/python -I scripts/select_genomes.py 50 100
T=${SLURM_CPUS_PER_TASK:-1}
for v in rubella hcv1b hiv1b rubella_n50 hcv1b_n50 hiv1b_n50 rubella_n100 hcv1b_n100 hiv1b_n100; do
  s=$(date +%s)
  $B/mafft --globalpair --thread $T --quiet sel/$v.fasta > aln/$v.mafft.fasta 2> logs/$v.mafft.log
  $B/trimal -in aln/$v.mafft.fasta -out aln/$v.trim.fasta -gappyout -fasta
  awk '/^>/{print; next} {print toupper($0)}' aln/$v.trim.fasta > aln/$v.fasta && rm aln/$v.trim.fasta
  /home/diepht/anaconda3/bin/python -I -c "
s={};n=None
for l in open('aln/$v.fasta'):
    l=l.strip()
    if l.startswith('>'): n=l[1:].split()[0]; s[n]=[]
    elif n: s[n].append(l)
s={k:''.join(x) for k,x in s.items()}; L={len(x) for x in s.values()}; assert len(L)==1
open('aln/$v.phy','w').write(f'{len(s)} {L.pop()}\n'+''.join(f'{k} {x}\n' for k,x in s.items()))"
  echo "$v done in $(( $(date +%s)-s ))s: $(head -1 aln/$v.phy)"
done
