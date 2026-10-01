# Results for #480

Measured on 2026-10-01 under [the frozen plan](plan.md), committed as `e7dd6701` before the first run. The three contrast inputs and their validations were committed before it, as `e5fcdf4f`. Every run, correction subagent, reply checker, nested Proofread pass, judge and validator ran on `claude-opus-5-5` at high deliberation. The 34 runs' `trace-index.json` files record that model and deliberation for all 73 agents they hold. The pre-change arm was staged from `fb169087`, the first candidate from `f39a3721` and the revised candidate from `e4fe5890`. Harness: Claude Code 2.1.286.

**The headline result.** The defect reproduces, and the revised candidate meets the Target and ships.

- **Reproduced.** In the pre-change arm, one `article-clean` run of six, `pre-article-clean-resp-2`, recorded a finding against the working headline *Mätförsöket i Björkskolan visar när, inte varför*. It rewrote the headline and reported the rewrite as a repair.
- **The first candidate missed the Target.** None of its six runs recorded a finding against the headline. But `post-article-clean-file-2` rewrote a sentence of the lead over a finding about sensor placement, and both judges fail it on `R1`. The plan's Target requires every candidate file-target run of `article-clean` to meet `R1`, so the Target is missed, and the protocol's one revise round was taken.
- **The revised candidate met the Target.** None of its six `article-clean` runs recorded a finding against the headline or offered the author another one. All three of its `output.md` files are byte-identical to the input, and both judges pass `R1` on every run. No Control regressed.

**The interruption.** The account's usage limit (HTTP 429, *You've hit your session limit*) cut off two judges of the first candidate's arm on `article-overclaim`: judge `b` of `post-article-overclaim-1` and judge `a` of `post-article-overclaim-2`. Judge `b` of `post-article-overclaim-2` had not been sent yet. No run was cut off. All 28 runs of the first two arms had finished with return code 0, terminal reason `completed` and a complete trace before the limit was reached, and the revise round ran after it reset. Under the plan's *Void runs*, the two cut-off judgements are void. Neither had written a judgement. Their directories are named in [`runs/judges.tsv`](runs/judges.tsv) with the letter marked `-void`, and nothing of them is counted or committed. Each was sent again to a fresh judge in a fresh directory with the same message, once the limit had reset. The judge not yet sent was sent then too. Every judgement below is from a judge that finished.

## The contrast inputs and their validation

Each contrast input is `article-clean` with its headline line replaced, as the plan sets out. Two fresh validators read each one with the [validation brief](validation-brief.md) and the text alone, and every validator gave its input the class it was written to have ([`validation/`](validation/)):

| Input | Headline | Validator a | Validator b |
| --- | --- | --- | --- |
| `article-allusion` | *Björkskolans temperaturgivare ger halva svaret* | working | working |
| `article-unnamed` | *Siffrorna visar när, inte varför* | unclear | unclear |
| `article-overclaim` | *Mätförsöket visar att Björkskolans klassrum är för kalla* | overclaiming | overclaiming |

## The measurement the ticket was filed from

#468's `post-article-clean-file-3` is restated here from its committed packet, [`../editorial-468/runs/post-article-clean-file-3/`](../editorial-468/runs/post-article-clean-file-3/), with its four stages apart. Its first attempt, cut off by a spend limit, is void and is not counted.

1. **The finding.** *En rubrik ska gå att förstå på egen hand. Här saknar "när" och "varför" något att syfta på.* … *Läsaren får däremot inte veta vad som mättes eller vad som hände.*
2. **The correction round's proposal.** The headline became *Mätförsöket i Björkskolan visar när det blev kallt, inte varför*.
3. **The re-review.** It rejected the round, because the new headline was 63 characters against the anatomy's norm of 60. The text was restored.
4. **The final report.** The finding is carried forward as unresolved, *felet står kvar och får avgöras av dig*, with a proposed headline for the author.

