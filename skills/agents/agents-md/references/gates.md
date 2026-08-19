# Gates

Apply in order to every candidate fact.

## Gate 1 — exist

A fact earns an always-loaded line only when all five hold:

1. **Universal** — true for every kind of session in this repo.
2. **Non-discoverable** — not a one-file lookup in code, config, or the tree. Cite the source before `CUT (discoverable)`. No citation → `KEEP` or `ASK`.
3. **Non-rotting** — no pin to a symbol or line that moves when code changes.
4. **Stable fact** — not a preference or a multi-step procedure.
5. **Load-bearing** — drop it and the next session makes a mistake it cannot recover from.

Nothing passes and no `--force` → create nothing. Ground rules alone do not create the files.

A no-op (the model already does this) is a `CUT`. Same meaning already in a tracked Project skill that starts when the line would have mattered is a `CUT` — see [`writes.md`](writes.md). Global-only skills never justify a `CUT`.

## Gate 2 — place

See [`placement.md`](placement.md). Always-needed vs situational, not short vs long.

## Gate 3 — express

Fewest tokens that keep the meaning. Load `writing-for-agents` when it is reachable; otherwise apply this bar:

- One meaning, one place. Point; do not copy.
- Imperatives and fragments. Drop “you should” / “remember to”.
- A pointer is `read when <situation>`. Situation is the class of work. Completeness test in [`placement.md`](placement.md).
- Correctness beats brevity. A load-bearing qualifier stays.

Relocating prose into `agents.d/` without shrinking it is a failed run.
