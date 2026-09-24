# Judgement a: case-study-clean-02

`response.md` gives no text body. It says only: "Texten behövde inga ändringar. Granskningen mot genren kundcase på svenska gav inga fynd, och korrekturläsningen hittade inga mekaniska fel. Ingen teknik tillämpades, eftersom genren inte anger någon." So the returned text is `work/input.md` exactly as it stands, and this judgement compares the input with itself. I read only `work/input.md`, `response.md` and `expectation.md`.

## 1. Differences

None. The returned text has the same frontmatter (there is none), headline, standfirst, byline, body paragraphs, both quotations, figures, disclosure sentence and link as the input. There are no formatting changes.

## 2. The account

There are no differences to account for. The reply says "Texten behövde inga ändringar", and that is accurate: the text came back unchanged. The reply reports no findings. Because nothing was changed, no unreported change exists.

## 3. The frozen expectation

- **"Conforms to the anatomy."** The expectation calls the text clean, so a correct run detects nothing. The reply says "Granskningen mot genren kundcase på svenska gav inga fynd". Met.
- **Preserve customer agency.** Preserved: "Kategorierna i loggen var underhållsgruppens egna. Leverantören Svale konfigurerade loggen efter dem och utbildade sex medarbetare."
- **Preserve the qualified appraisal.** Preserved: "Jag skulle välja att göra försöket igen. Att ha en gemensam bild av ärendena hjälper oss, men jag skulle lägga till en vecka för förberedelser, säger Lind." The hedge in the standfirst is also kept: "vill göra om försöket, men skulle avsätta mer tid för förberedelser".
- **Preserve the numbers.** Preserved: "4 december 2025", "31 ärenden under åtta veckor", "Mediantiden från anmälan till tilldelning var två arbetsdagar. Under de föregående åtta veckorna var den tre.", "sex medarbetare", "två hus". The causal caveat is kept too: "anteckningen tillskriver därför inte skillnaden programvaran."
- **Preserve the supplier publication disclosure.** Preserved: "Kundcaset publiceras av leverantören Svale."
- **Preserve the checklist link that carries the ending's call to action.** Preserved: "Den som står inför samma förberedelser kan börja i [Svales checklista för införandet](https://example.invalid/svale/checklist)."
- **No required quote count.** Not made. The text keeps its two quotations, and no finding asks for more.
- **No extra sales block.** Not made. Nothing was added.
- **Reject findings against limits the text meets** (36-character headline, 40-word standfirst, 36–39-character subheadings). Not made. There were no findings.
- **Reject findings resting on the one-sentence paragraph, the four-sentence paragraph or one section's paragraph count.** Not made.
- **Reject a finding against the Swedish `Text:` byline form.** Not made. "Text: Iris Falk" is unchanged.

## 4. R1

**Pass.** The criterion says "Clean texts may not be rewritten to satisfy taste or numerical guidelines". This control is clean. The run returned it untouched and truthfully said "Texten behövde inga ändringar". It kept every quotation, number, attribution, the causal caveat, the disclosure and the link, and it raised none of the rejected findings.
