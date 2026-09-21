# Judgement B — `article-pac` / write

Genre: `article` (the text's `kntnt` metadata and the brief's "webbartikel" agree), so the anatomy applies as a requirement, not as description.

## 1. Outcome

**Delivered.** The reply carries the complete draft in a fenced block and states "The draft is delivered with known defects."

**Two source comparisons, both completed.** `evidence/source-check/report.md` ends "**Complete.** The whole draft was compared against the whole of the supplied material"; `evidence/source-check-2/report.md` ends "Comparison complete. The whole draft was accounted for". The two `checker-prompt*.txt` files are the two separate dispatches, each naming its own scratch directory (`source-check`, `source-check-2`), and each report names its own draft and material file. The reply's account agrees: "Two comparisons ran and both completed."

**The delivered prose is byte-identical to the last prose a checker saw.** `evidence/source-check-2/draft.md` and `delivered.md` are identical byte for byte (`diff` reports no difference), and `evidence/draft.md` is identical to both. Between the two comparisons the prose did change, in exactly the two places the first report's three findings named: `evidence/draft.md`/`source-check-2/draft.md` differ from `source-check/draft.md` only at the two paragraphs of the first H2 section, where "Each sensor logged a value every five minutes" became "Values were logged every five minutes", "the trial never compared them against one another" became "they were never compared experimentally", and the split-off sentence "The report makes no claim about any legal requirement." was folded back into "…, not a claim about a legal requirement." Those are the first report's F2, F3 and F1 repairs and nothing else. No repair was made after the second comparison; the reply says so explicitly ("prose changed after it would be prose no comparison has read"), and the file comparison bears it out.

There is no separate dispositions file under `evidence/`; the reply's "What was checked" paragraph is the only disposition record, and it is consistent with the draft files.

## 2. Headings

- `# A four-week trial shows when to look closer` — **statement**
- `## Fourteen of 120 lesson periods held a reading below 20 degrees` — **statement**
- `## Ventilation, draught and radiant heat went unrecorded` — **statement**
- `## A count of periods is not a measure of how cold it got` — **statement**
- `## Pair the readings with usage times before changing the controls` — **statement**, **overclaim**

Notes on two borderline marks.

*Headline, not marked `echo`.* It shares the noun phrase "a four-week trial" with the standfirst's second sentence ("This is what a four-week trial at one school established"), but the propositions differ: the headline says the trial identifies which periods to examine, the standfirst says what the sensors can and cannot tell. A shared subject noun is not a repeated phrasing of the standfirst's claim.

*Fourth subheading, marked `overclaim`.* The material carries the recommendation as Rask's — "**Hon rekommenderar** att koppla temperaturserier till användningstider innan man ändrar styrningen" — and the section carries it at that strength ("she recommends pairing the temperature series with the times the rooms are used"). The bare imperative heading carries it at a higher strength, as the article's own instruction. That is what the mark records; it is evidence, not a verdict, and see G2 for why it does not fail there.

The second subheading and the second paragraph beneath it repeat almost the same words ("Ventilation, draught and radiant heat went unrecorded" / "Ventilation, draught and perceived temperature were not measured at all"). This is not an `echo` under the definition, which is fixed on the *first* sentence under the heading — that sentence is "A sensor reports the temperature of the air at the point where it is mounted" — but it is recorded here as a rhythm observation for W1.

## 3. F1 — **fail**

Most of the text stays inside the material, and the passages where a lesser draft would have slipped are the ones this draft holds hardest: it declines the forbidden characterisation explicitly ("Nor does the trial supply anything to set that figure against — no norm, no target, no capacity — so it is a count with its exclusions rather than a verdict"), it leaves the cause open, it keeps "at least one reading" every time the figure appears, it attributes the count to the report by name and date, it preserves "ännu" in "no adjustment has yet had its effect measured", and it preserves the undecided funding. The quotation is faithful: "Vi vet ännu inte" is rendered "We still don't know", which keeps the not-yet rather than converting it into a flat denial, and the *Vi vet … Vi vet ännu inte* antithesis survives.

It fails on one passage.

