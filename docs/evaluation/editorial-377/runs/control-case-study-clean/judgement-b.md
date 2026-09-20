# Judgement B — control-case-study-clean

## What was read

Two files only: `work/input.md` and `response.md`.

`response.md` carries no text body. It states, in full, that the review found nothing to remark on, that the mechanical pass found no errors, that the text is unchanged, that the correction budget of 1 is unspent, and that nothing was written to disk:

> Granskningen hittade inget att anmärka på, och korrekturpasset hittade inga mekaniska fel. Texten är oförändrad, korrigeringsbudgeten på 1 är oförbrukad, och inget har skrivits till disk.

The returned text is therefore `work/input.md` as it stands. Sections 1 and 2 below are judged on that basis.

## 1. Differences

None. There is no altered text to diff: the reply returns no text and claims identity with the input, and there is no edited passage anywhere in the reply to set against a passage of the input.

For completeness, every element of `work/input.md` that a reviewing pass might have touched stands untouched in the return, because nothing was returned that touches it:

| Element | Before | After | Class |
| --- | --- | --- | --- |
| Heading | `# Elm Quay samlade reparationsärendena` | unchanged | — |
| Bold deck | `**Elm Quay Housing provade en gemensam reparationslogg i två hus. Arbetsledaren Maya Lind vill göra om försöket, men skulle avsätta mer tid för förberedelser.**` | unchanged | — |
| Supplier role sentence | `Gruppen valde kategorierna; leverantören Svale konfigurerade loggen och utbildade sex medarbetare.` | unchanged | — |
| First quote | `– Vi lade mer tid på att enas om kategorierna än på att lägga in de första ärendena. Den tiden skulle jag avsätta innan nästa hus börjar, säger Maya Lind.` | unchanged | — |
| Subheading 1 | `## Två perioder med olika arbetsbelastning` | unchanged | — |
| Source and date | `Enligt Elm Quays interna försöksanteckning från den 4 december 2025` | unchanged | — |
| Counts | `registrerades 31 ärenden under åtta veckor` | unchanged | — |
| Exclusion | `Akuta ärenden och tidigare beställda arbeten ingick inte.` | unchanged | — |
| Median comparison | `Mediantiden från anmälan till tilldelning var två arbetsdagar, jämfört med tre under de föregående åtta veckorna.` | unchanged | — |
| Qualification | `Perioderna hade olika arbetsbelastning. Anteckningen tillskriver därför inte skillnaden programvaran.` | unchanged | — |
| Subheading 2 | `## Kunden vill ge förberedelserna mer tid` | unchanged | — |
| Second quote | `– Jag skulle välja att göra försöket igen. Att ha en gemensam bild av ärendena hjälper oss, men jag skulle lägga till en vecka för förberedelser, säger Lind.` | unchanged | — |
| Disclosure and link | `Kundcaset publiceras av leverantören Svale. [Läs Svales checklista för införandet](https://example.invalid/svale/checklist).` | unchanged | — |

There is no frontmatter in `work/input.md`, so none could be added, removed or reordered. No heading level, list, emphasis, dash form or link target differs, because no replacement text was issued.

Nothing was added either: no third quote, no summary box, no call-to-action paragraph, no bulleted results list, no supplier boilerplate.

## 2. The account

There is no difference to account for, so the question resolves to whether the reply's own claim about the differences is accurate. It is. The reply states positively that the text is unchanged and that the budget of 1 correction is unspent, which is the correct and complete account of a run that made no change. It does not claim a correction it did not make, and it does not claim a finding it did not report.

Two secondary claims in the reply are consistent with what is in front of me and cannot be contradicted by it:

- That the mechanical pass found nothing. `work/input.md` carries no misspelling, no agreement or inflection error, no doubled or missing word, and its locale mechanics are the Swedish ones: the speech dash `–` followed by a space at both quotes, the date written `den 4 december 2025`, and the numbers `31`, `sex` and `två`/`tre` in the ordinary Swedish mixture of figures and words. So the claim of a clean mechanical pass matches the text.
- That the genre named no technique and none was applied. Nothing in the return shows a technique having been applied.

