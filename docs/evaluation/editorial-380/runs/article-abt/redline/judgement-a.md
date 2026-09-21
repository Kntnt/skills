# Redline judgement A — row `article-abt`

Genre from the text's own `kntnt` metadata: `article`. The fixed skeleton applies, and its counted requirements are judged on the script's figures.

## 1. Changes

Two differences between `redline/work/input.md` and `redline/delivered.md`, and no others (line-for-line comparison of the two files shows changes at two lines only).

| # | Before | After | Kind |
|---|---|---|---|
| 1 | `## Effekten av eventuella justeringar är inte mätt` | `## Uppföljningen är planerad men ännu inte finansierad` | **Change to what a claim says** — scope and subject. The old subheading asserted, as the section's own statement, that adjustments may have been made and that their effect is unmeasured. The new one asserts that the follow-up is planned and unfunded. It is at the same time **the repair of a visible defect**: the section under the heading contains no sentence about adjustments or about an unmeasured effect, so the old heading claimed more than the text it headed carried. |
| 2 | `— Vi vet när vi behöver titta närmare. …` (U+2014 em dash) | `– Vi vet när vi behöver titta närmare. …` (U+2013 en dash) | **Mechanical correction** — Swedish locale mechanics: the speech dash before a quoted line is the Swedish *tankstreck*, not the English em dash. |

No other word, sentence, paragraph, heading, frontmatter key or byline was touched.

## 2. Headings

### Input (`redline/work/input.md`)

