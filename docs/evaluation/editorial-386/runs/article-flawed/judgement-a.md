# Judgement A — run `article-flawed`

## Changes

1. Headline `Givarna räddar skolan från en katastrof` → `Mätförsöket i Björkskolan saknar operativ temperatur` — change to what a claim says: an unsupported rescue-and-catastrophe claim replaced by an absence the body carries (`Operativ temperatur saknas`).
2. Standfirst `Givarna registrerade temperaturer under 20 grader i sex klassrum. Givarna registrerade temperaturer under 20 grader i sex klassrum.` → `Ett mätförsök i Björkskolan visade temperaturer under fastighetskontorets egen arbetsgräns på 20 grader. Men flera uppgifter saknas i underlaget. Här är vad försöket fångade, vad det inte fångade och vad driftteknikern rekommenderar innan styrningen ändras.` — repair of a visible defect (the duplicated sentence), carrying two new summarising claims that the body supports.
3. Lead opening `Givarna registrerade temperaturer under 20 grader i sex klassrum.` → `I rapporten *Mätförsök i Björkskolan* från den 12 mars 2026 redovisar fastighetskontoret mätningar med givare i sex klassrum.` — repair of a visible defect (the definite `Givarna` now introduced) **and** a change to what a claim says: `i sex klassrum` moves from the sub-20 readings to the measurements as a whole.
4. `Katastrofen lurade bakom varje hörn.` → deleted — change to what a claim says (invented drama removed).
5. `Fastighetskontorets rapport *Mätförsök i Björkskolan* från den 12 mars 2026 anger att` → `Rapporten anger att` — mechanical: the source moved into the preceding sentence, attribution unchanged.
6. `och att försöket varade fyra veckor, medan två givare stod vid ytterväggar och fyra vid innerväggar, utan att placeringens effekt jämfördes experimentellt.` → split; `Rapporten anger också att två givare stod vid ytterväggar och fyra vid innerväggar, utan att placeringens effekt jämfördes experimentellt.` becomes its own section — repair of a visible defect.
7. New H2 `## Placeringen redovisas, men inte dess effekt` — repair of a visible defect (no section existed).
8. New H2 `## Underlaget har flera luckor` — repair of a visible defect.
9. Paragraph break inserted before `Det saknas mätningar av luftdrag…` — repair of a visible defect.
10. `, men ändå är det helt säkert att givarna har gjort eleverna friskare, trots att ingen effekt på hälsan har undersökts` → `. Ingen effekt på hälsan har undersökts.` — change to what a claim says: a certainty and a causal claim removed, the limit kept at full strength as its own sentence.
11. New H2 `## Elin Rask vill se användningstiderna först` — repair of a visible defect.
12. `Driftteknikern Elin Rask rekommenderar …, och nästa försök är tänkt …` → two sentences — repair of a visible defect (rhythm), wording otherwise intact.
13. `Det är viktigt att notera att detta är mycket viktigt för alla som tycker att temperatur är viktigt.` → deleted — removal of a sentence carrying no claim.
14. `Kontakta oss för att rädda framtiden.` → deleted — change to what a claim says (a sales call unconnected to the explanation).
15. `Givarna registrerade temperaturer under 20 grader.` added as the lead's closing sentence — the surviving half of the original opening; it now restates the preceding sentence.

Nothing measured was deleted. Every figure and limiting clause in the input is present in `delivered.md`: `14 av 120 lektionspass`, `kontorets egen arbetsgräns på 20 grader`, `vilket inte är en lagregel`, `fyra veckor`, `två givare … fyra vid innerväggar`, `utan att placeringens effekt jämfördes experimentellt`, the whole operative-temperature sentence, the missing-measurements sentence, `den 12 mars 2026`, `Elin Rask`, `i november`, `fast finansieringen inte är beslutad`.

## Headings

**Input**

