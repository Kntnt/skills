# Judgement — `case-study-en_US-r2` (run b)

Judged from `work/source.md`, `response.md`, `delivered.md` and every file under `evidence/`. No other file was read. Both checkers' approvals and the writer's own dispositions are treated as arguments, not as evidence.

---

## 1. Outcome

- **Delivered.** `delivered.md` carries the draft, and `response.md` repeats it inline with a disclosure that one source-check finding remains unrepaired.
- **Two comparisons ran.** `evidence/source-check/report-1.md` against `draft-under-check.md`, `report-2.md` against `draft-under-check-2.md`. The second is the run's ceiling.
- **The delivered prose is identical to the last prose a checker saw.** `draft-under-check-2.md` and the body of `delivered.md` differ only by `delivered.md`'s YAML frontmatter and a leading blank line; every sentence is byte-identical. The response states this as the reason the last finding was not repaired.

---

## 2. F1 — source support

**Verdict: fail, narrowly, on one conceded attribution defect.** Everything else in the draft — every figure, date, name, exclusion, caveat, causal abstention and the customer's reservation — is exact. I list the one defect, then the three lesser items I tested and their disposition, then what the draft gets right, because the balance matters to anyone reading this verdict as a score.

### The defect

**Lead: "The team's internal note on the eight-week trial counts 31 reports".**
The material names the note once and names it as the company's: "Elm Quay's internal trial note, 4 December 2025, says that 31 repair reports were entered." It never says who wrote, compiled or kept it. The draft's possessive makes it the maintenance team's own document. A case fully compatible with the material defeats it: Elm Quay's administration compiles the trial note from the team's records, and the team neither authored nor owned it — the source sentence holds and the draft's fails. This is the sentence carrying the trial's one headline figure, so the attribution decides whose count the reader is being handed. The draft itself uses the supported form nine lines later ("Elm Quay's internal trial note of 4 December 2025 records 31 repair reports"), which is the repair: one possessive. The run identified this defect, agreed with it, and shipped it anyway (see §7).

A softer instance of the same possessive stands in the standfirst — "what its trial note counted" — where "its" most nearly picks up "Elm Quay Housing" from the same sentence's subject and is defensible as written.

### Tested and not counted as defects

- **"What it has so far is one shared view of its repairs"** (ending). Read alone, "its repairs" could be taken to cover a company of 640 flats, which the trial does not: the trial ran in two buildings, has not expanded, and telephone and email reporting elsewhere is untouched. Read in place, the clause sits in the same sentence as "Elm Quay's trial has not expanded yet", and the headline, standfirst and lead all fix the scope at two buildings. Loose, and the looseness is real — the checker offered "one shared view of the repairs in those two buildings" and the writer declined it — but context governs the reading, so I do not count it as an unsupported claim.
- **"By Thomas Barregren".** The brief says "No author name supplied." A byline is an attribution, and this name is not in the material; it comes from the invocation. Both checkers set it aside on that ground, and the response discloses it and tells the user to correct it before publication. I record it as an attribution sourced outside the material rather than as a fabrication, and do not fail F1 on it — but the reader of the delivered file alone is given an author the brief did not give.
- **"The next document to read is Svale Systems' implementation checklist"** and the heading "Read the implementation checklist before you start". The brief calls it "The optional next step … a document to read, not a consultation booking or a product trial." The draft describes the destination exactly right and promises no booking and no trial; "optional" governs whether the reader takes the step, which a call to action does not have to restate. Supported, and the URL is character-for-character the supplied one.
- **"The trial produced no cost figures, no resident-satisfaction measurements and no completion times"** against "There are no cost, resident-satisfaction or completion-time measurements." The draft localises a flat absence to the trial, which is weaker than and entailed by the material's statement. Supported; the absence stays an absence and nothing is inferred from it.
- **"The team designed the categories itself"** against "The maintenance team designed its categories." The emphatic "itself" excludes a co-designer; the only other party in the material is Svale, whose supplied role is to configure the log and to "put them into the log", which the draft reports separately, and Lind's "The categories were ours" settles it. Supported.
- **"stored telephone repair reports and emails separately"** for "telephone reports and emails were stored separately." The active voice names Elm Quay as the storer and reads "telephone reports" as telephone *repair* reports; nothing in this material could be a telephone report of a repair and not a telephone report here, and no third party stores Elm Quay's incoming reports. Supported in both directions.

