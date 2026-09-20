# Real Skill runs, results

Run on 2026-09-20 as `plan.md` says: nine `/write` runs and four `/redline` pairs, each a fresh `claude-opus-5` subagent at high deliberation in Claude Code, against a staged byte copy of the working tree. Nothing was rerun. Each run directory holds `write/` (source, reply, evidence, inventories), `draft.md` where a draft was delivered, `judgement.md`, and for four rows `redline/`.

One difference between what ran and what is committed: the comparison task that ran ends "Write the paired accounting and findings to the report path"; the committed task says "Write the complete claim accounting and findings …", the wording the writer's paragraph and `help.md` use, restored after the independent review. No run was made after that edit.

## Write

| Row | Outcome | Comparisons | Delivered prose = last checked prose | F1 | G2 | L1 | Judge's class | Wall time |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `opinion-en_US-r1` | stopped | 2 | not delivered | fail (last draft) | pass | pass | valid stop | 1 024 s |
| `opinion-en_US-r2` | stopped | 2 | not delivered | fail (last draft) | pass | pass | valid stop | 963 s |
| `opinion-en_GB-r1` | delivered | 2 | yes | pass | pass | pass | valid delivery | 896 s |
| `opinion-en_GB-r2` | delivered | 2 | **no** | **fail** (judge: pass, one residual) | pass | pass | valid delivery | 925 s |
| `opinion-sv-r1` | delivered | 2 | yes | pass | pass | pass | valid delivery | 871 s |
| `column-sv-r1` | delivered | 2 | yes | pass | pass | pass | valid delivery | 688 s |
| `column-sv-r2` | delivered | 1 | yes | pass | pass | pass | valid delivery | 418 s |
| `case-study-en_US-r1` | delivered | 2 | yes | pass | pass | pass | valid delivery | 1 191 s |
| `opinion-absence-en_GB-r1` | delivered | 2 | yes | pass | pass | pass | valid delivery | 726 s |

Median wall time 896 s. The GPT-family selection in #329 had a median of 616 s; different models, harnesses and cases, so not a comparison of cost. Side effects, from the inventories: in all nine runs `source.md` and the staged install are unchanged and nothing remains but the two files the evaluator asked for.

### What the runs show

- **The variable swap did not occur.** All four English opinion drafts rendered "digital vana" as habit or familiarity from the first draft on ("digital habits", "digital habit", "how used to digital services people are"). No checker in a real run had the swap to catch. In this family it was exercised only in `../checker/`.
- **Supported reflection was kept.** Neither column run had a finding against a reflective transition, a struck passage or a stop. `column-sv-r1`'s two repairs (an added claim that such a discovery "knappast går att boka in i förväg"; "hos någon" for the notes' "hos andra") were judged supported.
- **Real faults were still caught.** Judged supported repairs include: "calls" for phone bookings, an absence widened from the documents to the world, time per booking for time per booking route, and, in five runs, a flat "we have not costed it" for the source's "gör inget anspråk på" (the #349 boundary). The case study dates only the decision to September and leaves the supplier choice undated (#344). The unknown/absent control leaves the consent status unclaimed (#355).
- **Sharp criticism survived.** `opinion-sv-r1` rejected a second-round finding against "det underlaget finns inte i dag" with a stated reading; the judge classed the rejection correct.
- **Both American English rows stopped.** Each second comparison found a real defect the first had not (a lead promising cost figures where the trial records time; a title committing the author to removing the phone). Both stops were judged valid. A stop is not a delivered draft, so the ticket's criterion of repeated delivered US drafts is **not met**.
- **One delivery broke the gate.** `opinion-en_GB-r2` made three repairs after the second comparison and delivered; its own `dispositions.md` says so. The repairs used the checker's proposed wording and the judge classed the delivery valid on the merits, but the delivered prose was never compared. `source-check.md` forbids this and the run did it anyway. The gate's wording is unchanged by this ticket, and no Claude-family baseline exists to say whether the change made it likelier.
- **A residual no checker caught.** The same draft ends "The trial costs something we have not costed", a denial where the material only declines to claim, in a draft whose first round had repaired that exact error elsewhere. The judge passed F1 with this as a cited residual. The protocol does not let an unsupported fact pass and the plan fixed "unknown kept apart from absent" under F1 before the runs, so the record scores it `fail`; the judge's reading is kept beside it.
- **Not flagged by any judge, observed by the evaluator:** three of four English drafts render "funktionsförmåga" as bare "ability", and two checkers cleared it by testing one direction ("nothing here could be funktionsförmåga without being ability"). "Measures nothing about ability" denies more than the source does.
- **Evidence gaps.** In `column-sv-r1` and `opinion-absence-en_GB-r1` the harness refused the checkers' file writes; the reports came back as text and only the drafts reached `evidence/`. Their intermediate judgements rest on the writer's account. Three runs overwrote their first draft in place.

## Redline pairs

Redline loads nothing this ticket changes. The pairs document what a source-blind review does to the drafts above. Inventories: `input.md` and the install unchanged in all four.

| Pair | R1 | Did a change remove or alter something the source required? |
| --- | --- | --- |
| `opinion-en_GB-r1` | **fail**: ten changes, one a real repair, nine of taste on a clean text, none reported | yes: "administration" became "officers" twice (the source's *förvaltningen*); "channel" and "route" merged |
| `opinion-en_GB-r2` | pass; the account calls "We make no claim to have … costed" → "We have not costed" "preserved in full" | yes: the funding disclaimer and the no-claim modality |
| `column-sv-r1` | pass | no |
| `column-sv-r2` | **fail**: two whole sentences deleted from a clean text, accurately reported | yes: both are the source's own caveats, near verbatim |
| `opinion-en_US-r1`, `-r2` | skipped: Write stopped, nothing to review | |
| `opinion-sv`, `case-study-en_US`, `opinion-absence-en_GB` | skipped: not paired, as `plan.md` says | |

In three of four pairs the sentence Redline changed is one that Write's comparison had made careful on purpose. Redline cannot know that, by contract. It is recorded here as a finding about how the two Skills meet, outside this ticket's change.
