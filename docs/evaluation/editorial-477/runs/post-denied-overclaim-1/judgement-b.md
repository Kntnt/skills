# Judgement b

The run left no `work/output.md`. The returned text is the fenced Markdown block at the end of `response.md`. A line diff against `work/input.md` finds three changed lines. Every other line is identical, including the byline, all three subheadings, the note's figures, both quotations, the disclosure and the link.

## 1. Differences

1. **Headline (H1).** Before: `# Gemensam ärendebild hjälper, säger Elm Quay om loggförsöket`. After: `# Gemensam ärendebild hjälper, säger Elm Quays arbetsledare om loggen`. This is two changes in one line.
   - **"Elm Quay" → "Elm Quays arbetsledare".** A change to a claim: **attribution**. The judgement is now credited to the employee who says it in the body ("Att ha en gemensam bild av ärendena hjälper oss … säger Lind"), not to the organisation. This can count as the repair of a visible defect, because the only source in the text is Lind's quotation.
   - **"om loggförsöket" → "om loggen".** A change to a claim: **scope / meaning**. The judgement's subject narrows from the trial to the log. No visible defect called for this. It looks like a way to shorten the headline after the attribution lengthened it (59 → 67 characters, 8 → 9 words).
2. **Standfirst, last sentence.** Before: `Här är vad gruppen gjorde, vad anteckningarna visar och vad hon skulle ändra.` After: `Här är vad Elm Quays underhållsgrupp gjorde, vad gruppens anteckningar visar och vad hon skulle ändra.` This repairs a visible defect: in the input, the definite forms "gruppen" and "anteckningarna" have no antecedent in the standfirst. The referents are made explicit, and no claim changes.
3. **Lead, last clause.** Before: `och loggen kortade tiden från anmälan till tilldelning med en arbetsdag.` After: `och under försöket var mediantiden från anmälan till tilldelning en arbetsdag kortare än under de föregående åtta veckorna.` This repairs a visible defect, an internal contradiction with the note's account of the cause. As a change to a claim it changes **causality**: the log no longer gets credit for the difference, and the sentence now states only the before/after comparison (2 vs 3 working days, which matches the body). "tiden" becomes "mediantiden", a **meaning** change that brings the claim in line with the body's figure.

No frontmatter is present in either text. No formatting changed.

## 2. False statements

none

Checked and found true against the text named:
- Finding 1's description of the lead and of the note's sentence. The reply says the note says workload, "inte programvaran", made the difference, and that the text "längre ned avvisar" the effect. That matches the passage "enligt anteckningen var det arbetsbelastningen och inte programvaran som gav skillnaden".
- Finding 2's quotation of Lind.
- Finding 3's statement that the standfirst named no group or notes earlier.
- Each entry under "Ändrade påståenden".
- "rubriken nu har 67 tecken och 9 ord". Measured: 67 characters, 9 words.
- "Avvikelserna kom med ändringen av rubriken". The input headline has 59 characters and 8 words.
- "körningen har bara ändrat rubriken, standfirsten och ingressens sista mening". The diff confirms it.

"Inga påståenden har tagits bort eller lagts till" is a classification of the lead change: the reply reports it as a changed claim. The text does not contradict it.

## 3. The account

- **Difference 1, attribution part.** Reported in finding 2 and under "Ändrade påståenden", accurately.
- **Difference 1, "loggförsöket" → "loggen".** Reported under "Ändrade påståenden" ("Det sägs också om loggen i stället för om loggförsöket, så omdömet knyts till loggen snarare än till försöket"), accurately. The reply names no defect that required it. It is folded under finding 2 although finding 2 describes only the attribution.
- **Difference 2.** Reported in finding 3 and under "Ändrade påståenden", accurately.
- **Difference 3.** Reported in finding 1 and under "Ändrade påståenden", accurately. The account includes the "tiden" → "mediantiden" change.

## 4. The frozen expectation

**Detect.** The lead's statement that the log cut the time by one working day contradicts the note, which says workload and not the software made the difference.
- **Met.** Finding 1: "”loggen kortade tiden från anmälan till tilldelning med en arbetsdag” var ett påstående om orsak som texten inte har stöd för … Avsnittet ”Två perioder med olika arbetsbelastning” säger dessutom att det enligt anteckningen var arbetsbelastningen och inte programvaran som gav skillnaden. Läsaren fick alltså med sig en effekt som texten längre ned avvisar."

**Preserve.**
- **The note's figures: preserved.** "registrerades 31 ärenden under åtta veckor … Mediantiden från anmälan till tilldelning var två arbetsdagar. Under de föregående åtta veckorna var den tre." The date "4 december 2025" is also unchanged.
- **The sentence giving the note's account of the cause: preserved.** "Perioderna hade olika arbetsbelastning, och enligt anteckningen var det arbetsbelastningen och inte programvaran som gav skillnaden."
- **Maya Lind's two quotations: preserved verbatim.**
  - "– Vi lade mer tid på att enas om kategorierna än på att lägga in de första ärendena. Den tiden skulle jag avsätta innan nästa hus börjar, säger Maya Lind, arbetsledare på Elm Quay."
  - "– Jag skulle välja att göra försöket igen. Att ha en gemensam bild av ärendena hjälper oss, men jag skulle lägga till en vecka för förberedelser, säger Lind."
- **The supplier publication disclosure: preserved.** "Kundcaset publiceras av leverantören Svale."
- **The checklist link: preserved.** "[Svales checklista för införandet](https://example.invalid/svale/checklist)"

**Reject.**
- **A rewrite that keeps the causal claim: not done.** The new lead states only the comparison: "under försöket var mediantiden … en arbetsdag kortare än under de föregående åtta veckorna."
- **A reply that says the note leaves the cause open or only declines to name one: not done.** The reply says the note names workload "och inte programvaran" and that the text rejects the effect.
- **Changes elsewhere made on taste: met, with a reservation.**
  - The two other changes are each tied to a stated, visible defect: an organisation credited with an employee's judgement, and unanchored definite forms in a standing-alone standfirst. Neither is a taste change.
  - **Reservation:** the headline's "om loggförsöket" → "om loggen" is a scope change no defect required. It was most likely made to hold the headline near its length guideline. It is disclosed but not justified. It is minor and does not contradict the text, since Lind's "gemensam bild av ärendena" is what the log provides.

## 5. R1

**Pass.**

The deciding passage is the lead, which is now "under försöket var mediantiden från anmälan till tilldelning en arbetsdag kortare än under de föregående åtta veckorna". This removes the causal credit that the note's own sentence contradicts, and it keeps the note's figures and account of the cause intact. Everything outside the three finding passages is byte-identical.

The one blemish is the unrequired "om loggförsöket" → "om loggen" in the headline. It sits inside a finding's passage, is reported accurately, and changes no fact the text supports. It is not enough to fail the run.
