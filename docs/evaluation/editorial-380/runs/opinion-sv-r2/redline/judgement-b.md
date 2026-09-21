# Judgement B — opinion-sv-r2 / redline

Genre is `opinion` in the text's own `kntnt` map, so the anatomy skeleton applies in full and its counted requirements are judged by the script's figures.

## 1. Changes

Four differences between `redline/work/input.md` and `redline/delivered.md`.

1. Lead, sentence 1 — before: "Tjänsteutlåtandet inför kommunstyrelsens möte den 18 juni **föreslår att telefonbokningen av föreningslokaler tas bort i alla sju lokaler** från september." / after: "Tjänsteutlåtandet inför kommunstyrelsens möte den 18 juni **vill ha webben som enda bokningsväg till samtliga sju föreningslokaler** från september." — **a change to what a claim says**: the speech act moves from *föreslår* (what a tjänsteutlåtande does) to *vill ha* (a want attributed to a document), and the object of the claim moves from the removal of the telephone route to the web as sole route. The facts named (source, 18 juni, seven premises, september) are unchanged.
2. Subheading 1 — before: "## Pilotrapporten mäter inte vem som inte kan boka digitalt" / after: "## Pilotrapporten från Lervik mäter inte vem som inte kan boka digitalt" — **a change of taste**: the added attribution helps the subheading stand alone, but repeats the standfirst's "Lerviks pilotrapport". No claim changes; script figures 56 → 68 characters, 9 → 11 words, still inside the 70-character requirement.
3. Section 1, paragraph 1 — before: "Under **de** åtta veckorna gjordes 96 bokningar via webben och 24 via telefon **i de två lokalerna**." / after: "Under åtta veckor **i två lokaler** gjordes 96 bokningar via webben och 24 via telefon." — **a change of taste**: the same two facts reordered, definite reference to the standfirst's period made indefinite. Script: 36 → 34 words. The repetition of the standfirst's "åtta veckor i två lokaler" survives the edit and sits earlier in the sentence than before.
4. Section 2, paragraph 1, sentence 2 — before: "Den är verklig och handlar om personalens arbetstid**, inte om att de som ringer skulle vara lata eller dyra**." / after: "Den är verklig och handlar om personalens arbetstid." — **a change to what a claim says**, by removal: the text no longer disclaims the motive it previously declined to impute to the administration. Script: 30 → 19 words in that paragraph.

No other line, number, heading, byline or frontmatter field differs.

## 2. Headings

### Input

- `# Kommunstyrelsen bör pröva båda bokningsvägarna ett halvår` — **statement**
- `## Pilotrapporten mäter inte vem som inte kan boka digitalt` — **statement**
- `## Handlingarna saknar mätning av vad det dubbla arbetet kostar` — **statement**
- `## Ett halvår med båda vägarna ger underlaget` — **statement**, **echo** (partial: "båda vägarna" against the first sentence's "båda bokningsvägarna kvar"; the heading's own claim, "ger underlaget", is not in that sentence)
- `## Kommunstyrelsen kan pröva först och besluta sedan` — **statement**, **echo** (partial: "Kommunstyrelsen kan" opens the first sentence under it)

### Returned text

