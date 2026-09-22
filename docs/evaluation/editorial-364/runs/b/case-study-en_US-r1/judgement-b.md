# Judgement — `case-study-en_US-r1` (run b)

## 1. Outcome

**Delivered.** The draft was returned in full in `response.md` and is preserved at `delivered.md`.

**Two comparisons ran.** `evidence/source-check/report-1.md` raised five source-support findings; `evidence/source-check/report-2.md` read the repaired prose and returned none.

**Delivered prose is identical to the last prose a checker saw.** `evidence/source-check/draft-prose.md` and the prose body of `delivered.md` differ by nothing but a leading blank line (the frontmatter block is not prose). The repairs from report 1 were therefore all made *before* comparison 2, and nothing was touched after it. The prose inside the fenced block in `response.md` is also byte-identical to `delivered.md`.

Length: 452 words of prose against a brief asking for "approximately 400 words, as material allows" — 13% over, and the reply names the overrun. Not a criterion here, but worth recording.

---

## 2. F1 — source support

**Verdict: fail**, on one item only. Every claim the draft makes *about its subject matter* is supported at the material's own strength, scope, time and attribution — I could not break a single one. The failure is an attribution the draft adds about itself.

### The defect

**The byline is invented.** The draft carries `By Thomas Barregren`. The brief says, in terms: "**No author name supplied.**" That is not silence the draft may fill — it is a supplied statement that no author is available, and the draft answers it by naming a real, identifiable person as the author of a piece the same draft declares is published and approved by Svale Systems. A byline is an attribution, and this one does not stand in the material; a reader takes from it that a named individual wrote supplier-approved promotional material, which no supplied passage supports and one supplied passage contradicts.

Two mitigations, neither of which removes it: the reply flags the byline explicitly and offers to change it ("If the piece is to run unsigned, under Svale Systems' own name or under a staff writer's, change that line before publication"), and both checkers were told, or assumed, that the byline came from the invocation rather than the material and excluded it from the comparison by instruction (report 1: "is therefore not assessed"; report 2: "excluded from this comparison per the task instruction"). The delivered artifact still carries it.

### Everything else: supported

Checked in both directions, term by term:

