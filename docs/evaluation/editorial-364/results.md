# Results for #364: a bridge prepares a quotation rather than pre-says it

Measured against [the frozen plan](plan.md) and the criteria in it. Nothing in the plan or in the judge briefs was edited after the first run.

## What is and is not finished

*Kept true from the first commit onwards, so that a session picking this up after an interruption can see where it stands.*

- **Finished.** The plan, the matrix, the criteria and the two judge briefs, frozen and committed. The baseline (`b`) arm's seven Write runs, all delivered and each read by two judges — with one gap inside that: judgement A of `case-question-en_GB-r3` returned no `L1` section, so thirteen of the fourteen Write judgements carry an `L1` verdict and that row is a one-judge row on `L1` alone. The seven paired source-blind Redline runs, all delivered and each read by two judges, on the four things their brief asks; `G2` and `L1` are not among them and are `skipped` in that record with that reason. The before-and-after inventory. The two independent load-chain reviews under [`reviews/`](reviews/). This file, the two records and ADR-0214.
- **Not reached, and why.** The candidate arm, and with it `K-bridge` and `K-controls`, both of which are stated over the candidate arm's drafts. The baseline took [exit 1](plan.md#exit) — the fault does not reproduce — and where the baseline takes exit 1 the plan writes no candidate wording at all, so there is nothing for either criterion to be read against. This is the exit taken as written, not a criterion dropped. `K-chain` is met: it is stated over the affected load chain rather than over a diff, and the chain exists whether or not anything changed it. [`K-cost`](#k-cost) is met the same way and is measured rather than asserted: a zero word delta over a mandatory reading counted file by file.

## The harness and the seat

Provider family `claude`. Claude Code 2.1.278. Every run is a fresh top-level session started from the shell with `claude -p`, the turn as its prompt, the child-session environment variables unset, the working directory set to that run's `work/`, and Claude Code's own `--model`, `--effort` and `--permission-mode` flags set to `claude-opus-5`, `high` and `bypassPermissions`. The declared difference from the addendum's "fresh `claude-opus-5` subagent at high deliberation" is the seat: a subagent of this harness has no agent-spawning tool, and both Skills declare `kntnt.capabilities: "subagents"`, so a Write run started in a subagent stops on the unsatisfied capability and a Redline run completes without the fresh correction seat its contract requires ([#394](https://github.com/Kntnt/skills/issues/394)). The model and the deliberation level are the ones the addendum names.

Judges are fresh `kntnt-opus-high` subagents (`claude-opus-5`, high deliberation) with no history; they start nothing, so the seat question does not reach them. Each delivered artefact was read by two, blind to this plan, to the hypothesis, to the expected answer and to any model identity.

The GPT-family baseline this ticket inherits was measured under native Codex CLI 0.155.1 on `gpt-6-astra/high`. It is not reproduced here and is not retested: [the protocol](../protocol.md) forbids a Claude session from driving a Codex harness. That is the difference from the baseline, stated rather than estimated.

Corpus commit: `218e3be1`.

## What ran

All seven rows of the frozen matrix delivered a draft, and each delivered draft got its paired source-blind Redline run. The staged install is byte-identical before the first run and after the last — `runs/install-b-before.txt` beside `runs/install-b-after.txt` — every row's private scratch directory is empty or removed, and each `work/` holds only its one input file.

Four rows were dispatched more than once, for reasons that are not the ticket's. `case-question-en_GB-r3` and `case-study-en_US-r1` were dispatched twice, the first attempt of each killed in an `HTTP 529 Overloaded` window; `case-study-sv-r1` and `case-study-sv-r2` were dispatched three times each, the first two attempts of each dying on `API Error: 500`. None of those six attempts delivered anything or wrote `finished.txt`. Each was voided whole to [`voided/`](voided/) and the row was re-dispatched from a clean directory holding only `work/source.md`, whose bytes were re-verified against the frozen inventory before dispatch. Six voided attempts are kept there; none reached a judge. This is why those rows' timings sit in a later window than the other three.

