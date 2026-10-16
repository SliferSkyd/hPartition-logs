#!/bin/bash
# Copy scripts, task lists, results and the essential per-run outputs/logs of the simulated-data rerun
# into the git archive, then commit. Safe to re-run while jobs are running (copies only; never moves).
# Usage: sync_archive.sh ["commit message"]
set -e
SRC=/home/diepht/sliferskyd/hPartition/rerun_sim
DST=/home/diepht/sliferskyd/hPartition/hPartition-sim-rerun
mkdir -p $DST/{scripts,tasks,results,logs,runs,patches}

rsync -a --delete $SRC/bin/ $DST/scripts/
rsync -a --delete --include='*.list' --include='*.sh' --exclude='*' $SRC/tasks/ $DST/tasks/
rsync -a --delete $SRC/results/ $DST/results/
rsync -a --delete --exclude='*.log' $SRC/done/ $DST/logs/done/            # per-task status markers
rsync -a --include='*/' --include='worker.*.out' --include='psi_test.*' --include='retry.*' --include='psi_fix.log' \
      --exclude='*' $SRC/logs/ $DST/logs/slurm/
( cd /home/diepht/sliferskyd/hPartition/gPartition && git diff ) > $DST/patches/gPartition-iqtree2.patch

# per-run essentials (only finished tasks, so the archive never holds half-written runs)
for ok in $SRC/done/*.ok; do
  t=$(basename $ok .ok); IFS=. read -r tag sim cat rep <<<"$t"
  case $tag in
    hpar) m=hPartition; keep=(hPartition/aln.partitions hPartition/aln.log hPartition/time.txt
            partition/aln.iqtree partition/aln.treefile partition/aln.log partition/time.txt
            partition/NORATE_FALLBACK partition/crashed_with_R/aln.log) ;;
    gpar) m=gPartition; keep=(gPartition/$rep.phy.FINAL.nex gPartition/time.txt gPartition/cmd.log
            partition/aln.iqtree partition/aln.treefile partition/aln.log partition/time.txt
            partition/NORATE_FALLBACK partition/crashed_with_R/aln.log) ;;
    psi)  m=PsiPartition; keep=($rep.csv $rep.iters.tsv last.nwk final.nwk $rep.last.iqtree $rep.final.iqtree
            $rep.last.parts $rep.final.parts time.txt NORATE_FALLBACK) ;;
  esac
  s=$SRC/out/$m/$sim/$cat/$rep; d=$DST/runs/$m/$sim/$cat/$rep
  [ -e $d/.synced ] && [ $d/.synced -nt $ok ] && continue
  mkdir -p $d
  for f in "${keep[@]}"; do
    [ -e $s/$f ] || continue
    mkdir -p $(dirname $d/$f)
    if [ $tag = gpar ] && [ $(basename $f) = cmd.log ]; then gzip -c $s/$f > $d/$f.gz
    else cp -p $s/$f $d/$f; fi
  done
  # Psi cmd.log is ~10 MB of tqdm progress bars: keep only the per-iteration summary lines
  [ $tag = psi ] && tr '\r' '\n' < $s/cmd.log | grep -E '^(iter|final) ' > $d/iterations.log || true
  cp $ok $d/status.txt
  touch $d/.synced
done

cd $DST
[ -d .git ] || git init -q
git add -A
if ! git diff --cached --quiet; then
  git commit -q -m "${1:-Sync simulated rerun results ($(ls $SRC/done | grep -c 'ok$') tasks done)}" \
    -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
  git log --oneline -1
else
  echo "nothing new to commit"
fi
