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

```
claude -p --model claude-opus-5 --effort high --permission-mode bypassPermissions "<the turn>"
```

with the child-session environment variables unset so the session is not a child, and with the working directory set to that run's `work/`. The model and the deliberation level are the ones the plan names; what changes is that the seat is a session rather than a subagent, which is what lets the Skill start the checker and correction subagents its contract requires. The addendum's "the supported native harness for this family is Claude Code itself" is what this is. The turn text is unchanged between arms and is recorded in [`runs/write-turn.md`](runs/write-turn.md) and [`runs/redline-turn.md`](runs/redline-turn.md).

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

Every Swedish Write row in both arms delivered a draft; none stopped. Only `c/case-study-sv-r1` writes the activity out, and it does so without being told to. All six English Write rows in the two arms carry the source sentence verbatim inside its quotation marks.

### The Redline rows: what came back

Mechanically, across **all three arms and every row**, the quoted sentence each frozen input carries came back inside the delivered artefact unchanged. No run in any arm expanded *before the next building starts*, *terminen drog i gång*, *expeditionen*, *before the winter* or *the depot*. The English preservation failure this ticket inherits from the GPT family therefore did not reproduce in the baseline arm, and neither wording caused it.

The two Swedish rows that are supposed to expose the miss came back the same way. `sv-control` returns *innan nästa hus börjar* and `sv-artefact` returns *innan nästa byggnad kommer i gång*, in `b`, in `c` and in `r`, and no run's reported findings name either sentence. The frozen negative control `ellipsis-sv` behaves identically: *Sedan gick lagret över* comes back untouched and unreported in every run of every arm, which `C-ellipsis` states is a fail — *silence is a fail* — and it fails equally in all three.

### What the blind judges said

Every artefact was read by two judges that saw it under an opaque id, in a directory carrying neither its arm nor any other run's, without this ticket, without the hypothesis and without each other. Where a criterion turns on a judgement it is theirs; where they split, both readings are recorded below and neither is treated as the answer.

**On the sentence this ticket is about, the judges do not agree with the ticket.** Across every Redline case judged so far — `sv-control`, `sv-artefact`, `en-positive`, `en-us-r1` and the three fixtures, in all three arms — both judges answer that every quoted passage came back word for word and that a reader of that text's language takes it **on one pass**. That answer includes the two sentences the frozen material treats as defects: *Den tiden skulle jag avsätta innan nästa hus börjar* in the mandatory Swedish control, and *Sedan gick lagret över* in `ellipsis-sv`, which `C-ellipsis` was written to catch. One judge put it in as many words: *innan nästa hus börjar is the ordinary Swedish shorthand for innan arbetet i nästa hus börjar — a metonymy the language uses of itself*, and called the smoother alternative *a preference, not an obstruction*.

The same judges do not find the English defect either. No run in any arm expanded *before the next building starts*, and both judges class every English quotation as returned verbatim and read on one pass.

**One judge divided against itself, and it is worth recording.** Judging the source-blind replays, judge A reads *innan nästa hus börjar* as one-pass Swedish. Judging a Write draft that had changed it to *innan arbetet i nästa hus börjar*, the same judge writes *a Swedish hus does not börja* and calls the checker's finding against it real. The two readings are made under two briefs, and the Redline brief carries an explicit warning that a figure a language uses itself reads on one pass however odd its literal parse. Neither reading is an oracle; the split is the evidence.

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

Pending.

## Findings that belong to another ticket

Pending.
