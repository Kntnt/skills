# Results for #438: what a quotation bridge may carry is stated where the writer reads

Measured on 2026-09-30 — the fourteen runs between 08:01 and 09:23 UTC (10:01 and 11:23 Central European Summer Time) — under the plan frozen in [`plan.md`](plan.md) at `6cd383f1`, before the first run. The record is [`../records/write-claude-2026-09-30-438.md`](../records/write-claude-2026-09-30-438.md).

**Outcome 1 of the plan's three: `post` meets the ship rule, and the candidate ships. No revise round was run.**

| Ship rule | Pre-change arm (`2afeb95e`) | Post-change arm (`2eca70b3`) | Verdict |
| --- | --- | --- | --- |
| Quotation bridges classed (a), every draft, both judges | 0 | 0 | not higher: met |
| Subheadings over a quotation counted as a pre-echo, all three rows | 0 | 0 | not higher: met |

Both totals are 0 in the pre-change arm, so the ship rule required 0 in the candidate arm, and it is 0. No judge split on either question, so the split rule decided nothing. This is a control, not a reproduction: a pre-change arm with no quotation bridge classed (a) is the expected reading, no result here is recorded as not reproduced, and no decision record is written.

## How it was run

- **Runs.** Fourteen `Write` runs, seven per arm, each made with [`../editorial-388/harness/staged_run.py`](../editorial-388/harness/staged_run.py) from the repository root with `--model=claude-opus-5-5 --effort=high`, `--corpus-revision=2afeb95e` and `--revision` set to `2afeb95e` for `pre` and `2eca70b3` for `post`, and the invocation `/write --genre=casestudy --language=<lang> --output=response source.md` with `--genre=casestudy` the installed genre name. The Harness was Claude Code 2.1.285. Every packet's `trace-index.json` records three agents, the writer and its two source-comparison subagents, all on `claude-opus-5-5`; every trace is `complete`, every run returned 0, every private root was removed (`cleanup.json`), and no run stopped, timed out or was interrupted. No run was void, so `voided/` does not exist.
- **Lanes.** The three `case-question-en_GB` runs of an arm went one after another in one lane and the four control runs in another, so no two runs on one input were ever made at the same time. The `post` arm started after the last `pre` run had finished.
- **The rule reached the writer.** Every post-change run's own transcripts hold the new `casestudy.md` text, the phrase "who has just read the quotation bridge", as the writer read it; no pre-change transcript does, and every pre-change transcript holds the old sentence "prepare a quotation rather than pre-say it", which no post-change transcript does.
- **Judges.** Twenty-eight judgements, two per draft, each by a fresh `kntnt-opus-high` subagent (`claude-opus-5-5` at high deliberation) under [`../editorial-396/write-judge-brief.md`](../editorial-396/write-judge-brief.md), used as it stands. Each judge had a directory of its own under the build's scratch root, named by a random token, holding only `work/source.md`, `response.md` and `delivered.md`; [`judges.json`](judges.json) maps each token to the run and the judge letter. The scratch root's own path carries this build's number, which is not the arm; the judges were told nothing of what it is. Each judgement is kept in the packet it judged as `judgement-a.md` or `judgement-b.md`. Two judges (`f1c4d3bb` and `e975a116`) say in their replies that they wrote a comparison file under `/tmp` once and deleted it at once; nothing they read or wrote changes their judgement.
- **Counting.** Both counts are per-arm totals, by the plan's rule: every draft's point-4 count of bridges classed (a), from both judges; and every subheading counted once as a pre-echo where either judge classes it pre-echo under point 4b. Each judgement's per-quotation lines were also searched for a bridge classed (a) or a subheading classed pre-echo that its summary counts leave out, and there is none in any of the twenty-eight.

The packets are under [`runs/pre/`](runs/pre/) and [`runs/post/`](runs/post/), copied there from the scratch directory after they were judged.

## The candidate

Committed as `2eca70b3` while the pre-change arm was running and before any pre-change draft had been read or judged. It was written from what the ticket's readiness addendum specifies and not from any draft of this evaluation, and no pre-change run could read it, because every run stages its install from a commit with `git archive` and the pre-change arm's commit is `2afeb95e`. The `post` arm was staged from it once the pre-change arm had finished.

