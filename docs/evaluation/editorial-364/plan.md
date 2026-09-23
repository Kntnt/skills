# Plan for #364: a bridge prepares a quotation rather than pre-says it

Frozen on 2026-09-22, before the first run of either arm and before any product change. Base: `main` at `218e3be1`.

The ticket's readiness addendum of 2026-09-20 is the requirement wherever it touches the body, and this plan is written against it. What the addendum names as frozen is frozen here: the three-row matrix with its two arms and per-arm run counts, the judge briefs with the (a)/(b)/(c) classing, and the re-run allowance for a stop unrelated to the bridge. Nothing in this file or in `runs/*-judge-brief.md` is edited after the first run.

## The failure

On product `5ecadb76`, in the GPT family, the run `case-question-en_GB-r1` introduced its last quotation with

> Asked about choosing the system again and what to change, Vale's endorsement was specific to new jobs, with more time allowed before extending its use:

and the quotation it introduces is

> I would use it again for new jobs. I would allow another week to check the status names before adding the backlog.

The bridge says both judgement points before the speaker does. F1 passes — the question was really asked and the content is in the source. G2 fails: narrative and quotation do the same work twice. The question framing itself is legitimate and is not the defect; this is not the invented-question defect of #352.

A separate source-blind Redline run on the same revision repaired the bridge to `Asked about choosing the system again and what to change, Vale said:` with the quotation and the rest of the text intact. **That repair is an example and not a prescribed wording**, and it does not pass the Write draft retroactively.

## What the product already says

Two shipped surfaces state the rule at issue and no others:

- `skills/kntnt/library/references/editorial/genres/case-study.md` — "Let attributed quotations carry the customer's experience and judgement, with narrative doing the connecting work. A bridge should prepare a quotation rather than pre-say it."
- `skills/kntnt/library/references/editorial/genres/case-study.review.md` — "Read bridges beside quotations and the standfirst beside the body's opening. Remove a redundant pre-echo while keeping the attribution and any distinct fact."

Both are byte-identical to the evaluated revision. The requirement therefore already exists, and the body is explicit that restating the same rule is not an explanation. A candidate has to do something the present wording does not.

## What has moved under the ticket, and what the product under test is

The product under test is `main` at `218e3be1`, not the `5ecadb76` the body describes. Three differences matter and are recorded rather than corrected:

- `skills/editorial/write/references/source-check.md` was rewritten for #362 and has changed twice since the addendum, so the addendum's word figure for it is stale. The comparison now pairs each draft passage with the source passage it rests on; a completed comparison stands when a further one fails, and the delivery rule turns on the last comparison the run **completed**.
- `9a29bad3` added the article-anatomy measuring script. Write's `SKILL.md` steps 7–9 became 8–10, so a step number quoted in the ticket may be one lower than the step it means.
- `skills/editorial/write/SKILL.md`, `skills/editorial/redline/SKILL.md` and `skills/editorial/redline/help.md` carry the caller-recovery text of ADR-0198, which landed for #328. It is neither new nor this ticket's concern.

