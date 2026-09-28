# Unslop and the sentences that limit a claim — results for #385

Measured on 2026-09-28, against [`plan.md`](plan.md) as it was frozen again at `4d10e603`, before the first run of the wave counted here. `plan.md`, the two turn files and the two judge briefs are unchanged from `4d10e603` onwards: every run and every judgement below was made after that commit, and none of those files was edited after the first of them. The runs, their inventories and both judgements of each are under [`runs/`](runs/); the mapping from each judge's neutral directory to its run is [`runs/judges.tsv`](runs/judges.tsv).

## How the plan came to be frozen twice

The plan was first frozen at `e3723890`, and a first wave of the four pre-change runs was made and judged against it on 2026-09-24. After those runs, `0d7fd057` respelled one line of the plan, the run command under *How a run is made*, as `--model=claude-opus-5-5 --effort=high`, because the repository's flag-grammar check (`tests/test_flag_grammar.py`) refused the frozen spelling with a space between each flag and its value. The plan says nothing in it is edited after the first run, so that first wave does not stand as this evaluation's pre-change arm. It is void and is not counted here. Its runs, judgements and inventories are kept byte for byte under [`runs/voided/wave-1/`](runs/voided/wave-1/), with [the reason](runs/voided/wave-1/reason.md).

`4d10e603` then froze the plan again. It adds one paragraph, **Frozen twice.**, which voids the first wave, names the replacement wave `wave-2`, and names the record for the date the replacement wave was made. It changes nothing else in the plan relative to `0d7fd057`. The turn files and judge briefs are byte-identical to `e3723890`. In the same commit, [`runs/run_turn.sh`](runs/run_turn.sh) took the plan's respelled command, so that the script that starts each session and the plan's command agree. The full suite passed on the refrozen plan before the commit. The four pre-change runs were then made again from nothing: fresh run directories, fresh sessions and eight fresh judges. No run, log or judgement from the first wave was reused.

What the void wave showed does not change the outcome. It is kept in `runs/voided/wave-1/`, and the section *The void first wave* below summarises it.

## The outcome: not reproduced

**No pre-change run reached a limiting sentence.** On all four drafts, and on both judges' readings, no limiting sentence was removed, weakened, hardened or recast outside classes (a) and (b). The pre-change arm therefore has no `N1` miss. The plan's exit for that case applies:

- the defect this ticket was filed for is recorded as not reproduced;
- the post-change arm and the seven controls were not run;
- the candidate (`d84b20ae`) stays reverted by its own commit (`18757082`);
- the three Unslop surfaces, its manpage, the catalog and the test suite are byte-identical to `c211a1d5`.

[ADR-0221](../../adr/0221-unslop-keeps-its-whole-passage-permission-measured-and-left-alone.md) records the decision.

So the answer to the question #385 was filed with is this. **Unslop, as it stands, did not reach a limiting sentence** on the texts where #377 found the defect. The divergence between Redline's narrowed rule and Unslop's unnarrowed one stands as intended.

## The pre-change arm

There were four runs, one on each draft. Each was a fresh top-level Claude Code 2.1.281 session on `claude-opus-5-5` at high deliberation against `install-pre` (`c211a1d5`), invoked as `/unslop --output=response input.md`. All four started at 07:29:15Z on 2026-09-28 and returned by 07:31:19Z. Each session's `init` event and its closing usage name `claude-opus-5-5` and no other model. That includes the one correction subagent, started in `pre-opinion-en_GB-r2`. Each artefact had two blind judges, fresh `kntnt-opus-high` subagents on the same model.

| Run | What came back | Differences (a / b) | Limiting sentences listed (a / b) | Touched | `N1` misses | `N2` misses |
| --- | --- | --- | --- | --- | --- | --- |
| `pre-column-sv-r1` | the Swedish no-change status | 0 / 0 | 7 / 7 | none | 0 | 0 |
| `pre-column-sv-r2` | the Swedish no-change status | 0 / 0 | 7 / 6 | none | 0 | 0 |
| `pre-opinion-en_GB-r1` | the English no-change status | 0 / 0 | 10 / 11 | none | 0 | 0 |
| `pre-opinion-en_GB-r2` | the text, after one correction round on one synonym-cycling finding | 3 / 3 | 13 / 13 | two host sentences, outside their limiting clauses | 0 | 0 |

The counts of limiting sentences include the borderline cases each judge listed and marked as borderline.

**The one run that changed anything** replaced *channel(s)* with *route(s)* in three places, on a synonym-cycling finding that names all three:

- *keeping both channels*
- *keep a channel*
- *before the channel goes*

A mechanical diff of `work/input.md` against the returned text confirms those three differences, on two lines, and no others. Each of the two changed sentences carries a limiting clause, and the edit falls outside it in both:

- *not any view that telephone users are lazy or expensive, and I do not accuse it of holding one*
- *The trial costs something we have not costed*

Both judges record both clauses kept word for word. Both also answer the brief's three questions, treating each host sentence conservatively as recast:

- The reply names a pattern inside the sentence: a single word, not the whole sentence.
- The pattern can be verified from the input alone. The text calls the same two ways of booking *routes* four times and *channel(s)* three times.
- The case is class (a): the limit is still stated word for word in the returned text.

Neither reading is an `N1` miss, so the stricter of the two gives none. Both judges class all three differences as pattern repairs that change no element of any claim, and find all three reported accurately. So there is no `N2` miss either.

**The sentence #377's diagnosis found hardened** through the False contrasts pattern, *I am not against digital booking.*, appears in both English drafts. All four judges of the two opinion runs list it as a limiting sentence and record it kept as it was. The same holds for three other sentences:

