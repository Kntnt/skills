# Judgement a

## 1. Differences

A line-by-line diff of `work/input.md` against the returned text (response.md, lines 2–24) shows exactly one changed line. The frontmatter, headline, standfirst, byline, subheadings, paragraph breaks and emphasis are all unchanged.

1. The opening paragraph, first sentence.
   - Before: "Kommunstyrelsen i Lervik bör skjuta upp bytet till enbart digital bokning av föreningslokaler."
   - After: "Kommunstyrelsen i Lervik bör skjuta upp bytet till enbart digital bokning av föreningslokaler, ett byte som kan ske i september."
   - Class: a change of taste presented as the repair of a visible defect. Measured as a claim, the added clause repeats something the standfirst already says ("I september kan telefonbokningen … försvinna") with the same modal "kan". It does not change the claim's scope, certainty, attribution, chronology, causality or meaning. It only adds the claim a second time, in the body. I do not count it as a defect repair because the body was already readable without the standfirst. The thesis sentence asks for the switch to be postponed, which tells the reader that a switch is scheduled. The closing line, "för att kalendern säger september", names the month itself, so its point does not depend on anything said earlier.

2. Formatting of the delivery. The returned text comes wrapped in a ```` ```markdown ```` code fence that the input does not have. This belongs to how the reply is presented, not to the text, and it changes no content.

No mechanical corrections were made. The reply says the proofreading pass found nothing.

## 2. The account

1. The added September clause. **Reported, and the description of the change is accurate.** Finding 1 names the location ("inledningens första mening"), quotes the added words ("kan ske i september") and says that the headline, standfirst and subheadings are unchanged. Under "Påståenden" it says the clause is copied from the standfirst with the same "kan", which is true. The finding's premise is overstated, though. It claims that a reader who skips the standfirst "fick aldrig veta att bytet kan ske i september, och därför gick slutradens poäng inte att förstå". The closing line states the month itself, and "skjuta upp bytet" already tells the reader that a switch is scheduled.
2. The code fence. Not reported. Nothing needed reporting, because it is presentation and not an edit.

## 3. The frozen expectation

**Detect / assess**

- "Conforms to the anatomy." **Not met.** The run does confirm every counted limit: "rubriken har 47 tecken och 6 ord", "ingressen har 39 ord och är ett stycke". But it also reports an anatomy breach that the expectation does not recognise: "Brödtexten ska gå att läsa utan ingressen, men september nämndes bara i ingressen." The run then rewrote the text to fix it. The expectation says the text conforms, so this finding is a false positive, and the text was edited because of it.

**Preserve**

- The polemical final sentence. **Preserved** word for word: "Ett antagande blir inte ett beslutsunderlag för att kalendern säger september."
- The early thesis. **Preserved.** It still opens the body: "Kommunstyrelsen i Lervik bör skjuta upp bytet till enbart digital bokning av föreningslokaler, …". The appended clause makes the sentence longer but does not soften or delay the demand.
- The attribution. **Preserved:** "Kommunens pilotrapport från den 8 april 2026 räknar 96 webbokningar och 24 telefonbokningar …".
- The real administrative objection. **Preserved:** "Förvaltningen vill slippa dubbel administration. Det är en relevant invändning."
- The cost uncertainty. **Preserved:** "Men handlingarna innehåller ingen mätning av tidsåtgången." and "ta ställning till dess ännu okända kostnad".
- The ending's named decision for the council. **Preserved:** "Kommunstyrelsen bör därför säga ja till halvåret med båda bokningsvägarna, ta ställning till dess ännu okända kostnad och ge förvaltningen i uppdrag att mäta tidsåtgången samt fråga användarna …".
- No flattening to neutral exposition and no generic hedges. **Met.** Nothing was flattened. The one addition keeps the standfirst's "kan" and adds no new hedge.

**Named rejections**

- A finding against a limit the text meets (47-character headline, 39-word standfirst, 33–40-character subheadings). **Not made.** The run measured the limits and passed them.
- A finding resting on the single-paragraph section. **Not made.**
- A finding resting on the one-sentence closing paragraph. **Not made.**
- A finding resting on the four-sentence paragraph. **Not made.**
- A finding against the Swedish `Text:` byline. **Not made.** The byline is untouched.

## 4. R1

**Fail.** The deciding passage is R1's rule, "Clean texts may not be rewritten to satisfy taste or numerical guidelines", read together with the expectation's first clause, "Conforms to the anatomy". The run edited a text that the standard calls clean, on the strength of this finding: "Den som hoppade över ingressen fick aldrig veta att bytet kan ske i september, och därför gick slutradens poäng inte att förstå." That premise does not hold. The closing line "för att kalendern säger september" states the month itself, and "bör skjuta upp bytet" already tells the reader that a switch is scheduled. The change is a restyling of a clean text, not the repair of a concrete visible defect.

The failure is narrow. No claim was changed, every element the expectation says to preserve survives verbatim, the account of the edit is accurate, and the run avoided all five named false positives.
