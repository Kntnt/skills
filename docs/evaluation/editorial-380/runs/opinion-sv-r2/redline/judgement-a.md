# Judgement A — redline, row `opinion-sv-r2`

Genre from the text's own `kntnt` map: `opinion`. The anatomy skeleton therefore applies as a requirement, and every counted line below quotes `anatomy-input.json` or `anatomy-delivered.json`.

## 1. Changes

Four differences between `redline/work/input.md` and `redline/delivered.md`.

1. **Lead, first sentence.** Before: "Tjänsteutlåtandet inför kommunstyrelsens möte den 18 juni föreslår att telefonbokningen av föreningslokaler tas bort i alla sju lokaler från september." After: "Tjänsteutlåtandet inför kommunstyrelsens möte den 18 juni vill ha webben som enda bokningsväg till samtliga sju föreningslokaler från september." — **repair of a visible defect, carrying a change to what the claim says.** The defect is real: the input lead repeated the standfirst's second sentence ("Ändå föreslås telefonbokningen av föreningslokaler försvinna i alla sju lokaler från september") almost word for word. The repair also moves the speech act from "föreslår" (what a tjänsteutlåtande formally does) to "vill ha" (a want attributed to the document), and states the proposal by its effect ("webben som enda bokningsväg") rather than its content. The effect-form is a small scope inference: the text names only telephone and web, so "only route" follows inside the text, but it forecloses routes the text never mentions. Script: lead 44 words before, 43 after; one paragraph in both; it still precedes the first H2.
2. **First subheading.** Before: "Pilotrapporten mäter inte vem som inte kan boka digitalt". After: "Pilotrapporten från Lervik mäter inte vem som inte kan boka digitalt" — **change of taste.** Script: 56 characters before, 68 after, against the 70-character requirement; still conforming, with no entry in `failures` or `norms`. The heading already worked, the added "från Lervik" repeats the standfirst's opening two words ("Lerviks pilotrapport"), and it leaves two characters of headroom under the requirement.
3. **First paragraph of section 1.** Before: "Under de åtta veckorna gjordes 96 bokningar via webben och 24 via telefon i de två lokalerna." After: "Under åtta veckor i två lokaler gjordes 96 bokningar via webben och 24 via telefon." — **change of taste.** Both figures and the scope survive; the numbers now land at the end of the sentence, which reads better, but the definite "de åtta veckorna … de två lokalerna", which pointed back to the pilot the standfirst had already introduced, becomes indefinite and re-introduces the same pilot as if new. Script: 36 words before, 34 after; sentence estimate 3 in both.
4. **Section 2, first paragraph, clause removed.** Before: "Den är verklig och handlar om personalens arbetstid, inte om att de som ringer skulle vara lata eller dyra." After: "Den är verklig och handlar om personalens arbetstid." — **change to what a claim says (scope of the concession).** What goes is the explicit denial that the administration's objection rests on callers being lazy or costly. Script: that paragraph falls from 30 words to 19.

Nothing else moved: frontmatter, headline, standfirst, byline, the three remaining subheadings, all figures and the whole of sections 3 and 4 are byte-identical.

## 2. Headings

### Input

