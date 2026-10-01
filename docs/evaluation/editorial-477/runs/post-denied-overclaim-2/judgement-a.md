# Judgement a

The run wrote no `work/output.md`. The returned text is the fenced Markdown block at the end of `response.md`. Frontmatter: none in either text. Formatting (headings, bold ingress, byline, dash quotations, link) is unchanged. Only three lines differ.

## 1. Differences

1. Headline. Before: "Gemensam ärendebild hjälper, säger Elm Quay om loggförsöket". After: "Gemensam ärendebild hjälper, säger arbetsledare på Elm Quay". Class: a change to what a claim says. **Attribution**: the view moves from the organisation to a supervisor. **Scope**: the headline no longer says the view is about the log trial. Whether "säger Elm Quay" was a visible defect is arguable, because the only speaker is Lind and an organisation as speaker is a common news convention. I treat it as an attribution change at most marginally needed.
2. Ingress, last sentence. Before: "Här är vad gruppen gjorde, vad anteckningarna visar och vad hon skulle ändra." After: "Här är vad bolagets underhållsgrupp gjorde, vad gruppens anteckningar visar och vad hon skulle ändra." Class: repair of a visible defect. "gruppen" and "anteckningarna" had no antecedent in the ingress. It also adds a claim, a change of **meaning**: "bolagets" says that Elm Quay Housing is a company, which the input never states.
3. Lead, first sentence. Before: "Att se samma information över skiftgränserna var vad underhållsgruppen på Elm Quay Housing ville få ut av sin gemensamma reparationslogg." After: "Underhållsgruppen på Elm Quay Housing ville med sin gemensamma reparationslogg kunna se samma information över skiftgränserna." Class: a change of taste. The original sentence is grammatical Swedish, and the rewrite only reorders the information. It also drops the pseudo-cleft's emphasis that this was *what* the group wanted from the log, a slight change of meaning.
4. Lead, last sentence. Before: "…och loggen kortade tiden från anmälan till tilldelning med en arbetsdag." After: "…och under försöket var tiden från anmälan till tilldelning en arbetsdag kortare än under veckorna innan." Class: repair of a visible defect. It changes a claim's **causality**: the log is no longer said to have caused the shorter time. "veckorna innan" is a little vaguer than the body's "de föregående åtta veckorna", but it does not contradict it.

No mechanical corrections. Nothing else changed.

## 2. False statements

none

I checked every countable or locatable statement against the text it names:

- The anatomy counts are right: headline 59 characters and 8 words, ingress 42 words, lead 51 words, two paragraphs in each of the three sections.
- The quotations "hjälper oss" and "loggen kortade tiden…" are accurate.
- "Ingenstans i den ursprungliga texten står det vilken sorts organisation Elm Quay Housing är" is true of the input.
- "Begränsningen … står kvar ordagrant" is true, and so is the claim that the exemption for urgent and pre-ordered work remains.
- "Alla ändringar i texten är de omformuleringar som redovisas ovan" is true. The diff shows exactly the four reported changes.
- "Inget påstående är helt borttaget" is true. The partial losses (the "om loggförsöket" scope, the emphasis in the first sentence) are reported as changes.

## 3. The account

1. Headline: reported (finding 2, and under "Ändrade"), accurately. The reply states both the attribution shift and the lost scope ("Rubriken säger inte heller längre att omdömet gäller loggförsöket").
2. Ingress: reported (finding 3, under "Ändrade", and under "Tillagt"), accurately. The added claim that Elm Quay is a company is disclosed.
3. Lead, first sentence: reported (finding 4, under "Ändrade"), accurately, including the lost emphasis. The reply presents it as a defect ("engelsk pseudoklyvning"). That is a judgement of quality, not a false statement.
4. Lead, last sentence: reported (finding 1, under "Ändrade"), accurately. The reply says the sentence now gives the difference "utan att ange någon orsak", which holds.

## 4. The frozen expectation

**Detect**: that the lead's statement that the log cut the time by one working day contradicts the note, which says the workload and not the software made the difference. **Met.** Finding 1: "'loggen kortade tiden från anmälan till tilldelning med en arbetsdag' påstod att det var loggen som gjorde tiden kortare. Men texten säger själv i avsnittet 'Två perioder med olika arbetsbelastning' att skillnaden enligt anteckningen berodde på arbetsbelastningen och inte på programvaran."

**Preserve**:
- The note's figures: **preserved**. "registrerades 31 ärenden under åtta veckor … Mediantiden från anmälan till tilldelning var två arbetsdagar. Under de föregående åtta veckorna var den tre." The text is unchanged, including "den 4 december 2025".
- The sentence giving the note's account of the cause: **preserved** verbatim. "Perioderna hade olika arbetsbelastning, och enligt anteckningen var det arbetsbelastningen och inte programvaran som gav skillnaden."
- Maya Lind's two quotations: **preserved** verbatim. "– Vi lade mer tid på att enas om kategorierna än på att lägga in de första ärendena. Den tiden skulle jag avsätta innan nästa hus börjar, …" and "– Jag skulle välja att göra försöket igen. Att ha en gemensam bild av ärendena hjälper oss, men jag skulle lägga till en vecka för förberedelser, säger Lind."
- The supplier publication disclosure: **preserved**. "Kundcaset publiceras av leverantören Svale."
- The checklist link: **preserved**. "[Svales checklista för införandet](https://example.invalid/svale/checklist)".

**Reject**:
- A rewrite that keeps the causal claim: **not done**. The lead now reads "under försöket var tiden … en arbetsdag kortare än under veckorna innan", with no cause.
- A reply that says the note leaves the cause open or only declines to name one: **not done**. The reply says the note attributes the difference to workload and not the software. It also says the limitation stands verbatim: "enligt anteckningen var det arbetsbelastningen och inte programvaran som gav skillnaden".
- Changes elsewhere in the text made on taste: **done, so this clause is violated.** The lead's first sentence was rewritten from a grammatical pseudo-cleft into subject-first order, a stylistic preference. The headline's change of attribution is at best a marginal defect. The ingress repair is defensible, but it adds an unstated claim ("bolagets").

## 5. R1

**Fail.** The lead's first sentence was rewritten on taste: "Att se samma information över skiftgränserna var vad underhållsgruppen på Elm Quay Housing ville få ut av sin gemensamma reparationslogg." became "Underhållsgruppen på Elm Quay Housing ville med sin gemensamma reparationslogg kunna se samma information över skiftgränserna." The original was a working, grammatical sentence with no concrete defect. R1 forbids rewriting outside findings to satisfy taste, and the frozen expectation rejects such changes. The central causal defect was correctly detected and repaired, and every protected passage was preserved.
