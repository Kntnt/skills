# Judgement — w-f53fcb (case study, Swedish, English source)

## 1. Outcome

**Delivered**, with four unrepaired findings disclosed in the reply.

**Comparisons: two completed.** `evidence/source-check-1/` and `evidence/source-check-2/` each hold a complete report. Neither report could be written to disk (both paths lie under `.git/`, which the harness refuses), so each checker returned its report in its reply; the run captured both as `report.md`. `source-check-1/report-reply.txt` shows an earlier attempt at the first comparison that came back as a safeguard error with no report, which the reply says was rerun and not counted. So: one aborted attempt, two completed comparisons.

**Delivered prose is identical to the last prose a checker read.** `diff evidence/source-check-2/draft.md delivered.md` shows one difference only: the seven-line YAML front matter (`genre: case-study`, `technique: none`, `language: sv`) prepended to the delivered file. Not one word of prose differs. The reply's claim on this point is true.

The first comparison's draft differs from the delivered one in four places (dek subject, one heading, two agent restorations, one quotation verb), all of them repairs made between the comparisons.

Judged draft: `delivered.md`.

## 2. F1 — **fail** (four small but real departures; every large trap avoided)

First, what holds. The draft makes none of the forbidden inferences. It never says the software caused the shorter assignment time — it states the workload difference and the note's explicit non-attribution, and heads that section *Siffrorna säger inget om orsaken*. It never converts assignment time into completion time: *från anmälan till tilldelning* is exact, and *tid till avslutat arbete* appears only in the list of what was not measured. No cost saving, no resident satisfaction, no rescued customer. Lind's reservation survives twice, inside her quotation (*men jag skulle lägga in en extra vecka*) and in narration (*Hon rekommenderar däremot inte Svale till alla bostadsbolag*, with the negated universal scoped correctly). Every figure matches: 640, September 2025, two buildings, eight weeks, six staff, two sessions, 4 December 2025, 31, two and three working days, one extra week. No count is characterised as high or low. The link is described as what the brief says it is, a document to read. Supplier narration stays third person throughout.

The departures:

1. **Dropped state-of-knowledge caveat.** Draft: "Någon jämförelse med en annan leverantör finns inte." Source: "No comparison with another supplier **is available**." The source reports the record in front of the writer; the draft reports the world. A comparison that was made and never written up satisfies the source and falsifies the draft. Nothing supplied excludes that case. (*finns inte redovisad* would hold.)
2. **Changed thing measured.** Draft: "redovisar 31 felanmälningar under de åtta veckorna." Source: "31 repair reports **were entered**." The material counts what reached the log; the draft counts what came in during the period. Telephone reporting stayed open, and the note's two exclusions (emergencies, work ordered before the trial) do not cover a report handled without being logged, so the two statements can come apart. Attributing the figure to the note limits the damage but does not repair it.
3. **Changed modality: an open decision becomes a scheduled step.** Draft: "Försöket har ännu inte utvidgats till fler hus. Teamet ska **först** se efter hur kategorierna fungerar för större reparationer." Source: "the team **will decide** after checking how the categories work for larger repairs." The decision itself disappears; *först*, read against the preceding sentence, answers "first, and then the expansion". The material leaves expansion genuinely open — the team may check and drop the log. This is the most consequential of the four, because the open-endedness is part of the customer's own caution.
4. **Widened term across languages.** Draft: "testat om loggen kunde visa status på **varje ärende**." Source: "the status of **each repair**." Tested both ways: in Swedish property management an *ärende* is any logged matter — a report closed without a repair is an *ärende* and not a *reparation* — so the draft claims a test of a wider class than the material records. The reverse direction is clean: every *reparation* here is an *ärende*. Minor, but real.

5. **Unseen by either checker: the repaired heading still dates things the material does not date.** "## Så förbereddes försöket i de två husen" gathers under *preparation* both Svale's training of six staff (the material gives no date for the two sessions) and the team keeping telephone reporting open for residents, which on the material's own wording ran through the trial rather than before it. Compatible case: the two training sessions fall in week three of the eight. Every supplied sentence survives; the heading does not. This is a much lighter version of the chronology defect checker 1 found in the previous heading ("innan loggen togs i bruk") — the repair reduced it rather than removing it.

Borderline, recorded but not counted against F1:

