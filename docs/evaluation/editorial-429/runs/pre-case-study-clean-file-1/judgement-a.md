# Judgement a

## 1. Differences

None. `work/output.md` and `work/input.md` are byte-identical (both 1825 bytes; `diff` returns no output and exit status 0). No frontmatter exists in either file, and the formatting is unchanged: the bold standfirst, the `Text: Iris Falk` byline, the three `##` subheadings, the en-dash quotation lines and the Markdown link.

| Before | After | Class |
|---|---|---|
| (no difference) | (no difference) | — |

## 2. The account

There are no differences to account for. The reply states this accurately: "Ingenting i texten har ändrats. `output.md` är byte för byte identisk med `input.md`." It also says that one correction round was made, rejected and fully rolled back ("den ursprungliga texten återställdes i sin helhet. Ingenting från rundan finns kvar i `output.md`"). The file confirms this. The closing claims section ("Inga påståenden har strukits, ändrats eller lagts till") is accurate.

## 3. The frozen expectation

**"Conforms to the anatomy."** Not met by the reply. The reply says the opposite: "Fynd 2 och 4 är krav i artikelanatomin som texten inte uppfyller, så texten följer inte anatomin fullt ut." It lists four findings against a text the expectation calls conforming:
- Finding 1, on the headline: "Rubriken säger vad Elm Quay gjorde, inte vad det gav … rubriken påstår mer än texten."
- Finding 2, on the standfirst: "Ingressen går inte att förstå fristående", which rests on the definite forms "gruppen" and "anteckningarna".
- Finding 3, a taste finding on the first body sentence: "engelsk syntax i svensk form".
- Finding 4, on the subheading: "Mellanrubriken 'Två perioder med olika arbetsbelastning' beskriver inte avsnittet."

None of these is a concrete visible defect that the expectation recognises. They are false positives. The Skill applied none of them to the delivered text.

**Preserve customer agency.** Preserved: "Kategorierna i loggen var underhållsgruppens egna. Leverantören Svale konfigurerade loggen efter dem och utbildade sex medarbetare."

**Preserve the qualified appraisal.** Preserved: "Att ha en gemensam bild av ärendena hjälper oss, men jag skulle lägga till en vecka för förberedelser, säger Lind." The rejected correction round would have damaged it, because its new headline dropped "oss" and so generalised the appraisal. The Skill caught this itself ("Den stryker 'oss' i 'hjälper oss', så att hennes omdöme blir generellt") and restored the text.

**Preserve the numbers.** Preserved: "4 december 2025", "31 ärenden under åtta veckor", "två arbetsdagar", "var den tre", "två hus", "sex medarbetare", "åtta veckor".

**Preserve the supplier publication disclosure.** Preserved: "Kundcaset publiceras av leverantören Svale."

**Preserve the checklist link that carries the ending's call to action.** Preserved: "Den som står inför samma förberedelser kan börja i [Svales checklista för införandet](https://example.invalid/svale/checklist)."

**No required quote count or extra sales block.** The run made neither mistake. The reply has no finding that asks for more quotations, and the delivered text adds no sales block.

**Reject a finding against a limit the text meets (36-character headline, 40-word standfirst, 36–39-character subheadings).** The run did not make this mistake. Finding 1 is about what the headline says, not its length. Finding 2 is about how the standfirst reads on its own, not its word count. Finding 4 is about what the subheading describes, not its character count. The reply says "Anatomiskriptet hittade inga fel i det som går att räkna." The only numeric limit it names (8 words, 60 characters) is applied to its own rejected replacement headline, not to the text.

**Reject a finding that rests on the one-sentence paragraph, the four-sentence paragraph or one section's paragraph count.** The run did not make this mistake. No finding mentions paragraph length or paragraph count.

**Reject a finding against the Swedish `Text:` byline form.** The run did not make this mistake. No finding mentions the byline, and the output keeps "Text: Iris Falk" unchanged.

## 4. R1

**Pass.** The corpus says R1's clause on clean texts is judged from `work/output.md` alone. That file is byte-identical to the input, so the Skill did not rewrite the clean text to satisfy taste or numerical guidelines. Every voice feature, argument, quotation and claim is preserved: customer agency, the qualified appraisal with "hjälper oss, men …", the numbers, the disclosure "Kundcaset publiceras av leverantören Svale." and the checklist link. The Skill verified nothing against unavailable sources.

The run is weak on detection. It reports four findings against a conforming text and states that the text "följer inte anatomin fullt ut", so the clause "Conforms to the anatomy" is not met in the account. It made none of the rejected mistakes the expectation names, and its false findings never reached the text.
