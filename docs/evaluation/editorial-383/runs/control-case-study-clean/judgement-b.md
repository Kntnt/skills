# Judgement b — control-case-study-clean

Judged: `work/input.md` against the returned text in `response.md`, on criterion R1, against the frozen expectation in `expectation.md`.

## 1. Differences

A line-by-line comparison of the input against the fenced text the reply returns gives one difference in the text itself, and one difference of presentation.

| Before | After | Class |
| --- | --- | --- |
| `## Två perioder med olika arbetsbelastning` (39 characters) | `## Anteckningen redovisar en kortare mediantid men ingen orsak` (59 characters) | **Change of taste**, on a subheading the frozen expectation records as meeting the limit. Secondarily a change to what the heading itself says — **meaning**: the old heading characterises the section's subject (two periods of unequal workload); the new one asserts what the internal note reports and does not report (a shorter median, no cause). The asserted content is supported by the body paragraphs, so nothing unsupported enters the text, but the heading no longer says the same thing. |
| Text delivered bare | Text delivered inside a ```` ```markdown ```` fence | Presentation of the reply, not a change to the document. No frontmatter exists in the input and none was added. |

Everything else is byte-identical: the title, the bold standfirst, the `Text: Iris Falk` byline, the opening paragraph, the two block quotations, every number and date (`31 ärenden`, `åtta veckor`, `två hus`, `sex medarbetare`, `två arbetsdagar`, `tre`, `den 4 december 2025`), the non-attribution sentence, the supplier disclosure and the checklist link with its URL. No spelling, punctuation, grammar or locale correction was made — so nothing in this run falls to the separate proofreading pass, and nothing here is excluded from R1 on that ground.

## 2. The account

- **The subheading rewrite.** Reported, and reported accurately as to fact: "en underrubrik är omskriven, från en nominalfras utan verb till en sats som säger vad avsnittet säger." The characterisation of the before-state (a verbless nominal phrase) and the after-state (a clause) is correct. The reply also claims "Inget påstående är borttaget, och inget står kvar med ändrad omfattning, säkerhet, källa, kronologi, orsak eller innebörd" — accurate for the body, but incomplete for the heading itself, whose propositional content did change (see class above). The reply does not mention that the rewritten heading is 59 characters against the 39 it replaced.
- **No mechanical corrections.** Reported accurately: "Den avslutande mekaniska genomgången hittade inget att rätta, så ingen stavning, interpunktion eller böjning är ändrad." True.
- **"I övrigt är texten ordagrant densamma."** True; verified by comparison.
- **"Granskningens enda fynd är åtgärdat"** — the reply declares one finding and no outstanding findings. That count matches the single difference. The reply does not state the finding as a defect claim (what rule the old heading broke); it states only the change it made.

The account is honest and complete as a change log. It does not misreport anything. Its one gap is that it does not disclose the heading's length change or that the heading's own claim changed.

## 3. The frozen expectation

The expectation names nothing to detect. It is a clean control: one clause of conformance, five things to preserve, and a set of findings to reject.

**"Conforms to the anatomy."** No detection is owed. The reply nonetheless produced a finding against the text as it came in — it rewrote a subheading on the ground that it was "en nominalfras utan verb". Measured against an expectation that states the text conforms, that is a finding against a conforming text. Not met.

**"Preserve customer agency"** — preserved verbatim: "– Jag skulle välja att göra försöket igen. Att ha en gemensam bild av ärendena hjälper oss, men jag skulle lägga till en vecka för förberedelser, säger Lind." The decision stays the customer's throughout; so does the earlier "Kategorierna i loggen var underhållsgruppens egna." Met.

**"the qualified appraisal"** — preserved. The qualification survives in both quotations ("men skulle avsätta mer tid för förberedelser" in the standfirst; "men jag skulle lägga till en vecka för förberedelser" in the closing quote), as does the non-attribution sentence "Perioderna hade olika arbetsbelastning, och anteckningen tillskriver därför inte skillnaden programvaran." Met. Note that the rewritten heading, "…men ingen orsak", restates that same qualification rather than undercutting it.

**"the numbers"** — preserved, every one, unchanged in value and in form: "registrerades 31 ärenden under åtta veckor", "Mediantiden från anmälan till tilldelning var två arbetsdagar. Under de föregående åtta veckorna var den tre", "utbildade sex medarbetare", "den 4 december 2025", "i två hus". The scope limit "Akuta ärenden och tidigare beställda arbeten ingick inte." is also intact. Met.

**"the supplier publication disclosure"** — preserved verbatim: "Kundcaset publiceras av leverantören Svale." Met.

**"the checklist link that carries the ending's call to action"** — preserved verbatim, text and target: "Den som står inför samma förberedelser kan börja i [Svales checklista för införandet](https://example.invalid/svale/checklist)." Met.

**"No required quote count or extra sales block."** No quote was added or removed; the two quotations are the two that came in. No sales block, boilerplate, CTA box or supplier pitch was appended. The reply's closing statement of no other change holds. Met.

**"Reject any finding against a limit the text meets (36-character headline, 40-word standfirst, 36–39-character subheadings)."** The headline (36 characters) and standfirst (40 words) are untouched and no finding was raised against either. Met for those two. For the subheadings it is **not** met: the run's only finding fell on `## Två perioder med olika arbetsbelastning`, one of the three subheadings the expectation certifies as within the 36–39-character band, and replaced it with a 59-character heading — outside the band the expectation records. The finding was not framed as a length finding, so this is not literally a finding *against the limit*; but it is a finding against a subheading the expectation declares compliant, and its remedy leaves that subheading twenty characters past the recorded band.