- H1 `Givarna räddar skolan från en katastrof` — **statement**, **overclaim** (the text states that no health effect was investigated and describes no catastrophe; `räddar` and `katastrof` are carried nowhere in it).
- No level-2 subheadings. `anatomy-input.json` reports `"sections": []` and the failure `{"part": "sections", "measured": "absent"}`.

**Returned text**

- H1 `Mätförsöket i Björkskolan saknar operativ temperatur` — **statement**. Not an echo: it shares the noun phrase `mätförsök i Björkskolan` with the standfirst, but the standfirst nowhere says that operative temperature is missing, so the headline carries its own information. Not an overclaim: the body states `Operativ temperatur saknas`.
- H2 `Placeringen redovisas, men inte dess effekt` — **statement**. Not an echo: the sentence beneath carries the numbers (`två givare … fyra vid innerväggar`) that the heading does not, so the heading is the more abstract of the two.
- H2 `Underlaget har flera luckor` — **statement**. Not an echo of its first sentence (`Operativ temperatur saknas, trots att…`), which shares no wording with it.
- H2 `Elin Rask vill se användningstiderna först` — **statement**, **echo**: the sentence directly beneath is `Driftteknikern Elin Rask rekommenderar att koppla temperaturserier till användningstider innan styrningen ändras`, repeating both the name and `användningstider`, so the heading adds nothing to a reader who then reads on. The reply reports this itself as remaining finding 2.

No **colon**, **question** or **overclaim** marks on the returned text.

## Against the expectation

- *Unsupported catastrophe/health certainty visible against explicit limits* — **detected and repaired.** Both carriers of the certainty are gone (`men ändå är det helt säkert att givarna har gjort eleverna friskare` and `Katastrofen lurade bakom varje hörn.`), and the limit survives as `Ingen effekt på hälsan har undersökts.` The health removal is reported accurately; the headline's catastrophe claim is removed but **not reported** (see R1).
- *A standfirst and lead that repeat each other and open on the same word* — **detected and repaired.** `anatomy-input.json` norms carry `{"part": "lead", "measured": "både öppnar på ‘givarna’"}` (`"both open on “givarna”"`); `anatomy-delivered.json` reports `"norms": []`. The reply names the finding: *fyndet att ingress och lead inledde med samma mening*.
- *Late concept* — **partly addressed, not reported.** The definition of operative temperature stands unchanged at the term's first occurrence in the body, now under its own subheading, and no reasoning precedes it that depends on it. But the term now also stands in the H1 ahead of that definition, and the reply's account does not list the concept among either its repairs or its remaining findings.
- *An unbroken paragraph mixing unlike jobs* — **detected and repaired.** `anatomy-input.json` gives the lead as `187 words`, `"sentences_estimate": 8`, one paragraph; `anatomy-delivered.json` gives `53 words`, `"sentences_estimate": 3`, plus `"sections": 3` and `"paragraphs": 6`.
- *No byline, reported as missing and left unfilled* — **done exactly.** Both JSON files carry `"byline": null` and the failure `{"part": "byline", "measured": "absent"}`, and remaining finding 1 states it is left unfilled rather than invented.
- *A 187-word lead* — **repaired**, per the figures above.
- *No subheading anywhere, so the body has neither a section nor an ending* — **repaired for the section, reported for the ending.** The `sections: absent` failure is gone from `anatomy-delivered.json`, whose only remaining failure is the byline. The ending still calls the reader to nothing, which remaining finding 4 reports and argues cannot be filled without inventing a task.
- *A closing sales line unrelated to the explanation* — **detected, removed and reported** (`Kontakta oss för att rädda framtiden.`).
- *The 39-character headline meets its limit and fails on truthfulness instead* — **no rejected finding made.** The reply makes no length complaint; the replacement is on truthfulness. `anatomy-input.json` gives `"characters": 39`, `anatomy-delivered.json` `"characters": 52` — both inside the 20–70 requirement.
- *Restore navigation without deleting measured facts, exclusions or funding uncertainty* — **met**, per the preserved list under Changes.
- *A supplied-source investigation is not a remedy* — **respected.** The reply asks for no source; it flags the one shifted scope for the user to check against the report.