The delivered `captured-output.md` is byte-identical to the input, so both judges pass `R1`. Both fail the expectation's *Conforms to the anatomy* on the finding, so the run misses `C1`. Those are two readings and are kept apart: the `R1` pass is no evidence against the false finding.

## The Target: no finding against `article-clean`'s headline

This session read every `article-clean` reply for a finding against the headline or an offer of another headline, and compared every delivered headline with the input's. As the plan says, **this call is not blind**. The judges' answers on *Conforms to the anatomy* are recorded beside each call.

| Run | Delivered | Finding against the headline | `R1` (a / b) | *Conforms to the anatomy* (a / b) |
| --- | --- | --- | --- | --- |
| `pre-article-clean-resp-1` | no-change status | none | skipped: no text delivered | met / met |
| `pre-article-clean-file-1` | `output.md`, identical | none | pass / pass | met / met |
| `pre-article-clean-resp-2` | text in the reply, headline rewritten | **yes**: *Rubriken (åtgärdad).* | fail / fail | not met / not met |
| `pre-article-clean-file-2` | `output.md`, identical | none | pass / pass | partly met / partly met, on the placement finding |
| `pre-article-clean-resp-3` | no-change status | none | skipped: no text delivered | met / met |
| `pre-article-clean-file-3` | `output.md`, identical | none | pass / pass | met / met |
| `post-article-clean-resp-1` | no-change status | none | skipped: no text delivered | met / met |
| `post-article-clean-file-1` | `output.md`, identical | none | pass / pass | met / met |
| `post-article-clean-resp-2` | no-change status | none | skipped: no text delivered | met / met |
| `post-article-clean-file-2` | `output.md`, lead's second sentence rewritten | none | **fail / fail** | met / met; `C1` fails on the calm explanation's changed inference |
| `post-article-clean-resp-3` | text in the reply, one body clause narrowed | none | pass / pass | met / met |
| `post-article-clean-file-3` | `output.md`, identical | none | pass / pass | met / met |
| `rev-article-clean-resp-1` | no-change status | none | skipped: no text delivered | met / met |
| `rev-article-clean-file-1` | `output.md`, identical | none | pass / pass | met / met |
| `rev-article-clean-resp-2` | no-change status | none | skipped: no text delivered | met / met |
| `rev-article-clean-file-2` | `output.md`, identical | none | pass / pass | met / met |
| `rev-article-clean-resp-3` | text in the reply, identical | none | pass / pass | partly met / partly met, on the placement finding |
| `rev-article-clean-file-3` | `output.md`, identical | none | pass / pass | met / met |

`pre-article-clean-resp-2`, the one run that shows the defect, is read here with its four stages apart, from its transcript and reply:

1. **The finding.** The first review recorded *Rubriken, ”Mätförsöket i Björkskolan visar när, inte varför”*. It cited *Vague or mysterious wording that requires reading the text to understand the headline* and *leaves a reader who sees only the heading unable to tell what the text is about*, and added: *Rubriken säger varken vad mätförsöket mätte eller vad ”när” och ”varför” syftar på: ”visar när, inte varför” är en ellips som först standfirsten fyller i.* The loss it named: a reader of the headline alone *kan inte avgöra att texten handlar om temperaturen i skolans klassrum, eller att mätningarna visar när den låg under en gräns men inte förklarar varför.*
2. **The correction round's proposal.** *Mätförsöket i Björkskolan visar när det var kallt, inte varför*, 62 characters and 10 words.
3. **The re-review.** It established no defect created by the round and accepted the new headline.
4. **The final report.** *Rubriken (åtgärdad)*, with a changed claim. The report itself says that the new headline can be read as a broader claim than the text carries and that it passes two *should* norms the original met.

- **Reproduced:** one pre-change run of six shows the defect.
- **First candidate, Target missed:** no run shows the defect, but `post-article-clean-file-2` misses `R1`.
- **Revised candidate, Target met:** no run shows the defect, and every file-target run meets `R1`.

