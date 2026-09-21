# Judgement B — article-sv / write

Genre: `article` (brief: "pedagogisk webbartikel"; metadata `genre: article`). The fixed article skeleton therefore applies, and counted requirements are settled by the script.

## 1. Outcome

**Delivered.** `response.md` carries the complete draft in a fenced block and a delivery account beside it; `delivered.md` holds that draft.

**One source comparison completed.** The evidence directory holds exactly one numbered cycle — `task-1.txt`, `reply-1.txt`, `report-1.md`, `validation-1.md` — and no second task, report or repair round. `validation-1.md` states "Complete by that route; one comparison ran, and it is the final one." `report-1.md` ends "Complete. … Findings: none. Unresolved findings: none." The report file itself could not be written by the checker; `report-1.md` and `reply-1.txt` are byte-identical, which is consistent with the account that the report arrived in the checker's reply and was saved from there. That the comparison was complete rather than truncated I can only take from the report's own coverage, which pairs 30 draft passages with source passages and covers headline, standfirst, lead, all four subheadings and all body paragraphs, plus a sweep of the brief's forbidden inferences. The material the checker read (`evidence/source-check/material.md`) is byte-identical to `work/source.md`, so it saw the whole brief.

**Delivered prose is byte-identical to the last prose a checker saw.** `diff evidence/source-check/draft.md delivered.md` is empty. The only disposition recorded (`validation-1.md`, item 11) is "accepted as written; no change made", and the reply states "Eftersom ingen prosa ändrades efter jämförelsen är det exakt den text granskaren läste som levereras här." No repair is recorded anywhere after the comparison.

## 2. Headings