**Standfirst — "Temperature sensors in six classrooms can tell a property manager when the air dropped below a chosen limit".** The material says a sensor reports one place and one quantity — "En givare mäter temperaturen där den sitter" — and that the trial measured only air temperature at those points, with two of the six sensors by exterior walls. What the report states is a count of periods containing *at least one* sampled reading below the limit — "14 av totalt 120 registrerade lektionspass innehöll **minst en mätning** under 20 grader Celsius" — recorded "var femte minut", and the report is explicitly silent on duration: "Den säger inte hur länge temperaturen låg under gränsen." The draft's sentence claims two things past that. "The air", unqualified, is the air of the classroom rather than the air at one point on one wall; and "when … dropped below" claims the occasion of a crossing, which a five-minute sample cannot supply and which the report does not report. The draft's own third section states the distinction the standfirst blurs — "A sensor reports the temperature of the air at the point where it is mounted, and nothing else about the room" — so the text is at odds with itself, with the wider claim in the part a busy reader reads first. Reader effect: a property manager is licensed to take the trial as having established that rooms went cold at identifiable moments, which the material does not support and the body then denies.

Two further changes I examined and do **not** count as failures:

- "The report does not say how long any reading stayed under the limit" narrows the source's silence ("hur länge **temperaturen** låg under gränsen") from the temperature to a discrete sample. It claims an absence of *less* than the source does, not more, and the two sentences that follow foreclose any aggregate reading ("Fourteen out of 120 counts the periods with at least one reading under the limit, and nothing beyond that"). It is a weakened caveat rather than an unsupported assertion, and the weakening is repaired by its own context.
- "left them there for four weeks" attaches to the sensors' stay a duration the material dates only for the recording ("Värden registrerades var femte minut under fyra veckor"). It is an unsupported circumstantial detail, and under the Claims contract duration is a claim; but the sensors were demonstrably present for those four weeks, so nothing the reader takes from the sentence is false. It is a defect of precision with no reader consequence, and I do not rest the verdict on it.

Kept apart from absent: the material is silent on who complained and when, on the cause of the cold, on any effect of the walkthrough, and on the funding decision; the draft asserts none of these and states the last three as open, which is correct.

Translated terms checked in both directions: *arbetsgräns* / "working limit", *lektionspass* / "lesson period", *luftdrag* / "draught", *upplevd temperatur* / "perceived temperature", *operativ temperatur* / "operative temperature", *styrningen* / "the controls", *vaktmästare* / "caretaker", *driftteknikern* / "operations technician", *finansiering* / "funding". In this context nothing falls under one and not the other. The report title is left in Swedish and italicised, which is right for an actual document. No natural gender is asserted anywhere the Swedish does not carry it: "she recommends" rests on *Hon*, and the caretaker takes no pronoun.

## 4. G1 — **pass**

The named reader is a municipal property manager who knows heating systems and not measurement technique, and the brief's angle is what a short trial can and cannot say about the heat in a school. The text does that job. The reader learns what was measured and how (six classrooms, five-minute logging, four weeks, two sensors by exterior walls and four on interior walls, placements documented but "never compared experimentally"); what was not measured ("Ventilation, draught and perceived temperature were not measured at all", and operative temperature explained as a different quantity); what the headline figure does and does not carry ("Fourteen out of 120 counts the periods with at least one reading under the limit, and nothing beyond that"); and what to do next ("Before the controls are changed, she recommends pairing the temperature series with the times the rooms are used"). The angle is held from the headline to the last section and never drifts into a savings, health or cause story. The brief's "Ingen kommersiell uppmaning" is honoured: the closing step is an operational one, with no offer, link or contact route anywhere in the text.

Craft is present and appropriate: attribution by document name and date, one quotation placed where it carries the argument rather than decorating it, and the limits stated as the substance of the piece rather than appended as a disclaimer.

## 5. G2 — **pass**

The anatomy applies (genre `article`) and the script reports `"conforms": true`, `"failures": []`, `"norms": []`.

Parts, in order, each doing its own job:

- **Headline** — `"characters": 43`, `"words": 8` (script), inside 20–70 characters. It states the angle of the whole text and is understood alone.
- **Standfirst** — `"words": 49`, `"paragraphs": 1` (script), inside the 60-word limit and one paragraph as required. It stands alone: read by itself it gives the instrument, the school, the limit, what is not available and the article's plan.
- **Byline** — "By Thomas Barregren". The brief states "Ingen byline är given", so the byline names the invoking user, and the delivery account states it in as many words: "**The byline carries your name.** The brief says 'Ingen byline är given', so the author is you." That is exactly what the criterion asks a Write run to do.
- **Lead** — `"words": 53`, `"paragraphs": 1` (script), one paragraph, and it stands before the first H2 in the text. It begins the work rather than restating the standfirst: it gives the occasion and the office's actual question, then turns — "The readings answer a narrower question than that one."
- **Sections** — four, each with `2` paragraphs (script `parts.sections`), so each has at least one. Subheadings measure `62`, `53`, `54` and `63` characters (script), all inside 70. The body is explanatory throughout.
- **Ending** — the closing paragraph supplies the useful next step the explanation supports, non-commercial as the assignment requires, and it meets the expectation the standfirst set: the standfirst promised "what to record before the controls are changed", and the ending delivers precisely that, with the next trial and the undecided funding as the honest remainder.

