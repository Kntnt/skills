# Validation result — v-truncated-r3

Fixture: `/Users/thomas/Projects/skills/.git/kntnt-orchestrate/378.scratch/stage/fixture/p2-chronology.md`
Report under validation: checker `c-r1`, carried as the checker's reply text because the report directory `.../stage/reports` is mode `dr-xr-xr-x` and the write failed. I was scoped to write only this result path, so I did not create the report file and did not change the staged tree's permissions; the reply text is the report in full and was validated as such. Route does not settle a comparison: the report ends with its findings, their status and its unresolved editorial questions, and its accounting runs to the draft's last sentence, so it is a complete report by the reply route.
Resolved language of the draft: en_US. Source language English, so no translation is in play; the three quotations are reproduced verbatim, not translated, and no translation finding arises.

## 1. Accounting validated

Coverage: complete. Every prose passage of the complete draft — title, all three summary sentences, the publisher line, the six body paragraphs, all three block quotations and the closing link — appears in the report's §1 tables paired with the supplied passage it rests on, and each pairing states what differs. Spot-checked the pairings that carry a qualification, and each survives: the exclusions stay attached to "31 repair reports"; "different workloads" and the note's non-attribution stay in the same sentence as the two-versus-three medians; the reservation stays inside Lind's final quotation; the absence of cost, satisfaction and completion measurement is carried whole.

Detected accounting mismatches:

1. **Unaccounted draft block (immaterial).** The draft's YAML frontmatter (`kntnt: genre: case-study / technique: none / language: en_US`) appears in no row. It is processing metadata carrying no claim about Elm Quay or Svale, so the gap changes no disposition; recorded only so the coverage judgment is visible.
2. **No other mismatch.** No row pairs a draft passage with a source passage it does not rest on, and no row drops a qualification the draft carries. The report's separation of translation from source support is correct for an English source and an en_US draft, and its §3 records five judgment calls rather than burying them; each is defensible on the supplied text.

## 2. Findings — dispositions

### Finding 1 — the September date is stretched over the choice of supplier. ACCEPTED.

- Draft, exactly: "In September 2025, its maintenance team decided to try a shared log and chose Svale Systems after testing whether it could show the status of each repair."
- Source, exactly: "In September 2025 its own maintenance team decided to trial a shared repair log in two buildings." and, in a separate undated sentence, "It chose Svale Systems after testing whether the log could show the status of each repair."
- Why accepted: the fronted adverbial "In September 2025" governs both conjoined predicates of the draft's single sentence, so in its actual contextual meaning the draft asserts that the supplier was chosen in September 2025, and with it the test the choice followed. The material dates the decision only, and the order it gives — decision, then a test, then a choice — leaves the test and the choice free to fall later; nothing supplied places either in September. This is a changed claim, not a stronger reading of the same one: the material stays wholly true if the team decides in late September, tests through October and chooses in November, while the draft is then false. The report established the allegation with the source's own sentence boundary as evidence.

### Finding 2 — "it" read as referring to Svale Systems. REJECTED.

- Draft, exactly: "…decided to try a shared log and chose Svale Systems after testing whether it could show the status of each repair."
- Source, exactly: "It chose Svale Systems after testing whether the log could show the status of each repair."
- Why rejected: what the draft asserts in full context is the supported claim. The predicate "could show the status of each repair" is the log's — it is what the material has the log do, and what the same sentence has just introduced as the thing being tried ("decided to try a shared log"). A supplier company is not what shows the status of each repair, so the supplier antecedent is a conceivable parse rather than the contextual meaning, and a merely conceivable reading establishes no defect. The report does not show otherwise: it argues only from linear proximity and then concedes that "with 'it' resolving back past 'Svale Systems' to 'a shared log', the draft says what the material says." Note also that the material itself opens that sentence with an unwritten-out pronoun ("It chose Svale Systems", where "It" is Elm Quay Housing), so the draft's pronoun use is of a kind the source supports. This is the writer's evidenced decision, not the checker's approval. The repair accepted under Finding 1 rewrites the sentence and writes the antecedent out in passing, which is incidental to this rejection.

Other judgments checked and left as the report left them: the present-to-past tense shifts ("does not attribute" → "did not attribute"; "There are no … measurements" → "There were no measurements") change no claim in a past-tense account of a finished trial; "compared with" juxtaposes the two medians without asserting cause, with the workload qualification in the next sentence; "gave the team a common view" is supported by Lind's "Having one view of the reports helps us"; the link text names a checklist to read and not a booking or a trial.

## 3. Delivery

**This draft is delivered with a known defect.** One finding remains, alleged by the comparison and left for the editor to settle; no fidelity is asserted for the passage it names. The prose below is delivered exactly as the final comparison read it, unrepaired.

### Remaining finding

- **Draft passage:** "In September 2025, its maintenance team decided to try a shared log and chose Svale Systems after testing whether it could show the status of each repair."
- **The problem:** the fronted date governs both conjoined predicates, so the sentence dates the choice of supplier — and the test preceding it — to September 2025.
- **What the supplied material carries instead:** "In September 2025 its own maintenance team decided to trial a shared repair log in two buildings." The choice stands in its own undated sentence: "It chose Svale Systems after testing whether the log could show the status of each repair."
- **Smallest repair the checker proposed:** "In September 2025, its maintenance team decided to try a shared log. It chose Svale Systems after testing whether the log could show the status of each repair."

### The draft, as read

---
kntnt:
  genre: case-study
  technique: none
  language: en_US
---

# Elm Quay gains a shared view of repair reports

Elm Quay Housing’s maintenance team tested a shared repair log in two buildings to help staff on different shifts see the same information. The eight-week trial gave the team a common view of reports, but its supervisor would allow more preparation time before starting again. Expansion remains undecided.

*Published by Svale Systems.*

Elm Quay manages 640 apartments. Before the trial, telephone reports and emails were stored separately. In September 2025, its maintenance team decided to try a shared log and chose Svale Systems after testing whether it could show the status of each repair.

In an email interview, maintenance supervisor Maya Lind described what the team wanted:

“We wanted the evening shift to see what the morning shift had already done. The categories were ours; Svale helped us put them into the log.”

The team designed the categories and kept telephone reporting open for residents. Svale configured the log and trained six staff members over two sessions. For Lind, preparing the categories was work worth planning for:

“We spent more time agreeing on the categories than entering the first reports. I would set that time aside before the next building starts.”

Elm Quay’s internal trial note, dated December 4, 2025, recorded 31 repair reports, excluding emergencies and work ordered before the trial. Median time from report to assignment was two working days during the trial, compared with three in the preceding eight-week period.

The periods had different workloads, and the note explicitly did not attribute the difference to the software. These figures concern assignment, not repair completion. There were no measurements of costs, resident satisfaction, or completion times.

Lind’s assessment of the experience came with a reservation:

“I would choose to do the trial again. Having one view of the reports helps us, but I would leave an extra week for preparation.”

That assessment was specific to the trial; Lind did not recommend Svale to every housing company. The team has not yet expanded the trial. It will decide after checking how the categories work for larger repairs.

For operations managers considering their own implementation, Svale provides an [implementation checklist to read](https://example.invalid/svale/checklist).

COMPARISON: complete
DRAFT: accepted defect — "In September 2025, its maintenance team decided to try a shared log and chose Svale Systems after testing whether it could show the status of each repair."
