# Judgement B — run `article-clean`

## Changes

none

`work/input.md` and `delivered.md` are byte-identical (both 1638 bytes, identical checksum; `diff` reports no difference). The two anatomy files are identical as well. The reply's account matches: "Texten är oförändrad, och inget har skrivits."

## Headings

### Input

- `# Mätförsöket i Björkskolan visar när, inte varför` — **statement** (a clause saying what the text says: the trial shows when, not why). Not **colon** (no colon), not **question**, not **echo** (the standfirst restates the point in other words — "pekar ut tillfällen att undersöka närmare, men förklarar inte varför luften var kall" — sharing only the single word "varför", which is not a repetition of wording or phrasing), not **overclaim** (the body carries exactly this: "räknar 14 lektionspass av 120 med minst en mätning under den gränsen … Hur länge temperaturen låg under den anger rapporten inte").
- `## En gräns för det lokala försöket` — **label** (a plain name for what the section holds: the office's own working limit). Not **statement**, **colon**, **question** or **overclaim**. Not **echo**: the first sentence under it is "Kontoret valde 20 grader Celsius som arbetsgräns", which shares the stem *gräns* but no wording or phrasing.
- `## Nästa försök behöver mer än givare` — **statement** (a clause: the next trial needs more than sensors). Not **colon**, **question** or **echo** (first sentence under it: "Rask rekommenderar att temperaturserierna kopplas till rummens användningstider innan styrningen ändras"). Not **overclaim**: the section carries both the recommendation and "finansieringen är inte beslutad".

### Returned text

Identical, the text being unchanged:

- `# Mätförsöket i Björkskolan visar när, inte varför` — **statement**.
- `## En gräns för det lokala försöket` — **label**.
- `## Nästa försök behöver mer än givare` — **statement**.

## Against the expectation

| What `expectation.md` asks | Outcome |
|---|---|
| Conforms to the anatomy | Preserved. Script: `"conforms": true`, `"failures": []`, `"norms": []` on both input and returned text. |
| Preserve the calm explanation | Preserved. The whole explanatory body is returned unchanged, including "Ett lågt värde säger alltså när luften var kall, men inte hur rummet kändes." |
| Preserve the independent result-bearing standfirst | Preserved, unchanged, 46 words, 1 paragraph (script), carrying its own result: "Under 14 av 120 lektionspass registrerade givarna … temperaturer under fastighetskontorets egen arbetsgräns." |
| Preserve the byline | Preserved. Script: `"byline": {"text": "Text: Hedda Lund"}`. |
| Preserve the quoted summary | Preserved: "Vi vet när vi behöver titta närmare. Vi vet ännu inte varför det blev kallt just då." |
| Preserve the undecided funding | Preserved: "men finansieringen är inte beslutad". |
| Preserve the ending's non-commercial next step | Preserved: "Lägg därför tiderna för när rummen används bredvid mätvärdena innan nästa givare sätts upp." No offer, link or commercial turn added. |
| ABT-shaped logic must not select a technique | Respected, and stated: "Ingen teknik tillämpades: ingen angavs, och genren artikel anger ingen som den vanligen skrivs med." |
| Reject any finding against a limit the text meets (48-char headline, 46-word standfirst, 32- and 34-char subheadings, no paragraph over 80 words) | No finding made. Script confirms the figures: headline 48 characters/7 words; standfirst 46 words; subheadings 32 and 34 characters; longest paragraph 45 words. |
| Reject any finding resting on the one-sentence paragraph, the four-sentence paragraph or one section's paragraph count | No finding made. Script: the final paragraph is `"sentences_estimate": 1`, the first body paragraph `"sentences_estimate": 4`, and `"sections_of_two_or_three_paragraphs": 2` of `"sections": 2`. The Skill left all three alone. |
| Reject a finding against the Swedish `Text:` byline form | No finding made; the form is returned as written. |
| Reject a name the text does not carry | No name introduced; the text is byte-identical, so the only names remain "Hedda Lund", "Elin Rask" and "Björkskolan". |

## G1 — pass

The article does an explanatory job for a reader of a municipal property office and a school: it tells them what a four-week sensor trial in six classrooms can and cannot settle, and keeps one recognisable angle — measurement locates occasions, not causes — from headline through quotation to ending. The reader learns the concrete result ("räknar 14 lektionspass av 120 med minst en mätning under den gränsen"), the two things the instruments did not capture ("Givarna mätte varken luftdrag eller elevernas upplevelse"), and one thing to do next. The craft is journalistic and sourced: a dated report, a named technician, an attributed quotation, and an explicit statement that the limit is the office's own choice ("Gränsen är kontorets egen, vald för det här försöket").

## G2 — pass

Every part is present, in order, and each does its own job. Script `parts`: `headline`, `standfirst`, `byline`, `lead`, then two `sections`, with `"other": []` — nothing falls outside the skeleton. The headline states the angle and is understood alone. The standfirst stands alone and carries the result, one paragraph (script: `"paragraphs": 1`). The byline names an author the text carries, "Text: Hedda Lund", so the missing-byline report does not arise. The lead begins the work — "En temperaturgivare mäter luften där den sitter" — and sits before the first H2 (script places it outside `sections`). The body is explanatory, and the ending shows the lead's expectation met: the lead promises "Genomgången nedan visar vad värdena räcker till och var gränsen går", and the close delivers the useful next step the explanation supports, "Lägg därför tiderna för när rummen används bredvid mätvärdena innan nästa givare sätts upp" — non-commercial, as the assignment warrants.

## P1 — pass

The reasoning is followable and the one unfamiliar idea is introduced before it is used: the lead defines what a sensor measures ("mäter luften där den sitter") before placement is made to matter ("Det gör placeringen viktig"). Transitions are real, not decorative — "alltså" carries the inference from what the sensors omitted to what a low value can mean, and "därför" carries the recommendation out of Rask's diagnosis. Conclusions stay proportionate to visible support: the count is qualified twice ("minst en mätning under den gränsen"; "Hur länge temperaturen låg under den anger rapporten inte"), and the quotation stops exactly where the data stops. Useful technical substance remains: the threshold and its provenance, the 14/120 count, the sampling gap, and the proposal to join temperature series to room-use times.

## W1 — pass

Every counted requirement is met on the script's figures, and no *should* is departed from. Headline: 48 characters, 7 words — inside 20–70 and inside the 60-character/eight-word norm. Standfirst: 46 words, at most 60, one paragraph. Lead: one paragraph, 33 words. Subheadings: 32 and 34 characters, at most 70. Sections: 2, each with at least one paragraph, longest paragraph 45 words — no paragraph over 80, no section over three paragraphs. Only H1 and H2 appear, so no heading level below the second. Standfirst and lead open on different first words ("Under" / "En"). The *most* statements are read across the whole text and hold: `"paragraphs_of_two_or_three_sentences": 5` of `"paragraphs": 7`, and `"sections_of_two_or_three_paragraphs": 2` of `"sections": 2`. A web reader can orient from two informative subheadings without the continuous explanation breaking; there is no density or fragmentation loss to identify.

## L1 — pass

The Swedish is native in idiom and syntax, with no generic translated-English feel. Constructions such as "Det gör placeringen viktig när fastighetskontoret ska tolka fyra veckors mätningar", "Hur länge temperaturen låg under den anger rapporten inte" (idiomatic Swedish fronting with V2 inversion) and "vald för det här försöket" are ones a Swedish professional would write. Vocabulary is domain-correct and unforced: *givare*, *arbetsgräns*, *driftteknikern*, *styrningen*, *lektionspass*. The quotation reads as speech: "Vi vet ännu inte varför det blev kallt just då."

## L2 — pass

Swedish locale mechanics govern throughout. Quotation marks are the Swedish pair ”…”, not English ones. The date is written in Swedish form, "daterad 12 mars 2026", with a lower-case month and no ordinal. The temperature is spelled out in Swedish usage, "20 grader Celsius". No currency appears, and none was invented; no date was converted or added. Established variation is preserved, including the byline form "Text: Hedda Lund".

## R1 — pass

The Skill returned the text unchanged and reported no findings. That is correct here, and it is the harder of the two outcomes to get right.

- **Removals and changed claims:** none. The files are byte-identical, so there is nothing to compare before and after, nothing whose strength, subject, scope or modality moved, and no removal to report. The account states this exactly and accurately: "Inga anmärkningar. Korrekturpasset hittade inga mekaniska fel. Texten är oförändrad, och inget har skrivits."
- **Visible defects not addressed:** none found. The script reports `"failures": []` and `"norms": []`, so no anatomy requirement or norm was left broken. Reading the text alone — the only material a source-blind Redline has — I find no internal contradiction: the standfirst's "temperaturer under … arbetsgräns" and the body's "minst en mätning under den gränsen" agree, the headline's "när, inte varför" matches the quotation's "Vi vet ännu inte varför", and the ending's action follows from Rask's recommendation. Swedish mechanics are clean, so the empty proofread result is accurate rather than a missed pass. Hidden invention cannot be required of a source-blind control, and no visible contradiction exists to catch.
- **Findings `expectation.md` rejects:** none made. The run made no finding against the 48-character headline, the 46-word standfirst, the 32- and 34-character subheadings, any paragraph length, the one-sentence closing paragraph, the four-sentence opening body paragraph, one section's paragraph count, or the `Text:` byline form; it introduced no name the text does not carry, and it selected no technique from the ABT-shaped logic.

No taste rewrite was imposed on a clean text, no *most* count was read against a single paragraph or section, and no *should* the text had good reason to leave was treated as a defect. None of the protocol's five unconditional rejections is triggered: no unsupported fact was added, the locale is untouched and correct, no substantive mechanical editing occurred, there is no mandatory finding left unreported, and there are no side effects.
