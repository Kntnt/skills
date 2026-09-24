# Focused behavioural regression for #401 — plan

Frozen on 2026-09-24, before the first run below. Nothing in this file, in [`redline-turn.md`](redline-turn.md), in [`wave-session.md`](wave-session.md) or in [`dispatch/`](dispatch/) is edited after the first run; [`README.md`](README.md) and `runs/` are written as the work produces them. This packet is governed by [`../README.md`](../README.md) and not by the corpus protocol or its `records/` format.

## What is under test

A correction subagent that Redline started for a round wrote its candidate to a fixed name in the scratchpad its session shared with a concurrent run on the same input. That run wrote the same name, and the subagent deleted the other run's repair as its own stale copy ([#401](https://github.com/Kntnt/skills/issues/401), found in `../../editorial-383/runs/pre-column-sv-r2/response.md`). Both correction briefs, `skills/editorial/redline/references/correction.md` and `skills/editorial/unslop/references/correction.md`, now carry one paragraph, headed **Your own working files.**, below their `---` line and immediately before **What you return.**, byte-identical in both. It says that any file the subagent writes for its own working purposes goes in a directory it created for this one round and removes before it returns, including on failure; that a fixed name under a shared temporary directory is not that; and why, in the failure's own terms.

Product under test: commit `01ee82a0`, which is the fix. Only Redline is run, because only a Redline run reached the collision; Unslop's brief carries the same paragraph and is not measured here.

## The install

Staged with `git archive` from `01ee82a0`, side by side, at `/Users/thomas/Projects/skills/.git/kntnt-orchestrate/401.scratch/install-post`, outside the scratchpad the wave lists:

```text
git archive 01ee82a0 skills/editorial/write skills/editorial/redline skills/editorial/proofread skills/editorial/unslop | tar -x -C <install> --strip-components=2
git archive 01ee82a0 skills/kntnt | tar -x -C <install> --strip-components=1
```

The shim finds the Manager at the Skill directory's parent, so `<install>` holds `kntnt/`, `redline/`, `proofread/`, `unslop/` and `write/`. The wave session runs with `PYTHONDONTWRITEBYTECODE=1`, so that no `__pycache__` appears in it.

## The turn and the dispatch message

[`redline-turn.md`](redline-turn.md) is `../../editorial-383/redline-turn-post.md` with path substitutions only: the staged `SKILL.md` path and `$HERE` point at the install above, and the sentence naming what a run may not read now names `/Users/thomas/Projects/skills` alone — the repository whose worktree `/Users/thomas/Projects/skills/.git/kntnt-orchestrate/401` this ticket is built in, and under which the install and every run directory lie — and allows each run its own run directory beside that install. The scratch sentence and the `response.md` sentence are kept exactly. Nothing about scratch files, collisions or this ticket is added.

The message that starts each run is in [`dispatch/`](dispatch/), one file per run: the turn's body under its heading, then the run's working directory, the invocation and its run directory. The turn is carried in the message rather than named by path, so that a run has no reason to open this packet.

## The wave session

The five runs are not started from the builder's session, which is itself a subagent in `/orchestrate` and shares its scratchpad with its parent and its siblings. The builder starts one separate session, the *wave session*:

```text
claude --print --model=claude-opus-5-5 --effort=high --dangerously-skip-permissions --session-id=<uuid> --output-format=stream-json --verbose
```

with [`wave-session.md`](wave-session.md) on stdin, its working directory a fresh empty directory under the builder's scratch directory, and `PYTHONDONTWRITEBYTECODE=1`. Its whole job is: list its own session scratchpad as its system prompt names it into `runs/scratchpad-before.txt`, with `find <scratchpad> -type f -exec shasum -a 256 {} + | sort -k 2`; start the five run subagents in one message, each a fresh `kntnt-opus-high` subagent (`claude-opus-5-5` at high deliberation); wait for all five; list the scratchpad again into `runs/scratchpad-after.txt`; and write each run's final reply to `runs/<run>/reply.md`. It writes its scratchpad's path to `runs/scratchpad-path.txt`. Nothing else writes in that scratchpad, and every subagent it starts, and every subagent those start, shares it: that is the shared directory the collision needs. `docs/evaluation/editorial-388/harness/staged_run.py` is not used, because it gives each run its own `TMPDIR` and `HOME`, so no two runs would share a scratchpad. The wave session is not recorded with `session_cleanup.py`.

The correction subagents inherit the run's seat; the run chooses how to start them, and this packet records what each reply says of that.

## The runs

Five runs, `post-column-sv-r2-a` to `post-column-sv-r2-e`, under `runs/`, each invoked as `/redline --output=response input.md`, all five started in one message so that they run at the same time on the same input. Each run directory holds `work/input.md`, a byte copy of `../../editorial-362/runs/column-sv-r2/redline/work/input.md` (`sha256` `74b966f1352c4f42e75dc58a7f247bd42571fced8760bcf12064067b8b81de42`), and nothing else before the wave. The #383 collision happened on this input, and it reaches a correction round.

No judge is dispatched. None of `../../editorial-383/plan.md`'s criteria (`R1`, `A1`, `A2`, `N1`, `N2`, `C1`, `C2`, `O1`, `S1`) is scored and none of its controls is run. There is no pre-change arm: the criterion compares against no earlier arm.

## What counts as a collision

Read from two sources: each run's `response.md`, and the two listings of the shared scratchpad.

A run counts as colliding where its `response.md`:

- reports that a file the run or its correction subagent wrote was changed, replaced or removed by something else; or
- reports that the run or its subagent changed, replaced or removed a file it had not written.

The listings add these outcomes for the wave:

- A file in `scratchpad-before.txt` that is changed or missing in `scratchpad-after.txt` means a run destroyed work that was not its own. It counts as one colliding run.
- A new file lying directly in the scratchpad, not in a subdirectory, is the fixed-name shape that collided in #383. It counts as one colliding run even where no reply mentions it.
- A new file inside a subdirectory of the scratchpad is recorded in `README.md` as a cleanup miss. It does not count as a collision.

Every new file is named in `README.md`, together with the reply that accounts for it, if any.

A run that never started a correction subagent did not exercise the brief: its reply shows no correction round. It is recorded **not exercised**, as `../384/` records such a run, and counts neither as a pass nor as a collision. If fewer than four of the five runs are exercised, the whole wave of five is run once more, in a fresh wave session, under `runs/repeat/`; that repeat is not the revise round. A repeat wave under-exercised again is recorded **not measured**, the wording ships all the same, and the unmeasured criterion is filed `needs-triage` naming #401.

A run cut off by a usage limit, an HTTP 5xx or an overload is void and is rerun, not counted.

## The exit

- If no run counts as colliding, the wording ships.
- If one does, one revise round is allowed: the paragraph is revised, identical in both briefs, committed, and staged as a second install; a second turn file, `redline-turn-revise.md`, points at it; and a new wave of five, `revise-column-sv-r2-a` to `-e`, is run in a fresh wave session with its own listings under `runs/revise/`.
- If a run still counts as colliding after that round, the result is recorded as measured, the wording whose wave had fewer colliding runs is kept — the first on a tie — and the remaining miss is filed `needs-triage` naming #401.

No criterion is softened, and nothing already written under `docs/evaluation/` is edited; the one line this packet adds to `../README.md` is an append.
