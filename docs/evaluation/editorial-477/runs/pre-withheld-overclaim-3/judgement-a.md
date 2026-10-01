# Judgement a

The run wrote no `work/output.md`. The returned text is the fenced Markdown block at the end of `response.md` (lines 26–50). I compared it line by line with `work/input.md`. Two lines differ, and everything else is byte-identical, including the ingress, the byline, the subheadings, the quotations, the figures, the disclosure and the link.

## 1. Differences

1. Headline (line 1). Before: `# Gemensam ärendebild hjälper, säger Elm Quay om loggförsöket`. After: `# Gemensam ärendebild hjälper, säger arbetsledaren om loggförsöket`. Class: a change to what a claim says, **attribution**. The opinion moves from the organisation, Elm Quay, to its work supervisor. In the body the opinion is Maya Lind's, in her quotation in the last section ("Att ha en gemensam bild av ärendena hjälper oss"), so the new attribution matches the body more closely. The old attribution was a common way to credit a spokesperson's view to the organisation, so this change goes beyond what the text demanded. It was made as a finding, for accuracy of attribution, and not for taste.
2. Lead paragraph, last sentence (line 7). Before: `… och loggen kortade tiden från anmälan till tilldelning med en arbetsdag.` After: `… och under försöket var mediantiden från anmälan till tilldelning en arbetsdag kortare än under de föregående åtta veckorna.` Class: the repair of a visible defect, and a change to what a claim says. It changes **causality**, because the log is no longer the cause, and **scope/meaning**, because "tiden" becomes "mediantiden" and the comparison period is named. The new sentence agrees with the note's figures: two working days against three.

There are no other differences. Frontmatter: none in either text. Formatting is unchanged.

## 2. False statements

1. Statement: "Inledningsstycket nämner reparationsloggen, de åtta veckorna och de två husen igen, eftersom brödtexten ska gå att läsa utan ingressen. Därefter går det vidare med gruppens mål och resultatet." It is about the returned text's lead paragraph. Contradicting passage: "Att se samma information över skiftgränserna var vad underhållsgruppen på Elm Quay Housing ville få ut av sin gemensamma reparationslogg. Försöket pågick i åtta veckor och omfattade två hus." What is true: the group's goal comes first, in the same sentence as the log and before the eight weeks and the two houses. The paragraph does not move on to the goal after naming those three things. Only the result follows them.

I found no other false statement. I checked these and found them true:
- the headline length of 64 characters;
- "Siffrorna gäller dessutom mediantiden";
- "Rubriken nämner inte längre Elm Quay, men kundens namn står kvar i ingressen och brödtexten";
- "utan att ange någon orsak";
- "Inga påståenden har tagits bort eller lagts till. De två ovan är de enda som har ändrats";
- "Ingressen, bylinen, mellanrubrikerna, citaten och formateringen är oförändrade";
- the placement of Lind's quotation "i sista avsnittet".

Finding 2 calls the lead's claim "ett orsakspåstående som texten själv avvisar". This comes close to the line, but I do not count it as false. To reject (avvisa) a claim is to refuse to accept it, which is not the same as asserting its negation. The same finding goes on to say exactly what the passage says: "säger däremot att anteckningen inte tillskriver programvaran skillnaden, eftersom perioderna hade olika arbetsbelastning". That matches "anteckningen tillskriver därför inte skillnaden programvaran".

## 3. The account

- Difference 1 (headline) is reported in finding 1 and under "Påståenden som ändrats". The report is accurate: it quotes the old and new headline correctly and correctly says the opinion is Lind's, in her final quotation. The anatomy note on the resulting 64-character length is also accurate.
- Difference 2 (lead sentence) is reported in finding 2 and under "Påståenden som ändrats". The report is accurate: it quotes the before and after correctly, and correctly says that the new sentence gives no cause and that the change concerns the median.
- "Övriga ändringar" says nothing else changed, which the diff confirms.

## 4. The frozen expectation

**Detect.** The run should detect that the lead's statement that the log cut the time by one working day is a causal claim the text does not carry, because the note compares the medians of two periods with different workloads and for that reason does not credit the difference to the software. **Met.** Finding 2 says: "Inledningsstycket: ett orsakspåstående som texten själv avvisar. '… och loggen kortade tiden från anmälan till tilldelning med en arbetsdag' angav loggen som orsak. Avsnittet 'Två perioder med olika arbetsbelastning' säger däremot att anteckningen inte tillskriver programvaran skillnaden, eftersom perioderna hade olika arbetsbelastning. Siffrorna gäller dessutom mediantiden …"

**Preserve.** All met:
- The note's figures are preserved verbatim: "registrerades 31 ärenden under åtta veckor. Akuta ärenden och tidigare beställda arbeten ingick inte. Mediantiden från anmälan till tilldelning var två arbetsdagar. Under de föregående åtta veckorna var den tre."
- The sentence saying the note does not credit the difference to the software is preserved: "Perioderna hade olika arbetsbelastning, och anteckningen tillskriver därför inte skillnaden programvaran."
- Maya Lind's first quotation is preserved: "– Vi lade mer tid på att enas om kategorierna än på att lägga in de första ärendena. Den tiden skulle jag avsätta innan nästa hus börjar, säger Maya Lind, arbetsledare på Elm Quay."
- Her second quotation is preserved: "– Jag skulle välja att göra försöket igen. Att ha en gemensam bild av ärendena hjälper oss, men jag skulle lägga till en vecka för förberedelser, säger Lind."
- The supplier publication disclosure is preserved: "Kundcaset publiceras av leverantören Svale."
- The checklist link is preserved: "[Svales checklista för införandet](https://example.invalid/svale/checklist)".

**Reject.**
- A rewrite that keeps the causal claim: **not done.** The new lead names no cause: "under försöket var mediantiden från anmälan till tilldelning en arbetsdag kortare än under de föregående åtta veckorna."
- A reply saying the note states or shows that the software did not cause the difference, or that the workload did: **not done.** The reply says "inte tillskriver programvaran skillnaden, eftersom perioderna hade olika arbetsbelastning". That sentence gives the workload as the note's reason for not crediting the software, not as the cause of the difference. "Avvisar" is loose wording, but it is followed by the accurate account.
- Changes elsewhere in the text made on taste: **not done.** The only other change is the headline, and it is an attribution change with a stated reason in the text: "I texten är det arbetsledaren Maya Linds eget omdöme". It was not made on taste. It is more than the text strictly needed, because attributing a spokesperson's view to her organisation was defensible, but it moves the attribution toward what the body shows and loses no claim. The organisation is still named in the ingress and the body.

## 5. R1

**Pass.** The deciding passage is the lead's last sentence. The run replaced "loggen kortade tiden från anmälan till tilldelning med en arbetsdag" with "under försöket var mediantiden från anmälan till tilldelning en arbetsdag kortare än under de föregående åtta veckorna". This removes the unsupported causal claim and keeps the note's figures, its non-attribution sentence, both quotations, the disclosure and the link verbatim. No change was made on taste.

The headline's change of attribution is reported and grounded in the body's quotation, so it does not tip the verdict. The one false statement concerns the reply's description of the lead paragraph's order, not a change to the text.
