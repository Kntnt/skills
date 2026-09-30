# Judgement a

Run directory: `/Users/thomas/Projects/skills/.git/kntnt-orchestrate/429.scratch/j/9e8942a218b0`

## 1. Differences

`work/input.md` and `work/output.md` differ in exactly three lines. Neither file has frontmatter. The formatting is the same in both: the bold standfirst, the `Text:` byline, the dash-led quotations, the `##` levels and the link are all unchanged.

1. **Headline (line 1).**
   Before: `# Elm Quay samlade reparationsärendena` (36 characters)
   After: `# Gemensam ärendebild hjälper, säger Elm Quays arbetsledare` (56 characters)
   Class: this changes what a claim says. The **meaning** changes: a factual statement of what the customer did becomes an appraisal attributed to Lind. The **certainty** changes too, and so does the **scope**. Her quotation is qualified ("hjälper oss, men jag skulle lägga till en vecka för förberedelser"). The headline states the benefit without the qualification and without "oss", so it reads as a general, unhedged verdict. The **attribution** is also reworded, from "arbetsledare på Elm Quay" to "Elm Quays arbetsledare". This is not the repair of a visible defect. It is a change of taste in a headline that already worked.

2. **First body paragraph, first sentence (line 7).**
   Before: `Att se samma information över skiftgränserna var vad underhållsgruppen på Elm Quay Housing ville få ut av sin gemensamma reparationslogg.`
   After: `Underhållsgruppen på Elm Quay Housing ville använda sin gemensamma reparationslogg för att se samma information över skiftgränserna.`
   Class: a syntactic repair of a front-heavy "Att … var vad …" construction, which borders on a change of taste. The propositional content is kept. The sentence loses only a small nuance, the idea of what the team wanted to "get out of" the log.

3. **Second subheading (line 15).**
   Before: `## Två perioder med olika arbetsbelastning` (39 characters)
   After: `## Tilldelningen tog i median två arbetsdagar under försöket` (57 characters)
   Class: a change of taste, and a change of **causality** framing at the level a reader skims. The old subheading carried the text's own caveat, that the two periods are not comparable. The new one shows only the favourable result. Read together with the new headline ("Gemensam ärendebild hjälper"), a reader who only skims now sees a benefit followed by a shorter time, and the caveat that blocks the causal reading is gone. The caveat still stands in the body.

## 2. The account

- **Difference 1: reported.** This is finding 1 in the reply. The reply is candid about what the headline loses: the missing "oss", the "Elm Quays arbetsledare" reading, and the qualification that is left out. The justification is inaccurate, though. The reply calls the definite form "reparationsärendena" an overclaim and says the headline fails a genre requirement to name customer benefit or a result. The text conforms to the anatomy, so the second reason is a finding against a clean text.
- **Difference 2: reported, but in the wrong place.** The reply calls the sentence "Ingressens första mening" and says in its claims section that the change is "ingressen". The ingress (the bold standfirst) is unchanged. The sentence that changed is the first sentence of the body. The reply's description of the change itself is otherwise accurate.
- **Difference 3: reported.** This is finding 2 in the reply. The reply says accurately that the caveat and the comparison with three days are gone from the subheading and that the body keeps them.
- **The reply's other statements.** It says "I övrigt är texten identisk med `input.md`", which is accurate. It says "Den avslutande språkgranskningen hittade inga fel", which is consistent with the diff. It says "Skriptet mätte gränserna" and that the text follows the anatomy without deviation. That second statement cannot be checked from these three files. However, the frozen expectation says the original 36-character headline and 36–39-character subheadings meet the limits. The replacements are 56 and 57 characters, so it is doubtful that they still do.

## 3. The frozen expectation

**"Conforms to the anatomy."** The expectation treats the text as clean, so the run should have reported no findings or only trivial ones. Instead the run reported three findings and rewrote two display elements. One finding says outright that the headline fails the genre: "Rubriken nämnde också bara en handling, inte kundens nytta eller resultat som genren kräver." **Not met.**

**Preserve:**

- **Customer agency: preserved.** "Kategorierna i loggen var underhållsgruppens egna. Leverantören Svale konfigurerade loggen efter dem och utbildade sex medarbetare." The headline also no longer names what the customer did ("samlade").
- **Qualified appraisal: preserved in the body only.** The quotation stands unchanged: "Att ha en gemensam bild av ärendena hjälper oss, men jag skulle lägga till en vecka för förberedelser, säger Lind." The standfirst also keeps "men skulle avsätta mer tid för förberedelser". But the new headline, "Gemensam ärendebild hjälper, säger Elm Quays arbetsledare", lifts the appraisal to the top of the page without its qualification. The appraisal is kept, but the headline weakens it. **Partly met.**
- **Numbers: preserved.** "31 ärenden under åtta veckor … två arbetsdagar … tre", "4 december 2025", "två hus", "sex medarbetare". The caveat about workload in the body is also preserved. It is removed from the subheading.
- **Supplier publication disclosure: preserved.** "Kundcaset publiceras av leverantören Svale."
- **Checklist link carrying the call to action: preserved.** "[Svales checklista för införandet](https://example.invalid/svale/checklist)"

**Must not do:**

- **Require a quote count: not done.**
- **Add an extra sales block: not done.** No block was added. The new headline does, however, move the text towards supplier-favourable framing.

**Reject:**

- **A finding against a limit the text meets** (the 36-character headline, the 40-word standfirst, the 36–39-character subheadings): the run made no finding on length. **Mistake not made.** Its rewrites probably break the headline and subheading limits, but that is a matter for preservation, not a rejected finding.
- **A finding resting on the one-sentence paragraph, the four-sentence paragraph or one section's paragraph count:** none. **Not made.**
- **A finding against the Swedish `Text:` byline form:** none. The byline is unchanged. **Not made.**

## 4. R1

**Fail.** The frozen expectation says the text conforms to the anatomy. R1 says "Clean texts may not be rewritten to satisfy taste." The run rewrote a working headline because it did not state "kundens nytta eller resultat som genren kräver". It also rewrote a working subheading so that it shows the result instead of the caveat. Neither was a visible defect. The combined effect changes what the text claims at the level a reader skims. The headline now reads "Gemensam ärendebild hjälper, säger Elm Quays arbetsledare", an unqualified benefit claim in a case study published by the supplier. The subheading, "Tilldelningen tog i median två arbetsdagar under försöket", no longer carries the text's own caveat that the periods are not comparable. The run avoided every finding the expectation names for rejection, and it kept the body's numbers, agency, disclosure and link. Those do not outweigh the rewriting of a clean text.
