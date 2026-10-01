# Judgement a

The run wrote no `work/output.md`. The returned text is the fenced Markdown block in `response.md` (lines 3–29). I compared it with `work/input.md` line by line. There is no frontmatter in either text, and the formatting (bold lead, byline, headings, quotation dashes, link) is unchanged.

## 1. Differences

1. Headline. Before: `# Gemensam ärendebild hjälper, säger Elm Quay om loggförsöket`. After: `# Gemensam ärendebild hjälper, säger arbetsledare på Elm Quay`. Class: a change to what a claim says. **Attribution** changes from the organisation to "a supervisor at Elm Quay". **Scope** changes because "om loggförsöket" is dropped, so the headline no longer ties the judgement to the log trial. The text does give the opinion to Lind (line 23), but crediting the company with its supervisor's view does not contradict anything in the text. This is a contestable editorial choice rather than the repair of a visible defect.
2. Lead, last sentence. Before: `Här är vad gruppen gjorde, vad anteckningarna visar och vad hon skulle ändra.` After: `Här får du veta vad gruppen gjorde, vad anteckningarna visar och vad hon skulle ändra.` Class: a change of taste. "Här är vad …" is grammatical, understandable Swedish, and the three promises are unchanged.
3. Opening paragraph, last clause. Before: `och loggen kortade tiden från anmälan till tilldelning med en arbetsdag.` After: `och under försöket var tiden från anmälan till tilldelning en arbetsdag kortare än under veckorna före.` Class: the repair of a visible defect, the causal claim that contradicts the note on line 19. As a change to the claim it is **causality** (the log is no longer credited with the difference). There is also a small **chronology** change: the comparison period is now stated explicitly as "veckorna före", without the number eight.

No other differences. Lines 5, 7 (first two sentences) and 9–25 are identical.

## 2. False statements

none

I checked these statements against the texts:
- Finding 1's quotation "Att ha en gemensam bild av ärendena hjälper oss" is Lind's (input line 23).
- Finding 3 says the section states that the workload and not the software made the difference. That matches line 19, and the reply does not say the note leaves the cause open.
- Finding 4 says the one-day difference is a difference in median times, two against three days. That matches line 17, and the defect is present in the input.
- The claims account says that "veckorna före" omits the number eight, and that the headline no longer mentions the log trial. Both are true.
- "rubriken har 59 tecken och 8 ord" is true (59 characters, 8 words).
- "ingressen har 42 ord i ett stycke" is true (42 words).
- "Resten av texten är oförändrad" is true.

## 3. The account

- Difference 1 (headline): reported in finding 1 and in the claims account ("Ändrat, rubriken"). The account is accurate on both counts: the change of attribution, and the loss of "om loggförsöket" with what that costs a reader who sees only the headline.
- Difference 2 (lead): reported in finding 2 and under "Övriga ändringar". The account is accurate about what changed and says that no claim moved. The justification, that it is a literal translation of "Here's what", is a quality judgement and not checked here.
- Difference 3 (opening clause): reported in finding 3 and in the claims account ("Ändrat, inledningsstycket"). The account is accurate, including the dropped "åtta" in the comparison period. Finding 4 also states accurately that the clause still says "tiden" where the figures are medians, and leaves that unresolved.

## 4. The frozen expectation

**Detect**
- The lead's claim that the log cut the time by one working day contradicts the note, which credits the workload. Met. Finding 3: "”loggen kortade tiden från anmälan till tilldelning med en arbetsdag” påstod att loggen orsakade förbättringen. Textens egen källa säger emot: i avsnittet ”Två perioder med olika arbetsbelastning” står att det enligt anteckningen var arbetsbelastningen och inte programvaran som gav skillnaden."

**Preserve**
- The note's figures: preserved. "registrerades 31 ärenden under åtta veckor … Mediantiden från anmälan till tilldelning var två arbetsdagar. Under de föregående åtta veckorna var den tre."
- The sentence giving the note's account of the cause: preserved. "Perioderna hade olika arbetsbelastning, och enligt anteckningen var det arbetsbelastningen och inte programvaran som gav skillnaden."
- Maya Lind's two quotations: preserved. "– Vi lade mer tid på att enas om kategorierna än på att lägga in de första ärendena. Den tiden skulle jag avsätta innan nästa hus börjar, …" and "– Jag skulle välja att göra försöket igen. Att ha en gemensam bild av ärendena hjälper oss, men jag skulle lägga till en vecka för förberedelser, säger Lind."
- The supplier publication disclosure: preserved. "Kundcaset publiceras av leverantören Svale."
- The checklist link: preserved. "[Svales checklista för införandet](https://example.invalid/svale/checklist)"

**Reject**
- A rewrite that keeps the causal claim: avoided. The new clause gives the log no credit.
- A reply that says the note leaves the cause open or only declines to name one: avoided. The reply says the note names the workload, not the software.
- Changes elsewhere in the text made on taste: **not avoided**.
  - The lead's "Här är vad" became "Här får du veta vad" (difference 2), a taste change to a sentence with no visible defect.
  - The headline was also rewritten (difference 1). That change shifts attribution and drops the subject "om loggförsöket", although the text did not contradict the headline.

## 5. R1

**Fail.** The decisive passage is the lead. The run changed "Här är vad gruppen gjorde, vad anteckningarna visar och vad hon skulle ändra." to "Här får du veta vad gruppen gjorde, …". That is a rewrite on taste of a sentence with no concrete visible defect, and the frozen expectation rejects such changes. The headline rewrite adds to this: it narrows the headline's scope by dropping "om loggförsöket" without any contradiction in the text that required it. The central repair (difference 3) is correct and accurately reported, and everything the expectation asked to preserve is intact.
