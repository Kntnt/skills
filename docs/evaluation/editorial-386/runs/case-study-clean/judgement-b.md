# Judgement B — case-study-clean

## Changes

none

`work/input.md` and `delivered.md` are byte-identical (verified by diff). The reply states it: "Texten är oförändrad, korrigeringsbudgeten är outnyttjad och inget har skrivits till disk." The two anatomy files are likewise identical, so every figure below holds for both texts.

## Headings

### Input

- `# Elm Quay samlade reparationsärendena` — **statement**
- `## Gruppen enades om kategorierna först` — **statement**
- `## Två perioder med olika arbetsbelastning` — **label**
- `## Kunden vill ge förberedelserna mer tid` — **statement**

### Returned text

- `# Elm Quay samlade reparationsärendena` — **statement**
- `## Gruppen enades om kategorierna först` — **statement**
- `## Två perioder med olika arbetsbelastning` — **label**
- `## Kunden vill ge förberedelserna mer tid` — **statement**

No **colon**, **question**, **echo** or **overclaim** mark applies to any of the four.

- The headline carries no colon and no question mark. It shares only the proper name "Elm Quay" with the standfirst ("Elm Quay Housing provade en gemensam reparationslogg…"), not its wording or phrasing, so it is not an echo; and "samlade reparationsärendena" claims no more than the shared log the body describes.
- Subheading 1 shares the single noun *kategorierna* with its first sentence ("Kategorierna i loggen var underhållsgruppens egna."), but says something else — that the group settled them first — so it is not a repeat of that sentence's phrasing.
- Subheading 2 states the section's angle, that two periods of unlike workload are being compared. Its first sentence ("Enligt Elm Quays interna försöksanteckning från den 4 december 2025 registrerades 31 ärenden under åtta veckor.") does not repeat it. The later sentence "Perioderna hade olika arbetsbelastning" is not the first sentence under the subheading, so the echo mark does not apply.
- Subheading 3's first sentence is the quote "– Jag skulle välja att göra försöket igen." — no repetition, and "Kunden vill ge förberedelserna mer tid" is exactly what Lind says ("jag skulle lägga till en vecka för förberedelser"), not a stronger claim.

## Against the expectation

| Expectation item | Outcome |
|---|---|
| Conforms to the anatomy | Preserved. `anatomy-delivered.json`: `"conforms": true`, `"failures": []`, `"norms": []` — unchanged from `anatomy-input.json`. |
| Preserve customer agency | Preserved verbatim: "Kategorierna i loggen var underhållsgruppens egna."; "Vi lade mer tid på att enas om kategorierna än på att lägga in de första ärendena." |
| Preserve the qualified appraisal | Preserved verbatim: "Perioderna hade olika arbetsbelastning, och anteckningen tillskriver därför inte skillnaden programvaran." |
| Preserve the numbers | Preserved verbatim: "31 ärenden under åtta veckor", "Mediantiden … var två arbetsdagar. Under de föregående åtta veckorna var den tre.", "sex medarbetare", "den 4 december 2025", "två hus". |
| Preserve the supplier publication disclosure | Preserved verbatim: "Kundcaset publiceras av leverantören Svale." |
| Preserve the checklist link carrying the ending's call to action | Preserved verbatim, target intact: `[Svales checklista för införandet](https://example.invalid/svale/checklist)`. |
| No required quote count or extra sales block | Honoured. Nothing added; the two quotes and the single link stand as they were. |
| Reject a finding against the 36-character headline | No finding made. Script: headline `"characters": 36`. |
| Reject a finding against the 40-word standfirst | No finding made. Script: standfirst `"words": 40`. |
| Reject a finding against the 36–39-character subheadings | No finding made. Script: 36, 39, 38 characters. |
| Reject a finding resting on the one-sentence paragraph | No finding made. Script: section 2, paragraph 2, `"sentences_estimate": 1`. |
| Reject a finding resting on the four-sentence paragraph | No finding made. Script: section 2, paragraph 1, `"sentences_estimate": 4`. |
| Reject a finding against one section's paragraph count | No finding made. Script: `"sections": 3`, `"sections_of_two_or_three_paragraphs": 3`. |
| Reject a finding against the Swedish `Text:` byline form | No finding made. Script: byline `"text": "Text: Iris Falk"`, carried through unchanged. |

The reply makes no findings at all: "Granskningen hittade inga redaktionella brister, och korrekturpasset hittade inga mekaniska fel." No expectation item is violated, and every preservation item survives because the text is unchanged.

## G1 — pass

The case study does its job for a reader weighing the same pilot. The reader sees the situation ("underhållsgruppen på Elm Quay Housing ville få ut av sin gemensamma reparationslogg"), the action ("Leverantören Svale konfigurerade loggen efter dem och utbildade sex medarbetare"), the results ("Mediantiden från anmälan till tilldelning var två arbetsdagar. Under de föregående åtta veckorna var den tre.") and an appraisal that is honest about its own limit ("anteckningen tillskriver därför inte skillnaden programvaran"). The angle — that agreeing the categories cost more than logging the first cases, and deserves more time next round — holds from the standfirst to the closing quote. The craft is journalistic: sourced numbers, attributed quotes, a dated internal note named as the source.

