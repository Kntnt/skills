# Judgement A — article-sv, Redline

Genre `article` (from the text's `kntnt` metadata), so the anatomy's skeleton applies and its counted requirements are judged on the script's figures.

## 1. Changes

Three differences between `redline/work/input.md` and `redline/delivered.md`; nothing else differs.

1. **Headline.** Before: *Mätningen i Björkskolan pekar ut lektioner, inte orsaker*. After: *Björkskolans mätning ringar in tiderna att undersöka*. **Repair of a visible defect and a change to what a claim says.** The defect is real: the input headline repeated the standfirst's verb *pekar ut* and its contrast. The new headline changes the claim's scope — it drops the limit *inte orsaker* and turns the angle from what the measurement cannot say into what it can.
2. **Sensor-placement sentences.** Before: *Två givare satt nära ytterväggar, fyra på innerväggar. Placeringarna dokumenterades, men de jämfördes inte experimentellt.* After: *Två givare satt nära ytterväggar och fyra på innerväggar, placeringar som dokumenterades men inte jämfördes experimentellt.* **Change of taste.** Two sentences merged into one; all three facts survive and no claim changes.
3. **Causal connective.** Before: *Rapporten redovisar därför lektionspass i stället för ett enda dygnsmedelvärde*. After: *Rapporten redovisar lektionspass i stället för ett enda dygnsmedelvärde*. **Change to what a claim says** — its modality: an asserted causal relation between the preceding observation and the report's choice becomes mere adjacency.

## 2. Headings

**Input**

- `# Mätningen i Björkskolan pekar ut lektioner, inte orsaker` — statement; echo (repeats the standfirst's verb *pekar ut* and its *men förklarar inte varför* contrast).
- `## Givaren mäter luften på sin egen plats` — statement.
- `## Ett värde under gränsen säger inte hur länge` — statement. Not an echo: the first sentence under it is *I rapporten Mätförsök i Björkskolan, daterad 12 mars 2026, står att …*, which it does not repeat.
- `## Två metodval styr vad siffrorna betyder` — statement.
- `## Koppla temperaturen till när rummen används` — statement.

**Returned text**

- `# Björkskolans mätning ringar in tiderna att undersöka` — statement; no echo (the standfirst's verb *pekar ut* is no longer repeated); no overclaim — Elin Rask's quoted *Vi vet när vi behöver titta närmare* and the 14 flagged lesson periods carry it.
- `## Givaren mäter luften på sin egen plats` — statement.
- `## Ett värde under gränsen säger inte hur länge` — statement.
- `## Två metodval styr vad siffrorna betyder` — statement.
- `## Koppla temperaturen till när rummen används` — statement.

No heading is a label, a colon construction or a question; none overclaims.

## 3. Criteria on the returned text

### G1 — pass

The named reader is a municipal property manager who knows heating but not measurement, and the text tells that reader exactly what a four-week trial buys: *Siffran 14 av 120 är därför ett antal, inte ett omdöme: att avgöra om det är mycket eller lite kräver ett jämförelsetal som mätningen inte ger.* The angle — what a short trial can and cannot say — holds from the standfirst to the closing advice. Journalistic craft is present and correct: a dated, named report (*Mätförsök i Björkskolan*, 12 mars 2026), an attributed quotation, and refusals stated as refusals (*Den säger heller inte om eleverna frös*). The reader leaves able to read such a report without over-reading it.

### G2 — pass

The parts appear in the anatomy's order and each does its own job. The script's `parts` shows a headline of 52 characters and 7 words (within the 20–70-character requirement), a standfirst of 45 words in 1 paragraph (within the 60-word maximum and the single-paragraph requirement), a byline *Av Thomas Barregren*, a lead of 46 words in 1 paragraph placed before the first H2, four sections each with at least one paragraph (3, 3, 2, 3), and `"other": []` — no part out of place. The standfirst stands alone: it names the trial, the finding and the offer (*så här kan du komplettera det*) without the body. The lead begins the work by supplying the motive (*ville veta om klagomålen på kall luft sammanföll med låga temperaturer*). The body explains. The ending meets the lead's expectation with a non-commercial next step: *är det värt att bestämma redan nu vad som ska noteras vid sidan av temperaturen*. The byline is filled, so the missing-byline report does not arise. The headline now states its angle without repeating the standfirst's wording.

### P1 — pass

Unfamiliar concepts arrive before use: *Operativ temperatur är ett annat mått, som väger in både luftens temperatur och värmestrålningen från omgivande ytor* precedes the point it supports, and *kontorets egen arbetsgräns för försöket. Den är inget påstående om ett rättsligt krav* separates a working threshold from a legal one before the number is passed on. Conclusions stay proportionate to visible support — *Ett enda värde strax under gränsen räknas likadant som en hel lektion under den.* Useful technical substance remains: five-minute sampling, two outer-wall and four inner-wall sensors, air versus operative temperature, lesson periods versus a daily mean. One transition is now weaker than it was: with *därför* gone, *Ett medelvärde för hela dygnet kan dölja variation under lektionerna. Rapporten redovisar lektionspass …* leaves the link to adjacency. The reader still makes it; the loss is small.

### W1 — pass

Every counted figure is the script's, on the returned text. Headline 52 characters and 7 words — inside the requirement of 20–70 characters and inside the *should* of eight words and 60 characters. Standfirst 45 words, 1 paragraph; lead 46 words, 1 paragraph. Subheadings 38, 44, 39 and 43 characters, all under the 70-character requirement. No heading below the second level (`"other": []`). Sections of 3, 3, 2 and 3 paragraphs — the *should* of at most three is met throughout, and `typical.sections_of_two_or_three_paragraphs` is 4 of 4 sections. The longest paragraph is 50 words, under the 80-word *should*. `typical.paragraphs_of_two_or_three_sentences` is 12 of 13 paragraphs, so the *most* holds across the text. `conforms` is `true` with `failures: []` and `norms: []`. The standfirst opens on *Fastighetskontoret* and the lead on *I*, so the different-first-word *should* is met, and the body covers what the standfirst promises. One qualitative concern, not a failure: the lead's first clause restates the standfirst's first sentence nearly item for item (*temperaturgivare i sex klassrum på Björkskolan*), so a reader entering at the lead reads the same facts twice before the lead's own contribution — the January date, the motive and *smalare än det kan se ut* — arrives.

### L1 — pass

The prose reads as native Swedish, not translated English: *Ett underlag utesluter ingenting som det inte har mätt*, *Siffran 14 av 120 är därför ett antal, inte ett omdöme*, *Planerar du ett eget mätförsök, är det värt att bestämma redan nu*. Verb-second order, the inverted conditional clause and the compounds (*dygnsmedelvärde*, *användningstiderna*, *arbetsgräns*) are all idiomatic. The new headline's *ringar in* is ordinary Swedish idiom for delimiting what to look at.

### L2 — pass

Swedish locale mechanics govern throughout: the date form *12 mars 2026* and *I januari 2026*; the temperature written out as *20 grader Celsius*; the speech dash *– Vi vet när vi behöver titta närmare* for quoted dialogue; the spaced en dash for parentheses (*ett underlag – smalare än det kan se ut*); lower-case month and no comma before *men* misuse. No new factual date and no currency conversion were introduced — no currency appears.

## 4. T2 — skipped

The returned text's `kntnt` metadata reads `technique: none`, and the reply states *Teknikvärdet där är `none` … så genren fick inte bidra med någon berättarteknik*. No technique was selected, so nothing is judged under this criterion.

## 5. R1 — fail

**What the Skill got right.** The account is accurate and complete on every change it made. All three differences in section 1 are reported; nothing was changed outside the reported findings; voice, quotations, the report's title and date, the 14-of-120 figure and every limitation sentence survive byte for byte. One of the three findings is a genuine visible defect: the input headline repeated the standfirst's verb *pekar ut* and its contrast, which the anatomy forbids, and the repair removed the repetition without overclaiming. The reply's candour on the side effect is exemplary — it states that *inte orsaker* left the headline, names where the limit still stands (*men förklarar inte varför* in the standfirst, and Rask's quotation), and invites the reader to weigh it. The claim change at *därför* is reported precisely and as a claim change. No unsupported fact was introduced, no locale was altered, no mechanical rewriting was smuggled in, no finding was left unreported, and no side effect went unnamed.

**Why it fails anyway.** The script records the input as clean — `conforms: true`, `failures: []`, `norms: []` — and two of the three changes rewrote passages of that clean text.

- The sentence merge in the first paragraph under *Givaren mäter luften på sin egen plats* is justified in the reply as *tre meningar på 8, 8 och 7 ord, vilket bryter mot anatomins krav på att meningslängden varierar inom stycket*. Per-sentence word counts are not measured in either JSON file, so that count is not the script's and I do not produce one; what the script does record is that the input met every requirement it measures. A finding stated as a breach of a requirement (*krav*) against a text the script reports as conforming, applied to one paragraph of thirteen, is a wrong finding, and the passage it altered already worked.
- The removal of *därför* was diagnosed as a reason *som texten ingenstans ger stöd för*. On the text alone, the immediately preceding sentence is that support: *Ett medelvärde för hela dygnet kan dölja variation under lektionerna.* Removing the connective changed what the sentence claims — asserted causation became adjacency — on a ground the text visibly supplies.

**Visible defect not addressed.** The lead's opening restates the standfirst's opening almost item for item (*temperaturgivare i sex klassrum på Björkskolan*, four weeks), which is the text's one real complementarity weakness. The single correction round went to a headline echo, a sentence merge and a connective instead.

**Removals and changed claims, against the Skill's own account.** Headline rewrite — reported, and reported accurately, including the loss of *inte orsaker*. *därför* — reported, and reported accurately as the one proposition removed. Sentence merge — reported, with the accurate statement that no claim changed. There is no unreported change and no irreparable finding was claimed. The failure is one of judgement about what needed changing, not of disclosure.

## 6. Source loss

Separate from every criterion above; the Skill could not see `write/work/source.md`.

- **The causal relation at *därför* was in the source.** The source reads: *Ett medelvärde för hela dagen kan dölja variation under lektionerna. Rapporten redovisar därför lektionspass i stället för ett enda dygnsmedelvärde.* The change struck that *därför*, so a causal statement the reporting material made explicit is now only implied by sentence order. The source-blind reviewer read the word as an unsupported attribution; the source had in fact supplied it.
- **The headline's limit was a source-level caution.** The source's *Forbidden inferences* list opens with *Ingen besparing, bättre hälsa, orsak till kyla … följer av materialet.* The input headline carried that caution in the headline itself (*inte orsaker*); the returned headline does not. The limit survives in the standfirst (*men förklarar inte varför*) and in Rask's quotation (*Vi vet ännu inte varför det blev kallt just då*), so nothing in the text now claims a cause — but the most-read line no longer states the limit, and the Skill named this loss itself.
- No other change touched a stated caveat, a careful formulation or a named limit. The sensor-placement merge preserved *dokumenterades men inte jämfördes experimentellt* intact.
