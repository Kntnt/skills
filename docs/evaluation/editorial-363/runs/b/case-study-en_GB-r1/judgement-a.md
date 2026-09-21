# Judgement — w-425c88

## 1. Outcome

**Delivered.** Two comparisons ran (`evidence/source-check-1`, `evidence/source-check-2`), each on a separate prose state.

The delivered prose is **identical** to the prose the second checker saw: `diff evidence/source-check-2/prose.md delivered.md` shows only the added `kntnt:` frontmatter block. Nothing was changed after the last comparison.

The reply delivers the draft while declaring three known, unrepaired defects, all in the standfirst, and declines to assert fidelity for them.

## 2. F1 — **Fail**

One real defect, plus two smaller shifts, all in the standfirst; the body is clean.

**Changed attribution (the defect).** Standfirst: "Supervisor Maya Lind says what came of it, **what the figures do and do not show**, and where she would spend more time next time." The material supplies Lind's "complete usable quotations", and none of the three touches the count, the medians or the workloads. The reading of the figures belongs to the note — "the note explicitly does not attribute the difference to the software" — and the material states of her closing remark that "It is not an inference from the figures." The standfirst therefore puts a reading of the measurements in Lind's mouth that the material expressly keeps out of it, and the body confirms the mismatch: the figures section quotes her nowhere. A reader of the standfirst expects a supervisor who interprets the numbers and meets an article in which she never does.

**Modality, smaller.** "…decided on its own to trial a shared repair log **for eight weeks**." The material gives an elapsed duration, "The trial lasted eight weeks", not a term fixed when the decision was taken. The draft's syntax makes eight weeks part of what was decided.

**Scope of "own", smaller.** "and decided **on its own** to trial" renders "its own maintenance team decided to trial". In the material "own" marks the team as the in-house one; in the draft it characterises the manner of the decision as unprompted. The material is silent on whose idea the trial was. This is a mild overreach rather than a plain misstatement — the brief itself insists the customer stay the acting party — but it does assert more than the sentence it renders.

**Checked and clean.** 640 flats; September 2025 attached only to the trial decision, with the supplier choice now in its own undated sentence; "no comparison with another supplier is available" carried with its availability modality; categories the team's and configuration Svale's; six staff, two sessions; telephone reporting kept open; internal note of 4 December 2025, 31 reports, with both exclusions; median **report to assignment** two days against three, never turned into completion time; the workload difference stated in the material's own voice and "explicitly" retained; absences stated as absences of measurements, not as acts of measuring; the reservation ("did not recommend Svale to every housing company") carried and the non-expansion kept with its stated condition; the supplier's third-person narration and the approval statement carried; the link given at the exact URL and described only as a document to read.

**Byline.** "By Thomas Barregren" is a name the material does not supply — the brief says "No author name supplied." It is plainly a run convention rather than a claim about the case (the reply flags it and offers to change it), so I record it without counting it against F1.

## 3. G2 — **Pass**

Headline, standfirst, byline, lead, four sections and an ending, in that order, each doing its own job. The headline states what happened and keeps the two-building scope; the standfirst adds the motive and the promise of the supervisor's account (its content defect is F1's, not G2's); the lead supplies the situation — 640 flats, telephone and email stored separately, the choice of Svale and the absence of a comparison — without repeating the standfirst; the sections separate what the team did, what the note shows, and Lind's appraisal; the ending is a distinct close rather than a restatement.

