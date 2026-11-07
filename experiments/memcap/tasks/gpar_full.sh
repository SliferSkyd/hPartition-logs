#!/bin/bash
unset LD_LIBRARY_PATH
O=/home/diepht/sliferskyd/hPartition/rerun_sim/memcap/out/gpar_mem
/home/diepht/anaconda3/bin/python -I - <<'PY' > $O/gpar_full.txt 2>&1
import os, time
f = "/home/diepht/sliferskyd/hPartition/rerun_sim/memcap/out/Neoaves_gPar/Neoaves.phy.sitelh"
def hwm():
    for l in open("/proc/self/status"):
        if l.startswith("VmHWM"): return int(l.split()[1])/1048576
print("node:", os.uname().nodename)
t0 = time.time()
# gPartition.py:801-806, verbatim, full file
lhArr = []
with open(f) as fh:
    for rl in fh:
        lhArr.append(rl.split(" ", 1)[1].split())
print("after lhArr : %.2f GiB  (%d x %d, %.1f s)" %
      (hwm(), len(lhArr), len(lhArr[0]), time.time()-t0))
# gPartition.py:809+ : the per-site argmax pass, 1/50 sample to show it adds nothing
nOP = len(lhArr)
for siteID in range(0, len(lhArr[0]), 50):
    mx, best = -1e9, 0
    for b in range(nOP):
        v = float(lhArr[b][siteID])
        if v > mx: mx, best = v, b
print("after loop  : %.2f GiB  (%.1f s total)" % (hwm(), time.time()-t0))
# the same data as float64
print("as float64  : %.2f GiB" % (nOP*len(lhArr[0])*8/1073741824))
PY
