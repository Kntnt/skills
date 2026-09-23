# Judgement B — run `article-flawed`

## Changes

The Skill returned a changed text. Every difference between `work/input.md` and `delivered.md`:

1. Headline — before: `Givarna räddar skolan från en katastrof`; after: `Mätförsöket i Björkskolan saknar operativ temperatur`. Change to what a claim says (rescue and catastrophe asserted, neither carried by the text) and the repair of a visible defect.
2. Standfirst — before: `Givarna registrerade temperaturer under 20 grader i sex klassrum. Givarna registrerade temperaturer under 20 grader i sex klassrum.` (the same sentence twice); after: `Ett mätförsök i Björkskolan visade temperaturer under fastighetskontorets egen arbetsgräns på 20 grader. Men flera uppgifter saknas i underlaget. Här är vad försöket fångade, vad det inte fångade och vad driftteknikern rekommenderar innan styrningen ändras.` Repair of a visible defect (duplication; standfirst and lead opening on the same word).
3. Opening of the body — before: `Givarna registrerade temperaturer under 20 grader i sex klassrum.`; after: `I rapporten *Mätförsök i Björkskolan* från den 12 mars 2026 redovisar fastighetskontoret mätningar med givare i sex klassrum.` plus a separate `Givarna registrerade temperaturer under 20 grader.` Change of scope: `i sex klassrum` now qualifies the measurements as a whole, not the readings below 20 degrees.
4. `Katastrofen lurade bakom varje hörn.` — removed. Repair of a visible defect (a claim the text supports nowhere).
5. `Fastighetskontorets rapport *Mätförsök i Björkskolan* från den 12 mars 2026 anger att 14 av 120 lektionspass …` — after: `Rapporten anger att 14 av 120 lektionspass …`. Mechanical consequence of change 3; title, date and source survive in the new first sentence, figures untouched.
6. `, medan två givare stod vid ytterväggar och fyra vid innerväggar, utan att placeringens effekt jämfördes experimentellt.` — after: a new `## Placeringen redovisas, men inte dess effekt` and `Rapporten anger också att två givare stod …`. Repair of a visible defect (`sections` measured `absent` in `anatomy-input.json`); `medan` → `också` is a change of taste in the joint.
7. `Operativ temperatur saknas, trots att resonemanget bygger på …` — text identical, now placed under a new `## Underlaget har flera luckor`. Repair of a visible defect.
8. `… hur länge temperaturerna låg under gränsen, men ändå är det helt säkert att givarna har gjort eleverna friskare, trots att ingen effekt på hälsan har undersökts.` — after: `… hur länge temperaturerna låg under gränsen. Ingen effekt på hälsan har undersökts.` Change to what a claim says: a certainty and a causal health effect removed; the limiting clause is kept at full strength as its own sentence.
9. `Driftteknikern Elin Rask rekommenderar …, och nästa försök är tänkt …` — after: a new `## Elin Rask vill se användningstiderna först` and the same two clauses as two sentences. Repair of a visible defect (sectioning); the sentence split is mechanical.
10. `Det är viktigt att notera att detta är mycket viktigt för alla som tycker att temperatur är viktigt.` — removed. Repair of a visible defect (carries no statement).
11. `Kontakta oss för att rädda framtiden.` — removed. Repair of a visible defect (a sales line unrelated to the explanation); the ending slot is left empty.
12. Byline — absent before, absent after. Unchanged and reported as missing.

Nothing was added that the input does not carry, and every figure, exclusion and hedge in the input survives: `14 av 120 lektionspass`, `20 grader`, `fyra veckor`, `två … fyra` sensors, `sex klassrum`, `12 mars 2026`, `Elin Rask`, `november`, `vilket inte är en lagregel`, `utan att placeringens effekt jämfördes experimentellt`, the whole operative-temperature sentence, the list of missing measurements, and `fast finansieringen inte är beslutad`.

## Headings

Input:

- `# Givarna räddar skolan från en katastrof` — **statement**, **overclaim** (the text nowhere says the sensors rescued anything, and the only catastrophe in it is the bare assertion `Katastrofen lurade bakom varje hörn.`). It shares the word `Givarna` with the standfirst but not its statement, so not **echo**.
- No level-2 subheading: `anatomy-input.json` measures `sections` as `absent` and `parts.sections` as `[]`.

Returned text:

- `# Mätförsöket i Björkskolan saknar operativ temperatur` — **statement**. Not **overclaim**: the body carries `Operativ temperatur saknas`. Not **echo**: it shares the subject `mätförsök i Björkskolan` with the standfirst, but the standfirst's statement (temperatures below the working limit) is a different one.
- `## Placeringen redovisas, men inte dess effekt` — **statement**, **echo** (its second half restates `utan att placeringens effekt jämfördes experimentellt` in the one sentence under it).
- `## Underlaget har flera luckor` — **statement**. No other mark.
- `## Elin Rask vill se användningstiderna först` — **statement**, **echo** (both the name and `användningstider` stand in the sentence directly under it). Not **overclaim**: `vill se … först` is a fair reading of `rekommenderar att koppla temperaturserier till användningstider innan styrningen ändras`.

