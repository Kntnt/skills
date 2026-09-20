# Results for #377

The post-change arm and the controls, run on 2026-09-20 against the method [`plan.md`](plan.md) froze before the first run. The pre-change arm is [`diagnosis.md`](diagnosis.md). Artefacts: `runs/`. The record is [`../records/redline-claude-2026-09-20-377.md`](../records/redline-claude-2026-09-20-377.md).

Twenty-two Redline invocations — four pre-change, eight post-change, ten controls — and forty-four judgements, two per artefact, each a fresh `kntnt-opus-high` subagent blind to the arm, to the model and to this ticket. No Codex Harness and no GPT model was started, controlled or invoked from this session. No source material was supplied to Redline in any run: every working directory held `input.md` and nothing else.

## The four inputs, twice each

| Run | Differences | Limiting sentences deleted or weakened | Changes to what a claim says, and whether the account names them | `R1` A / B |
| --- | --- | --- | --- | --- |
| `post-column-sv-r1-a` | 4 | 1 deleted, **class (a)** on both judgements | 1 (scope, meaning), **named** in the reply's *Ändrat* section with both wordings quoted | fail / fail |
| `post-column-sv-r1-b` | 1 | none | none | pass / pass |
| `post-column-sv-r2-a` | 1 | none | none | pass / pass |
| `post-column-sv-r2-b` | 1 | none | none | pass / pass |
| `post-opinion-en_GB-r1-a` | 8 | none | 4 (attribution ×3, scope and meaning ×1), **all named** in *What the corrections did to the claims* | pass / fail |
| `post-opinion-en_GB-r1-b` | 8 | none | A: 1 (certainty, chronology); B: 2, adding one of scope. **Both named**; judge B holds the second's class is asserted away | fail / fail |
| `post-opinion-en_GB-r2-a` | 4 | none | none | pass / pass |
| `post-opinion-en_GB-r2-b` | 3 | none | none | fail / pass |

**N1 — met in all eight runs.** Across sixteen judgements, one limiting sentence was deleted and none was weakened or hardened. The deletion is `post-column-sv-r1-a`'s `Det är min reflektion, med den räckvidd en reflektion har.`, and the reply reports the finding that licensed it: the sentence immediately before it already states the whole of that limit. Both judges verified that from `work/input.md` alone and both answered **class (a)**; both record that the deletion raises nothing the text asserts.

One tension in the wording is worth recording. Both judges answered **no** to *does the reply name a defect inside that sentence, as opposed to naming the whole sentence as the defect*, and then answered **(a)**. Class (a) is a relation between two sentences rather than a fault inside one, so a finding of class (a) can never name something interior; the criterion this ticket is held to asks for *a finding of class (a) or (b), verified by a judge from the input alone*, and that is what both judgements record. The Skill's own wording answers the same way: its `SKILL.md` and its correction brief now permit the deletion only where a retained sentence still states the limit in full, which is what the run said and what both judges checked.

**The behaviour the ticket was filed for does not recur.** `pre-column-sv-r2` deleted `Det här är en iakttagelse av ett dokument, inte en scen från ett visst möte.` and `Det är min reflektion, inte något jag har mätt hos andra.` on the ground that the finding named the whole sentence, and both judges found neither class (a) nor class (b). Both post-change runs on that input return both sentences byte for byte and raise no finding at all. `pre-opinion-en_GB-r1` hardened `I am not against digital booking.` into `I support digital booking` unreported; both post-change runs on that input keep it verbatim.

**N2 — met in all eight runs.** Every change to what a claim says that either judge identified is named in the reply that made it. The two `opinion-en_GB-r1` runs are where this is visible: eight differences each, and the replies report the claim changes individually, with both wordings and the finding each answered. `post-opinion-en_GB-r1-a` reports the two attribution moves and the `We` → `Öppna beslut` narrowing the #362 run made silently; it also states of the disclaimer that both disclaimed items survive, which both judges verified.

One split is recorded rather than resolved. In `post-opinion-en_GB-r1-b`, `the work each route costs staff` became `what each route costs staff`. The reply names the change and says its scope stands; judge A agrees and records the borderline, judge B calls it a change of scope whose class the reply asserts away. Both classes stand; neither judge is an oracle. Under the stricter of the two the change is still **named**, which is what N2 asks.

