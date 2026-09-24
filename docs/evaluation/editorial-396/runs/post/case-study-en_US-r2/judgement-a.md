# Judgement: run d71ce57c

## 1. Outcome

- The run **delivered** a draft.
- **Two comparisons** ran, according to the reply: the first found four problems, all repaired, and the second (final) raised one headline finding, which the writer left for the user to decide.
- **Is the delivered prose identical to the last prose a checker saw? Yes, as far as the reply shows.** The reply reports no change after the final check, and `delivered.md` matches the draft embedded in `response.md` word for word. There is no `evidence/` directory, so this cannot be confirmed from the drafts themselves.

## 2. F1: **fail** (narrowly; one clear defect and one borderline point)

- **Unsupported attribution, the byline "By Thomas Barregren" (line 12).** The brief states "No author name supplied". The draft credits the piece to a named person who does not appear anywhere in the material. This is the only clear F1 defect. The reply discloses it ("the byline uses your name … Change it if…"), but the delivered text still carries it. The source did support another byline, "Svale Systems" as publisher, or the piece could have gone unsigned. On supplier-published material, a personal byline also tilts the piece towards looking like independent reporting, which the source explicitly says it is not.
- **Borderline certainty shift, the headline "Elm Quay trial gives shifts one repair view".**
  - What the source supports: the goal ("The team wanted staff on different shifts to see the same information") and Lind's own qualified appraisal ("Having one view of the reports helps us, but …").
  - What the headline changes: it moves "one view" from Lind's attributed judgement into the publisher's unattributed voice, as a result achieved for the shifts. It also drops the two-building scope, although the word "trial" signals that the scope was limited.
  - Why it is not a clear defect: "one view" is Lind's own phrase, and a shared log does by definition give one view. It is a slight move in certainty, not an invented result.
- **Clean elsewhere.** Each of these matches the source:
  - the 640 flats, and the separate storage before the trial
  - the September 2025 decision, the two buildings, and the choice after the status test
  - the six staff trained in two sessions, and telephone reporting kept open for residents
  - the eight weeks, and the note of 4 December 2025 (written in US form)
  - 31 reports, with emergencies and work ordered before the trial excluded
  - a median of 2 vs 3 working days, with the different workloads and the note's explicit non-attribution kept
  - "assignment, not completion", and no cost, satisfaction or completion measurements
  - "did not recommend Svale to every housing company"
  - no expansion yet, with the decision waiting on how the categories work for larger repairs

  Nothing says the software caused the shorter time, saved money, pleased residents or rescued the customer. Assignment time is never turned into completion time.
- **The acting party is kept.** The customer stays the actor: the team decided, chose, designed its categories, kept phone reporting open, and will decide on expansion. Svale is only configurer and trainer, in third person.
- **The call to action describes its destination correctly.** "start by reading the implementation checklist" presents it as a document to read, not a booking or a trial.
- **Terms checked in both directions:**
  - "quicker assignment" (subheading) = the shorter median to assignment. It is not completion.
  - "from Svale Systems" (standfirst) is supported by the choice of supplier.
  - "flats" is kept from the source. It is faithful, though British in an en_US text. That is a locale-vocabulary matter, not F1.
- **Unknown kept apart from absent.** The dropped line "No comparison with another supplier is available" is harmless, because the draft implies no comparison.

## 3. G2 and L1

**G2: pass, with a weakness.**

- **Order.** Headline, standfirst, byline, lead, four sections and an ending come in the required order.
- **Each part does its own job:**
  - The standfirst addresses operations managers and promises preparation, the note's limits and Lind's qualified verdict. It does foreshadow the third quotation's conclusion ("would run the trial again with more time for preparation"), which is acceptable at standfirst distance.
  - The lead sets the situation: 640 flats, the separate reports, the September 2025 decision.
  - The sections cover the motive, the setup, the result with its caveats, and the appraisal.
  - The ending is the open decision plus the checklist call to action, built from the supplied link.
- **Customer-account requirements are met:** the customer's situation, action, results and appraisal are all there, and the customer stays the acting party.
- **Weakness, the publisher stance.** It is silent rather than untrue. Nothing claims independence, but nothing says the piece is supplier-published either. Together with the personal byline, a reader could take it for independent journalism. The reply leaves the label to the user.

**L1: pass.**

- **The prose is idiomatic, plain professional English**, e.g. "Answering questions by email, Lind describes the starting point", "These figures concern assignment, not completion."
- **Minor points:**
  - "How that went is recorded in an internal trial note and described by …" is slightly stiff.
  - "Any expansion waits on larger repairs" is compressed. It can be read as waiting for larger repairs to happen, rather than for a check of how the categories handle them.
  - "flats" in en_US is a locale-vocabulary point, not L1.

## 4. Bridges into quotations

1. **Bridge:** "Answering questions by email, Lind describes the starting point:"
   **Quotation:** "We wanted the evening shift to see what the morning shift had already done. The categories were ours; Svale helped us put them into the log."
   **Class (b).** The words that put it there are "Answering questions by email" (the occasion) and "describes the starting point" (the subject).
   *Alternative reading:* the email detail is a fact the quotation does not carry, which would make it (c). I chose (b) because the brief lists the occasion under (b).