## Against the expectation

- *Unsupported catastrophe certainty, visible against explicit limits* — detected and repaired: `Katastrofen lurade bakom varje hörn.` removed, the overclaiming headline replaced. The account names the sentence; it does not name the headline.
- *Unsupported health certainty, visible against explicit limits* — detected and repaired: `det är helt säkert att givarna har gjort eleverna friskare` removed, `Ingen effekt på hälsan har undersökts.` kept as its own sentence. Reported accurately.
- *Standfirst and lead repeating each other and opening on the same word* — detected and repaired. `anatomy-input.json` norms: `both open on "givarna"`; `anatomy-delivered.json` has `"norms": []`, and the two now open on `Ett` and `I`.
- *Late concept* — detected and repaired: the report and the sensors are introduced in the new first sentence before the definite `Givarna` is used. The account states the finding as `ledet använde *Givarna* i bestämd form utan att ha introducerat dem`.
- *Unbroken paragraph mixing unlike jobs* — detected and repaired: `anatomy-input.json` `typical.paragraphs` 2, `sections` 0; `anatomy-delivered.json` `typical.paragraphs` 6, `sections` 3.
- *No byline, reported as missing and left unfilled* — done exactly. `anatomy-delivered.json` still lists the `byline` failure with `"measured": "absent"`, and remaining finding 1 reports it and declines to invent a name.
- *187-word lead* — repaired. `anatomy-input.json` `parts.lead.words` 187; `anatomy-delivered.json` `parts.lead.words` 53, with no lead norm left.
- *No subheading anywhere, so the body has neither a section nor an ending* — the sections are restored (three, per `anatomy-delivered.json`); the ending is **not** restored. The Skill reports this as remaining finding 4 and argues no reader action exists in the material.
- *Closing sales line unrelated to the explanation* — detected, removed, reported.
- *The 39-character headline meets its limit and fails on truthfulness instead* — respected. `anatomy-input.json` gives `characters: 39`, inside 20–70, and the Skill makes no length finding against it; it replaced it on truthfulness.
- *A supplied-source investigation is not a remedy* — respected. The account hands the scope question back (`Stämmer den nya räckvidden inte med rapporten är det här det behöver rättas`) instead of claiming to have checked the report.

No finding was made that `expectation.md` rejects.

## G1 — pass

The returned text does an explanatory article's job. The reader learns what was measured (`14 av 120 lektionspass hade minst ett värde under kontorets egen arbetsgräns på 20 grader`), on what basis (`mätningar med givare i sex klassrum`, `försöket varade fyra veckor`), what the basis cannot say (`Operativ temperatur saknas`, `Det saknas mätningar av luftdrag och elevernas upplevelse`, `Ingen effekt på hälsan har undersökts.`), and what is recommended before anything is changed (`koppla temperaturserier till användningstider innan styrningen ändras`). The angle — a trial whose own basis is thinner than its conclusion — is recognisable from headline to last line, and the craft is journalistic: every figure is attributed to the report, and the one non-legal limit is marked as such (`vilket inte är en lagregel`).

## G2 — fail

Headline, standfirst, lead, sections and an explanatory body are present and do distinct jobs, and the byline's absence is not held against the text: nobody names an author, and the run reports it missing and leaves it unfilled, which is what this criterion asks of a Redline run. The failure is the ending. The last paragraph — `Nästa försök är tänkt att använda likadant placerade givare i november, fast finansieringen inte är beslutad.` — is the property office's next step, not the reader's, so the article genre's call to action is absent from the returned text; a reader who has followed the gaps is left with nothing to do about them. A second part-level flaw: `## Elin Rask vill se användningstiderna först` is not understood apart from the sentence under it, which repeats both the name and `användningstider`. The reply reports both as findings it could not repair without knowing whom the article addresses and without a second correction round; the detection and reporting are scored under `R1`, but the returned text is still missing the part.

## P1 — pass

The reasoning is followable in sequence: the report is named and dated, the figures follow, then the limits, then the recommendation. The unfamiliar concept is introduced where the body first uses it — `operativ temperatur, som är ett mått på lufttemperatur och värmestrålning från omgivande ytor, medan givarna bara mätte luften där de satt` — and the headline's use of the term is resolved a few lines later. The transitions are real rather than decorative (`Rapporten anger också att …`). Conclusions are now proportionate to the visible support: with the certainty about pupils' health gone, nothing in the text claims more than the trial measured. The technical substance survives intact — sensor placement, duration, the missing draught and experience measurements, the undecided funding.

