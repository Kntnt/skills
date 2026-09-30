# Judgement

The judged draft is `delivered.md`, a Swedish customer case. The run directory has no `evidence/` directory. No checker report, intermediate draft or disposition file exists. Everything in point 6 therefore rests on what `response.md` says.

## 1. Outcome

- **Delivered**, with two known defects flagged to the user.
- **Two comparisons ran**, according to the reply. After the first, four findings were repaired. After the second, two findings were left unrepaired and handed to the user.
- **Identical to the last prose a checker saw**: yes, according to the reply ("Texten är exakt den som jämförelsen läste"). The evidence cannot confirm this because no draft files exist. `delivered.md` is byte-for-byte the Markdown block in `response.md`.

## 2. F1: fail

None of the forbidden inferences appears. The draft does not claim that the software caused the shorter assignment time, and it makes no claim about saving money or pleasing residents. Assignment time is not turned into completion time. Lind's reservation survives, and so does the note's non-attribution. The workload caveat and the missing cost, satisfaction and completion measures are all in the body. The draft still carries these defects:

1. **Invented byline: "Av Thomas".** The brief says "No author name supplied". The reply says the name came from the account's email address, which is outside the supplied material. This attributes authorship to a named person. The material says only that the supplier publishes the piece. The reply flags this, but the draft still carries it.
2. **Changed term in a subheading: "PM:et tillskriver inte loggen den kortare tilldelningstiden".** The source says "the note explicitly does not attribute the difference to the software". Checked in both directions: "loggen" covers more than "the software". It can mean the whole trial of a shared repair log, meaning the working method, categories and single view. The source says nothing about whether the note credits or disclaims the method. So the subheading states something about the note that is unknown. The body uses the right term ("tillskriva programvaran skillnaden"), so the draft also contradicts itself. The effect is small: the subheading makes the disclaimer broader, not the claim stronger.
3. **Narrowed scope of the exclusion: "Enligt det fördes 31 felanmälningar in i loggen. Akuta ärenden och arbeten som beställdes före provet räknas inte med."** In the source, "It excludes …" follows a sentence whose subject is the note. The exclusion therefore most plausibly covers the note's figures, including the medians. In the draft, "räknas inte med" is attached to the count of 31, and the medians sit in a separate paragraph. A reader will take the exclusion as applying to the count only. This is a scope change, not an invention, and it is minor.
4. **Minor, not decisive: "i två av husen".** This presupposes that Elm Quay has more than two buildings. The source says only "in two buildings". Lind's own "before the next building starts" supports the presupposition, so I do not count it as a defect.

Everything else checks against the source: 640 flats, the September 2025 decision, separate telephone and email storage, the shift motive, the choice made after the status test, "Någon jämförelse med en annan leverantör finns inte redovisad", six staff trained in two sessions, telephone reporting kept open, eight weeks, the 4 December 2025 note, 31 reports, medians of 2 against 3 working days, "Lind rekommenderade inte Svale för alla bostadsbolag", the expansion decision still pending, and a CTA that describes the checklist as a document to read. The standfirst's "kortare" is backed by the supplied comparison (two days against three), and the same sentence keeps the non-attribution.

F1 fails on item 1, an unsupported attribution, and item 2, a changed term. Both are local and easy to fix. Item 1 is the more serious because it concerns who stands behind the text.

## 3. G2: pass. L1: pass

**G2, pass.** The parts come in the required order: headline, standfirst, byline, lead, three body sections and a CTA ending.
- The headline states the event.
- The standfirst gives the motive, the choice, the hedged result and the voice to come. Its last sentence, "Arbetsledaren Maya Lind berättar hur hon ser på provet", is thin but does a job.
- The lead sets up the situation and says the trial is not yet expanded.
- The sections carry situation and action (the team's goal, the status test, Svale's configuration and training, telephone reporting kept open), the results with every caveat, and the appraisal: Lind's qualified verdict, her non-recommendation and the open decision.
- The customer stays the acting party. The team decided, designed the categories, tested and chose. Svale only "konfigurerade" and "utbildade".
- Supplier narration stays in the third person. Nothing claims independence.
- The CTA uses the supplied link and describes it correctly as a checklist to read before a trial.

Weaknesses:
- The draft never discloses that Svale publishes it. Together with a personal byline in a journalistic format, a reader could take it for independent reporting. The stance is not false, but it is not stated. The reply leaves disclosure as an editorial decision.
- Quote 1's shift motive has already appeared in the standfirst ("personalen på olika skift skulle se samma information"). The quote makes it concrete, so it still adds something.

**L1, pass.** The prose reads as native Swedish news style: "Innan valet föll på Svale Systems", "Tidigare sparades telefonanmälningar och mejl var för sig", "avstår uttryckligen från att tillskriva programvaran skillnaden", "Den som leder underhållet i ett mindre bostadsbolag". Small blemishes:
- "Den tiden skulle jag avsätta innan nästa hus sätter i gång" is a mild calque of "before the next building starts". A building does not "sätta i gång". "Innan vi drar i gång i nästa hus" would be idiomatic.
- "Enligt det fördes …" has a stiff pronoun; "Enligt PM:et" reads better.
- "rekommenderade inte Svale för alla bostadsbolag" is acceptable, though "till" is more usual.

None of these would stop a professional reader.

## 4. Bridges into quotations

