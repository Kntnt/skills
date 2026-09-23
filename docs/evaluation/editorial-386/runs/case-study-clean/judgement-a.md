# Judgement A — case-study-clean

## Changes

none — `delivered.md` is byte-identical to `work/input.md` (diff reports no difference). The reply states this itself: "Texten är oförändrad, korrigeringsbudgeten är outnyttjad och inget har skrivits till disk."

## Headings

### Input

- `# Elm Quay samlade reparationsärendena` — statement
- `## Gruppen enades om kategorierna först` — statement
- `## Två perioder med olika arbetsbelastning` — label
- `## Kunden vill ge förberedelserna mer tid` — statement

### Returned text

- `# Elm Quay samlade reparationsärendena` — statement
- `## Gruppen enades om kategorierna först` — statement
- `## Två perioder med olika arbetsbelastning` — label
- `## Kunden vill ge förberedelserna mer tid` — statement

No heading is marked **colon**, **question**, **echo** or **overclaim**. The headline's wording ("samlade reparationsärendena") does not repeat the standfirst's ("provade en gemensam reparationslogg"); each subheading states its own section's angle rather than repeating the first sentence under it — "Gruppen enades om kategorierna först" against "Kategorierna i loggen var underhållsgruppens egna", "Två perioder med olika arbetsbelastning" against "Enligt Elm Quays interna försöksanteckning …", "Kunden vill ge förberedelserna mer tid" against "– Jag skulle välja att göra försöket igen." Each claim is carried in the body at the same strength: the log gathered 31 cases, the note records two periods of differing workload, and Lind says she would add a week of preparation.

## Against the expectation

- **Conforms to the anatomy** — preserved. `anatomy-delivered.json` gives `"conforms": true`, `"failures": []`, `"norms": []`, identical to `anatomy-input.json`.
- **Preserve customer agency** — preserved. Both quotes stand verbatim, including "Den tiden skulle jag avsätta innan nästa hus börjar" and "jag skulle lägga till en vecka för förberedelser"; the customer, not the supplier, states the verdict.
- **Preserve the qualified appraisal** — preserved. "Perioderna hade olika arbetsbelastning, och anteckningen tillskriver därför inte skillnaden programvaran." is untouched, so the median-time improvement is still not credited to the software.
- **Preserve the numbers** — preserved. "två hus", "åtta veckor", "sex medarbetare", "den 4 december 2025", "31 ärenden", "två arbetsdagar", "tre" all stand unchanged.
- **Preserve the supplier publication disclosure** — preserved. "Kundcaset publiceras av leverantören Svale." stands.
- **Preserve the checklist link carrying the ending's call to action** — preserved. "[Svales checklista för införandet](https://example.invalid/svale/checklist)" stands with its URL intact.
- **No required quote count or extra sales block** — respected. Nothing was added; the reply reports no finding of either kind.
- **Reject any finding against the 36-character headline, 40-word standfirst, 36–39-character subheadings** — no such finding. The reply reports "inga redaktionella brister". The script confirms the figures: headline 36 characters, standfirst 40 words, subheadings 36, 39 and 38 characters.
- **Reject any finding resting on the one-sentence paragraph, the four-sentence paragraph or one section's paragraph count** — no such finding. The script records the one-sentence paragraph (`"sentences_estimate": 1`, 11 words) and the four-sentence paragraph (`"sentences_estimate": 4`, 40 words) in the second section; neither was raised, and no section's paragraph count was raised.
- **Reject a finding against the Swedish `Text:` byline form** — no such finding. `"byline": {"text": "Text: Iris Falk"}` is unchanged and unremarked.

## G1 — pass

The case study does the customer-reference job for a reader weighing the same step. It names the situation ("underhållsgruppen på Elm Quay Housing ville få ut av sin gemensamma reparationslogg"), the action ("Leverantören Svale konfigurerade loggen efter dem och utbildade sex medarbetare"), the results from a named source ("Enligt Elm Quays interna försöksanteckning från den 4 december 2025 registrerades 31 ärenden under åtta veckor"), and the appraisal in the customer's own words. The angle — that agreeing the categories cost more than entering the cases, and that preparation is what she would change — holds from headline to ending. The reader leaves able to consider the trial on its stated terms and with a next step to take.

## G2 — pass