In `skills/kntnt/library/references/editorial/genres/casestudy.md` the sentence

> A bridge should prepare a quotation rather than pre-say it.

is replaced where it stands by

> A quotation bridge should carry the speaker, the occasion or the question the quotation answers, where the material gives one, and any fact the quotation does not itself give; it should not carry the quotation's judgement, figure or concession. Test it before writing it: a reader who has just read the quotation bridge meets the quotation as new material, never as the quotation bridge said again.

The paragraph's other two sentences are byte for byte as they were. `genres/casestudy.review.md` and `headlines.md` are unchanged. The wording stays at *should*, says *quotation bridge* every time, and leaves the definition of the term to `headlines.md`.

Tests in `tests/test_kntnt.py`:

- `BARE_BRIDGE_KEPT` no longer holds the old sentence and still holds the review half's; the comment above `HEADLINES` and the docstring of `test_editorial_prose_says_quotation_bridge_never_a_bare_bridge` say that one sentence keeps its word.
- A new test, `test_what_a_quotation_bridge_may_carry_is_ruled_where_the_writer_reads`, asserts that the phrase "who has just read the quotation bridge" is in `genres/casestudy.md` and not in `genres/casestudy.review.md`, and names #438. It and the changed bare-bridge test were run and seen failing before the wording was written, then passing after it.

The catalog was regenerated (`manager_digest` only). **Reading cost:** a `casestudy` `Write` run reads 56 words more, `casestudy.md` growing from 282 to 338 words.

## The quotation bridges

No judge classed any quotation bridge (a), in either arm: the total is 0 in both. Bridges per judge, (a)/(b)/(c), and how many quotations stand with no bridge:

| Draft | Pre A | Pre B | Post A | Post B |
| --- | --- | --- | --- | --- |
| `case-question-en_GB-r1` | 0/2/0 | 0/2/0 | 0/3/0 | 0/3/0 |
| `case-question-en_GB-r2` | 0/2/0 | 0/2/0 | 0/3/0 | 0/3/0 |
| `case-question-en_GB-r3` | 0/2/0 | 0/2/0 | 0/2/0 | 0/2/0 |
| `case-study-en_US-r1` | 0/2/1 | 0/1/2 | 0/1/1, 1 without | 0/1/1, 1 without |
| `case-study-en_US-r2` | 0/3/0 | 0/3/0 | 0/2/1 | 0/2/1 |
| `case-study-sv-r1` | 0/1/0, 2 without | 0/0/0, 3 without | 0/2/1 | 0/2/1 |
| `case-study-sv-r2` | 0/2/0, 1 without | 0/2/0, 1 without | 0/1/0, 2 without | 0/1/0, 2 without |

Where a count differs between the two judges of a draft, the difference is what each took to be the bridge: `case-study-en_US-r1` (pre), one judge classed "comes with a reservation" (c) and the other (b), and `case-study-sv-r1` (pre), one judge counted a bridge over the first quotation and the other counted none.

**Live (a) readings.** Weighed and rejected, they were recorded by six of the fourteen pre-change judgements, over four drafts: both judges of `case-question-en_GB-r2`, one over a bridge that names both halves of the interview question and one over the paragraph before it; judge B of `case-question-en_GB-r1`, over that same kind of preceding paragraph; both judges of `case-study-en_US-r1` over "comes with a reservation"; and judge A of `case-study-sv-r2`, over a bridge saying an appraisal follows. None was classed (a). No post-change judge recorded one. That is 6 of 14 against 0 of 14, and it is a reading of two small arms by the same kind of judge, offered as measured and not as a criterion. The plan makes the class counts the control, and `editorial-364` and `editorial-396` found the same edge in the same way.

## The subheadings over a quotation

No subheading was classed pre-echo by either judge, in either arm: the total is 0 in both. Per draft, the subheadings over quotations, prepares/neutral per judge A / B (pre-echo was 0 throughout):

