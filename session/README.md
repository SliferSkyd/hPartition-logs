# Session backup

`STATE.md` — what the work is, where everything lives, what is decided and what is open.
Read this first; it is written to be enough on its own.

`session-1841f9c7.jsonl.gz` — the full Claude Code transcript, 2026-10-15 to 2026-10-20,
8,740 messages.

## Resuming

On the original machine:

```bash
cd /home/diepht/sliferskyd/hPartition
claude --resume 1841f9c7-ff4e-4032-9c4c-3cc4ce587094
```

Elsewhere, restore the transcript first so the session is visible to the CLI:

```bash
mkdir -p ~/.claude/projects/-work-backup-home-diepht-sliferskyd-hPartition
gunzip -c session-1841f9c7.jsonl.gz \
  > ~/.claude/projects/-work-backup-home-diepht-sliferskyd-hPartition/1841f9c7-ff4e-4032-9c4c-3cc4ce587094.jsonl
```

The project directory is keyed to the working-directory path, so the same layout
(`/work/backup/home/diepht/sliferskyd/hPartition`) has to exist for `--resume` to find it.
Failing that, read the file directly: one JSON object per line, `type` is `user` or `assistant`,
and `message.content` holds the text.

## Reading it without the CLI

```bash
gunzip -c session-1841f9c7.jsonl.gz | python3 -c '
import json,sys
for line in sys.stdin:
    try: d=json.loads(line)
    except: continue
    if d.get("type") not in ("user","assistant"): continue
    c=d.get("message",{}).get("content")
    if isinstance(c,list): c="".join(x.get("text","") for x in c if isinstance(x,dict))
    if isinstance(c,str) and c.strip():
        print(f"--- {d[\"type\"]} {d.get(\"timestamp\",\"\")}\n{c}\n")
' | less
```

The transcript is a working record, not a result. Where it disagrees with `STATE.md`, trust
`STATE.md`: several conclusions in the transcript were later corrected.
