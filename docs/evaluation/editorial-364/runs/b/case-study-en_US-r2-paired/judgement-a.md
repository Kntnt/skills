# Judgement A — case-study / en_US / r2-paired

## 1. Every difference between input and delivered text

| # | Before | After | Kind |
|---|---|---|---|
| 1 | standfirst: "manages 640 flats" | "manages 640 apartments" | Mechanical (locale: en_US vocabulary) |
| 2 | body §1: "Elm Quay Housing manages 640 flats," | "The company is responsible for 640 apartments," | Defect repair (verbatim echo of the standfirst) **carrying a claim change**: *manages* → *is responsible for* is a different relation between company and flats; the locale half of it is mechanical |
| 3 | body §1: "and telephone reports and emails had been stored separately." | "and a repair reported by telephone had been filed apart from one reported by email." | **Change to what the claim says (scope)**: the input says two kinds of report were stored separately — readable as each kept apart from the log or from one another; the delivered sentence fixes it to one reading, that a phone-reported repair sat apart from an email-reported one, and swaps *stored* for *filed* |
| 4 | "The team designed the categories itself and kept telephone reporting open for residents." | "The team kept telephone reporting open for residents." | **Removal of a claim** (defect repair: the clause pre-said Lind's quotation) |
| 5 | "trained six staff in two sessions" | "trained six employees in two sessions" | Mechanical (locale: *staff* as a count noun is BrE) |
| 6 | subheading 2: "The trial note counts 31 reports and claims no cause" | "Median time to assignment fell by a day, and no cause is claimed" | **Change to what the claim says (strength, subject, attribution)** — see §4 |
| 7 | "trial note of 4 December 2025 records" | "trial note of December 4, 2025, records" | Mechanical (locale: US date form, with the required comma after the year) |
| 8 | "two working days" | "two business days" | Mechanical (locale: en_US vocabulary) |

Nothing else moved. Standfirst, byline, lede, all three quotations, every limiting sentence, the closing section and the URL are byte-identical.

## 2. Bridges into quotations

Three quotations in the input, in order.

**Q1 — "We wanted the evening shift to see what the morning shift had already done. The categories were ours; Svale helped us put them into the log."**

- Bridge in the input: *"Maya Lind, the maintenance supervisor, puts the aim beside the division of work:"*
- Bridge in the delivered text: identical.
- Class before: **(b)**. It gives the speaker, her office and the shape of what follows ("puts the aim beside the division of work"), but delivers neither the aim (the evening shift seeing the morning shift's work) nor the division (the categories were the team's, Svale did the configuring). Naming the two topics is not saying what the quotation says.
- Class after: **(b)**, unchanged.
- Changed: no. Nothing named, nothing supplied, nothing lost.
- Worth recording: the *pre-echo* the run repaired was not in the bridge but one paragraph earlier — "The team designed the categories itself" against "The categories were ours". The run removed the earlier clause and left the bridge alone, which is the right end to cut. The reply names this repair, though it calls the removed clause "the narrative pre-saying Maya Lind's quotation", not a bridge.

**Q2 — "We spent more time agreeing on the categories than entering the first reports. I would set that time aside before the next building starts."**

- Bridge in the input: *"Lind's account returns to the categories."*
- Bridge in the delivered text: identical.
- Class before: **(b)**. Speaker plus subject ("the categories"); it does not say that agreeing took longer than entering reports, nor that she would set the time aside.
- Class after: **(b)**, unchanged.
- Changed: no; nothing supplied, nothing lost.

**Q3 — "I would choose to do the trial again. Having one view of the reports helps us, but I would leave an extra week for preparation."**

- Bridge in the input: *"Her verdict is qualified, and she does not extend it to every housing company."*
- Bridge in the delivered text: identical.
- Class before: **(c)**. "she does not extend it to every housing company" is a fact the quotation does not carry — Lind never mentions other housing companies, or any scope at all; the clause is the article's own reading of the limits of her verdict. "Her verdict is qualified" also front-runs the *but* clause, which edges toward (a), but the (c) element decides the class.
- Class after: **(c)**, unchanged.
- Changed: no. Since it is unchanged, nothing the input's bridge carried was lost — including the non-extension claim, which the quotation still does not carry and which therefore still rests on the narrator alone.

Summary: all three bridges came back untouched; classes before and after are (b), (b), (c).

## 3. Quotations themselves

| Quotation | Wording back unchanged? | Notes |
|---|---|---|
| Q1 (Lind, aim and division of work) | Yes, verbatim, including the semicolon | Meaning, stance, certainty and voice intact |
| Q2 (Lind, time agreeing on categories) | Yes, verbatim | Intact |
| Q3 (Lind, would do it again, extra week) | Yes, verbatim, including the reservation "but I would leave an extra week for preparation" | Intact |

No quotation was cut, merged, trimmed, re-punctuated or converted to indirect speech. The reply's claim that "Every quotation is verbatim" is true.

## 4. R1 — **fail**

### What the run got right

- All four locale corrections are correct en_US and needed: *flats* → *apartments* (both places), *staff* → *employees*, *working days* → *business days*, and `4 December 2025` → `December 4, 2025,` with the closing comma. None of them touches a figure or a name.
- The standfirst/body echo at the top of §1 was a genuine, visible defect: the input's first body sentence repeated the standfirst's first clause almost word for word. Repairing it was legitimate.
- The pre-echo repair (difference 4) is legitimate: the narrative was saying "The team designed the categories itself" a few lines before Lind says "The categories were ours", and the run cut the narrative side, not the quotation.
- Every limiting sentence survives verbatim — *No comparison with another supplier is available*, *the note explicitly does not attribute the difference to the software*, *Assignment is not completion*, *The trial produced no cost figures…*, *she does not extend it to every housing company*, *Elm Quay's trial has not expanded yet*. A case study of this kind lives on those sentences and the run left them alone.
- The text was not rewritten to taste: three paragraphs, the lede, the byline, both later sections and all three bridges came through untouched. There is no taste-only change anywhere in the diff.
- The reply's account of the removal (difference 4) is accurate: it names the removed clause, the finding it served, and where the claim still stands (Lind's quotation, and subheading 1 "The team chose the supplier and made the categories").