## G1 — pass

The article does the article's job for a Swedish reader of a municipal property office's measurement trial. The reader learns what was measured and by whom (`I rapporten *Mätförsök i Björkskolan* från den 12 mars 2026 redovisar fastighetskontoret mätningar med givare i sex klassrum`), what the figure means and does not mean (`14 av 120 lektionspass hade minst ett värde under kontorets egen arbetsgräns på 20 grader, vilket inte är en lagregel`), what the trial could not answer (`Operativ temperatur saknas, trots att resonemanget bygger på operativ temperatur`), and what happens next under what uncertainty (`fast finansieringen inte är beslutad`). The angle — the basis has gaps — is recognisable from headline to last line, and every claim is attributed to the report or to the named technician.

## G2 — pass

The parts do distinct jobs. The headline states the angle and is true to the body; the standfirst stands alone and sets three expectations (`vad försöket fångade, vad det inte fångade och vad driftteknikern rekommenderar`); the lead begins the work and comes before the first H2, which `anatomy-delivered.json` confirms by reporting a `lead` part separate from `"sections"`; the three sections answer the three expectations in order, and the last shows the standfirst's expectation met. Each section holds at least one paragraph (`1`, `2`, `1` in `anatomy-delivered.json`), so the counted requirement holds. The byline is absent (`"byline": null`), which for a Redline run on a text naming no author is the required behaviour, and remaining finding 1 reports it. Two shortfalls remain in the returned text: the subheading `Elin Rask vill se användningstiderna först` repeats its first sentence, which the reply reports as finding 2 but leaves standing after its single correction round; and the ending calls the reader to no action — the reply reports that as finding 4 and states it cannot be supplied without inventing an act the material does not contain, which is a method limit of a source-blind review, so it is scored under R1. Neither shortfall stops a part from doing its work, so the criterion holds.

## P1 — pass

The reasoning is followable and the conclusions are now proportionate to what is visible. The unfamiliar concept is defined where the body first uses it: `Operativ temperatur saknas, trots att resonemanget bygger på operativ temperatur, som är ett mått på lufttemperatur och värmestrålning från omgivande ytor, medan givarna bara mätte luften där de satt.` The transitions are real rather than decorative (`Rapporten anger också att…`; `Det saknas mätningar av…`). The technical substance is entirely retained — the 14-of-120 count, the four-week duration, the two-outer/four-inner sensor split, the air-versus-radiation distinction and the unfunded November trial. The one certainty that outran its support is gone, and what replaces it is the bare limit (`Ingen effekt på hälsan har undersökts.`). The reader meets `operativ temperatur` in the headline before the definition, a mild cost that the body pays back two paragraphs later.

## W1 — pass

A web reader can now enter the text. `anatomy-delivered.json` reports `"norms": []` — not one departure from a *should* — against `anatomy-input.json`'s two (`187 words` for the lead, and standfirst and lead opening on the same word). The counted figures all sit inside their requirements: headline `52` characters and `6` words, standfirst `35` words and `1` paragraph, lead `53` words and `1` paragraph, subheadings `43`, `27` and `42` characters. Standfirst and lead open on different first words (`Ett` / `I`) and complement each other: the standfirst promises three things and the body covers all three, so the body is complete when the standfirst is covered. The headings are informative where this genre needs them. Read across the whole text, the *most* statements are partly met — `"paragraphs_of_two_or_three_sentences": 4` of `"paragraphs": 6`, and `"sections_of_two_or_three_paragraphs": 1` of `"sections": 3` — and two sections carry a single short paragraph each. That is a qualitative thinness, not a reader loss: no explanation is cut across a heading, and it may not be scored against those single sections. No fragmentation or density costs the reader anything the input did not already cost more.

## L1 — pass

