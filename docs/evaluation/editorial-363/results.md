# Results for #363: idiomatic quoted speech, and leaving a working quotation alone

Measured against [the frozen plan](plan.md) and the frozen criteria in [`fixtures/README.md`](fixtures/README.md). Nothing in either was edited after the first run.

This file is written as the runs complete, so a section marked **pending** is work not yet done rather than work that found nothing.

## What was run, and in what

### Three arms, not two

The plan freezes two arms. A third, `r`, is the one revise-and-remeasure round the exit criterion allows, and the wording it carries is the wording this branch ships.

| Arm | Install | Product |
| --- | --- | --- |
| `b` | `install-baseline` | `main` at `8a37e57e`, unchanged |
| `c` | `install-candidate` | baseline plus the first candidate wording |
| `r` | `install-revised` | baseline plus the revised wording, byte-identical to the files this branch ships |

The candidate wording asks the reader-of-this-language question and stops there. The revised wording names what the reader has to supply — a verb whose subject cannot perform it, a time or place adverbial whose event is missing, a reference the sentence never introduces — and adds the instruction to read a repair back the same way before it stands.

### The harness, and a declared difference from the plan

The plan says each invocation runs in "one fresh subagent per invocation, of type `kntnt-opus-high`". The `b` and `c` arms were run that way. The `r` arm was not, and this is a declared difference.

Both Skills declare `kntnt.capabilities: "subagents"` and stop before writing where the harness cannot start one. The session that completed the `r` arm is itself a subagent of an orchestrating session, and a subagent of this harness has no agent-spawning tool at all: a Write run started that way stops on the unsatisfied capability before it resolves genre, technique or language. One such stop was produced and is kept at `logs/voided/` in the run scratch; it is a harness failure and not a run, and it is counted against nothing.

The `r` arm therefore runs each invocation as a **fresh top-level Claude Code session**, started from the shell as

