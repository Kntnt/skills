# Results for #383

Both arms and the ten controls, run on 2026-09-22 against the method [`plan.md`](plan.md) froze before the first run. Artefacts: `runs/`. The record is [`../records/redline-claude-2026-09-22-383.md`](../records/redline-claude-2026-09-22-383.md).

Twenty-three Redline invocations — four pre-change, eight post-change on the same four inputs, ten controls, and one pre-change replay of the single control that missed — and forty-six judgements, two per artefact, each a fresh `kntnt-opus-high` subagent blind to the arm, to the model and to this ticket. No Codex Harness and no GPT model was started, controlled or invoked from this session. No source material was supplied to Redline in any run: every working directory held `input.md` and nothing else before its turn was dispatched.

**The headline result.** The three changes this ticket makes are in the product and they do what they were built to do: every difference a round returns is traced to a finding, and every reply now closes with a paragraph saying by kind what the run changed beyond the claim account. On the controls that is a clear gain — all three of the blemishes [#377 recorded](../editorial-377/results.md) are now covered, and the `article-flawed` and `opinion-clean` defects [#386](../editorial-386/runs/results.md) recorded are gone. On the four #362 drafts the criteria `A1` and `A2` are **not met**, and not for the reason this ticket was filed: what the judges now class as taste outside any finding is the article anatomy's missing-part requirements — a standfirst, subheadings, a call to action — being repaired by authoring new prose into a text that has none. That arrived in the product after #377's arm was run and is outside what #383 settles. The measured result is recorded as measured, the post-change arm ships as the better of the two, and the residual is filed.

## Why the pre-change arm was replayed

#383 allows #377's post-change arm to serve here only if nothing Redline loads has changed since. The diff against `0f490dd4` is twenty-seven files, and five of them did not exist then: `article-anatomy.md`, `article-anatomy.review.md`, `headlines.md`, `headlines.review.md` and `scripts/article_anatomy.py`, all of which Redline now loads, measures with and reviews against for `article`, `case-study`, `column` and `opinion`. `base.review.md`, `delivery.md`, seven genres, both techniques, the shared craft brief, Redline's own `SKILL.md`, its `help.md` and its correction brief changed too. So the four inputs were replayed once each against `3167fb68` before any wording was touched.

That replay is what makes this evaluation readable at all: the same defect the judges name in the post-change arm is present in the pre-change arm in the same shape and the same strength.

## The four inputs

`R1` fails on every judgement of both arms — eight of eight before the change, sixteen of sixteen after. The failure clause is the same in all twenty-four: *clean texts may not be rewritten to satisfy taste or numerical guidelines*.

| Run | Arm | Differences (A / B) | Changes to a claim (A / B) | Limiting sentences deleted or weakened | `R1` A / B |
| --- | --- | --- | --- | --- | --- |
| `pre-column-sv-r1` | pre | 7 / 9 | 3 / 6 | none | fail / fail |
| `pre-column-sv-r2` | pre | 7 / 8 | 1 / 1 | none | fail / fail |
| `pre-opinion-en_GB-r1` | pre | 11 / 12 | 2 / 4 | none | fail / fail |
| `pre-opinion-en_GB-r2` | pre | 4 / 5 | 1 / 0 | none | fail / fail |
| `post-column-sv-r1-a` | post | 9 / 7 | 0 / 3 | none | fail / fail |
| `post-column-sv-r1-b` | post | 6 / 8 | 0 / 0 | none | fail / fail |
| `post-column-sv-r2-a` | post | 6 / 7 | 3 / 2 | none | fail / fail |
| `post-column-sv-r2-b` | post | 6 / 9 | 2 / 3 | none | fail / fail |
| `post-opinion-en_GB-r1-a` | post | 10 / 12 | 2 / 3 | none | fail / fail |
| `post-opinion-en_GB-r1-b` | post | 11 / 11 | 1 / 5 | none | fail / fail |
| `post-opinion-en_GB-r2-a` | post | 9 / 9 | 2 / 1 | none | fail / fail |
| `post-opinion-en_GB-r2-b` | post | 6 / 6 | 2 / 2 | none | fail / fail |

**`N1` — met in all eight post-change runs, and in all four pre-change runs.** Across forty-eight limiting-sentence readings not one sentence was deleted, weakened or hardened; every judgement records them surviving byte for byte, both halves of every two-part disclaimer included. `We make no claim to have funded or costed that trial`, `Det är min reflektion, inte något jag har mätt hos andra` and `Det här är en iakttagelse av ett dokument, inte en scen från ett visst möte` come back verbatim in every run of both arms. What #377 repaired stays repaired.

**Four judges name a fourth form of hardening, and it is worth recording.** The judge brief tests for three forms, all of them edits to a limit, and invites a judge finding a fourth to name it. `pre-column-sv-r1`'s judge A calls it **superscription**: a new unhedged assertion mounted *above* a limit the text retains. `pre-column-sv-r1`'s judge B, `post-column-sv-r2-a`'s judge A and `post-column-sv-r2-b`'s judge A report the same thing independently. The instance is always the same kind of sentence — a standfirst or a heading the run authored, asserting flatly what a retained sentence bounds. It appears in both arms, so the change measured here neither caused it nor removed it. It is not `N1`'s subject, which is what happens to the limiting sentence itself, and nothing in this evaluation scores it; it is recorded because a judge was asked to name a fourth form and four of them did.

**`N2` — met in seven of the eight post-change runs.** Every change to what a *received* claim says is named in the reply that made it, with both wordings, except in `post-opinion-en_GB-r1-a`: the headline `Don't switch off Lervik's phone booking before we know what it costs` became `Don't end phone booking before counting the cost`, and both judges record that the loss of `Lervik's` is a change of scope which the reply reports only as *the headline shorter*. Two further inaccuracies are recorded rather than counted, because in each the change *is* named and the error is in the description: in both judgements of `post-opinion-en_GB-r1-b` the reply says the shortened headline `asks for less than it did` where dropping the place name makes it ask for more, and in `post-opinion-en_GB-r2-a` judge A the reply files an altered claim under a heading that opens `No claim was removed`.

**`A1` — not met in any of the eight post-change runs.** In every one, both judges class the run's structural additions as a change of taste answering no finding: a standfirst or summarising ingress, two or three section subheadings, and — in the two `column-sv-r1` runs — a closing exhortation authored in the bylined writer's first person. The replies do not present these as findings either; they present them as parts the anatomy requires, in as many words:

> Jämfört med texten som den kom in har den fått struktur: en sammanfattande ingress före bylinen och mellanrubriker genom brödtexten, så att texten nu har ett inledande stycke, avsnitt och en avslutning.

> Two parts the anatomy requires were put in place.

> en ingress är tillagd där anatomin kräver en

**The trace check is not what fails here, and the evidence says so plainly.** A difference that answers an anatomy requirement traces to a finding of the review that commissioned the round, so the check accepts it, which is the check working as specified. The same additions are in the pre-change arm in the same quantity — `pre-opinion-en_GB-r1` has eleven differences to `post-opinion-en_GB-r1-a`'s ten, both including a manufactured lead, a relocated byline and rewritten subheadings — so nothing about them is a consequence of this ticket. What changed is that the run now says it did them.

**`A2` — not met in eight of the eighteen post-change replies, and the eight are these eight runs.** The *uncovered kind* half is met throughout: every judgement of every input run reports that each difference is disclosed at least generically, and one says so in terms — `Not reported: nothing.` The *false statement* half fails, and it fails on one sentence in every case: the itemised claim account's closing assurance that no claim was removed and none was left standing with its scope, certainty, attribution, chronology, causality or meaning moved. That sentence is scoped to the claims the run *received*, and it is true of them; the judges read it against a text that now carries assertions the run *added*, and call it false or misleading.

- `post-column-sv-r2-b`, both judges: `inget påstående har tagits bort eller fått ändrad omfattning, säkerhet, attribution, kronologi, kausalitet eller innebörd` against a new ingress asserting `En full kalender är inget kvitto på att något blivit bestämt` over a retained `Det är min reflektion, inte något jag har mätt hos andra`.
- `post-opinion-en_GB-r1-a`, both judges: `Nothing. No passage carrying a claim was removed, and no claim was left standing with its scope … moved` beside a manufactured lead asserting what the papers before the board comprise.
- `post-opinion-en_GB-r2-b`, both judges: `Nothing else shifted in scope, certainty, attribution, chronology or causality` contradicted by the run's own finding 2 on the same page.
- `post-column-sv-r1-a` judge B, `post-column-sv-r1-b` judge A, `post-column-sv-r2-a` judge A and `post-opinion-en_GB-r1-b` judge B record the same sentence, or a qualifier inside the closing summary, as false against the delivered text.

**What #383's decisions do not reach.** The triage comment settles how a change to a claim is presented and how everything else is summarised. Neither says what a run owes a claim it *adds*, and the claim account's own wording — inherited from #377 — is written about claims received. Every one of these eight `A2` misses sits exactly there. Answering it is a requirement this ticket does not state, so it is filed rather than guessed at.

## The ten controls

Each run once against the post-change install, judged on `R1` against that control's frozen expectation in the corpus's *Redline controls* table.

| Control | `R1` A / B | What the judgements record |
| --- | --- | --- |
| `article-clean` | pass / pass | Returned unchanged, no findings; every preservation clause verbatim and every named rejection avoided. Both judges measured the limits themselves and confirm the text meets them. |
| `article-flawed` | pass / pass | Catastrophe and health certainty, the late concept, the 187-word lead, the missing byline, the absent subheadings and the closing sales line all detected; the 39-character headline failed on truthfulness rather than length; measured facts, exclusions and the funding caveat verbatim. The reservation is new: the standfirst/lead repetition is repaired but diagnosed as overclaiming instead of as the repetition. |
| `case-study-clean` | **fail / fail** | One difference: the subheading `## Två perioder med olika arbetsbelastning` became `## Anteckningen redovisar en kortare mediantid men ingen orsak`. Both judges class it as a taste rewrite of a conforming text and both note it now sits outside the 36–39-character band the expectation names. Preservation is otherwise perfect and the change is reported. |
| `case-study-flawed` | pass / pass | Supplier praise, the rescue line, the pre-echoed quote, the duplicate standfirst/lead and the causal contradiction all detected and quoted; the missing byline and the missing call to action reported and left unfilled; the customer's reservation, both quotations and every measure verbatim. Reservation: the two non-descriptive subheadings were replaced without their defect being named, and `Resultatet bevisar allt` is missing from the removed-claims list. |
| `column-clean` | pass / pass | Returned unchanged; the 83-word paragraph unsplit, the reflection, doubt, recurrence and non-commercial ending intact, every named rejection avoided. |
| `column-flawed` | pass / pass | The incompatible participation claims, the empty opening, the tautology and the recycled ending all addressed; every surviving sentence character for character; no replacement memory invented. Reservation: the headline was replaced with its defects never named, and its replaced claim is absent from the removed-claims list. |
| `opinion-clean` | pass / pass | Returned unchanged, no findings; the polemical close, early thesis, attribution, administrative objection and cost uncertainty verbatim; no hedge added. |
| `opinion-flawed` | pass / pass | Unsupported motives, the population inference against the booking denominator, the cost non sequitur and the vague exhortation all detected, repaired from the text's own material and accounted for; **the two label subheadings are now named as a finding and reported**. Reservation: the ending still sits inside the last section while the reply states the anatomy conforms. |
| `web-copy-clean` | pass / pass | Returned unchanged; the information page survives with no sales template and no CTA; nothing invented. |
| `web-copy-flawed` | pass / pass | The calque, the abstract opener, the six opaque headings and the misleading `Book and pay` label all detected and named; price, scope, timing, deliverables, the three link conditions and the destination verbatim. The run reports against itself that its own headline repair dropped `including VAT`. |

**`C1` — met on nine of ten.** `case-study-clean` misses.

**`C2` — met on all three.** Every control blemish `editorial-377/results.md` recorded is now either absent or covered:

- `opinion-flawed`'s **two rewritten section headings**, unreported in #377, are now a stated finding: *de två etikettunderrubrikerna* appear in the run's own list of what the round was given, and both judges confirm the label-heading clause of the frozen expectation is met.
- `article-flawed`'s **repaired paragraph split**, unnamed in #377, is now covered by the closing summary: *det 187 ord långa ledet är delat i ett led och fyra stycken fördelade på två sektioner*.
- `case-study-flawed`'s **pre-echoed quote and duplicate lead**, repaired but unnamed in #377, are now both detected and quoted; both judges record that clause of the expectation as met.

**What #386 found on four more texts is gone on three of them.** `opinion-clean` returned unchanged with no account to be wrong about, where #386 found an invented exclusion clause in its lead. `article-flawed`'s account now opens on the removed headline claim — *Att givarna räddar skolan från en katastrof — rubrikens påstående om räddning och katastrof* — where #386 found four claims listed and the headline not among them. `case-study-flawed` now names its removed claims with the finding each answered, though its two replaced subheadings are still unnamed, so that one is improved rather than clear. `case-study-sv` is a pipeline row and was not run here.

**`A1` and `A2` on the controls.** `A1` is met on nine of the ten: no judge classes a difference as taste outside a finding except on `case-study-clean`. `A2` is met on five of the ten — the four clean controls that changed nothing, and `article-flawed`, where both judges find every difference reported and no statement false. It misses on `case-study-clean` (the length change omitted, the scope shift denied), `case-study-flawed` (two differences unreported, the removed-claim tally short by one), `column-flawed` (the headline's replaced claim absent from the list), `opinion-flawed` (the reply states the anatomy conforms while the ending has no section of its own) and `web-copy-flawed` (the headline's `shared-room booking` inference unreported). Of the eighteen post-change replies, `A2` is met on five.

### The one control that missed, and what the replay establishes

`case-study-clean` was replayed once against the pre-change install, as the revise-and-remeasure allowance permits, to establish whether the miss is pre-existing. It is not: **both judges pass the pre-change replay.** That run changed one thing too — the lead's `Försöket pågick i åtta veckor` became `Ett försök med loggen pågick i åtta veckor` — and both judges class it as the repair of a visible defect, a definite noun phrase whose antecedent stood only in the standfirst.

What the replay does **not** establish is that the change measured here caused the miss. The two installs differ in six files, and none of them authorises a heading rewrite: the trace check restores a difference that answers no finding, the closing summary only says what happened, and the catalogue's guard narrows what may be recorded rather than widening it. The two runs raised *different* findings on the same clean text — a lead reference in one, a subheading's descriptiveness in the other — and one run per arm cannot separate that variance from a caused regression. Recorded as measured, and filed.

## Side effects

`O1` — met on all twenty-three runs, and `S1` with it, from the before-and-after `sha256` inventories in each run directory and the wave inventories beside them. In every run the staged install's digest is unchanged, `work/input.md` is unchanged, and the run directory's only new file is the evaluator's `response.md`. No `scratch/` directory survived any run: the two the `pre-opinion-en_GB` runs created during their turn were gone by the after-inventory, and a sweep for `scratch*` directories across the whole tree at the end of every wave found none.

Scope 4 is the two checkouts' `git status --porcelain --untracked-files=all` and `git rev-parse HEAD`, per the plan's declared narrowing. Across all six waves neither checkout gained a file from any run. `/Users/thomas/Projects/skills-388-391` shows only this session's own work in progress and `/Users/thomas/Projects/skills` only another session's; the `wave-<n>-*-repo.txt` files carry both.

The `judgement-a.md` and `judgement-b.md` in each run directory were written by judges after that run's after-inventory was taken, as were a handful of judges' own scratch files, each of which its judge reported deleting. `wave-<n>-before-scratch.txt` and `wave-<n>-after-scratch.txt` carry the full listing of the staging root, both installs included, at each wave boundary.

## `T1`, `R2` and the rest

`T1` and `R2` are recorded `skipped` on every run, for the reason #377's plan gives: both are answerable only from a Harness trace, and a session cannot read the transcript of a subagent it started. Nothing here claims either passed and nothing fails for lacking them. Every other criterion the corpus applies to a run of this kind — `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — is recorded `skipped`, naming `R1`, `A1`, `A2`, `N1`, `N2`, `C1`, `C2`, `O1` and `S1` as this evaluation's criteria.

Re-using #377's judge briefs as #383 requires means no judge was handed a measured figure. Several judges counted a control's character and word limits themselves and reported figures agreeing with the corpus table; the one place a count decides a verdict is `case-study-clean`, where both judges note the new subheading's length against the expectation's 36–39-character band. That is a declared limit of the frozen briefs against a product that now measures those limits by script, and it is named in the record.

## The revise-and-remeasure round, and the exit

The round available under the plan was spent on one run and two judges — the `case-study-clean` replay above — and not on a second post-change arm. Nothing a second arm would have measured differently was in reach: `A1` misses because the article anatomy turns a missing standfirst into a finding and repairing it authors prose, and `A2` misses because the claim account's assurance is written about claims received and says nothing about claims added. Neither is a question #383 settles, and neither could be answered here without inventing a requirement nobody has stated. No criterion was softened, no frozen plan, brief or fixture was edited, and every run made is kept.

**The post-change arm ships**, as the better of the two:

- it is the arm in which the three `editorial-377` control blemishes are covered and three of #386's four are gone;
- it is the arm in which every reply says what the run changed beyond the claims — the `channel` → `route` substitution that failed `post-opinion-en_GB-r2-b` in #377 is now reported in every run that makes it, as *settled on one name for the booking routes where the text had been alternating between two*;
- and it is no worse than the pre-change arm on `R1`, `N1` or `N2`, where the two are level or the post arm is ahead.

## What is measured and not fixed

- **The article anatomy's missing parts are repaired by authoring prose into somebody's finished text, and `R1` rejects it.** Twenty-four of twenty-four judgements of the four #362 drafts fail on that clause, in both arms, and it is what `A1` measures on those runs. A standfirst, section subheadings and a call to action get written where the text had none, the run grounds them in the anatomy rather than in a defect, and on a signed first-person column the new prose speaks about its author in the third person above her own byline. Filed as [#397](https://github.com/Kntnt/skills/issues/397).
- **The claim account's assurance is written about claims received, and a run that adds a claim reports that nothing happened to the claims.** Eight of eight post-change replies on the four inputs carry a sentence a judge finds false or misleading for that reason, and it is the whole of `A2`'s failure there. #383 settles how a changed claim and how everything else are reported, and says nothing about an added one. Filed as [#398](https://github.com/Kntnt/skills/issues/398).
- **`case-study-clean` misses `C1` in the post-change arm and passes in the pre-change replay**, on a subheading rewritten to describe its section. One run per arm cannot separate variance from a caused regression. Filed as [#399](https://github.com/Kntnt/skills/issues/399).
- **Three control accounts still leave a repaired defect unnamed** — `case-study-flawed`'s two subheadings, `column-flawed`'s headline, `article-flawed`'s standfirst/lead repetition — where the blemishes #377 recorded are now covered. The pattern #386 called inconsistent rather than systematic is narrower than it was and is not gone. Filed as [#400](https://github.com/Kntnt/skills/issues/400).
- **A correction subagent's scratch path is still shared between concurrent runs.** In `pre-column-sv-r2` the correction agent wrote its candidate to a fixed path in the session scratchpad, found it overwritten mid-task by a concurrent sibling working on the same input, took it for its own stale file and deleted it; it reported all of this and built its result from the candidate it had been handed directly, so nothing of the other repair reached the delivered text. This is the hazard `editorial-377/results.md` records for judges, now observed one level down, in a party the evaluator's turn cannot reach: the turn binds the run, and the run's fresh subagent receives only the correction brief. Every later wave was run at four or five concurrent runs on distinct inputs and no second collision was reported. Two judges also reported using and then deleting a path under `/tmp` despite being told to keep scratch in their own run directory. Filed as [#401](https://github.com/Kntnt/skills/issues/401).
- **Unslop was not measured.** It receives the same two procedural changes in its own vocabulary; [#385](https://github.com/Kntnt/skills/issues/385) measures it.