- "Vad loggen skulle lösa hade teamet redan bestämt." *Bestämt* is firmer than "The team wanted staff on different shifts to see the same information", but "The maintenance team designed its categories" and Lind's "The categories were ours" carry a settled, prior aim. Defensible.
- "Hon rekommenderar" (present) for "Lind did not recommend" (past). Ordinary Swedish reporting of a standing position, and the material marks the final quotation as "her actual, qualified assessment".
- "Utfallet finns i en intern notering." *Utfall* names the figures the note records; no verdict is asserted, and the section beneath withholds one.
- **The byline.** "Av Thomas Barregren" is an authorship attribution that the material does not supply ("No author name supplied"). It is not an assertion about the case, the customer or the supplier, it is the name of whoever ran the job, and the reply states plainly that the line carries the user's name and must be changed if the text is to go unsigned. I record it, and do not count it as an F1 failure.

No invented event, no invented personal attribute, no invented scene, emotion or remembered dialogue — the material forbids all four and the draft supplies none. Unknown is kept apart from absent everywhere except in departure 1.

## 3. G2 — **pass**, with one named weakness

Parts present, in order: headline (*Elm Quay testade gemensam felanmälningslogg i två hus*), standfirst, byline, lead, four sections, ending.

Each part does its own job. The headline names actor, thing and scope without a verdict. The standfirst carries the forward hook the headline cannot ("arbetsledaren har redan en sak hon skulle göra annorlunda") — a promise the last two sections pay off. The lead supplies the before-state (telephone reports and emails stored separately) that the headline and standfirst do not. The four sections divide cleanly: setup, figures with their cause withheld, what is still pending, the qualified verdict. The ending closes on the reservation, then the offer, then the disclosure.

The customer account: **situation** (640 flats, separate storage, shifts unable to see each other's work); **action** (the team decided to trial, tested the supplier on status visibility, designed its categories, kept telephone reporting open, Svale configured and trained); **results** (31 reports, median two vs three working days, and an explicit list of what was not measured); **appraisal** (Lind's own qualified assessment, endorsement and reservation in one quotation). **Publisher stance** is truthful and in the right place: *Texten publiceras av Svale Systems, som var leverantör i försöket*, plus the email origin of the interview. **The customer is the acting party** throughout after the repairs — *Teamet valde Svale Systems*, *Telefonanmälan höll teamet öppen*, *bestämde underhållsteamet*; Svale acts only where the material has it act (configuring, training). **The call to action** is built from the one supplied route and describes its destination correctly, with no booking and no trial.

Weakness: the standfirst and the lead overlap more than a 385-word text can afford. "Elm Quay Housing förvaltar 640 lägenheter" and "ett bostadsbolag med 640 lägenheter" sit in consecutive paragraphs, and *underhållsteamet* + *åtta veckor* are given twice. The reader who has read the standfirst gets roughly a third of the lead for the second time. Not enough to collapse the division of labour — the lead still adds the before-state, the September date and the two-building scope — but it is the one place where two parts do the same job.

## 4. L1 — **pass**

The draft reads as Swedish written by a Swede, not as English rendered. V2 is right at every fronting: *I september 2025 bestämde underhållsteamet*, *Under åtta veckor hösten 2025 provade underhållsteamet*, *Vad loggen skulle lösa hade teamet redan bestämt*, *Telefonanmälan höll teamet öppen för de boende*, *Den tiden skulle jag avsätta*, and the article-less conditional *Står du inför samma fråga i ditt eget bestånd, är införandechecklistan…* — a construction an English-shaped draft never reaches for. Compounds are solid throughout (*felanmälningslogg*, *underhållsteamet*, *arbetsbelastningen*, *införandechecklistan*, *kvällsskiftet*). Double definiteness holds everywhere it must (*den interna noteringen*, *de första anmälningarna*, *de åtta veckorna*, *de två husen*, *ditt eget bestånd*). Address is *du*; *man* appears nowhere; speech takes the Swedish speech dash. *Bestånd* and *arbetsledare för underhållet* are the field's own words. Sentences are short in the Swedish way, and two fronted-object sentences give the prose an idiomatic rhythm English word order would not produce.

