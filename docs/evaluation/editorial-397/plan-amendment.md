# Amendment to the plan: how a run is made

Written on 2026-09-24 and committed before the first valid run of either arm. [`plan.md`](plan.md) stays frozen as it was committed; this file replaces its section *How a run is made* where the two differ, and changes nothing else in it — not the matrix, the judging, the criteria, the rule for `R1`, the inventory scopes 3 to 5 or the exit.

## Why

The plan makes each run a fresh `kntnt-opus-high` subagent of this build's session, as #383 did and as the readiness addendum's clause 1 asks. Eight such runs were dispatched against `install-pre`. Seven of them stopped at Redline's step 1 before reviewing anything: the subagent had no tool for starting a subagent of its own, so it could not confirm the `subagents` Capability Redline declares, and it reported the Unsatisfied Capability as the Skill requires. The eighth, `pre-control-article-clean`, went on, found nothing to correct and so never needed a correction subagent, and returned the no-change status. This build's session is itself a subagent of the run that dispatched it, and a subagent of a subagent is not given the tool that starts a third. #383's runs were subagents of a top-level session and could.

Those eight replies are kept under [`voided/subagent-runs/`](voided/subagent-runs/), with their inventories. They are not findings about Redline: seven are the Skill correctly refusing a Harness the evaluator put it in, and the eighth ran in a Harness lacking a Capability the Skill declares, so none of them is a run of the method. None of them wrote anything but the evaluator's `response.md`.

The readiness addendum requires a Claude Code session that can start subagents, every run on `claude-opus-5-5` at high deliberation, and every correction subagent on the run's seat. A subagent run from this seat meets none of that for Redline. A fresh top-level Claude Code session started with `--model claude-opus-5-5 --effort high` meets all of it, and [`../editorial-388/harness/staged_run.py`](../editorial-388/harness/staged_run.py) is the protocol's Claude-family runner that starts exactly that, as #396's build did in the same unattended run. The addendum reserves that runner for criteria answered from a Harness trace; it is used here because it is the one sanctioned way from this seat to give Redline a session that can start its correction subagents, and no criterion here is answered from the trace it keeps.

## How a run is made, as amended

Every Redline run of both arms, and of any revise round, is made with `staged_run.py`, run from this working tree:

```
uv run docs/evaluation/editorial-388/harness/staged_run.py \
  --revision=<commit> --corpus-revision=a321690f \
  --invocation='<invocation from the matrix>' \
  --input=<input> --input-name=input.md \
  --output=<scratch>/packets/<run> \
  --model=claude-opus-5-5 --effort=high
```

- `<commit>` is `20133068` (`<start>`) for the pre-change arm, the committed candidate for the post-change arm, and the committed revised candidate for a revise round. The runner stages `skills/editorial/{write,redline,proofread,unslop}` and `skills/kntnt` from `<commit>` with `git archive` into a private root of its own, installed as the session's Skills, so the flat installs `install-pre` and `install-post` of the plan are not used.
- `<input>` is the draft or control the matrix names, read from this working tree at `a321690f` or later, where the inputs are byte-identical to `a321690f`'s. The invocation is the matrix's, verbatim, and it is the whole prompt: the two turn files are not sent, because the Skill is installed rather than named by path, and the reply is captured by the runner as `response.txt` rather than saved by the run.
- The seat is the one the plan names: `claude-opus-5-5` at high deliberation, which `run.json` requests and `trace-index.json` records for the session and every nested agent. The correction subagents and the nested Proofread pass run inside that session and take its seat.
- The run's private root — its `HOME`, working directory, temporary directory and caches — is made by `mkdtemp` under the system temporary directory and removed by the runner on every exit, as for #396. It is not under this build's scratch directory because a working directory there would sit under `/Users/thomas/Projects/skills`, whose `CLAUDE.md` a Claude Code session loads from every directory above it. The packet, which is what survives, is written under this build's scratch directory.
- A run's correction subagents write their scratch inside that private root, so a run here and a run of the sibling build cannot collide in the session scratchpad (#401). The `case-study-clean` lock is taken all the same, as the build's brief requires.

## What each run keeps, as amended

In place of the plan's run directory, each run is a packet as `staged_run.py` writes it: `supplied-input.md`, `invocation.txt`, `prompt.txt`, `run.json`, `response.txt`, `inventory-before.json`, `inventory-after.json`, `filesystem-changes.json`, `cleanup.json`, `transcripts/`, `trace-index.json`, `trace-status.json` and the runner's own files. The evaluator adds `expectation.md` for a control, and `judgement-a.md` and `judgement-b.md`. After both judges have written, the packet is copied into `runs/<run>/`.

**Scopes 1 and 2 of the inventory** are the runner's before-and-after inventories of the run's private root, which holds its working directory, its staged install and its scratch. Scopes 3 to 5 are unchanged and are read around each wave as the plan says. **`S1`** is read from `supplied-input.md` and the runner's before-inventory: the working directory held `input.md` and nothing else when the session started.

**Judges.** Each judge's neutral directory holds `work/input.md`, copied from the packet's `supplied-input.md`, and `response.md`, copied from its `response.txt`, and nothing else — the same two files the plan names — because `run.json`, `transcripts/` and `trace-index.json` name the revision and the model.