## W1 — pass

A web reader can orient: three informative subheadings where the input had none, and a standfirst that stands alone and is fully covered by the body (it promises what the trial caught, what it did not and what the technician recommends; all three are delivered). `anatomy-delivered.json` reports `"norms": []` — no paragraph over 80 words, no *should* left anywhere — against `anatomy-input.json`'s two lead norms (`187 words`, `both open on "givarna"`). Counted requirements hold: headline `characters: 52` and `words: 6`, standfirst `words: 35` in one paragraph, lead `words: 53` in one paragraph before the first H2, subheadings at `43`, `27` and `42` characters, every section carrying at least one paragraph. Read across the whole text, `typical.paragraphs_of_two_or_three_sentences` is 4 of `paragraphs` 6 — typical holds for paragraphs. `sections_of_two_or_three_paragraphs` is 1 of `sections` 3, so the second *most* statement does not hold across the text; that count supports a judgement rather than making a failure, and the reader loss is small, because the thin sections are the honest residue of removing unsupported material rather than fragmentation of an argument. The one genuine reader cost is the echo noted under G2 and the redundant `Givarna registrerade temperaturer under 20 grader.` at the end of the lead, both of which the reply itself reports.

## L1 — pass

The prose reads as written in Swedish, not translated into it: `Underlaget har flera luckor`, `Rapporten anger också att`, `fast finansieringen inte är beslutad`, `Driftteknikern Elin Rask rekommenderar att koppla temperaturserier till användningstider`. Syntax and word order are native throughout, and the new sentences the run wrote (headline, standfirst, the report-naming opener) are idiomatic. The one clumsy stretch — `mätningar av luftdrag och elevernas upplevelse och uppgifter om hur länge temperaturerna låg under gränsen`, with two coordinating `och` in a row — is carried over verbatim from the input rather than introduced here.

## L2 — pass

Swedish locale mechanics govern throughout: the date is `den 12 mars 2026` in Swedish long form, the temperature is `20 grader` with the unit spelled out, `14 av 120` uses no separators, and the quantities keep the input's forms. No date was changed and no currency or unit was converted. Established variation in the input is preserved; the final mechanical pass reports nothing found to correct, and nothing in the returned text contradicts that.

## R1 — pass

The run addressed the concrete visible defects and preserved everything outside its findings. Removals and changed claims, against the Skill's own account:

- `Katastrofen lurade bakom varje hörn.` — removed; reported, and accurately (`tillverkad dramatik utan stöd i materialet`).
- `det är helt säkert att givarna har gjort eleverna friskare, trots att ingen effekt på hälsan har undersökts` — certainty and causality removed, the limit kept; reported, and accurately, including the fact that the limiting clause survives as its own sentence.
- `Det är viktigt att notera att detta är mycket viktigt …` — removed; reported, and accurately (`bar inget sakpåstående`).
- `Kontakta oss för att rädda framtiden.` — removed; reported, and accurately, with the consequence for the ending stated separately as finding 4.
- `Givarna registrerade temperaturer under 20 grader i sex klassrum` — split, with `i sex klassrum` moved onto the measurements as a whole; reported, and accurately, including which two findings the repair answered and the flag that the new scope is the place to correct if the report says otherwise.
- The three added subheadings — acknowledged indirectly, in findings 2 and 3 (`den mellanrubriken fanns inte i texten som kom in`; `uppstod ur korrigeringsrundan, som delade den ursprungliga öppningsmeningen i två`).
- The replaced headline — **not reported**. `Givarna räddar skolan från en katastrof` was the text's largest overclaim and the run was right to remove it, but the account's list of what happened to the claims never names it, and the `Katastrofen`-bullet quotes only the body sentence. This is the run's one accounting gap: a legitimate removal left unlisted. It is not an unresolved finding going unreported, and it leaves nothing false in the text, so it does not overturn the verdict.
- The replaced standfirst — covered, since its only content was the duplicated sentence accounted for above.

Visible defects the run did not address: the ending still calls the reader to nothing, and `## Elin Rask vill se användningstiderna först` still repeats its first sentence, as does `Givarna registrerade temperaturer under 20 grader.` repeat the sentence before it. All three are reported as remaining findings with reasons — an exhausted correction budget for the two the repair itself created, and absent knowledge of the intended reader for the ending. Two of the three would not exist without the repair, which the account says plainly instead of hiding.

No clean passage was rewritten to taste, no *most* count was applied to a single paragraph or section, no *should* with good reason behind it was overturned, and no finding was made against a requirement the input met — in particular, the 39-character headline was never faulted on length. No verification of the unavailable report is claimed anywhere. No side effects: the reply states that no `kntnt` frontmatter existed or was added and that nothing was written to disk.
