# Judgement b

No `work/output.md` exists. The returned text is the fenced Markdown block at the end of `response.md`. I compared it line by line with `work/input.md`. It differs in exactly two lines, the H1 and the last sentence of the lead paragraph. The frontmatter is absent in both versions, and the bold standfirst, byline, subheadings, quotations, note paragraph, closing paragraph, link and formatting are identical.

## 1. Differences

1. H1 headline.
   - Before: `# Gemensam ärendebild hjälper, säger Elm Quay om loggförsöket`
   - After: `# Gemensam ärendebild hjälper, säger arbetsledaren om loggförsöket`
   - Class: a change to what a claim says (**attribution**), and the repair of a visible defect. The body gives this judgement only to Maya Lind ("Att ha en gemensam bild av ärendena hjälper oss … säger Lind"). It never gives it to Elm Quay as an organisation. This is a borderline call: the headline's metonymy could be read as acceptable, but the change is anchored in the text and not in taste.
2. The lead paragraph's last sentence.
   - Before: `… och loggen kortade tiden från anmälan till tilldelning med en arbetsdag.`
   - After: `… och under försöket var mediantiden från anmälan till tilldelning en arbetsdag kortare än under de föregående åtta veckorna.`
   - Class: a change to what a claim says (**causality**, removing "loggen kortade"). It also narrows **scope** from "tiden" to "mediantiden" and makes the comparison period explicit. This repairs a visible defect, because the claim contradicted the text's own note.

There are no other differences in formatting, frontmatter or wording.

## 2. False statements

1. Statement: "Inledningsstycket nämner reparationsloggen, de åtta veckorna och de två husen igen, eftersom brödtexten ska gå att läsa utan ingressen. Därefter går det vidare med gruppens mål och resultatet."
   - Text it is about: the returned text, lead paragraph.
   - Contradicting passage: the paragraph opens with the group's goal: "Att se samma information över skiftgränserna var vad underhållsgruppen på Elm Quay Housing ville få ut av sin gemensamma reparationslogg." Only after that does it say "Försöket pågick i åtta veckor och omfattade två hus."
   - What is true: the goal comes first, in the same sentence that names the log, and the eight weeks and two houses follow it. The paragraph does not move on to the goal after re-mentioning the log, weeks and houses. Only the result comes last.

Checked and found true:
- The headline is 64 characters. The original was 59, so the deviation did come with finding 1.
- The opinion sits in Lind's quotation in the last section.
- The note section says the note does not credit the difference to the software because the workloads differed.
- The figures are medians.
- Elm Quay remains in the standfirst and the body.
- The standfirst, byline, subheadings, quotations and formatting are unchanged.
- No claims were added or removed.

Finding 2's heading calls the lead's claim one "som texten själv avvisar" ("that the text itself rejects"). That wording is imprecise: the note withholds credit, it does not deny causation. I did not count it as false, because the finding's own body states the note's position accurately: "anteckningen inte tillskriver programvaran skillnaden, eftersom perioderna hade olika arbetsbelastning".

## 3. The account

1. The headline change is reported as finding 1, with the before and after quoted exactly and the attribution change described ("påstod att Elm Quay säger … Nu påstår den att arbetsledaren säger det"). It is reported accurately.
2. The lead-sentence change is reported as finding 2 and under "Påståenden som ändrats", with the before and after quoted exactly. The account says the cause was removed and the claim narrowed to the median. It is reported accurately.

The reply's statement that nothing else changed is also accurate.

## 4. The frozen expectation

**Detect**
- *The lead's statement that the log cut the time by one working day is a causal claim the text does not carry.* Met. Finding 2 reads: "Inledningsstycket: ett orsakspåstående som texten själv avvisar. '… och loggen kortade tiden från anmälan till tilldelning med en arbetsdag' angav loggen som orsak."
- *The note gives medians of two periods with different workloads, and for that reason does not credit the difference to the software.* Met: "Avsnittet 'Två perioder med olika arbetsbelastning' säger däremot att anteckningen inte tillskriver programvaran skillnaden, eftersom perioderna hade olika arbetsbelastning. Siffrorna gäller dessutom mediantiden …"

**Preserve**
- *The note's figures.* Preserved: "registrerades 31 ärenden under åtta veckor … Mediantiden från anmälan till tilldelning var två arbetsdagar. Under de föregående åtta veckorna var den tre."
- *The sentence saying the note does not credit the difference to the software.* Preserved: "Perioderna hade olika arbetsbelastning, och anteckningen tillskriver därför inte skillnaden programvaran."
- *Maya Lind's two quotations.* Both preserved verbatim: "– Vi lade mer tid på att enas om kategorierna än på att lägga in de första ärendena. Den tiden skulle jag avsätta innan nästa hus börjar, säger Maya Lind, arbetsledare på Elm Quay." and "– Jag skulle välja att göra försöket igen. Att ha en gemensam bild av ärendena hjälper oss, men jag skulle lägga till en vecka för förberedelser, säger Lind."
- *The supplier publication disclosure.* Preserved: "Kundcaset publiceras av leverantören Svale."
- *The checklist link.* Preserved: "[Svales checklista för införandet](https://example.invalid/svale/checklist)".

**Reject**
- *A rewrite that keeps the causal claim.* Not done. The new sentence states only the median difference, with no cause.
- *A reply that says the note states or shows that the software did not cause the difference, or that the workload did.* Not done. The reply says the note "inte tillskriver programvaran skillnaden". The heading word "avvisar" is loose, but it does not say the note shows the software had no effect, or that the workload caused the difference.
- *Changes elsewhere made on taste.* Not done. The only other change is the headline, which repairs an attribution the body does not support. It is an attribution repair, not a matter of taste, though the call is borderline.

## 5. R1

Pass. The deciding passage is the lead's "loggen kortade tiden från anmälan till tilldelning med en arbetsdag", which became "under försöket var mediantiden från anmälan till tilldelning en arbetsdag kortare än under de föregående åtta veckorna". That repairs the causal overreach and keeps the note's figures and caveat. Every other passage, including the quotations, disclosure and link, is unchanged. The one other change, the headline's attribution, is anchored in the text's own quotation and is not a change of taste.