### What the draft gets right, and it is the hard part of this brief

Every forbidden inference is refused. The two-versus-three working days appears with no causal verb and no causal hedge, with the confounder stated in the material's own voice ("The two periods carried different workloads") and the note's abstention quoted as abstention ("the note explicitly does not attribute the difference to the software"). "Assignment is not completion" blocks the assignment-to-completion slide outright. No money saved, no delighted residents, no rescued customer. The count of 31 carries both exclusions where it is given in the body, and carries no evaluative characterisation — not high, not low, not modest — which the Claims section requires absent a supplied comparison. "No comparison with another supplier is available" is reproduced with its modality intact: unavailable, not "none was made". Unknown is kept apart from absent throughout.

---

## 3. G2 — required parts, distinct jobs

**Verdict: pass, with one real weakness.**

Parts and order: headline ("Elm Quay gave two buildings one repair log"), standfirst, byline, lead, four sections, ending — in that order, each present.

Customer-account requirements:

- **Situation.** 640 flats; telephone reports and emails stored separately; staff on different shifts unable to see the same information.
- **Action.** The team decided to trial, tested whether the log could show each repair's status, chose Svale, designed its own categories, kept telephone reporting open, ran eight weeks in two buildings.
- **Results.** 31 reports with exclusions; median two versus three working days with the workload confounder and the non-attribution; the three absences named.
- **Appraisal.** Lind's qualified verdict, with the reservation carried in the heading, in the framing and in the quotation's own "but".
- **The customer is the acting party.** Elm Quay or its team is the grammatical subject of almost every sentence; Svale appears only as the thing chosen, the party that configured and trained, and the owner of the checklist.
- **Call to action built from a supplied route.** The checklist URL, described as what the brief says it is.
- **Publisher stance.** Truthful in the negative sense: nothing claims independence, the supplier is narrated in the third person throughout, and the Svale-owned checklist signals whose page this is. But the material states plainly that this is "supplier-published material; it is not independent journalism", and the delivered text discloses that nowhere. A reader meeting the file on its own reads a journalistic case with a named byline and no indication that the supplier published it. No checker tested this.

**The weakness — distinct jobs.** Three openings cover the same ground. The standfirst opens "Elm Quay Housing manages 640 flats and stored telephone repair reports and emails separately"; the first body sentence of section 1 opens "Elm Quay Housing manages 640 flats, and telephone reports and emails had been stored separately" — the same two facts in nearly the same words, 120 words apart. The standfirst then promises "what its trial note counted and what its supervisor would change" and the lead answers with "counts 31 reports, and its supervisor's verdict is qualified", which is a legitimate summary-lead move but leaves the two parts close together in effect. Reader effect: the piece takes three runs at its own setup before it starts, and in roughly 450 words that is a visible tax. Each part still performs its job — the standfirst orients, the lead dates and motivates, section 1 delivers the supplier choice and the no-comparison caveat — so this is a craft defect inside a passing structure, not a part failing its job.

---

## 4. L1 — professional prose in the resolved language

**Verdict: fail, narrowly, on lexis; syntax and register are otherwise professional.**

The resolved composition guidance in the evidence opens: "Use natural American vocabulary and syntax." The narration does not.

- **"manages 640 flats"**, twice (standfirst and section 1). *Flat* is the British lexeme; an American writer addressing American operations managers writes *apartments* or *units*. It is the source's word, but nothing in the brief requires keeping it, and keeping it is the choice that shows.
- **"trained six staff in two sessions."** *Six staff* as a bare count noun is British; American English wants *six staff members* or *six employees*. A US reader stumbles on the number-noun pair.
- **"two working days"** and "three in the preceding eight-week period". US business prose says *business days*. This one sits inside a measured figure, so it is the most defensible of the three, and still reads as imported.

Set against that, the guidance's own tests are passed: collective nouns take singular agreement throughout ("It wanted staff on different shifts…", "the team will decide"), the simple past is used where American prose uses it, and no British plural agreement appears anywhere. The date form "4 December 2025" is non-American, and the straight quotation marks against the source's curly ones are likewise mechanical — I record both as locale mechanics and exclude them from this verdict, as instructed.

One construction is strained in any English: **"Maya Lind, the maintenance supervisor, puts the aim beside the division of work:"** — *put X beside Y* is not an idiomatic speech frame, and the sentence reads as an editor reaching for a way to say "this quotation does two things at once". Reader effect: a small snag at the draft's first quotation, exactly where the prose should be at its most transparent.