- *We make no claim to have funded or costed that trial.* This is the sentence #377's hardening form 1 is modelled on, and it keeps both *funded* and *costed*.
- *A booking made by phone is not proof that somebody cannot use the web.*
- *That a booking comes in by telephone is not proof that somebody cannot use the web.*

**Target figure.** `N1` and `N2` misses together, over the arm's four runs, come to 0 / 4 = 0. There is nothing for a candidate to beat. That is why the exit is *not reproduced*, rather than the comparison of clause 4.

## Not run

The eight post-change runs and the seven controls in the plan's matrix were not run. The plan's order of work requires this where the pre-change arm shows no `N1` miss. The revise round was not spent. The record lists each of them as skipped with that reason, so that none reads later as a run that passed. The seven `expectation.md` files were prepared under the scratch root before the first wave and never used.

## The check on #383's work

This is recorded here and is not one of this ticket's criteria. The only run that changed the text was `pre-opinion-en_GB-r2`. There, both judges find:

- all three differences trace to the one finding the reply reports;
- the reply's closing **What changed:** paragraph names all three instances and covers the one kind of difference;
- the closing paragraph says nothing false against the returned text.

In the three runs that changed nothing, all six judges find:

- no difference to trace;
- no closing paragraph owed;
- a one-line status that is true.

One of them, the second judge of `pre-column-sv-r1`, notes that the reply returns no copy of the text. That is the no-change status the response target asks for, and the judge records nothing false in it. Nothing is filed.

## `O1`, `S1` and the rest

- **`S1`** — pass on all four. Each run directory's `inventory-before.txt` lists `work/input.md` and nothing else. The inventory was taken immediately before the session started.
- **`O1`** — pass on all four. Between each run's two inventories:
  - the staged install's digest is unchanged (`00f68701…`, 70 files);
  - `work/input.md` is unchanged;
  - the only new file in the run directory is the evaluator's `response.md`.

  `pre-column-sv-r1` and `pre-column-sv-r2` each left an empty `scratch/` directory in the run directory. That is the directory the turn names for scratch, and it holds no file.

  Across the wave, the two checkouts' `HEAD` and porcelain status are identical before and after (`runs/wave-2-*-repo.txt`). The scratch root changed only by the four run directories, the sessions' logs and the wave inventories themselves (`runs/wave-2-*-scratch.txt`).

  The Harness keeps each session's own transcript and tool-result files under `~/.claude/projects/`. That is the Harness's storage, not a Skill file.
- **Interrupted runs** — none. All four sessions ended with `success`. One Bash call in `pre-column-sv-r1` failed: a `git status` on the run's working directory, which lies inside the repository's git directory and so is not a work tree. That was a failed command, not a usage limit, a 5xx or an overload, so the run is valid.
- **`T1` and `R2`** — `skipped` on every run. This ticket's scope runs Unslop through turn files and answers no criterion from a Harness trace.
- **`R1`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2`** — `skipped` on every run. The editorial-quality corpus's criteria are Redline's and Write's, and do not apply to Unslop.

## Facts the plan asked to be confirmed

- **#383 and #398 had landed.** At `c211a1d5`:
  - `anti-slop.md` carries *The test before a pattern is recorded*;
  - Unslop's step 7 carries the trace check;
  - Unslop's step 9 carries the closing summary;
  - #398 is closed and merged.
- **The English hedge-chain line is not in Unslop's scope.** One search on 2026-09-28, `grep -n "^## \|hedge" skills/kntnt/library/references/languages/en_GB.md`, finds the line at line 47. That is under `## Review` (line 37), before `## Anti-slop` (line 53).
- **The installs were staged as the plan says.** Before the replacement wave, both installs were compared with a fresh `git archive` of `c211a1d5` and `d84b20ae`, laid out as the plan's two commands lay them out, and found identical. After the wave, the shim was run once from each install with `--output=response input.md` on stdin, and the `$LIBRARY` it printed was `…/install-pre/kntnt/library` and `…/install-post/kntnt/library` respectively, with nothing written into either install.
- **The inputs.** The four drafts under the scratch root are byte-identical (`cmp`) to the #362 files the plan names.
- **The locks.** Each run took `/Users/thomas/Projects/skills/.git/kntnt-eval-lock-<draft>` at once, because no other build held one at that moment. Each run removed its lock when its session returned. Two such lock directories, for `column-sv-r1` and `column-sv-r2`, were created at 07:30:12Z. That is after both Swedish runs had returned and released theirs, so they are the sibling build's.

## The void first wave

This section is for the record only; nothing in it is counted. The first wave's four runs, made on 2026-09-24 against the plan as first frozen, came out the same way:

- three no-change statuses;
- one run, `pre-opinion-en_GB-r1` that time, that replaced *channel* with *route* in two sentences on a synonym-cycling finding;
- no `N1` or `N2` miss on either judge's reading.

Which English draft drew a finding differed between the two waves.

## What this measurement does not settle

The four drafts gave Unslop little to do: three came back clean, and the fourth raised one finding. A limiting sentence can be reached only by a repair, and a pass that raises no finding near one never reaches it. So this arm tested the recognition half of the question, whether Unslop takes a limit for a pattern, much more than the repair half.

It found no limit taken for a pattern among the thirty-seven limiting sentences and clauses each judge listed across the four runs, borderline cases included. Twice, a repair did land in a sentence carrying a limit, and it left the limiting clause word for word. But the drafts carried no pattern inside a limiting clause that Unslop found, so no run put one in front of a correction subagent. ADR-0221 records that as the limit of this result.
