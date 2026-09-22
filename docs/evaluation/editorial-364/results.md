# Results for #364: a bridge prepares a quotation rather than pre-says it

Measured against [the frozen plan](plan.md) and the criteria in it. Nothing in the plan or in the judge briefs was edited after the first run.

## What is and is not finished

*Kept true from the first commit onwards, so that a session picking this up after an interruption can see where it stands.*

- **Finished.** The plan, the matrix, the criteria and the two judge briefs, frozen and committed. The baseline (`b`) arm's seven Write runs, all delivered and all judged twice. The seven paired source-blind Redline runs, all delivered and all judged twice. The before-and-after inventory. This file and the two records.
- **Not reached, and why.** The candidate arm, and with it `K-bridge`, `K-controls` and `K-chain`. The baseline took [exit 1](plan.md#exit) — the fault does not reproduce — and where the baseline takes exit 1 the plan writes no candidate wording at all, so there is no change to measure and no changed load chain to review. This is the exit taken as written, not a criterion dropped.

## The harness and the seat

Provider family `claude`. Claude Code 2.1.278. Every run is a fresh top-level session started from the shell with `claude -p`, the turn as its prompt, the child-session environment variables unset, the working directory set to that run's `work/`, and `--model claude-opus-5 --effort high --permission-mode bypassPermissions`. The declared difference from the addendum's "fresh `claude-opus-5` subagent at high deliberation" is the seat: a subagent of this harness has no agent-spawning tool, so both Skills stop on their `subagents` capability there ([#394](https://github.com/Kntnt/skills/issues/394)). The model and the deliberation level are the ones the addendum names.

Judges are fresh `kntnt-opus-high` subagents (`claude-opus-5`, high deliberation) with no history; they start nothing, so the seat question does not reach them. Each delivered artefact was read by two, blind to this plan, to the hypothesis, to the expected answer and to any model identity.

The GPT-family baseline this ticket inherits was measured under native Codex CLI 0.155.1 on `gpt-6-astra/high`. It is not reproduced here and is not retested: [the protocol](../protocol.md) forbids a Claude session from driving a Codex harness. That is the difference from the baseline, stated rather than estimated.

Corpus commit: `218e3be1`.

## What ran

All seven rows of the frozen matrix delivered a draft, and each delivered draft got its paired source-blind Redline run. The staged install is byte-identical before the first run and after the last — `runs/install-b-before.txt` beside `runs/install-b-after.txt` — every row's private scratch directory is empty or removed, and each `work/` holds only its one input file.

Four rows ran twice for reasons that are not the ticket's. `case-question-en_GB-r3` and `case-study-en_US-r1` were killed in an `HTTP 529 Overloaded` window; `case-study-sv-r1` and `case-study-sv-r2` died twice on `API Error: 500`. None of those attempts delivered anything or wrote `finished.txt`. Each was voided whole to [`voided/`](voided/) and the row was re-dispatched from a clean directory holding only `work/source.md`, whose bytes were re-verified against the frozen inventory before dispatch. Six voided attempts are kept there; none reached a judge. This is why those rows' timings sit in a later window than the other three.

| Row | Wall time, Write | Wall time, paired Redline |
| --- | --- | --- |
| `case-question-en_GB-r1` | 12m28s | 9m41s |
| `case-question-en_GB-r2` | 19m31s | 14m24s |
| `case-question-en_GB-r3` | 17m57s | 7m22s |
| `case-study-en_US-r1` | 13m32s | 10m00s |
| `case-study-en_US-r2` | 24m35s | 11m01s |
| `case-study-sv-r1` | 21m31s | 16m08s |
| `case-study-sv-r2` | 18m58s | 16m45s |

## The bridge classing

Every delivered draft, both judges, in the (a)/(b)/(c) classing the plan froze. A quotation standing with no bridge at all is its own answer and is counted separately.

| Row | Judge A | Judge B | Agreed? |
| --- | --- | --- | --- |
| `case-question-en_GB-r1` | (a) 0, (b) 2, (c) 0 | (a) 0, (b) 2, (c) 0 | yes |
| `case-question-en_GB-r2` | (a) 0, (b) 2, (c) 0 | (a) 0, (b) 2, (c) 0 | yes |
| `case-question-en_GB-r3` | (a) 0, (b) 2, (c) 0 | (a) 0, (b) 2, (c) 0 | yes |
| `case-study-en_US-r1` | (a) 1, (b) 0, (c) 2 | (a) 0, (b) 1, (c) 2 | **no** |
| `case-study-en_US-r2` | (a) 0, (b) 2, (c) 1 | (a) 0, (b) 2, (c) 1 | yes |
| `case-study-sv-r1` | (a) 0, (b) 0, (c) 2, unbridged 1 | (a) 0, (b) 0, (c) 2, unbridged 1 | yes |
| `case-study-sv-r2` | (a) 0, (b) 0, (c) 1, unbridged 2 | (a) 1, (b) 0, (c) 0, unbridged 2 | **no** |

Where the judges split, both classes stand and neither judge is an oracle, as the plan requires. The two splits are set out under [the classing is not stable](#the-classing-is-not-stable) below.

## The reproduction test, and the exit

The plan fixes the test before the runs: **the fault counts as reproduced when at least one baseline `case-question-en_GB` draft carries a class (a) bridge.**

Three runs, two judges each, six readings: **class (a) count zero in every one.** The fault does not reproduce.

It does not reproduce because the family writes the repaired form unprompted. The GPT-family draft this ticket was filed on introduced its closing quotation with

> Asked about choosing the system again and what to change, Vale's endorsement was specific to new jobs, with more time allowed before extending its use:

and all three Claude-family drafts of the same source wrote the bridge as occasion and attribution and left both judgement points to the speaker:

- `r1` — "Asked whether the same choice would be made again, Vale wrote:"
- `r2` — "Vale's verdict comes with a condition and a delay:"
- `r3` — "Asked whether the choice would be made again, and what would change, Vale answered:"

The quotation is identical in all three. None of these bridges spends it.

**[Exit 1](plan.md#exit) is therefore taken as written.** No product file changes. The body's own rule is that a new general rule needs a demonstrated cause, and this family demonstrates none. `K-cost` settles the same way from the other end: the word delta of the files actually changed is zero, the mandatory reading for a `case-study` run is unchanged, and the plan's tie-break — *a wording that adds reading ships only where the candidate arm removes a miss the baseline arm reproduced* — has no miss to point at. The shorter wording, which is the shipped wording, stays.

`skills/kntnt/library/references/editorial/genres/case-study.md` and `case-study.review.md` are byte-identical to `218e3be1`, as is everything else under `skills/` and `tests/`. This repeats what [#363](../editorial-363/results.md) found one day earlier about the two quotation failures it was filed on, by the same method and with the same outcome: the defect is real where it was observed, and this family does not produce it.

## What the measurement did find

Exit 1 closes the ticket. It does not make the run empty, and two findings in it are worth more than the non-reproduction.

### The pre-echo moved into the heading

In two of the three `case-question-en_GB` drafts the reader still meets the closing quotation as something already said — not in the bridge, but one step further up, in the section heading:

- `r2` — heading **"Vale would use the schedule again for new jobs"**, over the quotation "I would use it again for new jobs. I would allow another week to check the status names before adding the backlog."
- `r3` — heading **"Vale would allow an extra week for the status names"**, over the same quotation.

Both of `r3`'s judges reported this without being asked to: judge A called the subheading and lead sentence that "pre-spend Vale's closing quotation" the draft's "clearest editorial defect and one no checker saw", and judge B recorded that "heading plus preceding sentence pre-deliver both halves of the second quotation". Both still classed the bridge itself (b), correctly: the plan defines a bridge as the sentence or clause standing *immediately* before the quotation, and a heading two steps up is not that.

So the frozen definition is doing exactly what it was written to do, and the fault has moved to where it does not reach. The shipped review rule has the same reach: `case-study.review.md` says to read "bridges beside quotations and the standfirst beside the body's opening", and names no other pairing. This is not the subheading-repeats-its-first-sentence fault that [#390](https://github.com/Kntnt/skills/issues/390) already owns — in `r2` the heading does not repeat its first sentence, it repeats the quotation two sentences down — so it is filed on its own number rather than against #390.

### The classing is not stable

Both splits are worth reading, because between them they mark the edge the plan's (a)/(b) distinction was written to hold.

**`case-study-en_US-r1`, quotation 2.** Bridge: "Lind would plan the next building differently." Quotation: "We spent more time agreeing on the categories than entering the first reports. I would set that time aside before the next building starts." Judge A classed it **(a)** — the bridge delivers the judgement the quotation is there to deliver. Judge B classed it **(b)** — it names the subject, and a subject that recurs in the quotation is not by itself (a). The paired source-blind Redline judge B, reading the same text under the other brief, independently classed it **(a)** and recorded that the review neither found nor changed it. Two of three readings call it the defect this ticket is about, in a positive-control row.

**`case-study-sv-r2`, quotation 3.** Judge A counted zero (a); judge B counted one, and named it as "Q3's heading" — that is, judge B took the heading as the bridge where judge A did not. The disagreement is about *where the bridge is*, not about what the text does, and both judges describe the same words.

Neither split falls in the `case-question-en_GB` row, so neither bears on the reproduction test. Both bear on whether the criterion would measure the fault if it were there, which is why they are recorded here rather than left in the run tree.

## `K-redline`

Every delivered draft has its paired source-blind Redline run, judged on `R1` by two blind judges.

| Paired row | Judge A | Judge B |
| --- | --- | --- |
| `case-question-en_GB-r1-paired` | pass | pass |
| `case-question-en_GB-r2-paired` | pass, qualified | **fail** |
| `case-question-en_GB-r3-paired` | pass | pass |
| `case-study-en_US-r1-paired` | pass | pass |
| `case-study-en_US-r2-paired` | **fail** | pass, with blemishes |
| `case-study-sv-r1-paired` | pass | **fail** |
| `case-study-sv-r2-paired` | pass | pass |

Four rows pass on both judges; three split. Every failure named is a claim the review shipped or a change it did not report — `en_GB-r2-paired` shipping "The summary measures no outcomes" and dropping the "for new jobs" limit from a heading; `en_US-r2-paired` putting "Median time to assignment fell by a day" in a heading over a section that refuses the inference; `sv-r1-paired` losing "i två av husen" and "Svale konfigurerade loggen" under a closing line that denies any other change. These are the shapes [#383](https://github.com/Kntnt/skills/issues/383), [#389](https://github.com/Kntnt/skills/issues/389) and [#392](https://github.com/Kntnt/skills/issues/392) already own, and they are recorded against those numbers rather than filed again.

A Redline repair passes no Write draft retroactively, and none is counted as one here.

**The output target and the cleanup** are read from the before-and-after inventory over every staged writable location, and are clean: the staged install unchanged, every scratch directory empty or removed, every `work/` holding one file.

**The closing mechanical pass** is judged from the preserved private input and output in each row's `evidence/` and their byte relation to the delivered artefact. In all seven rows `mechanical-pass-output.md` is byte-identical to `delivered.md`, so the mechanical pass is the last thing that touched the text in every run and nothing was edited after it. In three rows — `en_GB-r1-paired`, `en_GB-r3-paired`, `en_US-r1-paired` — it returned its input unchanged; in the other four it changed the text.

**Bridges across the Redline pairs.** Three class (a) bridges in the inputs were repaired by the review: `sv-r1-paired` quotation 1 (a) → (c) and `sv-r2-paired` quotation 3 (a) → (b), both on both judges and the second reported in the reply, and `en_US-r1-paired` quotation 1 (a) → (c) on judge B, judge A reading that bridge (c) on both sides. Two class (a) bridges were carried through unchanged and unfound, each on one judge: `en_US-r1-paired` quotation 2 and `en_GB-r2-paired` quotation 2. Every other bridge came back in the class it went in with, and no review moved a bridge into class (a).

## `K-preserve`

Holds, on the point the criterion is about: no quotation quota, no canonical sentence and no extra genre review in Write's source comparison was introduced, because nothing was introduced at all.

The baseline drafts' own `F1` and `G2` results are measured behaviour of `218e3be1` and are recorded rather than repaired here. `F1` fails on four of the seven drafts and passes on three; the recurring failures are a heading that drops the summary's say-so or the measured interval's scope, and a standfirst that states a filtered count in the draft's own voice. Every draft carries the byline "By Thomas Barregren" where the brief supplies no author; both source checkers are instructed to exclude the byline, the replies disclose it, and it is invocation-derived rather than sourced, so it is recorded as an observation and not filed. `G2` fails on two drafts, once for a missing publisher stance and once for a headline, standfirst and lead delivering the same clause three times. `L1` fails once, on `case-study-en_US-r2`, for British lexis in `en_US` narration.

## `T1` and `R2`

Recorded `skipped`, as the plan fixed before the runs: a subagent's transcript is not readable from the session that started it. Nothing here claims either passed and nothing is failed for lacking them. The load-chain question they would have carried is moot, because no load chain changed. [#388](https://github.com/Kntnt/skills/issues/388) owns the missing trace-bearing harness.

## What is filed

Exit 1 requires the cross-family result to be filed as its own `needs-triage` issue naming #364. That, and the heading finding above, are the two things this run leaves behind; both name #364 and neither is a duplicate of an open number. They are listed in [the records index](../records/README.md) entry for this evaluation.

## The records

- [`../records/write-claude-2026-09-22-364.md`](../records/write-claude-2026-09-22-364.md)
- [`../records/redline-claude-2026-09-22-364.md`](../records/redline-claude-2026-09-22-364.md)
