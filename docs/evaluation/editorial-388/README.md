# A trace-bearing Claude-family harness — #388

Two criteria of the [editorial-quality matrix](../corpus/editorial-quality/README.md) are answerable from a Harness trace and from nothing else:

- **T1** — do the resolved configuration **and the actual loaded files** honour selection precedence?
- **R2** — does the trace establish full scoped contract loading, a fresh correction when one was needed, budget and re-review, and exactly one closing installed Proofread pass with no substantive edit after it?

Every entry of the two #386 records scores both `skipped`, because the session that started a run agent could not read that agent's transcript. That is a limit of the method rather than a finding about Write or Redline. This directory removes it.

## What it is

[`harness/run.py`](harness/run.py) runs **one** Formal Invocation in a real Claude Code session of its own and keeps everything that session recorded. The invocation is typed as a user types it — the staged Skills are installed in the run's own configuration directory, so `/write …` is a Formal Invocation and not a paraphrase of one — and nothing is added to the prompt beside it but the fixture's own Contextual Instruction, where the fixture has one.

Claude Code writes the session's own transcript and one transcript per subagent, each beside a `.meta.json` naming the call that started it and the agent that made that call. A run given its own `CLAUDE_CONFIG_DIR` has all of them under one root, which is what makes the nested trace preservable at all.

[`harness/trace_index.py`](harness/trace_index.py) turns those transcripts into `trace-index.json` and `trace-status.json`. The runner runs it, so a packet is complete when it is written; it can be run again over any saved packet.

## Running one

```
uv run docs/evaluation/editorial-388/harness/run.py \
  --revision=<commit> --corpus-revision=<commit> \
  --invocation='/write --genre=web-copy --language=sv --output=response source.md' \
  --input=docs/evaluation/corpus/editorial-quality/sources/web-copy.md \
  --input-name=source.md \
  --output=docs/evaluation/editorial-388/runs/<name> \
  --model=opus --effort=high
```

`--revision` is the commit the Skills are exported from with `git archive`, so the run reads that revision and never the working tree. `--corpus-revision` is recorded rather than used, and is the commit a record would name. `--instruction` supplies a Contextual Instruction where the fixture has one; `--capture-output-name` copies a file the invocation directed output to. An output directory that already exists is refused, so failed evidence is never overwritten.

Read [the protocol](../protocol.md) first. A Claude session runs Claude-family evaluations only, and this runner starts `claude` and nothing else.

## What a packet holds

| File | What it is |
|---|---|
| `invocation.txt`, `contextual-instruction.txt`, `prompt.txt` | The Formal Invocation verbatim, the Contextual Instruction or `none`, and the complete text the Harness was given |
| `run.json` | Both revisions as full commits, the Harness version, the requested identity, the session id, the staged Skills, the argv and the environment |
| `supplied-input.md` | The fixture as it was staged |
| `inventory-before.json`, `inventory-after.json`, `filesystem-changes.json` | `sha256` of every path under the private root, before and after, and the difference |
| `stream.jsonl`, `stderr.txt`, `response.txt` | The Harness's own event stream, its error output, and the final reply |
| `result.json` | Exit status, timeout and interruption, duration, the Harness's own result event, what was harvested, and whether the process group is gone |
| `transcripts/parent.jsonl` | The session's own record, verbatim |
| `transcripts/subagents/` | Every nested agent's record and its `.meta.json`, verbatim |
| `transcripts/extra/` | Anything else the Harness kept beside them, offloaded tool results among it |
| `trace-index.json` | One entry per agent: identity, parent, the call that started it, its instruction, the Seats it ran on, every tool call with its arguments, the files it touched, and the agents it started |
| `trace-status.json` | Whether the trace is whole, and every way it is not |
| `packet.json`, `cleanup.json` | What the packet is, and what the run removed |

## Reading T1 and R2 out of it

Each agent in `trace-index.json` carries `file_activity`, one entry per file the trace records it touching, and `skill_bodies`, one entry per Skill body the Harness loaded with the installation directory it came from. Together they answer *what was loaded*: which references under the staged `library/references/editorial/` were opened, that no `.review.md` was opened in a Write run, that no unselected genre or technique was opened, and that the Skill's own body came from the staged installation.

