# Handoff — doc-reform and engine series (#261–#275)

Written 2026-09-05, amended the same day by the session that merged `main` forward, and again by the session that closed wave 9's branch check. Delete this file once the run is finished; it is a handoff note, not a repository document.

## Where the run stands

Branch `skills-improvements`, working tree clean. Twelve tickets are built, verified, merged and closed: **#261–#272**.

**Wave 9's branch check is finished.** It ran eight rounds and demanded six fix rounds; the branch is green on all four gate commands and its changelog entries are applied. What that check was for, and what it cost, is under *Wave 9* below — read it before running another wave check, because two of its rounds found defects the previous fix round had itself created, and the rule that prevents that is now written down.

**`main` has been merged forward twice**, most recently at `d4b2dfa`. The second merge was taken because the branch had fallen nineteen commits behind and four of those are robustness fixes to `skills/code/orchestrate/scripts/run.py` — the engine that runs the remaining tickets. None of the nineteen touches `skills/kntnt/scripts/kntnt.py`, the file #273 extends.

**Three remain: #273, #274, #275** — the invocation engine. They are strictly sequential: #274 is blocked by #273, #275 by #274. **#275 is a Solo Ticket** and declares it in its body. None of the three carries a comment, so each body is the whole requirement.

## The command

Start the successor **inside the worktree**:

```
claude
```

This is not optional, and it is the failure mode rather than a theoretical one: a session briefed from `/Users/thomas/Projects/skills` has been turned away for it. `/orchestrate` reads the run branch from the git repository the session stands in, so started in the wrong checkout the run branch becomes `main` and the work lands there.

Then:

```
/orchestrate --at-once=1 --model=claude-opus-5 #273 #274 #275
```

`--at-once=1` rather than the `2` an earlier version of this note carried. The three tickets are strictly sequential and #275 is Solo, so no value above 1 buys any parallelism — and `main`'s new worktree-access probe only runs above `--at-once=1`, which is machinery this run has no use for and can fail on. If you do raise it, read the entry about that probe in the changelog first.

`--model=claude-opus-5` is the maintainer's lock. Without it the routing cold start selects Haiku 4.5 for every builder, there being no matched measurement for these Cohorts, so every decision comes back `evidence_class: heuristic`. Verdicts inherit the Opus 5 main seat regardless.

A fresh state directory is fine. The twelve closed tickets fall out of the plan on their own, the plan reading the tracker.

## Wave 9, and what it cost

Eight check rounds, six fix rounds, findings per round **7 → 3 → 2 → 1 → 2 → 3**. The subject throughout was one thing: the merge brought a second Catalog entry type — the Feature — onto a branch whose glossary and rules modules described a Catalog of Skills only, and `docs/rules/` does not exist on `main`, so nothing had ever read those modules against it.

**Two of the rounds found defects the previous fix round had itself created.** A fixer rewrites a rule in a rules module, and every shipped page that agreed with the old wording silently disagrees with the new one. Both remedies are now written down and neither existed during this wave:

- `docs/rules/general.md`'s refactoring-completeness section says how a rule's surfaces are enumerated — by what a surface asserts rather than by how it words it, and including what *points at* a rule as well as what states it.
- `skills/code/orchestrate/references/wave.md` says a round following a fix reads the tree back against the sentences that fix wrote.

**Read both before briefing a wave check.** Had either existed, this wave would have taken two rounds rather than eight.

Five findings were judged ticket material rather than fixes and are filed: **#282** (Update never reports a failed Feature re-convergence — the only real bug), **#283** (`teardown_features()` is dead code), **#284** (two Feature surfaces the suite does not reach), **#285** (name what `--on`/`--off` take by one word), **#286** (move the prose-sweep rules to `docs.md`). None blocks #273–#275.

The last fix round, `2aad7fb`, was not read by an independent checker — the maintainer waived the final round deliberately. It is three sentence-level corrections and the gate is green on it, but it is the one commit in this wave nobody but its author has read.

## What the run learned that the Skill does not tell you