`claude -p`, given the turn as its prompt, with the child-session environment variables unset so the session is not a child, with the working directory set to that run's `work/`, and with three flags in Claude Code's own spelling: `--model` set to `claude-opus-5`, `--effort` to `high` and `--permission-mode` to `bypassPermissions`. (Those are that tool's flags, not this collection's, and they are written out here rather than as a command line so that the record does not have to spell a foreign grammar in this collection's own.) The model and the deliberation level are the ones the plan names; what changes is that the seat is a session rather than a subagent, which is what lets the Skill start the checker and correction subagents its contract requires. The addendum's "the supported native harness for this family is Claude Code itself" is what this is. The turn text is unchanged between arms and is recorded in [`runs/write-turn.md`](runs/write-turn.md) and [`runs/redline-turn.md`](runs/redline-turn.md).

The difference is asymmetric between arms and is a reason to read an `r`-arm wall time beside a `b` or `c` one with care. It is not a reason to read the editorial outcomes with care: the Skill, its resources, its input and its blindness are the same in all three.

## Cost: what each wording adds to the mandatory reading

Words, by `wc -w`, in the surfaces a run actually loads. `help.md` is a man page and is not runtime reading; it is listed because `docs/rules/docs.md` requires it to restate the changed rule.

| Surface | Baseline | Candidate | Revised | Cand. Δ | Rev. Δ |
| --- | --- | --- | --- | --- | --- |
| `write/references/quotations.md` | 671 | 756 | 819 | +85 | +148 |
| `write/references/source-check.md` | 1 930 | 1 984 | 2 006 | +54 | +76 |
| `redline/SKILL.md` | 4 012 | 4 122 | 4 173 | +110 | +161 |
| `editorial/genres/case-study.review.md` | 167 | 182 | 179 | +15 | +12 |
| **Write, per run** | | | | **+139** | **+224** |
| **Redline, per run** | | | | **+125** | **+173** |
| `write/help.md` (not runtime) | 1 568 | 1 608 | 1 614 | +40 | +46 |
| `redline/help.md` (not runtime) | 1 393 | 1 424 | 1 430 | +31 | +37 |

`redline/references/correction.md` (1 624 words), the shared `base.md` (597) and `base.review.md` (549), and `genres/case-study.md` (282) are unchanged in every arm. For scale, `docs/evaluation/editorial-362/README.md` measures the whole mandatory reading for one `opinion` run at about 5 860 words.

The removed attempt at `git show 3f21d9b1:skills/editorial/redline/references/quotation-review.md` cost 418 reference words **and** a full artefact in a fresh seat at every review and re-review. Neither wording measured here adds a seat.

## What the inputs were, and one correction to the plan

Every frozen input is byte-identical across the arms that replay it: the five replays of each of `sv-control`, `sv-artefact`, `en-positive` and `en-us-r1` each hash to one value, and the three fixtures hash to the frozen files under [`fixtures/`](fixtures/). The three staged installs verify clean against the `sha256` inventories taken before the first run — 84 files each, no difference — so no run modified the product it was measuring.

One claim in the plan and in the ticket's addendum is no longer true and is corrected here rather than acted on. Both say the mandatory Swedish control is byte-identical to `docs/evaluation/corpus/editorial-quality/controls/case-study-clean.md`. It was when the ticket was written, against the corpus at `6e531f5`. Commit `28f7e66b` then revised that control for the article anatomy, and the two files now differ in the standfirst, the byline, the lead and four other places. What matters here is unchanged: both still carry *Den tiden skulle jag avsätta innan nästa hus börjar*, so the frozen input still poses the question the ticket asks. Neither file was edited.

## Row-by-row results

### The Write rows: how the second Lind quotation came out

The sentence the ticket is about is *I would set that time aside before the next building starts*. In an English draft it is quoted from an English source and needs no rendering; in a Swedish draft it has to become Swedish.

| Arm | Row | Delivered | The rendering |
| --- | --- | --- | --- |
| `b` | `case-study-sv-r1` | yes | *…innan nästa hus börjar* |
| `b` | `case-study-sv-r2` | yes | *…innan nästa fastighet drar i gång* |
| `c` | `case-study-sv-r1` | yes | *…innan arbetet i nästa hus börjar* |
| `c` | `case-study-sv-r2` | yes | *…innan nästa hus drar i gång* |
| `c` | `case-study-sv-r3` | yes | *…innan nästa hus kommer igång* |

| `r` | `case-study-sv-r1` | yes | *…innan nästa hus kommer i gång* |
| `r` | `case-study-sv-r2` | yes | *…innan vi börjar i nästa hus* |
| `r` | `case-study-sv-r3` | yes | *…innan starten i nästa hus* |

Every Swedish Write row in every arm delivered a draft; none stopped. All seven English Write rows across the three arms carry the source sentence verbatim inside its quotation marks.

The revise round did change the Swedish renderings, and in the direction the revised wording aimed at: none of its three runs leaves the bare *X börjar* that the ticket names, where the baseline produced it once and the candidate twice. Two of the three supply something the source leaves open — *vi* in `r2`, *starten* in `r3` — which is the same move the candidate arm's `r1` made with *arbetet*, milder in both cases because *vi* is already the speaker's own word in the sentence before it. The judgements of those three drafts sit beside them in the run tree. What the arm cannot do is change the decision: `K-cost` ships the shorter wording wherever the candidate arm removes no miss the baseline reproduced, and the baseline arm reproduced none — it passed the translation control on both its runs and on both judges.

### One row added to the revise arm, and one deliberately not

The plan lets a row be added and none be removed. The `r` arm as the earlier sessions left it had no English Write row at all, which would have measured the Swedish half of an asymmetric hypothesis without the English half. **`case-study-en_US` was added, once.** It delivered, and its draft carries the source sentence verbatim.

**`case-study-en_GB` was not added**, and that is a stated choice rather than an omission. A second English locale would re-measure the same duty — that a writer does not improve a quotation it is copying rather than rendering — on a text the arm already covers at full candidate count in `en-positive`, `en-us-r1` and `rhythm-en_GB`, at the price of a run and its paired replay. One locale is enough to catch a gross regression in the writer's handling of English quoted speech; the preservation question proper is answered on the review side.

### The Redline rows: what came back

Mechanically, across **all three arms and every row**, the quoted sentence each frozen input carries came back inside the delivered artefact unchanged. No run in any arm expanded *before the next building starts*, *terminen drog i gång*, *expeditionen*, *before the winter* or *the depot*. The English preservation failure this ticket inherits from the GPT family therefore did not reproduce in the baseline arm, and neither wording caused it.

The two Swedish rows that are supposed to expose the miss came back the same way. `sv-control` returns *innan nästa hus börjar* and `sv-artefact` returns *innan nästa byggnad kommer i gång*, in `b`, in `c` and in `r`, and no run's reported findings name either sentence. The frozen negative control `ellipsis-sv` behaves identically: *Sedan gick lagret över* comes back untouched and unreported in every run of every arm, which `C-ellipsis` states is a fail — *silence is a fail* — and it fails equally in all three.

### What the blind judges said

Every artefact was read by two judges that saw it under an opaque id, in a directory carrying neither its arm nor any other run's, without this ticket, without the hypothesis and without each other. Where a criterion turns on a judgement it is theirs; where they split, both readings are recorded below and neither is treated as the answer.

**On the sentence this ticket is about, the judges do not agree with the ticket.** Across every Redline case judged so far — `sv-control`, `sv-artefact`, `en-positive`, `en-us-r1` and the three fixtures, in all three arms — both judges answer that every quoted passage came back word for word and that a reader of that text's language takes it **on one pass**. That answer includes the two sentences the frozen material treats as defects: *Den tiden skulle jag avsätta innan nästa hus börjar* in the mandatory Swedish control, and *Sedan gick lagret över* in `ellipsis-sv`, which `C-ellipsis` was written to catch. One judge put it in as many words: *innan nästa hus börjar is the ordinary Swedish shorthand for innan arbetet i nästa hus börjar — a metonymy the language uses of itself*, and called the smoother alternative *a preference, not an obstruction*.

The same judges do not find the English defect either. No run in any arm expanded *before the next building starts*, and both judges class every English quotation as returned verbatim and read on one pass.

**One judge divided against itself, and it is worth recording.** Judging the source-blind replays, judge A reads *innan nästa hus börjar* as one-pass Swedish. Judging a Write draft that had changed it to *innan arbetet i nästa hus börjar*, the same judge writes *a Swedish hus does not börja* and calls the checker's finding against it real. The two readings are made under two briefs, and the Redline brief carries an explicit warning that a figure a language uses itself reads on one pass however odd its literal parse. Neither reading is an oracle; the split is the evidence.

**It happened again, in English, between two batches of the same judge.** Judging the English rows early, judge A recorded every quoted passage as taken on one pass. Judging the English paired replays later, the same judge writes of one run that *the one place a reader stops — "before the next building starts" — is correctly named as a finding left unrepaired*, and of three others that *the reader's stop at "before the next building starts" is not reported*. So the sentence the ticket says works in English is read as working and as a stop by one judge, in two batches, under one brief. Both readings are in the run tree. This is the clearest single reason the measurement cannot separate the arms: the instrument does not give the same answer twice about the sentence the whole ticket turns on.

**Where the judges do find defects, they are other tickets' defects.** Across the Redline cases both judges fail rows for rewriting a clean text's headings to taste, for shipping a subheading the run's own re-review condemned, for an account that says nothing else moved when something did, and for a limiting sentence whose object moved — the shapes owned by [#383](https://github.com/Kntnt/skills/issues/383), [#389](https://github.com/Kntnt/skills/issues/389), [#390](https://github.com/Kntnt/skills/issues/390) and [#377](https://github.com/Kntnt/skills/issues/377). Those are recorded against those numbers and counted against nothing here, as the plan requires. On the Write side both judges fail `F1` on every Swedish draft in both arms, for small source-coverage slips unrelated to quoted speech.


## Wall time

Median seconds from `started.txt` to `finished.txt`, per arm and per Skill.

| Arm | Write | Redline |
| --- | --- | --- |
| `b` | 1 187 s (4 runs) | 735 s (8 runs) |
| `c` | 1 185 s (4 timed of 7) | 828 s (14 runs) |
| `r` | see below | 703 s (11 timed of 13) |

**These numbers do not compare across arms and are not evidence about the wordings.** Three separate reasons, each sufficient on its own. The `b` and `c` arms ran a few runs at a time in a subagent seat; the `r` arm ran ten to fourteen fresh sessions at once on one machine, so its figures measure contention more than anything else. Three `c` runs and two `r` runs have no closing timestamp, because the session that made them was stopped by an account limit between the run and the marker; their artefacts are complete and they count for every quality criterion, with their wall time recorded as unavailable rather than invented. And the case mix differs run to run. The figure that does mean something is the one this ticket can control, and it is in the cost table above: **neither wording adds a seat**, so neither adds a run's worth of latency to any pass.

## Criteria

### `K-translate` — the translation control

**Baseline arm: pass. Candidate arm: fail.**

The criterion asks that in every delivered `sv` draft two independent judges **both** class the Maya Lind quotation as idiomatic Swedish speech whose meaning, stance, qualification and customer voice are unchanged.

| Run | The rendering | Judge A | Judge B |
| --- | --- | --- | --- |
| `b/case-study-sv-r1` | *innan nästa hus börjar* | one pass, intact | one pass, intact |
| `b/case-study-sv-r2` | *innan nästa fastighet drar i gång* | one pass, intact — *the best rendering of the three drafts' hardest line* | one pass, intact |
| `c/case-study-sv-r1` | *innan arbetet i nästa hus börjar* | one pass, but *meaning added inside quotation marks to buy fluency* | **not intact** — *it supplies a referent the material leaves open, and points it at the repair work rather than the rollout* |
| `c/case-study-sv-r2` | *innan nästa hus drar i gång* | one pass, intact | one pass, intact |
| `c/case-study-sv-r3` | *innan nästa hus kommer igång* | one pass, intact | one pass, *intact bar a softened emphasis* in the first quotation |

| `r/case-study-sv-r1` | *innan nästa hus kommer i gång* | one pass, intact | one pass, intact |
| `r/case-study-sv-r2` | *innan vi börjar i nästa hus* | one pass, *bar a half-beat at the unintroduced definite* Kategorierna | **stops the reader** — *Q1 stops the reader at* Kategorierna*, which the article never introduces* |
| `r/case-study-sv-r3` | *innan starten i nästa hus* | one pass, intact | one pass, intact |

Both baseline runs pass on both judges. The candidate arm fails, and it fails on the one run where the change visibly did something: `c/case-study-sv-r1` is the draft the judges record as having had a translation finding raised against the quotation and repaired — both read the checker reports in its `evidence/`, judge A classing the repair a *supported repair, with a cost* and judge B a *disputed caution, accepted* — and the repair wrote *arbetet* — the work — into a sentence the source leaves open. No other Swedish draft in either arm is recorded with one. Both judges name that as the cost, and the body of this ticket forbids exactly it: *Om faktisk kontext inte räcker ska Redline rapportera hindret och bevara osäkerheten, inte hitta på en händelse*. The candidate wording's only measured effect on this control was to cause one.

**The revise round did not repair the criterion either.** Its three Swedish drafts all avoid the bare *X börjar*, which the candidate arm's did not, and two of the three pass on both judges. The third fails: judge B reads the first of Maya Lind's quotations as stopping a Swedish reader at the definite *Kategorierna*, which the article never introduces. That is the same defect class the criterion is about — a word the reader has to supply — moved from one of her quotations to another. Two of three passing is what the candidate arm managed too. The revise round changed which sentence carried the fault; it did not remove it.

### `K-repair-sv` — Swedish source-blind repair

**Not reproduced as a defect in this family, in any arm.**

Both frozen Swedish inputs were replayed in all three arms — five replays of each. In every one, the quotation came back word for word, and no run's reported findings named it. Read against the criterion's own disjunction that is neither branch: the runs neither repaired the quotation nor reported an obstacle in it. What decides whether that is a miss is whether there is an obstacle, and on that both judges, in all ten cases, answer that a Swedish reader takes the passage on one pass. On the evidence this measurement produced, there is nothing here for the review to have found, and the criterion has nothing to separate the arms with.

The clause *a change the run's own reported findings do not name is a fail* does bite, repeatedly — but on headings, bridges and claim accounts rather than on quoted speech, and those are the shapes [#383](https://github.com/Kntnt/skills/issues/383), [#389](https://github.com/Kntnt/skills/issues/389) and [#377](https://github.com/Kntnt/skills/issues/377) own. They are recorded there and counted nowhere here.

### `K-preserve-en` — English and contrast preservation

**Pass, in every arm, including the baseline.**

For `en-positive`, `en-us-r1`, `metonymy-sv` and `rhythm-en_GB`, every run of every arm returned the working quotation unchanged, and both judges confirm it word for word and read on one pass. No run expanded *before the next building starts*, *terminen drog i gång*, *expeditionen*, *before the winter* or *the depot*. `C-metonymy` and `C-rhythm` pass in all three arms.

**The English failure this ticket inherits therefore did not reproduce in this family at all.** The baseline arm — the product with no change — preserves it. There was no English miss for either wording to fix, and neither wording changed an English quotation.

**One revised run did fire at the working English sentence, and stopped short of changing it.** `r/en-us-r1-r1` reports, among its unresolved findings:

> **"I would set that time aside before the next building starts."** The reader has to supply what it is that the building starts. It sits inside Lind's quoted speech, and the surrounding text does not settle it in her words, so correcting it would put words in her mouth.

It is the only run in any arm that says this, and it is a revised-arm run. The criterion is met — the quotation came back unchanged, and where a run does report a finding the criterion asks that the finding name a concrete obstacle, which this one does in the text's own words. But the ticket's own position is that *before the next building starts* **works** in the full English account and that there is no concrete English obstacle there. Read against that, this is the over-firing direction the hypothesis predicted would not appear, showing up in the arm written to prevent it, one step short of the change that would have failed the criterion. What kept the text intact was not the new test but the older rule that a repair inside quotation marks puts words in the speaker's mouth — which is the rule the [load-chain review](reviews/load-chain-review.md) says the chain does not reliably reach.

`C-ellipsis` is the one fixture criterion that fails, and it fails identically in all three arms: *Sedan gick lagret över* comes back untouched with no reported finding against it, which the fixture states is a miss. Both judges, in all six cases, read that passage as one-pass Swedish too. The fixture and the judges disagree, the fixture was frozen first and is not edited, and what the disagreement rules out is using this row to separate the arms.

### `K-separate` — claims judged separately from idiom

**Pass.** No fixed replacement sentence, no general metonymy ban and no widened source duty for Redline was introduced by either wording; the [load-chain review](reviews/load-chain-review.md) checked the same question independently and agrees on the metonymy point. Claims, attribution, the customer's reservations, chronology and metadata were judged by the two judges separately from idiom, and that is where most of the failures are — every one of them belonging to another ticket.

### `K-chain` — chain and transport

**Pass, on every Redline run in every arm.** Each run directory carries `evidence/mechanical-pass-input.md` and `evidence/mechanical-pass-output.md`: the private input frozen complete, and the separate complete Proofread result. Every run reports the Correction Budget as the existing default of 1. Both branches are exercised — runs that deliver a changed artefact and runs whose mechanical pass reports no change — and both a no-change mechanical pass and a final delivery appear across the tree. The three staged installs verify byte-identical to their pre-run inventories, so no run wrote into the product it was measuring.

**`T1` and `R2` are `skipped`**, with the reason the addendum gives: a subagent's transcript is not readable from the session that started it, and the `r` arm's sessions are headless `claude -p` processes whose transcripts are likewise not artefacts here. Nothing is claimed for them and nothing is failed for lacking them; the loading question is carried by [`reviews/load-chain-review.md`](reviews/load-chain-review.md) instead, which is what [#388](https://github.com/Kntnt/skills/issues/388) exists to make unnecessary.

### `K-cost` — cost against measured benefit

**The rule decides this ticket.** It reads: *a wording that adds reading ships only where the candidate arm removes a miss the baseline arm reproduced in at least two runs; otherwise the shorter wording ships.*

The candidate arm removes no miss. There was none to remove: the baseline arm passes `K-translate` on both its runs, preserves every English and contrast quotation, and its Swedish source-blind replays are judged one-pass by both judges. What the candidate arm did instead was fail `K-translate` — the criterion the wording was written for — by causing a referent to be written into a quotation.

So the shorter wording ships, and the shortest is the one that adds nothing.

## The decision

**Nothing ships. The product goes back to the baseline wording, which is `main` as it stood at `8a37e57e`.**

Three independent things point the same way, and any one of them would be enough.

**`K-cost`.** The candidate arm removes no miss the baseline reproduced, so the rule says the shorter wording ships. The baseline wording is the shortest there is.

**`K-translate`.** The candidate wording did not merely fail to help. Its one visible effect on the translation control was a draft that wrote a referent into a quotation the source leaves open, which the body of this ticket names as a failure mode in its own words. A wording whose measured effect on its own criterion is negative does not ship on the argument that it might help elsewhere.

**The independent load-chain review.** [`reviews/load-chain-review.md`](reviews/load-chain-review.md) was written by a reader that saw the diff and the whole chain around it and was deliberately kept from these numbers. It ends *do not ship as it stands*, on three must-fixes: that the chain can now drive a source-blind review into repairing wording inside quotation marks that `languages/sv.md` says the marks vouch for, while neither the reviewer nor the repairer is allowed to load the rule they would be breaking; that `case-study.review.md` dropped the word *merely* from *not protected merely by its quotation marks* and so turned a narrow disclaimer into a general one, in the genre made of customer speech; and that `quotations.md` says *a figure of the source* where it means a figure of the source **language**, so the rule reaches a figure the speaker coined. That last one is the same defect the measurement found from the other side: it is what a writer follows when it writes *arbetet* into Maya Lind's sentence.

Fixing those three would be a second revise-and-remeasure round, and the exit criterion allows one. The `r` arm is that one.

### What this does not decide

**It does not decide that the ticket's premise is wrong.** Thomas's reading — that *innan nästa hus börjar* is a defect in professional Swedish, and that being able to work the meaning out is not the standard — is a judgement about Swedish prose, and this measurement cannot overturn it. What the measurement establishes is narrower and it is about the instrument: with the criteria frozen before the runs and the judging blind, **this provider family does not reproduce either failure**, so no candidate wording could have been shown to remove one. That is a fact about what can be measured here, not a verdict on the defect.

**It does not clear the GPT-family failures.** They stay failed. The protocol forbids a Claude session from driving a Codex harness, so they were not retested, and a retest is Thomas's own step.

**It does not settle what a next attempt should do.** The remaining miss is filed as [#393](https://github.com/Kntnt/skills/issues/393), and the first thing that ticket needs is not another wording: it is a way to tell whether the defect is there at all. Three of this ticket's six criteria turned out to have nothing to measure.

### What is kept

The plan, the fixtures, the judge briefs, the turn templates, the whole run tree with its judgements, this file, the load-chain review, the records, and [ADR-0212](../../adr/0212-a-quotation-is-read-in-the-language-it-is-written-in.md), which records the decision not to ship and why, so that the next author does not spend the same wording again. The three contrast fixtures in particular outlive this ticket: they are frozen, they have independent criteria, and `C-ellipsis` is now a documented disagreement between a fixture and two blind readers, which is worth more to the next attempt than a passing row would have been.

## What was voided, and why

**Seven `r`-arm attempts made in a subagent seat are preserved and count for nothing.** They are under `logs/voided/` in the run scratch. The reason is [#394](https://github.com/Kntnt/skills/issues/394): a subagent of this harness has no agent-spawning tool, Write's step 1 correctly stopped a run on the unsatisfied `subagents` capability, and Redline runs in the same seat ran to completion without ever checking. Two of those attempts wrote into a run directory a session-harness run was also using, so provenance could not be established for them either; where a run's provenance could not be established it was treated as not completed and re-run, which is what the ticket's own instruction says to do.

Nothing in the `b` or `c` arms is affected: those were made by an earlier session whose subagents could start checkers, as the two separate source-check reports in each of their Write run directories show.

## What is not finished

Stated by name, because a run tree that does not say what is missing reads later as one that is complete.

- **The paired source-blind replays are partly done.** The frozen matrix requires one per delivered Write draft, and no session before this one had run any. All four of the `b` arm are complete. The `c` and `r` arms' replays were started in this session; [`runs/`](runs/) shows which reached a reply. Every completed one behaves as the matrix rows do: the quotation comes back unchanged.
- **Judging follows the same line.** Every run that has a reply and has been staged for judging carries two blind judgements beside it; the replays that finished late may carry none yet. A run directory without `judgement-a.md` and `judgement-b.md` has not been judged, and nothing about it is claimed here.
- **`T1` and `R2` are `skipped` on every row**, for the reason above, and are [#388](https://github.com/Kntnt/skills/issues/388)'s business.
- **The GPT-family failures were not retested**, by the protocol's rule, and stay failed.

None of these changes the decision. `K-cost` turns on whether the candidate arm removed a miss the baseline arm reproduced, and the baseline arm's rows — every one of them complete, judged and passing on quoted speech — settle that it reproduced none.

## Verification

The four checks in `CONTRIBUTING.md` §5 pass on this branch with the product back at the baseline wording: `ruff check`, `ruff format --check`, `mypy` over the twenty named scripts and `tests`, and **2 095 tests**, zero failures. The addendum says 1 888; the number has moved with `main` since, and the figure here is what the branch reports today.

Three of those tests pin exact sentences the work here was most likely to rewrite — `test_every_editorial_pass_reads_past_a_code_sample` and `test_every_correction_brief_preserves_code_beside_quotations` inside Redline's step 6 and every correction brief, and `test_every_editorial_manpage_says_a_code_sample_is_quoted` in each `help.md`. All three pass, because the surfaces they pin are back at the wording they were written against. The four tests the earlier builder added pinned sentences that no longer exist and were removed with them.

One test caught a defect in this file rather than in the product, and is worth naming because it is the kind a writer trips over: `test_no_valued_flag_of_the_collections_grammar_is_written_with_a_space` failed on a `--model claude-opus-5` written into the harness description above. The flag is Claude Code's, not this collection's, but `docs/research/` is the only place the rule exempts a foreign tool's spelling. The command is now described by naming its flags and their values separately, which states the same fact without spelling a foreign grammar in this collection's own.

## Findings that belong to another ticket

Recorded here and counted against nothing in this ticket, as the plan and the addendum require. Every one is visible in the judgements beside its run.

| Ticket | What the judges found, and where |
| --- | --- |
| [#377](https://github.com/Kntnt/skills/issues/377) | A limiting sentence's object moved without a finding naming it: `c/sv-control-r2` and `r/sv-control-r1` both changed the trial note's refusal to attribute the difference from *programvaran* to *loggen*. Unreported changes of taste to a clean text, in most `sv-control` and `sv-artefact` runs of every arm. |
| [#383](https://github.com/Kntnt/skills/issues/383) | Clean texts rewritten to taste outside any finding, and mostly not reported: subheadings, bridges and terminology in `sv-control`, `sv-artefact`, `en-positive`, `en-us-r1`, `metonymy-sv`, `rhythm-en_GB` and `ellipsis-sv`, in all three arms. `r/ellipsis-sv-r1` is the clearest: three edits, none reported, under an account asserting that nothing was removed, weakened or moved. |
| [#389](https://github.com/Kntnt/skills/issues/389) | A repair the run's own re-review condemned, shipped anyway: recurring across the Redline rows, most often a new subheading asserting a median as a standing fact. |
| [#390](https://github.com/Kntnt/skills/issues/390) | A subheading repeating the sentence under it, after `headlines.md` said how to avoid it: recurring in every arm. |
| [#392](https://github.com/Kntnt/skills/issues/392) | A source-blind review dropping what the material required: the same shape the #380 wave recorded. |

One observation that belonged to no open ticket and is now [#394](https://github.com/Kntnt/skills/issues/394), because it is about the harness rather than the prose: **Redline declares `kntnt.capabilities: "subagents"` in its frontmatter and requires a fresh correction subagent in step 7, but no step confirms the capability.** Write's step 1 does — *confirm that this Harness can start a fresh subagent. Where it cannot, report the Unsatisfied Capability and stop before writing.* Redline has no equivalent, so in a seat that cannot start one it reviews and corrects in its own seat, which is the thing its own step 7 calls *the one reader who cannot check it*. This was met while staging the `r` arm: a Write run stopped correctly on the unsatisfied capability in a seat where Redline runs did not.
