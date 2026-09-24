# Results for #396: a subheading standing over a quotation does not pre-say it

Measured on 2026-09-24, Central European Summer Time — the fourteen runs between 22:33 and 23:57 UTC on 2026-09-23 — under the plan frozen in [`plan.md`](plan.md) at `5d54ac71`, before the first run. The record is [`../records/write-claude-2026-09-24-396.md`](../records/write-claude-2026-09-24-396.md).

**Outcome: reproduced, and the candidate passes every criterion in its first arm. It ships, and no revise round was run.**

| Criterion | Pre-change arm (`385976f7`) | Post-change arm (`5bafd03e`) | Verdict |
| --- | --- | --- | --- |
| *Reproduced*: a `case-question-en_GB` draft carries a subheading counted as a pre-echo | 3 of 3 drafts, 5 subheadings | — | reproduced |
| *Pass*: no `case-question-en_GB` draft carries one, and the row's count is lower | 5 | 0, in 0 of 3 drafts | pass |
| *Control*: `case-study-en_US` count not higher | 5 | 0 | pass |
| *Control*: `case-study-sv` count not higher | 4 | 0 | pass |
| *Control*: bridges classed (a), all drafts, both judges, not higher | 0 | 0 | pass |

No judge split on whether any subheading is a pre-echo, in either arm, so the split rule decided nothing.

## How it was run

- **Runs.** Fourteen `Write` runs, seven per arm, each made with [`../editorial-388/harness/staged_run.py`](../editorial-388/harness/staged_run.py) from the repository root with `--model=claude-opus-5-5 --effort=high`, `--corpus-revision=385976f7` and `--revision` set to `385976f7` for `pre` and `5bafd03e` for `post`. The Harness was Claude Code 2.1.281. Every packet's `trace-index.json` records three agents — the writer and its two source-comparison subagents — and all three on `claude-opus-5-5`; every trace is `complete`, every private root was removed (`cleanup.json`), and no run stopped, timed out or was interrupted. No run was void, so `voided/` does not exist.
- **Lanes.** The three `case-question-en_GB` runs of an arm went one after another in one lane and the four control runs in another, so no two runs on one input were ever made at the same time.
- **The rule reached the writer.** Every post-change run's own transcript (`transcripts/parent.jsonl`) holds the new `headlines.md` text — the phrase "outside the quotation bridge" — as read by the writer; no pre-change transcript does.
- **Judges.** Twenty-eight judgements, two per draft, each by a fresh `kntnt-opus-high` subagent (`claude-opus-5-5` at high deliberation) with no history, under [`write-judge-brief.md`](write-judge-brief.md). Each judge had a directory of its own under the build's scratch root, named by a random token, holding only `work/source.md`, `response.md` and `delivered.md`; [`judges.json`](judges.json) maps each token to the run and the judge letter. The scratch root's own path carries this build's number, which is not the arm; the judges were told nothing of what it is. Each judgement is kept in the packet it judged as `judgement-a.md` or `judgement-b.md`.
- **Counting.** Judges classed a subheading once per quotation under it. The counts below are per distinct subheading, each counted as a pre-echo where either judge classed it pre-echo against any quotation under it.

The packets are under [`runs/pre/`](runs/pre/) and [`runs/post/`](runs/post/), copied there from the scratch directory after they were judged.

## The candidate

Committed as `5bafd03e` once all seven pre-change runs had finished and the `case-question-en_GB` row, the one the reproduction test reads, had been judged and had reproduced the defect. The last pre-change control, `case-study-sv-r2`, was judged while the post-change arm started; nothing in the candidate drew on it.

**A departure from the plan.** `plan.md` says the exact wording "is written after the pre-change arm". It was drafted, with its tests, while the pre-change arm was running, from what the ticket's addendum specifies rather than from the baseline drafts, and it was committed, and so staged for any run, only at the point above. No pre-change run could read it, because every run stages its install from a commit with `git archive`, and the pre-change arm's commit is `385976f7`.

It changes six shipped files and adds three tests:

- `skills/kntnt/library/references/editorial/headlines.md` gains a section, *A subheading over a quotation*. A quotation carries what only its speaker can say — a judgement, a figure, a concession — and the subheading over it leaves that to the quotation: it states the section's angle from what the rest of the section says, or, where the quotation is the section's point, names the subject, the occasion or the speaker, and not the point. The test is the anatomy's lead test turned on the subheading: *a reader who has just read the subheading meets the quotation as new material, never as the subheading said again*. One invented example, from a domain no fixture uses, shows each side. The section defines the quotation bridge in #364's frozen words and says that a subheading standing over a quotation is outside the quotation bridge and governed by this section. The line-31 instruction now ends "and leave a quotation standing under it the judgement, figure or concession it is there to carry".
- `headlines.review.md` reads each subheading against any quotation under it, lists the pre-spending subheading in its *Avoid* list with its repair, and says under *Leave alone* that a subheading naming the subject, the occasion or the speaker over a quotation is not "a subject named with nothing said about it".
- Write `SKILL.md` step 7 tells the writer to read each subheading against any quotation under it, which `heading_pairs` does not show, and bounds its heading repair by the quotation; Write `help.md` line 21 and Redline `references/correction.md` line 35 bound the same repair the same way; the editorial `README.md` paragraph on `headlines.md` names the new rule and where the quotation bridge ends.
- Unchanged, as the addendum requires: `CONTEXT.md`, `case-study.md` (its line 17 byte for byte), `case-study.review.md`, and `article_anatomy.py`. No new or changed shipped sentence says a bare "bridge".
- Tests in `tests/test_kntnt.py`: that `headlines.md` places the subheading outside the quotation bridge and the review half's *Avoid* list names the quotation; that every sentence telling a heading to be worded from its whole section or text also bounds it by the quotation; and that no editorial prose says a bare "bridge" beyond the two sentences written before the term was settled. The first two were run and seen failing before the prose was written; the third is a guard that passed from the start.

**Reading cost.** A `case-study` `Write` run reads 259 words more: `headlines.md` grows from 620 to 844 words and Write `SKILL.md` from 2 655 to 2 690. Outside Write's reading, `headlines.review.md` grows by 109 words, `help.md` by 17, `correction.md` by 15 and the editorial `README.md` by 20.

## The subheadings, draft by draft

**Pre-change arm.** Every subheading counted below was classed pre-echo by both judges.

| Draft | Subheading over a quotation | Class A / B | Counted |
| --- | --- | --- | --- |
| `case-question-en_GB-r1` | The workshop set the statuses, Benchline configured them | prepares / prepares | — |
| | Vale would spend longer checking the status names | pre-echo / pre-echo | pre-echo |
| `case-question-en_GB-r2` | 'Ready for work' needed an agreed meaning | pre-echo / pre-echo | pre-echo |
| | Fenwick kept the schedule for new jobs and held back the backlog | pre-echo / pre-echo | pre-echo |
| `case-question-en_GB-r3` | ‘Ready for work’ needed an agreed meaning | pre-echo / pre-echo | pre-echo |
| | Status definitions come before the backlog | pre-echo / pre-echo | pre-echo |
| `case-study-en_US-r1` | Elm Quay wanted its shifts to share one picture | pre-echo / pre-echo | pre-echo |
| | The maintenance team designed its own categories | pre-echo / pre-echo | pre-echo |
| | Lind would repeat the trial, with an extra week to prepare | pre-echo / pre-echo | pre-echo |
| `case-study-en_US-r2` | Elm Quay tested repair tracking before picking Svale | neutral / neutral | — |
| | Elm Quay designed the categories, and Svale set up the system | pre-echo / pre-echo | pre-echo |
| | The supervisor would repeat the trial with more preparation | pre-echo / pre-echo | pre-echo |
| `case-study-sv-r1` | Teamet utformade kategorierna, Svale hjälpte till att lägga in dem | pre-echo / pre-echo | pre-echo |
| | Arbetsledaren skulle göra om provet med mer förberedelse | pre-echo / pre-echo | pre-echo |
| `case-study-sv-r2` | Olika skift skulle ha samma information | pre-echo / pre-echo | pre-echo |
| | Att enas om kategorierna tog mer tid än första inmatningen | pre-echo / pre-echo | pre-echo |
| | Frågan om fler hus är ännu öppen | neutral / neutral | — |

Fourteen of seventeen subheadings over a quotation are counted: 5 in `case-question-en_GB`, 5 in `case-study-en_US`, 4 in `case-study-sv`. The measured fault is the one the body describes — `case-question-en_GB-r1`'s "Vale would spend longer checking the status names" is `editorial-364`'s `r3` heading again in other words — and it is not confined to that row: every draft of both control rows carries it too. Where one subheading stood over two quotations, a judge sometimes classed it prepares against one and pre-echo against the other (`case-question-en_GB-r1` A, the categories headings in both `case-study-en_US` drafts, the two lower headings in the `case-study-sv` drafts); the subheading counts once, as a pre-echo.

**Post-change arm.** No subheading was classed pre-echo by either judge.

