# Judgement a: case-study-clean-01

## 1. Differences

None. The reply says "Ingen ändring behövdes" and returns no altered text. The text in `work/input.md` stands as the returned text: the frontmatter (the file has none), the H1 headline, the bold standfirst, the `Text: Iris Falk` byline, the three H2 subheadings, both quotations, the figures (31 ärenden, åtta veckor, två arbetsdagar, tre), the causal hedge, the publication disclosure and the checklist link are all unchanged. No mechanical corrections, no repairs, no changes of taste, no changes to any claim.

## 2. The account

There are no differences to account for. The reply says that nothing was changed ("Ingen ändring behövdes"), that the review found nothing ("Granskningen gav inga fynd, så ingen korrigeringsrunda användes"), that proofreading found no language errors, and that "inga påståenden togs bort eller ändrades". All of these statements match the text: no change is left unreported, and the reply claims no change that was not made.

## 3. The frozen expectation

**Detect: "Conforms to the anatomy."** The run should detect conformance, not defects. The reply says: "Texten följer kraven för genren kundcase på svenska". Met.

**Preserve: customer agency.** Preserved. "Kategorierna i loggen var underhållsgruppens egna. Leverantören Svale konfigurerade loggen efter dem och utbildade sex medarbetare."

**Preserve: the qualified appraisal.** Preserved. "– Jag skulle välja att göra försöket igen. Att ha en gemensam bild av ärendena hjälper oss, men jag skulle lägga till en vecka för förberedelser, säger Lind." The standfirst's "men skulle avsätta mer tid för förberedelser" and the causal hedge "anteckningen tillskriver därför inte skillnaden programvaran" are also unchanged.

**Preserve: the numbers.** Preserved. "registrerades 31 ärenden under åtta veckor", "Mediantiden från anmälan till tilldelning var två arbetsdagar. Under de föregående åtta veckorna var den tre." The date "4 december 2025" and "sex medarbetare" are also unchanged.

**Preserve: the supplier publication disclosure.** Preserved. "Kundcaset publiceras av leverantören Svale."

**Preserve: the checklist link carrying the call to action.** Preserved. "Den som står inför samma förberedelser kan börja i [Svales checklista för införandet](https://example.invalid/svale/checklist)."

**Reject: a required quote count.** The run did not make this mistake. It made no finding, and it added no quotation.

**Reject: an extra sales block.** The run did not make this mistake. Nothing was added.

**Reject: a finding against a limit the text meets.** The limits are a 36-character headline, a 40-word standfirst and 36–39-character subheadings. The run did not make this mistake. It made no finding against any of them.

**Reject: a finding resting on the one-sentence paragraph, the four-sentence paragraph or one section's paragraph count.** The run did not make this mistake. It made no finding.

**Reject: a finding against the Swedish `Text:` byline form.** The run did not make this mistake. "Text: Iris Falk" is unchanged, and the reply names no finding against it.

## 4. R1

**Pass.** This is a clean control. R1 asks for defects to be fixed while "Clean texts may not be rewritten to satisfy taste or numerical guidelines". The run made no rewrite and no finding. Its account, "Granskningen gav inga fynd, så ingen korrigeringsrunda användes. Korrekturläsningen hittade inga språkfel, och inga påståenden togs bort eller ändrades.", matches the unchanged text exactly. Every claim, quotation, number, the disclosure and the link are still in place, and none of the rejected findings appears.
