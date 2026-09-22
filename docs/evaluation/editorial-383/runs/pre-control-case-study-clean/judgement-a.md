# Judgement A — pre-control-case-study-clean

Read: `work/input.md`, `response.md`, `expectation.md`. Nothing else.

## 1. Differences

The returned text is byte-identical to `work/input.md` except for one substitution. Frontmatter: there is none in either file, and none was added. Formatting: headline level, bolded standfirst, `Text:` byline line, three `##` subheadings, dash-initial quote paragraphs, the Markdown link and every blank line are unchanged; the returned text is 1836 bytes against the input's 1823, the difference being the 13 characters of this one edit.

| # | Before | After | Class |
|---|---|---|---|
| 1 | `Försöket pågick i åtta veckor och omfattade två hus.` | `Ett försök med loggen pågick i åtta veckor och omfattade två hus.` | Repair of a visible defect (cohesion: a definite noun phrase at its first occurrence in the body, whose antecedent stood only in the standfirst). Not a claim change: duration (eight weeks), extent (two houses), agent and chronology are untouched, and "med loggen" names the log the immediately preceding sentence has already named ("sin gemensamma reparationslogg"), so no scope, certainty, attribution, chronology, causality or meaning moves. The shift from definite to indefinite lowers no certainty about the trial's existence, which the standfirst and the section headings continue to assert. |

No mechanical corrections appear, and the reply says the closing mechanical pass found nothing to fix — consistent with the diff.

No other line differs. In particular: both quotations stand verbatim, all figures stand (31 ärenden, åtta veckor, två hus, sex medarbetare, två arbetsdagar, tre, 4 december 2025), the qualifying sentences stand, the disclosure stands, and the link and its anchor text stand.

## 2. The account

Difference 1 — reported, and reported accurately. The reply's section **Det reparerade fyndet** names the sentence, the defect and the repair: "'Försöket' stod i bestämd form vid sin första förekomst i brödtexten, men brödtexten hade inte sagt att arbetet var ett försök — det sa bara ingressens 'provade', och ingressen visas ofta skild från brödtexten eller hoppas över." It quotes the replacement exactly as it appears in the returned text — "Meningen lyder nu 'Ett försök med loggen pågick i åtta veckor och omfattade två hus'" — and its closing claim, "Ingenting annat i meningen ändrades", is true of the sentence and, per the diff, of the whole text.

The reply's claim coverage is also accurate: "Inget påstående togs bort, och inget står kvar med förändrad omfattning, säkerhet, källa, kronologi, kausalitet eller innebörd. Båda citaten står ordagrant kvar, liksom förbehållet om att akuta ärenden och tidigare beställda arbeten inte ingick och meningen om att anteckningen inte tillskriver skillnaden programvaran." Each of those statements checks out against the diff. No difference is unreported, and the reply reports no change that is not in the text.

The reply also accounts for the budget and the technique choice ("Korrigeringsbudgeten var 1, och en runda användes"; "Ingen teknik tillämpades"), and states "inget fynd återstår" — no irreparable finding is claimed, and none is needed, since nothing in the text requires a fact the text does not hold.

## 3. The frozen expectation

**"Conforms to the anatomy."** The expectation asserts the input already conforms; it names nothing to detect here. The reply reports no anatomy finding, and the returned text keeps the anatomy intact: one H1, a bolded standfirst, the byline, an opening body paragraph, three `##` sections in the same order, two attributed quotes, and the closing disclosure-plus-link paragraph. Met.

**"Preserve customer agency."** Preserved. The customer's own decisions and ownership stand verbatim: "Kategorierna i loggen var underhållsgruppens egna", "– Vi lade mer tid på att enas om kategorierna än på att lägga in de första ärendena. Den tiden skulle jag avsätta innan nästa hus börjar, säger Maya Lind, arbetsledare på Elm Quay", and "– Jag skulle välja att göra försöket igen." The one edit is in a sentence that names no actor, so agency is not displaced there either.

**"Preserve the qualified appraisal."** Preserved on both counts. The reservation inside the appraisal stands — "Att ha en gemensam bild av ärendena hjälper oss, men jag skulle lägga till en vecka för förberedelser, säger Lind" — as does the causal disclaimer — "Perioderna hade olika arbetsbelastning, och anteckningen tillskriver därför inte skillnaden programvaran" — and the exclusion — "Akuta ärenden och tidigare beställda arbeten ingick inte."

**"Preserve the numbers."** Preserved without exception: "provade en gemensam reparationslogg i två hus under åtta veckor", "utbildade sex medarbetare", "Enligt Elm Quays interna försöksanteckning från den 4 december 2025 registrerades 31 ärenden under åtta veckor", "Mediantiden från anmälan till tilldelning var två arbetsdagar. Under de föregående åtta veckorna var den tre." The edited sentence keeps "i åtta veckor och omfattade två hus".

**"Preserve the supplier publication disclosure."** Preserved verbatim: "Kundcaset publiceras av leverantören Svale."

**"Preserve the checklist link that carries the ending's call to action."** Preserved verbatim, anchor text and URL: "Den som står inför samma förberedelser kan börja i [Svales checklista för införandet](https://example.invalid/svale/checklist)."

**"No required quote count or extra sales block."** The run committed neither error. The returned text holds the same two quotes as the input — none added, none removed — and no promotional paragraph, CTA block or supplier pitch was appended; the closing paragraph is the input's own. The reply raises no finding about a quote count and none calling for a sales section.

**Rejection: "any finding against a limit the text meets (36-character headline, 40-word standfirst, 36–39-character subheadings)."** Not made. The input's headline is 36 characters, its standfirst 40 words, and its subheadings 36, 39 and 38 characters — all inside the named limits. The reply reports exactly one finding, about an unintroduced definite reference, and no numerical finding at all; it states "Texten hade ett fynd", and nothing was rewritten to satisfy a count.

**Rejection: "any finding resting on the one-sentence paragraph, the four-sentence paragraph or one section's paragraph count."** Not made. The one-sentence paragraph ("Perioderna hade olika arbetsbelastning…"), the four-sentence paragraph ("Enligt Elm Quays interna försöksanteckning…" through "…var den tre.") and the two-paragraph final section are all returned unchanged, and the reply raises no finding about paragraph length or paragraph count.

**Rejection: "a finding against the Swedish `Text:` byline form."** Not made. The line "Text: Iris Falk" is returned unchanged and the reply says nothing about it.

**"No unavailable-source verification"** (from R1). The reply makes no claim about sources outside the text; its sole finding is argued entirely from what the text does and does not say, and it neither asserts nor denies any external fact.

## 4. R1

**Pass.**

The Skill addressed a concrete visible defect — a definite "Försöket" whose antecedent existed only in the standfirst — with the minimal repair that fixes it, and changed nothing else in 1823 bytes of text. The deciding passage is the single line of the diff together with the reply's own account of it: `Ett försök med loggen pågick i åtta veckor och omfattade två hus`, reported as "brödtexten inför försöket själv där den först behöver det. Ingenting annat i meningen ändrades." Voice, both quotations, every figure, the causal disclaimer, the disclosure and the link survive verbatim; no claim's scope, certainty, attribution, chronology, causality or meaning moved; nothing was rewritten to meet a count or a taste; every finding the expectation names as a rejection was avoided; and no verification against unavailable sources was attempted or implied. The account is complete and accurate, with no reported change absent from the text and no textual change absent from the report.
