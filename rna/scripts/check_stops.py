import re, sys
from pathlib import Path
from Bio.Seq import Seq
D = Path('/home/diepht/sliferskyd/hPartition/rna_datasets/beetle/aln')
PCG = ['atp6','atp8','cox1','cox2','cox3','cob','nad1','nad2','nad3','nad4','nad4l','nad5','nad6']
cs = {m[0]: (int(m[1]), int(m[2])) for m in re.findall(r'charset (\S+) = (\d+)-(\d+);', (D/'beetle.genes.nex').read_text())}
seqs, cur = {}, None
for line in (D/sys.argv[1]).read_text().splitlines():
    if line.startswith('>'): cur = line[1:].strip(); seqs[cur]=''
    elif cur: seqs[cur]+=line.strip()
bad = 0
for g in PCG:
    a,b = cs[g]
    for t,s in seqs.items():
        nt = s[a-1:b].replace('-','')
        if len(nt) < 30: continue
        p = str(Seq(nt[:len(nt)//3*3]).translate(table=5)).rstrip('*')
        if '*' in p:
            print(f'  {t} {g}: {p.count("*")} internal stops'); bad += 1
print(f'{sys.argv[1]}: {len(seqs)} taxa, {bad} sequences with internal stops')
