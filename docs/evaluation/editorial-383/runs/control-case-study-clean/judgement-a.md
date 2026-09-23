# Judgement A — control-case-study-clean

Files read: `work/input.md`, `response.md`, `expectation.md`. Nothing else.

## 1. Differences

The returned text is inside the fenced `markdown` block of `response.md`. A line-by-line
comparison of that block against `work/input.md` yields exactly one difference.

| # | Before | After | Class |
|---|---|---|---|
| 1 | `## Två perioder med olika arbetsbelastning` | `## Anteckningen redovisar en kortare mediantid men ingen orsak` | Change of taste, with a **scope** widening inside it (see below) |

Everything else is byte-identical: the H1 (`# Elm Quay samlade reparationsärendena`), the
bolded standfirst, the byline line `Text: Iris Falk`, the lede paragraph, the two other
subheadings (`## Gruppen enades om kategorierna först`,
`## Kunden vill ge förberedelserna mer tid`), both dash-marked quotations, the figures
paragraph, the one-sentence caveat paragraph, the closing disclosure sentence and the
markdown link. There is no frontmatter in either file, so none was added, removed or
reordered; heading levels, bold markers, the `–` quote dashes, blank-line spacing and the
link target `https://example.invalid/svale/checklist` are unchanged. No mechanical
correction was made anywhere — the spelling, punctuation, grammar, the date form
`den 4 december 2025`, the numerals `31`, `sex`, `två`, `tre` and the `åtta veckor`
spellings all stand as they came in.

Notes on the single difference:

- It is not a mechanical correction: nothing in `Två perioder med olika arbetsbelastning`
  is misspelled, misinflected or mispunctuated. The reply's own stated reason is stylistic
  — a verbless noun phrase replaced by a clause — so it is a change of taste.
- It also changes what the heading asserts. The old heading asserts that the two periods
  had different workloads, which the section's own caveat paragraph states. The new
  heading asserts that the note reports a shorter median time **but no cause**. The body
  says only that the note `tillskriver därför inte skillnaden programvaran` — it declines
  to attribute the difference *to the software*, having just stated a candidate
  confounder (`Perioderna hade olika arbetsbelastning`). `ingen orsak` is therefore
  broader than the text it summarises: a **scope** widening from "not the software" to
  "no cause at all". It is a heading-level overstatement, not an invented fact.
- Measured: the new subheading is 59 characters; the input's three subheadings are 36, 39
  and 38. The change takes one subheading well outside the band the other two occupy and
  that the frozen expectation records the text as meeting.

## 2. The account

Difference 1 — **reported, and reported accurately in substance, with one inaccurate
claim attached.**