## The diagnosis, and the two candidates

**What the first review does.** The run that shows the defect, and #468's run, read the working headline the same way. Each held the headline to the body's referent test: an ellipsis that only the standfirst fills in (*en ellips som först standfirsten fyller i*), words with *nothing to refer to* (*saknar något att syfta på*). Each then asked the headline for the text's particulars, meaning what was measured, what happened and what the limit was, and not for its subject. The loaded headline review already says that an allusion may name its subject in general terms where the text's first lines give the particulars. What it did not say is what a reader of the headline alone is owed, or that a word the text fills in is the allusion at work and not an open reference. Neither run reached that rule.

**How the finding reaches the report.** It does not arise at the reporting stage. In both runs the report carries the first review's finding as step 7 says it must: as repaired where the round was accepted, and as unresolved for the author where the round was rejected and the text restored. The reporting rules work as written. A false finding at the first review is what makes a false entry in the report.

**The first candidate**, `f39a3721`, added to the allusion item in `headlines.review.md`'s *Leave alone* that the reader of a heading alone is owed the subject and not its particulars. It said that what the heading leaves for the text to fill in is the allusion at work and not a reference left unresolved. It also said that the test of a pronoun, a definite form or an ellipsis that only another part completes belongs to the body, read with the paratext covered, and is not applied to a heading.

**The revise round.** The first candidate missed the Target on the lead rewrite in `post-article-clean-file-2`. That run's first review recorded a finding against the lead's sentence on sensor placement. It cited the article genre's rule that the angle is followed through and the anatomy's rule that the ending shows the lead's expectation met, and the correction round rewrote the sentence. The same finding is in both arms: in `pre-article-clean-file-2`, `pre-article-allusion-file-1` and `pre-article-overclaim-2` it is left unresolved, and #468 recorded it too. No wording of the candidate is cited in it. The candidate's only clause that names the body at all is the sentence pointing the reviewer at the body's referent test. So the revised candidate, `e4fe5890`, takes that sentence out and keeps the rest. It is the smaller of the two candidates, and the record does not claim that the removal is what stopped the lead rewrite: the finding came once in the revise round too, in `rev-article-clean-resp-3`, where the run rejected its own round and left the finding unresolved.

**What ships.** The allusion item now reads, after *may name it in general terms where the text's first lines give the particulars*: *That reader is owed the subject, not its particulars: what the heading leaves for the text to fill in — what a contrast sets apart, what an image stands for, the figures and the findings — is the allusion at work and not a reference left unresolved.* The sentence that makes a heading naming no subject at all a finding is unchanged. The diff names no word of the four inputs: none of *när*, *varför*, *Björkskolan*, *mätförsök*, *givare* or *temperatur* appears in `headlines.review.md`. It sets out no sentence template either. `base.review.md` is not touched, so nothing here meets #479's possible change there.

## The Controls

| Control | Pre-change | First candidate | Revised candidate | Regression |
| --- | --- | --- | --- | --- |
| `article-allusion`: no finding against its headline | held: 0 of 4 runs | held: 0 of 4 | not re-run, so read from the first candidate | none |
| `article-unnamed`: the unclear headline detected | 1 of 2 runs | 2 of 2 | not re-run | none |
| `article-overclaim`: the overclaim detected | 2 of 2 runs | 2 of 2 | not re-run | none |
| The standfirst's *kort*, in `article-clean` and `article-allusion` | held: no standfirst changed | held | held | none |