2. **Bridge:** "Lind describes the setup from the team's side:"
   **Quotation:** "We spent more time agreeing on the categories than entering the first reports. I would set that time aside before the next building starts."
   **Class (b).** The words are "describes the setup" (the subject) and "from the team's side" (the angle, as opposed to Svale's configuration). The bridge states nothing of what the quotation delivers.
3. **Bridge:** "Of the trial itself, she writes:"
   **Quotation:** "I would choose to do the trial again. Having one view of the reports helps us, but I would leave an extra week for preparation."
   **Class (b).** The words are "Of the trial itself" (the subject) and "she writes" (the attribution and medium).
   *Alternative reading:* if the preceding sentence, "Lind did not recommend Svale to every housing company.", is read as part of the bridge (the word "itself" leans on it), the bridge carries a fact the quotation does not, which would make it (c). I chose (b) because the bridge is defined as the sentence immediately before the quotation.

No quotation stands without a bridge.

- **Counts:** (a) 0, (b) 3, (c) 0.
- **Interviewer:** the draft puts no question or utterance in an interviewer's mouth. "Answering questions by email" quotes no question and is supported by "All interviews occurred by email".
- **Unsupported bridge assertions:** none.

## 4b. Subheadings over quotations

1. **Subheading:** "Why Elm Quay wanted one log"
   **Quotation:** "We wanted the evening shift to see what the morning shift had already done. The categories were ours; Svale helped us put them into the log."
   **Prepares.** "Why … wanted" names the subject, the motive, without stating it; the handover between shifts is left to the quotation.
   *Alternative reading:* "wanted one log" echoes "We wanted", which would make it pre-echo. I rejected that because the quotation's point is what the shifts should see, which the heading does not say.
2. **Subheading:** "What the setup demanded"
   **Quotation:** "We spent more time agreeing on the categories than entering the first reports. I would set that time aside before the next building starts."
   **Prepares.** "What … demanded" names the subject and hints at effort, but not the point (categories took longer than the first entries).
3. **Subheading:** "Maya Lind looks back on the trial"
   **Quotation:** "I would choose to do the trial again. Having one view of the reports helps us, but I would leave an extra week for preparation."
   **Prepares.** The heading names the speaker and the occasion ("looks back"), not her verdict.

**Counts:** pre-echo 0, prepares 3, neutral 0.

## 5. Quoted speech

- **All three quotations are verbatim.** Meaning, stance, certainty, the reservation ("but I would leave an extra week for preparation"; "I would set that time aside") and Lind's own voice are unchanged.
- **Nothing that surrounds a quotation overstates it.** The one exception is the headline point under F1, which is not placed next to any quotation.
- **Each quotation adds experience beyond the narration.** There is a small overlap, where "Svale configured the log" repeats the substance of "Svale helped us put them into the log" in the next section.
- **No quotation is missing.** The material offers three and the draft uses all three.

## 6. Intermediate

No report files exist, so every line is judged from the reply's description and the delivered text. The original wording of the first-check passages is not visible.

- **Headline, second (final) check.**
  - *Allegation:* it states the shift-sharing goal as a result achieved, and drops the two-building scope.
  - *What the writer did:* not repaired; left for the user, with the checker's proposed repair quoted.
  - *My class:* **disputed caution.** The finding has some merit (a certainty shift from Lind's attributed view to an unattributed claim), but "one view" is Lind's own wording.
- **A subheading claiming the note declined to credit the software in general, first check.**
  - *What the writer did:* repaired to "…for quicker assignment".
  - *My class:* **supported repair.** The note only declines to attribute the difference.
- **"With one change", first check.**
  - *Allegation:* it implies Lind would change only one thing.
  - *What the writer did:* removed it.
  - *My class:* **supported repair.** The source does not limit her to one change, and she also says to set the categorising time aside.
- **The lead-in to the second quotation, first check.**
  - *Allegation:* it implied how the preparation time was divided.
  - *What the writer did:* rewritten as "Lind describes the setup from the team's side:".
  - *My class:* **supported repair.**
- **"Elm Quay's maintenance supervisor", first check.**
  - *Allegation:* it implies she is the only one.
  - *What the writer did:* changed to "Elm Quay maintenance supervisor".
  - *My class:* **supported repair.** The source gives only "maintenance supervisor Maya Lind".

**A real defect that no checker saw:** yes, the invented byline "By Thomas Barregren". It is the only clear F1 defect. The writer mentions it in the reply, but no checker finding raised it and it was not repaired. The silence about supplier publication was also raised only by the writer, not by a checker. No point-4 defect exists.

## 7. Stop or delivery

**Valid delivery.** The draft is faithful on every substantive point. The forbidden inferences are avoided, the customer's reservation survives and the call to action is accurate. The two remaining issues do not warrant a stop:

- **The byline:** disclosed to the user, and a one-line fix.
- **The borderline headline:** disclosed as a disputed caution.

The byline should nonetheless have been repaired before delivery, either to "Svale Systems" or to no byline, rather than handed to the user. That is the reason F1 fails.