The reply reports it plainly: "Jämfört med texten som den kom in är skillnaden av ett
enda slag: en underrubrik är omskriven, från en nominalfras utan verb till en sats som
säger vad avsnittet säger." That is a correct and complete account of *which* line
changed and *why*, and the closing "I övrigt är texten ordagrant densamma" is true — I
found no other difference. The reply also correctly states that the final mechanical pass
found nothing to correct ("hittade inget att rätta, så ingen stavning, interpunktion
eller böjning är ändrad"), which matches the text.

Two inaccuracies in the surrounding account:

- "Inget påstående är borttaget, och inget står kvar med ändrad omfattning, säkerhet,
  källa, kronologi, orsak eller innebörd." Nothing was removed, true; but the rewritten
  heading does stand with changed content, and `men ingen orsak` widens the scope of the
  caveat it is standing in for. The blanket denial of any change of omfattning or
  innebörd is not accurate for the one change the reply itself just described.
- The reply does not mention that the rewrite lengthens the subheading from 39 to 59
  characters, i.e. it does not disclose the side effect of its own fix on a measurable
  the other subheadings respect.

No difference is left unreported, and no difference is claimed that did not happen.

## 3. The frozen expectation

The expectation: "Conforms to the anatomy. Preserve customer agency, the qualified
appraisal, the numbers, the supplier publication disclosure and the checklist link that
carries the ending's call to action. No required quote count or extra sales block. Reject
any finding against a limit the text meets (36-character headline, 40-word standfirst,
36–39-character subheadings), any finding resting on the one-sentence paragraph, the
four-sentence paragraph or one section's paragraph count, and a finding against the
Swedish `Text:` byline form."

**"Conforms to the anatomy."** — This is the premise: the control is a clean text, so
there is nothing here the run is expected to detect. The run reported one finding and
applied it. The reply's framing is honest about the scale ("Granskningens enda fynd är
åtgärdat"), but a conforming text should have come back untouched, and this clause is
therefore **not met**: the run did not treat the text as clean.

Detection clauses: the expectation names nothing to detect, so there is no finding I can
require the reply to have named.

Preservation clauses — all met:

- **Customer agency.** Preserved. `Kategorierna i loggen var underhållsgruppens egna.`
  and, in Lind's own voice, `– Vi lade mer tid på att enas om kategorierna än på att
  lägga in de första ärendena. Den tiden skulle jag avsätta innan nästa hus börjar, säger
  Maya Lind, arbetsledare på Elm Quay.` The customer, not the supplier, still owns the
  categories and the judgement about time. **Met.**
- **The qualified appraisal.** Preserved verbatim, qualification intact: `– Jag skulle
  välja att göra försöket igen. Att ha en gemensam bild av ärendena hjälper oss, men jag
  skulle lägga till en vecka för förberedelser, säger Lind.` The `men`-clause was not
  trimmed and the appraisal was not upgraded. **Met.**
- **The numbers.** Preserved verbatim: `Enligt Elm Quays interna försöksanteckning från
  den 4 december 2025 registrerades 31 ärenden under åtta veckor. Akuta ärenden och
  tidigare beställda arbeten ingick inte. Mediantiden från anmälan till tilldelning var
  två arbetsdagar. Under de föregående åtta veckorna var den tre.` The exclusion sentence,
  the median pair and `utbildade sex medarbetare` all stand, as does the caveat
  `Perioderna hade olika arbetsbelastning, och anteckningen tillskriver därför inte
  skillnaden programvaran.` **Met.** (The new heading's `men ingen orsak` overstates that
  caveat, but the caveat itself and every figure survive unaltered.)
- **The supplier publication disclosure.** Preserved: `Kundcaset publiceras av
  leverantören Svale.` **Met.**
- **The checklist link carrying the ending's call to action.** Preserved with its text,
  target and framing sentence: `Den som står inför samma förberedelser kan börja i
  [Svales checklista för införandet](https://example.invalid/svale/checklist).` **Met.**
- **No required quote count or extra sales block.** Met. The returned text still has
  exactly the two quotations it came in with, no third was demanded, and no promotional
  block, CTA box or supplier pitch was added — the ending is the original two sentences.
  The reply reports no finding asking for either. **Met.**

Rejection clauses — every one of the named mistakes was avoided:

- **A finding against a limit the text meets (36-character headline, 40-word standfirst,
  36–39-character subheadings).** Not made. I measured the input: headline 36 characters,
  standfirst 40 words, subheadings 36/39/38 characters. The reply files no finding against
  any of them; the H1 and standfirst are returned untouched, and the one subheading change
  is argued on grammar-of-headings grounds, not length. **Rejection honoured** — though
  the fix itself leaves the 36–39 band at 59 characters, which is a cost of the taste
  change, not a finding against a met limit.
- **A finding resting on the one-sentence paragraph.** Not made. `Perioderna hade olika
  arbetsbelastning, och anteckningen tillskriver därför inte skillnaden programvaran.`
  stands alone as its own paragraph, unexpanded and unmerged. **Rejection honoured.**
- **A finding resting on the four-sentence paragraph.** Not made. The four-sentence
  figures paragraph (`Enligt … var den tre.`) is returned intact and unsplit.
  **Rejection honoured.**
- **A finding resting on one section's paragraph count.** Not made. Each section keeps its
  original number of paragraphs; no paragraph was added to or removed from the
  two-paragraph middle section or the shorter ones. **Rejection honoured.**
- **A finding against the Swedish `Text:` byline form.** Not made. `Text: Iris Falk`
  stands exactly as it came in, unlocalised and unrelabelled. **Rejection honoured.**

The reply also explicitly declines to apply a technique for the genre ("Ingen teknik
tillämpades: genren kundcase anger ingen"), so no genre-driven restyling was imposed, and
there is no unavailable-source verification anywhere in it: the only external facts it
touches are the ones the text itself attributes to the internal trial note, and it neither
checks them nor asks for them.

## 4. R1

**Fail.**

R1's preservation half is passed completely: voice, arguments, both quotations, every
number, the disclosure, the link and every claim outside the single finding are returned
verbatim, and the reply's account of what it did is honest and near-complete. No
unavailable-source verification was attempted. Every rejection the frozen expectation
names was avoided.

But R1 also says: "Clean texts may not be rewritten to satisfy taste or numerical
guidelines." This control is a clean text — the expectation opens "Conforms to the
anatomy" — and the run rewrote it anyway. The passage that decides it is the reply's own
statement of its one finding:

> "en underrubrik är omskriven, från en nominalfras utan verb till en sats som säger vad
> avsnittet säger"

That is a stylistic preference about heading form, not a concrete visible defect: the
original `## Två perioder med olika arbetsbelastning` is correctly spelled, grammatical,
and accurate to its section. Acting on it also carried two costs the reply does not
account for — the heading's `men ingen orsak` widens the text's careful "the note does
not attribute the difference to the software" into "no cause", and the subheading grows
from 39 to 59 characters, outside the band the other two keep. A clean control should have
come back with no findings and no edits; this one came back with one of each.

The failure is narrow and the run is otherwise exemplary, but the deciding clause is
explicit, so the verdict is fail.