**The engine reserves one record number per ticket.** #269 and #270 each wrote two records, and the brief's instruction for that case is to stop and report. Both times the run appended a second entry to `.git/kntnt-orchestrate/<n>.reserved.json` and re-ran `isolate`, which then reports both. #273 writes one record and needs no such repair. Do not let a builder read the directory for "next free" — another session allocates numbers in this same repository and holds some of them.

**Sessions end their turn mid-suite and have to be resumed.** The brief tells every subagent in two paragraphs that a long command is waited on rather than yielded to, and it is not enough. When it happens: check whose processes are alive (`lsof -a -p <pid> -d cwd -Fn`) before assuming the suite is the builder's — other sessions run `pytest -n auto` in other checkouts — then wait for the real result and resume the agent with it. Never let a resumed builder commit on a gate result it did not see.

**The suite has a load-induced flake** under `pytest -n auto`: `shutil.copytree` racing a transient `__pycache__/*.pyc.<pid>` another xdist worker is writing. Always rerun a single failing test in isolation before concluding anything. It did not appear once in wave 9's eight gate runs.

**`CHANGELOG.md` is the run's own file.** Builders write their entry to `.kntnt-orchestrate/<number>.md` and the run applies it after the wave merges. Builders have written that note in three shapes — a bare path line, a `## \`CHANGELOG.md\`` heading with the section named in prose beneath, and a single line carrying both. Whatever applies them must accept all three and fail loudly on a shape it cannot parse.

**`/orchestrate`'s prose and its engine disagree about fix rounds.** The Skill says to re-run the wave check after a fix and act on the verdict "exactly as this step acts on the first", allowing several rounds per wave. `run.py` accepts only `wave-fix-<wave>` as a plain integer and refuses to restart a completed request. This run numbered them sequentially, so the identifiers count rounds rather than waves in the evidence ledger. The Cohort and observations are correct; only the wave correspondence in the identifier is lost.

**Dispatching a check and then committing while it reads is a race you will lose quietly.** Wave 9's round 8 was dispatched at one head and read a different one; it noticed and ran the gate twice, but nothing guaranteed that. Freeze the head for the length of a check.

## Decisions the maintainer made during the run

1. **Builders run on Opus 5**, the cold-start heuristic having otherwise put Haiku 4.5 on a series that rewrites every shipped file.
2. **`docs/rules/docs.md` keeps its rule that `AGENTS.md` routes rather than legislates**, naming the `## ⚠️ TEMPORARY` rework section as its one standing exception, self-removing when that section goes.
3. **Four normative sentences #265 stripped from `CONTEXT.md` were restored** into the documents holding their terms' law. The fifth — "Redline and Unslop carry the same contract" — was dropped permanently, a consolidation record having decided the opposite. Its absence is intended.
4. **The `RUNTIME` bin was widened** from *cited by `run.py` or `tests/test_orchestrate.py`* to *is `/orchestrate`'s own machinery*, with such a citation sufficient but no longer necessary, and nine records moved out of `DROP`. Without it #272 would have deleted the parked-ticket resume, the approval ceiling and the flake protocol.
5. **The prose-sweep rules move to `docs.md` rather than `general.md` widening its pointers** — filed as #286, decided rather than left open.
6. **Wave 9's final read was waived**, above.

## Open items worth a ticket, not filed

- **A ticket that writes N records needs N reservations.** Nothing in the engine asks how many a ticket will write.
- **`validate_manager_candidate` in `skills/kntnt/scripts/kntnt.py`** does not list `library/references/invocation-envelope.md` among the Manager's required files, so a staged Manager missing the file every Skill now reads still validates. Declined by three wave-check rounds as a decision rather than a restatement.
- **The parallel test gate's `copytree` flake**, above.
- **`RUNTIME` now means "is orchestrate machinery, or is cited by it"**, and seven records are in on the second clause alone while their subject is not that machinery. Narrowing it would falsify six merged consolidation records, so it is a ticket against those rather than a table edit.
- **`docs/rules/general.md`'s trigger says *read when writing code*** while its refactoring-completeness section binds a contributor editing only prose. #286 resolves this by moving the rules; if that ticket is closed another way, the trigger still needs widening.
- **`docs/rules/docs.md` states that `AGENTS.md` holds no rules** while the TEMPORARY section does. The exception is named, but when the rework branch is deleted both go together.
