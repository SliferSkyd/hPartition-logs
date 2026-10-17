#!/bin/bash
# MAFFT G-INS-1 (as Patino-Galindo et al. 2018) + trimAl -gappyout; outputs aln/<virus>.{fasta,phy}
B=/home/diepht/miniconda3/envs/rnaaln/bin
cd /home/diepht/sliferskyd/hPartition/rna_datasets
for v in denv1 zika rabies mumps measles; do
  s=$(date +%s)
  $B/mafft --globalpair --thread 1 --quiet sel/$v.fasta > aln/$v.mafft.fasta 2> logs/$v.mafft.log
  $B/trimal -in aln/$v.mafft.fasta -out aln/$v.fasta -gappyout -fasta
  $B/trimal -in aln/$v.fasta -out aln/$v.phy -phylip
  echo "$v done in $(( $(date +%s)-s ))s"
done
