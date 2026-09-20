# Run judgement — opinion / en_US / r3

Judge B. Read: `write/work/source.md`, `write/response.md`, `write/evidence/source-check/{draft.md,draft-2.md,report.md,report-2.md}`. Nothing else.

---

## 1. Outcome

**A draft was delivered**, with two known defects declared above it. **Two comparisons ran.**

**The prose the user received is byte-identical to the last prose a checker saw.** The fenced block in `response.md`, with its four-line `kntnt` frontmatter map removed, matches `evidence/source-check/draft-2.md` byte for byte (verified by diff; both 477 words of prose). No prose change was made after the last comparison, and the reply's own account claims none.

One difference that is not prose: the delivered block carries frontmatter (`genre: opinion`, `technique: none`, `language: en_US`) that `draft-2.md` does not. It asserts nothing about the source material, and the reply states the map is there because Handoff Metadata is on. Not a defect; recorded for completeness.

**An evidence gap.** `draft.md` and `draft-2.md` are byte-identical (md5 `e4fb0a51…`), yet `report.md` quotes a draft that differs from both in seven places — "community halls", "two halls", "We have not funded", "does not record", "the same booking twice", "worth to residents", "how long a booking takes". The first draft file was therefore overwritten with the repaired text; the pre-repair draft is not preserved. The seven repairs remain individually verifiable, because `report.md` quotes the old wording and `draft-2.md` carries the new (I checked each: all seven old forms absent, all seven repaired forms present). What cannot be checked from the evidence is whether anything *else* changed between the first draft and `draft-2.md`, since no first-draft file and no disposition file survive. Round-one dispositions exist only as the reply's narration.

## 2. Remaining findings

The last comparison (`report-2.md`) raised two findings. **Neither was repaired.** For each, the reply names the passage, states what the material carries instead, and gives a proposed smallest repair — all three, for both.

**F1 — "two of the seven premises."** The reply quotes it and locates it ("first line under the first heading" — correct). It says what the material carries: *"The material says the pilot ran* i två lokaler *and, separately, that the proposal covers* alla sju lokaler*. It nowhere states that the two pilot premises are among those seven, and it never says seven is the total."* It states why the relation matters: *"it tells the reader what fraction of the affected premises the evidence base covers."* It gives the repair verbatim: *"The pilot report of April 8 covers eight weeks in two premises: 96 bookings through the web, 24 by phone."* Complete.

**F2 — "a labor cost with a number attached."** Quoted and located ("second paragraph under 'What we are asking for'" — correct). Material stated: *"The proposed trial records* tidsåtgång per bokningsväg — *time per route. Nothing in the material converts that time into money, and the association explicitly disclaims having costed anything."* Repair given verbatim: *"That gives the board what it lacks now: the time each route actually takes, in numbers, and a reason for the phone from the people still using it."* Complete.

**A qualification the reply attaches to both.** *"Both are the checker's allegations for you to settle, not established facts about the text. I make no fidelity claim for those two passages."* The disclosure is full and the user can act on it unaided; but the framing invites the reader to treat both as open questions. On my own reading of the source, both are real defects, not open questions — see §3.

**One reply claim I checked.** *"one of them introduced by my own first-round repair."* True, and true of F1 specifically: `report.md` #8 shows the first draft read "two **halls**" with no set relation, and `report.md`'s F1 repair proposed "two of them" as a short form. The writer wrote "two of the seven premises" and introduced the overlap. F2 was *not* introduced by a repair — "a labor cost with a number attached" stood in the first draft and `report.md` #21 passed it. The reply's "one of them" is therefore accurate as stated.

## 3. F1 — source fidelity, on the delivered text

**FAIL.** Two unsupported additions survive into delivered prose. Both were seen by the last checker and left in.