| Draft | Subheading over a quotation | Class A / B |
| --- | --- | --- |
| `case-question-en_GB-r1` | Fenwick defined its statuses before Benchline configured them | prepares / prepares |
| | The manager looks back on the trial | prepares / prepares |
| `case-question-en_GB-r2` | Fenwick defined its own job statuses | prepares / prepares |
| | Vale looks ahead to the backlog | prepares / prepares |
| `case-question-en_GB-r3` | The workshop set its own status rules | prepares / prepares |
| | Vale on making the same choice again | prepares / prepares |
| `case-study-en_US-r1` | Why the maintenance team wanted a shared log | prepares / prepares |
| | Maya Lind weighs the trial | prepares / prepares |
| `case-study-en_US-r2` | Why Elm Quay wanted one log | prepares / prepares |
| | What the setup demanded | prepares / prepares |
| | Maya Lind looks back on the trial | prepares / prepares |
| `case-study-sv-r1` | Telefonen blev kvar och sex anställda utbildades | neutral / neutral |
| | Arbetsledaren ser tillbaka på provet | prepares / prepares |
| `case-study-sv-r2` | Varför teamet ville ha en gemensam logg | prepares / prepares |
| | Teamet och Svale delade på införandet | neutral / prepares |
| | Maya Lind ser tillbaka på testet | prepares / prepares |

Several post-change subheadings drew a pre-echo reading that the judge weighed and rejected, and they are recorded here because they are where the rule's edge is. Both judges of the status headings in all three `case-question-en_GB` drafts set out a pre-echo reading ("The workshop set its own status rules" over "We had to agree what ready for work meant…") and chose prepares because the heading names who set the statuses and not why agreement was needed; the same reading was weighed and rejected for the same shape of heading in the pre-change `case-question-en_GB-r1`. Over Lind's closing appraisal, "Maya Lind weighs the trial" drew "a mild pre-echo" from judge A and "leans toward pre-echo" from judge B, "What the setup demanded" drew "a faint pre-echo" from judge B, and "Arbetsledaren ser tillbaka på provet" and "Why Elm Quay wanted one log" each drew a pre-echo reading one judge rejected. Every one of them was classed prepares in the end, by both judges.

Four of the seven post-change drafts put a heading in the shape the new section's example gives — the speaker "looks back on" the trial — over the closing quotation. That is the example being followed, and it is a subheading that names the speaker and the occasion; whether it is also a formula worth varying is a question for review, not a finding of this measurement.

## Bridges

No judge classed any bridge (a), in either arm: the total is 0 in both, so the control holds. Bridges, per judge, (a)/(b)/(c):

| Draft | Pre A | Pre B | Post A | Post B |
| --- | --- | --- | --- | --- |
| `case-question-en_GB-r1` | 0/3/0 | 0/2/0 | 0/2/0 | 0/2/0 |
| `case-question-en_GB-r2` | 0/2/0 | 0/2/0 | 0/2/0 | 0/2/0 |
| `case-question-en_GB-r3` | 0/2/0 | 0/2/0 | 0/2/0 | 0/2/0 |
| `case-study-en_US-r1` | 0/1/3 | 0/1/3 | 0/3/0 | 0/3/0 |
| `case-study-en_US-r2` | 0/2/2 | 0/2/2 | 0/3/0 | 0/3/0 |
| `case-study-sv-r1` | 0/1/1, 1 without a bridge | 0/1/1, 1 without | 0/1/2 | 0/1/2 |
| `case-study-sv-r2` | 0/1/1, 2 without | 0/1/1, 2 without | 0/2/1 | 0/2/1 |

`case-question-en_GB-r1`'s pre-change judges divided Vale's second answer differently, A as two quotations and B as one, which is the whole of their difference in count.

A live (a) reading was weighed and rejected in both arms, as `editorial-364` found at the same edge. Pre-change: both judges of `case-question-en_GB-r2` over "…Priya Vale named one status." ("Second reading, (a)"; "could be read as a partial (a)"), both of `case-study-en_US-r2` over two bridges, and both of `case-study-sv-r2` over one. Post-change: judge A of `case-question-en_GB-r1`, both of `case-question-en_GB-r3` where they read the prior sentence as part of the bridge ("(c), with (a) overtones"; "leans towards (a)"), and both of `case-study-en_US-r1` over "Her overall assessment is qualified:" ("Reading two, leaning (a)"; "leans toward (a)"). None was classed (a). The quotation bridge's definition is unchanged, so this edge is where it was.

## What else the judges found

Recorded as measured; none of it is this ticket's criterion.