**`R1` is not this ticket's criterion for these eight runs, and it is recorded as measured.** Ten of sixteen judgements pass, against one of eight before the change. Every one of the six failures turns on the same thing, and it is not a limiting sentence: a clean passage rewritten to taste outside any finding — an opening claim widened in `post-column-sv-r1-a`, `set … against` becoming `weigh … against` and `channel` becoming `route` in the opinion runs. That is the second half of what #362 found and the half this ticket did not set out to repair; the readiness addendum scopes the body's *clean texts are returned unchanged* to the five clean controls alone and says in as many words that it does not reach these four inputs. It is filed for triage as [#383](https://github.com/Kntnt/skills/issues/383).

## The ten controls

Each run once against the post-change install, judged on `R1` against that control's frozen expectation in the corpus's *Redline controls* table.

| Control | `R1` A / B | What the judgements record |
| --- | --- | --- |
| `article-clean` | pass / pass | Returned unchanged; heading, independent ingress and absent byline preserved; ABT-shaped logic selected no technique; no numerical or missing-name finding. |
| `article-flawed` | pass / pass | Catastrophe certainty, health certainty, the thrice-repeated lead and the late `operativ temperatur` concept all detected and named; measured facts, exclusions and `fast finansieringen inte är beslutad` preserved. Both judges record the paragraph split as repaired in the text but not named as a finding. |
| `case-study-clean` | pass / pass | Returned unchanged; customer agency, the qualified appraisal, every number and the publisher disclosure preserved. |
| `case-study-flawed` | pass / pass | Supplier praise, the rescue claim and the causal contradiction detected and reported with the claim each removal took; the customer's reservation and every measure preserved; two findings reported as needing material the text lacks. Both judges record the pre-echoed quote and the duplicate lead as repaired but unnamed. |
| `column-clean` | pass / pass | Returned unchanged; reflection, early point, purposeful recurrence, the single H1 and the 103-word paragraph preserved. |
| `column-flawed` | pass / pass | The incompatible participation claims reported as unrepairable with the scene returned verbatim rather than replaced; generic opening and ending removed and reported; reflection and doubt preserved word for word. |
| `opinion-clean` | pass / pass | Returned unchanged; the polemical close, the early thesis, the attribution, the administrative objection and the cost uncertainty preserved; no hedge added. |
| `opinion-flawed` | pass / pass | Unsupported motives, the population inference against the booking denominator, the cost contradiction and the vague exhortation all detected and named; qualified facts, both figures and the proposal preserved; the ending rebuilt from the actor and action already in the thesis. Both judges record two section headings rewritten and unreported. |
| `web-copy-clean` | pass / pass | Returned unchanged; the information page survives with no sales template and no CTA; nothing invented. |
| `web-copy-flawed` | pass / pass | The calque, the abstract opener, the opaque headings and the `Book and pay now` label contradicted by the page all detected and named; price, scope, timing, deliverables, conditions and destination preserved; the one repair needing an absent fact reported unresolved. |

**C1 — met on all ten.** No control missed its frozen expectation, so the plan's re-run of a missing control against the pre-change install was not needed and was not made. The five flawed controls that require a real removal or a real repair each made one and accounted for it; the five clean controls each came back with no editorial change at all, so the question the addendum settles — whether a locale-mechanical correction from the step 9 Proofread pass counts against a clean control — did not arise in any of them.

## Side effects

`O1` — met on all twenty-two runs, from the before-and-after `sha256` inventories in each run directory. In every run the diff over the working copy and the staged install is empty, `work/input.md` is unchanged, and the run directory holds nothing the Skill created: no scratch directory survived any run. The `response.md` in each is the evaluator's, written by the one instruction the turn adds to the Skill; `judgement-a.md`, `judgement-b.md` and one judge's `judge-a-returned.txt` under `control-case-study-flawed` were written by judges after the run's after-inventory was taken.

The committed `inventory-before.txt` and `inventory-after.txt` carry one `sha256` over the working copy's listing, one over the staged install's listing, and the run directory's listing in full; `inventory-outside-diff.txt` carries the diff of the two large listings, and is empty in all twenty-two runs. The full listings ran to 1.6 MB per run and are not committed.

## `T1`, `R2` and the rest

`T1` and `R2` are recorded `skipped` on every run: both are answerable only from a Harness trace, and a session cannot read the transcript of a subagent it started. Nothing here claims either passed and nothing fails for lacking them. Every other criterion the corpus applies to a run of this kind — `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — is recorded `skipped`, naming `R1`, `N1`, `N2` and `C1` as this ticket's criteria.

## What is measured and not fixed

- **Redline still rewrites clean passages to taste, outside any finding and mostly unreported.** Six of sixteen post-change judgements fail `R1` on it, and four of the twenty control judgements name it as their one reservation. Filed as [#383](https://github.com/Kntnt/skills/issues/383).
- **A judge writing scratch to a shared path can read another judge's text.** One judge reported finding `/tmp/after.md` overwritten under it mid-task by a concurrent sibling, noticed, and recovered. Every judge launched after that was told in its message to keep scratch inside its own run directory. The judgements written before it are self-consistent — each quotes the input and the returned text it compared — but the hazard is recorded rather than argued away.
- **The `column-sv-r2` frontmatter damage** #362 recorded is filed as [#384](https://github.com/Kntnt/skills/issues/384) and was neither fixed nor counted here.
- **Whether Unslop's whole-passage permission needs the same narrowing** is filed as [#385](https://github.com/Kntnt/skills/issues/385). Nothing here measured Unslop.
