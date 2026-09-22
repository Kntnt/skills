# Judgement B — pre-control-case-study-clean

Read: `work/input.md`, `response.md`, `expectation.md`. The returned text is the fenced
`markdown` block in `response.md`; I extracted it to `returned-b.txt` in this run directory
and diffed it against the input line by line.

## 1. Differences

The whole diff is one substitution inside the third body sentence of the opening paragraph.
Everything else — frontmatter-free title line, the bolded standfirst, the `Text:` byline, all
three subheadings, both dialogue-dash quotations, every number and date, the qualifier
sentence, the disclosure sentence, the checklist link, paragraph breaks, blank lines and
trailing newline — is byte-identical.

| # | Before | After | Class |
|---|---|---|---|
| 1 | `Försöket pågick i åtta veckor och omfattade två hus.` | `Ett försök med loggen pågick i åtta veckor och omfattade två hus.` | Repair of a visible defect (definite noun phrase at its first occurrence in the body text, with no antecedent in the body text; the following sentence's `det` hangs off the same referent). Not a mechanical correction, not taste. |

On difference 1 and the claim classes: the sentence's asserted content is unchanged. Duration
(`åtta veckor`), extent (`två hus`) and tense stand as they were, so chronology and scope are
untouched; nothing was hedged or firmed, so certainty is untouched; no source was added or
moved, so attribution is untouched; no cause is asserted either way, so causality is untouched.
The only shift is referential form — definite to indefinite — and the added `med loggen` pins
the referent to the log the first sentence has just named, so the trial the standfirst describes
and the trial the body now introduces remain one and the same event. I therefore do not count
this as a change to what the claim says under any of the six heads. It is a small change, and it
is defensible on a real Swedish convention: the body text of a case study is expected to stand
without the standfirst, which is often displayed apart from it or skipped, and the input's body
text used `Försöket` before introducing any trial. Note also that the standfirst itself contains
`försöket` in definite form after `provade`, so the defect is specific to body-text
independence, which is how the reply frames it.

No difference falls in the mechanical class (spelling, punctuation, grammar, or a locale form of
dates, numbers or currency), so the separate proofreading pass has nothing recorded against it
here — consistent with the reply's claim that the closing mechanical pass found nothing.

## 2. The account

Difference 1 — reported, and reported accurately. The reply carries a dedicated section, **Det
reparerade fyndet**, which names the finding, the mechanism and the replacement:

> "Försöket" stod i bestämd form vid sin första förekomst i brödtexten, men brödtexten hade inte
> sagt att arbetet var ett försök — det sa bara ingressens "provade", och ingressen visas ofta
> skild från brödtexten eller hoppas över.

and

> Meningen lyder nu "Ett försök med loggen pågick i åtta veckor och omfattade två hus", så
> brödtexten inför försöket själv där den först behöver det. Ingenting annat i meningen ändrades.

The quoted after-text matches the returned text exactly. The reply's scope claims are also
accurate against the diff: "Texten hade ett fynd, det är reparerat, och inget fynd återstår"
matches one and only one change; "Den avslutande mekaniska genomgången hittade inget att rätta"
matches zero mechanical differences; "Inget påstående togs bort, och inget står kvar med
förändrad omfattning, säkerhet, källa, kronologi, kausalitet eller innebörd" matches my
classification above; and "Båda citaten står ordagrant kvar, liksom förbehållet ... och meningen
om att anteckningen inte tillskriver skillnaden programvaran" is verifiable in the returned text.
No difference in the text is unreported, and the reply reports no change that did not happen.

## 3. The frozen expectation

**"Conforms to the anatomy."** Met, in the sense that matters here: the reply files no anatomy
finding at all. It reports exactly one finding, and that finding is referential, not anatomical
— it does not allege a missing, misplaced or oversized part. The returned text keeps the same
parts in the same order: title, bolded standfirst, byline, opening paragraph, three
subheaded sections, closing disclosure and link.

**"Preserve customer agency."** Preserved. The customer's own decision and her own reservation
stand verbatim in her own voice:

> – Jag skulle välja att göra försöket igen. Att ha en gemensam bild av ärendena hjälper oss, men
> jag skulle lägga till en vecka för förberedelser, säger Lind.

and, in the first quotation, "Den tiden skulle jag avsätta innan nästa hus börjar". The standfirst
likewise still reads "vill göra om försöket, men skulle avsätta mer tid för förberedelser".

**"Preserve the qualified appraisal."** Preserved, word for word:

> Perioderna hade olika arbetsbelastning, och anteckningen tillskriver därför inte skillnaden
> programvaran.

The scope qualifier on the count survives too: "Akuta ärenden och tidigare beställda arbeten
ingick inte."

**"Preserve the numbers."** All preserved and unaltered in value and form: `två hus`, `åtta
veckor` (both occurrences), `sex medarbetare`, `den 4 december 2025`, `31 ärenden`, `två
arbetsdagar`, `tre`, and `en vecka`. Quoting the sentence that carries most of them:

> Enligt Elm Quays interna försöksanteckning från den 4 december 2025 registrerades 31 ärenden
> under åtta veckor. ... Mediantiden från anmälan till tilldelning var två arbetsdagar. Under de
> föregående åtta veckorna var den tre.

No number was rounded, converted, re-localised or restated.

**"Preserve the supplier publication disclosure."** Preserved, verbatim and in place:

> Kundcaset publiceras av leverantören Svale.

**"Preserve the checklist link that carries the ending's call to action."** Preserved, with its
anchor text, its target and the sentence that turns it into a call to action:

> Den som står inför samma förberedelser kan börja i [Svales checklista för
> införandet](https://example.invalid/svale/checklist).

**"No required quote count."** Not violated. The reply files no finding about the number of
quotations, and the returned text still holds exactly the two the input held.

**"No extra sales block."** Not violated. Nothing was added to the ending; the closing section is
the input's two sentences unchanged, and no promotional paragraph, box, CTA block or
supplier pitch appears anywhere in the returned text.

**Rejection — "any finding against a limit the text meets (36-character headline, 40-word
standfirst, 36–39-character subheadings)."** Mistake not made. The reply files no length or count
finding of any kind, and none of these elements was touched. For the record, the text does meet
them: the headline "Elm Quay samlade reparationsärendena" is 36 characters, the standfirst is 40
words, and the subheadings are 36, 39 and 38 characters.

**Rejection — "any finding resting on the one-sentence paragraph, the four-sentence paragraph or
one section's paragraph count."** Mistake not made. The one-sentence paragraph ("Perioderna hade
olika arbetsbelastning …") stands untouched as its own paragraph; the four-sentence paragraph in
"Två perioder med olika arbetsbelastning" stands untouched with all four sentences; no section
gained or lost a paragraph. The reply files no finding on paragraph length or paragraph count.

**Rejection — "a finding against the Swedish `Text:` byline form."** Mistake not made. The line
`Text: Iris Falk` is returned exactly as given, and the reply says nothing about the byline.

**"No unavailable-source verification."** Not violated. The reply nowhere claims to have checked
the trial note, the supplier, the median times or the link against anything outside the text. Its
only verification claims are before/after comparisons within the text it was given ("Båda citaten
står ordagrant kvar"), which is exactly what it is entitled to assert. It does not speculate
about what a source would say, and it does not treat the absence of a source as a finding.

## 4. R1

**Pass.**

The Skill addressed one concrete visible defect and left everything else alone. The deciding
passage is the single difference and the reply's account of it:

> "Försöket" stod i bestämd form vid sin första förekomst i brödtexten, men brödtexten hade inte
> sagt att arbetet var ett försök

— a defect visible in the supplied text alone, repaired in place with the minimum edit ("Ett
försök med loggen pågick i åtta veckor och omfattade två hus") and nothing else disturbed. Set
against the criterion's failure modes: no working voice was flattened (both quotations and the
byline are verbatim); no argument, quotation or claim outside the finding moved; no clean passage
was rewritten to satisfy taste or a numerical guideline — not one length, count or paragraph
finding was filed, and each of the three named rejections was avoided; no claim changed scope,
certainty, attribution, chronology, causality or meaning; nothing was verified against an
unavailable source; and the account is complete in both directions, reporting the one change that
happened and no change that did not. The one edit is small and marginal in value, but it rests on
a defect the text itself exhibits rather than on preference, and it costs the text nothing — so it
does not read as a clean text rewritten to taste.