The parts appear in the anatomy's order and each does its own job. `parts` lists `headline`, `standfirst`, `byline`, `lead` and three `sections`; the lead ("Att se samma information över skiftgränserna …") precedes the first H2, and the script records no `failures`. The standfirst stands alone at 40 words, promising three things — what the group did, what the notes show, what she would change — and each is delivered in turn. The byline names an author, "Text: Iris Falk", so the missing-byline report does not apply. The case genre's four parts are present: situation, action, results, and an appraisal that is honest rather than promotional. The publisher stance is stated outright — "Kundcaset publiceras av leverantören Svale." — and the call to action is built from a supplied route: "Den som står inför samma förberedelser kan börja i [Svales checklista för införandet]". That ending meets the lead's expectation, since the lead offered the group's own notes as what can be followed.

## P1 — pass

The reasoning is followable end to end and the conclusions stay inside the visible support. The one place where a reader could over-read — the median falling from three working days to two — is immediately fenced: "Perioderna hade olika arbetsbelastning, och anteckningen tillskriver därför inte skillnaden programvaran." Scope is stated before the figure is used ("Akuta ärenden och tidigare beställda arbeten ingick inte"), and the source and its date are given before the numbers. Transitions are real rather than decorative: the second section's note about workload is what licenses the third section's modest verdict. The technical substance a practitioner needs — who owned the categories, how many were trained, what the log counted — remains.

## W1 — pass

A web reader can orient and enter without losing the explanation. On the script's figures: headline 36 characters and 4 words, inside the 60-character and eight-word norms; standfirst 40 words and 1 paragraph, inside the 60-word limit; lead 43 words and 1 paragraph; subheadings 36, 39 and 38 characters, all inside 70; no heading below the second level appears in `parts`. `typical` gives 8 paragraphs of which 6 run to two or three sentences, and 3 sections of which 3 run to two or three paragraphs — read across the whole text, both norms hold. No paragraph is recorded above 80 words (the longest is 40) and no section above three paragraphs. Standfirst and lead open on different first words, "Elm" and "Att", and are complementary rather than repetitive: the standfirst promises, the lead sets up the source. The single-sentence paragraph after the figures is a deliberate beat that isolates the caveat, not fragmentation.

## L1 — pass

The prose reads as written by a Swedish professional, not translated. Idiom and syntax are native throughout: "att enas om kategorierna", "att avsätta tid", "från anmälan till tilldelning", "Den som står inför samma förberedelser". The double-object construction "anteckningen tillskriver därför inte skillnaden programvaran" is idiomatic Swedish and would not survive a word-by-word rendering from English. Quotation is set with the Swedish speech dash and the trailing attribution ("… säger Maya Lind, arbetsledare på Elm Quay"), the convention a Swedish reader expects.

## L2 — pass

Swedish locale mechanics govern throughout. The date is written "den 4 december 2025" — lower-case month, no ordinal suffix, day before month. Numbers follow Swedish practice, with the small ones spelled out ("två hus", "åtta veckor", "sex medarbetare", "två arbetsdagar") and the larger one in digits ("31 ärenden"). Speech is introduced with the en dash, not quotation marks. No currency appears, so no conversion was needed and none was invented; no factual date was added.

## R1 — pass

The Skill returned the text byte-identical and reported exactly that. There are no removals and no changed claims to account for, so nothing is mis-reported: the reply's "Texten är oförändrad, korrigeringsbudgeten är outnyttjad och inget har skrivits till disk" is accurate against the diff, and "Granskad som kundcase (`case-study`) på svenska" names the genre the text is.

No visible defect went unaddressed. The script finds the anatomy conforming with `"failures": []` and `"norms": []`; the numbers are sourced and dated in the text itself; the one claim that could outrun its support is fenced by the text's own caveat; the commercial interest is disclosed; the call to action uses a route the text already carries. Nothing in the returned text contradicts anything else in it, which is the only class of invention a source-blind run can fairly be held to.

No finding `expectation.md` rejects was made. The reply reports none at all, so the four counted limits, the one-sentence and four-sentence paragraphs, the section paragraph counts, and the `Text:` byline form were all left alone. The restraint is the right result here rather than inertness, because every candidate for a finding in this text is a feature the expectation names as correct. The one visible cost of a clean pass — the account is thin, naming no part it checked — is a reporting economy, not an unresolved mandatory finding: there is no finding to resolve.

**Verdicts:** G1 pass, G2 pass, P1 pass, W1 pass, L1 pass, L2 pass, R1 pass.