Account requirements: situation (separate telephone and email records, shifts unable to see each other's work), action (two buildings, own categories, telephone kept open, six staff trained), results (31 reports, the two medians with their workload caveat, the absences), appraisal (all three quotations, with the reservation and the "not to every housing company"). The publisher stance is truthful and in place — "Svale Systems publishes this account and approved its publication; it is not independent journalism." The customer is the acting party throughout: Elm Quay decides, designs, picks, keeps, chooses; Svale configures and trains. The call to action is built from the one supplied offer, at the supplied URL, described as the document to read next and not as a booking or a trial.

## 4. L1 — **Pass**

Idiomatic British English throughout, with no imported phrasing. "Trial" as a verb, "picked two buildings for a trial", "the team kept that route open", "Nor has the trial expanded yet", "is what Elm Quay has to go on", "put another week into preparation next time" are all native constructions, and the sentence rhythm varies rather than marching. The figures section is the test of the register and it passes: "The two periods carried different workloads, and the note explicitly does not attribute the difference to the software" is plain, unhedged reporting that a professional desk would print. Two small blemishes, neither an L1 failure: the comma in "leaves out emergencies, and work ordered before the trial began" is doing no work, and "Eight weeks, two buildings and 31 reports **is** what Elm Quay has to go on" takes a singular verb over a plural list — defensible as a single summed quantity, slightly awkward read aloud.

## 5. Quoted speech

1. **"We wanted the evening shift to see what the morning shift had already done. The categories were ours; Svale helped us put them into the log."** — renders the material's first complete usable quotation, word for word. A British-English reader takes it on one pass; nothing has to be supplied. Meaning, stance and voice are the source's, including the ownership claim "The categories were ours".
2. **"We spent more time agreeing on the categories than entering the first reports. I would set that time aside before the next building starts."** — renders the second supplied quotation, word for word. One pass: yes. The comparative is elliptical ("more time agreeing … than entering"), which is how the language itself does this, and no reader stops at it. Stance and modality intact, "I would" preserved, and the framing "On the preparation, she is specific" keeps her horizon at Elm Quay's next building rather than extending it to other companies.
3. **"I would choose to do the trial again. Having one view of the reports helps us, but I would leave an extra week for preparation."** — renders the third supplied quotation, word for word. One pass: yes. The reservation survives whole, with "but I would leave an extra week" attached where the source attaches it, and the following sentence ("She does not recommend Svale Systems to every housing company") reinforces rather than dilutes it.

**Missing.** None. All three quotations the material offers and permits are used, none is welded to another, and no fourth quotation appears. Only the quotation marks change, to British single marks, which is a locale mechanic.

**One sentence:** Every passage of quoted speech in this draft is speech a British-English reader takes on one pass, with the source's meaning, stance, reservation and voice intact.

## 6. Intermediate

First comparison — nine findings, all accepted and repaired (verified by diffing the two prose states):

| Passage | Allegation | What the writer did | Class |
|---|---|---|---|
| "In September 2025 the team picked two buildings for the trial, and Svale Systems as the supplier" | The date governs both objects; the material dates only the trial decision | Split into two sentences, leaving the supplier choice undated | Supported repair |
| "It states that the two periods carried different workloads" | Attributes to the note a fact the material asserts in its own voice | Restored the material's voice | Supported repair |
| "She has one piece of advice for a housing company planning the same work" | Reframes an internal lesson as advice to other companies, which the material's "did not recommend Svale to every housing company" cuts against | Replaced with "On the preparation, she is specific" | Supported repair |
| Heading "Elm Quay does not credit the software for the difference" | Gives a document's non-attribution as the organisation's stance | Heading now names the note | Supported repair |
| "it does not attribute the difference to the software" | "explicitly" dropped, weakening a load-bearing disclaimer | "explicitly" restored | Supported repair |
| "Nothing was measured about cost…" | Asserts a non-event where the material reports absent measurements | Rewritten as "There are no measurements of…" | Supported repair (minor but right) |
| "the implementation checklist sets out what to prepare before a trial begins" | Describes contents and timing the brief never establishes | Reduced to "the document to read next" | Supported repair; this is the finding the material's own judging section asks for |
| Title "Elm Quay's shifts shared one repair log" | Drops the two-building scope across 640 flats | Retitled "Two Elm Quay buildings shared one repair log" | Supported repair |
| "Maya Lind, who supervises the maintenance team" | Enlarges a supplied job title into a span of responsibility | Replaced with "Elm Quay's maintenance supervisor" | Supported repair |

Second comparison — three findings, all accepted as alleged and none repaired, the reply declaring them and delivering anyway:

| Passage | Allegation | What the writer did | Class |
|---|---|---|---|
| Standfirst: "what the figures do and do not show" | Credits Lind with reading the figures | Reported to the user, prose unchanged | Right finding, accepted but left unrepaired — I reach the same finding independently |
| Standfirst: "decided on its own" | "own" moved from the team onto the manner of the decision | Reported, prose unchanged | Disputed caution, though I agree it asserts a little more than the source |
| Standfirst: "for eight weeks" | Elapsed duration turned into a decided term | Reported, prose unchanged | Disputed caution at the edge of a real finding; I count it as a small modality shift |

No wrong finding was accepted, and no right finding was rejected outright.

**Did any real defect escape every checker?** No. Everything I found under F1 or under point 4 was raised by one of the two comparisons. The second comparison's three findings are, if anything, a superset of what I would have raised on my own.

## 7. Stop or delivery

**A valid delivery, though not a clean one.** The draft is fit to hand over: the body is faithful line by line, the reservation survives, the forbidden inferences are all avoided, and the one real defect is confined to a summary line that any editor can fix in a single stroke. The reply does not launder it — it names the passage, quotes the supplied sentences that contradict it, proposes the smallest repair, and states plainly that it asserts no fidelity for those three passages. A reader of the reply cannot publish the standfirst unknowingly.

What keeps this from being a clean delivery is that the defect is real and the run knew it. The standfirst was rewritten between comparisons — the first version's "Supervisor Maya Lind explains how the eight-week trial went" carried no such claim — so the second comparison caught a defect the repair round had introduced, and the run then had no round left to spend on it. Delivering with a declared, correctly diagnosed defect is the right call over stopping on a two-word standfirst error; introducing it in the first place is the run's cost.
