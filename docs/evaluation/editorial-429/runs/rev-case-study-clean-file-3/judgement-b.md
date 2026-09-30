# Judgement b

Run directory: `/Users/thomas/Projects/skills/.git/kntnt-orchestrate/429.scratch/j/677aaeb93751`

## 1. Differences

Neither file has frontmatter. The two files are otherwise identical: the standfirst, the byline, all three subheadings, both quotations, the numbers paragraph, the disclosure and the link are unchanged, and so is all formatting (bold standfirst, `##` levels, en-dash quotation marks, the Markdown link). There are three differences, in two lines:

| # | Before | After | Class |
|---|---|---|---|
| D1 | `# Elm Quay samlade reparationsärendena` | `# Elm Quay samlade reparationsärenden under ett försök` | Change to a claim, **scope**. The definite plural ("the repair cases", read as all of them, as a settled fact) is narrowed to indefinite cases gathered during a trial. The body limits the trial to two buildings over eight weeks and leaves out emergency and pre-ordered work, so the narrowing repairs a visible overclaim. It is a defensible repair, though a borderline one. The headline grows from 36 to 52 characters. |
| D2 | `Att se samma information över skiftgränserna var vad underhållsgruppen på Elm Quay Housing ville få ut av sin gemensamma reparationslogg.` | `Underhållsgruppen på Elm Quay Housing ville kunna se samma information över skiftgränserna med sin gemensamma reparationslogg.` | Repair of a visible defect: the anglicised pseudo-cleft "X var vad Y ville få ut av" is rewritten in plain Swedish word order. The meaning holds, and the group stays the grammatical agent. This is the change closest to taste, but the construction is a recognisable defect of idiom, not a matter of preference. |
| D3 | `Vad det krävde, och vad det gav, går att följa i gruppens egna anteckningar.` | `Vad det krävde berättar arbetsledaren Maya Lind, och vad som registrerades står i Elm Quays interna försöksanteckning.` | Change to a claim, **causality** and **attribution**. The lead's promise to show "vad det gav" (what the trial yielded) is removed. That promise was in visible tension with the body's statement that the note does not credit the software with the difference, so this is a legitimate removal. What the trial required is now attributed to Maya Lind rather than to "gruppens egna anteckningar". What was registered is attributed to the single internal trial note that the body cites. |

The reply reports that the mechanical proofreading pass changed nothing, and no mechanical correction appears in the diff.

## 2. The account

- **D1:** Reported as finding 1, with the old and new headline quoted, and again under "Påståenden" ("Ändrat: rubriken säger nu …"). The account is accurate: it names the scope and settled-fact reading it removed. It does not mention that the headline grew by 16 characters. Its statement that the script found every limit met after the correction cannot be checked against these three files.
- **D2:** Reported as finding 2, quoting the new sentence and stating "Innebörden är densamma". The closing paragraph says the same. Accurate.
- **D3:** Reported as finding 3, with its reason: the promise of "gav" conflicts with the body's non-attribution, and the body cites one note, not several. Under "Påståenden" it is itemised as two removals and two changes, covering the effect promise, the plural notes, the attribution to Lind and the single source. Accurate and complete.

The reply also lists one unresolved finding: the standfirst's plural "anteckningarna" against a single note in the body. It is left because the budget ran out. The finding is reported, not applied, so it makes no difference to the text. The mismatch it names is sharper in the output than in the input, because the lead now names a single note while the standfirst still says "anteckningarna".

## 3. The frozen expectation

- **"Conforms to the anatomy."** Met. The reply says: "texten följer anatomin utan avvikelser. Skriptet räknade gränserna före och efter korrigeringen, och båda gångerna låg allt inom dem." It reports no anatomy finding.
- **Preserve customer agency.** Preserved. The returned text keeps "Kategorierna i loggen var underhållsgruppens egna. Leverantören Svale konfigurerade loggen efter dem och utbildade sex medarbetare." The lead now opens with the group as subject: "Underhållsgruppen på Elm Quay Housing ville kunna se …"
- **Preserve the qualified appraisal.** Preserved. The returned text keeps "Perioderna hade olika arbetsbelastning, och anteckningen tillskriver därför inte skillnaden programvaran." and Lind's "Jag skulle välja att göra försöket igen. … men jag skulle lägga till en vecka för förberedelser". D3 strengthens this appraisal rather than weakening it.
- **Preserve the numbers.** Preserved: "den 4 december 2025 registrerades 31 ärenden under åtta veckor … Mediantiden från anmälan till tilldelning var två arbetsdagar. Under de föregående åtta veckorna var den tre." The text also keeps "två hus" and "sex medarbetare".
- **Preserve the supplier publication disclosure.** Preserved: "Kundcaset publiceras av leverantören Svale."
- **Preserve the checklist link that carries the call to action.** Preserved: "Den som står inför samma förberedelser kan börja i [Svales checklista för införandet](https://example.invalid/svale/checklist)."
- **No required quote count or extra sales block.** Met. No finding asks for more quotations, and no sales block was added.
- **Reject findings against met limits (36-character headline, 40-word standfirst, 36–39-character subheadings).** The run did not make this mistake. No finding rests on a length limit. The headline was changed on scope grounds, not length grounds, and the standfirst finding concerns the plural "anteckningarna", not its length.
- **Reject findings resting on the one-sentence paragraph, the four-sentence paragraph or one section's paragraph count.** The run did not make this mistake. None was raised, and the reply affirms "varje stycke bär en tanke".
- **Reject a finding against the Swedish `Text:` byline.** The run did not make this mistake. None was raised, and "Text: Iris Falk" is unchanged.

## 4. R1

**Pass.** Each of the three edits answers a concrete, reported defect that the text itself shows, rather than a taste or a numerical guideline.

The deciding passage is D3. The input lead promises that the notes show "vad det gav", while the body says "anteckningen tillskriver därför inte skillnaden programvaran". The run removed that promise and reported the removal as a claim change. The rewrite keeps every quotation, number, the disclosure, the link and the group's agency. Outside the reported findings, no claim changed.

D1 (a scope narrowing) and D2 (an idiom repair) are the closest to taste. Both are reasoned, accurately reported and preserve meaning. The run makes none of the rejected findings.
