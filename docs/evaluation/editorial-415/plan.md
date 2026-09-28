# Plan for #415: a headline, subheading or standfirst that asserts past a limit the text keeps

Frozen on 2026-09-28, before the first run of either arm and before any product wording is written or committed. Nothing in this file, in the two turn files, in the three judge briefs beside it or in `runs/turn_run.sh` is edited after the first run; `results.md` and the `runs/` tree are written as the work produces them. Read [the protocol](../protocol.md) and [the corpus](../corpus/editorial-quality/README.md) first, then [#383's plan](../editorial-383/plan.md), whose method this one copies, and [#400's plan](../editorial-400/plan.md) with [its amendment](../editorial-400/plan-amendment.md), whose staging this one re-uses; this file says only what those leave open and what #415 settles differently.

**`<start>` is `708bff52`**, the head of the branch `kntnt-orchestrate/main/415` when the build began. #397, #398, #400 and #402, the four tickets the thread orders this one after, are closed and their changes are in it. The pre-change arm is staged from it. **The corpus commit is `708bff52` too.** Every input and every frozen expectation is read from it, and this ticket's diff does not touch the corpus.

The requirement is the ticket's thread as it stood on 2026-09-28: the body, the triage comment of 2026-09-23 06:36 UTC, the addendum of 19:22 UTC on the block, the readiness addendum of 19:39 UTC and its clarifications of 19:56 UTC. Where they conflict, the later one stands.

## The ruling, and why

The body asks first whether the form is a defect at all. The readiness addendum settles it, and this evaluation does not judge the question again.

**The form.** A headline, a subheading or a standfirst that the run wrote or changed asserts past a limiting sentence the text keeps: sharper, more general, or a conclusion that sentence withholds. The limiting sentence itself survives byte for byte. The limit then reaches the reader as a qualification of something already asserted flatly above it.

**It is a defect.** Two rules the collection already ships forbid it:

- [`headlines.md`](../../../skills/kntnt/library/references/editorial/headlines.md), *Every word supported* (line 27): *A headline claims only what its text claims. Every figure, name, claim and conclusion in it is in the text, at the text's own strength: never sharper, never more general, never a conclusion the text does not draw.* Line 3 of the same file says *headline* covers a text's subheadings too.
- [`base.md`](../../../skills/kntnt/library/references/editorial/base.md), *Claims*: every claim has *proportionate strength* (line 23), and *This boundary holds in the title, summary, headings and body alike. Preserve chronology, scope and qualifications wherever a claim appears.* (line 27).

A part that asserts past a limit the body keeps states the text's claim at more than the text's own strength, which both rules name. A part that asserts no more than the kept limiting sentence allows, with the limit below it, is ordinary structure and is not the form.

**No new rule is written.** The rule exists. What does not see the form is Redline's *limit rule*: what it ships on limiting sentences, in `skills/kntnt/library/references/editorial/base.review.md`, step 7 of `skills/editorial/redline/SKILL.md`, the paragraph *What a repair may take with it, and what it may not* in `skills/editorial/redline/references/correction.md`, and `skills/editorial/redline/help.md`. The limit rule tests edits to the limiting sentence itself: the sentence going, being weakened or being recast. A part added or changed above a sentence that survives meets it.

The options the addendum did not choose were:

- to rule the form ordinary structure, rejected because the two rules above already forbid it;
- to write a new rule in the article anatomy or in Write, rejected because every instance was written by a Redline run, no Write run shows the form, and a second rule would answer it twice.

The addendum marks that ruling as decided in Thomas's absence and open to his review.

## What is under test

**The candidate, written only if the pre-change arm shows the form.** The limit rule names the form in one clause — a headline, subheading or standfirst that asserts past a limit the body keeps — and points at `headlines.md` *Every word supported* and `base.md` *Claims*, saying nothing more about what those rules require. It changes these four places and nothing else in the product:

- `base.review.md`, the paragraph on a sentence that bounds what the text asserts: the form is a defeat of that limit from above, by a part the run wrote or changed. The finding lies in that part, and the limiting sentence stays exactly as it stands. The pointer names `headlines.md` for the genres that load it.
- `redline/SKILL.md` step 7, the bullet carrying the permission for limiting sentences: the same form beside that permission, with the same pointer. The existing handling of a finding a round created — the last bullet of step 7 and the loop's third stop condition — applies to it unchanged.
- `redline/references/correction.md`, the paragraph on what a repair may take with it: the same form as something a repair must not write, with the same pointer. The paragraph before it already names *a headline or a heading claiming more than the text claims* as the subagent's own defect, and is not restated.
- `redline/help.md`, the sentence stating the limit-edit rule: the form added in a sentence of its own.

Each place is found by its content, not by a line number. `headlines.md` is loaded only for `article`, `case-study`, `column` and `opinion`, so a pointer to it names those genres. No file is added to any load list. `headlines.md`, `base.md` and `article-anatomy.md` do not change, nothing under `skills/editorial/write/` or `skills/editorial/unslop/` changes, and #400's account rule, which names what a removal costs the reader, is not the sentence changed. The exact wording is written after the pre-change arm has been judged and is recorded in `results.md` with its commit.

**Unslop is not measured here**, and is out of scope whatever its label says: it writes no headline, subheading or standfirst.

## How a run is made

Provider family `claude`, in Claude Code 2.1.283, from a Claude session. [The protocol](../protocol.md) forbids a Claude session from starting, controlling or invoking a Codex Harness or a GPT model, and none is.

This build's session is itself a subagent, and a subagent of it has no tool for starting Redline's correction subagent, as [#397's amendment](../editorial-397/plan-amendment.md) found. So every Redline run is a fresh **top-level** Claude Code session, `claude --print --model=claude-opus-5-5 --effort=high`, started by [`runs/turn_run.sh`](runs/turn_run.sh) and sent a turn file, as #383's plan dispatches a turn. No criterion here is answered from a Harness trace, so [`../editorial-388/harness/staged_run.py`](../editorial-388/harness/staged_run.py) is not used.

- **The seat.** `claude-opus-5-5` at high deliberation for the session. Its correction subagents and its nested Proofread pass run inside that session and take its seat. Where #383's plan says `claude-opus-5`, this evaluation launches `claude-opus-5-5`, as the readiness addendum settles. `turn_run.sh` writes the model each session and nested agent ran to the run's `seats.tsv`, and that file, not the request, is what the record names. Every judge is a fresh subagent of type `kntnt-opus-high`, which launches the same model at the same deliberation.
- **The runner.** `runs/turn_run.sh` is #400's `runs/turn_run_2.sh` with its two inventory calls taken out, because this evaluation scores no criterion on an inventory. It gives each session a private root as its home, configuration, temporary directory and caches; copies the staged install's `proofread/` into that home's `~/.agents/skills/` so that Redline's dependency check is met by the Proofread the run follows, as #400's amendment found necessary; passes `claudeMdExcludes` for `/Users/thomas/.claude/CLAUDE.md`, `/Users/thomas/Projects/skills/CLAUDE.md` and `/Users/thomas/Projects/skills/AGENTS.md`; strips every `CLAUDE_*`, `ANTHROPIC_*` and `KNTNT_*` variable; and removes the private root on every exit.
- **The installs.** Each is written with `git archive` from the commit it names, never copied from a working tree, and extracted flat into this build's scratch root, `<scratch>` = `/Users/thomas/Projects/skills/.git/kntnt-orchestrate/415.scratch`. `skills/editorial/{write,redline,proofread,unslop}` are extracted with `--strip-components=2`, and `skills/kntnt` with `--strip-components=1`, so that each Skill's directory and `kntnt/` stand side by side and the shim finds `HERE.parent / "kntnt"`. The clarifications' example strips `skills/kntnt` by two components too, which would spill the Manager's files into the install's root; one component gives the layout the same sentence asks for, as #400 found. `<scratch>/install-pre` is `<start>`. `<scratch>/install-post` is the committed candidate, staged only after the candidate is committed. A revise round's install is `<scratch>/install-revise`, from the committed revised wording.
- **The turn files.** [`redline-turn-pre.md`](redline-turn-pre.md) and [`redline-turn-post.md`](redline-turn-post.md) are #383's with two substitutions and no other change: `<scratch>/install-pre` and `<scratch>/install-post` in place of #383's install paths, and `/Users/thomas/Projects/skills-rework` in place of `/Users/thomas/Projects/skills-388-391`, which no longer exists. The checkouts a run may not read are every path `git worktree list` showed at the freeze: `/Users/thomas/Projects/skills`, `/Users/thomas/Projects/skills-rework`, `/Users/thomas/Projects/skills/.git/kntnt-orchestrate/414` and `/Users/thomas/Projects/skills/.git/kntnt-orchestrate/415`. The two turn files name the first two, and the other two lie under the first. A revise round's turn file is `redline-turn-post.md` with `install-revise` in place of `install-post`, written when the round is taken; that is a path substitution too. No turn names the seat.
- **The message.** The prompt is the turn file, a line `---`, and three lines naming the working directory, the invocation the user typed and the run directory, as `turn_run.sh` writes it to `prompt.txt`. Nothing else is added. No hint of the defect under investigation appears in any turn or any invocation.
- **Where runs execute.** Under `<scratch>`, as the clarifications settle. A run has the run directory `<scratch>/runs/<run>/`, whose `work/` is its working directory, holding `input.md` and nothing else when the session starts, and whose `scratch/` is the only scratch the turn allows. Its packet is `<scratch>/packets/<run>/` and its private root `<scratch>/env/<run>`. Each run directory is copied into this evaluation's `runs/` only after its judging is done.
- **One run per input at a time.** Runs on different inputs run side by side, at most five at once. The two runs of one draft in one arm, and a revise run, are made one after the other, never beside another run on the same input. The sibling ticket built beside this one makes no evaluation runs, so no lock outside this build's scratch root is taken.
- **The reply.** The turn asks the run to save its reply verbatim to `response.md` in its run directory. `turn_run.sh` also keeps the reply the Harness returned, as `response.txt`. Where the two differ, `results.md` says so, and the judges read `response.md`.

## The matrix

The four drafts are `docs/evaluation/editorial-362/runs/{column-sv-r1,column-sv-r2,opinion-en_GB-r1,opinion-en_GB-r2}/redline/work/input.md`, copied byte for byte. Each carries its own `kntnt` map, so the invocation names no genre and no language. The ten controls are the ten rows of the corpus's *Redline controls* table, staged as the corpus says — only the linked artifact as `input.md` — and invoked as #383's matrix invokes them, with no contextual instruction and no technique.

| Input | SHA-256 (first 16) | Invocation |
| --- | --- | --- |
| `column-sv-r1` | `4fe7a78864930951` | `/redline --output=response input.md` |
| `column-sv-r2` | `74b966f1352c4f42` | `/redline --output=response input.md` |
| `opinion-en_GB-r1` | `02171183566bb9a1` | `/redline --output=response input.md` |
| `opinion-en_GB-r2` | `cfefda44d50dcb42` | `/redline --output=response input.md` |
| `article-clean` | `f183e6da31cf7808` | `/redline --genre=article --language=sv --output=response input.md` |
| `article-flawed` | `1c0e3b3ef98e06b2` | `/redline --genre=article --language=sv --output=response input.md` |
| `case-study-clean` | `32037623b16754f3` | `/redline --genre=case-study --language=sv --output=response input.md` |
| `case-study-flawed` | `ce574061bd09328e` | `/redline --genre=case-study --language=sv --output=response input.md` |
| `column-clean` | `98b65197fa9dd800` | `/redline --genre=column --language=sv --output=response input.md` |
| `column-flawed` | `9b12ad3fb2cb7401` | `/redline --genre=column --language=sv --output=response input.md` |
| `opinion-clean` | `179cc9615d2aa633` | `/redline --genre=opinion --language=sv --output=response input.md` |
| `opinion-flawed` | `ab033d9f4c817c9e` | `/redline --genre=opinion --language=sv --output=response input.md` |
| `web-copy-clean` | `8de234f1c80fe947` | `/redline --genre=web-copy --language=sv --output=response input.md` |
| `web-copy-flawed` | `a5470e4b3aea20a0` | `/redline --genre=web-copy --language=en_US --output=response input.md` |

| Arm | Turn file | Runs |
| --- | --- | --- |
| pre | `redline-turn-pre.md` | `pre-<draft>-a` then `pre-<draft>-b` on each draft; `pre-control-<row>` once on each control. 18 runs |
| post | `redline-turn-post.md` | `post-<draft>-a` then `post-<draft>-b` on each draft; `post-control-<row>` once on each control. 18 runs, made only if the pre-change arm shows the form |
| revise | the revise turn file | only if a revise round is taken; see *Exit* |

The pre-change arm runs each draft twice, not once as #383's did, so that the two arms have the same shape and "fewer" below is a plain count.

**A clean control is run once, not twice.** The protocol's rule on a clean control asks for a response-target and a file-target run. The ticket fixes #383's matrix, so only the response-target run is made, as in #383, #397, #398, #400 and #402. That is a declared narrowing.

## Judging

Two independent judges per brief per judged run, each a fresh `kntnt-opus-high` subagent, blind to the arm, to the model, to the expected verdict and to this ticket. The two judges of one run on one brief are dispatched together and are not told of each other.

- **The paratext brief.** [`paratext-judge-brief.md`](paratext-judge-brief.md) is new, and is frozen with this file. It carries the frozen run brief's opening rules — read only `work/input.md` and `response.md`, and know nothing of the arm or the model — its definition of a limiting sentence verbatim, what the question's three parts are, and one question: *Does the returned text contain a headline, a subheading or a standfirst that the run wrote or changed, one absent from `work/input.md` or worded differently there, that asserts past a limiting sentence the returned text keeps: sharper, more general, or a conclusion that sentence withholds?* The judge answers `yes` or `no`, and for each yes quotes the part and the limiting sentence and says in one line what the part asserts that the sentence bounds. It names neither this ticket nor any name a judge of #383 gave the form. **Every run of every arm, controls included, gets two judges on it**, writing `paratext-a.md` and `paratext-b.md`.
- **The frozen briefs.** [`redline-judge-brief.md`](redline-judge-brief.md) and [`control-judge-brief.md`](control-judge-brief.md) are byte copies of #383's. The first judges the draft runs and decides `R1` and `N1`, and the second judges the control runs and decides `C1`, with two judges per run writing `judgement-a.md` and `judgement-b.md`. They are run over the pre-change arm only where that arm shows the form, and then over every run of the post-change arm and of any revise round. A control judge's message carries the row's frozen expectation as one paragraph headed **Frozen expectation**, as that brief says: the row's *Frozen expectation and rejection* cell in the corpus README at `<start>`, copied verbatim to the run's `expectation.md`.
- **Neutral paths.** Each judge gets a directory of its own made by `mktemp -d` under the system temporary directory, whose path names neither the arm, the input, the run nor this ticket, holding `work/input.md` and `response.md` copied from the run directory, and a copy of its brief, and nothing else. The dispatching message names that directory, the brief's path in it and the judge's letter, and tells the judge to keep any scratch of its own there. Its judgement is copied into the run directory under the name above, the mapping from directory to run and brief is kept in `runs/judges.tsv`, and each directory is removed once its judgement is copied. This is the one departure from the build's confinement to its worktree and its scratch root: a `mktemp -d` path is unique, so no other session can have chosen it, and a path under the scratch root would name this ticket. #385, #398 and #402 made the same departure.

## Criteria, fixed before the runs

### The form, and how a run counts

This is the criterion a later evaluation re-uses to measure the form without re-deriving it: the paratext brief, and this counting rule.

- **A run counts** when both of its paratext judges answer `yes`. This is the split rule of the copied plan, under which neither judge is an oracle.
- **A split** — one `yes`, one `no` — is recorded with both readings and does not count, in either arm.
- **A part the run wrote counts** even where writing that part was #397's behaviour, a part a finished text lacked written into it. That writing is recorded under #397 as well.
- **An arm's count** is the number of its 18 runs that count. It is this ticket's target criterion.

### The frozen criteria

- **`R1`** on each draft run, and **`C1`** on each control run, as the judges give them under heading 4 of their briefs.
- **`N1`** on each draft run, as #377's plan defines it: no limiting sentence is deleted or hardened unless the account reports a finding of class (a) or (b), verified by a judge from the input text alone.
- Where the two judges split on `R1`, `N1`, `C1` or on whether a control passed, **the stricter judgement governs**, as #377's plan says. Both readings are recorded.
- `A1`, `A2`, `N2`, `O1` and `S1` are recorded `skipped` on every run: this is not their evaluation, as the clarifications settle, and no inventory is taken. `C2`, `T1`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2` and `T2` are recorded `skipped` too, naming the paratext count, `R1`, `N1` and `C1` as this evaluation's criteria.

### The limiting sentences already protected

The sixth acceptance criterion as amended: no limiting sentence is deleted, weakened or hardened in a post-change draft run where it survived in the in-session pre-change draft runs. Read it this way:

- Limiting sentences are the ones listed under heading 3 of the frozen run brief, matched across judges and runs by their text in `work/input.md`.
- A limiting sentence **survived** in the pre-change arm when it survived in both pre-change runs of that draft, by the stricter judge.
- In a post-change draft run it **fails** when either judge reads it deleted or weakened under heading 3, or hardened, read from heading 1 where heading 3 has no such answer.
- The criterion holds when no surviving sentence fails in any post-change draft run.

### Whose miss

A miss caused by a behaviour another ticket was filed against is recorded under that ticket's number and not counted against this one: #397 (paratext authored into a finished text), #398 (the claim account's assurance, and a claim the run added), #400 (a paratext change accounted for as something else) and #402 (anatomy conformance reported unexamined). The same reaches the tickets filed from these inputs since, each only for exactly its own shape, among them #429 (a working column headline reworded under the headline contract), #430 (`article-clean` or `column-clean` returned with a rewritten headline), #431, #432, #433, #434, #435, #436 and #437. Both judges' readings are recorded. The paratext count is the exception the addendum makes: a run counts by the rule above even where #397's behaviour wrote the part.

## Sequence and exit

1. **The pre-change arm first**, all 18 runs, judged by the paratext brief only.
2. **Not reproduced.** Where no pre-change run counts, the result is *not reproduced*. No product file changes. The decision record, ADR-0223, says so, as ADR-0212 did for #363 and ADR-0214 for #364. The paratext brief and this counting rule stay as the criterion later evaluations use. The frozen briefs are not run over that arm, no post-change arm is run, and the ticket is done.
3. **Reproduced.** Where any pre-change run counts, the pre-change arm is judged by the frozen briefs as well. Then the candidate is written, committed and staged, and the post-change arm is run and judged by all three briefs, four judges a run.
4. **The pass mark.** The candidate meets this ticket's criteria when all three hold:
   - fewer of its 18 runs count than of the pre-change arm's 18;
   - none of its ten control runs counts;
   - the limiting sentences already protected are, as read above.
5. **One revise round**, at most, where the candidate misses the pass mark. The revised wording is committed first and staged to `install-revise`. The round reruns every post-change draft run that counted, under the name `revise-<draft>-<letter>`, and every control, as `revise-control-<row>`, all judged by all three briefs. The revised arm is the post-change arm with each rerun run replaced by its revise run, so its count is over the same 18-run shape, and it is compared with the pre-change arm's count.
6. **What ships.** The wording read last — the candidate, or the revised wording where a round was taken — ships where its arm meets the pass mark. Where it does not, it ships only where its arm's count is lower than the pre-change arm's, no control that passed in the pre-change arm fails in its arm, and the limiting sentences already protected are. Where the revised wording fails that, the candidate is read by the same test on the post-change arm. Otherwise the product stays as it is, and the candidate is reverted by a commit of its own. A control **passed** in an arm when it meets `C1` by the frozen control brief there and does not count. The limiting-sentence protection is held on every route, because it is an acceptance criterion of its own and not the target.
7. **Either way**, the result is written down as measured, each remaining miss is filed as its own `needs-triage` ticket naming #415, and the ticket is done.

No criterion is softened, no frozen plan, brief, turn file or fixture is edited to fit a result, and no arm is re-run to get a better reading.

**Void runs.** A run or judge cut off by a usage limit, an HTTP 5xx or an overload is void, not a finding, and is rerun. A void run's directory and packet are moved whole to `voided/` beside `runs/` before its input is run again. A run that completes and stops is a finding.

## What is written

This file, the two turn files, the three judge briefs and `runs/turn_run.sh`, committed before the first run.

`results.md` beside them holds the outcome whichever way it falls, and states in one place the four instances #383's judges named, in the collection's terms, located in their runs' `response.md` against `work/input.md`.

The judged run directories go under `runs/`. Each holds `work/input.md`, `response.md`, `response.txt`, `prompt.txt`, `seats.tsv`, `run.json`, `result.json`, `exit.json`, `expectation.md` for a control, `paratext-a.md` and `paratext-b.md`, and `judgement-a.md` and `judgement-b.md` where the frozen briefs were run. Beside them is `runs/judges.tsv`, and any void run goes under `voided/`. The transcripts `turn_run.sh` keeps are read for `seats.tsv` and are not committed.

One record goes to `../records/redline-claude-<date>-415.md`, in the protocol's format, where `<date>` is the date of the first counted run. The record's line for `../records/README.md` is appended by the run that integrates this build. Nothing else already under `docs/evaluation/` changes.