| Draft | Pre A | Pre B | Post A | Post B |
| --- | --- | --- | --- | --- |
| `case-question-en_GB-r1` | 2/0 | 2/0 | 3/0 | 3/0 |
| `case-question-en_GB-r2` | 2/0 | 2/0 | 3/0 | 3/0 |
| `case-question-en_GB-r3` | 2/0 | 2/0 | 2/0 | 2/0 |
| `case-study-en_US-r1` | 2/1 | 2/1 | 2/1 | 2/1 |
| `case-study-en_US-r2` | 3/0 | 3/0 | 2/1 | 2/1 |
| `case-study-sv-r1` | 3/0 | 2/1 | 1/2 | 1/2 |
| `case-study-sv-r2` | 3/0 | 3/0 | 2/1 (A) | 3/0 |

Both arms carry subheadings of the shape #396 shipped, and judges in both arms weighed a pre-echo reading at the same edge and rejected it: over the status-definition quotation in the `case-question-en_GB` drafts ("set the rules", "defined the statuses", "drew up its statuses" against "we had to agree what ready for work meant"), and over "weighs the trial" in `case-study-en_US-r2` (both arms). None was classed pre-echo in the end.

## What else the judges found

Recorded as measured; none of it is this ticket's criterion. F1, G2 and L1 per draft, judge A / judge B:

| Draft | Pre F1 | Pre G2 | Pre L1 | Post F1 | Post G2 | Post L1 |
| --- | --- | --- | --- | --- | --- | --- |
| `case-question-en_GB-r1` | pass / fail | pass / pass | pass / pass | fail / fail | pass / pass | pass / pass |
| `case-question-en_GB-r2` | pass / fail | pass / pass | pass / pass | pass / fail | pass / pass | pass / pass |
| `case-question-en_GB-r3` | fail / fail | pass / pass | pass / pass | fail / fail | pass / pass | pass / pass |
| `case-study-en_US-r1` | fail / fail | pass / pass | pass / pass | pass / fail | pass / pass | pass / pass |
| `case-study-en_US-r2` | fail / fail | fail / fail | pass / pass | fail / fail | pass / pass | pass / pass |
| `case-study-sv-r1` | fail / pass | pass / pass | pass / pass | fail / fail | pass / pass | fail / pass |
| `case-study-sv-r2` | pass / pass | pass / pass | pass / pass | fail / fail | pass / pass | pass / pass |

- **The byline.** Every draft in both arms carries a byline, `By Thomas`, `Av Thomas` or `Av Thomas Barregren` against a brief that supplies no author. Most judges name it, several as the whole of the F1 failure, and the writer discloses it in its reply. It is recorded and not filed, as the #364 and #396 records did.
- **Delivery.** Twenty-six judgements call the delivery valid. Both pre-change judges of `case-question-en_GB-r3` call it a delivery that should not have happened, because the writer knew of two defects and delivered them unrepaired; that is the shape `editorial-364` assigned to [#376](https://github.com/Kntnt/skills/issues/376), and no post-change judge says it.
- **G2.** Both pre-change judges of `case-study-en_US-r2` fail it for a draft that never says the supplier published it. In the post-change arm no judge fails G2, though several name the same weakness as a reservation.
- **`T1` and `R2`** are not judged. Every packet keeps its complete trace, so they can be judged from it later.

None of it is caused by the wording under test, and each F1 or G2 failure is a fault other tickets own (the byline, an unrepaired disclosed finding, an absent publisher stance), so under the protocol's *Whose miss* none is counted here.

## What ships

The candidate ships, as the plan's outcome 1 says: the `casestudy.md` change, the test changes and the regenerated catalog. `genres/casestudy.review.md`, `headlines.md` and `docs/research/editorial-review-half-sweep.md` are unchanged, the last being research and read as of its date. No decision record is written, and ADR-0214 stands as the account of the earlier Claude-family measurement of the sentence this replaces; the change is one sentence and easily reversed.

The GPT-family retest stays [#395](https://github.com/Kntnt/skills/issues/395), Thomas's hand step, and it now measures this wording.

## Files

[`plan.md`](plan.md) as frozen; this file; [`judges.json`](judges.json); the judged packets under [`runs/pre/`](runs/pre/) and [`runs/post/`](runs/post/); and the record [`../records/write-claude-2026-09-30-438.md`](../records/write-claude-2026-09-30-438.md).