**(a) Changed scope — an unsupported set membership, and a count-size framing with no supplied comparison.** Delivered: *"The pilot report of April 8 covers eight weeks in two of the seven premises."* The material says *"ett åtta veckor långt försök i två lokaler"*, and separately *"telefonbokning tas bort för alla sju lokaler"*. It never states that the two pilot premises are among the seven, and never states that seven is the total stock of *föreningslokaler*. "Two of the seven" asserts both. It is also a count-size judgement — it hands the reader a fraction (2/7) of the affected set as the evidence base — and the corpus criterion requires a supplied comparison for exactly that. None is supplied. The draft's own lead ("all seven association premises") already gives the reader the contrast without the assertion.

**(b) Changed thing measured — time reported as money.** Delivered: *"That gives the board what it lacks now: a labor cost with a number attached."* What the proposed trial records is *"tidsåtgång per bokningsväg"* — time per booking route. Nothing in the material prices that time; no wage rate, no staffing figure, no conversion step. The material treats the two as distinct in its own words — *"Någon tidsmätning eller ekonomisk besparingsberäkning finns inte i handlingarna"* lists a time measurement and a cost calculation as two missing things, and the proposal supplies only the first. The draft promises the board the second. It also contradicts the draft's own next paragraph, *"We make no claim to have funded this trial or costed it."* Sanna Ek's *arbetskostnaden* appears in the material only as what the municipality must eventually be able to weigh — not as an output of the trial.

**Two borderline passages, both cited for completeness, neither driving the verdict.**

- *"eight weeks of counting that was never built to answer the question."* "Built to" asserts design intent, which the material nowhere describes; it states the pilot's *limits*, not its purpose. Read as a capability claim — the reading the two preceding paragraphs set up — it is *"kan därför inte användas för att säga"* and is supported. The boundaries expressly license sharp criticism of the decision basis, so I let it stand. `report-2.md` reached the same place as O2.
- *"should say so with the figure in front of it."* The definite article sits two sentences after a disclaimer that nobody has costed anything, and can be heard as presupposing a figure exists. In context it reads as a demand that one exist before the board decides, and the preceding clause ("has a price") keeps the cost unpriced. Stands. `report.md` reached the same place as Q1.

**What the draft got right, and which the criterion specifically tests.**

- The third unmeasured item is habit, not ability: *"It does not measure age, functional ability, or how used to digital services anyone is."* — *digital vana* rendered as habituation, not as skill or capacity. Correct, and it is the trap the criterion names.
- Unknown is kept apart from absent: *"Twenty-four phone bookings therefore say nothing about how many people in Lervik cannot book digitally — not that the share is small, and not that it is large."* Both directions stated. No absence-of-evidence-as-evidence-of-absence.
- Modality on the disclaimer is exact: *"We make no claim to have funded this trial or costed it"* for *"gör inget anspråk på att ha finansierat eller kostnadsberäknat"*.
- The figures are attributed as the boundaries require ("Both figures are the report's") and carry no evaluative gloss — no "only 24", no "just".
- The administration's motive is not falsified: *"It is not that people who call are lazy or expensive, and I will not pretend otherwise"* — scoped to the objection, not to the contents of the papers.
- Chronology holds throughout: eight-week pilot → April 8 report → June 18 meeting → September start → six months → decision.
- No law, protest, discrimination case, party motive or established saving appears anywhere — every boundary exclusion respected.
- Term check in both directions: *föreningslokaler* → "association premises" admits nothing the Swedish excludes and excludes nothing it admits; *användarna* → "the people who book" is kept distinct from *invånarna* → "people in Lervik", which the draft uses separately and correctly.

## 4. G2 — do the required parts do distinct jobs?

**PASS**, and strongly on the objection.