| Draft | F1 A / B | G2 A / B | L1 A / B | Delivery A / B |
| --- | --- | --- | --- | --- |
| pre `case-question-en_GB-r1` | fail / fail | pass / pass | pass / pass | should not have happened / should not have happened |
| pre `case-question-en_GB-r2` | fail / fail | fail / fail | fail / pass | valid / valid |
| pre `case-question-en_GB-r3` | fail / fail | pass / pass | pass / pass | valid / valid |
| pre `case-study-en_US-r1` | fail / fail | pass / fail | pass / pass | valid / valid |
| pre `case-study-en_US-r2` | fail / fail | pass / pass | pass / pass | valid / valid |
| pre `case-study-sv-r1` | fail / fail | fail / fail | pass / pass | valid / valid |
| pre `case-study-sv-r2` | fail / pass | pass / pass | pass / pass | valid / valid |
| post `case-question-en_GB-r1` | fail / fail | pass / pass | pass / pass | valid / valid |
| post `case-question-en_GB-r2` | fail / fail | pass / pass | pass / pass | valid / valid |
| post `case-question-en_GB-r3` | fail / pass | fail / pass | pass / pass | valid / valid |
| post `case-study-en_US-r1` | fail / fail | pass / pass | pass / pass | should not have happened / should not have happened |
| post `case-study-en_US-r2` | fail / fail | pass / pass | pass / pass | valid / valid |
| post `case-study-sv-r1` | fail / fail | pass / pass | pass / pass | valid / valid |
| post `case-study-sv-r2` | fail / fail | pass / fail | pass / pass | valid / valid |

Most F1 failures in both arms rest wholly or partly on the byline `By Thomas Barregren` / `Av Thomas Barregren`, which every draft carries against a brief that says no author name is supplied, and which the #364 record already recorded as owned by no ticket. The rest are small source slips a comparison mostly caught and the run disclosed: a headline stating a quoted view as fact, "advice" for a first-person plan, "de egna husen" for flats Elm Quay manages. The two deliveries both judges say should not have happened — pre `case-question-en_GB-r1`, whose ending advises other workshops against the material's "not a recommendation for every workshop", and post `case-study-en_US-r1`, which delivered two confirmed one-line F1 findings unrepaired — are a true finding reaching the final comparison and being delivered disclosed, the shape `editorial-364` assigned to #376; neither is a subheading and neither is filed here.

## Wall time and cost

As `result.json` records them, under whatever load the API carried:

| Row | Pre | Post |
| --- | --- | --- |
| `case-question-en_GB-r1` / `-r2` / `-r3` | 10m44s / 9m22s / 8m08s | 7m02s / 7m22s / 6m52s |
| `case-study-en_US-r1` / `-r2` | 10m17s / 8m36s | 7m41s / 9m22s |
| `case-study-sv-r1` / `-r2` | 10m03s / 12m55s | 12m12s / 12m24s |
| Harness cost, whole arm | $16.56 | $15.22 |

## What this measurement does not reach

- **The rule's text is general, and three of the four genres it governs were not measured.** Write loads `headlines.md` for `article`, `case-study`, `column` and `opinion`; every run here is `case-study`.
- **No Redline run was made**, so the Redline-side changes — `headlines.review.md`'s *Avoid* and *Leave alone* entries and `correction.md`'s bounded repair — are unmeasured.
- **The comparison is the in-session pre-change arm, not `editorial-364`.** That evaluation ran on `claude-opus-5` against `218e3be1`, before `09fb8991` and the other changes to what Write loads; its drafts were not re-run or re-judged and are not the comparison. Its bridge table is not the control either.
- **Two arms of seven runs.** A count of 14 against 0 on one input family is a large difference on a small sample; it says the candidate removed the measured fault here, not that no subheading will ever pre-spend a quotation.

## A decision record

None is written, and `0221`, the number reserved for this ticket, stays unused. `docs/rules/docs.md` asks for all three of its criteria at once. The change is **not hard to reverse**: it is prose in six shipped files and three tests, reverted by one commit. It is **partly surprising** without its context — why a subheading is kept outside the quotation bridge, and why the shipped text says "quotation bridge" — but both reasons are stated where a reader meets them: the first in `headlines.md` itself and in the ticket's addendum, the second in `CONTEXT.md`'s entry for **Bridge** and the docstring of the test that holds it. It **was a real trade-off**, widening the bridge against a separate subheading rule, decided in Thomas's absence and open to his review on the ticket. One criterion of three fails, so the decision is a rule, and it lives in `headlines.md`.

## Misses filed

None. Every criterion was met in the first candidate arm, so rule 4 files nothing, and the `heading_pairs` extension to pair a subheading with the quotation under it is not needed by this measurement.