### Why it fails

**The review introduced a claim the text refuses to make, and shipped it.** Subheading 2 now reads "Median time to assignment fell by a day, and no cause is claimed" against an input subheading of "The trial note counts 31 reports and claims no cause". Three things moved:

- *Strength*: the section reports two medians — two business days in the trial, three in the preceding period — and immediately bounds them with "The two periods carried different workloads". "Fell by a day" converts two static figures into a movement, which is the exact inference the trial note declines to license. In the scan layer of the article, the text now delivers a result the body withholds.
- *Attribution*: "The trial note … claims no cause" named who declines to attribute. "no cause is claimed" is agentless; the body still says it is the note, so the heading is now weaker than and detached from the sentence it heads.
- *Subject*: the heading no longer carries the count of 31 reports, which is the section's one hard figure.

The run's reply reports all of this, precisely and without evasion, and explains that the budget was spent on the round that created it. That candour is real and it is the reason this is a near miss rather than a bad run — but R1 asks what the delivered text does, and the delivered text now overstates its own evidence in a heading, on the one axis this genre exists to hold. The review created the defect; it did not find it. The input's subheading was at worst mildly repetitive of the first sentence beneath it; the replacement is a fidelity error.

**One claim change went unreported.** Difference 3 — "telephone reports and emails had been stored separately" → "a repair reported by telephone had been filed apart from one reported by email" — changes what is asserted. The input leaves open whether the two kinds of report were kept apart from each other or each kept outside a common log; the delivered sentence settles it as the former, and substitutes *filed* for *stored*. The reply's claim account covers the first half of that sentence only ("*Elm Quay Housing manages 640 flats* became *The company is responsible for 640 apartments* … the claim is the same relation named differently") and says nothing about the second half. So the sentence's other movement is neither named nor defended.

Also unstated, though arguably inside what the reply does name: *manages* → *is responsible for* is not simply "the same relation named differently". Managing 640 apartments and being responsible for them are different assertions about the company's role, and the standfirst still says *manages*, so the article now says both. The echo could have been broken without touching the relation at all.

### Removals and changed claims, one by one, against the reply

| Change | Reported? | Reported accurately? |
|---|---|---|
| "The team designed the categories itself and" removed | Yes | Yes — names the clause, the finding, and where the claim survives |
| Subheading 2 rewritten (strength, attribution, dropped count) | Yes, at length, as an unresolved finding | Yes — the reply's own analysis matches mine, including that the run created it |
| "manages" → "is responsible for" | Yes | Partly — called "the same relation named differently", which understates it |
| "stored separately" → "filed apart from one reported by email" | **No** | — |
| Four locale corrections | Yes, as a group (*flats*, *working days*, *six staff*, plus the date) | Yes |
| Standfirst/body echo repair | Yes | Yes |

**Verdict: fail on R1** — voice, quotations, bridges, arguments and every limiting sentence were preserved, and the mechanical work is clean, but the run delivered a heading asserting a decline the section refuses to assert, and left one body claim change out of its account.
