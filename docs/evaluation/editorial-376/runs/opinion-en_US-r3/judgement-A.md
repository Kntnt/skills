# Run judgement — opinion / en_US / r3

Judged from `write/work/source.md`, `write/response.md`, and the four files under `write/evidence/source-check/`. Nothing else read.

## 1. Outcome

**A draft was delivered.** The response opens by declaring it: "**This draft is delivered with known defects.** The final source comparison left two findings, both about source support, neither repaired — a repair no comparison has read would be unchecked prose, and this run had used both of its comparisons."

**Two comparisons ran.** `report.md` (against `draft.md`, 7 findings) and `report-2.md` (against `draft-2.md`, 2 findings).

**The delivered prose is byte-identical to the last prose a checker saw.** Extracting the fenced block from `response.md`, stripping the `kntnt` frontmatter, and diffing against `evidence/source-check/draft-2.md` produces no difference at all. The dispositions in the response's "How it was checked" paragraph describe changes made *between* the two comparisons only; nothing is claimed or visible after the second. No difference to quote.

One evidence defect, not a prose defect: `draft.md` and `draft-2.md` are the same file byte for byte (md5 `e4fb0a51…`). The round-one draft was overwritten in place by the repairs, so **the evidence does not preserve the text checker 1 actually read**. It survives only as quotations inside `report.md` — which is enough to verify every round-one disposition (each of the seven quoted originals is absent from the delivered text and each proposed repair is present), but the run cannot show its own first draft.

## 2. Remaining findings

Both findings of the last comparison reached the user unrepaired. For each, the response names the passage, states what the material carries instead, and gives the smallest repair — quoting the checker verbatim.

**Report-2 F1 — "two of the seven premises".**
- Passage named: yes — *"**Finding 1 — "two of the seven premises" (first line under the first heading).**"*
- What the material carries instead: yes — *"The material says the pilot ran *i två lokaler* and, separately, that the proposal covers *alla sju lokaler*. It nowhere states that the two pilot premises are among those seven, and it never says seven is the total."*
- Why it matters: given — *"the overlap carries weight: it tells the reader what fraction of the affected premises the evidence base covers."*
- Smallest repair: given verbatim — *"The pilot report of April 8 covers eight weeks in two premises: 96 bookings through the web, 24 by phone."*

**Report-2 F2 — "a labor cost with a number attached".**
- Passage named: yes, with location — *"(second paragraph under "What we are asking for")"*.
- What the material carries instead: yes — *"The proposed trial records *tidsåtgång per bokningsväg* — time per route. Nothing in the material converts that time into money, and the association explicitly disclaims having costed anything."*
- Smallest repair: given verbatim — *"That gives the board what it lacks now: the time each route actually takes, in numbers, and a reason for the phone from the people still using it."*

The response then hedges both: *"Both are the checker's allegations for you to settle, not established facts about the text. I make no fidelity claim for those two passages."* That disclaimer is honest about provenance but under-commits. F2 in particular is not a debatable allegation — the material supplies no wage rate, no pricing step, and an explicit disclaimer of any costing, and the writer's own round-one repair (`tidsåtgång per bokningsväg` → "the time each route takes") sits two lines above it, making the gap between what is recorded and what is promised visible in the writer's own text. It could have been settled from the material without a third comparison.

## 3. F1 — **fail** (judged on the delivered text)

Most of the draft is tight, and several traps are cleared cleanly:

- Third unmeasured item is habituation, not ability: *"It does not measure age, functional ability, or how used to digital services anyone is"* — `digital vana` rendered as habituation, never as "digital skills". Correct.
- Unknown kept apart from absent, in both directions: *"Twenty-four phone bookings therefore say nothing about how many people in Lervik cannot book digitally — not that the share is small, and not that it is large."* This is the source's single negative spelled out without converting absence of evidence into evidence of absence.
- No count-size judgement: 96 and 24 are stated with no "only", "just" or "a small minority", and both are attributed — *"Both figures are the report's."*
- No invented event, law, protest, discrimination case, party motive or established saving. Chronology (eight-week pilot → April 8 report → June 18 meeting → September start → six-month trial → decision after) is intact throughout.
- Cost uncertainty preserved and the board's three options named in order with modality intact: *"Six months on, it can close a channel, change one, or keep both."*
- Modality repaired correctly at *"We make no claim to have funded this trial or costed it"* (`gör inget anspråk på att ha` ≠ "we have not").
- Author perspective correct: the one releasable standpoint is carried as Sanna Ek's own unquoted prose, which is right because she is the byline and the material permits `citeras eller refereras`.

It nonetheless fails, on two unsupported items that reached the reader:

1. **Set membership not in the material — "two of the seven premises".** The material says `i två lokaler` and, in a separate sentence about a separate document, `för alla sju lokaler`. It never states that seven is the total stock of `föreningslokaler`, and never places the two pilot premises inside the seven. The draft asserts the overlap and the overlap does work: it tells the reader the evidence base covers 2/7 of what the decision would change. Minor in isolation, but it is an addition, and it is one the run **introduced itself** — checker 1's quotation shows round one read *"covers eight weeks in two halls"*, with no relation asserted. The term repair (`halls` → `premises`) was right; the relation was smuggled in with it.

