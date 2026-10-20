#!/bin/bash
R=/home/diepht/sliferskyd/hPartition/rerun_sim
for ds in Morpho Choreutidae; do $R/bin/diffuse_run.sh $ds; done