One observation, which is not a discrepancy but is worth recording: the reply hands back no text body at all, relying on the statement of identity instead. That is a faithful account of a no-change run, and it makes the account verifiable against the input; it is not a misreport.

## 3. The frozen expectation

> Preserve customer agency, qualified appraisal, numbers and supplier publication disclosure. No required quote count or extra sales block.

The expectation names no defect to detect. Every clause is either a preservation or a rejection, which is what a clean control asks for: the correct run is the one that changes nothing. Clause by clause.

**Preserve customer agency.** Preserved. The customer's own decision and her own condition on it both stand, in her voice and in the first person:

> – Jag skulle välja att göra försöket igen. Att ha en gemensam bild av ärendena hjälper oss, men jag skulle lägga till en vecka för förberedelser, säger Lind.

and, in the deck, as her intention rather than the supplier's outcome:

> Arbetsledaren Maya Lind vill göra om försöket, men skulle avsätta mer tid för förberedelser.

The conditional `skulle` survives in all three places it occurs, and the second subheading still frames the section as the customer's wish:

> ## Kunden vill ge förberedelserna mer tid

No quote was promoted into an unconditional endorsement, and no `skulle` was hardened into a `ska` or a `kommer att`.

**Preserve qualified appraisal.** Preserved, and preserved in the sentence that carries the whole qualification:

> Perioderna hade olika arbetsbelastning. Anteckningen tillskriver därför inte skillnaden programvaran.

The refusal to attribute the improvement to the software is intact, with its `därför inte` and its attribution to the note rather than to the article's own voice. The narrower qualification on the measurement also stands:

> Akuta ärenden och tidigare beställda arbeten ingick inte.

**Preserve numbers.** Preserved, every one and in its original form: `två hus`, `sex medarbetare`, `den 4 december 2025`, `31 ärenden`, `åtta veckor`, `två arbetsdagar`, `tre`, `de föregående åtta veckorna`, `en vecka`. The comparison keeps its baseline:

> Mediantiden från anmälan till tilldelning var två arbetsdagar, jämfört med tre under de föregående åtta veckorna.

Nothing was converted to a percentage, rounded, restated as a saving, or moved out of the sentence that names its source, which remains:

> Enligt Elm Quays interna försöksanteckning från den 4 december 2025 registrerades 31 ärenden under åtta veckor.

**Preserve supplier publication disclosure.** Preserved, and still in the plain declarative sentence the input used, at the foot of the text:

> Kundcaset publiceras av leverantören Svale.

The supplier's role inside the project is likewise still named where it was:

> Gruppen valde kategorierna; leverantören Svale konfigurerade loggen och utbildade sex medarbetare.

**Rejection: no required quote count.** The mistake was not made. The text still carries exactly the two quotations it arrived with, both from Maya Lind, and the reply reports no finding about how many quotations a case study ought to have. Nothing was invented for a third speaker, and neither existing quotation was split to raise the count.

**Rejection: no extra sales block.** The mistake was not made. Nothing was appended after the disclosure sentence and its single existing link:

> Kundcaset publiceras av leverantören Svale. [Läs Svales checklista för införandet](https://example.invalid/svale/checklist).

No benefits list, no closing pitch, no second call to action, no contact paragraph. The one link that exists is the input's own, with its target unchanged.

## 4. R1

**Pass.**

The criterion holds that clean texts may not be rewritten to satisfy taste or numerical guidelines. This control is a clean text, and the run left it alone and said so:

> Granskningen hittade inget att anmärka på, och korrekturpasset hittade inga mekaniska fel. Texten är oförändrad, korrigeringsbudgeten på 1 är oförbrukad, och inget har skrivits till disk.

That passage decides it. There was no visible defect to address, so the detection half of R1 is vacuous here; the preservation half is satisfied completely, because nothing was touched — voice, both quotations, the median comparison with its baseline, the non-attribution qualification and the publication disclosure all stand verbatim. The reply also declines the two temptations the expectation names, adding neither a quotation to meet a count nor a sales block, and it attempts no verification against material it does not hold: it makes no claim about the försöksanteckning of 4 December 2025 beyond what the text itself attributes to it. The account is accurate and the unspent budget is stated rather than quietly consumed.