- **Early position.** First paragraph, second sentence: *"Öppna beslut is asking the board to wait: six months with both the phone and the web open, in all seven of them."* The title carries it too. Nothing is withheld for a reveal.
- **Support.** Two sections doing different work: what the instrument can and cannot show (bookings not people; no age, ability or habit), then what the decision basis lacks (*"no timing of either route, no calculated saving"*). Neither restates the other.
- **A relevant real objection.** *"The staff report gives one reason for closing the phone line: staff should not have to enter booking details into two separate workflows. That is the administration's actual objection, and it is a serious one."* This is the opposing case at its real strength, conceded as serious, with the cheap version explicitly refused. A second objection — against the author's own proposal — is then met rather than dodged: *"Six months of both routes has a price, and weighing it against what those routes are worth to the people who use them is the board's job, not ours."* Two live objections, neither a straw man, neither neutralised into mush. This is the part most opinion drafts fail, and it is the strongest thing in this one.
- **Identifiable action and actor.** Actor: the municipal executive board, named, with its meeting date. Action: postpone, run six months in all seven premises with both routes, then choose. A second actor with a second action: *"The administration records the time each route takes and asks the people who book to say, if they want to, why they chose as they did."* The close names all three outcomes the material allows — *"it can close a channel, change one, or keep both"* — with the cost uncertainty left standing.

Reader effect: a reader finishes knowing who decides, when, what is being asked of them, and what the evidence cannot settle. No section could be cut without losing a job.

*Outside G2, noted once:* the brief asked for ~400 words and the delivered prose is 477, about 19 percent over. The reply states the number and its reasoning. Not a criterion here.

## 5. L1 — professional en_US, no Swedish phrasing

**PASS.**

No Swedish syntax survives. No V2 inversion, no calqued article use, no *dock*/*redan*/*alltså* connectives, no nominal stacking. The rhythm is English-argumentative and the strongest lines are ones a Swedish source would not produce: *"It counts bookings, not people, so one resident who books every week is many bookings and still one resident"*; *"The board is being asked to close a channel to spare an amount of work its own papers never state"*; *"Waiting is no vote against digital booking — I am not against it."* Sentence length varies deliberately; the short declaratives land where the argument turns. It reads as written, not as rendered.

Two register slips, which I record as **locale mechanics and keep out of the L1 verdict** as the criterion directs: **"costed it"** is BrE — the en_US idiom is "priced it out" or "put a cost on it" (`report-2.md` O3 saw this and correctly placed it outside its own scope); **"Six months on"** is likewise BrE, where AmE takes "Six months later". Both are one-word fixes and neither obstructs a US reader.

One phrase worth a note but not a finding: **"association premises"** is accurate and institutionally plausible, if slightly stiff on first encounter. It is the right trade — the alternatives that read more naturally ("community halls", "community centers") are the ones that add what the Swedish does not say, which is exactly why round one repaired it.

## 6. Intermediate — every checker finding, one line each

**First comparison (`report.md`, 7 findings, all repaired — each repair verified present in `draft-2.md`):**

| # | Passage | Allegation | Writer's action | Class |
|---|---|---|---|---|
| F1 | "community halls" / "two halls" | *föreningslokal* is premises let to associations; "community hall" adds both "hall" and "community" | Repaired to "association premises" / "two of the seven premises" | **Supported repair** — right finding, correct fix on the noun, but the rewrite overshot into a set relation and created `report-2.md` F1 |
| F2 | "We have not funded this trial or costed it" | *gör inget anspråk på att ha* records an absent claim, not an absent act | Repaired to "We make no claim to have funded this trial or costed it" | **Supported repair** |
| F3 | "enter the same booking twice" | *föra in uppgifter i två flöden* is two workflows, not one record keyed twice | Repaired to "enter booking details into two separate workflows" | **Supported repair** |
| F4 | "Nothing in these documents says that people who call are lazy or expensive" | widens a claim about the administration's objection into a claim about the whole document set | Repaired to "It is not that people who call are lazy or expensive" | **Supported repair** — and it preserves the boundary's demand that no false motive be invented |
| F5 | "worth to residents" | *värdet för användarna* is the people who book, not the population; the draft uses "people in Lervik" for *invånarna* elsewhere | Repaired to "worth to the people who use them" | **Supported repair** |
| F6 | "does not record age…" | *mäter inte* denies measurement, not possession of the data | Repaired to "does not measure age…" | **Supported repair** — and it is the sentence the corpus criterion tests |
| F7 | "how long a booking takes on each route" | *tidsåtgång per bokningsväg* is time per route, not per booking | Repaired to "the time each route takes" | **Supported repair** |

