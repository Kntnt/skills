# Results for #364: a bridge prepares a quotation rather than pre-says it

Measured against [the frozen plan](plan.md) and the criteria in it. Nothing in the plan or in the judge briefs was edited after the first run.

## What is and is not finished

*Kept true from the first commit onwards, so that a session picking this up after an interruption can see where it stands.*

- **Finished.** The plan, the matrix, the criteria and the two judge briefs are frozen and committed.
- **Running.** The baseline (`b`) arm's seven Write runs.
- **Not started.** Baseline judging, the paired source-blind Redline runs, the candidate arm, the load-chain reviews, the records.

## The harness and the seat

Provider family `claude`. Claude Code 2.1.278. Every run is a fresh top-level session started from the shell with `claude -p`, the turn as its prompt, the child-session environment variables unset, the working directory set to that run's `work/`, and `--model claude-opus-5 --effort high --permission-mode bypassPermissions`. The declared difference from the addendum's "fresh `claude-opus-5` subagent at high deliberation" is the seat: a subagent of this harness has no agent-spawning tool, so both Skills stop on their `subagents` capability there ([#394](https://github.com/Kntnt/skills/issues/394)). The model and the deliberation level are the ones the addendum names.

Judges are fresh `kntnt-opus-high` subagents (`claude-opus-5`, high deliberation) with no history; they start nothing, so the seat question does not reach them.

The GPT-family baseline this ticket inherits was measured under native Codex CLI 0.155.1 on `gpt-6-astra/high`. It is not reproduced here and is not retested: [the protocol](../protocol.md) forbids a Claude session from driving a Codex harness. That is the difference from the baseline, stated rather than estimated.

Corpus commit: `218e3be1`.
