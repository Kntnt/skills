# Judgement — run `article-clean`

## 1. Changes

none

`delivered.md` is byte-identical to `work/input.md` (same 1638 bytes, line for line). No mechanical correction, no repair, no change of taste, no change to what any claim says. The reply confirms it: "Texten är oförändrad, och inget har skrivits."

## 2. Headings

### Input

- `# Mätförsöket i Björkskolan visar när, inte varför` — **statement** (a clause: the trial shows *when*, not *why*). No colon. No question. Not an echo: the standfirst opens "Under 14 av 120 lektionspass …" and shares no phrasing with it. No overclaim — the body carries both halves ("Vi vet när vi behöver titta närmare. Vi vet ännu inte varför det blev kallt just då.").
- `## En gräns för det lokala försöket` — **label** (a plain name for what the section holds). No colon, no question. Not an echo: the first sentence under it is "Kontoret valde 20 grader Celsius som arbetsgräns."; the shared stem *gräns* is the section's subject, not a repetition of the sentence's wording. No overclaim — "lokala försöket" matches "Gränsen är kontorets egen, vald för det här försöket."
- `## Nästa försök behöver mer än givare` — **statement**. No colon, no question, no echo of "Rask rekommenderar att temperaturserierna kopplas till rummens användningstider …". No overclaim: the section says exactly that sensors alone are not enough.

### Returned text

Identical, and marked identically:

- `# Mätförsöket i Björkskolan visar när, inte varför` — **statement**
- `## En gräns för det lokala försöket` — **label**
- `## Nästa försök behöver mer än givare` — **statement**

## 3. Against the expectation

- *Conforms to the anatomy.* — Confirmed by the script on both texts: `"conforms": true`, `"failures": []`, `"norms": []`. The run treated it as conforming and reported "Inga anmärkningar."
- *Preserve the calm explanation.* — Preserved; the text is unchanged.
- *Preserve the independent result-bearing standfirst.* — Preserved verbatim, 46 words on one paragraph per `anatomy-delivered.json`.
- *Preserve the byline.* — Preserved: `"byline": {"text": "Text: Hedda Lund"}` in both JSON files.
- *Preserve the quoted summary.* — Preserved: ”Vi vet när vi behöver titta närmare. Vi vet ännu inte varför det blev kallt just då.”
- *Preserve the undecided funding.* — Preserved: "men finansieringen är inte beslutad."
- *Preserve the ending's non-commercial next step.* — Preserved: "Lägg därför tiderna för när rummen används bredvid mätvärdena innan nästa givare sätts upp." No offer, link or contact route added.
- *ABT-shaped logic must not select a technique.* — Satisfied. The account states: "Ingen teknik tillämpades: ingen angavs, och genren artikel anger ingen som den vanligen skrivs med."
- *Reject any finding against the 48-character headline.* — No finding made. Script: `"characters": 48`, within 20–70.
- *…against the 46-word standfirst.* — No finding made. Script: `"words": 46`, within 60.
- *…against the 32- and 34-character subheadings.* — No finding made. Script: `32` and `34`, within 70.
- *…against "no paragraph over 80 words".* — No finding made. The script's largest paragraph is 45 words.
- *…resting on the one-sentence paragraph.* — No finding made. The script shows one paragraph at `"sentences_estimate": 1` ("Lägg därför tiderna …"); *most* is read across the text and `paragraphs_of_two_or_three_sentences: 5` of `paragraphs: 7`.
- *…resting on the four-sentence paragraph.* — No finding made. The script shows `"sentences_estimate": 4` for "Kontoret valde 20 grader Celsius …", again a *most* statement not failed by one paragraph.
- *…resting on one section's paragraph count.* — No finding made. Script: `sections: 2`, `sections_of_two_or_three_paragraphs: 2`.
- *…against the Swedish `Text:` byline form.* — No finding made; the form stands.
- *…naming a name the text does not carry.* — No name is introduced anywhere; the reply names nobody.

## 4. Criteria

### G1 — pass

The article does an article's job for a reader who has to decide what a four-week sensor trial is worth. That reader learns the count and its provenance — "Rapporten *Mätförsök i Björkskolan*, daterad 12 mars 2026, räknar 14 lektionspass av 120 med minst en mätning under den gränsen" — and immediately learns what it does not establish: "Hur länge temperaturen låg under den anger rapporten inte." The angle is recognisable and held from headline to ending: a measurement says *when*, not *why*. The craft is journalistic and appropriate — an attributed document, a named source with a role ("Driftteknikern Elin Rask"), and a conclusion kept at the strength of the evidence.

### G2 — pass

Every required part is present, in order, and each does its own job. `anatomy-delivered.json` lists `headline`, `standfirst`, `byline`, `lead` and two `sections`, with `"conforms": true` and `"failures": []`.

- Headline: a statement of the angle, understood alone, claiming no more than the body ("visar när, inte varför").
- Standfirst: stands alone and carries the result — "Under 14 av 120 lektionspass registrerade givarna i Björkskolan temperaturer under fastighetskontorets egen arbetsgräns." It is not a repetition of the headline; it supplies the figures the headline withholds.
- Byline: `"Text: Hedda Lund"` — an author is named, so there is nothing for a Redline run to report as missing.
- Lead: one paragraph of 33 words per the script, placed before the first H2 (line 7, first `##` at line 9), and it begins the work rather than summarising — "En temperaturgivare mäter luften där den sitter."
- Body: explanatory, and neither subheading repeats the standfirst or the sentence beneath it.
- Ending: the lead promises "Genomgången nedan visar vad värdena räcker till och var gränsen går"; the close delivers the useful next step that the explanation supports — "Lägg därför tiderna för när rummen används bredvid mätvärdena innan nästa givare sätts upp." It is the article genre's non-commercial call to action, which suits an assignment that warrants none.

