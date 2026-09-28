# Results for #415

The pre-change arm, run and judged against the method [`plan.md`](plan.md) sets out, frozen at `22ef6183` before the first run and not edited since. Artefacts: `runs/`. The record is [`../records/redline-claude-2026-09-28-415.md`](../records/redline-claude-2026-09-28-415.md).

**The headline result: not reproduced.** None of the eighteen pre-change runs counts. All thirty-six paratext judgements answer `no`, so there is no split either. As the plan's *Sequence and exit* settles:

- no product file changes, and no candidate wording was written;
- the frozen briefs were not run over the arm, and the post-change arm was not run;
- the decision record is [ADR-0223](../../adr/0223-a-part-that-asserts-past-a-kept-limit-is-measured-first-and-not-written-into-the-limit-rule.md);
- [`paratext-judge-brief.md`](paratext-judge-brief.md) and the counting rule in `plan.md` stay as the criterion a later evaluation uses to measure the form.

## The four instances #383's judges named

The four judge reports the readiness addendum lists are the whole of this account. Each was read, and its instance was located in its run's `response.md` against that run's `work/input.md`, under [`../editorial-383/runs/`](../editorial-383/runs/). All four are in the two Swedish column drafts. In each, a headline, subheading or standfirst the run wrote asserts past a limiting sentence the returned text keeps word for word.

| # | Report | The part the run wrote | The limiting sentence kept | What the part asserts that the sentence bounds |
| --- | --- | --- | --- | --- |
| 1 | `pre-column-sv-r1/judgement-a.md`, lines 63–72 | Subheading `## Ett försök är värt en ruta till` (`response.md` line 33) | *Jag vet inte om ytterligare en ruta gör våra möten bättre. Kanske blir frågan bara en rad till att fylla i.* (`work/input.md` line 22), and the closing *Jag vill prova den i alla fall, och behålla båda hållningarna så länge* (line 24) | A conclusion those sentences withhold: that the trial is worth one more box. This is the judge who names the form "superscription". |
| 2 | `pre-column-sv-r1/judgement-b.md`, lines 19, 21 and 58 | Subheading `## Bokad tid är inte samma sak som uträttat arbete` (`response.md` line 21), and the subheading in instance 1 | *Jag har inte mätt det här hos andra, och jag påstår inget om möten i allmänhet.* (`work/input.md` line 16), and the sentences in instance 1 | More general: a claim about booked time in general over a section that disclaims any claim about meetings in general. The second subheading repeats instance 1. |
| 3 | `post-column-sv-r2-a/judgement-a.md`, line 11 | A standfirst the run added, opening *En full kalender är inget kvitto på att något blivit bestämt.* (`response.md` line 13) | *Det är min reflektion, inte något jag har mätt hos andra.* (`work/input.md` line 16; `response.md` line 23) | Sharper and more general: a flat general truth where the text offers the writer's own unmeasured reflection. |
| 4 | `post-column-sv-r2-b/judgement-a.md`, line 13 | The standfirst sentence *Du får en fråga att ta med till nästa dagordning.* (`response.md` line 13) | *Jag vet inte om den överlever mötet med en verklig dagordning, och jag tänker inte låtsas att jag gör det.* (`work/input.md` line 22; `response.md` line 33) | **A variant.** It promises the reader a takeaway, and the limit contradicting it is in the closing section rather than under the standfirst. It still counts under the question, which does not ask where the limit sits. |

**What the four have in common.** Every part was absent from `work/input.md`. Both drafts arrive with a headline, a byline and body paragraphs, and no standfirst and no subheading. In each instance the run wrote the part into a finished text that lacked it, which is the behaviour #397 was filed for. Instances 1 and 2 are from #383's pre-change arm, and 3 and 4 from its post-change arm, so the form is not a consequence of #383's change. In instance 1 the run's own reply reports the subheading it wrote as a remaining finding (`response.md` line 54), saying it *drar en slutsats som texten avstår från*. So that run saw the defect and still delivered it.

## The runs

| Arm | Staged from | Runs | Made |
| --- | --- | --- | --- |
| pre | `708bff52` (`<start>`) | `pre-<draft>-a` then `pre-<draft>-b` on each of the four drafts; `pre-control-<row>` on each of the ten controls | 18, on 2026-09-28 between 09:23 and 09:45 UTC |
| post | — | not run: the pre-change arm shows no form to measure | — |

- **The sessions.** Every run was a fresh top-level Claude Code 2.1.283 session started by [`runs/turn_run.sh`](runs/turn_run.sh) with `--model=claude-opus-5-5 --effort=high`.
- **The seat.** Each run's `seats.tsv` names `claude-opus-5-5` alone, for the session and for each correction subagent in it. Fifteen runs started a correction subagent. `article-clean`, `column-clean` and `web-copy-clean` started none, because they found nothing to correct.
- **The replies.** Every run ended with return code 0 and terminal reason `completed`. Each run's `response.md` is byte-identical to the reply the Harness returned, `response.txt`.
- **Scheduling.** Runs on different inputs ran side by side, at most five at once, and the two runs of each draft ran one after the other.
- **The inputs.** Each run's `work/input.md` hashes to the matrix's SHA-256 prefix.
- **The install.** The staged install was byte-identical to `git archive` of `708bff52` after the last run.
- **Judging.** Each run was judged by two fresh `kntnt-opus-high` judges on the paratext brief. Each judge worked in its own `mktemp -d` directory, whose mapping to runs is `runs/judges.tsv`, and every directory was removed after its judgement was copied.
- **Isolation.** No Codex Harness and no GPT model was started, controlled or invoked. No source material was supplied to any run.

No run and no judge was void.

## The pre-change arm, by the paratext brief

