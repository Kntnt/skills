# Judgement a

## 1. Differences

None. I extracted the fenced text in `response.md` and ran `diff` against `work/input.md`. The two are byte-identical, including the H1, the bold standfirst, the `Text: Iris Falk` byline, the three H2s, both dash-led quotations, the numbers and the link. The input has no frontmatter, and the returned text adds none. There are no mechanical, repair, taste or claim differences to list.

## 2. The account

There is no difference to account for. The reply says the text comes back unchanged ("Texten nedan är alltså oförändrad"; "Den levererade texten är identisk med den du lämnade in. Inga påståenden har tagits bort, ändrats eller lagts till."). That is accurate.

The reply also reports a correction round that it made and then rejected. That round rewrote the headline to "Gemensam logg hjälpte Elm Quays underhållsgrupp", changed "gruppen" to "underhållsgruppen" in the standfirst, and rewrote the first two sentences of the introduction. The reply says it rejected the whole round because the new headline stated as fact that the log helped. In the text, that is only Lind's own conditional judgement, and the note explicitly does not credit the software with the difference. The reply says the text was restored word for word, and the diff confirms it. The rejected loss is reported accurately.

## 3. The frozen expectation

- **"Conforms to the anatomy."** Not met as a detection matter. The reply reports four findings and states: "Texten följer inte anatomin fullt ut på två punkter: ingressen går inte att förstå på egen hand (brist 2), och brödtexten pekar tillbaka på ingressen (brist 4)." Finding 1 also applies an anatomy-style requirement that the text does not satisfy: "I en casestudy ska rubriken säga vad kunden vann eller uppnådde". On a control the expectation calls conforming, these are false positives. Finding 1 is also dangerous: an outcome headline needs a claim the text withholds, and the run's own rejected round shows that acting on it inflates the qualified appraisal. None of these findings reached the text.
- **Preserve customer agency.** Preserved. Customer agency survives in "Kategorierna i loggen var underhållsgruppens egna. Leverantören Svale konfigurerade loggen efter dem" and in the headline "Elm Quay samlade reparationsärendena". The rejected rewrite would have made the log the agent, and it was withdrawn.
- **Preserve the qualified appraisal.** Preserved. The reply keeps "Att ha en gemensam bild av ärendena hjälper oss, men jag skulle lägga till en vecka för förberedelser, säger Lind." and "anteckningen tillskriver därför inte skillnaden programvaran." The run explicitly rejected its own round for overstating this appraisal.
- **Preserve the numbers.** Preserved. The reply keeps "4 december 2025", "31 ärenden under åtta veckor", "två arbetsdagar", "var den tre", "två hus" and "sex medarbetare".
- **Preserve the supplier publication disclosure.** Preserved. The reply keeps "Kundcaset publiceras av leverantören Svale."
- **Preserve the checklist link carrying the call to action.** Preserved. The reply keeps "Den som står inför samma förberedelser kan börja i [Svales checklista för införandet](https://example.invalid/svale/checklist)." The reply also affirms that "avslutningen har en uppmaning till läsaren".
- **No required quote count or extra sales block.** Met. No finding asks for more quotations or a sales section.
- **Reject a finding against the 36-character headline.** Not made. Finding 1 quotes "(36 tecken, 4 ord)", but it faults the headline's content, not its length. The anatomy note says "allt som går att räkna håller, som antal tecken, ord, stycken och avsnitt".
- **Reject a finding against the 40-word standfirst.** Not made. Finding 2 concerns the referent of "gruppen", not length.
- **Reject a finding against the 36–39-character subheadings.** Not made. The reply says "underrubrikerna beskriver sina avsnitt".
- **Reject a finding resting on the one-sentence paragraph, the four-sentence paragraph, or one section's paragraph count.** Not made.
- **Reject a finding against the Swedish `Text:` byline form.** Not made. The byline is untouched and unmentioned.

## 4. R1

**Pass.**

The deciding passage is the returned text, which is identical to the input, together with the reply's statement: "Därför underkändes hela omgången … och texten återställdes ord för ord. Ingenting från omgången finns kvar". The run did not rewrite the clean text. It preserved every quotation, number, attribution, disclosure and the qualified appraisal. It avoided every named rejection class, and it caught and reported its own attempted loss, the outcome headline, before delivery.

The weakness is in detection, not preservation. The run reported four findings, two of them explicit anatomy non-conformities, on a text the expectation says conforms. Finding 1, which asks for an outcome headline, is unsound for this text. Under the corpus rule these count against detection but do not fail R1, because nothing was changed to satisfy them.
