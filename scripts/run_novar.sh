#!/bin/bash
# Wait for the variant-only-seeding build, then run the eight small DNA datasets through it.
BIN=/home/diepht/sliferskyd/hPartition/iqtree2-novar/build/iqtree2
for i in $(seq 1 180); do [ -x $BIN ] && break; sleep 20; done
[ -x $BIN ] || { echo "build never finished"; exit 1; }
echo "binary ready: $(ls -la $BIN | awk '{print $5}') bytes"
exec /home/diepht/sliferskyd/hPartition/rerun_sim/bin/worker.sh novar