The two-comparison cap and the delivery gate belong to [#376](https://github.com/Kntnt/skills/issues/376) and are not touched here.

## The hypothesis

Not that the rule is missing, but that it is abstract where the composing step needs a test. `pre-say` is a coined verb with no reader-facing question behind it, and it sits two sentences after an instruction that tells the narrative to do the connecting work — which a writer can satisfy by summarising what the quotation is about to say. The same collection already states the identical shape of rule concretely one resource away, in `article-anatomy.md`: "A reader who has just read the standfirst meets the lead as new material, never as the standfirst said again."

So the candidate family is: **give the bridge rule the reader test the anatomy gives the lead, and name what a bridge may carry, without prescribing a sentence and without forbidding bridges.** The alternative the body also offers — removing an existing over-steer rather than adding to one — is in the family and may be what is tried.

**The exact candidate wording is deliberately not frozen here.** It is written after the baseline arm and before the candidate arm, from what the baseline drafts actually do, and is recorded in `results.md` with the diff it corresponds to. It is not in the addendum's frozen list, and where the baseline arm takes exit 1 below there is no candidate at all. What is frozen is that no canonical replacement sentence is written into any surface, no quotation quota is introduced, no general prohibition on bridges or on subject orientation is introduced, and no extra genre review is added to Write's source comparison.

## How a run is made

Provider family `claude`, in Claude Code, from a Claude session. [The protocol](../protocol.md) forbids a Claude session from starting, controlling or invoking a Codex harness or a GPT model, so nothing here runs `editorial-329/harness/run.py`; the ticket's pointer at it is read as history. The GPT-family failure this ticket inherits stays failed and is not retested. A GPT-family retest is Thomas's own step, ordered separately.

The staging is the method frozen in [`../editorial-362/runs/plan.md`](../editorial-362/runs/plan.md) and reused by [#363](../editorial-363/plan.md):

- A byte copy of `skills/editorial/{write,redline,proofread,unslop}` and `skills/kntnt` side by side in a private staging directory, so the shim finds the Manager beside the Skill and no global install is read. One staged install per arm: `install-baseline` is `main` at `218e3be1` unchanged; a candidate install is that tree plus this ticket's change and nothing else.
- The turn names the staged `SKILL.md` as its instructions and `$HERE` as its directory, and carries the Formal Invocation verbatim. The staged copy is not an installed Skill, so the Skill tool cannot start it.
- One working directory per run, holding only `source.md` (Write) or `input.md` (Redline) and nothing about where it came from.
- A `sha256` inventory of every writable location staged for the run — the whole working copy, the run directory and the staged install — before and after.

**The seat.** Every run is a fresh top-level Claude Code session started from the shell: `claude -p` with the turn as its prompt, the child-session environment variables unset so the session is not a child, the working directory set to that run's `work/`, and Claude Code's own `--model`, `--effort` and `--permission-mode` flags set to `claude-opus-5`, `high` and `bypassPermissions`. This is what the addendum's "a fresh `claude-opus-5` subagent at high deliberation" has to be here: both Skills declare `kntnt.capabilities: "subagents"`, and a subagent of this harness has no agent-spawning tool, so a Write run started in a subagent seat stops on the unsatisfied capability and a Redline run completes without the fresh correction seat its contract requires. #363 voided ten attempts over this ([#394](https://github.com/Kntnt/skills/issues/394)) and recorded the session seat as the harness that works. The model and the deliberation level are the ones the addendum names; the seat is a session rather than a subagent, and that is the declared difference.

Judges are fresh subagents of type `kntnt-opus-high` (`claude-opus-5`, high deliberation) with no history, which need no seat of their own because they start nothing.

Four evaluator additions to each turn, declared here because they are not the Skill's and each is visible in the run directory as a file the Skill did not write:

1. Copy Write's source-check scratch, and Redline's private mechanical input and result, to `evidence/` before the Skill removes them.
2. Save the complete user-facing reply verbatim to `response.md`.
3. Save the delivered text to `delivered.md`, exactly as the reply carries it and with nothing added, and write nothing there where the run delivered nothing.
4. Write the UTC timestamp to `finished.txt` on ending; the launcher writes `started.txt`.

## The frozen matrix

Three rows, two arms. The list is exhaustive for this ticket. Every delivered draft additionally gets one paired fresh source-blind Redline run on the delivered artifact, invoked `/redline --output=response input.md`.

| Row | Input | Write invocation | Runs per arm |
| --- | --- | --- | --- |
| `case-question-en_GB` | the bytes of `../editorial-329/followup/runs/account-candidate/case-question-en_GB-r1/write/supplied-input.md`, SHA-256 `75160dbc12d41294eccfc615f4a8e1b2df1b5202185f5ba1f24a2f3d5fd69afc`, which the tree matches | `/write --genre=case-study --language=en_GB --output=response source.md` | 3 |
| `case-study-en_US` | `../corpus/editorial-quality/sources/case-study.md` | same with `--language=en_US` | 2 |
| `case-study-sv` | the same corpus source | same with `--language=sv` | 2 |

The first row is the case the fault was found in. The other two are the positive controls: that corpus source prints its quotations without their questions, so an authentic question cannot be quoted there and must not be invented — this is the body's *källa utan lämnad fråga*. The Swedish row is in because a change to a shared genre resource reaches every locale that loads it; it is known to stop, or to carry a defect, for the idiom question of #363, which measured that this family does not reproduce it.

A run that stops for a finding **unrelated to the bridge** is recorded as a stop with its reason and its wall time, is not counted against this ticket's criterion, and **that row may be re-run once**. No other row is re-run, no arm is re-run to get a better reading, and every run is kept whatever it shows.

## What the judges are asked

Each delivered artefact is judged by **two** independent judges, blind to the expected answer, to the hypothesis, to this plan and to any model identity. Where they split, both classes are recorded, no judge is an oracle, and the row counts as unmet. A mechanical question — byte identity, a count, whether a file is present — takes one judge.

For every bridge that introduces a quotation, a judge classes it as exactly one of:

- **(a)** it states what the quotation then says, adding no understanding of its own;
- **(b)** it names the subject, the occasion or the attribution and no more;
- **(c)** it carries a fact the quotation does not carry.

The judge is not told which class is the defect. Only **(a)** fails. This is the distinction the body asks to preserve and it is what keeps the criterion from becoming a ban on bridges: a subject introduction is not a defect merely because the subject recurs in the quotation, and no canonical sentence is prescribed.

## Criteria, fixed before the runs

- **`K-bridge`**. In the candidate arm, no delivered draft of any row carries a class (a) bridge, on both judges. A stop is never counted as a pass.
- **`K-controls`**. Both positive-control rows run with the fixtures above. Across the candidate arm's positive-control drafts, bridges of class (b) and of class (c) both still occur — the change has not collapsed every introduction into bare attribution — and no draft invents an interview question or any other interviewer utterance the source does not supply. The record states, for each positive-control draft, the bridges it kept and their class.
- **`K-preserve`** (the body's fourth criterion, unchanged). The customer's agency, words, reservations, facts, chronology, metadata and an independently informative lead survive in every delivered draft. No quotation quota, no canonical sentence and no general extra genre review in Write's source comparison is introduced.
- **`K-redline`** (the addendum's fourth criterion). Every delivered draft has a paired source-blind Redline run, judged on `R1` for both repair and preservation. The output target and the cleanup are read from the before-and-after inventory over every staged writable location. The closing mechanical pass is judged from the preserved private input and output in `evidence/` and their byte relation to the delivered artefact. Write and the final text get their own verdicts, and a Redline repair passes no Write draft retroactively.
- **`K-chain`**. Two fresh subagents independently review the whole affected load chain rather than the diff, and their reports are filed under `reviews/`.
- **`K-cost`**. The word delta of the files actually changed, the resulting mandatory reading for a `case-study` run, and measured wall times per arm. A wording that adds reading ships only where the candidate arm removes a miss the baseline arm reproduced; otherwise the shorter wording ships.
- **F1, G2, L1** from [the corpus README](../corpus/editorial-quality/README.md) on every delivered draft, and **R1** on every Redline pair, so that a repair to composition is not bought with a fidelity, genre or idiom defect.

**`T1` and `R2` are recorded `skipped`**, with the reason that a subagent's transcript is not readable from the session that started it. Nothing here claims either passed and nothing is failed for lacking them; the loading question is carried instead by the independent load-chain reviews under `reviews/`.

A finding of a shape another open ticket owns — [#377](https://github.com/Kntnt/skills/issues/377), [#383](https://github.com/Kntnt/skills/issues/383), [#388](https://github.com/Kntnt/skills/issues/388), [#389](https://github.com/Kntnt/skills/issues/389), [#390](https://github.com/Kntnt/skills/issues/390), [#391](https://github.com/Kntnt/skills/issues/391), [#392](https://github.com/Kntnt/skills/issues/392), [#393](https://github.com/Kntnt/skills/issues/393), [#394](https://github.com/Kntnt/skills/issues/394) — is recorded against that number and is neither fixed nor filed again here.

## The two US artefacts, and what is not this ticket's fault

The body treats one US case as one artefact. There are two:

- `../editorial-329/followup/runs/final-delivery-original/case-study-en_US-r1/` is the clear pre-echo the body's evidence list points at; its `draft.md` reads "Lind's assessment combines a reason to repeat the trial with a reservation about the time allowed:" and its `final.md` reads "Lind said:".
- `../editorial-329/followup/runs/account-candidate/case-study-en_US-r1/` carries the milder cue the body quotes, "Lind's assessment includes a reservation about preparation:". That sentence is in no other draft and not in the directory the evidence list names.

The milder cue is the class (b) case. Redline flattened it to "Lind said:" in that run's `final.md`; that is not a failure of this ticket, which is about Write's draft. A Redline that rewrites a working subject bridge is neither required nor forbidden here, is not counted against the positive controls, and is its own `needs-triage` issue if it is worth fixing.

## Exit

Both exits are the addendum's and are taken as written.

1. **The fault does not reproduce.** If no draft in the baseline arm's `case-question-en_GB` rows carries a class (a) bridge, no product file changes — the body's own rule is that a new general rule needs a demonstrated cause — the non-reproduction is recorded here and in the record, the cross-family reproduction is filed as its own issue labelled `needs-triage` naming #364, and this ticket is done.
2. **The candidate does not measure better.** One revise-and-remeasure round. If the criterion is still unmet, the measured result is recorded as measured, the shipped wording is the better of the two arms, the remaining miss is filed as its own issue labelled `needs-triage` naming #364, and this ticket is done. No criterion is softened to fit a result and no arm is re-run until it passes.

The fault counts as reproduced when at least one baseline `case-question-en_GB` draft carries a class (a) bridge.

## What is written

`results.md` beside this file; the run tree under `runs/`; the independent load-chain reviews under `reviews/`; and records for both Skills under [`../records/`](../records/README.md) in the protocol's format, named with this issue's number after the date. Nothing already frozen is edited — not the corpus, not anything under `editorial-329/`, not anything under `editorial-362/`, not anything under `editorial-363/`.