The plan's re-run allowance — *A run that stops for a finding **unrelated to the bridge** is recorded as a stop with its reason and its wall time, is not counted against this ticket's criterion, and **that row may be re-run once**.* — is not what these re-dispatches were made under, and the two Swedish rows exceed it read as a count. That allowance governs a run that completed and stopped; a server-side kill produced no run, no delivered artefact and no judgement, so there was nothing to select between. Both are stated here rather than left to be reconstructed from the directory names.

| Row | Wall time, Write | Wall time, paired Redline |
| --- | --- | --- |
| `case-question-en_GB-r1` | 12m28s | 9m41s |
| `case-question-en_GB-r2` | 19m31s | 14m24s |
| `case-question-en_GB-r3` | 17m57s | 7m22s |
| `case-study-en_US-r1` | 13m32s | 10m00s |
| `case-study-en_US-r2` | 24m35s | 11m01s |
| `case-study-sv-r1` | 21m31s | 16m08s |
| `case-study-sv-r2` | 18m58s | 16m45s |

## The bridge classing

Every delivered draft, both judges, in the (a)/(b)/(c) classing the plan froze. A quotation standing with no bridge at all is its own answer and is counted separately.

| Row | Judge A | Judge B | Agreed? |
| --- | --- | --- | --- |
| `case-question-en_GB-r1` | (a) 0, (b) 2, (c) 0 | (a) 0, (b) 2, (c) 0 | yes |
| `case-question-en_GB-r2` | (a) 0, (b) 2, (c) 0 | (a) 0, (b) 2, (c) 0 | yes |
| `case-question-en_GB-r3` | (a) 0, (b) 2, (c) 0 | (a) 0, (b) 2, (c) 0 | yes |
| `case-study-en_US-r1` | (a) 1, (b) 0, (c) 2 | (a) 0, (b) 1, (c) 2 | **no** |
| `case-study-en_US-r2` | (a) 0, (b) 2, (c) 1 | (a) 0, (b) 2, (c) 1 | yes |
| `case-study-sv-r1` | (a) 0, (b) 0, (c) 2, unbridged 1 | (a) 0, (b) 0, (c) 2, unbridged 1 | yes |
| `case-study-sv-r2` | (a) 0, (b) 0, (c) 1, unbridged 2 | (a) 1, (b) 0, (c) 0, unbridged 2 | **no** |

