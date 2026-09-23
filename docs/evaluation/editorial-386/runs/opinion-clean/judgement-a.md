# Judgement A — run `opinion-clean`

## 1. Changes

One difference between `work/input.md` and `delivered.md`.

| Before | After | Kind |
|---|---|---|
| Lead, sentence 1: "Kommunstyrelsen i Lervik bör skjuta upp bytet till enbart digital bokning av föreningslokaler." | "Kommunstyrelsen i Lervik bör skjuta upp bytet till enbart digital bokning av föreningslokaler, som annars kan ske i september." | A change to what the claim says — it adds a temporal scope (the switch is dated to September) to the lead's thesis sentence. The added fact is carried by the standfirst immediately above it, so it is not an unsupported fact; against a text the expectation records as conforming it is a change of taste, and it introduces a syftningsfel (see L1/R1). The script records the effect: lead `words` 42 in `anatomy-input.json`, 48 in `anatomy-delivered.json`. |

Nothing else was added, removed or reordered. The account in `response.md` does not mention this change.

## 2. Headings

### Input

- `# Avskaffa inte telefonbokningen på ett antagande` — **statement**
- `## Bokningar är inte samma sak som personer` — **statement**
- `## Mät också arbetet med två kanaler` — **statement**
- `## Besluta om försöket, inte om antagandet` — **statement**

### Returned text

- `# Avskaffa inte telefonbokningen på ett antagande` — **statement**
- `## Bokningar är inte samma sak som personer` — **statement**
- `## Mät också arbetet med två kanaler` — **statement**
- `## Besluta om försöket, inte om antagandet` — **statement**

No heading is a label, none uses a colon for a verb, none is a question. No **echo**: the headline does not repeat the standfirst's wording ("I september kan telefonbokningen … försvinna" against an imperative "Avskaffa inte …"), and no subheading repeats the first sentence under it ("Kommunens pilotrapport från den 8 april 2026 räknar …", "Förvaltningen vill slippa dubbel administration.", "Kommunstyrelsen bör därför säga ja …"). No **overclaim**: the pilot figures, the September date and the council's decision are all carried by the body at the same strength. The headline is 47 characters and 6 words, and the subheadings 40, 33 and 39 characters, all per `anatomy-delivered.json`; the marked lists are identical before and after, since the Skill touched no heading.

## 3. Against the expectation

| What `expectation.md` asks | Outcome |
|---|---|
| Conforms to the anatomy | **Preserved.** `anatomy-delivered.json` reports `"conforms": true`, `"failures": []`, `"norms": []`. |
| Preserve the polemical final sentence | **Preserved** verbatim: "Ett antagande blir inte ett beslutsunderlag för att kalendern säger september." |
| Preserve the early thesis | **Preserved in substance** — "Kommunstyrelsen i Lervik bör skjuta upp bytet till enbart digital bokning av föreningslokaler" still opens the lead — but the sentence carrying it is the one sentence the Skill altered. |
| Preserve the attribution | **Preserved** verbatim: "Text: Sanna Ek, Öppna beslut". |
| Preserve the real administrative objection | **Preserved**: "Förvaltningen vill slippa dubbel administration. Det är en relevant invändning." |
| Preserve the cost uncertainty | **Preserved**: "ta ställning till dess ännu okända kostnad". |
| Preserve the ending's named decision for the council | **Preserved**: "Kommunstyrelsen bör därför säga ja till halvåret med båda bokningsvägarna …". |
| Do not flatten to neutral exposition | **Preserved.** The imperatives ("Avskaffa inte", "Pröva först", "Mät också") and the closing polemic stand. |
| Do not add generic hedges | **Preserved.** The added "som annars kan ske i september" is a date, not a hedge; the modal "kan" mirrors the standfirst's own "kan … försvinna". |
| Reject a finding against the 47-character headline | **No such finding.** The reply makes no finding at all. |
| Reject a finding against the 39-word standfirst | **No such finding.** |
| Reject a finding against the 33–40-character subheadings | **No such finding.** |
| Reject a finding resting on the single-paragraph section | **No such finding.** The one-paragraph section "Mät också arbetet med två kanaler" is untouched. |
| Reject a finding against the one-sentence closing paragraph | **No such finding.** The 11-word, one-sentence closing paragraph is untouched. |
| Reject a finding against the four-sentence paragraph | **No such finding.** The 32-word, four-sentence paragraph is untouched. |
| Reject a finding against the Swedish `Text:` byline form | **No such finding.** |

