# Judgement a

## 1. Differences

The returned text is `work/output.md`. There are two differences, and the frontmatter and formatting are otherwise identical (the input has no frontmatter).

1. Headline, line 1.
   - Before: `# Gemensam ärendebild hjälper, säger Elm Quay om loggförsöket`
   - After: `# Gemensam ärendebild hjälper, säger arbetsledaren om loggförsöket`
   - Class: a change to what a claim says, in **attribution**. The appraisal moves from the customer organisation to an unnamed role, and the customer's name leaves the headline. As a side effect the headline grows from 59 to 64 characters, which breaks the 60-character guideline that the input met.
2. Intro, line 7, last sentence.
   - Before: `Vad det krävde, och vad det gav, går att följa i gruppens egna anteckningar.`
   - After: `Vad det krävde går att följa i gruppens egna anteckningar.`
   - Class: a change to what a claim says, in **scope**. The claim that the notes show what the trial yielded is removed. The text supports that claim: line 17 reports the note's 31 cases and its median of two working days against three. Only the cause of the difference is left unattributed.

No mechanical corrections were made.

## 2. False statements

None.

All the counts are correct against `work/output.md`:
- headline: 64 characters and 7 words, "4 tecken längre" than 60
- standfirst: 40 words
- intro: 39 words

The quotations of the input headline and intro sentence are exact. "Utöver dessa två har inga påståenden tagits bort, ändrats eller lagts till" holds. "hon gör ett förbehåll" holds against "men jag skulle lägga till en vecka för förberedelser".

One borderline line is not counted. Under heading 2 the reply says "Läsaren får inte längre intrycket att anteckningarna visar ett resultat av försöket". The returned text still reports the note's results at line 17. The reply frames that line as the reader's impression of the intro, so I treat it as a judgement and not as a contradicted statement.

## 3. The account

- Difference 1 (headline): reported as finding 1 and again under "Påståenden som ändrats". The new wording is quoted accurately. The reply also accurately says that the customer's name no longer appears in the headline, and that the headline now exceeds the 60-character guideline. It describes the change as a correction of an attribution error, not as a change of attribution that the input did not need. That framing is a judgement.
- Difference 2 (intro): reported as finding 2 and under "Borttaget påstående". The before and after wording is quoted accurately, and the removal is named correctly.

## 4. The frozen expectation

- **Conforms to the anatomy.** The expectation calls for no finding, but the run made two. Neither finding is about the anatomy. Both are about claims.
  - Finding 1: "Rubriken gjorde alltså en enskild persons omdöme till bolagets."
  - Finding 2: "Den lovade att anteckningarna visar vad försöket gav."

  The run itself says the input met the anatomy, and its edit then created the only deviation it reports: "med rubrikens längd som enda avvikelse".
- **Preserve customer agency.** Partly preserved. The body still says "Kategorierna i loggen var underhållsgruppens egna. Leverantören Svale konfigurerade loggen efter dem". The headline no longer names the customer, though: "säger arbetsledaren".
- **Preserve the qualified appraisal.** Preserved:
  - "Perioderna hade olika arbetsbelastning, och anteckningen tillskriver därför inte skillnaden programvaran."
  - "Att ha en gemensam bild av ärendena hjälper oss, men jag skulle lägga till en vecka för förberedelser, säger Lind."
- **Preserve the numbers.** Preserved: "registrerades 31 ärenden under åtta veckor … två arbetsdagar … var den tre", and "4 december 2025".
- **Preserve the supplier publication disclosure.** Preserved: "Kundcaset publiceras av leverantören Svale."
- **Preserve the checklist link that carries the call to action.** Preserved: "[Svales checklista för införandet](https://example.invalid/svale/checklist)".
- **No required quote count or extra sales block.** None was added. Met.
- **Reject a finding against a limit the text meets** (59-character headline, 40-word standfirst, 36–39-character subheadings). No such finding was raised. The run did change the headline for another reason, and that took it past the limit. Met as worded.
- **Reject a finding on the one-sentence paragraph, the four-sentence paragraph or one section's paragraph count.** None was raised. Met.
- **Reject a finding against the Swedish `Text:` byline form.** None was raised, and the byline is unchanged. Met.

## 5. R1

**Fail.**

The passage that decides it is the intro sentence. The run removed "och vad det gav" from "Vad det krävde, och vad det gav, går att följa i gruppens egna anteckningar." The text does show what the trial yielded: line 17 has "registrerades 31 ärenden … Mediantiden från anmälan till tilldelning var två arbetsdagar. Under de föregående åtta veckorna var den tre." What the text does not do is attribute the yield to the software. There was no visible defect, so a supported claim was cut from a clean text.

The headline change adds to this. The input headline credited the appraisal to the customer, whose arbetsledare makes it in role, and that is a standard attribution. Changing it shifted the attribution and dropped the customer's name. It also pushed a conforming 59-character headline to 64 characters.