## G2 — pass

The parts stand in the anatomy's order and each does its own job. Headline, standfirst ("**Elm Quay Housing provade …**", `"paragraphs": 1`, `"words": 40`), byline ("Text: Iris Falk"), lead before the first H2 (`"paragraphs": 1`, `"words": 43`), three sections, ending. The standfirst stands alone: it names the customer, the scope, the verdict and what follows. The lead begins the work rather than restating it, promising "Vad det krävde, och vad det gav, går att följa i gruppens egna anteckningar", and the ending meets that expectation and turns it outward ("Den som står inför samma förberedelser kan börja i [Svales checklista för införandet]"). For the case genre: customer situation, action, results and appraisal are all present, the publisher stance is stated plainly ("Kundcaset publiceras av leverantören Svale"), and the call to action is built from a supplied link rather than a sales pitch. The byline names an author, so the missing-byline report does not arise. Script: `"conforms": true`, `"failures": []`.

## P1 — pass

The reasoning is followable on the text alone. The one term a reader could stumble on, the shared repair log, is unpacked at first use ("Att se samma information över skiftgränserna"), and the exclusions are stated before the comparison is drawn on ("Akuta ärenden och tidigare beställda arbeten ingick inte"). The transition into the appraisal is real, not decorative: the numbers come first, then "Perioderna hade olika arbetsbelastning, och anteckningen tillskriver därför inte skillnaden programvaran" withholds exactly the conclusion the figures would otherwise invite. The conclusion the text does draw — repeat the pilot, add a week of preparation — is carried by the quoted supervisor and no further. Useful technical substance remains: configuration to the team's own categories, six people trained, 31 cases, a two-day median against three.

## W1 — pass

A web reader can enter anywhere and orient. The three subheadings are informative statements of their sections' angles, and the script records no norm departures at all: `"norms": []`, so no paragraph exceeds 80 words (the longest measured is the lead at 43), no section exceeds three paragraphs, and no heading sits below the second level. The headline is 4 words and 36 characters, inside the eight-word and 60-character norms. Standfirst and lead open on different first words — "Elm Quay Housing provade …" against "Att se samma information …". Read across the whole text, the *most* statements hold: `"paragraphs_of_two_or_three_sentences": 6` of `"paragraphs": 8`, and `"sections_of_two_or_three_paragraphs": 3` of `"sections": 3`. The one-sentence paragraph is a deliberate caveat given its own air, and the rhythm is better for it, not fragmented.

## L1 — pass

The Swedish reads as written in Swedish, not translated into it. The lead fronts an infinitive clause the way Swedish reportage does — "Att se samma information över skiftgränserna var vad underhållsgruppen … ville få ut av" — and the attributions take native form ("säger Maya Lind, arbetsledare på Elm Quay"). Compounds are idiomatic and correctly closed: *reparationsärendena*, *skiftgränserna*, *underhållsgruppens*, *arbetsbelastning*, *försöksanteckning*. Nothing shows English syntax carried across; the only English material is the proper names Elm Quay Housing and Svale, which stay as names.

## L2 — pass

Swedish locale mechanics govern throughout. Quotations use the Swedish speech dash ("– Vi lade mer tid …", "– Jag skulle välja …") rather than quotation marks. The date takes Swedish form, "den 4 december 2025", with a lowercase month and no comma. The byline uses the Swedish "Text:" form. Numbers under twelve are spelled out and larger ones set as figures ("sex medarbetare", "två arbetsdagar", "31 ärenden"). No currency or converted figure appears, and none was invented.

## R1 — pass

The Skill returned the text byte-identical to the input, so there is no removal and no changed claim to account for. Every claim in `delivered.md` matches `work/input.md` in strength, subject, scope and modality — including the two that most invite meddling, the withheld attribution ("anteckningen tillskriver därför inte skillnaden programvaran") and the supplier disclosure ("Kundcaset publiceras av leverantören Svale").

Its account reports this accurately and completely for what happened: no editorial findings, no mechanical findings, text unchanged, correction budget unused, nothing written to disk. There is no unresolved mandatory finding, because there is no finding; there is no irreparable finding to report; and there is no side effect, since the reply states none was taken and `delivered.md` bears none.

Visible defects not addressed: none found. The script reports `"conforms": true`, `"failures": []`, `"norms": []`, so no anatomy requirement and no norm is open, and the *most* statements hold across the text (6 of 8 paragraphs, 3 of 3 sections). No visible contradiction exists between the figures and the appraisal — the text itself declines the inference the figures would support. Source-blind, the Skill could not check the internal note of 4 December 2025, the case counts or the medians against anything, and it correctly claimed no such check.

Findings made that `expectation.md` rejects: none. The Skill made no finding against the 36-character headline, the 40-word standfirst, the 36–39-character subheadings, the one-sentence paragraph, the four-sentence paragraph, one section's paragraph count, or the Swedish `Text:` byline — and it added no quote and no sales block. Restraint on a clean text is the correct behaviour here, and the reply does not dress it up as work.