**"any finding resting on the one-sentence paragraph"** — the one-sentence paragraphs ("Perioderna hade olika arbetsbelastning…" and the two quotation paragraphs) drew no finding and are unchanged. Not made.

**"the four-sentence paragraph"** — "Enligt Elm Quays interna försöksanteckning… var den tre." is returned with all four sentences, unsplit and unmerged. No finding rests on it. Not made.

**"or one section's paragraph count"** — no section gained or lost a paragraph; every section has the same number of paragraphs it came in with. No finding rests on a paragraph count. Not made.

**"and a finding against the Swedish `Text:` byline form."** The byline is returned exactly as `Text: Iris Falk`. No finding was raised against it, and it was not converted to `Av`, `By`, italics or a frontmatter field. Not made.

**No unavailable-source verification.** The run raised nothing requiring the trial note, the supplier or any external document to be checked, and asserted nothing about them. The reply's only claim about sources is that the note itself does not attribute the difference — which is what the text says. Met.

So: five of five preservation clauses met; the three named paragraph-shape rejections and the byline rejection all avoided; the headline and standfirst limits respected; no unavailable-source verification. The conformance clause and the subheading half of the limits clause are not met.

## 4. R1

**Fail.**

R1's last sentence is the one that decides it: "Clean texts may not be rewritten to satisfy taste or numerical guidelines." This control is a clean text — the frozen expectation opens "Conforms to the anatomy." and names nothing to detect — and the run rewrote it anyway. The deciding passage is the reply's own account of what it did:

> "Jämfört med texten som den kom in är skillnaden av ett enda slag: en underrubrik är omskriven, från en nominalfras utan verb till en sats som säger vad avsnittet säger."

That is a rewrite justified by a preference about heading form, applied to a heading with no visible defect: `## Två perioder med olika arbetsbelastning` is accurate to its section, which reports two eight-week periods of unequal workload and their two median figures. Nothing in the text was wrong before the change, and the change is the whole of the run's output.

Two things make the fail firmer rather than softer. First, the remedy takes the heading from 39 to 59 characters, past the 36–39-character band the expectation records for this text's subheadings — the run's taste change leaves the document further from the anatomy's subheading measure than it found it, and the reply never mentions the length at all. Second, the rewritten heading changes what the heading asserts: it stops naming the section's subject and starts making a claim about what the internal note reports. The claim is supported by the body, so nothing false enters the text, and the reply's "Inget påstående är borttaget" is true — but a clean control is precisely where a heading's proposition should not have moved.

What keeps the fail narrow is everything R1's first half asks about: voice, arguments, quotations and claims outside findings are preserved exactly. Both quotations, all numbers, the scope exclusion, the non-attribution sentence, the supplier disclosure, the checklist link and the `Text:` byline come back verbatim; no quote was added to hit a count, no sales block appended, no source verified that the run could not see, and none of the four named rejections was made. The run fails on one axis only — it did not leave a clean text alone.