A run counts when both judges answer `yes`. Here, where the paratext is changed, it means a headline, subheading or standfirst the returned text carries in wording `work/input.md` does not. This session read that column mechanically from the two files.

| Run | What the run did to the headline, subheadings and standfirst | A | B | Counts |
| --- | --- | --- | --- | --- |
| `pre-column-sv-r1-a` | headline `Mallen har en ruta för allt utom poängen` → `Bibliotekets mötesmall har rutor för allt utom poängen` | no | no | no |
| `pre-column-sv-r1-b` | none; one dash in the body | no | no | no |
| `pre-column-sv-r2-a` | headline `Rutan som inte finns` → `Mötesmallen kan behöva ett varför bredvid klockslagen`; the missing standfirst and sections reported, not written | no | no | no |
| `pre-column-sv-r2-b` | headline `Rutan som inte finns` → `Mötesmallen frågar efter tid och deltagare, inte syfte` | no | no | no |
| `pre-opinion-en_GB-r1-a` | third subheading → `Find out why people still ring before settling how booking works`; a byline added under the headline | no | no | no |
| `pre-opinion-en_GB-r1-b` | third subheading → `Measure staff time and ask why people still phone before deciding`; a byline added under the headline | no | no | no |
| `pre-opinion-en_GB-r2-a` | headline `Keep the telephone until …` → `Keep telephone booking until …` | no | no | no |
| `pre-opinion-en_GB-r2-b` | the same headline change as `-a` | no | no | no |
| `pre-control-article-clean` | none; the no-change status | no | no | no |
| `pre-control-article-flawed` | headline → `Mätförsök i Björkskolan fann värden under 20 grader`; the standfirst rewritten | no | no | no |
| `pre-control-case-study-clean` | none; its one round rejected and the text returned unchanged | no | no | no |
| `pre-control-case-study-flawed` | headline → `Elm Quays ärenden tilldelades snabbare under försöket`; the standfirst rewritten; both subheadings replaced and two added | no | no | no |
| `pre-control-column-clean` | none; the no-change status | no | no | no |
| `pre-control-column-flawed` | headline `Möten förändrar allt` → `Mötesmallen rymmer inte det vi ska förstå tillsammans` | no | no | no |
| `pre-control-opinion-clean` | none; one sentence of the lead | no | no | no |
| `pre-control-opinion-flawed` | none; its one round rejected and the text returned unchanged | no | no | no |
| `pre-control-web-copy-clean` | none; the no-change status | no | no | no |
| `pre-control-web-copy-flawed` | headline → `A review of how a shared room in your housing association is booked`; the six fragment headings replaced by one subheading; the opening paragraph rewritten | no | no | no |

**Count: 0 of 18.** No split.

**What the judges read in the rewritten parts.** The judges' replies say why each changed part does not assert past a kept limit:

- **`column-sv-r2`.** The new headlines are hedged below the body's own strength. `pre-column-sv-r2-a` says *kan behöva* where the body says *borde*. `pre-column-sv-r2-b` stays an observation of the one document.
- **`column-sv-r1`.** The rewritten headline names the one template the text says it examines. That makes it narrower, not more general.
- **`opinion-en_GB-r1`.** The new third subheadings say what their section already says.
- **The flawed controls.** The rewritten headlines and standfirsts claim no more than the limits the texts keep. `case-study-flawed`'s new headline says only that assignment was faster during the trial, beside the kept sentence that the difference cannot be credited to the software.

## Why the form did not reproduce

**Every instance #383's judges named was a part written into a text that had none.** In this arm, no run wrote a standfirst or a subheading into a draft that lacked one. `pre-column-sv-r2-a` reported the missing standfirst and sections and left them unwritten, saying *En granskning skriver inte en del som saknas*. That is #397's change, which is in `<start>`. [#397's results](../editorial-397/results.md) recorded the same: every draft run wrote such parts before its change, and none after it. The route by which the form reached #383's drafts is closed.

**A part the run changes can still carry the form**, and the arm gave it that chance. Eleven of the eighteen runs changed a headline, a subheading or a standfirst that the text already had: seven on the drafts, four on the controls. No judge found any of them asserting past a kept limit.

**What this does not show.** The arm tests the form on these fourteen inputs, on `claude-opus-5-5`, against the product as #397, #398, #400 and #402 left it. It does not show that Redline could never write such a part. It shows only that the shipped rules produce none on these inputs, so there is no miss for a change to the limit rule to be measured against. [ADR-0223](../../adr/0223-a-part-that-asserts-past-a-kept-limit-is-measured-first-and-not-written-into-the-limit-rule.md) records the decision and what would reopen it.

## Criteria not scored

- **`R1`, `N1` and `C1`** are recorded as not run. The plan runs the frozen briefs over the pre-change arm only where that arm shows the form, and it does not.
- **The limiting-sentence protection** is recorded as not exercised. The sixth criterion compares a post-change arm with this one, and no post-change arm was run. No product file changed, so no protection already shipped could weaken.
- **`A1`, `A2`, `N2`, `O1`, `S1`, `C2`, `T1`, `R2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2` and `T2`** are recorded `skipped`, as the plan settles.

No remaining miss is filed, because the arm has none.

## Departures, disclosed

- **The judges' directories** were made with `mktemp -d` in the system temporary directory, outside the build's worktree and scratch root. The plan declares this departure, as #385, #398 and #402 did: a path under the scratch root would name this ticket.
- **No `expectation.md`** was written into a control's run directory. The plan lists it for a control, but only a control judge on the frozen brief reads it, and none was sent.
- **The install layout** strips `skills/kntnt` by one component, not two as the clarifications' example has. The plan says why.
- **`main` moved during the build**, from `708bff52` to `61bcdc99`. The installs are written by `git archive` from `708bff52`, so no run read the moved tree.
