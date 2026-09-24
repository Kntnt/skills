# Unslop and the sentences that limit a claim — results for #385

Measured on 2026-09-24 against the plan frozen in [`plan.md`](plan.md) at `e3723890`, before the first run. Nothing in that plan, the two turn files or the two judge briefs was edited after it. The runs, their inventories and both judgements of each are under [`runs/`](runs/); the mapping from each judge's neutral directory to its run is [`runs/judges.tsv`](runs/judges.tsv).

**One respelling of the frozen plan, after the runs.** The code block in `plan.md`'s *How a run is made* was frozen with the values of `--model` and `--effort` separated from their flags by a space. The repository's verification gate then refused it: `tests/test_flag_grammar.py` holds every command line in `docs/` to the collection's `--flag=value` spelling, and exempts `git`, `gh`, `uv` and `npx` but not `claude`. That line alone was respelled `--model=claude-opus-5-5 --effort=high`, in a commit of its own after the runs; nothing else in the plan, the turn files or the briefs changed, and the plan as frozen is `e3723890`. It changes no method: the sessions were started by `runs/run_turn.sh`, which the gate does not read and which is unchanged, and `claude --print --safe-mode --model=claude-opus-5-5 --effort=low` was run once to confirm that the respelled form starts a session on `claude-opus-5-5`. It is still an edit to a file the plan says is not edited after the first run, and it is recorded here for that reason.

## The outcome: not reproduced

**No pre-change run reached a limiting sentence.** On all four drafts, on both judges' readings, no limiting sentence was removed, weakened, hardened or recast outside classes (a) and (b), so the pre-change arm has no `N1` miss. The plan's exit for that case applies: the defect this ticket was filed for is recorded as not reproduced, the post-change arm and the seven controls were not run, the candidate (`d84b20ae`) is reverted by a commit of its own (`18757082`), and the three Unslop surfaces, its manpage, the catalog and the test suite are byte-identical to `c211a1d5`. [ADR-0221](../../adr/0221-unslop-keeps-its-whole-passage-permission-measured-and-left-alone.md) records the decision.

So the answer to the question #385 was filed with is that **Unslop, as it stands, did not reach a limiting sentence** on the texts #377 found the defect on, and the divergence between Redline's narrowed rule and Unslop's unnarrowed one stands as intended.

## The pre-change arm

Four runs, one on each draft, each a fresh top-level Claude Code 2.1.281 session on `claude-opus-5-5` at high deliberation against `install-pre` (`c211a1d5`), invoked `/unslop --output=response input.md`. Each session's `init` event and its closing usage both name `claude-opus-5-5` and no other model, the one correction subagent among them included. Two blind judges each, fresh `kntnt-opus-high` subagents on the same model.

| Run | What came back | Differences (a / b) | Limiting sentences listed (a / b) | Touched | `N1` misses | `N2` misses |
| --- | --- | --- | --- | --- | --- | --- |
| `pre-column-sv-r1` | the Swedish no-change status | 0 / 0 | 6 / 7 | none | 0 | 0 |
| `pre-column-sv-r2` | the Swedish no-change status | 0 / 0 | 5 / 6 | none | 0 | 0 |
| `pre-opinion-en_GB-r1` | the text, after one correction round on one synonym-cycling finding | 2 / 2 | 12 / 10 | one host sentence, outside its limiting clause | 0 | 0 |
| `pre-opinion-en_GB-r2` | the English no-change status | 0 / 0 | 13 / 13 | none | 0 | 0 |

**The one run that changed anything** replaced *channel* with *route* in two sentences, on a synonym-cycling finding that names that word: *close a channel for good on the strength of an inconvenience the documents put no number on* and *decide whether a channel should be removed, changed or kept*. A mechanical diff of `work/input.md` against the returned text confirms those two differences and no others. The first sentence carries a limiting clause, *an inconvenience the documents put no number on*. Judge A records the clause kept word for word, the edit falling outside it. Judge B records the host sentence as strictly recast and answers the three questions: the reply names a pattern inside the sentence, a single word; the pattern is verifiable from the input alone, *channel* being the only other name for what the text calls a *route* seven times over; and the case is class (a), the limit being stated word for word in the returned text. Neither reading is an `N1` miss, so the stricter of the two gives none. Both judges class both differences as pattern repairs that change no element of any claim, so there is no `N2` miss either.