Three places are stiffer than the rest, none of them an import of English syntax: *intern notering* for an internal trial note (*anteckning* or *PM* is the more ordinary Swedish word for the artefact); *nöjdhet hos de boende*, which reads as administrative Swedish where *hur nöjda de boende är* would read as prose; and *tid till avslutat arbete*, a stiff nominal rendering of completion time. Reader effect: three small bumps in an otherwise fluent read, all of the kind a Swedish editor would smooth and none of the kind that betrays a translation.

## 5. Quoted speech

Three passages, in draft order. The material supplies exactly three usable quotations and permits their translation.

**Q1** — Draft: "– Vi ville att kvällsskiftet skulle se vad morgonskiftet redan hade gjort. Kategorierna var våra, och Svale hjälpte oss att lägga in dem i loggen, säger Maya Lind, arbetsledare för underhållet." Source: "We wanted the evening shift to see what the morning shift had already done. The categories were ours; Svale helped us put them into the log."
- *One pass:* yes. Nothing is left for the reader to supply; *kvällsskiftet*/*morgonskiftet* are the Swedish words, *lägga in dem i loggen* is what a Swede says, and the pluperfect *redan hade gjort* lands where "had already done" does.
- *Meaning, stance, certainty, voice:* intact. The division of labour survives — the categories stay theirs, Svale only *hjälpte*. The source's semicolon becomes *och*, which flattens a faint contrastive edge, but the possessive *våra* still carries the emphasis and no stance has moved. Attribution correct: name and role as supplied.

**Q2** — Draft: "– Vi lade mer tid på att enas om kategorierna än på att lägga in de första anmälningarna. Den tiden skulle jag avsätta innan nästa hus kommer igång, säger Lind." Source: "We spent more time agreeing on the categories than entering the first reports. I would set that time aside before the next building starts."
- *One pass:* yes, though this is the weakest of the three. *Komma igång* collocates with activity in Swedish, and *nästa hus kommer igång* reads as the metonymy Swedish itself uses for the next unit coming onstream — the reader does not stop to supply a verb. (The pre-repair wording, *innan nästa hus börjar*, did stop a Swedish reader: a *hus* does not *börja*, and the housing context makes the wrong reading, a building starting construction, live.)
- *Meaning, stance, certainty, voice:* intact. The comparison of time is exact, *den tiden* keeps the referent of "that time", and the conditional *skulle* keeps "would". It stays a lesson drawn, not a complaint and not blame of Svale. The fronted object is idiomatic emphasis, not added emphasis.

**Q3** — Draft: "– Jag skulle välja att göra om försöket. Att ha en samlad bild av anmälningarna hjälper oss, men jag skulle lägga in en extra vecka för förberedelser, säger hon." Source: "I would choose to do the trial again. Having one view of the reports helps us, but I would leave an extra week for preparation."
- *One pass:* yes. *Göra om försöket* is read as repeating the trial in this context, *en samlad bild av anmälningarna* is the Swedish figure for one view of them, and the *men* clause closes where the source's does.
- *Meaning, stance, certainty, voice:* intact, including the pivot that is the point of the remark: the endorsement is conditional (*skulle* twice, matching "would" twice), the help is present-tense and scoped to *oss* rather than generalised, and the reservation stays inside the quotation instead of being moved to narration. The material's warning is honoured — the quotation is presented as her assessment and is nowhere derived from the median figures. Two different verbs, *avsätta* in Q2 and *lägga in* here, match the source's two different verbs, so her voice is not flattened into one formula.

**Missing quotations:** none. All three usable quotations appear, and each carries experience the surrounding narrative does not: the shift problem in her own words (Q1), the cost of agreeing categories (Q2), the qualified verdict (Q3).

**In one sentence:** yes — every passage of quoted speech in this draft is speech a Swedish reader takes on one pass, with the source's meaning, stance, reservation and voice intact.

## 6. Intermediate — every finding in the evidence

**Comparison 1** (three findings, three editorial questions):

| Passage | Allegation | What the writer did | Class |
|---|---|---|---|
| Dek: "teamet har redan en sak **det** skulle göra annorlunda" | Gives the team a position only Lind states in the first person singular ("I would set that time aside", "I would leave an extra week") | Repaired to "arbetsledaren har redan en sak **hon** skulle göra annorlunda" | **Supported repair.** The defect is real: the material attributes no such position to the team and marks the closing view as hers. |
| Heading: "Teamet lade upp försöket **innan loggen togs i bruk**" | Asserts a chronology the material does not establish, and Lind's own remark points against | Replaced with "Så förbereddes försöket i de två husen" | **Supported repair**, incomplete. The flat chronology claim is gone; a lighter one remains (see F1 item 5). |
| Q2: "innan nästa hus **börjar**" | Obstructs a Swedish reader — a *hus* does not *börja* | Repaired to "innan nästa hus **kommer igång**" | **Supported repair.** I read the original as a genuine stop, and the replacement as clearing it. |
| §4.1 two s-passives ("Svale Systems valdes", "Telefonanmälan hölls öppen") | Raised as an editorial question, not a finding: the agent drops out where the brief wants the customer acting | Acted on: "Teamet valde Svale Systems…", "Telefonanmälan höll teamet öppen…" | **Correct action on a correct note.** Not a support defect; the change serves the brief's acting-party instruction and costs nothing. |
| §4.2 "it is not independent journalism" not rendered | Editorial question only | Left as is; the draft discloses the publisher and its stake | **Wrong to call it a defect, and it was not called one.** Correct handling. |
| §4.3 length short of 400 words | Editorial question only; the contract forbids padding | Left as is; the reply names what further material would close the gap | **Correct.** |
| §4.4 "varje **ärende**" and "utfallet" set aside as defensible | — | No action | **Wrong set-aside on *ärende*.** Comparison 2 found it; I agree with comparison 2 (F1 item 4). |

**Comparison 2** (four findings, none repaired):

| Passage | Allegation | What the writer did | Class |
|---|---|---|---|
| "Någon jämförelse med en annan leverantör finns inte." | "is available" became non-existence | Not repaired; disclosed in the reply with the minimal fix (*redovisad*) | **Right finding rejected.** |
| "redovisar 31 felanmälningar under de åtta veckorna" | "were entered" dropped; log entries read as reports received | Not repaired; disclosed with the minimal fix (*i loggen*) | **Right finding rejected.** |
| "Teamet ska först se efter hur kategorierna fungerar för större reparationer." | "will decide" dropped; expansion reads as scheduled | Not repaired; disclosed with the minimal fix (*och därefter ta ställning*) | **Right finding rejected** — and this is the one that costs the reader most. |
| "status på varje ärende" (marked minor) | *ärende* is wider than *repair* | Not repaired; disclosed with the minimal fix (*varje reparation*) | **Right finding rejected.** |

Comparison 2 raised no translation finding and no editorial question; it confirmed the three repairs comparison 1 asked for. The reply's account of the disagreement between the two comparisons (the first read points 1 and 4 as correct, the second objects to them) is accurate against the evidence.

**A real defect no checker saw:** yes — the heading "Så förbereddes försöket i de två husen" (F1 item 5). Comparison 2's accounting states that "every heading" was compared, but its tables carry rows for the other three headings and none for this one; the heading introduced by comparison 1's repair was never checked by anybody. Comparison 1 could not see it, since it did not yet exist. Nothing under point 4 (quoted speech) went unseen: the one obstruction was found and repaired.

## 7. Stop or delivery

**A valid delivery, with one reservation about how it is framed.**

Valid, because of what the reply does rather than what the draft is. Two comparisons is the ceiling, both ran, and the second's four findings arrived after the last comparison was spent. Repairing them would have delivered prose no checker had read; delivering them silently would have been worse. The run took the third course: it delivered exactly the text the final checker read, said so, listed all four findings with the passage, the source wording, the reader consequence and the smallest repair for each, and named the disagreement between the two comparisons. The reply's factual claims about the run all hold against the evidence — the identity of delivered and checked prose, the four repairs made after comparison 1, the rerun of the first comparison and why, and the byline's provenance. A reader of that reply can fix all four defects in under a minute and knows exactly where to look.

The reservation: the reply calls the four "invändningar som du avgör, inte konstaterade fel i texten" — objections for the reader to settle, not established errors. Three of them are established errors. *finns inte* for "is available", the lost "entered", and the lost "will decide" each say something the material does not support, and the third thins the customer's own open-endedness, which is close to the thing the brief exists to protect. Presenting them as matters of taste understates them, and a reader who skims the reply and publishes the draft publishes three unsupported statements. A stop would have been defensible here; delivery with an accurate but firmer framing would have been better than delivery with an accurate but softened one.

Not a false stop, not a delivery made in ignorance: the run knew what it was handing over and said so.