- `# Kommunstyrelsen bör pröva båda bokningsvägarna ett halvår` — **statement**
- `## Pilotrapporten från Lervik mäter inte vem som inte kan boka digitalt` — **statement** (no echo of the first sentence under it; the added "från Lervik" does repeat the standfirst's "Lerviks pilotrapport", but the standfirst is not the comparison for a subheading)
- `## Handlingarna saknar mätning av vad det dubbla arbetet kostar` — **statement**
- `## Ett halvår med båda vägarna ger underlaget` — **statement**, **echo** (partial, as above)
- `## Kommunstyrelsen kan pröva först och besluta sedan` — **statement**, **echo** (partial, as above)

No heading in either text is a label, carries a colon standing in for a verb, is a question, or overclaims: every figure and conclusion in a heading ("mäter inte vem", "saknar mätning", "kan pröva först") is carried at the same strength in the section beneath it.

## 3. G1 — pass

The opinion does its job for a Lervik resident and for the kommunstyrelse it addresses. The reader is given a position in the headline ("Kommunstyrelsen bör pröva båda bokningsvägarna ett halvår"), the two things the decision papers lack ("varken en tidsmätning eller en ekonomisk besparingsberäkning finns i handlingarna"), and a concrete alternative to weigh ("ett sex månader långt försök i alla sju lokaler, med båda bokningsvägarna kvar"). The angle — decide only once the two missing measurements exist — holds from the standfirst to the last sentence, "Vi motsätter oss att frågan avgörs innan de två uppgifterna ligger på bordet". The craft of the form is present: figures are attributed to the report that carries them, and the author's own limits are stated rather than hidden ("Vi gör inget anspråk på att ha kostnadsberäknat eller finansierat försöket").

## 4. G2 — pass

Every part of the anatomy is present, in order, and each does its own job. The script reports `conforms: true`, `failures: []` and `norms: []` for the returned text, so no counted requirement fails.

- Headline: 57 characters, 7 words (script, `parts.headline`) — inside the 20–70-character requirement and inside the *should* of 60 characters and eight words. It states the angle and is understood alone.
- Standfirst: 46 words, 1 paragraph (script, `parts.standfirst`) — inside the 60-word requirement and the one-paragraph requirement. It stands alone: report, proposal, and the association's ask are all in it.
- Byline: "Av Sanna Ek, talesperson för föreningen Öppna beslut" (script, `parts.byline`, 8 words). The text names its author, so there is nothing for a Redline run to report as missing and nothing was filled in.
- Lead: 1 paragraph, 43 words (script, `parts.lead`), and it stands before the first H2. It begins the work by naming the meeting, the proposal and its stated motive, then poses the article's own question ("Men två uppgifter som borde ligga på kommunstyrelsens bord saknas i handlingarna").
- Sections: four, each with at least one paragraph (script, `parts.sections`), each explanatory rather than decorative.
- Ending: "Den kan också låta båda vägarna stå kvar ett halvår, ta ställning till kostnaden och sedan avgöra om en kanal ska tas bort, ändras eller behållas" meets the expectation the lead set.

The opinion-specific parts hold. Position early: headline plus "Öppna beslut vill se ett halvår med både telefon och webb" in the standfirst. Support: the counting defect in the pilot report and the two absent measurements. A relevant real objection, conceded rather than dismissed: "Förvaltningens invändning mot att behålla båda vägarna är den dubbla administrationen. Den är verklig." The call to action is the change itself, addressed to an identifiable actor — kommunstyrelsen, named in the headline, the final subheading and the final paragraph. Nothing commercial appears.

One cost of the Redline edit is visible but does not fail the criterion: the lead's "vill ha webben som enda bokningsväg" no longer names the document's act as a proposal, so the ending's "säga ja till förslaget" now refers back to "Ett förslag som tar bort en bokningsväg i sju lokaler" in section 2 rather than to the lead. The referent is recoverable; the part still does its job.

## 5. P1 — pass

The reasoning is followable by a resident with no special knowledge. Each step is stated before it is used: bookings are counted, not people ("Rapporten räknar bokningar, inte unika personer"), therefore the phone figure cannot measure exclusion ("Därför säger den ingenting om hur stor andel av invånarna som inte kan boka digitalt"). The text then refuses the symmetrical over-reading as well — "har lika lite stöd i rapporten som den som hävdar motsatsen" — which keeps the conclusion proportionate to the visible support. The transitions are real, not decorative: "Men varken en tidsmätning eller en ekonomisk besparingsberäkning finns i handlingarna" turns the conceded objection into the second gap. Technical substance remains after the review: the 96/24 split, the eight weeks, the two premises, the seven premises, the September date and the 18 June meeting all survive unchanged, and the proposed trial still specifies what would be measured ("registrerar förvaltningen tidsåtgången per bokningsväg"). The one term a lay reader might not hold, *tjänsteutlåtande*, is given its function in the same sentence it appears in — it goes before a named meeting and contains a proposal.

## 6. W1 — pass

A web reader can orient and enter without losing the continuous argument. The four subheadings are informative statements that say what their sections conclude, and the text's voice — first-person association, plain administrative vocabulary — is unbroken across them.

Counted evidence, all from the script's `anatomy-delivered.json`:

- `typical.paragraphs: 10`, `typical.paragraphs_of_two_or_three_sentences: 9`. Read across the whole text as *most* requires, the text is typical. The single four-sentence paragraph is the closing one; it is not judged against *most* on its own.
- `typical.sections: 4`, `typical.sections_of_two_or_three_paragraphs: 3`. Again typical across the whole text; the one-paragraph final section is not a failure on its own, and a one-paragraph section meets the "at least one paragraph" requirement.
- Longest paragraph: 57 words (`parts.sections[3].paragraphs[0]`), under the 80-word *should*. No paragraph departs.
- Headline: 57 characters, 7 words — inside the *should* of 60 characters and eight words, so nothing to excuse.
- Subheadings: 68, 60, 42, 49 characters — all inside the 70-character requirement.
- Heading levels: only the level-1 headline and level-2 subheadings appear; no level below the second.
- `failures: []`, `norms: []`.

Standfirst and lead are complementary and open on different first words — "Lerviks" against "Tjänsteutlåtandet" — so the counted *should* is met. On substance the returned text is better here than the input was: the input's lead opened by restating the standfirst's second sentence almost word for word ("telefonbokningen av föreningslokaler tas bort i alla sju lokaler från september" against "telefonbokningen av föreningslokaler försvinna i alla sju lokaler från september"), and the edit breaks that repetition. The body completes what the standfirst promises: both the half-year with both routes and the figures on time per route are delivered in sections 2 and 3. No density or fragmentation loss is identifiable.

## 7. L1 — pass

The prose reads as professionally written Swedish, with native syntax and no imported English shape. The negation-first constructions are idiomatic — "Rapporten räknar bokningar, inte unika personer", "Att en bokning går via telefon är inte ett bevis för att någon inte kan använda webben" — and the administrative register is the one Swedish municipal debate uses: *tjänsteutlåtande*, *handlingarna*, *förvaltningen*, *ta ställning till*, *ligga på kommunstyrelsens bord*. Sentence rhythm varies without strain. The edited lead's "Tjänsteutlåtandet … vill ha webben som enda bokningsväg" is an established Swedish metonymy for what a document proposes and reads naturally, even though it is looser than the *föreslår* it replaced.

## 8. L2 — pass

Swedish locale mechanics govern throughout. The date is written "den 18 juni", not an English or numeric form. Figures follow Swedish practice: digits inside the sentence ("96 bokningar via webben och 24 via telefon") and the word at sentence start ("Tjugofyra telefonbokningar kan vara tjugofyra invånare"). Compounds are closed as Swedish requires — *bokningsvägarna*, *föreningslokaler*, *besparingsberäkning*, *telefonbokningen*, *tidsåtgången*. No currency amount and no converted figure appears, and no new date is introduced: 18 June and September are the input's. Established variation in the input is preserved. Nothing in the returned text is a mechanical error left standing.

## 9. T2 — skipped

No technique is named in the text's metadata or in the reply. The `kntnt` map in `redline/delivered.md` reads `technique: none`, and the reply states it explicitly — "Genre `opinion`, teknik `none` och språk `sv`" and "kartan säger att ingen teknik var utlöst, så genrens vanliga båge tillämpas inte". Nothing is judged under this criterion, and no technique is inferred from the shape of the prose.

## 10. R1 — fail

The script measured the input as already conforming: `conforms: true`, `failures: []`, `norms: []` in `anatomy-input.json`. The Skill read this correctly and made no counted finding — its account says "texten uppfyller varje krav och avviker inte från någon norm". So all three findings were qualitative, made against a text with no anatomy defect, and the test is whether each addressed a concrete visible defect.

**Change 1 (lead rewrite) — a defensible repair, reported, reported accurately.** The visible defect was real: the input lead's first sentence repeated the standfirst's second sentence nearly verbatim, so the lead's opening added nothing. The account reports the change, quotes both versions, names the finding it answered, states exactly what moved — "talakten har flyttats från 'föreslår' till 'vill ha'" — and says where the displaced information now appears. It also hands the trade-off back to the user rather than concealing it: "Om 'föreslår' ska tillbaka är en avvägning för dig: det är det ord ett tjänsteutlåtande handlar med, och avslutningens 'säga ja till förslaget' syftar tillbaka på det." That is accurate and complete reporting of a claim change. The repair is weaker than the defect deserved — it swapped a precise speech-act verb for a looser one and broke the antecedent of "förslaget" — but it is a repair of something visibly wrong, not taste.

**Change 4 (removal of "inte om att de som ringer skulle vara lata eller dyra") — a change of taste to a passage that already worked, and it removed a claim.** Nothing about that clause was visibly defective. It did not contradict anything, overclaim anything, or break a count. Its job in an opinion piece is exactly what the Skill treated as its fault: it declines, in the author's own voice, to impute a bad motive to the administration whose objection the section has just conceded as real. Removing it thins the text's handling of the opponent's position, which is the part of the opinion form under most pressure. The removal is reported and the removed content is quoted accurately — "Det som försvann är påståendet att förvaltningens invändning inte handlar om att de som ringer skulle vara lata eller dyra" — so the reporting duty is met. But the account's closing assertion about it is not accurate: "Texten avgränsar därmed sina anspråk precis lika långt som förut." The text no longer delimits that claim at all; the disclaimer is the delimitation, and it is gone. Unlike change 1, this one was not offered back to the user as a judgement call.

**Changes 2 and 3 (subheading and paragraph reordering) — changes of taste to passages that worked, and neither is reported.** The account's inventory is confined to claims and ends "Inga andra påståenden ändrade omfattning, säkerhet, källa, kronologi, orsakssamband eller betydelse. Samtliga siffror står kvar som de stod, liksom rubriken, ingressen, bylinen och frontmattern." Each of those statements is true as far as it goes, and neither change alters a claim, so neither is a reporting rejection. But the account says three findings were raised and all three repaired, and never says what the third was or what it changed. A user comparing the two texts finds two edits — a rewritten subheading and a resequenced opening sentence — that the reply does not account for. Change 3 also fails on its own terms: if the repetition of the standfirst's "åtta veckor i två lokaler" was the defect, the edit preserved it and moved it forward in the sentence, while change 2 added a second echo of the standfirst ("Lerviks pilotrapport" → "Pilotrapporten från Lervik").

**What was preserved.** Every figure, the quotation-derived passage "Att en bokning går via telefon är inte ett bevis…", the headline, the standfirst, the byline, the frontmatter and all four section arguments stand untouched. No claim outside a finding was altered, no source was invented, and no unavailable-source verification was attempted. Nothing was written to the filesystem, and the reply says so.

**Verdict.** The reporting discipline is good and the one real defect was addressed. But a text the script measured as fully conforming had a claim removed on a taste judgement, with the reply asserting that the text's delimitation was unchanged when it was not, and two further unreported cosmetic edits — one of which did not achieve what its finding described. `R1` fails on "a clean text is not rewritten to satisfy taste".

## 11. Source loss

No part of any criterion above; the Skill never saw `write/work/source.md` and could not have known this.

**One required formulation was removed.** The source states, in the paragraph on the tjänsteutlåtande: "Förvaltningens verkliga invändning mot att behålla båda kanalerna är dubbel administration, **inte att telefonanvändare är lata eller dyra**." The boundaries section reinforces it: "Författaren ska kunna kritisera beslutsunderlaget skarpt **utan falska motiv** eller tandlös neutralisering." Change 4 deleted precisely the half of that sentence the source marks — "Den är verklig och handlar om personalens arbetstid, **inte om att de som ringer skulle vara lata eller dyra**" became "Den är verklig och handlar om personalens arbetstid." The careful statement of what is *not* being claimed about the administration's motive, which the source supplies and the brief's boundaries require, is no longer in the text.

**One attribution was weakened.** The source reads: "Tjänsteutlåtandet inför kommunstyrelsens möte den 18 juni **föreslår** att telefonbokning tas bort för alla sju lokaler från september." Change 1 replaced *föreslår* with *vill ha webben som enda bokningsväg*, so the document is no longer described as making a proposal. The underlying fact survives and no figure or date moved, but the source's precise characterisation of the document's act did not.

No other source caveat, limit or careful formulation was touched: the association's disclaimer about funding and costing, the report's inability to measure exclusion, and the naming of the kommunstyrelse's possible decisions with the cost uncertainty intact all remain in the returned text.