**The sentence #377's diagnosis found hardened** through the False contrasts pattern, *I am not against digital booking.*, is in both English drafts. All four judges of the two opinion runs list it as a limiting sentence and record it kept as it was. So are *We make no claim to have funded or costed that trial.*, the sentence #377's hardening form 1 is modelled on, and *A booking made by phone is not proof that somebody cannot use the web.*

**Target figure.** `N1` and `N2` misses together, over the arm's four runs: 0 / 4 = 0. There is nothing for a candidate to beat, which is why the exit is not reproduced rather than the comparison of clause 4.

## Not run

The eight post-change runs and the seven controls in the plan's matrix were not run, as the plan's order of work requires where the pre-change arm shows no `N1` miss. The revise round was not spent. The record lists each of them as skipped with that reason, so that none reads later as a run that passed.

## The check on #383's work

Recorded, and not one of this ticket's criteria. In the one run that changed the text, both judges find that both differences trace to the one finding the reply reports, and that the reply's closing paragraph (**What changed:**) covers the one kind of difference and says nothing false against the returned text. Judge A notes one looseness in it: *everywhere else the text calls the phone and web ways of booking "routes"* passes over *two flows* in the opening paragraph, which the judge reads as arguably naming staff's two data-entry processes rather than the two ways of booking, and which it records as making no statement about the changes false. In the three runs that changed nothing, all six judges find no difference to trace and no closing paragraph owed, and the one-line status true. Nothing is filed.

## `O1`, `S1` and the rest

- **`S1`** — pass on all four. Each run directory's `inventory-before.txt`, taken immediately before the session started, lists `work/input.md` and nothing else.
- **`O1`** — pass on all four. Between each run's two inventories the staged install's digest is unchanged, `work/input.md` is unchanged, and the only new file in the run directory is the evaluator's `response.md`. `pre-opinion-en_GB-r1` left an empty `scratch/` directory in its run directory — the one the turn names for scratch — after removing the two private `TMPDIR` directories it had made there; it holds no file. Across the wave, the two checkouts' `HEAD` and porcelain status are identical before and after (`runs/wave-1-*-repo.txt`), and the scratch root changed only by the four run directories, the sessions' logs, and evaluator files written during the wave (`expectations/`, `mkjudge.sh`, the wave inventories themselves). The Harness keeps each session's own transcript and tool-result files under `~/.claude/projects/`, which is its storage and not a Skill file.
- **Interrupted runs** — none. One Bash call in `pre-opinion-en_GB-r1` was refused by the Harness's own safety check (an `rm -rf` on a variable path); the run removed the directory by a literal path instead and went on. That is the Harness, not a usage limit, a 5xx or an overload, and the run is valid.
- **`T1` and `R2`** — `skipped` on every run: this ticket's scope runs Unslop through turn files and answers no criterion from a Harness trace.
- **`R1`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2`** — `skipped` on every run: the editorial-quality corpus's criteria are Redline's and Write's, and do not apply to Unslop.

## Facts the plan asked to be confirmed

- **#383 and #398 had landed.** `anti-slop.md` at `c211a1d5` carries *The test before a pattern is recorded*; Unslop's step 7 carries the trace check and step 9 the closing summary; #398 is closed and merged into `c211a1d5`.
- **The English hedge-chain line is not in Unslop's scope.** One search, `grep -n "^## \|hedge" skills/kntnt/library/references/languages/en_GB.md`, finds it at line 47, under `## Review` (line 37), before `## Anti-slop` (line 53).
- **The installs were staged as the plan says**, and the shim printed a `$LIBRARY` under each. The thread's one-command example lays `kntnt`'s contents out flat, and the shim then fell back to the globally installed Manager; that layout was caught by this check before any run and never used.
- **The locks.** Each run took `/Users/thomas/Projects/skills/.git/kntnt-eval-lock-<draft>` at once, the sibling build holding none of them at that moment, and removed it when its session returned.

## What this measurement does not settle

The four drafts gave Unslop little to do: three came back clean and the fourth raised one finding. A limiting sentence can only be reached by a repair, and a pass that raises no finding near one never reaches it, so this arm tested the recognition half of the question — whether Unslop takes a limit for a pattern — much more than the repair half. It found no limit taken for a pattern, among the thirty-four to thirty-eight limiting sentences and clauses the judges listed across the four runs, the count depending on the judge. It did not put a pattern inside a limiting sentence in front of a correction subagent, because the drafts carried none that Unslop found. ADR-0221 records that as the limit of this result.