- `# Kommunstyrelsen bör pröva båda bokningsvägarna ett halvår` — **statement**. (Shares "ett halvår" with the standfirst's third sentence, but states the demand in its own clause rather than repeating the phrasing; not marked **echo**.)
- `## Pilotrapporten mäter inte vem som inte kan boka digitalt` — **statement**.
- `## Handlingarna saknar mätning av vad det dubbla arbetet kostar` — **statement**.
- `## Ett halvår med båda vägarna ger underlaget` — **statement**.
- `## Kommunstyrelsen kan pröva först och besluta sedan` — **statement**. (Opens on the same subject and modal as the first sentence under it, "Kommunstyrelsen kan säga ja till förslaget", but names a different thing; not marked **echo**.)

### Returned text

- `# Kommunstyrelsen bör pröva båda bokningsvägarna ett halvår` — **statement**. Unchanged.
- `## Pilotrapporten från Lervik mäter inte vem som inte kan boka digitalt` — **statement**, **echo**: "Pilotrapporten från Lervik" repeats the standfirst's opening words "Lerviks pilotrapport".
- `## Handlingarna saknar mätning av vad det dubbla arbetet kostar` — **statement**. Unchanged.
- `## Ett halvår med båda vägarna ger underlaget` — **statement**. Unchanged.
- `## Kommunstyrelsen kan pröva först och besluta sedan` — **statement**. Unchanged.

No heading in either text carries **colon**, **question** or **overclaim**. The single **echo** is one the Skill introduced while repairing a different one.

## 3. G1 — pass

The named reader is a Lervik resident, and the text does an opinion piece's job for that reader. It puts the position in the standfirst — "Öppna beslut vill se ett halvår med både telefon och webb, och siffror på hur lång tid varje bokningsväg tar" — and never drifts from it. The reader learns what the pilot did measure ("96 bokningar via webben och 24 via telefon"), what it did not ("Rapporten mäter inte heller ålder, funktionsförmåga eller digital vana"), what the handlingar lack ("varken en tidsmätning eller en ekonomisk besparingsberäkning finns i handlingarna"), and what the decision-maker may do instead. The angle — decide after measuring, not before — is recognisable in every section heading. The craft is that of a debattartikel: sharp on the decision basis, not on the people, and it concedes the other side's strongest point ("Den är verklig") before answering it.

## 4. G2 — pass

Every required part is present, in order, and each does its own job. Script, `anatomy-delivered.json`: `conforms: true`, `failures: []`, `norms: []`.

- **Headline**: 57 characters, 7 words — inside the 20–70-character requirement, and inside the ≤60-character, ≤8-word norm. It states the angle and is understood alone.
- **Standfirst**: 46 words, 1 paragraph — inside the 60-word requirement and the one-paragraph requirement. It stands alone: report, proposal and demand in three sentences.
- **Byline**: "Av Sanna Ek, talesperson för föreningen Öppna beslut" — the text names its own author, so the missing-byline report does not arise for a Redline run here.
- **Lead**: 43 words, 1 paragraph, before the first H2. It begins the work by naming the two missing items the body then supplies.
- **Sections**: four, each with at least one paragraph; subheadings at 68, 60, 42 and 49 characters, all inside the 70-character requirement; no heading level below the second (`other: []`).
- **Ending**: "Kommunstyrelsen kan säga ja till förslaget och stänga telefonbokningen i september. Den kan också låta båda vägarna stå kvar ett halvår…" meets the standfirst's expectation and calls for the stance the piece argued.

Opinion's own parts: the position is early (headline and standfirst); the support is the two named gaps; the relevant real objection is stated at its strongest and granted ("Förvaltningens invändning … är den dubbla administrationen. Den är verklig"); the call to action is a change with an identifiable actor — the kommunstyrelse running six months with both routes before deciding. Reservation, not a failure: the repaired lead no longer contains the word "förslag", so the ending's "säga ja till förslaget" now reaches back to the standfirst's "föreslås" rather than to the sentence before it. The chain holds, one link longer than it was.

## 5. P1 — pass

The reasoning is followable in one pass and each step is visible: the report counts bookings, not people, therefore it cannot say how many residents cannot book digitally ("Tjugofyra telefonbokningar kan vara tjugofyra invånare eller betydligt färre som ringt flera gånger"); the handlingar contain no time measurement, therefore the cost of the double route is unknown; therefore measure for six months and then decide. The transitions are real, not decorative — "Därför säger den ingenting om…", "Men varken en tidsmätning…". Municipal terms a resident may not use daily are placed in a sentence that explains them by their function: "Tjänsteutlåtandet inför kommunstyrelsens möte den 18 juni" tells the reader what kind of document it is and when it is decided.

Conclusions stay inside the visible support, and the text polices itself in both directions: "Den som vill använda telefonsiffran som bevis för att alla klarar webben har lika lite stöd i rapporten som den som hävdar motsatsen", and "Vi gör inget anspråk på att ha kostnadsberäknat eller finansierat försöket." The useful technical substance — the two counts, the four things the report does not measure, the two documents — survives the edit intact.

## 6. W1 — pass

A web reader can enter anywhere: four informative subheadings, each a statement of what its section shows. The counted requirements are met on the script's figures (`conforms: true`, `failures: []`), and no *should* was departed from (`norms: []`): the longest paragraph is 57 words against the 80-word norm; the longest section is three paragraphs against the three-paragraph norm; the headline is 57 characters and 7 words against 60 and 8; there is no heading below level two.

Standfirst and lead are now complementary rather than duplicative, which is this edit's main gain for the reader: the standfirst reports the pilot and states the demand, the lead names the decision and announces the two gaps. They open on different first words — "Lerviks" and "Tjänsteutlåtandet" — as they did before.

*Most* is read across the whole text and passes: the script counts 9 of 10 paragraphs at two or three sentences, and 3 of 4 sections at two or three paragraphs. The one-paragraph closing section and the one four-sentence paragraph are not failures.

No density or fragmentation loss: paragraph rhythm alternates long and short, and the section on what the report does not measure ends on a 29-word two-sentence paragraph that carries the piece's sharpest line.

## 7. L1 — pass

The prose is idiomatic Swedish debate writing, not translated English. Natural constructions throughout: "ska slippa föra in uppgifter i två flöden", "bör kunna svara på den frågan", "ta ställning till kostnaden", "motsätter oss att frågan avgörs innan de två uppgifterna ligger på bordet". Word order is Swedish where English would have pulled it straight: "Att en bokning går via telefon är inte ett bevis för att någon inte kan använda webben." The introduced clause "vill ha webben som enda bokningsväg till samtliga sju föreningslokaler" is idiomatic Swedish journalese — a document that "vill ha" something is standard in Swedish reporting — though "bokningsväg till … lokaler" is a fraction stiffer than the input's plainer verb. Not enough to disturb the voice, which is one voice from first line to last.

## 8. L2 — pass

Swedish locale mechanics hold. Date: "den 18 juni", Swedish form, no comma, lower-case month. Numerals: "96 bokningar", "24 via telefon", with "Tjugofyra telefonbokningar" spelled out at the start of a sentence as Swedish practice asks. Duration: "ett sex månader långt försök", "åtta veckor". No currency appears, and none was invented — the text says the cost is unknown rather than pricing it. Punctuation is Swedish: no Oxford comma, no English quotation marks, no en-dash-for-comma habit. Established variation in the input was preserved; the Skill's own account states the closing mechanical pass found no objective language errors to correct, and none is visible in the returned text.

## 9. T2 — skipped

No technique is named in the text's metadata or in the reply. The frontmatter says `technique: none`, and the reply confirms it: "Genre `opinion`, teknik `none` och språk `sv` lästes alla tre ur textens egen `kntnt`-karta". Nothing is judged under this criterion, and no technique is inferred from the shape of the prose.

## 10. R1 — pass

**Defects addressed.** One concrete visible defect was in the input and the Skill found it: the lead's first sentence repeated the standfirst's second sentence almost verbatim. That is a real reader loss — the first paragraph after the byline told the reader nothing the three lines above had not — and the repair removes it without touching the date, the seven venues or September.

**Preservation.** Voice, arguments, all figures, the headline, the standfirst, the byline and the frontmatter are byte-identical. The Ek position that the source material marked as quotable survives word for word as prose: "Att en bokning går via telefon är inte ett bevis för att någon inte kan använda webben. Det är ett skäl att ta reda på varför telefonen fortfarande används." The self-limiting sentence "Vi gör inget anspråk på att ha kostnadsberäknat eller finansierat försöket" is untouched. No anatomy count was worsened: the script reports `conforms: true`, `failures: []`, `norms: []` for both texts, so no finding was made against a requirement the text met, none against a *should* the text had reason to leave, and none against a *most* read at a single paragraph or section — the three failure modes this criterion names are all absent.

**Every removal and every changed claim, against the account.**

- *Removal of ", inte om att de som ringer skulle vara lata eller dyra."* — **reported, and reported accurately.** The account quotes the sentence before and after, names exactly what disappeared ("påståendet att förvaltningens invändning inte handlar om att de som ringer skulle vara lata eller dyra"), and gives the reason: nobody in the text is credited with that view, so the clause denies an accusation the text never contains. That is a defensible finding — introducing an idea only to deny it is a real weakness. The account's closing claim about it, "Texten avgränsar därmed sina anspråk precis lika långt som förut", is the one place where it overstates: the clause did work the remaining half-sentence does not do, namely keeping a sharp criticism of the decision basis from reading as an imputation against staff. The removal is reported; its cost is understated by one sentence.
- *Changed claim in the lead, "föreslår" → "vill ha".* — **reported, and reported accurately, including against itself.** The account quotes both versions, names the shift as a moved speech act, lists what survived (source, date, seven venues, September), says where the removed content now first appears ("tar bort en bokningsväg i sju lokaler", "stänga telefonbokningen i september"), and hands the user the residual risk unprompted: "Om 'föreslår' ska tillbaka är en avvägning för dig: det är det ord ett tjänsteutlåtande handlar med, och avslutningens 'säga ja till förslaget' syftar tillbaka på det." That is the reporting this criterion asks for, and the piece of it the Skill was least obliged to volunteer.

**Visible defects not addressed.** One: the repair introduced a new heading echo. "Pilotrapporten från Lervik" now repeats the standfirst's opening "Lerviks pilotrapport", and the re-review reported no findings left ("omgranskningen av den korrigerade texten lämnade inga fynd kvar"), so the Skill's own second pass missed a defect of exactly the kind its first pass caught. Minor in effect, but it is the same defect class.

**Changes of taste to passages that already worked.** Two, items 2 and 3 in the Changes list. Neither damages the text: one costs two characters of headroom under the 70-character requirement (68 on the script's count) and adds the echo above; the other trades a working anaphoric link back to the standfirst for better end-of-sentence emphasis. Both are small, and both are undisclosed — the account's change section is headed "Påståenden som togs bort eller ändrades" and covers claims only, and the statement "Samtliga siffror står kvar som de stod, liksom rubriken, ingressen, bylinen och frontmattern" is true but says nothing about the subheading or the section-1 opening. A user comparing the two files finds two edits the account never mentions. The account also says three findings were noted and all three repaired without listing them one by one, so the reader cannot map four textual changes onto three findings.

**Verdict.** Pass. A genuine defect was found and repaired, the returned text conforms on every counted requirement and departs from no norm, voice and arguments and figures and quotations are preserved, and both the removal and the changed claim are reported with their trade-offs handed back to the user. Against that: two unreported taste edits, a new echo the re-review declared clean, and one understated cost. None of the protocol's five unconditional rejections is triggered — no unsupported fact was introduced, the locale is right, no substantive editing was done under a mechanical heading, no finding was left unresolved and unreported, and the reply states that nothing was written to the filesystem. The text is delivered with no remaining quality problem reported as irreparable.

## 11. Source loss

*Separate from every criterion above: the Skill never saw `write/work/source.md` and could not have known any of this.*

**Yes — one change removed a careful formulation the source required.**

The source states the boundary explicitly, as part of the material and not as an optional colour:

> "Förvaltningens verkliga invändning mot att behålla båda kanalerna är dubbel administration, inte att telefonanvändare är lata eller dyra."

and the judging boundaries repeat the intent: "Författaren ska kunna kritisera beslutsunderlaget skarpt utan falska motiv eller tandlös neutralisering."

The change that removed it:

> Before: "Den är verklig och handlar om personalens arbetstid, inte om att de som ringer skulle vara lata eller dyra."
> After: "Den är verklig och handlar om personalens arbetstid."

The source's sentence is built on a contrast, and the negative half is the half that does the work: it is the source's own guard against attributing a false motive to the administration. The input had carried it across faithfully. The returned text keeps the positive half and drops the guard, so the one place where the source insisted on saying what is *not* being claimed no longer says it.

Two lesser source points survive the edit and are worth recording as intact: the seven venues, the 18 June meeting and both booking counts are unchanged, and the source's requirement that "Kostnaden behöver kommunstyrelsen ta ställning till" with "kostnadsosäkerheten bevarad" is still carried word-perfectly by "Vad ett halvår med båda vägarna kostar måste kommunstyrelsen ta ställning till." No other source caveat, limit or careful formulation was touched.