### P1 — pass

The reasoning is followable end to end, and the one concept the argument turns on is introduced before it is used: "En temperaturgivare mäter luften där den sitter. Det gör placeringen viktig …" — placement matters, therefore readings must be read carefully. The working limit is likewise defined before it is leaned on, then bounded: "Gränsen är kontorets egen, vald för det här försöket." Transitions are real, not decorative: "Givarna mätte varken luftdrag eller elevernas upplevelse. Ett lågt värde säger alltså när luften var kall, men inte hur rummet kändes" earns its *alltså*, and "Lägg därför tiderna …" earns its *därför* from Rask's recommendation. Conclusions stay proportionate to visible support — the text repeatedly declines to explain causes, and leaves funding open ("finansieringen är inte beslutad"). The technical substance survives intact: the 20 °C threshold, the 14-of-120 count, the unmeasured duration, and what the sensors did not record.

### W1 — pass

Every counted requirement is met on the script's figures for the delivered text, and `"norms": []` records no departure from a *should*:

- Headline: `"characters": 48`, `"words": 7` — inside 20–70 characters, and under both the 60-character and eight-word norms.
- Standfirst: `"words": 46`, `"paragraphs": 1` — at most 60 words, one paragraph.
- Subheadings: `"characters": 32` and `"characters": 34` — at most 70, and both at level 2, with no level below it.
- Lead: `"paragraphs": 1`.
- Sections: each has at least one paragraph (three and two).
- No paragraph over 80 words: the largest is 45 words.

The *most* statements are read across the whole text and both hold: `paragraphs_of_two_or_three_sentences: 5` of `paragraphs: 7`, and `sections_of_two_or_three_paragraphs: 2` of `sections: 2`. The four-sentence opening paragraph and the one-sentence close are individual paragraphs following their own content and are not failures. Standfirst and lead complement rather than duplicate: the standfirst gives the result and the question left open, the lead gives the method and the frame, and they open on different first words — "Under" against "En". The body completes what the standfirst promises ("vad som behövs för att komma vidare" is answered by the second section). A web reader can orient from headline and standfirst alone, and both subheadings are informative enough to enter at. No density or fragmentation loss.

### L1 — pass

The Swedish is native in idiom and syntax, with no translated-English residue. Constructions that only a competent Swedish writer produces: "Det gör placeringen viktig när …", "Givarna mätte varken luftdrag eller elevernas upplevelse", "men inte hur rummet kändes", "vald för det här försöket". Compounds are formed correctly and unforced — *arbetsgräns*, *lektionspass*, *temperaturserierna*, *användningstider*, *driftteknikern*. Verb-second order and inversion are handled throughout ("Hur länge temperaturen låg under den anger rapporten inte"), and the imperative close is plain Swedish.

### L2 — pass

The resolved locale governs every mechanic. Quotation marks are the Swedish right-facing pair on both sides: ”Vi vet när vi behöver titta närmare. … just då.” Dates take the Swedish form, "daterad 12 mars 2026", with a lower-case month. The temperature is written out in Swedish style, "20 grader Celsius", not "20°C". Numbers are plain digits with no imported thousands separator, and the report title is set in italics rather than English quotation marks. No new factual date, currency or conversion is invented anywhere — the run added nothing at all.

## 5. R1 — pass

**Removals and changed claims.** There are none. `delivered.md` is a byte copy of `work/input.md`, so no claim's strength, subject, scope or modality moved, and there is nothing for the account to report or misreport. The account's own statement of this is accurate: "Texten är oförändrad, och inget har skrivits."

**Was leaving it alone correct?** Yes. The script finds the input conforming — `"conforms": true`, `"failures": []`, `"norms": []` — and `expectation.md` opens with "Conforms to the anatomy." A clean text is not to be rewritten to satisfy taste, and this run did not. The three things a weaker run would have touched — the four-sentence paragraph, the one-sentence closing paragraph, and the second section's two paragraphs — are *most* statements read across the whole text, where the script's own totals (5 of 7 paragraphs, 2 of 2 sections) show the text typical. Leaving them is right, not lazy.

**Visible defects not addressed.** None found. Every proper noun, figure and attribution in the text is internally consistent: the 14-of-120 count appears identically in the standfirst and in the body; the report title in the body matches the school named in the headline; Rask is introduced with her role at first mention and referred to by surname after; the quotation's two sentences say precisely what the headline claims. The locale mechanics listed under L2 are correct throughout, so the Proofread pass finding nothing is a true result, not a missed one. Nothing in the text contradicts anything else in it, which is the only class of invention a source-blind run can fairly be held to.

**Findings the expectation rejects.** None. The run made no findings at all, so it made none against the 48-character headline, the 46-word standfirst, the 32- and 34-character subheadings, the 80-word paragraph norm, the one-sentence or four-sentence paragraph, the section's paragraph count, or the `Text:` byline form. It selected no technique despite the ABT-shaped logic, and stated why: "ingen angavs, och genren artikel anger ingen som den vanligen skrivs med."

**Unconditional rejections.** None triggered: no unsupported fact was introduced (nothing was introduced), the locale is unchanged and correct, no substantive editing was carried out under the mechanical pass, there is no mandatory finding left unreported because there is no defect to find, and there are no side effects — the returned text is the input, byte for byte.
