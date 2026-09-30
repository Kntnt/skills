# Judgement a

## 1. Differences

None. `work/output.md` is byte-for-byte identical to `work/input.md` (`diff` exits 0). This covers the headline, the standfirst, the `Text: Iris Falk` byline, all three subheadings, both quotations, the numbers, the supplier disclosure and the checklist link. There are no mechanical corrections, no repairs, no changes of taste and no changes to any claim. The input has no frontmatter, and none was added.

## 2. The account

There are no differences to account for. The reply states this correctly: "Jag har skrivit texten oförändrad till `output.md`" and "`output.md` byte för byte identisk med `input.md`". Both statements are true.

The reply also describes a correction round that it threw away. That round changed the headline, the standfirst, the first paragraph and the subheading "Två perioder med olika arbetsbelastning" → "Tilldelningen tog i median två arbetsdagar mot tre före försöket". The reply says it discarded the round because the new subheading dropped the workload caveat and widened "de föregående åtta veckorna" to "före försöket". Those are changes of certainty and chronology. Nothing from the discarded round is in the returned text, so it cannot be checked against the file, and it counts as neither a difference nor a loss. The account of the round agrees with itself, and it gives a sound reason for discarding it.

## 3. The frozen expectation

**"Conforms to the anatomy."** Not met by the reply. The text is expected to be clean, but the reply reports four findings and concludes "Texten uppfyller därför inte anatomin fullt ut". The findings:

1. The headline "säger vad Elm Quay gjorde, men inte vad det gav kunden", and the definite "reparationsärendena" overstates scope.
2. The standfirst says "vad anteckningarna visar" without saying which notes.
3. The first body paragraph "börjar prata om 'Försöket'" without introducing it.
4. The subheading "Två perioder med olika arbetsbelastning" "är svår att förstå utan att läsa avsnittet" and repeats the section's second paragraph.

All four are judgements of content and self-sufficiency. The frozen expectation treats the text as conforming, so these are false positives on a control. Findings 2 and 3 are also weak on the text itself: the standfirst says what the trial was, and the body's first paragraph names "sin gemensamma reparationslogg" before it says "Försöket".

**Preserve customer agency.** Preserved: "Kategorierna i loggen var underhållsgruppens egna. Leverantören Svale konfigurerade loggen efter dem".

**Preserve the qualified appraisal.** Preserved: "Jag skulle välja att göra försöket igen. Att ha en gemensam bild av ärendena hjälper oss, men jag skulle lägga till en vecka för förberedelser".

**Preserve the numbers.** Preserved: "registrerades 31 ärenden under åtta veckor … Mediantiden från anmälan till tilldelning var två arbetsdagar. Under de föregående åtta veckorna var den tre." The caveat "anteckningen tillskriver därför inte skillnaden programvaran" is also intact. The run deliberately discarded a repair that would have weakened it.

**Preserve the supplier publication disclosure.** Preserved: "Kundcaset publiceras av leverantören Svale."

**Preserve the checklist link that carries the call to action.** Preserved: "[Svales checklista för införandet](https://example.invalid/svale/checklist)". The reply also says "uppmaningen bygger på den länk som finns".

**No required quote count or extra sales block.** Not violated. The reply demands neither.

**Reject findings against limits the text meets (36-character headline, 40-word standfirst, 36–39-character subheadings).** Not violated. The reply says "mätskriptet hittade inga fel i det som går att räkna, som längder och antal". Finding 1 is about what the headline says, not its length. Finding 4 is about what the subheading describes, not its length.

**Reject findings resting on the one-sentence paragraph, the four-sentence paragraph or one section's paragraph count.** Not violated. No finding rests on any of them.

**Reject a finding against the Swedish `Text:` byline form.** Not violated. There is no such finding, and the byline is unchanged.

## 4. R1

**Pass.** R1 is judged on the returned text, and the returned text is identical to the input: "Därför är `output.md` byte för byte identisk med `input.md`." The clean text was not rewritten to satisfy taste or numerical guidelines. Every voice, argument, quotation and claim survives, and nothing depended on a source the Skill did not have.

The run's weakness is in detection. It reported four anatomy findings on a text the corpus says conforms. That is scored apart from the final text, but it means the "conforms to the anatomy" clause is not met in the reply's own verdict.
