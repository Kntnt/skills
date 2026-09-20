# Real Skill runs for #362

Frozen on 2026-09-20 after the checker and validation diagnostics and before any run below. Product under test: the working tree at `65834c32` plus the change to `skills/editorial/write/references/source-check.md` (the round-3 comparison task and the validation paragraph reworded to match it). Nothing else in the Collection differs from `65834c32`.

## How a run is made

Provider family `claude`, in Claude Code, from a Claude session. Each run is one fresh subagent with no history, of type `kntnt-opus-high` (`claude-opus-5`, high deliberation); the checkers it starts inherit that seat, as `source-check.md` says. The session's own seat is `claude-fable-5-1`; runs are delegated to Opus to spare that seat's budget, which is a declared difference from "inherit the session's identity". The earlier GPT-family runs used `gpt-6-astra/high` in Codex CLI 0.155.1; no Codex harness or GPT model is started from here, so those failures are not retested and stay failed.

The staged copy is not an installed Skill, so the Skill tool cannot start it. As in `records/write-claude-2026-08-26.md`, the turn names the staged `SKILL.md` as its instructions and `$HERE` as its directory, and carries the Formal Invocation verbatim. The staged install is a byte copy of `skills/editorial/{write,redline,proofread,unslop}` and `skills/kntnt` side by side in the session scratchpad, so the shim finds the Manager beside the Skill and the global install is never read. Each run has its own working directory holding only `source.md` (Write) or `input.md` (Redline, the delivered text with its metadata and nothing else).

Two evaluator instructions are added to the turn and declared here because they are not the Skill's: copy the source-check scratch directory to `evidence/` before removing it, and save the user-facing reply verbatim to `response.md`. A `sha256` inventory of the working directory and the staged install is taken before and after.

## Matrix

| Row | Invocation | Source | Runs | Paired Redline |
| --- | --- | --- | --- | --- |
| `opinion-en_US` | `/write --genre=opinion --language=en_US --output=response source.md` | corpus `opinion.md` | 2 | yes |
| `opinion-en_GB` | `… --language=en_GB …` | corpus `opinion.md` | 2 | yes |
| `opinion-sv` | `… --language=sv …` | corpus `opinion.md` | 1 | no |
| `column-sv` | `/write --genre=column --language=sv --output=response source.md` | corpus `column.md` | 2 | yes |
| `case-study-en_US` | `/write --genre=case-study --language=en_US --output=response source.md` | corpus `case-study.md` | 1 | no |
| `opinion-absence-en_GB` | `/write --genre=opinion --language=en_GB --output=response source.md` | `opinion-absence-en_GB.md` | 1 | no |

Nine Write runs and up to six Redline runs. Redline loads nothing this change touches, so it is paired only on the rows the ticket centres on; the other three are recorded as skipped for that reason. A stopped Write run has no Redline. No row is rerun; every run is kept.

## Criteria, fixed before the runs

Judged by a fresh judge per draft from the source and the artefacts, without the ticket, the diagnostics or any model identity.

- **F1** on the delivered draft, from the corpus README. For the opinion rows in English this includes: where the draft says what the pilot report does not measure, the third item is habit, familiarity or experience, not skill or ability; the limit counts as exercised only if the draft expresses that item at all. For every row: no unsupported date, scope, personal attribute or event; unknown kept apart from absent.
- **G2** and **L1** on the delivered draft, from the corpus README.
- **Intermediate** on every checker finding and every writer disposition: a supported repair, a disputed caution, a wrong finding accepted, a right finding rejected, a valid stop, or a false stop. A delivered draft that passes F1 does not excuse a wrong finding accepted on the way.
- **Delivery**: the number of comparisons run, whether the delivered prose is byte-identical to the last checked prose, and wall time.
- **R1** on each Redline pair.