2. **Changed thing measured — "a labor cost with a number attached".** The proposed trial records `tidsåtgång per bokningsväg`: time per route. Time is not cost without a price for the time, and the material supplies no wage rate, no staffing figure and no costing step; the association disclaims having costed anything at all. The draft tells the reader the trial hands the board a labor cost with a figure on it. This is a changed thing measured in the strict sense the criterion names, and it also contradicts the draft's own next section (*"We make no claim to have … costed it"*). This is the substantive failure.

Two smaller slippages, recorded but not carrying the verdict:

- *"Six months of both routes has a price, and weighing it against what those routes are worth to the people who use them is the board's job"*. The material holds two distinct cost objects: the trial's cost, which `kommunstyrelsen ta ställning till`, and `arbetskostnaden`, which Ek says must be weighed against `värdet för användarna`. The draft weighs the first against the second. The two largely coincide here, so it is a blend rather than an invention — but it is not what either sentence says.
- *"should say so with **the** figure in front of it"*. The definite article presupposes a figure that the material says nowhere exists. Read in context it is a demand that one be produced, which is defensible; the definite article is the weakest point in an otherwise well-preserved treatment of the cost.

Translated terms checked both directions: `association premises` for `föreningslokaler` lets in a private association's own clubhouse that the municipality would not book, and `föreningslokaler` is fully covered — acceptable, and far better than round one's `community halls`, which added both "hall" and "community". `functional ability` for `funktionsförmåga`, `the municipal executive board` for `kommunstyrelsen`, `the staff report` for `tjänsteutlåtandet`, `the people who use them` for `användarna`, `people in Lervik` for `invånarna` all hold in both directions. `how used to digital services anyone is` is narrower than `digital vana`, but since the source denies measurement of the wider construct, the narrower denial is entailed — it claims less, not more. `booking details` for `uppgifter` specifies slightly; the whole document concerns bookings, so nothing else is in play.

## 4. G2 — **pass**; L1 — **pass**

**G2 (opinion: early position, support, relevant real objection, identifiable action and actor) — pass.** The four parts do distinct work and none is decorative.

- *Early position*: the title and the first paragraph. *"Öppna beslut is asking the board to wait: six months with both the phone and the web open, in all seven of them"* — the ask is stated before any evidence, in the reader's first breath.
- *Support*: "What the pilot actually measured" is the argument's load, and it is a specific one — the instrument counts bookings rather than people and measures none of the attributes the decision turns on, so the 24 settles nothing either way.
- *Relevant real objection*: "The real objection deserves a real number" states the administration's actual case and concedes it — *"That is the administration's actual objection, and it is a serious one. It is not that people who call are lazy or expensive, and I will not pretend otherwise."* This is the strongest structural move in the piece: it refuses the easy motive the material forbids, and then answers the real objection on its own ground (*"A serious objection deserves a measurement, and the documents hold none"*). A reader who came in sympathetic to the administration is met rather than caricatured.
- *Identifiable action and actor*: both are unambiguous. Actor — the municipal executive board, on June 18. Action — postpone, run six months in all seven premises with both routes, with the administration recording time per route and asking users why they chose. Closing action named with the board's three options and the cost left open.

The only structural cost is length: 477 words against a brief asking for `ungefär 400`, about 19 percent over. The response argues the excess is load-bearing qualification, and that is true of the two-directional sentence and the attribution of the figures — but "The decision on June 18" carries three sentences of cost-positioning where one would do, so the overage is not wholly forced. Brief compliance, not a G2 failure.

**L1 — pass.** The prose reads as written in English, not translated into it. No Swedish syntax survives: no verb-second inversions, no calqued connectives, no run-on comma splices. The idiom is native and, at its best, genuinely good — *"a decision with something behind it"*, *"The board is being asked to close a channel to spare an amount of work its own papers never state"*, *"I will not pretend otherwise"*. Rhythm varies: the clipped *"Six months, all seven premises, both routes open."* lands against the longer analytical sentences around it. Reader effect: a composed, unhedged, specific advocate who is arguing about the decision basis rather than about the administration's character — which is the voice the boundaries ask for.

Register nits, none of them Swedish interference: *"costed it"* is Commonwealth register where en_US would reach for "priced it out" or "put a cost on it"; *"association premises"* is precise rather than idiomatic for a US reader (a US municipality would say community facilities or meeting rooms), and *"functional ability"* reads faintly institutional. These are en_US register, not imported phrasing, and they do not obstruct an ordinary reader.

## 5. Intermediate — every checker finding

**Report 1 (against the round-one draft; 7 findings, all repaired).**