1. **Quote 1.** Bridge: the speech tag ", skriver Maya Lind, arbetsledare i underhållsteamet, i sina svar via e-post." There is no narrative sentence before the quotation, because a subheading stands directly above it. The tag counts as a bridge because it carries a title and the medium besides the attribution. Quotation: "Vi ville att kvällsskiftet skulle se vad morgonskiftet redan hade gjort. Kategorierna var våra, Svale hjälpte oss att föra in dem i loggen". **Class (b)**, from the words "arbetsledare i underhållsteamet" (attribution) and "i sina svar via e-post" (occasion). Second reading: (c), because "i sina svar via e-post" is a fact the quotation does not carry. I chose (b) because the email medium is the occasion of the utterance, not a fact about the story.
2. **Quote 2**, "Vi lade mer tid på att enas om kategorierna än på att föra in de första anmälningarna. Den tiden skulle jag avsätta innan nästa hus sätter i gång": **no bridge**. A subheading stands directly above it, and its tag ", skriver Lind." carries only the attribution.
3. **Quote 3**, "Jag skulle välja att göra provet igen. En samlad bild av anmälningarna hjälper oss, men jag skulle lägga in en extra vecka för förberedelser.": **no bridge**. It follows quote 2 directly as a further dash line, with no tag. By Swedish convention it is attributed to Lind by continuity.

- Counts: (a) 0, (b) 1, (c) 0, and two quotations with no bridge.
- Interviewer: the draft attributes no question or utterance to an interviewer.
- Unsupported bridge assertion: none. The title matches "maintenance supervisor", and the email medium matches "All interviews occurred by email".

## 4b. Subheadings over quotations

1. "## Teamet testade om loggen kunde visa status innan det valde Svale" over quote 1, "Vi ville att kvällsskiftet skulle se vad morgonskiftet redan hade gjort. Kategorierna var våra, Svale hjälpte oss att föra in dem i loggen". **Neutral.** "testade om loggen kunde visa status" is about the selection test, which the quotation does not mention. Second reading: prepares, because "loggen" and "Svale" name things the quotation mentions. I chose neutral because the quotation's subject is the shift motive and who owned the categories, not the status test or the choice.
2. "## Arbetsledaren ser tillbaka på åtta veckors prov" over quote 2, "Vi lade mer tid på att enas om kategorierna än på att föra in de första anmälningarna. Den tiden skulle jag avsätta innan nästa hus sätter i gång". **Prepares.** "Arbetsledaren" names the speaker and "ser tillbaka på åtta veckors prov" names the occasion. It does not say that category work took longest.
3. The same subheading over quote 3, "Jag skulle välja att göra provet igen. En samlad bild av anmälningarna hjälper oss, men jag skulle lägga in en extra vecka för förberedelser.". **Prepares.** "ser tillbaka" names a retrospective without giving the verdict ("göra provet igen") or the reservation ("en extra vecka"). A pre-echo reading is not available, because nothing in the subheading states her conclusion.

Counts: pre-echo 0, prepares 2, neutral 1.

## 5. Quoted speech

- **Quote 1:** meaning and stance intact. "The categories were ours; Svale helped us put them into the log" keeps the customer's ownership and Svale's supporting role. The semicolon became a comma, which is acceptable in Swedish.
- **Quote 2:** intact. The advice is kept as her own conditional ("skulle jag avsätta"), with the mild calque noted under L1.
- **Quote 3:** intact. The conditional "skulle välja" is kept, the positive clause "hjälper oss" is not strengthened, and the reservation "men … en extra vecka för förberedelser" survives. The earlier "göra om provet" was repaired to "göra provet igen", which removes the reading that the trial had failed.
- Lind's first-person voice is kept throughout, and no quotation has moved in certainty.
- All three permitted quotations are used. None is missing.

## 6. Intermediate

There are no report files, so each line rests on the reply's description.

| Round | Passage | Allegation | What the writer did | Class |
|---|---|---|---|---|
| 1 | Headline | It claimed all repair reports were collected in the log. | Repaired. | **Supported repair.** Telephone reporting stayed open and the note excludes emergencies, so "all" was unsupported. The original wording is not in evidence, but the delivered headline is clean. |
| 1 | Standfirst | Its comparison period was wrong, and it was unclear who does not attribute the difference to the software. | Repaired. | **Supported repair.** The standfirst now reads "under de åtta veckorna före" and "PM:et tillskriver inte programvaran skillnaden". |
| 1 | A subheading | It presupposed that the status display worked. | Repaired. | **Supported repair.** The source says the team tested *whether* it could show status, and the subheading now says "testade om". |
| 1 | Quote 3, "göra om provet" | It could read as repeating a failed trial. | Repaired to "göra provet igen". | **Supported repair.** |
| 2 | Subheading "PM:et tillskriver inte loggen …" | "loggen" is broader than "programvaran". | Not repaired. Flagged to the user with the fix. | **Right finding rejected (in effect).** It was deferred to the user rather than disputed. The finding is correct, see F1 item 2. |
| 2 | "Akuta ärenden … räknas inte med." | The exclusion is tied to the 31 reports only, but the source's "It" may cover the whole note, medians included. | Not repaired. Flagged to the user with the fix. | **Right finding rejected (in effect).** The finding is correct and minor, see F1 item 3. |

**Seen by no checker:** yes. The invented byline "Av Thomas" (F1 item 1) is a real defect that no reported checker finding names. The writer raised it in the reply only as a setting for the user to change. The undisclosed supplier stance was not raised by any checker either. The writer mentioned it as an editorial choice. No point-4 defect exists to have been missed.

## 7. Stop or delivery

**Valid delivery.** The draft respects every forbidden inference, keeps every caveat and the customer's reservation, and uses the quotations faithfully. Its defects are small, local and fixable:
- the "loggen" subheading;
- the scope of the exclusion;
- the byline.

The reply discloses all three and gives exact fixes for two of them. Stopping would have withheld a sound draft over wording the user can settle in seconds. The byline should not have been filled from outside the material. Leaving the slot as a visible placeholder would have kept F1 clean.
