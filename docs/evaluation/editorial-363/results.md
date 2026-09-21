# Results for #363: idiomatic quoted speech, and leaving a working quotation alone

Measured against [the frozen plan](plan.md) and the frozen criteria in [`fixtures/README.md`](fixtures/README.md). Nothing in either was edited after the first run.

It was written as the runs completed and is finished: every row of the frozen matrix ran, every delivered draft got the paired source-blind replay the matrix requires, and every run in the tree carries two blind judgements. What was not done is named in *What is and is not finished* rather than left out.

## What was run, and in what

### Three arms, not two

The plan freezes two arms. A third, `r`, is the one revise-and-remeasure round the exit criterion allows. **None of the three wordings ships**; *The decision* below says why, and the six surfaces on this branch are byte-identical to `install-baseline`, which is the `b` arm's product.

| Arm | Install | Product |
| --- | --- | --- |
| `b` | `install-baseline` | `main` at `8a37e57e`, unchanged — and the state this branch leaves the product in |
| `c` | `install-candidate` | baseline plus the first candidate wording, which this branch does not ship |
| `r` | `install-revised` | baseline plus the revised wording, which this branch does not ship |

The revised wording is recoverable: it is the tree at `19862dc2`, whose six surfaces hash to `install-revised` file for file, and `36e2b599` is the commit that returned them to the baseline.

The candidate wording asks the reader-of-this-language question and stops there. The revised wording names what the reader has to supply — a verb whose subject cannot perform it, a time or place adverbial whose event is missing, a reference the sentence never introduces — and adds the instruction to read a repair back the same way before it stands.

### The harness, and a declared difference from the plan

The plan says each invocation runs in "one fresh subagent per invocation, of type `kntnt-opus-high`". The `b` and `c` arms were run that way. **Most of the `r` arm was not, and seven of its rows were**, which makes that arm mixed; both halves are set out below, because an earlier draft of this file described the whole arm as sessions and that was not true of those seven.

Both Skills declare `kntnt.capabilities: "subagents"` and stop before writing where the harness cannot start one. The session that finished the `r` arm is itself a subagent of an orchestrating session, and a subagent of that harness has no agent-spawning tool at all: a Write run started that way stops on the unsatisfied capability before it resolves genre, technique or language. One such stop was produced and is kept in [`voided/`](voided/); it is a harness failure and not a run, and it is counted against nothing.

**Fifteen of the `r` arm's twenty-two runs therefore ran as a fresh top-level Claude Code session**, started from the shell as