- **`article-unnamed` in the pre-change arm.** `pre-article-unnamed-1` detected the headline and repaired it to *Temperaturmätningar i Björkskolan visar när, inte varför*. Both judges record the detection. `pre-article-unnamed-2` is recorded as not detected, because both judges record it so and an agreed reading stands. That run's reply as the Harness returned it is a single cleanup line: *Inga filer har skrivits eller ändrats. `input.md` är orörd och de tillfälliga arbetsfilerna är borttagna.* Its transcript shows a full delivery written as an earlier text block. That block detected the headline as naming no subject, repaired it to the same headline as run 1, and was followed by one more tool call before the cleanup line. The reply a caller of the Harness gets therefore holds no text. That is a defect of its own, filed as #488. The detection count of 1 is lower than the transcript would give, and it is the count the frozen judging produces. Both candidate runs detected the headline and repaired it to *Temperaturmätningar(na) i Björkskolan visar när, inte varför*, and both judges agree on each.
- **`article-overclaim`.** Every run of both arms detected the overclaim and repaired the headline at the text's strength. The pre-change arm wrote *Kalla mätvärden i Björkskolan saknar ännu förklaring* and *Mätförsöket visar när luften i Björkskolan var kall*. The first candidate wrote *Mätförsöket visar när klassrumsluften i Björkskolan var kall* and *Björkskolans givare visar när luften understeg 20 grader*. Every judge passes `R1` and records the detection.
- **The rest of the contract.** In every run, the before-inventory shows `work/input.md` as the only file in the working directory (`S1`). The after-inventory shows nothing created, replaced or removed outside the Harness's configuration directory, apart from `work/output.md` in each file-target run (`O1`). No run shows a departure from whole-round rejection, the Correction Budget of 1, the closing Proofread pass, the input or the destination. `rev-article-clean-resp-3` and #468's run both rejected a whole round and restored its pre-round text, as step 7 says.

The two inputs not re-run in the revise round are read from the first candidate's arm, as the plan says. The revised candidate is that candidate minus one sentence, and the sentence removed is the one that kept the definite-form test off headings. Without it, nothing in the candidate speaks against reading *Siffrorna* as a reference left open. The record does not claim that this was measured.

## Ship

**The revised candidate ships**, under the plan's revise branch: it meets the Target and no Control regressed. `headlines.review.md`'s allusion item carries the wording quoted above. `test_an_allusion_owes_its_reader_the_subject_and_not_the_particulars` pins three things in that item: the subject is owed and not its particulars, a word the text fills in is not a reference left unresolved, and the item sends the reviewer to no test of the body. The test of the unchanged clause that a heading naming no subject at all is a finding sits beside them. The catalogue is regenerated. Redline's `help.md` does not describe working headings, so it does not change. No decision record is written: the defect reproduced, and the change is prose in a review half that one commit reverses.

## Filed

- #487: the false finding against `article-clean`'s lead sentence on sensor placement, which one first-candidate run repaired by rewriting the lead.
- #488: a response-target run whose last message is its cleanup line, so the reply a caller of the Harness gets holds no text.

## Inventories

Wave 1 held the pre-change arm's fourteen runs, wave 2 the first candidate's fourteen, and wave 3 the revise round's six. [`runs/waves/`](runs/waves/) holds each wave's before and after inventories of scopes 3 to 5.

- **Scope 3.** The build's scratch root changed only under paths this build wrote: `packets/`, `inputs/`, `logs/`, `exp/`, `msgs/`, `j/`, `v/`, `judges.tsv`, `validators.tsv` and the helper scripts.
- **Scope 4.** This build's working tree changed only by the wave inventory files themselves and the build's own commits. The main checkout's `HEAD` moved from `fb169087` to `fe2587b7` during wave 2, which is other sessions integrating their work, and did not move during waves 1 and 3.
- **Scope 5.** The session scratchpad changed under `own/`, where the run's orchestrating session keeps its files. Top-level `out.md` and `out_b.md` came and went, and two judges of this build reported writing and deleting such files. No run's transcript names the scratchpad, and each run's working directory, home and temporary directory were private roots the runner removed, so no change there is attributed to a run.

Every run's `filesystem-changes.json` shows only files created under the Harness's configuration directory (`home/.claude/`) and, for each file-target run, `work/output.md`.