The prose reads as written in Swedish, not translated into it. `Här är vad försöket fångade, vad det inte fångade och vad driftteknikern rekommenderar innan styrningen ändras` uses native ellipsis and word order; `Underlaget har flera luckor` and `Placeringen redovisas, men inte dess effekt` are idiomatic Swedish headings rather than calques. The added attribution `I rapporten … redovisar fastighetskontoret mätningar` inverts subject and verb the way Swedish requires after a fronted adverbial. The one clumsy stretch — `mätningar av luftdrag och elevernas upplevelse och uppgifter om hur länge temperaturerna låg under gränsen` — is carried over verbatim from the input, not introduced.

## L2 — pass

Swedish locale mechanics govern throughout and nothing factual was converted or invented. The date keeps its Swedish form (`den 12 mars 2026`), the temperature its Swedish unit and spelling (`under 20 grader`), and the counts their Swedish phrasing (`14 av 120 lektionspass`, `fyra veckor`, `två givare`, `fyra vid innerväggar`). Sentence case is used for headline and subheadings, as Swedish takes it. No new date, figure or currency appears anywhere in `delivered.md`. The reply states that the closing mechanical pass found nothing to correct, and none of the returned text contradicts that.

## R1 — fail

The repair work itself is strong. Every finding is aimed at a defect the text actually carries: the certainty that outran the sentence beside it, the manufactured catastrophe, the content-free sentence, the sales close, the duplicated standfirst, the undefined definite reference, and the 187-word wall. Nothing outside those findings was touched — the working voice, the attributions, the technician's recommendation and every limiting clause survive verbatim, and the reply's own claim that they did (`Alla gränssättande uppgifter kom igenom oförändrade`) checks out against `delivered.md`. No clean passage was rewritten to taste, no *most* count was read against a single paragraph or section, and no *should* was enforced where the text had reason to leave it. The Skill made no finding that `expectation.md` rejects: no length complaint against the 39-character headline, and no demand for the source it cannot see.

Removals and changed claims, against the reply's account:

- `men ändå är det helt säkert att givarna har gjort eleverna friskare` — **reported accurately**, with the reason and with the preserved limit quoted.
- `Katastrofen lurade bakom varje hörn.` — **reported accurately**.
- `Det är viktigt att notera att detta är mycket viktigt…` — **reported accurately** (`bar inget sakpåstående`).
- `Kontakta oss för att rädda framtiden.` — **reported accurately**.
- `i sex klassrum` moved from the sub-20 readings to the measurements — **reported accurately and candidly**, including the instruction to check the new scope against the report. This is the change most likely to have cost something, and the reply is exact about it.
- Headline `Givarna räddar skolan från en katastrof` replaced — **not reported at all.** The most prominent claim in the text asserted a rescue and a catastrophe, was removed, and appears in no bullet. Worse, the account opens its ledger with `Fyra påståenden togs bort, och alla fyra togs bort därför att fyndet pekade ut just dem som defekten` — a completeness claim that is false, because a fifth claim was removed and a sixth (`räddar`, a causal claim distinct from the drama of `Katastrofen lurade bakom varje hörn.`) went with it.
- Standfirst replaced wholesale, with two new assertions (`Men flera uppgifter saknas i underlaget.` and the three-part promise) — **not reported as a change.** Both are supported by the body, so nothing false entered the text, but the reader is told only, obliquely inside the scope-move bullet, that the duplicate opening was a finding; they are never told the standfirst now says something new.

Visible defects left standing, all four reported: the missing byline (correct behaviour), the echoing subheading, the redundant `Givarna registrerade temperaturer under 20 grader.`, and the absent call to action. The first is required, the last is a genuine method limit, and the middle two are repairable with material in hand and were left only because the single correction round was spent — which the reply says plainly.

The criterion requires that every before/after claim be compared and every legitimate removal reported. A source-blind review's account is the record the user checks against the material the Skill never saw; an account that enumerates four removals while making five, and that silently rewrites both the headline and the standfirst, does not give the user that record. The verdict is `fail` on the account, not on the editing.
