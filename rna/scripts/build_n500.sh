#!/bin/bash
# Taxon-scaling to 500: same selection rules and aligner as the n50/n100 sets, so the only thing that
# changes along the ladder is the number of taxa. Reports the constant-site fraction at the end.
set -e
B=/home/diepht/miniconda3/envs/rnaaln/bin
R=/home/diepht/sliferskyd/hPartition/rna_datasets
cd $R
T=${SLURM_CPUS_PER_TASK:-1}
VIRUSES=rabies,denv1 /home/diepht/anaconda3/bin/python -I scripts/select_genomes.py 500
for v in rabies_n500 denv1_n500; do
  s=$(date +%s)
  $B/mafft --globalpair --thread $T --quiet sel/$v.fasta > aln/$v.mafft.fasta 2> logs/$v.mafft.log
  $B/trimal -in aln/$v.mafft.fasta -out aln/$v.fasta -gappyout -fasta
  /home/diepht/anaconda3/bin/python -I -c "
s={};n=None
for l in open('aln/$v.fasta'):
    l=l.strip()
    if l.startswith('>'): n=l[1:].split()[0]; s[n]=[]
    elif n: s[n].append(l)
s={k:''.join(x) for k,x in s.items()}; L={len(x) for x in s.values()}; assert len(L)==1
open('aln/$v.phy','w').write(f'{len(s)} {L.pop()}\n'+''.join(f'{k} {x}\n' for k,x in s.items()))"
  echo "$v aligned in $(( $(date +%s)-s ))s"
done
echo
echo "=== constant-site fraction along the ladder ==="
/home/diepht/anaconda3/bin/python -I -c "
from pathlib import Path
def cf(p):
    s,c={},None
    for l in open(p):
        if l[0]=='>': c=l[1:].strip(); s[c]=[]
        else: s[c].append(l.strip())
    rows=[''.join(v).upper() for v in s.values()]
    cols=list(zip(*rows))
    return len(rows), len(cols), sum(len(set(x)-set('-N?'))<=1 for x in cols)/len(cols)
print(f'{\"dataset\":<14}{\"taxa\":>6}{\"sites\":>8}{\"const%\":>9}')
for v in ['rabies','rabies_n50','rabies_n100','rabies_n500','denv1','denv1_n50','denv1_n100','denv1_n500']:
    p=Path('aln')/f'{v}.fasta'
    if p.exists():
        t,L,c=cf(p); print(f'{v:<14}{t:>6}{L:>8}{c:>9.1%}')
"