| Passage | Allegation | Writer's action | Class |
|---|---|---|---|
| "all seven community halls" / "two halls" | `föreningslokaler` is not "community halls"; adds both hall and community | Repaired to "association premises" / "of the seven premises" / "all seven premises" | **Supported repair** — the term was genuinely wider and differently shaped. But the repair introduced report-2 F1 (the set relation), so: right repair, defectively executed |
| "We have not funded this trial or costed it" | `gör inget anspråk på att ha` records the absence of a claim, not the absence of the act | Repaired to "We make no claim to have funded this trial or costed it" | **Supported repair** — a real modality change, correctly restored |
| "staff should not have to enter the same booking twice" | `föra in uppgifter i två flöden` is information into two workflows, not one record keyed twice | Repaired to "enter booking details into two separate workflows" | **Supported repair** — the original specified a duplication the material does not describe |
| "Nothing in these documents says that people who call are lazy or expensive" | The material establishes the administration's real objection, not the contents of the whole document set | Repaired to "It is not that people who call are lazy or expensive" | **Supported repair** — the negative's scope was genuinely wider than the source's |
| "worth to residents" | `användarna` are the people who book; `invånarna` are the population — and the draft used "people in Lervik" for the latter elsewhere | Repaired to "worth to the people who use them" | **Supported repair** — two distinct populations, correctly separated |
| "does not record age…" | `mäter inte` denies measurement, not possession of the data | Repaired to "does not measure age…" | **Supported repair** — not measuring is compatible with holding the data; not recording is not |
| "how long a booking takes on each route" | `tidsåtgång per bokningsväg` is per route, not per booking; commits the association to a method it did not propose | Repaired to "the time each route takes" | **Supported repair** — and it sharpened the still-unrepaired cost claim two lines later |

**Report 2 (against the delivered draft; 2 findings, neither repaired).**

| Passage | Allegation | Writer's action | Class |
|---|---|---|---|
| "two of the seven premises" | Set membership the material never states; seven is never given as the total | Not repaired; disclosed in the response with the checker's repair quoted | **Right finding rejected** — correct, though the least consequential of the two |
| "a labor cost with a number attached" | The trial records time; nothing converts time to money, and the association disclaims any costing | Not repaired; disclosed in the response with the checker's repair quoted | **Right finding rejected** — correct and substantive, and settleable from the material alone |

**Non-findings that should have been findings.** Report 1 row #21 affirmatively cleared *"a labor cost with a number attached"*, calling it *"Author, resting on supported material"* and `arbetskostnaden` → "a labor cost" *"exact"*. That is a **missed defect**, caught one round later by a fresh checker. It is the single clearest illustration in this run of why the second comparison earns its cost — and, symmetrically, report-1's own repair created report-2's F1, illustrating the opposite risk the response names when it declines to repair unchecked.

**Did a real F1 defect escape every checker?** Essentially no — both defects that reached the user were seen and reported, and the response passed both on to the reader intact. The one thing neither checker filed as a finding is the conflation at *"Six months of both routes has a price, and weighing it against what those routes are worth to the people who use them"*: report-2 §1.16 examined the passage and cleared it, addressing who does the weighing but not that the material's `Kostnaden` (the trial's cost, for the board to take a position on) and `arbetskostnaden` (weighed against user value) are two different objects. Minor, and not enough on its own to change any verdict. The *"with the figure in front of it"* presupposition was raised by checker 1 as an editorial question (Q1) rather than a finding, and by checker 2 as supported; I agree it does not rise to a defect, but it is the closest call either checker declined to file.

## 6. Preservation

The user is left holding the complete prose. The delivered draft appears inline in `response.md` as a fenced Markdown block with its `kntnt` frontmatter intact, so nothing depends on a file the user cannot reach — which matters here, because the response states plainly *"the draft was composed and compared in a scratch directory that has been removed, and `source.md` is untouched."*

What was and was not compared is stated exactly: two comparisons, the first against the whole draft and the whole of `source.md` leaving seven findings, all seven itemised in the response by their original wording; a fresh checker on the repaired draft leaving the two above. The response also volunteers that one of the two remaining findings *"was introduced by my own first-round repair"* — verifiable against `report.md`'s quotations, and true. It states that no translation finding was raised in either pass and why. It names the gaps in the material ("No cost, anywhere", "Nothing about who calls", "Nothing about the seven premises", "No stated wage rate or staffing figure") and what would close them, and it declares the length overage (477 against ~400) with its reason rather than leaving the user to count.

The one thing the user is *not* left holding is the round-one draft: `draft.md` in the evidence was overwritten by the repairs and is byte-identical to `draft-2.md`, so the text checker 1 read exists only as quotations inside its own report.

The disclosure is unusually complete and the hedge *"I make no fidelity claim for those two passages"* is honest. But honesty is not the same as delivery: the user receives prose carrying one defect (the cost-for-time substitution) that the supplied material settles without any further comparison, and the run chose to explain it rather than fix it.

---

**Verdicts: F1 fail · G2 pass · L1 pass.**