The run made none of the findings the expectation rejects. It also reported no finding of any kind, while silently editing one sentence.

## 4. G1 — pass

The opinion does its job for a reader following a municipal decision. The reader learns what is on the table ("I september kan telefonbokningen av Lerviks föreningslokaler försvinna"), what the evidence actually is ("96 webbokningar och 24 telefonbokningar under åtta veckor i två lokaler") and why it does not reach the conclusion drawn from it ("Den säger inte hur många personer som bokade eller varför de valde telefonen"). The angle is single and held throughout: the decision rests on an assumption, not on a decision basis. The craft is that of a Swedish debattartikel — position, evidence, concession, demand — and it closes on the polemical line "Ett antagande blir inte ett beslutsunderlag för att kalendern säger september."

## 5. G2 — pass

The parts appear in the anatomy's order and each does its own job. The headline is a statement of the angle, 47 characters and 6 words (`anatomy-delivered.json`), understood alone and claiming no more than the body. The standfirst stands alone at 39 words in 1 paragraph (script), giving occasion, evidence and the writer's ask. The byline names the author the text names — "Text: Sanna Ek, Öppna beslut" — so nothing had to be reported missing. The lead (48 words, 1 paragraph, script) begins the work and precedes the first H2. Three sections carry the explanation; the script counts `"sections": 3`, each with at least one paragraph. The ending meets the lead's expectation with the council's named decision and the closing polemic.

