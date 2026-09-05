# Handoff — doc-reform and engine series (#261–#275)

Written 2026-09-05 by the session that ran #261–#272, and amended the same day by the session that merged `main` forward. Delete this file once the run is finished; it is a handoff note, not a repository document.

## Where the run stands

Branch `skills-improvements`, working tree clean. Twelve tickets are built, independently verified, merged and closed: **#261, #262, #263, #264, #265, #266, #267, #268, #269, #270, #271, #272**.

**Three remain: #273, #274, #275** — the invocation engine. They are strictly sequential: #274 is blocked by #273, #275 by #274, and #275 is a Solo Ticket.

**`main` has been merged forward into this branch**, on Thomas's decision, before any of the three is built. The branch had fallen 17 commits behind: since the merge-base `3de96f0`, `main` took the harness-integration merge and the Catalog/Feature work, including 917 added lines in `skills/kntnt/scripts/kntnt.py` — the file #273 extends with `invoke`. Building the engine on the stale branch would have written `invoke` against a `kntnt.py` a thousand lines out of date and discovered it at integration. What the merge settled is listed under *The merge* below; the four gate commands pass on the result.

**Wave 9's branch check has not run.** #272 is merged and its changelog note applied, but no session has yet read the integrated branch for coherence. That is the first thing to do — and read the note on its `<since>` below before briefing it.

## The command

Start the successor **inside the worktree**:

```
cd /Users/thomas/Projects/skills-improvements && claude
```

A session briefed from `/Users/thomas/Projects/skills` has already been turned away once for exactly the reason below, so this is the failure mode rather than a theoretical one.

This is not optional. `/orchestrate` reads the run branch from the git repository the session stands in. Started in `/Users/thomas/Projects/skills`, the run branch becomes `main` and the work lands on the wrong branch.

Then:

```
/orchestrate --at-once=2 --model=claude-opus-5 #273 #274 #275
```

`--model=claude-opus-5` is the maintainer's lock. Without it the routing cold start selects Haiku 4.5 for every builder — there is still no matched measurement for these Cohorts, so every decision comes back `evidence_class: heuristic`. Verdicts inherit the Opus 5 main seat regardless of the lock.

A fresh state directory is fine. The twelve closed tickets fall out of the plan on their own, because the plan reads the tracker.

## The merge (`main` → `skills-improvements`)

Eight files conflicted. Seven resolutions and one collision of substance, all under the four gate commands, which pass: `ruff check`, `ruff format --check`, `mypy`, and the full suite at 1378 passed.

- **`AGENTS.md`** — the reform's pointer list stands; `main`'s Feature wording was folded into the `docs/rules/skills.md` line, since the merged module now holds the Feature rules.
- **`tests/support/contract.py`** — kept `main`'s new `PYTHON_STANDARD`, retargeted to `docs/rules/python.md`.
- **`tests/test_adr.py`** — the relation machinery and the refusal-clause constants stay removed. `main` had only added two `RELATIONS` entries inside a block #272 deleted; the deletion is the settled decision and it wins.
- **`skills/kntnt/scripts/kntnt.py`** — `main` removed the `integrations` key from `verified_outcome`'s uncheck return and the branch had only renumbered the comment that went with it, so `main`'s code stands; `main`'s docstring paragraph on `integrations`/`removed_integrations` was kept with the branch's renumbering.
- **`skills/models/model-selector/scripts/capture.py`** — `main`'s stderr paragraph kept, at the branch's ADR number.
- **`CHANGELOG.md`** — the Unreleased section was rebuilt heading by heading, branch entries then `main`'s, rather than union-merged into whichever heading the conflict happened to sit under.
- **`skills/kntnt/catalog.json`** — regenerated, never hand-resolved. It is a declared generated file.
- **`docs/adr/0090-…`** — deleted in this branch, modified on `main` (`main` had added an *amended by ADR-0173* pointer to it). The fold stands and the record stays deleted.

**Ten record numbers `main` cites were deleted by #272**, and every live citation of them was repointed to the consolidation that absorbed it: 0003, 0036, 0043 → **0175**; 0061, 0076 → **0177**; 0112 → **0178**; 0090, 0157, 0160, 0167 → **0179**. Records under `docs/adr/` were not rewritten — `test_every_cited_number_has_a_record` exempts the archive by design, a number inside a record being an address as of that record's date.

**`main`'s new `Feature` glossary entry legislated**, which #265's reformed `CONTEXT.md` forbids, and `test_no_entry_states_the_law_a_rules_module_holds` caught it at five sentences. Two rules it carried had no home anywhere under `docs/rules/` — *a Feature is Global only* and *its Enabled state is what its Harnesses hold, never a file on disk* — so both were written into the `## FEATURE.md` section of `docs/rules/skills.md` before the entry was trimmed to a definition and a pointer. Nothing was dropped.

**Wave 9's `<since>` is no longer an ordinary one.** `eb624138950d26feca6a05eec46a9b85d0c27ee8` still marks the last clean wave pass, but the merge commit now sits between it and the head, so that range holds #272's work *and* everything the merge brought into the same files. Brief the check knowing it reads both — it is more than a wave check normally takes on, and the alternative, reading only #272, would skip precisely the files the merge touched.

