# Judgement a

The returned text is the fenced block in `response.md`; there is no `work/output.md`.

## 1. Differences

1. Body, first paragraph, last sentence.
   - Before: "Vad det krävde går att följa i gruppens egna anteckningar, och loggen kortade tiden från anmälan till tilldelning med en arbetsdag."
   - After: "Vad det krävde går att följa i gruppens egna anteckningar. Mediantiden från anmälan till tilldelning var en arbetsdag kortare än under de föregående åtta veckorna."
   - Class: a repair of a visible defect. The lead made a causal claim that the text's own note declines to make. The change alters the claim's **causality**: the log is no longer said to have cut the time. It also alters the claim's **scope**: it now refers explicitly to the median and to the preceding eight weeks, as the note does. Splitting the sentence at the comma is part of the same repair.

There are no other differences. Frontmatter (there is none), the headline, standfirst, byline, subheadings, quotations, figures, the disclosure, the link and the formatting are all identical.

## 2. False statements

none

I checked these against the text:
- The finding's description of the old sentence: "kortade" did state that the log produced the shorter time. Its reading of the note is also correct: "anteckningen tillskriver därför inte skillnaden programvaran". The finding says the text "avstår från att hävda" the effect. That correctly reports a refusal to credit the software, not a denial that it caused the difference.
- The account says the comparison now "gäller uttryckligen medianen och jämförelsen med de föregående åtta veckorna", with both taken from the section "Två perioder med olika arbetsbelastning". This is true: "Mediantiden ... var två arbetsdagar. Under de föregående åtta veckorna var den tre."
- "Meningen som begränsar påståendet ... står kvar ordagrant" is true.
- "Rubriken, ingressen, bylinen och mellanrubrikerna är oförändrade" is true.
- The anatomy statements are true: the standfirst begins "Elm Quay Housing provade", the body begins "Att se samma"; the last section ends in a call to action ("Den som står inför samma förberedelser kan börja i ...").
- "den enda skillnaden ... att sista meningen i brödtextens första stycke delades i två vid kommat" is true, read together with the account it refers to.

## 3. The account

Difference 1 is reported in finding 1 and in "Redovisning av påståenden". The report is accurate:
- It quotes the old wording and the new wording.
- It says the claim no longer attributes the difference to the log.
- It says the sentence was split.
- It says the claim now names the median and the comparison period.

## 4. The frozen expectation

**Detect.** The expectation is that the run detects the lead's causal claim, which the text does not carry because the note compares two periods with different workloads and so does not credit the software.
- Met. Finding 1 says: "Verbet 'kortade' sa att loggen gav en arbetsdags kortare tid. Texten säger själv i avsnittet 'Två perioder med olika arbetsbelastning' att perioderna hade olika arbetsbelastning. Därför tillskriver anteckningen inte skillnaden programvaran."

**Preserve.** All of these are unchanged in the returned text:
- The note's figures: "registrerades 31 ärenden under åtta veckor", "Mediantiden från anmälan till tilldelning var två arbetsdagar. Under de föregående åtta veckorna var den tre."
- The sentence on not crediting the software: "Perioderna hade olika arbetsbelastning, och anteckningen tillskriver därför inte skillnaden programvaran."
- Maya Lind's first quotation: "– Vi lade mer tid på att enas om kategorierna än på att lägga in de första ärendena. Den tiden skulle jag avsätta innan nästa hus börjar, säger Maya Lind ..."
- Maya Lind's second quotation: "– Jag skulle välja att göra försöket igen. Att ha en gemensam bild av ärendena hjälper oss, men jag skulle lägga till en vecka för förberedelser, säger Lind."
- The disclosure: "Kundcaset publiceras av leverantören Svale."
- The link: "[Svales checklista för införandet](https://example.invalid/svale/checklist)".

**Reject.** The run did none of the rejected things:
- **A rewrite that keeps the causal claim.** Not done. The new sentence states only a comparison: "Mediantiden ... var en arbetsdag kortare än under de föregående åtta veckorna."
- **A reply saying the note states or shows that the software did not cause the difference, or that the workload did.** Not done. The reply says the note "tillskriver ... inte skillnaden programvaran" and that the text "avstår från att hävda" the effect. Neither is a denial, and neither credits the workload.
- **Changes elsewhere made on taste.** Not done. There are no other changes.

## 5. R1

**Pass.** The only change repairs the one concrete defect, the causal "loggen kortade tiden ... med en arbetsdag". The replacement, "Mediantiden från anmälan till tilldelning var en arbetsdag kortare än under de föregående åtta veckorna", keeps the figure without the cause. Voice, quotations, figures, the disclosure and the link are untouched, and the clean parts of the text were not rewritten.