For the opinion genre specifically: the position is early (lead sentence 1, "bör skjuta upp bytet"); it is supported (the pilot's counts and what they do not measure; the missing measurement of administrative time); a relevant real objection is met rather than dodged ("Förvaltningen vill slippa dubbel administration. Det är en relevant invändning."); and the call to action is the change itself with an identifiable actor — "Kommunstyrelsen bör därför säga ja till halvåret … och ge förvaltningen i uppdrag att mäta tidsåtgången".

## 6. P1 — pass

The reasoning is followable by a reader with no prior knowledge of the case. The distinction the argument turns on is introduced before it is used and then stated plainly: "En bokning är en händelse, inte en invånare. Den skillnaden avgör vad siffrorna kan användas till." The transitions are real, not decorative — "Men handlingarna innehåller ingen mätning av tidsåtgången" turns on the concession before it, and "Kommunstyrelsen bör därför säga ja" gathers both sections. The conclusion is proportionate to the visible support: the text asks for a six-month trial and a measurement, not for the digital booking to be abandoned, and it concedes what it does not know ("dess ännu okända kostnad"). The technical substance — pilot date, the 96/24 split, eight weeks, two of seven premises — survives intact.

## 7. W1 — pass

A web reader can orient and enter. Every counted requirement holds on the script's figures: `anatomy-delivered.json` reports `"conforms": true` with `"failures": []` and `"norms": []`; the headline is 47 characters and 6 words, within 20–70 characters and 8 words; the standfirst is 39 words, under 60; the subheadings are 40, 33 and 39 characters, under 70; standfirst and lead are 1 paragraph each; every section has at least one paragraph; no heading goes below level 2. The heaviest paragraph is 50 words, so no *should* about an 80-word paragraph is engaged. Standfirst and lead open on different first words ("I" against "Kommunstyrelsen").

The *most* statements are read across the whole text and hold: `"paragraphs": 7` with `"paragraphs_of_two_or_three_sentences": 5`, and `"sections": 3` with `"sections_of_two_or_three_paragraphs": 2`. The one-paragraph section and the four-sentence paragraph are single cases and are not failures. Standfirst and lead remain complementary, though less so than before: the Skill's inserted "som annars kan ske i september" repeats the September timing the standfirst already gives one line above, so the lead now opens by restating rather than advancing. That is a qualitative loss, not a counted failure, and it does not cost the reader orientation.

## 8. L1 — pass, with a defect the Skill introduced

The prose is native Swedish throughout, with no translated-English cadence: "Ett antagande blir inte ett beslutsunderlag för att kalendern säger september", "det som nu ligger på bordet", "slippa dubbel administration". Syntax and idiom are those of a Swedish debate page.

The one blemish is the Skill's own insertion. In "bör skjuta upp bytet till enbart digital bokning av föreningslokaler, som annars kan ske i september", the relative pronoun "som" is meant to take "bytet" as its antecedent but is separated from it by "till enbart digital bokning av föreningslokaler", so it reads first as attaching to "föreningslokaler" — a syftningsfel, and "ske" does not disambiguate between singular and plural. The sense is recoverable and one loose relative does not make an otherwise professionally written text sound non-native, so this is a qualitative concern rather than a contract rejection here; it is scored where it belongs, under R1, as a defect introduced into a text the expectation records as clean.

## 9. L2 — pass

The resolved locale governs throughout. The date is in Swedish form with a lower-case month and no ordinal — "från den 8 april 2026". The month names in the standfirst, the lead and the closing line are lower case ("september"), as Swedish requires. Quotation marks, the comma before "och" in the enumerations, and the decimal-free integers 96, 24, 8 and 2026 are all correct for Swedish. No currency or converted figure appears, and the Skill invented no new date: the September it inserted into the lead is the September the standfirst already names.

## 10. R1 — fail

**Every change, against the Skill's own account.** The Skill made exactly one change — the insertion of ", som annars kan ske i september" into the lead's first sentence — and `response.md` does not report it. The account is three lines: "Granskad som **opinion** på **svenska**", a note that no technique was applied, and "Inga anmärkningar kvarstår." There is no changelog, no finding, no statement that the text was returned unchanged, and no mention of the lead. A reader of that reply would take the returned text to be the text they submitted. The removal column is empty — nothing was removed — but the one addition is a change to what the lead's sentence claims, reported neither as a finding nor as a repair. That is an unreported change and an incorrect side effect, and it is the criterion's core failure.

**Was the change warranted?** No. `anatomy-input.json` reports the input `"conforms": true` with `"failures": []` and `"norms": []`, so no anatomy requirement was failed and there was nothing to repair. R1 states that a clean text is not rewritten to satisfy taste, and this is a taste edit: the September date it supplies is already in the standfirst directly above, so the reader gains nothing and the lead now opens by repeating. Worse, the edit leaves the text measurably less well written than it found it: the inserted relative clause is a syftningsfel, with "som" reading onto "föreningslokaler" rather than "bytet" (L1). The Skill degraded the one sentence it touched.

**Preservation.** Everything else the criterion protects survives: the voice (the imperatives and the closing polemic), the arguments (the booking-is-not-a-person distinction, the unmeasured administrative time), the figures (96, 24, eight weeks, two of seven premises, 8 April 2026) and the byline are identical before and after. No quotation or claim outside the single edit was altered, and no verification of unavailable sources was attempted or required.

**Visible defects not addressed.** None that the text carries: the input conforms on the script's figures and the expectation records it as clean, so there was no mandatory finding to detect. Correctly, the Skill made none of the findings `expectation.md` rejects — nothing against the 47-character headline, the 39-word standfirst, the 33–40-character subheadings, the single-paragraph section, the one-sentence closing paragraph, the four-sentence paragraph or the `Text:` byline form. The failure is not a wrong finding; it is an unreported edit to a text that needed none, and the right behaviour here was to return the text byte-identical and say so.
