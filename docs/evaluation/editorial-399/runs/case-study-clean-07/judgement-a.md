# Judgement a: case-study-clean-07

The reply returns no separate text. It says "Ingen ändring behövdes … så ingenting har skrivits." So the returned text is `work/input.md` as it stands. That file is the only file in `work/`, and it reads as a clean, complete case study with nothing half-edited in it. I compare the input against that unchanged text.

## 1. Differences

None. The headline, standfirst, byline, headings, body, quotations, numbers, the disclosure sentence and the link are all unchanged. There are no frontmatter or formatting changes, because the file has no frontmatter and nothing was written.

## 2. The account

There are no differences to account for. The reply says the text was not changed ("ingenting har skrivits"), and that is correct. It also says the review found no defects and the proofreading pass found no mechanical errors. Both statements agree with what is returned.

## 3. The frozen expectation

- **"Conforms to the anatomy."** The run should find nothing, and it found nothing: "Granskningen hittade inga brister." The run treated the text as conforming. It reviewed it as a case study ("granskades som kundcase (case-study) på svenska").
- **Preserve customer agency.** Preserved. The customer chose the categories and the supplier followed them: "Kategorierna i loggen var underhållsgruppens egna. Leverantören Svale konfigurerade loggen efter dem …"
- **Preserve the qualified appraisal.** Preserved. The recommendation keeps its condition: "Jag skulle välja att göra försöket igen. … men jag skulle lägga till en vecka för förberedelser". The attribution also stays hedged: "anteckningen tillskriver därför inte skillnaden programvaran."
- **Preserve the numbers.** Preserved: "31 ärenden under åtta veckor", "Mediantiden … var två arbetsdagar. Under de föregående åtta veckorna var den tre.", "sex medarbetare", "4 december 2025".
- **Preserve the supplier publication disclosure.** Preserved: "Kundcaset publiceras av leverantören Svale."
- **Preserve the checklist link carrying the call to action.** Preserved: "Den som står inför samma förberedelser kan börja i [Svales checklista för införandet](https://example.invalid/svale/checklist)."
- **No required quote count or extra sales block.** Not made. The reply asks for no additional quotes, and nothing was added.
- **Reject findings against met limits (36-character headline, 40-word standfirst, 36–39-character subheadings).** No such finding was made.
- **Reject findings resting on the one-sentence paragraph, the four-sentence paragraph or one section's paragraph count.** No such finding was made.
- **Reject a finding against the Swedish `Text:` byline form.** No such finding was made. "Text: Iris Falk" is unchanged.

The run made none of the rejected mistakes.

## 4. R1

**Pass.** The deciding passage is in the reply: "Granskningen hittade inga brister och korrekturläsningen inga mekaniska fel, så ingenting har skrivits." R1 says a clean text must not be rewritten to satisfy taste or numerical guidelines. The text is a clean control, and the run left all of its voice, arguments, quotations and claims unchanged. It raised no finding that the corpus rejects. It did not try to verify anything against a source it did not have.