Where the judges split, both classes stand and neither judge is an oracle, as the plan requires. The two splits are set out under [the classing is not stable](#the-classing-is-not-stable) below.

## The reproduction test, and the exit

The plan fixes the test before the runs: **the fault counts as reproduced when at least one baseline `case-question-en_GB` draft carries a class (a) bridge.**

Three runs, two judges each, six readings: **class (a) count zero in every one.** The fault does not reproduce.

The GPT-family draft this ticket was filed on introduced its closing quotation with

> Asked about choosing the system again and what to change, Vale's endorsement was specific to new jobs, with more time allowed before extending its use:

and the three Claude-family drafts of the same source wrote, over an identical quotation:

- `r1` — "Asked whether the same choice would be made again, Vale wrote:"
- `r2` — "Vale's verdict comes with a condition and a delay:"
- `r3` — "Asked whether the choice would be made again, and what would change, Vale answered:"

**The three are not alike, and the result should not be read as three clean bridges.** `r1` and `r3` give the occasion and the attribution and nothing else, and every second reading their four judges record **of the closing bridge** reaches back to the *narrative sentence or heading before* it rather than questioning what the clause itself does. (Three of their four second readings of the *opening* bridge do stay inside the clause: two test and reject an (a) reading of "what the team had to settle", and one tests and rejects a (c) reading of the email and the interviewer's identity. The fourth, judge B of `r3`, reaches back to the standfirst and rejects the (a) reading on the ground that "the standfirst is not the bridge".) Judge A of `r1` calls that wider reading "genuinely close" and still classes the clause (b), "because the definition fixes the bridge at the clause immediately preceding and that clause adds nothing of the answer". `r2` is the arguable one, and both its judges said so in terms. "Vale's verdict comes with a condition and a delay" previews the shape of the answer, and each judge set out the (a) reading before choosing (b):

- judge B — **"Class (b), chosen over a live (a) reading"**, with "*comes with a condition and a delay* is a structural preview, and it is the reason this one is arguable", and the rejected reading stated as "the bridge pre-announces both of the quotation's two moves, leaving the quotation to supply only their values";
- judge A — **"Class (b), with a second reading given"**, whose "**Second reading, toward (a)**" is that "the quotation's two moves are announced before they arrive and land as confirmation rather than as news".

Both chose (b) on the same ground: the substance — *for new jobs*, *another week*, and the reason for it — arrives only inside the quotation marks, and a bridge that announces a shape has not delivered a substance.

**A third reading of that same bridge, under the other brief, is (a).** The paired source-blind Redline judge B classed `en_GB-r2-paired` quotation 2 **(a) → (a)**, because, in that judge's words, "'comes with a condition and a delay' maps one-to-one onto the quotation's two sentences and is the bridge's own reading of them" — the same cross-brief disagreement this file records at [`case-study-en_US-r1`](#the-classing-is-not-stable), and recorded here for the same reason. The balance is the opposite one: there, two of the four readings call the bridge this ticket's defect; here, three of four call it (b).

**What the frozen test reads is the Write judges' classing**, which is what the plan names and what the judge brief asked for, and on it the count is zero across all six readings. The exit below therefore stands on the classing as given, with the confidence that classing actually carries: two clean bridges, and one that both judges of the row resolved to (b) after stating the reading that would have failed it.

**[Exit 1](plan.md#exit) is therefore taken as written.** No product file changes. The body's own rule is that a new general rule needs a demonstrated cause; the cause this ticket names is a class (a) bridge, and no Write judge recorded one in the row the test reads. [`K-cost`](#k-cost) settles the same way from the other end, and has no miss to point at either.

`skills/kntnt/library/references/editorial/genres/case-study.md` and `case-study.review.md` are byte-identical to `218e3be1`, as is everything else under `skills/` and `tests/`. This repeats what [#363](../editorial-363/results.md) found one day earlier about the two quotation failures it was filed on, by the same method and with the same outcome: the defect is real where it was observed, and this family does not produce it.

## What the measurement did find

Exit 1 closes the ticket. It does not make the run empty, and two findings in it are worth more than the non-reproduction.

### The pre-echo moved into the heading

In two of the three `case-question-en_GB` drafts the reader still meets the closing quotation as something already said — not in the bridge, but one step further up, in the section heading:

- `r2` — heading **"Vale would use the schedule again for new jobs"**, over the quotation "I would use it again for new jobs. I would allow another week to check the status names before adding the backlog."
- `r3` — heading **"Vale would allow an extra week for the status names"**, over the same quotation.

Both of `r3`'s judges reported this without being asked to, in these words. Judge A: "the redundancy is real and is the clearest editorial defect in the piece: the subheading in particular should not have pre-spent the quotation's own figure", and, of the same item, "Neither checker raised it … It is nonetheless the clearest weakness in the delivered text, and no part of the run caught it." Judge B: "the **section heading** *Vale would allow an extra week for the status names* states the quotation's second sentence in advance, and the preceding sentence states its first in documentary form — so the reader arrives at the quotation with both halves already in hand. That is the class-(a) hazard sitting one layer above the bridge", and later "heading and preceding sentence between them pre-delivering both halves of Vale's answer … was noticed by neither checker". Both still classed the bridge itself (b), correctly: the judge brief — frozen with the plan, and the only place in this evaluation where the term is defined — fixes a bridge as the narrative sentence or clause standing *immediately* before the quotation, and a heading two steps up is not that.

So the frozen definition is doing exactly what it was written to do, and the fault has moved to where it does not reach. The shipped review rule has the same reach: `case-study.review.md` says to read "bridges beside quotations and the standfirst beside the body's opening", and names no other pairing. This is not the subheading-repeats-its-first-sentence fault that [#390](https://github.com/Kntnt/skills/issues/390) already owns — in `r2` the heading does not repeat its first sentence, which is the bridge "Vale's verdict comes with a condition and a delay:"; it repeats the quotation two sentences down — so it is filed on its own number, [#396](https://github.com/Kntnt/skills/issues/396), rather than against #390.

**This is the line the two records draw too**, so that one finding is not charged to two tickets: a heading or a narrative sentence that pre-says a **quotation** standing further down is #396's, filed by this run; a display line that repeats the sentence directly under it, or a headline and standfirst restating each other, is #390's. Every `notes` entry in the Write record names one or the other on that test, on all seven rows. The Redline record names one or the other in the four rows where it charges a heading or a run-up against a ticket — `case-question-en_GB-r1-paired`, `-r2-paired`, `case-study-en_US-r1-paired` and `case-study-sv-r2-paired` — and names neither in the other three, which charge no such finding.

### The classing is not stable

The two Write-judge splits are worth reading, because between them they mark the edge the plan's (a)/(b) distinction was written to hold. The whole cross-brief picture follows them.

**`case-study-en_US-r1`, quotation 2.** Bridge: "Lind would plan the next building differently." Quotation: "We spent more time agreeing on the categories than entering the first reports. I would set that time aside before the next building starts." Judge A classed it **(a)** — the bridge delivers the judgement the quotation is there to deliver. Judge B classed it **(b)** — it names the subject, and a subject that recurs in the quotation is not by itself (a). The paired source-blind Redline judge B, reading the same text under the other brief, independently classed it **(a)** and recorded that the review neither found nor changed it; that pair's judge A classed it **(b)** on both sides. Two of the four readings call it the defect this ticket is about, in a positive-control row.

**`case-study-sv-r2`, quotation 3.** Judge A counted zero (a); judge B counted one, and named it as "Q3's heading" — that is, judge B took the heading as the bridge where judge A did not. The disagreement is about *where the bridge is*, not about what the text does, and both judges describe the same words. Both Redline judges of the paired run admitted the same heading as the bridge and classed it **(a)**, so three of the four readers of that draft read it as judge B did.

Neither Write-judge split falls in the `case-question-en_GB` row, so neither bears on the reproduction test. Both bear on whether the criterion would measure the fault if it were there, which is why they are recorded here rather than left in the run tree.

**Every reading of every delivered draft, across both briefs.** Each draft was read four times on its bridges — twice by its Write judges under [`runs/write-judge-brief.md`](runs/write-judge-brief.md), and twice more by its paired Redline judges under [`runs/redline-judge-brief.md`](runs/redline-judge-brief.md), who class each bridge as the input carries it before classing it as delivered. The two briefs put the classing to different readers on the same words. The table below lists **every bridge in the seven drafts that any of its four readers classed (a)**, together with the one bridge no reader classed (a) but whose whole run-up a reader did, so that no bridge classed (a) anywhere in the run tree is left unreconciled with the test above. It is not a list of every *mention* of an (a) reading: several further bridges — among them `en_GB-r1` Q1 and Q2, `en_US-r1` Q3 and `en_US-r2` Q3 — had an (a) reading of some clause stated and then rejected by a judge who classed the bridge otherwise, and those are read in the per-row entries of the two records rather than here:

| Draft, quotation | Write judge A | Write judge B | Redline judge A, as input | Redline judge B, as input |
| --- | --- | --- | --- | --- |
| `en_GB-r2` Q2 | (b) | (b) | (b) | **(a)** |
| `en_GB-r3` Q2 | (b) | (b) | (b), with the whole run-up called **(a)** | (b) |
| `en_US-r1` Q1 | (c) | (c) | (c) | **(a)** |
| `en_US-r1` Q2 | **(a)** | (b) | (b) | **(a)** |
| `sv-r1` Q1 | (c) | (c) | **(a)** | **(a)** |
| `sv-r2` Q3 | no bridge | **(a)** | **(a)** | **(a)** |

**Five of the six bridges in the table are classed (a) by at least one of their four readers, and the `case-question-en_GB` row is among them; the sixth, `en_GB-r3` Q2, draws its (a) only on a whole-run-up reading.** What varies between the two briefs is almost entirely *what counts as the bridge*: the Redline judges read the run-up as the input carries it and take in a whole preceding paragraph or a heading, where the Write judges hold to the brief's clause standing immediately before the quotation. At `sv-r1` Q1 both Write judges name the same whole-paragraph reading and reject it on that definition; at `sv-r2` Q3 the Write judges divide over exactly that question. Three places turn on something other than position: `en_GB-r2` Q2 and `en_US-r1` Q2, where the same clause is read two ways on its content, and `en_US-r1` Q1, where a bridge carrying both a clause that says what the quotation says and a fact the quotation lacks is classed by whichever of the two the reader lets govern — judge A of the Redline pair writes that "taken whole, the bridge adds matter of its own, so (c) is the class, with an (a) defect inside it", where judge B lets the (a) clause govern.

The remaining classings differ in four more places, none of them touching (a) and all of them the same question of position: `en_GB-r2` Q1, which one Redline judge reads (c) for the *by email* and *Benchline's case writer* the other three take as occasion and attribution; and `sv-r1` Q2, `sv-r2` Q1 and `sv-r2` Q2, where a Write judge records a quotation as standing with no bridge and a Redline judge classes the bare speech tag or the sentence before it. Every other bridge in the seven drafts drew the same class from all four readers.

**The frozen test is not restated over this table, and is not softened by it.** The plan fixes the test over the classing the Write judges give the Write draft, which is the measurement this ticket commissioned; on that classing the count is zero, and [the exit above](#the-reproduction-test-and-the-exit) stands. What the table adds is the confidence to attach to it: this criterion is measured by readers who do not agree on where a bridge begins, which is the second half of what [#396](https://github.com/Kntnt/skills/issues/396) is filed on.

## `K-redline`

Every delivered draft has its paired source-blind Redline run, judged on `R1` by two blind judges.

| Paired row | Judge A | Judge B |
| --- | --- | --- |
| `case-question-en_GB-r1-paired` | pass | pass |
| `case-question-en_GB-r2-paired` | pass, qualified | **fail** |
| `case-question-en_GB-r3-paired` | pass | pass |
| `case-study-en_US-r1-paired` | pass | pass |
| `case-study-en_US-r2-paired` | **fail** | pass, with blemishes |
| `case-study-sv-r1-paired` | pass | **fail** |
| `case-study-sv-r2-paired` | pass | pass |

Four rows pass on both judges; three split. Every failure named is a claim the review shipped or a change it did not report:

- `en_GB-r2-paired` — shipping the subheading "The summary measures no outcomes" that the sentence beneath it contradicts, and the companion clause that drops the "for new jobs" limit, both created by the round's own repair; four further changes unreported, one of them a claim move.
- `en_US-r2-paired` — putting "Median time to assignment fell by a day" in a heading over a section that refuses the inference, and leaving one further claim change neither named nor defended.
- `sv-r1-paired` — two things, which the record keeps apart. The two substantive losses, "i två av husen" from the lead and "Svale konfigurerade loggen" from the narrative, were **reported, and reported accurately**; judge B says so of both, and judge A weighs the disclosure as what carries the pass. What the closing line *Inga andra påståenden ändrades* denies is a different set: the heading narrowed to "Mediantiden till tilldelning", the call to action turned from a statement into an imperative, and the three normalised dashes — none of them named. Judge B's failure rests on the losses **and** on the false closing sentence, not on the losses being hidden.

These are the shapes [#377](https://github.com/Kntnt/skills/issues/377), [#383](https://github.com/Kntnt/skills/issues/383), [#389](https://github.com/Kntnt/skills/issues/389) and [#392](https://github.com/Kntnt/skills/issues/392) already own, and they are recorded against those numbers rather than filed again. #377 — keep limiting sentences, report every change to a claim — is the most cited of the four in the Redline record, and is named here for that reason.

A Redline repair passes no Write draft retroactively, and none is counted as one here.

**The output target and the cleanup** are read from the before-and-after inventory over every staged writable location, and are clean: the staged install unchanged, every scratch directory empty or removed, every `work/` holding one file.

**The closing mechanical pass** is judged from the preserved private input and output in each row's `evidence/` and their byte relation to the delivered artefact. In all seven rows `mechanical-pass-output.md` is byte-identical to `delivered.md`, so the mechanical pass is the last thing that touched the text in every run and nothing was edited after it. In three rows — `en_GB-r1-paired`, `en_GB-r3-paired`, `en_US-r1-paired` — it returned its input unchanged; in the other four it changed the text.

**Bridges across the Redline pairs.** These classes are the Redline judges', given to the same delivered drafts the Write judges classed, and the two sets differ; [the table above](#the-classing-is-not-stable) is where every difference touching class (a) is set against the reproduction test, so that a class (a) count of zero and three class (a) bridges in the inputs are not left standing beside each other unexplained. Three class (a) bridges in the inputs were repaired by the review: `sv-r1-paired` quotation 1 (a) → (c) and `sv-r2-paired` quotation 3 (a) → (b), both on both judges and the second reported in the reply, and `en_US-r1-paired` quotation 1 (a) → (c) on judge B, judge A reading that bridge (c) on both sides. Two class (a) bridges came back in class (a) and unfound, each on one judge:

- `en_US-r1-paired` quotation 2, *Lind would plan the next building differently.*, which the review did not touch at all — judge B: "This class (a) bridge was in the input and the run left it alone".
- `en_GB-r2-paired` quotation 2, which the review **did** change, in wording and not in class: *Vale's verdict comes with a condition and a delay:* came back as *Vale's verdict on the bench schedule comes with a condition and a delay:*. Judge B classes it (a) → (a), judge A (b) → (b); both record the added phrase as supplying nothing and as unreported. What the review did remove above it is the heading *Vale would use the schedule again for new jobs*, which both judges record as having pre-stated the quotation's first sentence and as no longer doing so — judge A logs the removal as difference #7 and the reply as not reporting it.

Every other bridge came back in the class it went in with, and no review moved a bridge into class (a).

## `K-chain`

Two fresh subagents read the whole chain a `case-study` run loads — from both `SKILL.md` files through what the shim resolves, the base contract, the genre and its review half, the anatomy and `headlines.md` — and answered one question: does the chain, as it stands, give a writer and a reviewer what they need to keep a quotation from being pre-said? Neither was handed the runs' results, and both read this evaluation's own output in the working tree anyway, which [the qualification below](#k-chain) sets out. Their reports are [`reviews/load-chain-review-1.md`](reviews/load-chain-review-1.md) and [`reviews/load-chain-review-2.md`](reviews/load-chain-review-2.md).

Both answered *partly*, and both arrived at the finding the measurement had already made from the other direction.

- **The rule's window is one sentence wide.** Review 1: "The rule's window is one sentence wide; the defect is as wide as everything the reader has already read." Both reviews record that *bridge* is nowhere defined, so a heading, a standfirst, a lead or an earlier paragraph can pre-say a quotation without the words of the rule reaching it.
- **Nothing pairs a subheading with the quotation under it.** `case-study.review.md` pairs bridges with quotations and the standfirst with the body's opening; both reviews name the missing pairing. Only review 1 proposes adding it, as its first must-fix; review 2 treats the gap itself as #396's and makes its own must-fix the question of which half the repair lands in — "#396 owns the heading gap. My insistence is on **where its repair goes**."
- **`headlines.md` pulls the other way.** Its instruction to word a subheading from its whole section, in words its first sentence does not use, is satisfied by a subheading that says what the quotation two sentences down says. Review 2 calls that line a must-fix in its own right, and notes that Write loads it.
- **The composing half gets the least.** Write loads the genre but no `.review.md`, so the only operable wording — "Remove a redundant pre-echo while keeping the attribution and any distinct fact" — reaches the reviewer and not the agent writing the sentence. Both reviews make this a must-fix, and rank it differently: review 2 its second — "any wording written for the heading case must land in a half the writer loads" — and review 1 its third and last, which it alone qualifies, calling its own first two blocking and this one "blocking on the merits of the reading alone".

Two of those must-fixes — the missing pairing, and what counts as a bridge — are the substance of [#396](https://github.com/Kntnt/skills/issues/396), and the asymmetry in what Write loads is recorded here and in that issue, whose body carries it under *A fourth reach problem, from the load chain rather than the runs*. The remaining one, `headlines.md`'s subheading recipe licensing the fault, is recorded here and in the two reviews and in no issue: #396 names `headlines.md` only as a candidate place for a future repair. Nothing from either review is acted on in this ticket, whose exit forbids a product change.

One qualification, so the independence is not overstated: **neither review is a blind reading.** Both had this evaluation's own output in the working tree and both used it.

- Review 2 cites ADR-0214 through its argument — for the heading result, for the `sv-r2` split over where the bridge is, and for the `en_US-r1` three readings — and cites `plan.md` for the only written definition of *bridge* in the repository — a citation that is itself inexact, since the definition is in the two judge briefs frozen beside the plan and not in `plan.md`. It names #396 by number.
- Review 1 cites the plan's definition — the same inexact citation — and how both judges read it in the body of its argument, and records under a heading *One note on the record*, near its end, that "After forming the above I read `docs/adr/0214-a-bridge-prepares-a-quotation-rather-than-pre-says-it.md`" — naming #396, the ADR and the seven-run non-reproduction in that section. So its own account is that its findings were formed before it read the record and checked against it afterwards — which is its statement about its own process, not something this file can verify from the artefact.

The corroboration is therefore worth what two informed readings are worth, one of which says it formed its findings first. That is less than two blind readings would be worth, and the claim here is held to it.

## `K-preserve`

Holds, on the point the criterion is about: no quotation quota, no canonical sentence and no extra genre review in Write's source comparison was introduced, because nothing was introduced at all.

The baseline drafts' own `F1`, `G2` and `L1` results are measured behaviour of `218e3be1` and are recorded rather than repaired here. The rule the records apply is the plan's, and the counts below apply it too: **where the two judges split, both readings stand, no judge is an oracle, and the row counts as unmet on that point.**

`F1` **fails on five of the seven drafts and passes on two.** It passes on both judges in `case-question-en_GB-r1` and `-r3` only. It fails on both judges in three rows, each on one shape — a display line or lead restating a supported claim at a strength or scope the material does not give it: `case-question-en_GB-r2`, a heading dropping the summary's say-so ("**It says** staff could see …"); `case-study-sv-r1`, a heading dropping the one interval the material measures; `case-study-en_US-r2`, a lead narrowing the note's owner from the company to the maintenance team. It fails on one judge in the two remaining rows, and both of those rest on the byline: in `case-study-en_US-r1` judge B's fail is on the byline and nothing else, and in `case-study-sv-r2` judge B's is on the byline together with an agentless passive that drops the maintenance team.

Every draft carries a byline naming Thomas Barregren — "By Thomas Barregren" in the English rows, "Av Thomas Barregren" in the Swedish — where the brief supplies no author; both source checkers are instructed to exclude the byline, the replies disclose it, and it is invocation-derived rather than sourced, so it is recorded as an observation and not filed. This file does not count it and then also set it aside: it is the whole of what makes `case-study-en_US-r1` split, and one of the two grounds judge B gives in `case-study-sv-r2`, the other being the agentless passive; the splits are what the counts above report.

One item that reads like a recurring failure and is charged by no judge is **not** counted above: the standfirst of `case-study-en_US-r1` stating the note's filtered count of 31 in the draft's own voice. Judge A records it as a reservation and does not charge it; judge B lists it first under "Four places I tested and would not fail, but which are tighter than the literal material", and calls it "A caveat deferred, not dropped."

`G2` fails on two drafts, both splits: `case-study-en_US-r2` on judge A, for no truthful publisher stance anywhere in the delivered text, and `case-study-sv-r1` on judge B, for a headline, standfirst and lead delivering the same clause three times. `L1` draws a verdict from thirteen of the fourteen Write judgements rather than all fourteen — judgement A of `case-question-en_GB-r3` has no `L1` section and gives no verdict, which the Write record carries as `skipped` on that judge with that reason — so `case-question-en_GB-r3` stands on one judge's `L1` reading and not two. Of the thirteen, `L1` fails once, on `case-study-en_US-r2` and on judge B, for British lexis in `en_US` narration.

## `K-cost`

The plan asks for the word delta of the files actually changed, the resulting mandatory reading for a `case-study` run, and measured wall times per arm. **The word delta is zero**, because no file under `skills/` or `tests/` changed. The mandatory reading is therefore what `main` already required at `218e3be1`, and it is measured here rather than carried forward from the ticket body's pre-#362 figure, which the addendum records as stale.

Measured with `wc -w` over the whole file, on the chain a `case-study` `Write` run is instructed to load — `SKILL.md` steps 5, 6 and 8, with the technique level empty because `case-study.md` names none, and `quotations.md` in because every row's material is speech to be quoted:

| File | Words |
| --- | --- |
| `skills/editorial/write/SKILL.md` | 2 486 |
| `skills/kntnt/library/references/editorial/base.md` | 597 |
| `skills/kntnt/library/references/editorial/genres/case-study.md` | 282 |
| `skills/kntnt/library/references/editorial/web-craft.md` | 184 |
| `skills/kntnt/library/references/editorial/article-anatomy.md` | 777 |
| `skills/kntnt/library/references/editorial/headlines.md` | 620 |
| `skills/editorial/write/references/quotations.md` | 671 |
| **Subtotal, language-independent** | **5 617** |
| `skills/editorial/write/references/source-check.md` | 1 930 |
| **Subtotal, including the comparison resource** | **7 547** |

The composition scope of the resolved language is added to that, and it is the only part that differs by row: `en_GB` 260 words, `en_US` 190, `sv` 568. So the mandatory reading is **7 807 words for a `case-question-en_GB` run, 7 737 for `case-study-en_US` and 8 115 for `case-study-sv`** — of which `source-check.md` is read by each source-comparison subagent rather than by the composing agent, so the composing agent's own share is 5 877, 5 807 and 6 185 respectively. No `.review.md` and no language scope but `composition` is in the count, because step 5 excludes them in as many words.

Wall times are per run rather than per arm, there being one arm: they are in [the table above](#what-ran) and in both records, and they run from 7m22s to 24m35s over the fourteen runs. They are wall times of a `claude -p` session under whatever load the API was carrying, and four rows' timings sit in a later window for the reason given above, so they are not a causal measure of anything the ticket changed — which is nothing.

The plan's tie-break — *a wording that adds reading ships only where the candidate arm removes a miss the baseline arm reproduced* — has no miss to point at, so the shorter wording, which is the shipped wording, stays.

## `T1` and `R2`

Recorded `skipped`, as the plan fixed before the runs: a subagent's transcript is not readable from the session that started it. Nothing here claims either passed and nothing is failed for lacking them. The load-chain question they would have carried is moot, because no load chain changed. [#388](https://github.com/Kntnt/skills/issues/388) owns the missing trace-bearing harness.

## What is filed

Exit 1 requires the cross-family result to be filed as its own `needs-triage` issue naming #364. Two issues are filed; both name #364 and neither duplicates an open number.

- [#395](https://github.com/Kntnt/skills/issues/395) — the fault does not reproduce in this family, and stays failed in the GPT family, which this session may not retest.
- [#396](https://github.com/Kntnt/skills/issues/396) — the pre-echo sits in the section heading, where the bridge rule does not reach, together with the two classing splits that any wording written for it would have to survive.

The decision not to change the shipped wording is recorded in [ADR-0214](../../adr/0214-a-bridge-prepares-a-quotation-rather-than-pre-says-it.md).

## The records

- [`../records/write-claude-2026-09-22-364.md`](../records/write-claude-2026-09-22-364.md)
- [`../records/redline-claude-2026-09-22-364.md`](../records/redline-claude-2026-09-22-364.md)
