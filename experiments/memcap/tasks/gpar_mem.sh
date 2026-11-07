#!/bin/bash
unset LD_LIBRARY_PATH
O=/home/diepht/sliferskyd/hPartition/rerun_sim/memcap/out/gpar_mem
/home/diepht/anaconda3/bin/python -I - <<'PY' > $O/gpar_mem.txt 2>&1
import os, sys
f = "/home/diepht/sliferskyd/hPartition/rerun_sim/memcap/out/Neoaves_gPar/Neoaves.phy.sitelh"
def rss():
    for l in open("/proc/self/status"):
        if l.startswith("VmHWM"): return int(l.split()[1])
r0 = rss()
# exactly gPartition's loop, truncated to N lines
N = 20
lhArr = []
with open(f) as fh:
    for i, rl in enumerate(fh):
        if i >= N: break
        rl = rl.split(" ", 1)[1]
        lhArr.append(rl.split())
r1 = rss()
ntok = sum(len(x) for x in lhArr)
print("node:", os.uname().nodename)
print("lines read:", len(lhArr), "tokens:", ntok)
print("VmHWM before: %.3f GiB" % (r0/1048576))
print("VmHWM after : %.3f GiB" % (r1/1048576))
print("bytes/token : %.1f" % ((r1-r0)*1024/ntok))
print("getsizeof('-1.83031') =", sys.getsizeof("-1.83031"))
print("--> full 286 lines would need: %.2f GiB" % ((r1-r0)*286/N/1048576))
PY
