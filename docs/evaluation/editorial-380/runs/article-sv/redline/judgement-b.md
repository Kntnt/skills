# Judgement B — article-sv, Redline

Genre is `article` (from the text's own `kntnt` block), so the anatomy skeleton applies and its counted requirements are judged by the script's figures.

## 1. Changes

Three differences between `redline/work/input.md` and `redline/delivered.md`. Nothing else differs; frontmatter, byline, quotation, figures, section order and every other paragraph are byte-identical.

1. **Headline.** Before: `# Mätningen i Björkskolan pekar ut lektioner, inte orsaker`. After: `# Björkskolans mätning ringar in tiderna att undersöka`. **Repair of a visible defect** (the headline reused the standfirst's verb phrase *pekar ut*), carrying with it **a change to what a claim says — scope and subject**: the negative half *inte orsaker* is gone from the headline, and the genitive *Björkskolans mätning* seats the measurement with the school, where the text seats it with the property office (*Fastighetskontoret i Lervik lät temperaturgivare mäta*).
2. **First paragraph under *Givaren mäter luften på sin egen plats*.** Before: `Två givare satt nära ytterväggar, fyra på innerväggar. Placeringarna dokumenterades, men de jämfördes inte experimentellt.` After: `Två givare satt nära ytterväggar och fyra på innerväggar, placeringar som dokumenterades men inte jämfördes experimentellt.` **Change of taste.** No fact moves; the documented-but-not-compared point is demoted from its own sentence to an appositive. The script shows the paragraph before the change at 23 words / 3 sentences inside a paragraph set where 12 of 13 paragraphs are of two or three sentences and `failures` and `norms` are both empty, so nothing in the measurement was out of bounds.
3. **Third section, second paragraph.** Before: `Rapporten redovisar därför lektionspass i stället för ett enda dygnsmedelvärde`. After: `Rapporten redovisar lektionspass i stället för ett enda dygnsmedelvärde`. **A change to what a claim says — modality**: the causal attribution of the report's design to the preceding observation is withdrawn, leaving juxtaposition.

## 2. Headings

**Input**

- `# Mätningen i Björkskolan pekar ut lektioner, inte orsaker` — statement; echo (the standfirst's second sentence runs *Rapporten pekar ut 14 av 120 lektionspass*; same verb, same pointing-out-but-not-explaining contrast)
- `## Givaren mäter luften på sin egen plats` — statement
- `## Ett värde under gränsen säger inte hur länge` — statement
- `## Två metodval styr vad siffrorna betyder` — statement
- `## Koppla temperaturen till när rummen används` — statement

**Delivered**

- `# Björkskolans mätning ringar in tiderna att undersöka` — statement
- `## Givaren mäter luften på sin egen plats` — statement
- `## Ett värde under gränsen säger inte hur länge` — statement
- `## Två metodval styr vad siffrorna betyder` — statement
- `## Koppla temperaturen till när rummen används` — statement

No colon, question or overclaim mark on either list. The delivered headline says the measurement circles the times to look at, which Elin Rask's quoted words carry at the same strength — *Vi vet när vi behöver titta närmare* — so it is not an overclaim, and it shares only the proper noun with the standfirst, so it is not an echo.

## 3. Criteria on the returned text

### G1 — pass

The article does an explanatory job for a reader who knows heating but not measurement. The reader learns what the instrument actually measures (*En givare mäter temperaturen där den sitter, och den mäter luft*), what it does not (*Operativ temperatur är ett annat mått, som väger in både luftens temperatur och värmestrålningen från omgivande ytor. Försöket mätte bara lufttemperatur*), and what the headline figure will not bear (*Siffran 14 av 120 är därför ett antal, inte ett omdöme*). The angle — how far a four-week trial reaches — is recognisable from the standfirst through to the close, and the craft is journalistic: the report is named and dated, the number is attributed to it, the technician is named and quoted.

### G2 — pass

The parts stand in the anatomy's order and each does its own work. The script reports `conforms: true`, `failures: []`, and `parts` holding a headline, a standfirst of 45 words in 1 paragraph, `byline: "Av Thomas Barregren"`, a lead of 46 words in 1 paragraph before the first H2, four sections each with three, three, two and three paragraphs, and `other: []`. The standfirst stands alone — it names who measured, what was found and what the piece will add — and the lead begins the work rather than restating it, closing on *användbart om du vet vad det mäter*. The ending is the article's call to action and is the next step the explanation supports, non-commercial as an article demands: *Planerar du ett eget mätförsök, är det värt att bestämma redan nu vad som ska noteras vid sidan av temperaturen*. The byline was already filled in the text handed to the Skill, so there was no missing byline to report. One reservation, short of failure: the delivered headline states only the affirmative half of the angle, and its genitive *Björkskolans mätning* sits a little off the body's own attribution of the trial to the property office; the standfirst repairs both in the next line (*men förklarar inte varför*).

### P1 — pass

Every unfamiliar term arrives before it is leaned on: operative temperature is defined in the sentence that introduces it, and the limits of a count are laid out before the count is judged. Conclusions stay inside visible support — *Den säger heller inte om eleverna frös*, *Vilken effekt eventuella justeringar har fått är ännu inte mätt* — and no cause, saving or legal duty is inferred. Useful technical substance survives: five-minute sampling, two outer-wall and four inner-wall sensors, air versus operative temperature, daily mean versus lesson slots. The one cost of change 3 is a softer transition — *Ett medelvärde för hela dygnet kan dölja variation under lektionerna. Rapporten redovisar lektionspass i stället…* now asks the reader to supply the link — but the trailing *ett val som formar vad underlaget kan visa* still marks it as a choice, so the reasoning holds.

### W1 — pass

Requirements, on the script's figures for the delivered text: headline 52 characters (inside 20–70), standfirst 45 words (at most 60), subheadings 38, 44, 39 and 43 characters (each at most 70), every section carrying at least one paragraph, standfirst and lead 1 paragraph each. `failures: []` and `norms: []`. The *should* statements are met rather than departed from: the headline is 7 words and 52 characters, the longest paragraph is 50 words, no heading level below the second appears (`other: []`), and standfirst and lead open on different first words (*Fastighetskontoret* / *I*). The *most* statements, read across the whole text as they must be: `paragraphs_of_two_or_three_sentences: 12` of `paragraphs: 13`, and `sections_of_two_or_three_paragraphs: 4` of `sections: 4`. The single one-sentence paragraph — the dated report citation — is a single paragraph and cannot fail a *most*. Subheadings are informative and the reader can enter at any of them; no density or fragmentation loss.

### L1 — pass

The Swedish is native in idiom and syntax, with no translated cadence. *Ett underlag utesluter ingenting som det inte har mätt* and *Den skillnaden är värd att ha med sig när siffran förs vidare* are both written in Swedish, not through English. The sentence the Skill merged is idiomatic apposition: *Två givare satt nära ytterväggar och fyra på innerväggar, placeringar som dokumenterades men inte jämfördes experimentellt*. The quotation uses the Swedish speech dash and the Swedish attribution order (*…, säger Elin Rask*).

### L2 — pass

Locale `sv` governs throughout: *12 mars 2026* and *I januari 2026* in Swedish date form, *20 grader Celsius* spelled out with a space-free Swedish idiom rather than an anglophone symbol, the en dash used as the Swedish parenthetical dash (*ett underlag – smalare än det kan se ut*), and a semicolon before *finansieringen är inte beslutad* in ordinary Swedish use. No new factual date and no currency conversion were introduced; both dates are unchanged from the input.

## 4. T2 — skipped

No technique is named in the text's metadata or in the reply: the delivered frontmatter reads `technique: none`, and the reply states *Teknikvärdet där är `none`* and that the genre contributed no narrative technique. Nothing is judged under this criterion.

## 5. R1 — pass

**Change 1, headline.** Reported, and reported accurately. The account names the finding (headline and standfirst sharing *pekar ut* and the same opposition), states plainly that the rewrite dropped the headline's own *inte orsaker*, and says where that limit survives — the standfirst's *men förklarar inte varför* and Rask's quoted *Vi vet ännu inte varför det blev kallt just då*. Both survivals check out in `delivered.md`. The defect was concrete and visible in the text alone, so repairing it is a legitimate finding rather than taste. The account does **not** report one consequence of its own rewrite: *Mätningen i Björkskolan* became *Björkskolans mätning*, which reads the trial as the school's where the body gives it to the property office. It is a small shift and the lead corrects it immediately, but it is an unreported change to a claim's subject.

**Change 2, sentence merge.** Reported, and honestly described, but it is a change of taste applied to a passage that already worked. The account justifies it as *anatomins krav på att meningslängden varierar inom stycket*, measured at one paragraph — three sentences of 8, 8 and 7 words. That is a per-paragraph reading of an evenness the script does not count as a requirement: it returns `failures: []` and `norms: []` for the input, and the paragraph sat at 23 words inside a text where 12 of 13 paragraphs already met the *most*. Nothing was lost — the account's claim that the sampling interval, the placement and the not-compared point all remain is correct — but a clean paragraph was rewritten to satisfy a count read where it does not bind.

**Change 3, *därför*.** Reported, and reported accurately: the account names the removed causal attribution as the claim that went out, and its statement that the observation, the report's practice and the *ett val* conclusion all stand unchanged is verified by the diff. Judged on the text alone — which is all this run had — the text nowhere established that the report chose lesson slots for that reason, so the finding is defensible and the repair is minimal.

**Preserved outside the findings.** The quotation is untouched word for word, as are every figure (14 of 120, 20 degrees, six rooms, four weeks, five minutes, 12 March 2026), the frontmatter, the byline, all four subheadings, the section order and ten of the thirteen paragraphs. No source verification was attempted and none was available.

**Visible defects not addressed.** None found on a full pass. The standfirst keeps *pekar ut*, which is correct once the headline no longer shares it; *hela dygnet* and *dygnsmedelvärde* are internally consistent; *Nästa försök planeras till november* and *finansieringen är inte beslutad* do not contradict each other; the section promising *Två metodval* still delivers two, since *ett val* survives change 3.

The verdict is pass: one legitimate repair, one defensible and minimal claim correction, one reported change of taste, and no unconditional rejection — no unsupported fact, no locale error, no substantive mechanical editing (the final mechanical pass changed nothing), no unresolved mandatory finding left unreported, and no incorrect side effect on metadata or structure. The unreported genitive shift and the taste merge are the two blemishes and are recorded above.

## 6. Source loss

Two changes touch what `write/work/source.md` supplied. Neither is a fatal loss, and neither was knowable to a source-blind Skill.

1. **The removed *därför* takes out a link the source states outright.** The source reads: *Ett medelvärde för hela dagen kan dölja variation under lektionerna. Rapporten redovisar därför lektionspass i stället för ett enda dygnsmedelvärde.* The delivered text now reads *Rapporten redovisar lektionspass i stället för ett enda dygnsmedelvärde*. The causal connection was reporting material, not the writer's inference, so the correction removed a supported fact. Nothing false resulted — the weaker text claims less than the source allows — and no caveat or limit was lost.
2. **The headline no longer carries the source's central negative.** The source's judging note states *Ingen besparing, bättre hälsa, orsak till kyla, effekt av givarna eller lagregel följer av materialet*, and the brief's angle is *vad ett kort mätförsök kan och inte kan säga*. The old headline held that boundary in its own words (*inte orsaker*); the new one holds only the affirmative half. The boundary itself is not lost — the standfirst's *men förklarar inte varför*, the whole of *Ett värde under gränsen säger inte hur länge*, and Rask's quote all keep it — and the new headline asserts no forbidden inference. What is lost is the boundary's place at the most-read line.

Every other source caveat is intact in the delivered text: the working-limit-not-legal-requirement distinction, the no-comparison-figure point, the air-versus-operative distinction, the unmeasured ventilation, draught and perceived temperature, the unmeasured effect of any adjustments, and the undecided funding.