- `# Mätningen i Björkskolan pekar ut lektioner, inte orsaker` — **statement**, **echo** (partial: it shares the verb phrase "pekar ut" with the standfirst's "Rapporten pekar ut 14 av 120 lektionspass", and its "inte orsaker" restates that standfirst clause's "men förklarar inte varför" in other words).
- `## Givaren mäter luften på sin egen plats` — **statement**. No echo: the first sentence under it is "Värden registrerades var femte minut under fyra veckor."
- `## Ett värde under gränsen säger inte hur länge` — **statement**. No echo: the first sentence under it is the report citation, not the duration point.
- `## Två metodval styr vad siffrorna betyder` — **statement**. No echo; the two method choices it counts (the working threshold, lesson periods instead of a daily average) are both in the section.
- `## Koppla temperaturen till när rummen används` — **statement** (imperative). No echo: the first sentence under it is "Efter försöket gick driftteknikern Elin Rask igenom tiderna för ventilation och värme tillsammans med skolans vaktmästare." Not marked **overclaim**: the imperative adopts advice the material carries (Rask's recommendation), which the body attributes explicitly two sentences later and the closing paragraph repeats in the author's own voice.

No heading carries a **colon** or is a **question**. No heading carries a figure, name or conclusion the text does not carry.

## 3. F1 — pass

Every assertion, quotation and attribution stays inside `work/source.md`. The passages that could have slipped, and why they do not:

- "Rapporten pekar ut 14 av 120 lektionspass med minst ett värde under 20 grader" (standfirst) drops the source's "totalt … registrerade" and "Celsius". The body restores both before the figure is used for anything: "14 av totalt 120 registrerade lektionspass innehöll minst en mätning under 20 grader Celsius." No wider set is asserted, and the ratio is stated within the trial's own set. Not a defect.
- "men förklarar inte varför" is an absence claim about the report. Supported: the brief states "Ingen … orsak till kyla … följer av materialet", and Rask says "Vi vet ännu inte varför det blev kallt just då."
- "Siffran 14 av 120 är därför ett antal, inte ett omdöme: att avgöra om det är mycket eller lite kräver ett jämförelsetal som mätningen inte ger." This is the forbidden evaluation declined, not made, and matches "14 av 120 saknar normjämförelse: kalla det inte högt/lågt."
- "Vilken effekt eventuella justeringar har fått är ännu inte mätt." The source is "Inga justeringars effekt har ännu mätts." The draft claims strictly less than the source: it leaves open whether any adjustment was made, where the source's phrasing could be read as presupposing some were. Keeping unknown apart from absent is exactly right here — the material says only that Rask went through the times with the caretaker. Not a defect.
- "Ett medelvärde för hela dygnet" for the source's "Ett medelvärde för hela dagen". Tested both directions: *dygn* is the full 24 hours and *dag* can mean the lit or working part, so the terms are not interchangeable in general. In this context the source's own following clause names the rejected alternative "ett enda dygnsmedelvärde", which settles that the average under discussion is the 24-hour one. Nothing here falls under one term and not the other. Not a defect.
- "Ett enda värde strax under gränsen räknas likadant som en hel lektion under den." This is an entailment of the counting rule the source states ("minst en mätning under 20 grader"), not an added fact, and it asserts nothing about how often either case occurred.
- "– Vi vet när vi behöver titta närmare. Vi vet ännu inte varför det blev kallt just då, säger Elin Rask." Reproduced word for word from "Rask sade: ”Vi vet när vi behöver titta närmare. Vi vet ännu inte varför det blev kallt just då.”" Source and target language are both Swedish, so no translation step exists; both certainty markers ("Vi vet" / "Vi vet ännu inte") and the deictic "just då" survive unresolved, as they must. The present-tense "säger" for "sade" changes neither the assertor nor the words.
- "finansieringen är inte beslutad" preserves the funding caveat in the same sentence as the November plan, so a planned trial is not turned into a settled one.
- "Av Thomas Barregren" is not compared against the material: the brief names no author ("Ingen byline är given"), so the invoking user's name is the byline, and the reply states this openly under "Bylinen bär ditt namn".
- Definite forms for the source's indefinites — "klagomålen" for "klagomål", "temperaturserierna"/"användningstiderna" for "temperaturserier"/"användningstider" — narrow generic wording to this trial. In each case the narrower reading is the one the surrounding paragraph establishes, and the office would not ask whether complaints coincided with low temperatures had none been made. Not defects.

None of the brief's forbidden inferences appears: no saving, no health claim, no cause of the cold, no effect of the sensors or of any adjustment, no legal rule, and no high/low verdict on 14 of 120. The article asserts the opposite of a cause twice, in the headline and in the quotation.

One passage is a genuine scope question rather than a defect, treated under *Checker findings* below: "En givare mäter temperaturen där den sitter, och den mäter luft." I record it as a qualitative concern, not an F1 failure.

## 4. G1 — pass

The named reader is a municipal property manager who knows heating systems but not measurement technique, and the brief's angle is "vad ett kort mätförsök kan och inte kan säga om värmen i en skola". The article holds that angle from the headline ("pekar ut lektioner, inte orsaker") to the close, and never drifts into the trial's findings as findings.

What the reader learns is concrete and usable: that a sensor reads air at its own position and not the radiant surroundings ("Operativ temperatur är ett annat mått, som väger in både luftens temperatur och värmestrålningen från omgivande ytor"); that the count rests on an at-least-one-reading rule, so "Ett enda värde strax under gränsen räknas likadant som en hel lektion under den"; that the 20-degree line is "kontorets egen arbetsgräns för försöket", not a legal threshold, and that the difference matters "när siffran förs vidare"; and that reporting lesson periods rather than a daily average is a choice that "formar vad underlaget kan visa". The journalistic craft is present — a named source, a dated report, an attributed quotation, an explicit statement of scope. No commercial request appears anywhere, as the brief required ("Ingen kommersiell uppmaning").

## 5. G2 — pass

All required parts are present and in order: headline, standfirst, byline, lead, four sections, and an ending. The script confirms the skeleton mechanically — `"conforms": true`, `"failures": []`, `"norms": []`.

- **Headline** — `"characters": 56`, `"words": 8`, inside the 20–70-character requirement. It states the angle of the whole text and is understood alone. It claims no more than the text claims. Its partial echo of the standfirst's "pekar ut" is a blemish, not a failure: the two carry different objects ("lektioner" against "14 av 120 lektionspass"), and the standfirst supplies the figure, the room count and the reader promise that the headline does not.
- **Standfirst** — `"words": 45` (requirement: at most 60) and `"paragraphs": 1`. It stands alone: who measured, where, for how long, what the report says, and what the piece will do for the reader ("Så långt räcker ett kort mätförsök – och så här kan du komplettera det").
- **Byline** — `"text": "Av Thomas Barregren"`. The brief names no author, so the invoking user is the author, and the delivery account states exactly that: "Briefen anger ingen författare, och då blir användaren författare." This satisfies the Write requirement.
- **Lead** — `"words": 46`, `"paragraphs": 1`, and it stands before the first H2. It begins the work rather than repeating the standfirst's function: it supplies the date, the office's motive and the frame the sections then carry ("smalare än det kan se ut, men användbart om du vet vad det mäter").
- **Body** — explanatory throughout, four sections, `"sections": 4`, each with at least one paragraph (3, 3, 2, 3).
- **Ending** — the lead's expectation is met: having promised a usable trial if you know what it measures, the text closes with what to settle before measuring. The call to action is the useful next step the explanation supports — "Planerar du ett eget mätförsök, är det värt att bestämma redan nu vad som ska noteras vid sidan av temperaturen" — built on Rask's recommendation and the November trial's added usage notes, and it is not commercial, which the assignment forbade.

## 6. P1 — pass

The reasoning is followable by this reader and every unfamiliar concept is introduced before it is used. *Operativ temperatur* is defined at first mention and immediately bounded ("Försöket mätte bara lufttemperatur"). The counting rule is stated before its consequence is drawn. The daily-average problem is stated before the reporting choice that answers it.

Transitions are real rather than decorative: "Mätningarna omfattar bara dessa sex rum och dessa fyra veckor. Siffran 14 av 120 är därför ett antal, inte ett omdöme" earns its *därför*; so does "Ett medelvärde för hela dygnet kan dölja variation under lektionerna. Rapporten redovisar därför lektionspass …", which is the source's own inference.

Conclusions stay proportionate to visible support, and the one general principle the author adds — "Ett underlag utesluter ingenting som det inte har mätt" — is the state-of-knowledge rule in the abstract, placed directly after the list of what was not measured, so the reader sees what it is about. Useful technical substance survives: the five-minute interval, the two-and-four exterior/interior split, the undocumented placement comparison, the air/operative distinction, the at-least-one-reading rule.

## 7. W1 — pass

A web reader can orient and enter without losing the continuous explanation or the voice. Every counted requirement is met, and the script records no norm departure at all: `"failures": []`, `"norms": []`.

- Headline `"characters": 56`, `"words": 8` — inside both the 20–70-character requirement and the eight-word/60-character *should*.
- Subheadings `"characters": 38`, `44`, `39`, `43` — all inside the 70-character requirement.
- Longest paragraph 50 words (the closing one), under the 80-word *should*; no paragraph approaches it.
- Sections of two or three paragraphs: `"sections": 4`, `"sections_of_two_or_three_paragraphs": 4` — every section inside the *should*.
- Heading levels: one level-1 headline and four level-2 subheadings, `"other": []`; no level below the second.
- Paragraph rhythm: `"paragraphs": 13`, `"paragraphs_of_two_or_three_sentences": 12`. *Most* is read across the whole text, and 12 of 13 satisfies it; the single one-sentence paragraph is the report citation, whose isolation is what makes the date and title easy to find.
- Standfirst and lead open on different first words: "Fastighetskontoret …" against "I januari 2026 …".

The subheadings are informative in the way this genre needs: each states its section's angle, and a reader scanning only them gets the argument's spine — the sensor reads its own spot, one reading says nothing about duration, two method choices govern the meaning, connect temperature to usage.

Qualitative concern, not a failure: the lead's first sentence restates the standfirst's first sentence closely — office, sensors, six classrooms, Björkskolan — so the second paragraph tells a scanning reader something the first just told them. The lead nevertheless adds the date, the motive and the frame, and the standfirst adds the figure and the promise, so the two remain complementary and the body is complete when the standfirst is covered. The total length is not measured by the script; the delivery account states 447 words against the brief's orientation of about 450, and I do not count it myself.

## 8. L1 — pass

The prose reads as Swedish written by a Swede, not as translated English. The idiom is native and varied: "Så långt räcker ett kort mätförsök", "värt att ha med sig när siffran förs vidare", "titta närmare", "vid sidan av temperaturen". The closing sentence uses the conditional inversion without *om* — "Planerar du ett eget mätförsök, är det värt att bestämma redan nu …" — which is a construction a non-native writer of Swedish would not reach for. Sentence rhythm alternates long and short to purpose, as in "Rapporten säger inte hur länge temperaturen låg under gränsen. Den säger heller inte om eleverna frös." No anglicism, no calque and no generic translated phrasing appears.

## 9. L2 — pass

The resolved locale is `sv` (metadata `language: sv`; the reply: "`sv`, från anropet"). Mechanics follow it throughout: the date form "12 mars 2026" with a lower-case month; the unit written out as "20 grader Celsius" with a space; "var femte minut"; no currency and no converted figure anywhere. Quoted speech uses the Swedish talstreck — "– Vi vet när vi behöver titta närmare. … , säger Elin Rask." — rather than imported quotation marks, and the reply names that choice deliberately. The parenthetical dash is the Swedish spaced tankstreck ("ett underlag – smalare än det kan se ut"). The report title is set in italics rather than quotation marks, which is established Swedish variation and is preserved consistently. No new factual date or conversion is invented.

## 10. T2 — skipped

The delivered text's `kntnt` metadata carries `technique: none`, and the reply states "**Teknik:** ingen." No technique was selected, so nothing is judged under this criterion, and I infer none from the shape of the prose.

## 11. Checker findings

`report-1.md` records no findings at all: "## 2. Findings — None. No claim in the draft was found to lack a source passage, to change the thing named or measured, the subject, scope, time, modality, certainty or assertor, or to lose a qualification that changes a claim." One item was raised and is listed here.

| Draft passage | What the checker alleged | What the writer did | My class |
|---|---|---|---|
| "En givare mäter temperaturen där den sitter, och den mäter luft." | Not a finding but an "editorial question" (report §3): the second clause continues the material's generic singular while its support, "försöket mätte bara lufttemperatur", is stated about this trial; a globe sensor for operative temperature is also "en givare" and the material does not exclude one. The checker proposed no repair and judged the passage defensible as written. | Kept as written. `validation-1.md`: "Disposition: accepted as written; no change made, so no second comparison is triggered." The reply repeats the reasoning and notes the checker proposed no change. | `disputed` |

I class it `disputed` because the material settles it neither way. It introduces operative temperature only as "ett annat mått" and says nothing about what instrument measures it, so neither the generic reading nor the trial-specific one is established by a supplied statement. Read as an ordinary reader would, in a paragraph that has just described this trial's six wall-mounted sensors and that states "Försöket mätte bara lufttemperatur" two sentences later, the clause is defensible; the repair the checker mentions without proposing (naming the trial's sensors in the second clause) would close the question at no cost, so it stays worth recording. The writer's disposition is reasoned from the text rather than asserted, which is what a disposition should be — though that reasoning is an argument I weigh, not evidence.

