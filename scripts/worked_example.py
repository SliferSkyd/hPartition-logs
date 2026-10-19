"""Compute the Stage-1 and Stage-2 numbers for the worked example in the manuscript.

Everything printed here is computed from the toy alignment with the same formulae the implementation uses,
so the example in the paper reports real arithmetic rather than illustrative values.
"""
from itertools import combinations

TAXA = ['t1', 't2', 't3', 't4', 't5', 't6']
#        123456789...                     site classes: 1-6 invariant, 7-11 slow, 12-16 fast
ALN = {
    't1': 'ACGTAC' 'AAACC' 'ACGTA',
    't2': 'ACGTAC' 'AAACC' 'CGTAC',
    't3': 'ACGTAC' 'AAGCC' 'GTACG',
    't4': 'ACGTAC' 'AGACC' 'TACGT',
    't5': 'ACGTAC' 'AAACT' 'ACGTA',
    't6': 'ACGTAC' 'AAACT' 'CGTAC',
}
m = len(ALN['t1'])

# sim(x, y) = number of matching characters between sequences x and y
sim = {(x, y): sum(a == b for a, b in zip(ALN[x], ALN[y])) for x, y in combinations(TAXA, 2)}
denom = sum(sim.values())

rates = []
for i in range(m):
    num = sum(s for (x, y), s in sim.items() if ALN[x][i] == ALN[y][i])
    rates.append(1 - num / denom)

print(f'alignment: {len(TAXA)} taxa x {m} sites;  sum of sim(x,y) over all pairs = {denom}\n')
print('pairwise sim(x,y):')
for (x, y), s in sim.items():
    print(f'   sim({x},{y}) = {s}', end='')
print('\n')
print(f"{'site':>5}{'column':>9}{'matching-pair sum':>20}{'r_i':>9}  class")
for i, r in enumerate(rates, 1):
    col = ''.join(ALN[t][i - 1] for t in TAXA)
    num = sum(s for (x, y), s in sim.items() if ALN[x][i - 1] == ALN[y][i - 1])
    cls = 'invariant' if r == 0 else ('slow' if r < 0.5 else 'fast')
    print(f'{i:>5}{col:>9}{num:>20}{r:>9.3f}  {cls}')

k0 = 4                                  # illustrative: the implementation uses ceil(m/100)
lo, hi = min(rates), max(rates)
w = (hi - lo) / k0
print(f'\nStage 2 with k0 = {k0} (illustrative; implementation uses ceil(m/100) = {-(-m//100)}):')
print(f'   rate range [{lo:.3f}, {hi:.3f}], bin width {w:.3f}')
bins = {j: [] for j in range(1, k0 + 1)}
for i, r in enumerate(rates, 1):
    j = min(k0, int((r - lo) / w) + 1) if w > 0 else 1
    bins[j].append(i)
for j, v in bins.items():
    a, b = lo + (j - 1) * w, lo + j * w
    print(f'   S{j}: [{a:.3f}, {b:.3f})  sites {v}  (n={len(v)})')