`report.md` also raised **Q1** ("with the figure in front of it") and **Q2** (length) as editorial questions, not findings; neither was acted on, and neither required action. I share Q1's mild unease and let the passage stand (§3).

**Second comparison (`report-2.md`, 2 findings, neither repaired):**

| # | Passage | Allegation | Writer's action | Class |
|---|---|---|---|---|
| F1 | "two of the seven premises" | set membership the material never states | Not repaired; disclosed in full, with the repair quoted; fidelity claim withdrawn for the passage | **Right finding left standing** — the nearest class in the list is *right finding rejected*, though the reply disputes nothing and rejects nothing; it declines to fix within budget and says so |
| F2 | "a labor cost with a number attached" | the trial records time; nothing converts it to money | Same | **Right finding left standing**, same qualification |

`report-2.md`'s **O1–O4** are observations requiring no repair; none was acted on. O3 ("costed" as BrE register) is a real en_US slip that no one owned, because the comparison correctly placed register outside its scope and the reply never picked it up.

**Was a real defect I found under F1 seen by no checker?** No. Both defects I cite were raised by the last checker, and both passages I flag as borderline were seen and reasoned about (`report.md` Q1; `report-2.md` O2). I found nothing the checkers missed. The failure here is not one of detection — it is that two correctly detected, correctly diagnosed defects with correct repairs in hand reached the user unrepaired.

## 7. Preservation — what the user is left holding

A draft was delivered, so the preservation question is narrower, but the reply handles it well.

- **The full prose is in the reply**, fenced, with frontmatter, ready to lift. The reply states that nothing was written to the filesystem for the user, that the scratch directory has been removed, and that `source.md` is untouched.
- **It says what was compared and what was not repaired.** Two comparisons, each described: the first left seven findings, all seven repaired and each named by the Swedish term at issue; the second left two, neither repaired, both quoted with the material and the proposed repair. It also says *why* no third pass ran — *"this run had used both of its comparisons"* — and why it did not silently fix them — *"a repair no comparison has read would be unchecked prose."* A user can act on either finding in under a minute without rereading the source.
- **It says where the material stops**, in four items, and names what would close each gap. It flags the length overrun with the number and the reasoning.
- **Two gaps.** The reply points to no report file: `report.md` and `report-2.md` exist under `write/evidence/source-check/`, but a reader of the reply alone does not know they exist or where. The disclosure is full enough that this costs little here. Second, the reply's *"nothing was written for you on the filesystem"* is true of the scratch directory and of a deliverable, but the user is left unaware of the evidence trail.
- **On honesty**, the reply is unusually good: it leads with the defects rather than burying them, refuses a fidelity claim for the two passages, and volunteers that one of the two was introduced by its own repair — a fact I verified against `report.md` and found accurate.

## 8. Verdicts

| Criterion | Verdict |
|---|---|
| **Outcome** | Draft delivered with two declared defects; two comparisons; delivered prose byte-identical to `draft-2.md` |
| **F1** | **FAIL** — "two of the seven premises" (unsupported set membership; count-size framing with no supplied comparison); "a labor cost with a number attached" (trial records time, not money) |
| **G2** | **PASS** — early position, non-overlapping support, two real objections conceded at strength, named actor and named action with a date |
| **L1** | **PASS** — native en_US idiom and syntax throughout, no Swedish importation; two BrE register slips ("costed", "Six months on") recorded as locale, not L1 |
| **Defect no checker saw** | None |