`delegations` and `agents` answer *who ran what and in what order*: a correction agent started fresh for one round, the round's own re-review after it, and the closing Proofread pass, each with its ordinal and its instant. Ordering within an agent is the `ordinal` of its calls; ordering across agents is the recorded instants.

An entry says how it was established, because the kinds are not equally strong:

- `established_from: "tool-argument"` with `exact: true` — the Harness's own record that the file was opened. This is the strongest evidence a trace carries.
- `established_from: "shell-command"` — the command the run submitted, kept verbatim in `command`. It establishes what was asked for, and the tool result beside it in the transcript establishes what came back.
- `exact: false` — the entry names a set rather than a file: a glob the shell expanded at run time, a path spelled with a variable, a recursive search, or a `Glob` or `Grep` call. Such an entry says the run looked somewhere; it never says which file under it was read.

A variable one command assigns in its own text is expanded before the path is recorded: a run writes the staged installation's path into `$LIB` and reads every reference through it, so a whole contract's loading would otherwise read as unresolved. The substitution is the one the shell itself made, and `command` keeps the assignment beside it, so an evaluator can check it. A value only the run had — a command substitution — is never substituted; the variable stays as it was written and the entry stays `exact: false`.

**The remaining observability limit is the inside of a shell command.** A `cat` of one named file is as good as a `Read`, and its result is in the transcript. A `grep -r` over a directory, or a `cat` of a glob, names the request; which files it reached has to be read out of the result, and a command whose output the transcript truncated cannot be settled from the trace at all. Where that matters to a criterion, the entry is `exact: false` and the evaluator says so in the record rather than reading it as a load.

**A run's own account of itself is never evidence here.** `trace-status.json` is computed from the transcripts and the runner's exit alone; `response.txt` is read by nobody but the evaluator, judging delivery. A packet whose reply says a correction agent ran and whose transcripts hold no such agent is `incomplete`, and says which delegation has no child.

## When the trace is not whole

`trace-status.json` names every way it is not, and the packet keeps everything it managed to preserve either way:

- `parent-transcript-missing` — the Harness wrote no session record, ordinarily a run killed before it started one.
- `unparsable-line` — a transcript ends mid-write; the count is per file, and the lines before it are still indexed.
- `delegation-without-child` — a call started a subagent whose transcript is absent, named by the call's own id.
- `child-without-delegation` — a subagent transcript no recorded call accounts for.
- `run-did-not-finish` — a non-zero exit, a timeout, or an interruption.

None of these is a judgement about a Skill. A packet reported `incomplete` is one whose criteria are scored from what it does hold, with the gap named.

## Isolation and cleanup

The run's `HOME`, its Claude configuration directory, its temporary directory and every cache are inside one private root under the system temporary directory. The Skills it can reach are the staged ones; no hook, no Measurement store and no configuration of the machine's own is in scope, so nothing this collection captures elsewhere sees the run and nothing the run does reaches the machine's own Harness state. The configuration directory is given a credential of its own, mode `600`, whose bytes are never hashed into an inventory and which goes with the root.

The root is inventoried before and after, then removed on every exit — success, failure, timeout and interruption alike — and `cleanup.json` names the one path removed. The child runs in a process group of its own, so a timeout or an interruption stops everything it started; `result.json` records whether that group is gone. The evidence packet is outside the root and survives all of it.

Isolation is not a sandbox: it does not stop a run writing outside the root. That is what the inventories and the working copy are for, exactly as in a run made by hand.

## The runs held here

- [`runs/write-web-copy-sv/`](runs/write-web-copy-sv/) — `/write --genre=web-copy --language=sv --output=response source.md` over the corpus `web-copy` source.
- [`runs/redline-web-copy-flawed/`](runs/redline-web-copy-flawed/) — `/redline --genre=web-copy --language=en_US --output=response input.md` over the `web-copy-flawed` control, which has findings, so the run spends its Correction Budget and closes with the installed Proofread pass.
- [`runs/interrupted/`](runs/interrupted/) — a run stopped by its own timeout, kept as the demonstration that an incomplete trace is reported as one and preserved.

[`validation.md`](validation.md) assigns `T1` and `R2` on the first two from the trace, with the evidence cited. It judges those two criteria and no others: it establishes that the method makes them observable, and it is not an evaluation of either Skill.