**Was a real defect I found under F1 seen by no checker?** No. I found no F1 defect, so there is nothing the comparison missed. I note that the checker's coverage matched my own reading at the places where a slip was most likely — the dropped "totalt … registrerade" in the standfirst, *dygn* against *dag*, "eventuella justeringar" against "Inga justeringars effekt", and the definite-for-indefinite shifts — and reached the same conclusions on each by the same evidence.

## 12. Remaining findings

The delivery account reports none: "**Inga avvikelser återstår.** Inga översättningsavvikelser heller: källa och måltext är båda på svenska, och citatet är ordagrant återgivet."

It does report, beside the draft, the one item the comparison raised and the writer declined, quoted here in full as the account carries it:

> Granskaren reste en redaktionell fråga, inte en avvikelse: meningen "En givare mäter temperaturen där den sitter, och den mäter luft" fortsätter i materialets generella singular, medan stödet för andra ledet ("försöket mätte bara lufttemperatur") är sagt om just det här försöket. Jag lät meningen stå.

- **Passage:** "En givare mäter temperaturen där den sitter, och den mäter luft."
- **What the material carries instead:** "En givare mäter temperaturen där den sitter." (generic) and, separately, "försöket mätte bara lufttemperatur." (this trial). The material makes no general statement that a sensor measures air.
- **Proposed repair:** none was proposed; the checker mentioned that naming this trial's sensors in the second clause would close the question without touching anything else.

Under `F1` I do not treat this as a defect, for the reason given in §11: the material settles neither reading, and in context the clause is defensible. The text is therefore not labelled as carrying a remaining quality problem, though the clause is the one place a stricter reading could bite.

The account also lists eight things the material does not contain and the article therefore does not say (duration below the threshold, whether pupils were cold, ventilation and perceived temperature, any comparison figure, any cause, whether adjustments were made, whether the November trial happens, who the author is). Each of those is a limit of the material correctly respected in the prose, not a finding against it.

## 13. Class of the run

**`valid delivery`.** One complete comparison of the current prose ran, it returned no finding, the single item it raised was recorded, reasoned and declined without a change, and the prose delivered is byte-identical to the prose that comparison read (`diff evidence/source-check/draft.md delivered.md` is empty). The delivery account states the byline's origin, the resolved language and locale, the technique's absence and the gaps in the material, and the reply reports the checker's file-write failure and the route the report took instead rather than concealing it. All eight applicable criteria pass; `T2` is skipped for want of a selected technique.