The fourth subheading's shift of whose recommendation it is (marked `overclaim` above) does not fail this criterion. The text does carry the recommendation; what differs is attribution, and the section attributes it to Rask within the same two paragraphs. An imperative subheading standing over a section that attributes the advice beneath it is an ordinary solution in instructional prose, and scoring it a failure would be scoring a preference between two valid editorial solutions.

## 6. P1 — **pass**

The reasoning is followable by a reader who knows boilers and not instruments. The one unfamiliar concept is introduced before it is used and in the reader's terms: "Operative temperature — a measure that takes in both the air temperature and the heat radiating from the surrounding surfaces — is a different quantity, and the trial recorded air temperature only." The distinction between a point and a room is made the same way, in a sentence rather than a definition: "A sensor reports the temperature of the air at the point where it is mounted, and nothing else about the room."

The transitions are real, not connective filler. The lead opens a question — "The readings answer a narrower question than that one" — and the last section closes it by name: "Which lesson periods to examine, then, is the narrower question these four weeks answer." The third section's two paragraphs move from what the report is silent about to why the count cannot be graded.

Conclusions stay proportionate to visible support. The strongest sentence in the piece is a refusal: "so it is a count with its exclusions rather than a verdict." Technical substance survives the simplification — the five-minute interval, the exterior/interior split, the uncompared placements, air versus operative temperature, and why lesson periods are reported instead of a daily mean are all still in the text and all doing work.

One thing left implicit: the article states that two sensors stood by exterior walls and that the placements were never compared experimentally, but never draws out for this reader why that pairing matters. It is recoverable from the point-versus-room sentence in the next section, so it is a qualitative observation rather than reader loss.

## 7. W1 — **pass**

A web reader can orient and enter, and nothing is fragmented into note form. The script's figures: `"paragraphs": 10` with `"paragraphs_of_two_or_three_sentences": 9`, and `"sections": 4` with `"sections_of_two_or_three_paragraphs": 4`. Both *most* statements are therefore satisfied across the whole text, and the one paragraph outside the typical band — the closing paragraph, `"sentences_estimate": 4`, `"words": 66` (script) — is not judged against, since *most* never fails a single paragraph.

No norm is departed from: the script reports `"norms": []`, so no paragraph exceeds 80 words (the longest measured is `66`), no section exceeds three paragraphs (each has `2`), no heading falls below the second level, and the headline is `43` characters and `8` words — inside 60 characters and not past eight words.

The standfirst and the lead complement rather than duplicate, and they open on different first words: standfirst `"Temperature sensors in six classrooms…"`, lead `"In January 2026 the property office in Lervik…"` (script `parts.standfirst.text`, `parts.lead.text`). The body is complete against the standfirst: the standfirst's three promises — what the trial established, what it did not measure, what to record before the controls are changed — are discharged by the first, second and fourth sections respectively, with the third adding the qualification on the figure.

Headings are informative and carry the argument on their own; a reader scanning only the four subheadings gets the article's case in order. The one rhythm blemish is the near-repetition noted above, where the second section's subheading and its second paragraph open on almost the same three words. It costs a beat, not comprehension.

## 8. L1 — **pass**

The prose reads as English written by someone writing English. "Complaints about cold air had come in" uses the past perfect where the sequence needs it; "went unrecorded", "stood near exterior walls", "went through the ventilation and heating times with the school's caretaker" and "before the controls are changed" are all native collocations. "Nor does the trial supply anything to set that figure against — no norm, no target, no capacity" is idiomatic inversion and understated in the British register the resolved locale asks for, and it lets the refusal carry its own weight without an intensifier.

