# Redline judgement B — row `article-abt`

Genre from the text's own `kntnt` metadata: `article`. The fixed skeleton therefore applies, with its three strengths (requirement / *should* / *most*) read as the brief sets them out. All counted lines below quote `redline/anatomy-input.json` and `redline/anatomy-delivered.json`.

## 1. Changes

Two differences between `redline/work/input.md` and `redline/delivered.md`. Nothing else differs; the diff is exhaustive.

| # | Before | After | What kind of change |
|---|---|---|---|
| 1 | `## Effekten av eventuella justeringar är inte mätt` | `## Uppföljningen är planerad men ännu inte finansierad` | Repair of a visible defect, and with it a change to what a claim says. The defect: the old subheading carried a claim its own section does not carry — the section says only that Elin Rask went through the ventilation and heating timings with the caretaker, that a new trial is planned for November and that funding is not decided; it says nothing about adjustments having been made, and nothing about any effect being unmeasured. The heading was therefore an overclaim against its section (see **Headings**). The new heading states what the section does hold. The change removes the claim *that adjustments may have been made and their effect is unmeasured* from the text — the only place in the article that claim stood. No body sentence moved or was lost with it. |
| 2 | `— Vi vet när vi behöver titta närmare.` (U+2014, em dash, speech dash before Rask's quotation) | `– Vi vet när vi behöver titta närmare.` (U+2013, en dash) | Mechanical correction, of locale mechanics. Swedish sets a *talstreck* as a *tankstreck* (en dash) with a following space; the em dash is the English form. The input was also internally inconsistent — line 48 of the input already uses U+2013 (`är det där du börjar – lägg tiderna`), so the repair brings the one outlier into line with the text's own practice. The quoted words themselves are untouched, byte for byte. |

No change of taste was made. No paragraph, sentence, figure, name, quotation or section was added, removed or reordered.

## 2. Headings

### Input (`redline/work/input.md`)

| Heading | Marks |
|---|---|
| H1 `Björkskolans mätning visar när, inte varför` | **statement** — a clause saying what the text says (the measurement establishes timing, not cause). No colon, no question. Not **echo**: the standfirst's nearest wording is "svarar inte på varför värdena såg ut som de gjorde", a different formulation, not a repetition. Not **overclaim**: the body carries exactly this, at this strength. |
| H2 `Placeringen jämfördes aldrig experimentellt` | **statement**. Not **echo** — the first sentence under it is "Två av givarna stod nära ytterväggar, fyra på innerväggar", which it does not repeat. Not **overclaim**: the second paragraph states that the placements were never set against each other in a controlled design. |
| H2 `Försöket mätte varken luftdrag eller strålning` | **statement**. Not **echo** — the first sentence under it is "En temperaturgivare svarar på en fråga i taget: hur varm är luften där utrustningen sitter?". Not **overclaim**: the section states that only air temperature was recorded and that ventilation, draught and perceived temperature were outside the measurement. |
| H2 `Rapporten säger hur ofta, inte hur länge` | **statement**. Not **echo** — the first sentence under it is the 14-of-120 sentence. Not **overclaim**: the third paragraph states that duration below the working limit is not reported. |
| H2 `Effekten av eventuella justeringar är inte mätt` | **statement**, **overclaim**. Overclaim because the heading's own text is its section, and that section carries neither a claim that adjustments were made nor any claim about an unmeasured effect. The reader is led to expect a passage about adjustments and their effect, and meets a passage about a review of timings, a planned November trial and undecided funding. Not **echo** — the first sentence under it is the Rask/caretaker sentence. |
| H2 `Lägg användningstiderna bredvid temperaturserien` | **statement** — an imperative clause stating the section's recommendation. Not **echo** by the definition used here: the first sentence under it is "Fyra veckors registrering i sex rum ger ett underlag som pekar ut tidpunkter värda en närmare granskning". (The closing sentence of the second paragraph does restate the heading's advice in other words; that is the section's last line, not its first, so the mark does not apply, and the restatement reads as a call to action rather than as redundancy.) Not **overclaim**: the section attributes the recommendation to Rask and carries it at that strength. |

### Returned text (`redline/delivered.md`)

| Heading | Marks |
|---|---|
| H1 `Björkskolans mätning visar när, inte varför` | **statement**. Unchanged; marks as above. |
| H2 `Placeringen jämfördes aldrig experimentellt` | **statement**. Unchanged. |
| H2 `Försöket mätte varken luftdrag eller strålning` | **statement**. Unchanged. |
| H2 `Rapporten säger hur ofta, inte hur länge` | **statement**. Unchanged. |
| H2 `Uppföljningen är planerad men ännu inte finansierad` | **statement**. Not **overclaim**: the section states "Ett nytt försök planeras till november, med likadant placerade givare och noteringar om när rummen används" and "Finansieringen är inte beslutad", which is precisely what the heading asserts and at the same strength. Not **echo** — the first sentence under it is the Rask/caretaker sentence, whose wording it does not reuse. |
| H2 `Lägg användningstiderna bredvid temperaturserien` | **statement**. Unchanged; marks as above. |

The one marked defect in the input list is the one the Skill repaired, and the repair carries no new mark.

## 3. G1 — pass

The genre does its job for the reader the text addresses: someone running municipal property who knows heating plant and does not know measurement technique. The reader learns what a four-week logging exercise settles and what it does not: "Av sammanlagt 120 registrerade lektionspass innehöll 14 minst en mätning under 20 grader Celsius" is given with its own scope attached — "Gränsen på 20 grader var kontorets egen arbetsgräns för försöket, inte ett påstående om ett rättsligt krav" — so the figure cannot be mistaken for a legal threshold. The angle announced by the headline, "visar när, inte varför", is recognisable in every section: placement documented but never compared, air temperature but not radiation or draught, frequency but not duration, a follow-up planned but unfunded. The journalistic craft is present and appropriate: the report is named and dated ("Rapporten Mätförsök i Björkskolan, daterad 12 mars 2026"), the technician is named and quoted, and no cause, saving or health effect is asserted anywhere. The reader can act: the closing section tells them what to do with series they already hold.

## 4. G2 — pass

The parts appear in the anatomy's order and each does its own job. The script's figures on the returned text, from `anatomy-delivered.json`: `"conforms": true`, `"failures": []`, `"norms": []`.

- **Headline** — `"characters": 43`, `"words": 6`, inside the 20–70-character requirement. It states the angle and is understood alone.
- **Standfirst** — `"words": 54`, `"paragraphs": 1`: within the 60-word requirement and the one-paragraph requirement. It stands alone: situation, what the measurement does and does not answer, and what the article will cover ("vad ett kort mätförsök av det här slaget avgör, vad det lämnar öppet och vad som rimligen blir nästa steg"). It does not repeat the headline's wording.
- **Byline** — `"text": "Av Thomas Barregren"`. An author is named, so there is no missing byline for a Redline run to report and none to leave unfilled. The Skill has no material that would let it check the name, and rightly did not touch it.
- **Lead** — `"words": 51`, `"paragraphs": 1`, and it stands before the first H2. It begins the work rather than restating the standfirst, adding the January 2026 date, the complaints that prompted the trial, and the named, dated report, and it closes on the hinge the article turns on: "Vad de inte mätte avgör hur långt siffrorna räcker."
- **Sections** — five, each with paragraphs (`3, 2, 3, 3, 2` by the script's `parts.sections[].paragraphs` arrays), so the at-least-one-paragraph requirement holds throughout. Subheadings measure `43`, `46`, `40`, `51`, `48` characters, all inside the 70-character requirement. The body is explanatory: "Operativ temperatur är ett annat mått, som väger in både luftens temperatur och värmestrålningen från omgivande ytor" introduces the concept at the point of use.
- **Ending** — "Lägg användningstiderna bredvid temperaturserien" is the useful next step the explanation supports, and only that step: "lägg tiderna då rummen faktiskt används bredvid kurvan, innan du rör styrningen". Nothing commercial is offered, which suits an explanatory article. The lead's expectation — that what was not measured decides how far the numbers reach — is met: the close says the timings the equipment could not capture are what the reader must supply.

The article genre's own demand, an explanatory body plus a non-commercial next step, is satisfied. The one part that did not do its job in the input, the fourth subheading, does it in the returned text.

## 5. P1 — pass

The reasoning is followable by a reader without measurement training. Unfamiliar concepts arrive before they are used: operative temperature is defined in the sentence that introduces it, and the article then says plainly "I Björkskolan registrerades bara lufttemperaturen", so the reader knows what the definition was for. The working limit is explained as the office's own before any inference rests on it. Transitions are real rather than decorative: "Men eftersom placeringarna aldrig ställdes mot varandra i ett kontrollerat upplägg" carries the section's actual reasoning from documented placement to what cannot be read out of it, and "Ett medelvärde för hela dagen kan dölja variation under lektionerna. Rapporten redovisar därför lektionspass i stället för ett enda dygnsmedelvärde" gives the reason before the consequence.

Conclusions stay proportionate to visible support. The 14-of-120 figure is never called high or low and is never attached to a cause; "Hur länge temperaturen låg under arbetsgränsen framgår inte. Rapporten säger heller ingenting om huruvida eleverna frös" marks the two limits explicitly. Useful technical substance remains after the review: the five-minute sampling interval, the split of two external-wall and four internal-wall sensors, the air-versus-operative distinction, the lesson-period rather than daily-mean reporting, and the November trial's design with usage notes.

## 6. W1 — pass

A web reader can orient and enter without losing the continuous explanation or the voice. The script's figures on the returned text: `"paragraphs": 14`, `"paragraphs_of_two_or_three_sentences": 12`, `"sections": 5`, `"sections_of_two_or_three_paragraphs": 5`.

- The *most* statements are read across the whole text and hold: 12 of 14 paragraphs run to two or three sentences, and all 5 sections to two or three paragraphs. The lead's `"sentences_estimate": 4` is a single paragraph and, per the brief, a *most* statement is never failed against one paragraph.
- No *should* is departed from. The longest paragraph the script measures is `"words": 37`, well under 80. The headline is `"words": 6` and `"characters": 43`, under eight words and 60 characters. Only H1 and H2 appear in `parts` — the script records no heading below the second level, and `"other": []`. The standfirst opens on "Under" and the lead on "I", different first words.
- Headings are informative where this genre needs them: each of the five names what its section settles, so a reader scanning the page can find the placement question, the draught-and-radiation limit, the frequency-versus-duration point, the follow-up's status and the recommended next step without reading through.
- The body is complete once the standfirst is covered: the standfirst promises what the trial decides, what it leaves open and what the next step is, and sections 1–3, 3–4 and 5 respectively deliver those three.

No reader loss for density or fragmentation is visible. The subheading change slightly improves orientation: a scanner who previously met "Effekten av eventuella justeringar är inte mätt" and found no adjustments in the section now meets a heading that matches what is there.

## 7. L1 — pass

The prose reads as professionally written Swedish, with native idiom and syntax rather than translated English. Fronted-subordinate constructions sit naturally: "Var givarna satt är dokumenterat", "Har du egna serier liggande är det där du börjar". The direct address in the closing paragraph keeps the register of a trade article without slipping into marketing tone. Compounds are formed as Swedish forms them, not as spaced English loans: "fastighetskontor", "temperaturgivare", "lektionspass", "dygnsmedelvärde", "användningstiderna", "arbetsgräns". Verb placement and negation are idiomatic — "Rapporten säger heller ingenting om huruvida eleverna frös" — and "heller ingenting" is the natural Swedish pairing rather than a calqued "also nothing". The colon construction "En temperaturgivare svarar på en fråga i taget: hur varm är luften där utrustningen sitter?" is ordinary Swedish exposition. Nothing in the returned text reads as English word order, English idiom or English punctuation habit carried across.

## 8. L2 — pass

The resolved locale is `sv`, from the text's `kntnt` metadata, and it governs throughout.

- Dates in Swedish order and lower case: "daterad 12 mars 2026", "I januari 2026", "planeras till november" — the month name is not capitalised, as Swedish requires.
- Units written out in Swedish form: "under 20 grader Celsius", "var femte minut", "fyra veckor".
- Numerals: "sex klassrum", "Två av givarna", "fyra på innerväggar" written as words at low values, and "120" and "14" as digits, which is established Swedish practice; no currency and no conversion appears, and none was invented.
- Punctuation: the speech dash before Rask's quotation is now the Swedish *tankstreck* with a following space, "– Vi vet när vi behöver titta närmare", which is the repair the Skill made and the change is correct for the locale. The en dash at "det där du börjar – lägg tiderna" was already correct and is untouched, so the text is now internally consistent on this mark where the input was not.

No established variation was flattened and no new factual date or conversion was introduced.

## 9. T2 — pass

A technique is named: the returned text's own metadata carries `technique: abt`, and the reply's first line states that it read the text against "tekniken `abt`", taken from the frontmatter. So the criterion applies.

The three movements relate, and none of them is manufactured.

- **Situation (and)** — the lead states the stable ground: sensors placed in January 2026, complaints of cold air behind them, the office wanting to know whether the complaints coincided with low temperatures during lesson time. This is given as fact, without dramatisation; the complaints are described, not made into a crisis.
- **Genuine complication (but)** — the lead's closing sentence is the turn: "Vad de inte mätte avgör hur långt siffrorna räcker." The complication is real, and it is the article's own subject rather than an invented obstacle: the placements were never compared in a controlled design, only air temperature was logged, and duration below the limit is unknown. The complication is also honestly bounded — "Underlaget omfattar dessutom bara dessa sex rum och dessa fyra veckor" — instead of being inflated into a failure of the trial.
- **Supported response (therefore)** — the close does not resolve the complication by claiming a cause or a fix, which would be the invented triumph this criterion guards against. It offers what the limits actually permit: "Rask rekommenderar att temperaturserierna kopplas till användningstiderna innan styrningen ändras", and then the reader's own version of that step. The quoted line "Vi vet när vi behöver titta närmare. Vi vet ännu inte varför det blev kallt just då" is the ABT turn stated in the source's own voice.

The 14-of-120 figure is used as the pointer to periods worth examining, never as evidence of a problem's size, so the complication rests on what the measurement lacks rather than on a number inflated past its support.

## 10. R1 — pass

The Skill addressed the one concrete visible defect in the text and one locale-mechanics error, preserved everything else, and accounted for both accurately.

**Every change, against the Skill's own account:**

1. *Subheading rewritten.* Reported, and reported accurately. The account states the before and after verbatim, says explicitly what disappeared — "Med den gamla rubriken försvann dess påstående — att justeringar kan ha gjorts och att effekten av dem inte är mätt" — and gives the reason the claim was the defect: "varken några justeringar eller någon omätt effekt nämns i avsnittet under rubriken, så inget påstående i brödtexten följde med bort." That last statement is true on the text: the section's three paragraphs cover the review of timings, the planned November trial with undecided funding, and the quotation, and none mentions adjustments or an unmeasured effect. This is the repair of a failed part-job — a subheading that claimed more than the text under it claims — not a rewrite to satisfy taste, and not a *most* count read against one section or a *should* the text had reason to leave. The replacement asserts only what the section carries, so the repair introduces no new claim.
2. *Em dash to en dash.* Reported, and reported accurately: "talstrecket framför Elin Rasks replik var ett engelskt em-streck (—) och är nu ett svenskt tankstreck (–)." The description matches the bytes (U+2014 to U+2013) and the reasoning matches Swedish practice.

The account's summary claim, "Inget annat påstående togs bort. Inget påstående fick sin räckvidd, säkerhet, källa, kronologi, orsakslogik eller innebörd förskjuten", is true: the diff between input and delivered contains nothing else. Every figure (120, 14, 20 grader, var femte minut, fyra veckor, sex klassrum, två/fyra givare), every name (Lerviks fastighetskontor, Björkskolan, Mätförsök i Björkskolan, 12 mars 2026, Elin Rask, Thomas Barregren) and the quotation's wording survive unchanged. The voice — the plain trade register, the fronted clauses, the direct address at the close — is untouched.

**Visible defects not addressed:** none that the text alone exposes. I looked for and did not find: a count outside a requirement (`"conforms": true`, `"failures": []` on both files), an internal contradiction between a heading and its section other than the one repaired, a claim in the body unsupported by another part of the text, a concept used before it is introduced, or a locale mark left in a foreign form after the dash repair. The closest thing to a remaining blemish is that the final paragraph's last clause restates the fifth subheading's advice in other words; that is a working call-to-action cadence, not a defect, and rewriting it would have been the taste-driven editing this criterion forbids.

**Changes of taste to passages that already worked:** none. The Skill left every clean sentence alone, including several a taste-driven reviewer would have reached for — the 51-word four-sentence lead, the two-sentence paragraph of 17 words opening section 1, and the colon construction in section 2.

**Unresolved mandatory findings not reported:** none. The reply states "Inga fynd återstår", and nothing in the returned text contradicts that. No unavailable-source verification was attempted or claimed; the Skill judged the subheading against the section beneath it, which is material it had.

On the protocol's five unconditional rejections: no unsupported fact was introduced, the locale is correct and was improved, the mechanical edit was a genuine mechanical correction and not substantive editing, no finding was left unreported, and no side effect appears — the frontmatter, the byline, the section order and the file's shape are all as they were.

## 11. Source loss

Separate from every criterion above, since the Skill never saw `write/work/source.md` and could not have known this.

**One loss.** The source material states, in its paragraph on Elin Rask:

> Driftteknikern Elin Rask gick efter försöket igenom tiderna för ventilation och värme med skolans vaktmästare. **Inga justeringars effekt har ännu mätts.** Nästa försök planeras för november med likadant placerade givare och noteringar om när rummen används; finansiering är inte beslutad.

That middle sentence is a careful statement of a limit: whatever was or was not adjusted after the review, no effect of it has been measured. In the input, the article carried that limit only in the fourth subheading, "Effekten av eventuella justeringar är inte mätt". The change to "Uppföljningen är planerad men ännu inte finansierad" removes it, and no sentence elsewhere in the returned text replaces it. A reader of the returned text is told that Rask reviewed the ventilation and heating timings with the caretaker, and is left without the source's explicit note that no effect of any resulting adjustment has been measured.

The loss is a loss of a caveat, not the creation of a false claim: the returned text nowhere says or implies that adjustments were made, that they worked, or that anything was measured about them, so it does not contradict the source, and the article's governing angle — "visar när, inte varför" — still stands. The source's other guarded formulations survive intact: the 20-degree limit as the office's own working threshold and not a legal requirement, the 14-of-120 figure without any high/low characterisation, the six rooms and four weeks as the whole of the basis, the absence of duration data, the absence of any statement about whether pupils were cold, the air-versus-operative distinction, and the undecided funding.

A reviewer holding the source would have kept the limit and moved it into the body rather than repairing the heading by dropping it — but the Skill, working from the text alone, had no way to know the sentence was ever there, and the heading it was lodged in was genuinely defective as a heading.