- H1 `Björkskolans mätning visar när, inte varför` — **statement**. (It shares the word *varför* with the standfirst's "svarar inte på varför värdena såg ut som de gjorde", but the phrasing is its own, so not **echo**.)
- H2 `Placeringen jämfördes aldrig experimentellt` — **statement**
- H2 `Försöket mätte varken luftdrag eller strålning` — **statement**
- H2 `Rapporten säger hur ofta, inte hur länge` — **statement**
- H2 `Effekten av eventuella justeringar är inte mätt` — **statement**, **overclaim**. The section it heads contains three paragraphs — Rask reviewing the ventilation and heating times with the caretaker, a November trial with undecided funding, and the Rask quotation. None of them says that adjustments were made, and none says that any effect is unmeasured. The heading therefore carries a claim the text under it does not carry.
- H2 `Lägg användningstiderna bredvid temperaturserien` — **statement**

### Returned text (`redline/delivered.md`)

- H1 `Björkskolans mätning visar när, inte varför` — **statement**
- H2 `Placeringen jämfördes aldrig experimentellt` — **statement**
- H2 `Försöket mätte varken luftdrag eller strålning` — **statement**
- H2 `Rapporten säger hur ofta, inte hur länge` — **statement**
- H2 `Uppföljningen är planerad men ännu inte finansierad` — **statement**. Not **overclaim**: the section states "Ett nytt försök planeras till november" and "Finansieringen är inte beslutad". Not **echo**: the first sentence under it is "Driftteknikern Elin Rask gick efter mätperioden igenom tiderna för ventilation och värme tillsammans med skolans vaktmästare", which it does not repeat.
- H2 `Lägg användningstiderna bredvid temperaturserien` — **statement**

No heading in either text is a **label**, a **colon** heading or a **question**.

## 3. G1 — pass

The text does the article's job for a reader who knows heating systems but not measurement technique. The angle is held from the headline "Björkskolans mätning visar när, inte varför" through the lead's "Vad de inte mätte avgör hur långt siffrorna räcker" to the closing "Vad som hände vid just de tidpunkterna ligger utanför vad utrustningen kunde fånga." The reader learns what a four-week sensor run establishes (which lesson slots are worth a closer look) and what it does not (why it was cold, for how long, whether anyone was cold): "Hur länge temperaturen låg under arbetsgränsen framgår inte. Rapporten säger heller ingenting om huruvida eleverna frös." Journalistic craft is present and appropriate — a dated report is named ("Rapporten Mätförsök i Björkskolan, daterad 12 mars 2026"), a named source is quoted, and the count 14 of 120 is given with its own limit stated ("Gränsen på 20 grader var kontorets egen arbetsgräns för försöket, inte ett påstående om ett rättsligt krav"), never characterised as high or low. The reader can act: pair the temperature series with room-usage times before touching the control.

## 4. G2 — pass

Every required part is present, in the anatomy's order, and each does its own job. The script's `parts` for the returned text confirms this: `headline` 43 characters / 6 words; `standfirst` 54 words, 1 paragraph; `byline` "Av Thomas Barregren", 3 words; `lead` 51 words, 1 paragraph, standing before the first H2; five `sections`, each with two or three paragraphs; `other: []`. `conforms: true`, `failures: []`.

- **Headline** states the angle and is understood alone; it claims no more than the body delivers.
- **Standfirst** stands alone — it names the measurement, the period, what it points out and what it does not answer, and promises the article's three moves ("vad ett kort mätförsök av det här slaget avgör, vad det lämnar öppet och vad som rimligen blir nästa steg"). All three are covered in the body.
- **Byline** is filled ("Av Thomas Barregren"), so nothing was owed as missing; the returned text leaves it as it stood.
- **Lead** begins the work rather than restating the standfirst: it dates the installation, gives the office's question, names the report and turns to the limit.
- **Sections** are explanatory body, each headed by a subheading that now states the angle of its own section (see §2 for the one that did not, and its repair).
- **Ending** meets the lead's expectation and is the useful next step the explanation supports, non-commercial: "Rask rekommenderar att temperaturserierna kopplas till användningstiderna innan styrningen ändras. Har du egna serier liggande är det där du börjar – lägg tiderna då rummen faktiskt används bredvid kurvan, innan du rör styrningen."

For the article genre the call to action must be the next step the explanation supports; here the explanation is that the series say *when* and not *why*, and the step is to put usage times beside the curve. It follows directly.

## 5. P1 — pass

The reasoning is followable by the named reader and the unfamiliar concept is introduced before it is used: "Operativ temperatur är ett annat mått, som väger in både luftens temperatur och värmestrålningen från omgivande ytor. I Björkskolan registrerades bara lufttemperaturen." The transitions are real rather than decorative — "Var givarna satt är dokumenterat. Men eftersom placeringarna aldrig ställdes mot varandra i ett kontrollerat upplägg går det inte att läsa ut vad väggen betydde för ett enskilt värde" turns documentation into its limit, and "Ett medelvärde för hela dagen kan dölja variation under lektionerna. Rapporten redovisar därför lektionspass i stället för ett enda dygnsmedelvärde" gives the reason for the reporting unit. Conclusions stay proportionate to visible support: the count "14 av sammanlagt 120 registrerade lektionspass" is never turned into a judgement about how cold the school is, and the causal question is explicitly left open by the quoted technician. Useful technical substance remains — sensor placement against outer and inner walls, a five-minute sampling interval, air temperature against operative temperature, lesson slots against a daily mean.

## 6. W1 — pass

Counted requirements, on the script's figures for the returned text: headline 43 characters (inside 20–70); standfirst 54 words (at most 60); the longest subheading is "Uppföljningen är planerad men ännu inte finansierad" at 51 characters (at most 70); every one of the five sections has at least one paragraph; standfirst and lead have `paragraphs: 1` each. `conforms: true`, `failures: []`.

Norms: the script reports `norms: []` — no paragraph over 80 words, no section over three paragraphs, no heading level below the second, no headline past eight words or 60 characters (6 words, 43 characters). Standfirst and lead open on different first words ("Under" / "I").

*Most* statements, read across the whole text: `typical` gives `paragraphs: 14` of which `paragraphs_of_two_or_three_sentences: 12`, and `sections: 5` of which `sections_of_two_or_three_paragraphs: 5`. Both hold across the text; the two paragraphs outside the sentence band are single-sentence paragraphs following their own content and are not failed individually.

For the reader, the subheadings carry the argument on their own — placement never compared, draught and radiation never measured, how often but not how long, follow-up planned but unfunded, and the closing instruction — so the page can be scanned and re-entered without the continuous explanation breaking. No density or fragmentation loss is visible.

## 7. L1 — pass

The Swedish is native in idiom and syntax, with no generic translated-English phrasing. Verb-second order and Swedish subordination are handled naturally throughout: "Men eftersom placeringarna aldrig ställdes mot varandra i ett kontrollerat upplägg går det inte att läsa ut vad väggen betydde för ett enskilt värde." Idiomatic constructions carry the closing: "Har du egna serier liggande är det där du börjar" uses the Swedish conditional inversion and the participial "liggande" the way a Swedish writer would. Domain vocabulary is the ordinary Swedish of the field — *driftteknikern*, *vaktmästare*, *arbetsgräns*, *styrningen*, *dygnsmedelvärde* — none of it a calque.

## 8. L2 — pass

The resolved locale is Swedish (`language: sv`) and governs the mechanics of the returned text. The date is Swedish form without a comma: "daterad 12 mars 2026". Temperature is written out in Swedish style, "under 20 grader Celsius", not with a degree symbol and abbreviation. The month "november" is lower-case, as Swedish requires. The quotation is set in the Swedish newspaper form — speech dash, sentence, attribution after a comma: "– Vi vet när vi behöver titta närmare. Vi vet ännu inte varför det blev kallt just då, säger Elin Rask." That dash is the one thing the Skill changed for mechanics, from U+2014 to U+2013, which is the Swedish *tankstreck*; the closing paragraph's parenthetical dash in "det där du börjar – lägg tiderna" was already the same character and is consistent with it. No factual date and no currency conversion was invented; the text carries no currency.

## 9. T2 — pass

A technique is named in the returned text's own metadata (`technique: abt`), and the reply names it too ("lästes mot genren `article`, tekniken `abt` och språket `sv`"), so the criterion is judged.

- **And** — the situation, stated without drama: "I januari 2026 satte Lerviks fastighetskontor temperaturgivare i sex klassrum i Björkskolan. Bakgrunden var klagomål på kall luft, och kontoret ville veta om klagomålen sammanföll med låga temperaturer under lektionstid."
- **But** — the genuine complication, set at the end of the lead and then developed across three sections: "Vad de inte mätte avgör hur långt siffrorna räcker." The complication is a real limit of the method (placement never compared experimentally, draught and radiation not measured, duration not recorded), not an invented crisis. Nothing claims the school is cold, that pupils suffered, or that a rule was broken.
- **Therefore** — the supported response: "Rask rekommenderar att temperaturserierna kopplas till användningstiderna innan styrningen ändras."

The three relate properly: the response follows from the complication rather than from the situation alone, and it is offered as a next step, not as a triumph. The honest note "Finansieringen är inte beslutad" keeps the resolution at the strength the text can support.

## 10. R1 — pass

**Every change, against the Skill's own account.**

1. *The subheading.* The account reports it explicitly and accurately: "En rättelse gjordes, och den skrev om mellanrubriken över det fjärde avsnittet: 'Effekten av eventuella justeringar är inte mätt' blev 'Uppföljningen är planerad men ännu inte finansierad'." It states the claim that disappeared with the old heading — "att justeringar kan ha gjorts och att effekten av dem inte är mätt" — and gives the reason: "varken några justeringar eller någon omätt effekt nämns i avsnittet under rubriken, så inget påstående i brödtexten följde med bort." That reading of the section is correct: its three paragraphs are the review of timings, the planned November trial with undecided funding, and the quotation, and none of them contains the claim. The account's summary "Inget annat påstående togs bort. Inget påstående fick sin räckvidd, säkerhet, källa, kronologi, orsakslogik eller innebörd förskjuten" matches the two-line comparison of input and delivered.

2. *The dash.* Reported, and accurately: "talstrecket framför Elin Rasks replik var ett engelskt em-streck (—) och är nu ett svenskt tankstreck (–)." The change is exactly that character and nothing else on the line.

**Was the subheading a legitimate finding?** Yes. It is not a *most* count read against a single section, nor a *should* the text had reason to leave, nor a matter of taste: the anatomy's plain requirement is that a subheading is understood on its own without claiming more than the text claims, and the old heading claimed something its section did not carry. Repairing that is not a rewrite. The script's figures do not contradict this — `failures: []` on the input reflects only the counted limits (character and word counts, paragraph counts), which the old heading also met at 47 characters; the defect is the qualitative one the counts cannot see.

**Was the repair the right size?** Yes, and it is the only repair available to a text-only pass. The alternative — keeping the heading and adding a supporting sentence to the body — would have required asserting a fact the Skill has no material for, which it must not do. Replacing the heading with a statement the section already carries ("Ett nytt försök planeras till november", "Finansieringen är inte beslutad") repairs the defect without inventing anything. The result is 51 characters, inside the counted limit.

**Working voice, arguments, quotations and claims outside the findings** are preserved exactly. The Rask quotation is unchanged in wording; every figure (fyra veckor, sex klassrum, var femte minut, 14 av 120, 20 grader, 12 mars 2026) is unchanged; the lead, standfirst, byline and closing call to action are byte-identical to the input.

**Visible defects not addressed.** I find none that rises to a defect. Two small things a stricter pass might have raised, neither of them a reader loss: the report title "Rapporten Mätförsök i Björkskolan" is set without quotation marks or italics, which Swedish practice often marks; and the headline and standfirst share the word *varför*, which is repetition of a word rather than of a phrasing and is doing useful work in both places. Leaving both is defensible.

**Changes of taste to passages that already worked.** None. Neither change touches a passage that worked as it stood.

**Irreparable findings.** The reply reports none — "Inga fynd återstår" — and on the returned text I find no remaining problem that would have needed unavailable material. Consequently no part of G1, G2, P1, W1, L1 or L2 above rests on a defect the Skill reported but could not repair.

**Unconditional rejections.** None is triggered: no unsupported fact was introduced (the new heading restates two sentences already in its section), the locale is right, the mechanical correction is a single locale character and not substantive editing, no finding was left unreported, and there are no incorrect side effects — frontmatter, byline, quotation and every other section are untouched.

## 11. Source loss

*This section is separate from every criterion above. The Skill did not have `write/work/source.md` and nothing here counts against it.*

**Yes — one limit stated in the source is no longer carried anywhere in the text.**

The source material states, as a flat fact about the state of play:

> Driftteknikern Elin Rask gick efter försöket igenom tiderna för ventilation och värme med skolans vaktmästare. **Inga justeringars effekt har ännu mätts.** Nästa försök planeras för november med likadant placerade givare och noteringar om när rummen används; finansiering är inte beslutad.

In the input, that limit survived only in the fourth subheading, "Effekten av eventuella justeringar är inte mätt". The returned text replaces that heading with "Uppföljningen är planerad men ännu inte finansierad", and the body under it never stated the limit, so after the change the article no longer says anywhere that no adjustment's effect has been measured.

This is a real loss of a source-stated limit, and it matters more than usual because the article's whole angle is what the measurement does not establish. It is also a loss the Skill could not have avoided: from the text alone, the heading was an unsupported claim, and the only two repairs are the one it made or the invention of a body sentence it had no material for. The right repair with the source in hand would have been to move the limit into the body — for instance a sentence after the review of timings saying that the effect of any adjustments has not yet been measured — and keep a heading that states it. Nothing else the source requires was removed or altered: the quotation is verbatim in substance, the working limit of 20 degrees is still marked as the office's own and not a legal requirement, "14 av 120" is still given without a high/low characterisation, and the untested items (ventilation, draught, perceived temperature, operative temperature, duration, whether pupils were cold) all remain stated.
