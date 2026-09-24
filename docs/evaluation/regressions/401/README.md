# Five concurrent Redline runs on one input, and no correction subagent's file collides

Five native `/redline --output=response input.md` runs, started together on 2026-09-24 for [#401](https://github.com/Kntnt/skills/issues/401) on the same input, against the product [`plan.md`](plan.md) fixes: commit `01ee82a0`, staged with `git archive`. Each run is a fresh `kntnt-opus-high` subagent (`claude-opus-5-5` at high deliberation) of one `claude --print` wave session on the same seat, in Claude Code 2.1.281. Provider family `claude`. No Codex Harness and no GPT model was started. No judge was used.

This packet is governed by [`../README.md`](../README.md) and not by the corpus protocol or its `records/` format.

It exists because a correction subagent in #383 wrote its candidate to a fixed name in the scratchpad its session shared with a concurrent run on this same column. That run wrote the same name, and the subagent deleted the other run's repair as its own stale copy. Both correction briefs now carry a paragraph, **Your own working files.**, telling the subagent to keep such a file in a directory it created for this one round and to remove it afterwards. The paragraph also names that failure. These runs test whether a wave arranged the way #383's collision was arranged still collides.

## Result

**No run counts as colliding.** All five runs were exercised, so the wording ships and no revise round was taken.

| Run | Correction subagent the run started | Reply reports a collision | Result |
| --- | --- | --- | --- |
| [`post-column-sv-r2-a`](runs/post-column-sv-r2-a/response.md) | `kntnt-opus-high` | no | **pass** |
| [`post-column-sv-r2-b`](runs/post-column-sv-r2-b/response.md) | `kntnt-opus-high` | no | **pass** |
| [`post-column-sv-r2-c`](runs/post-column-sv-r2-c/response.md) | `kntnt-opus-high` | no | **pass** |
| [`post-column-sv-r2-d`](runs/post-column-sv-r2-d/response.md) | `kntnt-opus-high` | no | **pass** |
| [`post-column-sv-r2-e`](runs/post-column-sv-r2-e/response.md) | `general-purpose` | no | **pass** |

The wave took 683 s. The runs took 238 s to 295 s each. Every run started exactly one correction subagent and repaired the headline in that round, so every run exercised the brief. Each run chose how to start its subagent. Four chose the type `kntnt-opus-high`. Run `e` chose `general-purpose`, which inherits the run's model.

**The listings.** The wave session's scratchpad was `/private/tmp/claude-501/-Users-thomas-Projects-skills--git-kntnt-orchestrate-401-scratch-wave-2-cwd/7e16ce48-978c-41cc-8af1-29fe59e0ba0d/scratchpad` ([`runs/scratchpad-path.txt`](runs/scratchpad-path.txt)). It was empty before the runs and empty after them. Both [`runs/scratchpad-before.txt`](runs/scratchpad-before.txt) and [`runs/scratchpad-after.txt`](runs/scratchpad-after.txt) are empty files, which is the listing command's output over a directory holding no file. So no file changed or disappeared. No new file appeared directly in the scratchpad or in a subdirectory of it. There is no collision and no cleanup miss to name.

**The replies.** No `response.md` says that a file the run or its subagent wrote was changed, replaced or removed by something else. None says that the run or its subagent changed, replaced or removed a file it had not written. Every `reply.md` the wave session saved is byte-identical to the `response.md` its run wrote. Every run's `work/input.md` still has the fixture's digest, `74b966f1…`. No run left a `scratch/` directory behind.

**Where the correction subagents put their files.** [`runs/correction-file-writes.txt`](runs/correction-file-writes.txt) lists every tool call each correction subagent made, read from the wave session's native subagent transcripts under `~/.claude/projects/`. Those transcripts are not copied into this packet. All five subagents wrote their candidate text into a directory they had just made with `mktemp -d`, and removed that directory in the same command, by `trap` or by a closing `rm -rf`. None wrote a file under a fixed name. None wrote in the scratchpad or directly under `/tmp`. `mktemp -d` resolves under the system temporary directory the wave session inherited, not under the scratchpad. The paragraph allows that, because the paragraph asks for a directory made unique when the subagent creates it, not for a particular parent directory.

## How the wave departed from the plan

[`plan.md`](plan.md) starts the wave session with `claude --print` and has it list "its own session scratchpad, as its system prompt names it". The first wave session started that way reported that its system prompt named no scratchpad directory. Claude Code 2.1.281 names a scratchpad only where its Artifact feature is on, and it keeps that feature off by default in a `--print` session. So that wave had no shared scratchpad to collide in or to list. It is kept, not counted, under [`runs/no-scratchpad/`](runs/no-scratchpad/). The replies there and in [`runs/no-scratchpad/wave-session-reply.md`](runs/no-scratchpad/wave-session-reply.md) show that all five runs were exercised and that none reported a collision. [`runs/no-scratchpad/correction-file-writes.txt`](runs/no-scratchpad/correction-file-writes.txt) shows that all five correction subagents again used `mktemp -d` directories. One of those subagents ran `cd /tmp` without writing there. Those five run directories were then moved under `runs/no-scratchpad/`, and fresh copies of the fixture were put at the planned paths.

The counted wave was started the same way, with one variable added: `CLAUDE_CODE_ARTIFACT=1`, which turns that feature on in a `--print` session. A probe made first (`claude-haiku-4-5-20251001`, one subagent) showed that, with this variable set, a subagent's own system prompt names its parent session's scratchpad. That is the configuration #383's collision happened in: one scratchpad, named to every subagent in the session and to every subagent those subagents start. Nothing else in the command, the wave session's instructions, the turn or the dispatch messages changed.

One line of [`plan.md`](plan.md) was edited after the runs. The wave session's command line there now writes each valued flag with `=` (`--model=claude-opus-5-5`, where the frozen line put a space between the flag and its value), because the repository's flag-grammar test rejects the spaced form on every Markdown surface under `docs/`. The command means the same either way, and the plan as it was frozen before the first run is commit `5a7276bc`. No other frozen file was edited.

## Limits

- There is no pre-change arm, as the ticket settles. So a clean wave shows that the collision did not recur with the fix in place. It does not show that the fix is why. In #383 one run of twenty-three reported a collision, and waves 2 to 6 of that evaluation ran four or five runs at once, on distinct inputs, without a second one. Five clean runs are consistent with the old rate as well as with a lower one.
- Unslop's brief carries the same paragraph and was not run here.
- In the counted wave, the scratchpad named to the correction subagents is inferred from the probe and from the wave session's own system prompt. A subagent's system prompt is not written to its transcript.
- The wave session's scratchpad directory, and the ones Claude Code made for the first wave session and the probe, are left on disk, empty. They are outside the directories the builder was given to write in.

## Files

- [`plan.md`](plan.md), frozen and committed before the first run.
- [`redline-turn.md`](redline-turn.md), the turn: `../../editorial-383/redline-turn-post.md` with its paths substituted.
- [`dispatch/`](dispatch/), the message that started each run.
- [`wave-session.md`](wave-session.md), the wave session's whole instruction.
- `runs/<run>/`, each with `work/input.md`, the `response.md` the run wrote and the `reply.md` the wave session saved.
- `runs/scratchpad-path.txt`, `runs/scratchpad-before.txt`, `runs/scratchpad-after.txt` and `runs/correction-file-writes.txt`, for the counted wave.
- `runs/no-scratchpad/`, the first wave, not counted.
