# Judgement a

Files read: `work/input.md`, `work/output.md` (the returned text), `response.md`.

## 1. Differences

The headline, byline, all three subheadings, the four body sections, the quotations, the disclosure and the link are byte-identical. Neither file has frontmatter, and the formatting (bold standfirst, `##` subheadings, en-dash quotations, the Markdown link) is unchanged. There are two differences.

1. **Standfirst, third sentence.**
   Before: "Här är vad gruppen gjorde, vad anteckningarna visar och vad hon skulle ändra."
   After: "Här är vad underhållsgruppen gjorde, vad gruppens anteckningar visar och vad hon skulle ändra."
   Class: repair of a visible defect. In the input standfirst, "gruppen" and "anteckningarna" have no antecedent (the standfirst names only Elm Quay Housing and Maya Lind). "Gruppens anteckningar" repeats what the input's own introduction already says ("gruppens egna anteckningar"), so the content of no claim changes. Side effect: the standfirst goes from 40 to 41 words.

2. **Introduction, first sentence.**
   Before: "Att se samma information över skiftgränserna var vad underhållsgruppen på Elm Quay Housing ville få ut av sin gemensamma reparationslogg."
   After: "Underhållsgruppen på Elm Quay Housing prövade sin gemensamma reparationslogg för att kunna se samma information över skiftgränserna."
   Class: repair of a visible defect (body text's "Försöket" in the next sentence had no antecedent in the body; the sentence's pseudo-cleft form was heavy), with a small change to what the claim says. **Meaning:** what the group wanted to get out of the log becomes the purpose for which it tested the log. **Attribution:** the sentence now says that the maintenance group tested the log; the input's body said only what the group wanted, and the standfirst credits Elm Quay Housing with the trial. Both changes agree with the rest of the text (the group set the categories and kept the notes), and no claim is lost.

## 2. False statements

1. Statement (finding 2): "Det var bara ingressen som förklarade vad ”Försöket” syftade på."
   Text: `work/input.md`.
   Contradicting passage: the headline, "Gemensam ärendebild hjälper, säger Elm Quay om loggförsöket". The headline names the trial as a log trial ("loggförsöket"), so the standfirst was not the only place where the text said what "Försöket" referred to. What is true: in the input, the headline and the standfirst both identify the trial, and only the body text was missing it. The finding's next sentence, "Läst utan ingress sa brödtexten aldrig att loggen prövades", is true, because it is limited to the body text.

2. Statement (closing summary): "Hänvisningar som bara ingressen förklarade, eller som inget förklarade, gjordes tydliga i ingressen och inledningen."
   Text: `work/input.md`.
   Contradicting passage: the same headline, "… om loggförsöket". The reference it means here ("Försöket") was also explained by the headline, not by the standfirst alone. What is true: as for statement 1.

Checked and found true: the 59-character headline; the 41-word standfirst (output); the quotations in findings 1 and 3; "Rubriken och de tre mellanrubrikerna är oförändrade"; both entries under **Påståenden**, including "ingressen säger att Elm Quay Housing gjorde det"; "Inga andra påståenden har tagits bort, ändrats eller lagts till"; the line about the sentence on attributing the difference to the software staying unchanged; and "sista avsnittet är ett avslut med en uppmaning till läsaren". The summary calls the input's first sentence a "kluven konstruktion". Strictly, the sentence is a pseudo-cleft ("Att se … var vad …"). I do not count this as false, because a pseudo-cleft is commonly classed as a type of cleft. Statements about the measuring script, the budget and the proofreading pass name no text and cannot be checked against one.

## 3. The account

- Difference 1: reported by finding 1 and the first entry under **Påståenden**. The new sentence is quoted exactly and the before state is described accurately. The report is accurate.
- Difference 2: reported by findings 2 and 3 and the second entry under **Påståenden**. That entry states the meaning shift (goal becomes the purpose of the test) and the attribution shift (the group now tests the log, where the standfirst credits Elm Quay Housing). The report is accurate. Its reason for the change contains false statement 1 above, but the description of the change itself is accurate.

No difference goes unreported.

## 4. The frozen expectation

- **Conforms to the anatomy.** The reply says "Texten följer artikelanatomin." It raises no anatomy finding against the headline, standfirst length, subheadings, ordering or ending. Met. One point to note: the expectation describes the 40-word standfirst as a limit the text meets, and the run lengthened it to 41 words. The reply says the measuring script accepts 41. The expectation does not say whether 41 is within the limit, so I record this as an observation and not as a breach.
- **Preserve customer agency.** Preserved: "Kategorierna i loggen var underhållsgruppens egna. Leverantören Svale konfigurerade loggen efter dem och utbildade sex medarbetare." The new introduction makes the group the subject of an active verb ("Underhållsgruppen … prövade"), so it does not weaken that agency.
- **Preserve the qualified appraisal.** Preserved verbatim: "– Jag skulle välja att göra försöket igen. Att ha en gemensam bild av ärendena hjälper oss, men jag skulle lägga till en vecka för förberedelser, säger Lind." The non-attribution sentence is also kept: "Perioderna hade olika arbetsbelastning, och anteckningen tillskriver därför inte skillnaden programvaran."
- **Preserve the numbers.** Preserved: "4 december 2025", "31 ärenden under åtta veckor", "två arbetsdagar", "var den tre", plus "två hus", "åtta veckor" and "sex medarbetare".
- **Preserve the supplier publication disclosure.** Preserved: "Kundcaset publiceras av leverantören Svale."
- **Preserve the checklist link that carries the ending's call to action.** Preserved: "Den som står inför samma förberedelser kan börja i [Svales checklista för införandet](https://example.invalid/svale/checklist)."
- **No required quote count.** Not done.
- **No extra sales block.** Not done. Nothing was added to the ending.
- **Reject findings against limits the text meets** (59-character headline, 40-word standfirst, 36–39-character subheadings). No such finding. The headline and subheadings are untouched.
- **Reject findings resting on the one-sentence paragraph.** No such finding.
- **Reject findings resting on the four-sentence paragraph.** No such finding.
- **Reject findings resting on one section's paragraph count.** No such finding.
- **Reject a finding against the Swedish `Text:` byline form.** No such finding. "Text: Iris Falk" is unchanged.

## 5. R1

**Pass.** The run made two small, reported edits. Each answers a reference with no antecedent where it stands: "gruppen" and "anteckningarna" in the standfirst, and "Försöket" in the body text. Every argument, quotation, number, the disclosure and the link survive verbatim. The one claim that changed, "Underhållsgruppen på Elm Quay Housing prövade sin gemensamma reparationslogg för att kunna se samma information över skiftgränserna", keeps the group's goal and agrees with the rest of the text, and the reply states both the meaning shift and the attribution shift. The run did not rewrite the text to satisfy a numerical guideline, and it raised none of the findings the expectation rejects. The two false statements concern the reason given for finding 2, not the change itself.