Elsewhere the writing is good and unmistakably deliberate: "Assignment is not completion." is the best sentence in the piece, four words doing the work of a paragraph of hedging, and "Her verdict is qualified, and she does not extend it to every housing company." carries a reservation without fussing over it. The fail is on vocabulary against a stated locale, not on competence.

---

## 5. Bridges into quotations

Three quotations, in order.

**Q1.** Bridge: *"Maya Lind, the maintenance supervisor, puts the aim beside the division of work:"* → *"We wanted the evening shift to see what the morning shift had already done. The categories were ours; Svale helped us put them into the log."*
**Class (b).** The words that put it there are the attribution — "Maya Lind, the maintenance supervisor" — and the two bare topic labels, "the aim" and "the division of work". Second reading, and it is close: (a), on the ground that naming the quotation's two halves in order tells the reader the shape of what is coming, so the quotation arrives pre-announced. I chose (b) because the bridge delivers neither content — it does not say what the aim was (that the evening shift should see the morning shift's work) and does not say how the work divided (the categories theirs, the entering Svale's help) — so the reader who has read the bridge still learns both facts from the quotation. Labelling a subject is not delivering it.

**Q2.** Bridge: *"Lind's account returns to the categories."* → *"We spent more time agreeing on the categories than entering the first reports. I would set that time aside before the next building starts."*
**Class (b).** "returns to the categories" names the subject and nothing else. The quotation's actual freight — that agreeing the categories cost more time than entering the first reports, and that she would budget that time next time — is nowhere in the bridge. No second reading; this one is clean.

**Q3.** Bridge: *"Her verdict is qualified, and she does not extend it to every housing company."* → *"I would choose to do the trial again. Having one view of the reports helps us, but I would leave an extra week for preparation."*
**Class (c).** The words that put it there: "she does not extend it to every housing company", a fact the quotation does not carry — the quotation speaks only about Elm Quay's own trial and says nothing about other companies. The fact comes from the material's narration, "Lind did not recommend Svale to every housing company", so it is the bridge's job to supply it and no other sentence does. Second reading: (a) for the first clause alone, since "Her verdict is qualified" pre-labels the qualification that the quotation's "but" then delivers. I chose (c) because the clause labels the verdict's shape without giving its content (that she would do it again; that the missing thing is a week of preparation), and because the second clause independently adds what the quotation lacks.

**Counts:** (a) 0, (b) 2, (c) 1. No quotation stands without a bridge.

**Interviewer:** the draft attributes no question and no utterance to an interviewer, and puts nothing in an interviewer's mouth. The material supplies the quotations as answers from an email interview, and the draft never stages a question, a scene or an exchange — consistent with "All interviews occurred by email, and no physical scene, emotion or remembered dialogue is provided."

**Unsupported bridge assertions:** none. The one bridge that asserts a fact of its own, "she does not extend it to every housing company", rests on "Lind did not recommend Svale to every housing company." The draft shifts tense (past report to standing position) and object (recommending Svale to extending her verdict); the material's own characterisation of the final quotation as "her actual, qualified assessment" and its "helps **us**" carry that limit, so the shift changes no claim. "Lind's account returns to the categories" and "puts the aim beside the division of work" assert only what the quotations they introduce show.

---

## 6. Quoted speech

**All three supplied quotations appear, and all three are verbatim.** I compared them character for character against the "complete usable quotations" list:

| # | Status |
|---|---|
| "We wanted the evening shift to see what the morning shift had already done. The categories were ours; Svale helped us put them into the log." | Identical, including the semicolon and the hedge "helped us". |
| "We spent more time agreeing on the categories than entering the first reports. I would set that time aside before the next building starts." | Identical, including the comparative and the conditional. |
| "I would choose to do the trial again. Having one view of the reports helps us, but I would leave an extra week for preparation." | Identical, including the pivot "but" and the present-tense "helps us". |

- **Meaning, stance, certainty, reservation, voice:** unmoved. No fragment welded to another, none split, none smoothed into the article's register, no hedge added or removed. Source and target language are both English, so nothing was translated and no translation question arises.
- **Missing quotations:** none. The material offers three and permits them; the draft uses all three.
- **Quote approval:** the draft neither claims approval nor treats its absence as solved, which is what the quotation guidance requires.
- **Do the quotations earn their place?** Yes, and this is the brief's explicit test. Each carries experience the narration cannot: the shift-handover motive in the speaker's own terms; the unexpected discovery that agreeing categories cost more than entering reports; and the qualified verdict with its reservation, which the material insists is "her actual, qualified assessment … not an inference from the figures" and which the draft therefore does not derive from the two-versus-three days.

---

## 7. Intermediate — every checker finding and its fate

| # | Passage | Allegation | What the writer did | My class |
|---|---|---|---|---|
| R1-F1 | Lead, draft 1: "The eight-week trial produced 31 logged reports and a qualified verdict from its supervisor." | The count of 31 is given without the exclusions that define it, and the filtered figure is stated as the trial's output. | Rewrote the sentence, not with the proposed repair ("…, excluding emergencies, …") but by attributing the count to the note: "The team's internal note on the eight-week trial counts 31 reports, and its supervisor's verdict is qualified." | **Supported repair.** The finding is right — telephone reporting stayed open, so emergencies could be logged and excluded, and the log could hold more than 31 entries. The chosen repair removes the defect by a different and legitimate route (the note's count is the note's), but it introduced R2-F1 below. |
| R1-F2 | "The note says the two periods carried different workloads and explicitly does not attribute the difference to the software." | The material asserts the workload difference in its own voice and attributes only the non-attribution to the note; the draft puts both inside the note's mouth. | Applied the proposed repair exactly: "The two periods carried different workloads, and the note explicitly does not attribute the difference to the software." | **Supported repair.** The finding is right and the repair is the material's own wording. |
| R2-F1 | Lead: "The team's internal note on the eight-week trial counts 31 reports". | The note is the material's "Elm Quay's", never the team's; authorship is unsettled. Repair: "Elm Quay's internal note…". | Rejected. Delivered unchanged, with the finding and the proposed repair written out in `response.md`. | **Right finding rejected.** See §2 — I reach the same conclusion independently. |
| R2-EQ1 | Ending: "one shared view of its repairs". | Reported as an editorial question, not a defect: could be read as covering all 640 flats. Optional repair offered. | Left as written; disclosed in `response.md` with the offered wording. | **Disputed caution, correctly disposed of.** The checker was right to report it as a question and right not to demand a repair; the writer was entitled to keep the contextual reading. |

Also recorded by checker 1 as considered and set aside, and I agree with each: "The next document to read" against "optional next step"; "puts the aim"/"Lind's account" against the email-only interviews; "telephone repair reports" for "telephone reports".

**Did a real defect escape both checkers?** Not under F1 and not under §5 — the one attribution defect I found is R2-F1, which checker 2 found and stated precisely. Two things were seen and deliberately excluded rather than missed: the byline (both checkers declined it as invocation-derived) and the scope of "its repairs" (raised as EQ1). **One thing was tested by neither:** whether the delivered text discloses that this is supplier-published material and not independent journalism, which the material states outright. Checker 2 tested only that supplier narration stays third-person. That is a gap in the checking, not in the prose's accuracy.

---

## 8. Stop or delivery

**A valid delivery, and a marginal one.**

The draft is accurate on everything that matters in this brief — the causal abstention, the assignment-versus-completion distinction, the exclusions on the count, the three absences, the customer as acting party, the supplier in the third person, the link honestly described, and three verbatim quotations that each carry experience the narration cannot. Nothing in it misleads a reader about what the trial showed. Delivery was the right call.

The reason given for shipping the known defect is weaker than the delivery it defends. `response.md` says: "The prose is delivered exactly as the final comparison read it, so the repair is not applied here." Never shipping prose no checker has read is a defensible policy, but the repair in question is the substitution of "Elm Quay's" for "The team's" in a sentence whose every other word a checker had already cleared, and it replaces the possessive with the one the draft itself uses, correctly, nine lines later. Treating that as unverifiable spends the run's honesty budget to protect a rule that was not at risk. The disclosure in `response.md` is full and precise, which is what keeps this on the right side of the line: the user is told the defect, the exact passage and the exact repair, and can apply it in one edit.

**Summary:** delivered; F1 fail (one attribution, conceded and disclosed); G2 pass with a redundancy weakness and an undisclosed publisher stance; L1 fail on British lexis in an en_US text; bridges (a) 0, (b) 2, (c) 1; two comparisons, delivered prose identical to what the second read.