`claude -p`, given the turn as its prompt, with the child-session environment variables unset so the session is not a child, with the working directory set to that run's `work/`, and with three flags in Claude Code's own spelling: `--model` set to `claude-opus-5`, `--effort` to `high` and `--permission-mode` to `bypassPermissions`. (Those are that tool's flags, not this collection's, and they are written out here rather than as a command line so that the record does not have to spell a foreign grammar in this collection's own.) The model and the deliberation level are the ones the plan names; what changes is that the seat is a session rather than a subagent, which is what lets the Skill start the checker and correction subagents its contract requires. The addendum's "the supported native harness for this family is Claude Code itself" is what this is. The turn text is unchanged between arms and is recorded in [`runs/write-turn.md`](runs/write-turn.md) and [`runs/redline-turn.md`](runs/redline-turn.md).

Those fifteen are all four `case-study` `Write` rows, their four paired replays, and the Redline rows `en-positive-r2`, `en-us-r1-r1`, `en-us-r1-r2`, `metonymy-sv-r1`, `metonymy-sv-r2`, `rhythm-en_GB-r1` and `rhythm-en_GB-r2`. The script that started them, its per-run log and its exit-status list are in this ticket's scratch directory rather than on the branch, so what the branch itself carries for them is the `started.txt` markers of the wave that begins at `22:08:49Z`.

**The `r` arm's other seven runs were not made that way**, and saying so is a correction to an earlier draft of this file. They are `sv-control-r1` and `r2`, `sv-artefact-r1` and `r2`, `ellipsis-sv-r1` and `r2`, and `en-positive-r1`. Their `started.txt` markers run from `17:30:54Z` to `17:31:37Z` in seven-second steps — the dispatch signature the `b` and `c` waves carry, where `b` steps from `16:01:58Z` to `16:03:04Z` the same way — four and a half hours before the session wave began, and none of them appears in the session script's status list or has a session log. They were dispatched as subagents, as the `b` and `c` arms were, and they were not among the ten attempts that were set aside and re-run.

What that costs is stated rather than argued away. For those seven rows the question [#394](https://github.com/Kntnt/skills/issues/394) names — whether Redline's correction round got the fresh seat its step 7 requires — is as open as it is for the attempts under [`voided/`](voided/), and the branch carries nothing that settles it either way. It changes no criterion verdict below, because every criterion that decides this ticket turns on the `b` and the `c` arms, and because those seven rows returned their quoted sentence unchanged and unreported exactly as the eleven `r`-arm Redline rows in the other seat did. It does mean the `r` arm is not one seat, and no sentence here should be read as saying it is.

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

One claim in the plan and in the ticket's addendum is no longer true and is corrected here rather than acted on. Both say the mandatory Swedish control is byte-identical to `docs/evaluation/corpus/editorial-quality/controls/case-study-clean.md`. It was when the ticket was written, against the corpus at `6e531f5`. Commit `28f7e66b` then revised that control for the article anatomy, and `diff` now reports the two files differing in six places: the standfirst, the byline, an added section heading with its lead paragraph and a fuller attribution on the quotation, the median sentence split in two, one sentence joined to the next, and the closing link. What matters here is unchanged: both still carry *Den tiden skulle jag avsätta innan nästa hus börjar*, so the frozen input still poses the question the ticket asks. Neither file was edited.

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

The revise round did change the Swedish renderings, though less distinctly than an earlier draft of this paragraph claimed. That draft said the baseline produced the bare *X börjar* once and the candidate twice; the eight renderings tabled above show it once in all three arms — `b/case-study-sv-r1`'s *innan nästa hus börjar* — and nowhere in the candidate arm, whose `r1` kept *börjar* but gave it a subject that can perform it and whose other two runs reached for *drar i gång* and *kommer igång*. So on this measure the candidate arm had already left the construction behind, and the revise arm's three runs do the same. Two of the three supply something the source leaves open — *vi* in `r2`, *starten* in `r3` — which is the same move the candidate arm's `r1` made with *arbetet*, milder in both cases because *vi* is already the speaker's own word in the sentence before it. The judgements of those three drafts sit beside them in the run tree. What the arm cannot do is change the decision: `K-cost` ships the shorter wording wherever the candidate arm removes no miss the baseline reproduced, and the baseline arm reproduced none — it passed the translation control on both its runs and on both judges.

### One row added to the revise arm, and one deliberately not

The plan lets a row be added and none be removed. The `r` arm as the earlier sessions left it had no English Write row at all, which would have measured the Swedish half of an asymmetric hypothesis without the English half. **`case-study-en_US` was added, once.** It delivered, and its draft carries the source sentence verbatim.

**`case-study-en_GB` was not added**, and that is a stated choice rather than an omission. A second English locale would re-measure the same duty — that a writer does not improve a quotation it is copying rather than rendering — on a text the arm already covers at full candidate count in `en-positive`, `en-us-r1` and `rhythm-en_GB`, at the price of a run and its paired replay. One locale is enough to catch a gross regression in the writer's handling of English quoted speech; the preservation question proper is answered on the review side.

### The Redline rows: what came back

Mechanically, across **all three arms and every row**, the quoted sentence each frozen input carries came back inside the delivered artefact unchanged. No run in any arm expanded *before the next building starts*, *terminen drog i gång*, *expeditionen*, *before the winter* or *the depot*. The English preservation failure this ticket inherits from the GPT family therefore did not reproduce in the baseline arm, and neither wording caused it.

The two Swedish rows that are supposed to expose the miss came back the same way. `sv-control` returns *innan nästa hus börjar* and `sv-artefact` returns *innan nästa byggnad kommer i gång*, in `b`, in `c` and in `r`, and no run's reported findings name either sentence. The frozen negative control `ellipsis-sv` behaves the same way on the clause the fixture is about: *Sedan gick lagret över* comes back untouched in all five of its runs, and in no run does a reported finding name it, which `C-ellipsis` states is a fail — *silence is a fail* — and it fails equally in all three arms.

One run in that row is not silent about the quotation as a whole, and the distinction is worth keeping. `b/ellipsis-sv-r1` delivers with three unresolved findings, the first of which is against this very quotation: it names *pärmar* and says the body neither prepares the discovery nor picks it up. That is a finding about a noun the text drops, not about `gick lagret över`, so `C-ellipsis` — which asks for a reported finding *against it* — still fails in that run. But "untouched and unreported in every run", which an earlier draft of this file said, is not what the tree shows.

### What the blind judges said

Every artefact was read by two judges that saw it under an opaque id, in a directory carrying neither its arm nor any other run's, without this ticket, without the hypothesis and without each other. Where a criterion turns on a judgement it is theirs; where they split, both readings are recorded below and neither is treated as the answer.

**On the Swedish sentence this ticket is about, the judges do not agree with the ticket.** The fifty Redline runs carry a hundred judgements between them. In every one of the thirty covering `sv-control`, `sv-artefact` and `ellipsis-sv`, both judges answer that the quoted passage came back word for word and that a Swedish reader takes it **on one pass**. That answer covers the two sentences the frozen material treats as defects: *Den tiden skulle jag avsätta innan nästa hus börjar* in the mandatory Swedish control, and *Sedan gick lagret över* in `ellipsis-sv`, which `C-ellipsis` was written to catch. Judge A put it in as many words, in `b/sv-control-r1`: *"innan nästa hus börjar" is the ordinary Swedish shorthand for "innan arbetet i nästa hus börjar" — a metonymy the language uses of itself. Nothing has to be supplied from outside.* The same sentence appears in that judge's readings of all four other `sv-control` runs. (An earlier draft of this file also had that judge calling the smoother alternative *a preference, not an obstruction*; no judgement in the tree contains that phrase, and it is withdrawn.)

**In English the judges divide, and five judgements read the ticket's own way.** Of the hundred Redline judgements, ninety-five find every quoted passage taken on one pass. The five that do not are all judge A, all on *before the next building starts*, and they are in `b/case-study-en_GB-r1-paired`, `b/case-study-en_US-r1-paired`, `c/case-study-en_US-r1-paired`, `r/en-us-r1-r1` and `r/en-us-r1-r2` — two of the `b` arm's paired replays, one of the `c` arm's, and both `r`-arm runs of the row the ticket names. Judge A's flattest statement of it is in `b/case-study-en_US-r1-paired`:

> One pass: no. The reader stops at "before the next building starts" and has to supply the elided noun — in English a building does not start; its rollout, its trial or the work in it does.

An earlier draft of this file said instead that both judges class every English quotation as returned verbatim and read on one pass, and that `K-preserve-en`'s evidence was unanimous. The first half is right and the second is not: the quotation did come back verbatim in all ten English replays, which is what the criterion asks, but the judging behind it is split, and the split runs the ticket's way rather than against it.

**What the five say about reporting matters more than the count.** In one of the five the run itself names the obstacle: judge A writes of `r/en-us-r1-r1` that *the reply does report it, as finding 7, and reports it exactly*. In the other four it does not, and judge A says so each time — of `r/en-us-r1-r2`, that *its five outstanding findings concern the byline, the closing sentence, and three things the round itself created; this obstacle, which arrived with the text, goes unmentioned*. So the one run in any arm that reported this sentence as an unresolved obstacle is a revised-arm run, which is the point `K-preserve-en` returns to below.

**The same judge reads the same sentence both ways, under one brief.** Seventeen Redline runs replay a text carrying that sentence: the five `en-positive` runs, the five `en-us-r1` runs and the seven paired replays of English drafts. Judge A takes it on one pass in twelve of them — in `b/en-positive-r1`, *"before the next building starts" is ordinary English shorthand for the next building's rollout and reads without a stop* — and stops at it in the five named above. Judge B takes it on one pass in all seventeen. In Swedish the division runs the other way round the briefs: judging a Write draft that had changed *innan nästa hus börjar* to *innan arbetet i nästa hus börjar*, judge A writes that *a Swedish hus does not itself börja* and classes the checker's finding *Supported repair, with a cost*, while judging the source-blind replays the same judge reads the unchanged sentence as one-pass Swedish. The Redline brief carries an explicit warning that a figure a language uses itself reads on one pass however odd its literal parse, and the Write brief does not. Neither reading is an oracle; the division is the evidence, and it is the clearest single reason the measurement cannot separate the arms.

**Where the judges do find defects, they are other tickets' defects.** Across the Redline cases both judges fail rows for rewriting a clean text's headings to taste, for shipping a subheading the run's own re-review condemned, for an account that says nothing else moved when something did, and for a limiting sentence whose object moved — the shapes owned by [#383](https://github.com/Kntnt/skills/issues/383), [#389](https://github.com/Kntnt/skills/issues/389), [#390](https://github.com/Kntnt/skills/issues/390) and [#377](https://github.com/Kntnt/skills/issues/377). Those are recorded against those numbers and counted against nothing here, as the plan requires.

On the Write side `F1` fails widely, for small source-coverage slips unrelated to quoted speech, but not uniformly, and an earlier draft of this file overstated it as both judges failing every Swedish draft in both arms. Of the eight Swedish drafts, both judges fail `F1` on four — `b/case-study-sv-r2` and all three `c` runs — judge A alone fails `b/case-study-sv-r1` and `r/case-study-sv-r3`, and both judges pass `r/case-study-sv-r1` and `r/case-study-sv-r2`. `b/case-study-sv-r1/judgement-b.md` records `F1 — **pass**` in as many words. Of the seven English drafts, both judges fail four and pass three.


## Wall time

Median seconds from `started.txt` to `finished.txt`, per arm and per Skill, recomputed over every run in the tree. The `Write` column covers the fifteen `case-study-<language>-rN` runs; the `Redline` column covers the other fifty, the fifteen paired replays included. Where an arm has an even number of timed runs the median is the mean of the two middle ones.

| Arm | Write | Redline |
| --- | --- | --- |
| `b` | 1 187 s — 4 runs, all timed | 674 s — 11 runs, all timed |
| `c` | 1 185 s — 7 runs, 4 timed | 798 s — 21 runs, all timed |
| `r` | 1 284 s — 4 runs, all timed | 739 s — 18 runs, 16 timed |

Five runs have no closing timestamp and are the ones the counts above leave out, named rather than dropped silently: the `c` arm's `case-study-en_GB-r1`, `case-study-sv-r2` and `case-study-sv-r3`, and the `r` arm's `sv-control-r1` and `ellipsis-sv-r1`. The session that made each was stopped by an account limit between the run and the marker. Their artefacts are complete and they count for every quality criterion; only their wall time is unavailable, and it is left unavailable rather than estimated.

An earlier draft of this table reported the three `Redline` medians as 735 s, 828 s and 703 s over eight, fourteen and thirteen runs, and left the `r` arm's `Write` median unstated. Those figures were taken while the paired replays were still landing and were never remeasured; the numbers above are what the committed markers give.

**These numbers do not compare across arms and are not evidence about the wordings.** Four separate reasons, each sufficient on its own. The `b` and `c` arms ran a few runs at a time in a subagent seat, and so did seven of the `r` arm's rows, while the rest of that arm ran ten to fourteen fresh sessions at once on one machine, so those figures measure contention more than anything else. The `r` arm is therefore not even one seat internally. Five runs are untimed, as above. And the case mix differs run to run. The figure that does mean something is the one this ticket can control, and it is in the cost table above: **neither wording adds a seat**, so neither adds a run's worth of latency to any pass.

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
| `c/case-study-sv-r3` | *innan nästa hus kommer igång* | one pass, intact | one pass, intact, on one qualification — Q1's *och* for the source's semicolon *softens her emphasis a shade* |

| `r/case-study-sv-r1` | *innan nästa hus kommer i gång* | one pass, intact | one pass, intact |
| `r/case-study-sv-r2` | *innan vi börjar i nästa hus* | *Almost one pass* on Q1 — *a recoverable half-beat inside the sentence, not a stop that breaks the reading* | **Not one pass** on Q1 — *the Swedish reader stops at* **Kategorierna**, *a reference the article never introduces* |
| `r/case-study-sv-r3` | *innan starten i nästa hus* | one pass, intact | one pass, intact |

Both baseline runs pass on both judges. The candidate arm fails, and it fails on the one run where the change visibly did something: `c/case-study-sv-r1` is the draft the judges record as having had a translation finding raised against the quotation and repaired — both read the checker reports in its `evidence/`, judge A classing the repair a *supported repair, with a cost* and judge B a *disputed caution, accepted* — and the repair wrote *arbetet* — the work — into a sentence the source leaves open. No other Swedish draft in either arm is recorded with one. Both judges name that as the cost, and the body of this ticket forbids exactly it: *Om faktisk kontext inte räcker ska Redline rapportera hindret och bevara osäkerheten, inte hitta på en händelse*. The candidate wording's only measured effect on this control was to cause one.

**The revise round did not repair the criterion either.** Its three Swedish drafts all avoid the bare *X börjar*, which the candidate arm's did not, and two of the three pass on both judges. The third fails: judge B reads the first of Maya Lind's quotations as stopping a Swedish reader at the definite *Kategorierna*, which the article never introduces. That is the same defect class the criterion is about — a word the reader has to supply — moved from one of her quotations to another. Two of three passing is what the candidate arm managed too. The revise round changed which sentence carried the fault; it did not remove it.

### `K-repair-sv` — Swedish source-blind repair

**Not reproduced as a defect in this family, in any arm.**

Both frozen Swedish inputs were replayed in all three arms — five replays of each. In every one, the quotation came back word for word, and no run's reported findings named it. Read against the criterion's own disjunction that is neither branch: the runs neither repaired the quotation nor reported an obstacle in it. What decides whether that is a miss is whether there is an obstacle, and on that both judges, in all twenty judgements of those ten runs, answer that a Swedish reader takes the passage on one pass. On the evidence this measurement produced, there is nothing here for the review to have found, and the criterion has nothing to separate the arms with.

The clause *a change the run's own reported findings do not name is a fail* does bite, repeatedly — but on headings, bridges and claim accounts rather than on quoted speech, and those are the shapes [#383](https://github.com/Kntnt/skills/issues/383), [#389](https://github.com/Kntnt/skills/issues/389) and [#377](https://github.com/Kntnt/skills/issues/377) own. They are recorded there and counted nowhere here.

### `K-preserve-en` — English and contrast preservation

**Pass, in every arm, including the baseline.**

For `en-positive`, `en-us-r1`, `metonymy-sv` and `rhythm-en_GB`, every run of every arm returned the working quotation unchanged, and every judge confirms the wording word for word. No run expanded *before the next building starts*, *terminen drog i gång*, *expeditionen*, *before the winter* or *the depot*. `C-metonymy` and `C-rhythm` pass in all three arms.

**The reading behind that pass is not unanimous, and an earlier draft of this section said it was.** On `en-positive`, `metonymy-sv` and `rhythm-en_GB` both judges take every quoted passage on one pass in every run. On `en-us-r1` judge A does so in the three `b`- and `c`-arm runs and stops at *before the next building starts* in both `r`-arm runs; judge A also stops at it in three paired replays of English drafts. *What the blind judges said* above lists all five and quotes them. The criterion is met either way — it asks that the working quotation come back unchanged or that a reported finding name a concrete obstacle, and the wording came back unchanged in all ten English replays — but it is met over a split instrument, not a unanimous one.

**The English failure this ticket inherits therefore did not reproduce in this family at all.** The baseline arm — the product with no change — preserves it. There was no English miss for either wording to fix, and neither wording changed an English quotation.

**One revised run did fire at the working English sentence, and stopped short of changing it.** `r/en-us-r1-r1` reports, among its unresolved findings:

> **"I would set that time aside before the next building starts."** The reader has to supply what it is that the building starts. It sits inside Lind's quoted speech, and the surrounding text does not settle it in her words, so correcting it would put words in her mouth.

It is the only run in any arm that says this, and it is a revised-arm run. The criterion is met — the quotation came back unchanged, and where a run does report a finding the criterion asks that the finding name a concrete obstacle, which this one does in the text's own words. But the ticket's own position is that *before the next building starts* **works** in the full English account and that there is no concrete English obstacle there. Read against that, this is the over-firing direction the hypothesis predicted would not appear, showing up in the arm written to prevent it, one step short of the change that would have failed the criterion. What kept the text intact was not the new test but the older rule that a repair inside quotation marks puts words in the speaker's mouth — which is the rule the [load-chain review](reviews/load-chain-review.md) says the chain does not reliably reach.

`C-ellipsis` is the one fixture criterion that fails, and it fails identically in all three arms: *Sedan gick lagret över* comes back untouched with no reported finding against it, which the fixture states is a miss. The row has five runs — one in `b`, two in `c`, two in `r` — and in all ten judgements of them both judges read that passage as one-pass Swedish too. (`b/ellipsis-sv-r1` does report an unresolved finding against a different part of the quotation, as *The Redline rows* above records; the fixture asks for one against `gick lagret över`, so the row still fails.) The fixture and the judges disagree, the fixture was frozen first and is not edited, and what the disagreement rules out is using this row to separate the arms.

### `K-separate` — claims judged separately from idiom

**Pass.** No fixed replacement sentence, no general metonymy ban and no widened source duty for Redline was introduced by either wording; the [load-chain review](reviews/load-chain-review.md) checked the same question independently and agrees on the metonymy point. Claims, attribution, the customer's reservations, chronology and metadata were judged by the two judges separately from idiom, and that is where most of the failures are — every one of them belonging to another ticket.

### `K-chain` — chain and transport

**Pass, on every Redline run in every arm.** All fifty run directories carry the mechanical pass's private input and its separate complete result in `evidence/`, and in all fifty the delivered artefact is byte-identical — not merely equal after stripping whitespace — to that result. Both branches are exercised: the mechanical pass returns the text unchanged in 37 runs and changed in 13.

**Twenty-one of the fifty name those two files differently from the turn template, and an earlier draft of this section did not say so.** The frozen template in [`runs/redline-turn.md`](runs/redline-turn.md) asks for `mechanical-pass-input.md` and `mechanical-pass-output.md`; twenty-nine runs used those names, twelve used `proofread-input.md`/`proofread-output.md` and nine used `proofread-private-input.md`/`proofread-private-output.md`. The files are present and complete in every case, so what the criterion asks about the transport is satisfied; the deviation is from an evaluator instruction, it is the run's naming rather than the Skill's behaviour, and it is recorded here rather than tidied by renaming the artefacts.

**The Correction Budget is the default in all fifty runs, and 41 of the fifty replies say so.** No invocation carries `--max`, which is what settles it. Of the 41 that mention the budget, 39 give its value as the existing default of one round and two mention it without a value; nine replies do not mention it at all. An earlier draft of this section said every run reports it, which is not what the replies show.

The three staged installs verify byte-identical to their pre-run inventories — 84 files each, no mismatch — so no run wrote into the product it was measuring.

**`T1` and `R2` are `skipped`**, with the reason the addendum gives: a subagent's transcript is not readable from the session that started it, and the fifteen `r`-arm runs made as headless `claude -p` sessions have no transcript that is an artefact here either. Nothing is claimed for them and nothing is failed for lacking them; the loading question is carried by [`reviews/load-chain-review.md`](reviews/load-chain-review.md) instead, which is what [#388](https://github.com/Kntnt/skills/issues/388) exists to make unnecessary.

### `K-cost` — cost against measured benefit

**The rule decides this ticket.** It reads: *a wording that adds reading ships only where the candidate arm removes a miss the baseline arm reproduced in at least two runs; otherwise the shorter wording ships.*

The candidate arm removes no miss. There was none to remove: the baseline arm passes `K-translate` on both its runs, preserves every English and contrast quotation, and its Swedish source-blind replays are judged one-pass by both judges. What the candidate arm did instead was fail `K-translate` — the criterion the wording was written for — by causing a referent to be written into a quotation.

So the shorter wording ships, and the shortest is the one that adds nothing.

## The decision

**Nothing ships. The product goes back to the baseline wording, which is `main` as it stood at `8a37e57e`.**

Three independent things point the same way, and any one of them would be enough.

**`K-cost`.** The candidate arm removes no miss the baseline reproduced, so the rule says the shorter wording ships. The baseline wording is the shortest there is.

**`K-translate`.** The candidate wording did not merely fail to help. Its one visible effect on the translation control was a draft that wrote a referent into a quotation the source leaves open, which the body of this ticket names as a failure mode in its own words. A wording whose measured effect on its own criterion is negative does not ship on the argument that it might help elsewhere.

**The independent load-chain review.** [`reviews/load-chain-review.md`](reviews/load-chain-review.md) was written by a reader that saw the diff and the whole chain around it and was deliberately kept from these numbers. It ends by answering its own question — *Would I ship this wording as it stands? No.* — on three must-fixes: that the chain can now drive a source-blind review into repairing wording inside quotation marks that `languages/sv.md` says the marks vouch for, while neither the reviewer nor the repairer is allowed to load the rule they would be breaking; that `case-study.review.md` dropped the word *merely* from *not protected merely by quotation marks* and so turned a narrow disclaimer into a general one, in the genre made of customer speech; and that `quotations.md` says *a figure of the source* where it means a figure of the source **language**, so the rule reaches a figure the speaker coined. That last one is the same defect the measurement found from the other side: it is what a writer follows when it writes *arbetet* into Maya Lind's sentence.

Fixing those three would be a second revise-and-remeasure round, and the exit criterion allows one. The `r` arm is that one.

### What this does not decide

**It does not decide that the ticket's premise is wrong.** Thomas's reading — that *innan nästa hus börjar* is a defect in professional Swedish, and that being able to work the meaning out is not the standard — is a judgement about Swedish prose, and this measurement cannot overturn it. What the measurement establishes is narrower and it is about the instrument: with the criteria frozen before the runs and the judging blind, **this provider family does not reproduce either failure**, so no candidate wording could have been shown to remove one. That is a fact about what can be measured here, not a verdict on the defect.

**It does not clear the GPT-family failures.** They stay failed. The protocol forbids a Claude session from driving a Codex harness, so they were not retested, and a retest is Thomas's own step.

**It does not settle what a next attempt should do.** The remaining miss is filed as [#393](https://github.com/Kntnt/skills/issues/393), and the first thing that ticket needs is not another wording: it is a way to tell whether the defect is there at all. Three of this ticket's six criteria turned out to have nothing to measure.

### What is kept

The plan, the fixtures, the judge briefs, the turn templates, the whole run tree with its judgements, this file, the load-chain review, the records, and [ADR-0212](../../adr/0212-a-quotation-is-read-in-the-language-it-is-written-in.md), which records the decision not to ship and why, so that the next author does not spend the same wording again. The three contrast fixtures in particular outlive this ticket: they are frozen, they have independent criteria, and `C-ellipsis` is now a documented disagreement between a fixture and two blind readers, which is worth more to the next attempt than a passing row would have been.

## What was voided, and why

**Ten `r`-arm attempts made in a subagent seat are preserved and count for nothing.** They are under [`voided/`](voided/), with a README saying what each one is. The reason is [#394](https://github.com/Kntnt/skills/issues/394): a subagent of this harness has no agent-spawning tool, Write's step 1 correctly stopped a run on the unsatisfied `subagents` capability, and Redline runs in the same seat ran to completion without ever checking. Two of those attempts wrote into a run directory a session-harness run was also using, so provenance could not be established for them either. They are the two Write attempts under [`voided/subagent-seat/`](voided/subagent-seat/): their `finished.txt` markers read `22:23:18Z` and `22:10:31Z`, while the session runs in `runs/r/case-study-sv-r1` and `runs/r/case-study-sv-r3` had started at `22:08:49Z` in those same directories. Where a run's provenance could not be established it was treated as not completed and re-run, which is what the ticket's own instruction says to do. The seven voided Redline attempts are not in that position: they all finished by `22:07:05Z`, before any session run started.

Nothing in the `b` or `c` arms is affected: those were made by an earlier session whose subagents could start checkers, as the two source-check reports in every one of their eleven Write run directories show — laid out as two directories under `evidence/` in seven of them, and as two reports inside one directory in the other four.

## What is and is not finished

Stated by name, because a run tree that does not say what is missing reads later as one that is complete.

- **The paired source-blind replays are done.** The frozen matrix requires one per delivered Write draft, and no session before this one had run any; all fifteen were run here — four in the `b` arm, seven in `c`, four in `r` — and every one of them returns the draft's own rendering of the quotation unchanged. That includes the baseline arm's replay of its own Swedish draft, which returns *innan nästa hus börjar* untouched: the pipeline reproducing this ticket's Swedish case end to end and leaving it alone. Both judges take the rendering on one pass in twelve of the fifteen; in `b/case-study-en_GB-r1-paired`, `b/case-study-en_US-r1-paired` and `c/case-study-en_US-r1-paired` judge A stops at the English *before the next building starts* while judge B does not, which *What the blind judges said* sets out.
- **Judging.** Every run in the tree carries two blind judgements beside it, as `judgement-a.md` and `judgement-b.md`; one run carries a third, for the reason its `judgement-c.note.md` gives. A run directory without both files has not been judged, and nothing about it is claimed here.
- **`T1` and `R2` are `skipped` on every row**, for the reason above, and are [#388](https://github.com/Kntnt/skills/issues/388)'s business.
- **The GPT-family failures were not retested**, by the protocol's rule, and stay failed.

None of these changes the decision. `K-cost` turns on whether the candidate arm removed a miss the baseline arm reproduced, and the baseline arm's rows — every one of them complete, judged and passing on quoted speech — settle that it reproduced none.

## Verification

The four checks in `CONTRIBUTING.md` §5 pass on this branch with the product back at the baseline wording: `ruff check`, `ruff format --check`, `mypy` over the twenty named scripts and `tests`, and **2 095 tests**, zero failures. The addendum says 1 888; the number has moved with `main` since, and the figure here is what the branch reports today.

Three of those tests pin exact sentences the work here was most likely to rewrite — `test_every_editorial_pass_reads_past_a_code_sample` and `test_every_correction_brief_preserves_code_beside_quotations` inside Redline's step 6 and every correction brief, and `test_every_editorial_manpage_says_a_code_sample_is_quoted` in each `help.md`. All three pass, because the surfaces they pin are back at the wording they were written against. The four tests the earlier builder added pinned sentences that no longer exist and were removed with them.

One test caught a defect in this file rather than in the product, and is worth naming because it is the kind a writer trips over: `test_no_valued_flag_of_the_collections_grammar_is_written_with_a_space` failed on the harness description above, where Claude Code's `--model` flag had been written with its value after a space rather than after an `=`. (Naming the offending text here would fail the same test a second time, which is why this sentence describes it instead of quoting it.) The flag is Claude Code's, not this collection's, but `docs/research/` is the only place the rule exempts a foreign tool's spelling. The command is now described by naming its flags and their values separately, which states the same fact without spelling a foreign grammar in this collection's own.

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