## What the run learned that the Skill does not tell you

**The engine reserves one record number per ticket.** #269 and #270 each wrote two records and the brief's own instruction for that case is to stop and report. Both times the run appended a second entry to `.git/kntnt-orchestrate/<n>.reserved.json` and re-ran `isolate`, which then reports both. #273 writes one record and needs no such repair. Do not let a builder read the directory for "next free" — another session is allocating numbers in this same repository and holds some of them.

**Five sessions ended their turn mid-suite and had to be resumed.** The brief tells every subagent that a long command is waited on rather than yielded to, in two paragraphs, and it is not enough. When it happens: check whose processes are actually alive (`lsof -a -p <pid> -d cwd -Fn`) before assuming the suite is the builder's — other sessions run `pytest -n auto` in other checkouts — then wait for the real result and resume the agent with it via SendMessage. Do not let a resumed builder commit on a gate result it never saw.

**The suite has a load-induced flake** under `pytest -n auto`: `shutil.copytree` racing a transient `__pycache__/*.pyc.<pid>` another xdist worker is writing. Seen by two builders on different tests, never by a wave check. Always rerun a single failing test in isolation before concluding anything.

**`CHANGELOG.md` is the run's own file.** Builders write their entry to `.kntnt-orchestrate/<number>.md` and the run applies it after the wave merges. Builders have written that note in three different shapes — a bare path line, a `## \`CHANGELOG.md\`` heading with the section named in prose beneath, and a single line carrying both path and section. Whatever applies them must accept all three and fail loudly on a shape it cannot parse; a silent no-op there loses a release entry.

**`/orchestrate`'s prose and its engine disagree about fix rounds.** The Skill says to re-run the wave check after a fix and act on the verdict "exactly as this step acts on the first", which allows several rounds per wave. `run.py` accepts only `wave-fix-<wave>` as a plain integer and refuses to restart a completed request. This run numbered them sequentially, so `wave-fix-1` … `wave-fix-9` count rounds rather than waves in the evidence ledger. The Cohort and observations are correct; only the wave correspondence in the identifier is lost.

## Findings settled by earlier wave checks

Carry these into every wave-check brief so they are not relitigated. Each may be re-raised only on grounds the earlier reading did not have.

- Record numbers `0173` and `0174` are no longer free and no longer a gap: the merge brought both in from `main` as real records. `0173` had expired with wave 1's reservation and `0174` was the other session's live ticket — that ticket has landed. The branch's own consolidations start at `0175` and are unaffected.
- `tests/test_adr.py`'s relation machinery was removed by #272 along with the outrun-pointer duty #267 retired. Settled.
- Records folded into a consolidation but cited in no rules module are not charged; the module-citation check is scoped by its own documented reasoning.

## Decisions the maintainer made during the run

1. **Builders run on Opus 5.** Asked before the first frontier was frozen, because the cold-start heuristic would otherwise have put Haiku 4.5 on a series that rewrites every shipped file.
2. **`docs/rules/docs.md` keeps its rule that `AGENTS.md` routes rather than legislates**, and names the `## ⚠️ TEMPORARY` rework section as its one standing exception — self-removing when that section goes.
3. **Four normative sentences #265 stripped from `CONTEXT.md` were restored** into the documents holding their terms' law. The fifth — "Redline and Unslop carry the same contract" — was dropped permanently, because ADR-0178 records the opposite decision and the glossary sentence was a simplification the record contradicts. Its absence is intended.
4. **The `RUNTIME` bin was widened** from *cited by `run.py` or `tests/test_orchestrate.py`* to *is `/orchestrate`'s own machinery*, with such a citation sufficient but no longer necessary, and nine records moved out of `DROP`: 0050, 0056, 0057, 0084, 0139, 0141, 0142, 0143, 0144. Without it #272 would have deleted the parked-ticket resume, the approval ceiling and the flake protocol.

## Open items worth a ticket, found during the run and not fixed

- **A ticket that writes N records needs N reservations.** Nothing in the engine asks how many a ticket will write.
- **`skills/kntnt/scripts/kntnt.py`'s `validate_manager_candidate`** does not list `library/references/invocation-envelope.md` among the Manager's required files, so a staged Manager missing the file every Skill now reads still validates. Declined by three wave-check rounds as a decision rather than a restatement.
- **The parallel test gate's `copytree` flake**, above.
- **`RUNTIME` now means "is orchestrate machinery, or is cited by it"**, and seven records — 0005, 0029, 0030, 0067, 0083, 0089, 0099 — are in on the second clause alone while their subject is not `/orchestrate`'s machinery. Narrowing it would falsify the six consolidation records already merged, so it is a ticket against those, not a table edit.
- **`docs/rules/docs.md` states that `AGENTS.md` holds no rules** while the TEMPORARY section does. The exception is named, but when the rework branch is deleted both the section and the exception clause go together.