No Swedish phrasing is imported. The obvious traps are avoided: *lektionspass* becomes "lesson period" rather than a calque, *vaktmästare* becomes "caretaker" rather than "janitor" or "custodian", *driftteknikern* becomes "operations technician", and *styrningen* becomes "the controls". The quotation is spoken English, contraction and all — "We still don't know why it got cold just then" — and follows English word order rather than the Swedish.

## 9. L2 — **pass**

The resolved locale is `en_GB` (the text's own metadata, `language: en_GB`), and it governs throughout.

- Spelling: "draught" for *luftdrag*, not "draft" — the British form, and the one that distinguishes the phenomenon from a document. No `-ise`/`-ize` word appears, so no house-style inconsistency is possible; the `-yse` group does not occur.
- Punctuation: single quotation marks as the outer mark — `'We know when we need to look more closely. … ' Rask said` — which is the British convention the resolved guidance names, and the document uses no other quoting convention that would contradict it. The spaced em dash is used three times and used the same way each time.
- Dates: "12 March 2026" in day–month–year order, from *12 mars 2026*; "January 2026" and "November" as the material has them, with no year invented for November.
- Numbers: "14 of the 120" mid-sentence, "Fourteen of 120" and "Fourteen out of 120" where the figure opens a heading or a sentence — the standard convention, applied consistently. "20 degrees Celsius" and "Twenty degrees" name the unit the material names, with no conversion to another scale and no currency anywhere to convert.
- Established variation preserved: the Swedish proper nouns Lervik, Björkskolan and the report title *Mätförsök i Björkskolan* are left as they stand.

## 10. T2 — **pass**

A technique is named: the delivered text's frontmatter carries `technique: pac`, and the reply states it came from `--technique=pac`. So PAC is judged.

- **Point / factual starting point and question.** The lead sets both: a four-week installation in six classrooms in January 2026, and the office's actual question — whether complaints about cold air "coincided with low temperatures during lesson time" — followed by the pivot that makes the article, "The readings answer a narrower question than that one."
- **Analysis.** Three sections of it, and each takes the question somewhere. What the trial recorded and what the report states; what a sensor measures and what operative temperature would have measured instead; what a count of periods carries and what it cannot ("Nor does the trial supply anything to set that figure against — no norm, no target, no capacity"), including why the report gives lesson periods rather than a daily mean.
- **Conclusion, warranted.** "Which lesson periods to examine, then, is the narrower question these four weeks answer", carried through to the operational step — pair the series with usage times before changing the controls — with the effect of any change stated as unmeasured and the next trial's funding stated as undecided.

No crisis is invented and no triumph is claimed: the cold has no cause in this text, the count has no grade, and the quotation is placed exactly where the argument turns from *when* to *why*. The answer is given early, in the standfirst, which the criterion allows.

## 11. Checker findings

**First comparison — `evidence/source-check/report.md`, three findings, all repaired.**

1. **F1** — passage: "Twenty degrees was the office's own working limit for the trial. **The report makes no claim about any legal requirement.**" Alleged: the source attaches the denial to the 20-degree limit — "Gränsen 20 grader var kontorets egen arbetsgräns för försöket, **inte ett påstående om ett rättsligt krav**" — and the draft re-attached it to the whole report. Writer: repaired, to "…for the trial, not a claim about a legal requirement", which is the source's own structure. My class: **supported** — the Swedish qualification governs the threshold, and the material nowhere says what else the report may contain.
2. **F2** — passage: "**Each sensor logged a value every five minutes** for the whole period." Alleged: the source is impersonal about the values — "Värden registrerades var femte minut" — and the draft distributed the interval over each of six sensors. Writer: repaired, to "Values were logged every five minutes for the whole period." My class: **supported** — a logger polling six sensors in rotation satisfies the Swedish and defeats the draft, and nothing supplied excludes it.
3. **F3** — passage: "the placements were documented, but **the trial never compared them against one another**." Alleged: "experimentellt" governs the negation in "Givarnas placering dokumenterades men jämfördes inte experimentellt", and the draft negated comparison of every kind. Writer: repaired, to "…but they were never compared experimentally." My class: **supported** — a non-experimental reading-off of the series is compatible with the material and defeats the unqualified negation.

**Second comparison — `evidence/source-check-2/report.md`, three findings and one editorial question, none repaired, all reported.**

4. **F1** — passage: "Temperature sensors in six classrooms can tell a property manager **when the air dropped below a chosen limit**." Alleged: the material supports a sampled reading at the point where a sensor sits, not the room's air and not the moment of a crossing. Writer: not repaired; reported in the delivery account with the repair "when a reading fell below a chosen limit". My class: **supported** — "En givare mäter temperaturen där den sitter", "minst en mätning", "var femte minut" and "Den säger inte hur länge temperaturen låg under gränsen" together bear the allegation out, and the draft's own third section states the distinction.
5. **F2** — passage: "The report does not say how long **any reading** stayed under the limit." Alleged: the source's silence is about the temperature — "hur länge **temperaturen** låg under gränsen" — and the narrower wording leaves an aggregate duration apparently available. Writer: not repaired; reported with the repair "how long the temperature stayed under the limit". My class: **disputed** — the material settles the facts but not the implicature; the draft asserts strictly less than the source and the following sentences close the opening the checker fears. The repair is an improvement, not a correction of a false claim.
6. **F3** — passage: "the property office in Lervik fitted sensors in six classrooms at Björkskolan and **left them there for four weeks**." Alleged: the material dates four weeks of recording, not of installation. Writer: not repaired; reported with the repair "and recorded there for four weeks". My class: **supported** — "Värden registrerades var femte minut under fyra veckor" is the only place four weeks appears, and the material never says when the sensors came down. Real, and trivial in effect.
7. **E1**, reported as an editorial question rather than a finding — passage: the subheading "Pair the readings with usage times before changing the controls". Alleged: the article issues in its own voice a recommendation the material gives as Rask's ("**Hon rekommenderar** att koppla temperaturserier…"). Writer: reported in the delivery account, explicitly as not a defect, with no repair. My class: **disputed** — the material fixes whose recommendation it is but leaves open whether a heading over a section that attributes it may carry it plainly. I marked the heading `overclaim` as evidence and did not fail G2 on it.

**Did a checker miss a real defect I found?** No. The only F1 failure I record — the standfirst's "when the air dropped below a chosen limit" — is the second comparison's F1, found and reported. Two things I examined and cleared were also examined by a checker: the generic "A sensor reports the temperature of the air", which would fail as a universal about instruments but is about this trial's sensors in its context, and the counterfactual "could have hidden variation within lessons" against the source's general "kan dölja". One thing no checker raised and I do not count as a defect: the material's scope limitation — "Mätningarna omfattar bara dessa sex rum och dessa fyra veckor" — is never stated as a limitation, only enacted, but the text generalises nowhere, so there is no claim for that caveat to qualify.

## 12. Remaining findings

The delivery account reports three, each with the passage, the material and a proposed repair.

1. **Standfirst — "can tell a property manager when the air dropped below a chosen limit."** The account quotes what the material carries instead: "En givare mäter temperaturen där den sitter", "minst en mätning under 20 grader Celsius", "Den säger inte hur länge temperaturen låg under gränsen", and gives the concrete case — a wall-adjacent sensor reading 19.6 °C while the room is at 21 °C, and a dip between two samples never seen. Proposed repair: "when a reading fell below a chosen limit". **This is a defect of the text**, and it is the one F1 fails on.
2. **Third section — "The report does not say how long any reading stayed under the limit."** The material carries "Den säger inte hur länge **temperaturen** låg under gränsen". Proposed repair: "how long the temperature stayed under the limit". **A weakened caveat rather than an unsupported claim**; I do not count it as an F1 defect, for the reason given there.
3. **Lead — "left them there for four weeks."** The material carries "Värden registrerades var femte minut under fyra veckor" and dates nothing else. Proposed repair: "and recorded there for four weeks". **A real but inconsequential defect** — an unsupported circumstantial duration with no false conclusion available to the reader.

The account also names E1, the fourth subheading, and states it is not a defect but an editorial choice. I agree, and marked the heading as evidence rather than as a failure.

## 13. Class of the run

**`valid delivery`.**

The run delivered, and the prose it delivered is byte-identical to the draft its second and last comparison read — `evidence/source-check-2/draft.md` and `delivered.md` do not differ — so the delivered text is the text a completed comparison read in full. The three findings that comparison left open were not repaired, and every one of them is reported beside the draft with its passage, the material that bears on it and the smallest proposed repair, which is what the contract requires of a finding a run does not repair. The reply also explains why no repair was attempted: prose changed after the last comparison would be prose no comparison has read. The text carries a remaining quality problem — the standfirst overclaim under F1 — but the run's handling of it is correct, and reporting it is precisely what keeps this a valid delivery rather than a defect concealed.