- **"640 apartments"** for the material's "640 flats" — in this context nothing could be one and not the other; a dwelling in a housing company's managed stock is both. Clean cross-variety rendering, outside quoted speech.
- **"December 4, 2025"** for "4 December 2025" — same date, en_US form. Locale mechanics, not a claim change.
- **"hold up for larger repairs"** for "work for larger repairs" — "hold up" adds a faint connotation of strain that "work" lacks, but both name the same pending test of the categories against larger repairs; nothing could satisfy one and not the other here.
- **Chronology and modality**: September 2025 start, eight-week trial, note of 4 December 2025, expansion still undecided — all preserved. Every conditional stays conditional ("would plan", "would repeat", "will decide once it has checked"). "Whether the log moves beyond the two buildings is still open" keeps *undecided* as undecided.
- **Causal limits**: the draft never asserts, hedges or implies that the software shortened assignment time. The two medians stand side by side; the differing workloads are stated; the note's non-attribution is stated *and* promoted into a heading ("The note measures assignment time, not the software's effect"). Assignment time is never converted into completion time — "report to assignment" is named as such, and completion time appears only among the unmeasured. No cost claim, no resident-satisfaction claim, no rescued-customer framing.
- **Author perspective / acting party**: Elm Quay or its team is the grammatical subject of every decision (decided to try, tested, chose, designed the categories, kept telephone reporting open, will decide). Svale appears in the third person only; there is no "we" outside Lind's quotations.
- **Publisher stance**: "Svale Systems publishes and approved this account, which is not independent journalism" carries both the brief's publisher identity and the material's disclaimer.
- **Link**: URL identical, described as a checklist to read, kept optional ("can … before they start"). No booking, demo or trial implied. Matches the brief's destination description exactly.
- **Reservation**: survives twice — "Lind did not recommend Svale to every housing company, and her own appraisal carries a condition" (verbatim non-recommendation plus the material's "qualified assessment"), and the "but I would leave an extra week" inside the quotation.
- **Unknown kept apart from absent**: "No comparison with another supplier is available" is reproduced word for word — *unavailable*, not *nonexistent*. The draft nowhere claims no other supplier was considered.
- **No count-size judgement**: 31 is given with its exclusions and no evaluative word; the medians are given without "faster", "improved" or "only".

### Four places I tested and would not fail, but which are tighter than the literal material

1. **Standfirst, "Thirty-one repair reports went into it over eight weeks."** The material carries the figure as the note's statement ("the note … says that 31 repair reports were entered") and the draft states it in its own voice, without the exclusions. The next standfirst clause names "Elm Quay's own trial note" as the source of the measures, and the body attributes the figure and carries both exclusions in the very next sentence. A caveat deferred, not dropped.
2. **"records 31 repair reports entered during the eight weeks"** binds the count to the trial window, which the material does not state in so many words — but the note is a *trial* note whose count "excludes … work ordered before the trial", which is the material's own binding.
3. **"Repair reports reached its maintenance team by telephone and by email"** names a recipient the material never names, and reads the material's bare "emails" as repair reports. The paragraph the material puts this in is about repair reporting and about that team's handling of it, and no rival recipient exists on any ordinary reading.
4. **"Cost, resident satisfaction, and completion time were not measured"** turns "There are no … measurements" into an assertion about the act of measuring. The material's form denies that such measurements exist for this trial, which is what the draft asserts. The gap is real but too thin to call a defect.

---

## 3. G2 — required parts

**Verdict: pass**, with one structural weakness recorded.

The order and the inventory hold: headline ("Elm Quay Housing tested one shared repair log"), standfirst (three sentences: what happened, the headline figure, a signpost), byline, lead (640 apartments, split channels, the shift motive, the decision as the customer's own), four `##` sections, ending (disclosure plus call to action).

Each part does its own job. The standfirst does not merely restate the headline — it adds September 2025, the 31 reports and the eight weeks, and tells the reader what the three sections will deliver. The lead supplies the situation the headline could not: 640 apartments, telephone and email stored separately, the shift problem. The four sections carry choice, setup, figures and appraisal respectively, and none duplicates another.

The customer account is complete:

- **Situation** — 640 apartments, separate storage of telephone and email reports, staff on different shifts unable to see the same information.
- **Action** — the team decided on the trial itself, tested the status display, chose Svale, designed its own categories, kept telephone reporting open, ran eight weeks in two buildings.
- **Results** — 31 reports with both exclusions, medians of two and three working days, the workload caveat and the note's non-attribution, and the three measurement gaps.
- **Appraisal** — Lind's own qualified verdict, quoted, with the condition intact.
- **Publisher stance** — truthful and unhedged, in the ending.
- **Customer as acting party** — held throughout; even the one supplier-subject heading ("Svale trained six staff members in two sessions") reports a service delivered, not a rescue.
- **Call to action** — built only from the supplied link, described as what it is.

**The weakness.** Section 1 opens by saying its own heading twice: "**Elm Quay picked Svale after a status test**" is followed by "Before choosing Svale Systems, the team tested whether the log could show the status of each repair. **It chose the supplier after that test.**" The second sentence adds nothing to the first, and the pair together add nothing to the heading. A reader gets the same small fact three times in four lines. Section 2 is likewise thin — two sentences of setup whose quotation is about category work rather than about the training the heading names. This is a distinctness problem inside a section rather than between the required parts, so it does not carry G2 to a fail, but it is the draft's least professional passage.

---

## 4. L1 — professional prose in en_US

**Verdict: pass.**

The prose is plainly American and plainly written. Collective nouns take singular agreement throughout, which is the en_US rule and the opposite of the British default: "The team wanted", "the team designed the categories itself", "the team will decide once it has checked". Lexis is American where it matters ("apartments", "staff members" rather than bare plural "staff"). The serial comma is used and held consistently ("what the team set up, what Elm Quay's own trial note measures, and how its supervisor judges the experience"; "Cost, resident satisfaction, and completion time"). Date form is American. No British or other-language syntax is imported anywhere — no "different to", no "in hospital", no present-perfect where the simple past belongs.

Sentences earn their length. "Whether the log moves beyond the two buildings is still open: the team will decide once it has checked how the categories hold up for larger repairs" is a colon doing real work, and the reader ends the piece knowing precisely how much is settled. "The team wanted staff on different shifts to see the same information, and the decision to try a shared log was its own" puts motive and agency in one clean line.

Two blemishes, neither disqualifying:

- **"Svale Systems publishes and approved this account"** yokes a present and a past tense to one subject. It is readable but it clunks; an editor would write "Svale Systems publishes this account and approved its publication."
- **"two working days"** / **"three working days"**: *business days* is the ordinary American term and *working days* reads faintly British. The material uses "working days" and it sits inside a statistic, so keeping it is defensible — but it is the one lexical choice in the draft a native American editor would pause over.

---

## 5. Bridges into quotations

Three quotations, in order.

### Q1

- **Bridge:** "The team designed the categories itself and kept telephone reporting open for residents."
- **Quotation:** "We wanted the evening shift to see what the morning shift had already done. The categories were ours; Svale helped us put them into the log,"
- **Speech tag (carries more than attribution):** "writes Maya Lind, Elm Quay's maintenance supervisor, who answered questions by email." — the role, the employer and the email medium are all supplied by the material ("Customer interview with maintenance supervisor Maya Lind"; "All interviews occurred by email"). Nothing in the tag is unsupported.
- **Class: (c).** The words that put it there: "**and kept telephone reporting open for residents**" — a fact the quotation does not carry at all.
- **Two readings.** The first half, "The team designed the categories itself", is answered almost word for word by the quotation's "The categories were ours", which is a class (a) move in miniature. I choose (c) because the bridge's second clause is a fact the quotation never touches, and because the quotation still delivers the evening-shift/morning-shift handover that the bridge has not given the reader. The (a) reading is real but partial: it pre-empts one of the quotation's two sentences, not the quotation.

### Q2

- **Bridge:** "Lind would plan the next building differently."
- **Quotation:** "We spent more time agreeing on the categories than entering the first reports. I would set that time aside before the next building starts,"
- **Speech tag:** "she writes." — attribution only.
- **Class: (b).** The words that put it there: "**Lind**" and "**the next building**" — the bridge names the speaker and the occasion the quotation speaks about, and stops.
- **Two readings.** It can be read as (a): "would plan the next building differently" is the gist of "I would set that time aside before the next building starts", and everything in the bridge is contained in the quotation, so the bridge adds no understanding of its own. I choose (b) because the quotation still delivers two things the reader does not have from the bridge — the comparison that motivates the change ("more time agreeing on the categories than entering the first reports") and the concrete remedy ("set that time aside"). Under the stated test, the quotation does not arrive as the bridge said again; "differently" is a pointer, not the content. Naming the subject a quotation goes on to speak about is not by itself (a).

### Q3

- **Bridge:** "Lind did not recommend Svale to every housing company, and her own appraisal carries a condition."
- **Quotation:** "I would choose to do the trial again. Having one view of the reports helps us, but I would leave an extra week for preparation,"
- **Speech tag:** "she writes." — attribution only.
- **Class: (c).** The words that put it there: "**Lind did not recommend Svale to every housing company**" — a fact about the scope of her endorsement that the quotation nowhere carries, and the most useful sentence in the section.
- **Two readings.** The second clause, "her own appraisal carries a condition", announces the quotation's "but" before the reader reaches it, which is an (a) move. I choose (c) on the strength of the first clause, which is genuinely additive; but the section is the draft's most pre-empted moment, because the heading above it ("The supervisor would repeat the trial, with more preparation") has *already* delivered both halves of the quotation — the repetition and the condition. The quotation is not pre-empted by its bridge so much as by its heading, which is outside the scope of this classification but worth the note.

**No quotation stands without a bridge.** All three have one.

**Counts.** The draft carries no class (a) bridges, one class (b) bridge (Q2) and two class (c) bridges (Q1, Q3).

**Interviewer utterances.** The draft attributes no question or utterance to an interviewer anywhere; the only trace of the interviewer is the supported relative clause "who answered questions by email", which reports the medium the material states ("All interviews occurred by email") and quotes no question.

**Unsupported bridge assertions.** None: Q1's bridge is the material's "The maintenance team designed its categories and kept telephone reporting open for residents"; Q2's bridge rests wholly inside the speaker's own conditional; Q3's bridge is the material's "Lind did not recommend Svale to every housing company" verbatim plus its "her actual, qualified assessment" rendered as "carries a condition".

---

## 6. Quoted speech

**All three quotations are word for word from the supplied usable quotations** — both sentences of each, in the supplied order, with nothing welded, compressed or dropped. Only the quotation marks differ (curly in the material, straight in the draft), which is mechanics.

- **Meaning** is untouched: "more time agreeing on the categories than entering the first reports" keeps the comparison; "one view of the reports helps us" keeps the present tense and the modest scope ("helps us", not "transformed us").
- **Stance** is untouched: Q1 keeps ownership with the customer and Svale as helper ("The categories were ours; Svale helped us"); Q3 keeps a favourable but bounded verdict.
- **Certainty and reservation** are untouched: "I would choose", "I would set", "I would leave", and above all the concessive "**but** I would leave an extra week for preparation" — the qualification the brief requires to survive, surviving in her own words.
- **Voice** is untouched: no smoothing into the article's register, no hedge added or removed, no self-correction misquoted.

**Nothing is missing.** The material offers exactly three "complete usable quotations" and the draft uses all three, each once. No permitted quotation is left out, and none is used twice or split across the piece.

One point in the draft's favour that the brief asks to be judged: each quotation contributes experience the narrative does not. Q1 supplies the shift-handover motive in the team's own terms; Q2 supplies the preparation lesson, which appears nowhere else in the draft; Q3 supplies her verdict, which by the material's own statement is "not an inference from the figures" and could not have been derived from the narrative.

---

## 7. Intermediate — checker findings and their dispositions

Report 1 raised five findings and one editorial question. Report 2 raised none. The reply's account of both matches the files.

| Passage (draft as checker 1 saw it) | Allegation | What the writer did | Class |
|---|---|---|---|
| Heading: "One check decided which supplier Elm Quay picked" | Turns the material's sequence ("chose … after testing") into a cause, and asserts the check was the whole evaluation ("One check") | Rewrote to "Elm Quay picked Svale after a status test" | **Supported repair.** The finding was right on both counts; the new heading states the sequence and claims no exhaustiveness |
| Heading: "Six staff members learned the log in two sessions" | Training delivered reported as competence acquired; no competence assessment exists in the material | Rewrote to "Svale trained six staff members in two sessions" (checker's own alternative) | **Supported repair.** The material measures training given, not learning achieved |
| Heading: "The figures cover counts and assignment time, nothing else" | "nothing else" converts three named measurement gaps into a closed set; unclaimed is not thereby known absent | Replaced with "The note measures assignment time, not the software's effect" | **Supported repair**, and an improvement beyond the finding: the replacement heading now carries the note's own non-attribution |
| "The note states that the two periods carried different workloads, and it does not attribute the difference to the software." | Moves into the note's voice a fact the material asserts in its own voice | Rewrote to "The two periods carried different workloads, and the note explicitly does not attribute the difference to the software." | **Supported repair.** Whose assertion it is now matches the material exactly |
| "The maintenance team's internal note …" and deck "what its own trial note measures" | Narrows the note's authoring party from the company to one unit inside it | Rewrote to "Elm Quay's internal trial note …" and "what Elm Quay's own trial note measures" | **Supported repair.** Minor, but the material names the document as Elm Quay's and never names its author |
| §5.3, editorial question: the dropped "explicitly" in the note's non-attribution | Not a support defect, but the material's deliberate disclaimer word | Restored "explicitly" as part of the F4 repair | **Supported repair.** A caveat put back at no cost |
| Report 2 — no findings | — | Nothing to do | Consistent with my own reading of the prose: I found no subject-matter defect in it either |

**A real defect seen by no checker: yes — the byline.** Both checkers set it aside by instruction rather than judging it, and report 1 stated a belief the report cannot have verified — that the name "comes from the invocation, not the material". The brief's "No author name supplied" is material, and the draft answers it with a name. The carve-out, not the checkers' reasoning, is what let it through; nothing in the evidence shows either checker weighing it and clearing it.

Four smaller items listed in §2 above (the standfirst's unattributed count, the eight-week binding, "reached its maintenance team", "were not measured") were all tested by at least one checker and set aside with arguments I accept. No checker missed a subject-matter defect I could find.

---

## 8. Stop or delivery

**A valid delivery**, with one qualification.

The sequence is sound and the evidence shows it rather than asserts it: a first comparison found five real defects in the prose, all five were repaired, the repairs were genuine corrections rather than cosmetic edits, a *second* comparison read the repaired prose in full, and the prose delivered is byte-for-byte the prose that second comparison cleared. No finding was left open, none was rejected, and nothing was changed after the last check — the ordinary failure mode of a repair-then-deliver loop, in which the delivered text has drifted past the last text anyone verified, did not occur here. On the material's own terms the draft is truthful: the causal firewall around the median figures holds in title, standfirst, headings and body alike, the customer stays the acting party, the reservation survives, and the call to action describes the supplied document accurately. The reply is also candid about what the material would not support and what further material would close each gap.

The qualification is that the delivered artifact carries an invented byline, and the process could not have caught it: the byline was placed outside both comparisons by the instruction the checkers worked to, so the only line in the piece that is unsupported is the one line no checker was allowed to look at. The reply discloses it and tells the reader to change it before publication, which is honest — but a Skill whose promise is that the delivered text stays inside the supplied material delivered a text that, in one line, does not. The delivery was right to happen; the byline should not have been in it.
