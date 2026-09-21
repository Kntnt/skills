# Judgement A — opinion-sv-r2 / write

Genre: `opinion` (frontmatter `genre: opinion`, brief: "Skriv en debattartikel"). The four-genre anatomy therefore applies in full; the scale is not advisory here.

## 1. Outcome

**Delivered.** `response.md` opens "Utkastet levereras i svaret" and carries the complete draft in a fenced block; `delivered.md` is that draft.

**Two source comparisons completed.** `evidence/` holds two full comparison sets, `source-check/` and `source-check-2/`, each with its own `prompt.txt`, `material.md`, `claims.md`, `prose.md` and `report.md`. The two prompts are identical but for their directory names, so the second was a fresh comparison of the same kind, not a continuation. Report 1 ends "**Unresolved findings: 4** … no repair has been applied"; report 2 ends "**Source-support findings: none. Translation findings: none. Unresolved findings: none.**" The delivery account says the same: "Två jämförelser mot underlaget genomfördes, båda av en ny granskare utan samtalshistorik."

**The delivered prose is byte-identical to the last prose a checker saw.** `diff source-check-2/prose.md delivered.md` is empty, as is `diff source-check-2/prose.md evidence/draft-final.md`. The only changes anywhere are the five edits between `source-check/prose.md` and `source-check-2/prose.md` — the four repairs of report 1's findings plus the tightened third subheading — all of them made *before* the second comparison. Nothing in the dispositions or the reply claims an edit after it; the reply states "Texten är levererad exakt som den jämförelsen läste den", and the diff bears that out.

One inaccuracy in the account, noted but not scored: after listing four bullets it introduces the subheading question as "En fjärde punkt", when the bullets already number four. The substance of what it reports is correct.

## 2. Headings

- `# Kommunstyrelsen bör pröva båda bokningsvägarna ett halvår` — **statement**
- `## Pilotrapporten mäter inte vem som inte kan boka digitalt` — **statement**
- `## Handlingarna saknar mätning av vad det dubbla arbetet kostar` — **statement**
- `## Ett halvår med båda vägarna ger underlaget` — **statement**
- `## Kommunstyrelsen kan pröva först och besluta sedan` — **statement**

No colon, question, echo or overclaim mark was earned, but three near misses are recorded so the marking is not read as blanket approval:

- The headline and the standfirst's third sentence ("Öppna beslut vill se ett halvår med både telefon och webb") share *ett halvår* and the two-route content. I do not mark **echo**: the subject differs (kommunstyrelsen's duty vs the association's wish), and the standfirst sentence adds the time-measurement demand the headline does not carry.
- `Ett halvår med båda vägarna ger underlaget` was tested hardest for **overclaim**. It asserts that the proposed trial yields the decision basis while the body keeps the cost question open ("Vad ett halvår med båda vägarna kostar måste kommunstyrelsen ta ställning till") and keeps the users' reasons voluntary. The material carries the same proposition at the same standpoint strength — "Därefter kan den avgöra om en kanal ska tas bort, ändras eller behållas" — and the qualification sits in the paragraph directly beneath the heading, so the heading does not claim more than the text claims. No mark.
- `Kommunstyrelsen kan pröva först och besluta sedan` shares the opening words "Kommunstyrelsen kan" with the first sentence under it. Two function words of overlap with wholly different predicates is not a repetition of phrasing; no **echo** mark. It is a rhythm observation, taken up under W1.

## 3. F1 — pass

Every assertion in the delivered text pairs with a supplied passage at the material's own scope, modality and certainty, and every passage without one is the bylined author's own advocacy resting on a supported absence. I checked the whole text against `work/source.md` myself rather than accepting either report.

The load-bearing pairings:

- "Under de åtta veckorna gjordes 96 bokningar via webben och 24 via telefon i de två lokalerna" ← "Under försöket gjordes 96 bokningar via webb och 24 via telefon" plus "ett åtta veckor långt försök i två lokaler". Figures, channels, period and site count unchanged; no count is characterised as high or low, so no supplied comparison is needed. The brief's requirement that figures be attributed to the report ("Siffror ska tillskrivas rapporten där de bär argumentet") is met by the section heading "Pilotrapporten" and the next sentence "Rapporten räknar bokningar, inte unika personer", which is verbatim.
- "Tjugofyra telefonbokningar kan vara tjugofyra invånare eller betydligt färre som ringt flera gånger" — the modal *kan vara* leaves both ends open and asserts neither, which is exactly the state the material leaves ("Rapporten räknar bokningar, inte unika personer"). No share of residents is asserted anywhere, which is what the material forbids.
- "Men varken en tidsmätning eller en ekonomisk besparingsberäkning finns i handlingarna" ← "Någon tidsmätning eller ekonomisk besparingsberäkning finns inte i handlingarna". The scope *i handlingarna* is preserved here and in the subheading above it, which the first comparison had found widened to the world ("Ingen har mätt") and which the repair fixed.
- "Vi gör inget anspråk på att ha kostnadsberäknat eller finansierat försöket" ← "Föreningen gör inget anspråk på att ha finansierat eller kostnadsberäknat försöket". Unclaimed stays unclaimed; the earlier draft's flat negative is gone. "Vad ett halvår med båda vägarna kostar måste kommunstyrelsen ta ställning till" ← "Kostnaden behöver kommunstyrelsen ta ställning till", with no figure, range or direction — the boundary "med kostnadsosäkerheten bevarad" holds to the last section.
- "Förvaltningens invändning … är den dubbla administrationen. Den är verklig och handlar om personalens arbetstid, inte om att de som ringer skulle vara lata eller dyra" ← "Förvaltningens verkliga invändning mot att behålla båda kanalerna är dubbel administration, inte att telefonanvändare är lata eller dyra", with *personalens arbetstid* resting on "personalen ska slippa föra in uppgifter i två flöden" and on the author's own "arbetskostnaden". No magnitude is asserted, and the counterfactual *skulle vara* keeps the lazy/expensive motive a denial rather than an imputation — the boundary "utan falska motiv" holds, and the concession keeps the criticism from being toothless.
- "Att en bokning går via telefon är inte ett bevis …" is word-for-word Sanna Ek's supplied ståndpunkt, which "får citeras eller refereras", set unquoted in the article she is bylined for, so no one else's words are absorbed.
- The ending names the board's options — approve and close in September, or keep both routes for six months, settle the cost, then remove, change or keep a channel — all of which are the material's own ("Därefter kan den avgöra om en kanal ska tas bort, ändras eller behållas").

Boundary check: no lagkrav, no protest, no diskrimineringsfall, no party-political motive and no saving is asserted anywhere; "Den som vill använda telefonsiffran som bevis …" is a generic *den som*, so no actual party is credited with an argument the material does not give it. No source, study, date or figure beyond the supplied ones appears; the report's date, 8 april 2026, is omitted, which narrows nothing.

Three passages I tested in both directions and did not score as defects, each named so the pass is not mistaken for a blanket one:

1. **"räknar bokningar, inte människor"** (standfirst) for "räknar bokningar, inte unika personer". A report that carried some non-unique headcount would satisfy the source and fail the draft. The material's account of the report has no room for a second tally — the only counts it reports are the 96/24 split of the same bookings — and the exact form is restored verbatim in the body two paragraphs later, with the whole next sentence unpacking it. Compression inside the article's own explanation, not a changed claim.
2. **"Under försöket registrerar förvaltningen tidsåtgången …"** for the material's deontic "ska förvaltningen registrera". The governing clause is "Öppna beslut föreslår ett sex månader långt försök", and *Under försöket* refers to a trial that does not exist, so the present tense states the proposal's content rather than a practice. *Frivilligt* — the qualification that limits what the trial can deliver — is carried over intact.
3. **"Öppna beslut motsätter sig inte digital bokning"** for "Hon motsätter sig inte digital bokning". The subject moves from the spokesperson to the association. The association's own supplied proposal keeps the web route in all seven lokaler and hands the board the choice to remove, change or keep a channel, so the material carries the association's non-opposition independently of her personal view.

Unknown is kept apart from absent throughout: the text says what the report does not measure and what the documents do not contain, never that the underlying facts do not exist.

## 4. G1 — pass

The genre does its job for the named reader, the residents of Lervik. A resident learns what is on the table (phone booking removed in all seven lokaler from September), what the evidence behind it is and is not (eight weeks, two lokaler, 96 web and 24 phone bookings, bookings rather than unique persons, no measurement of age, ability or digital habit), what the documents lack (no time measurement, no savings calculation), and what the board can do instead. The angle is recognisable and held from the headline to the last sentence: decide later, measure first.

The craft the brief asked for is there. It is sharp on the decision basis — "Ett förslag som tar bort en bokningsväg i sju lokaler bör kunna svara på den frågan" — without inventing a motive, and it concedes the administration's real objection in its own voice: "Den är verklig och handlar om personalens arbetstid". The symmetry in "har lika lite stöd i rapporten som den som hävdar motsatsen" refuses the easy advocacy of claiming the 24 calls prove exclusion, which is the intellectually honest move the material demands. There is no commercial CTA, as the brief required.

The brief's "ungefär 400 ord" is not measured by the script, which reports only per-part counts; I record it as not measured rather than producing a figure.

## 5. G2 — pass

The parts appear in the anatomy's order and each does its own job. The script reports `"conforms": true`, `"failures": []` and `"norms": []`.

Counted requirements, all from the script:

- Headline: `"characters": 57`, inside 20–70. (`"words": 7`, so the *should* of at most eight words and 60 characters is met as well.)
- Standfirst: `"words": 46`, at most 60; `"paragraphs": 1`.
- Lead: `"paragraphs": 1`, and the script places it as the `lead` part, so it stands before the first H2.
- Subheadings: `56`, `60`, `42` and `49` characters, all at most 70.
- Sections: `"sections": 4`, with paragraph lists of 3, 2, 2 and 1 — every section has at least one paragraph.

The jobs, not just the counts. The standfirst stands alone: it gives the report's basis, the proposal on the table and what the association wants, without depending on the headline. The lead begins the work rather than repeating the standfirst — it names the tjänsteutlåtande, its stated motive, and sets the two-missing-items frame the body then fills. The body explains rather than asserts, one section per missing item and one for the proposal. The ending meets the lead's expectation exactly: the lead promises "två uppgifter som borde ligga på kommunstyrelsens bord saknas i handlingarna" and the close returns to it — "Vi motsätter oss att frågan avgörs innan de två uppgifterna ligger på bordet."

The byline reads "Av Sanna Ek, talesperson för föreningen Öppna beslut" (script: `"words": 8`), which is the author the brief names ("Avsändare är Sanna Ek, talesperson för föreningen Öppna beslut"). The delivery account identifies her as the author — "hon är artikelns författare" — though it never states in so many words where the byline came from; the substance of the requirement is met and I do not fail it on that phrasing.

Opinion's own parts: the position is early (headline and standfirst both state it, before any argument); the support is the report's limits and the documents' gaps; a relevant real objection is met head-on rather than strawmanned ("Förvaltningens invändning … Den är verklig"); and the call to action is the stance itself with an identifiable actor — "Den kan också låta båda vägarna stå kvar ett halvår, ta ställning till kostnaden och sedan avgöra …", addressed to the kommunstyrelse.

## 6. P1 — pass

A Lervik resident can follow this. Each unfamiliar object is introduced before it is used: "Lerviks pilotrapport" with its span and scope in the standfirst; "Tjänsteutlåtandet inför kommunstyrelsens möte den 18 juni" with its proposal and motive in the lead; "handlingarna" only after the documents it names have been introduced. The transitions are real and carry argument rather than decoration — *Ändå* against the proposal, *Därför* from the unmeasured variables to what the report cannot say, *Men* from the conceded objection to the missing measurement.

Conclusions stay proportionate to visible support. From "Rapporten räknar bokningar, inte unika personer" the text draws only "kan vara tjugofyra invånare eller betydligt färre"; from the absent measurements only "säger den ingenting om hur stor andel", not a claim about how many residents need the phone. The technical substance a reader needs survives: the 96/24 split, eight weeks, two lokaler against seven, the 18 June meeting, September, and the distinction between a booking count and a person count.

One qualitative concern, not a failure: *uppgifter* carries two senses in adjacent sentences of the lead — data entered in two flows, then the two missing items ("Motivet är att personalen ska slippa föra in uppgifter i två flöden. Men två uppgifter som borde ligga på kommunstyrelsens bord saknas i handlingarna"). The second sense is recoverable from "saknas i handlingarna" and from the ending's "ligger på bordet", so the reader is delayed rather than lost.

## 7. W1 — pass

A web reader can orient and enter. The four subheadings are informative statements that say what their sections hold, so the piece scans, and the explanation still runs continuously from one to the next because each section ends on the argument the following heading picks up.

The counted and near-counted lines, all from the script:

- No norm departure is recorded at all: `"norms": []`. So no paragraph runs over 80 words (the longest the script reports is `"words": 57`), no heading sits below the second level, and the headline is inside eight words and 60 characters at `"words": 7` and `"characters": 57`.
- *Most* read across the whole text, as it must be: `"paragraphs": 10` with `"paragraphs_of_two_or_three_sentences": 9`, and `"sections": 4` with `"sections_of_two_or_three_paragraphs": 3`. Both hold across the text. The one paragraph outside the range (`"words": 57, "sentences_estimate": 4`) is the closing paragraph, and the one section outside it is the closing section of a single paragraph — neither is failed on its own, and a short closing section that lists the board's options in one breath reads better than the same material split.
- Standfirst and lead open on different first words: "Lerviks" against "Tjänsteutlåtandet".

Standfirst and lead are complementary rather than duplicative — the standfirst carries the evidence and the ask, the lead carries the document and its motive — and the body covers everything the standfirst promises: the eight weeks and two lokaler (section 1), the seven lokaler from September (lead), the half-year with both routes and the time figures (section 3). No density or fragmentation loss: paragraphs are single-topic, and the only repetition of phrasing is the "Kommunstyrelsen kan" that opens both the last heading and the sentence under it, which is a small rhythm blemish, not reader loss.

## 8. L1 — pass

The prose reads as professionally written Swedish. The idiom is native throughout and the syntax is Swedish, not translated: "slippa föra in uppgifter i två flöden", "ligger på bordet", "ta ställning till", "på dagens underlag", "bör kunna svara på den frågan". The register is that of a Swedish debattartikel — nominal where the subject is administrative, plain where the argument turns. Sentence openings vary and the verbs carry the work ("gjordes", "mäter", "saknas", "vägas"). No generic-translation tells: no stacked hedges, no "det är viktigt att notera", no English clause order or calqued connective. The one rhetorical set piece, "har lika lite stöd i rapporten som den som hävdar motsatsen", is idiomatic Swedish comparison.

## 9. L2 — pass

The resolved locale is `sv` (frontmatter `language: sv`; brief: source language Swedish) and it governs throughout. Month names are lower case in the Swedish manner — "den 18 juni", "från september", "i september" — and the date form is the Swedish "den 18 juni", with no year invented where the material gives none. Numerals follow Swedish practice: figures for the data ("96 bokningar", "24 via telefon") and a spelled-out "Tjugofyra" at the start of a sentence. Spelling and compounding are Swedish and consistent ("bokningsvägarna", "tjänsteutlåtandet", "besparingsberäkning", "funktionsförmåga"). No currency appears anywhere, so no conversion could be and none was invented; no decimal or thousands separator is in play. No quotation marks are used, so no locale quotation form is at issue.

## 10. T2 — skipped

T2 — skipped — no technique is named in the text's metadata or in the reply. The frontmatter reads `technique: none`, and the delivery account states "Ingen teknik är upplöst". Nothing is judged under this criterion, and no technique is inferred from the shape of the prose.

## 11. Checker findings

### `evidence/source-check/report.md` (first comparison) — four findings

| # | Draft passage | Checker's allegation | Writer's disposition | My class |
|---|---|---|---|---|
| 1 | `## Ingen har mätt vad det dubbla arbetet kostar` | Scope: widens "finns inte i handlingarna" from one document set to the world | Repaired to `## Handlingarna saknar mätning av vad det dubbla arbetet kostar` (the checker's own smallest repair) | **supported** — the material scopes the absence explicitly with *i handlingarna* and never says no measurement exists anywhere; the draft's own body already had the correct scope |
| 2 | "Vi har inte kostnadsberäknat försöket och gör inget anspråk på att ha finansierat det." | State of knowledge: turns "gör inget anspråk på att ha … kostnadsberäknat" into a negative fact | Repaired to "Vi gör inget anspråk på att ha kostnadsberäknat eller finansierat försöket." | **supported** — the material records an unclaimed, not a non-event, and the sentence's own financing half showed the asymmetry |
| 3 | "…, och siffror på vad varje bokningsväg kostar." (standfirst) | The thing measured: the proposal asks for *tidsåtgång per bokningsväg*; cost is what the board must take a position on | Repaired to "…, och siffror på hur lång tid varje bokningsväg tar." | **supported** — the supplied proposal names only time registration, and the draft's own body kept cost with the kommunstyrelse, so the standfirst was making a demand the article did not make |
| 4 | "Rapporten är tydlig med vad siffrorna är: bokningar, inte unika personer." | Attribution: credits the report with an explicitness the material does not establish | Repaired to "Rapporten räknar bokningar, inte unika personer." | **supported** — the material says what the report counts, never what it discloses about its own unit |

The same report's §5 records three items expressly as editorial questions rather than findings; they are listed here for completeness:

| Item | Checker's note | Writer's disposition | My class |
|---|---|---|---|
| `## Sex månader med båda vägarna ger svaren` | Read as a prediction it outruns the material's *frivilligt*; read as advocacy it is the party's own standpoint — "genuinely unsettled" | Tightened anyway to `## Ett halvår med båda vägarna ger underlaget`, the checker's suggested wording | **disputed** — the material settles neither reading; the voluntary limb leaves the prediction reading open, and the standpoint reading is equally available |
| "räknar bokningar, inte människor" (standfirst) | Contrast term is not the material's word; judged defensible | Left as written | **disputed** — the material leaves a second, non-unique tally formally open while giving it no room; see F1 |
| Omitted report title/date, omitted *först*, the two senses of *uppgifter* | Recorded as not findings (omissions and wording) | Left as written | **false** for the two omissions, which change no claim; **disputed** for the *uppgifter* ambiguity, which is a clarity matter the material cannot settle |

### `evidence/source-check-2/report.md` (second comparison) — no findings

The report states "**Findings: None.**" and "**Source-support findings: none. Translation findings: none. Unresolved findings: none.**" It records six passages tested in both directions and set aside (§3.1–§3.6: the *människor* compression, "säger den ingenting", "handlar om personalens arbetstid", the `ger underlaget` heading, "tjugofyra invånare", and the two passive agents). There is no finding line to write for any of them, and none is claimed as a defect.

### Did a checker miss a real defect?

No. I found no defect under F1. The three passages I tested hardest — the *människor* compression, the present-tense "registrerar", and "Öppna beslut motsätter sig inte digital bokning" — were all seen: the first by both comparisons, the other two by the second (§T2 and §C3). Nothing I would have scored went unseen.

## 12. Remaining findings

**None.** The delivery account reports no unrepaired finding: "Den andra och slutgiltiga jämförelsen läste den lagade texten och rapporterade inga kvarstående invändningar, varken om källstöd eller om översättning. Texten är levererad exakt som den jämförelsen läste den." That matches `source-check-2/report.md`, and my own reading under F1 finds no defect the account should have reported.

The account's "Där materialet tar slut" section lists three things the text cannot say — how many residents need the phone, what the double work costs, what the association's own trial costs — and names what would close each gap. These are limits of the supplied material honoured by the text, not findings against it; nothing in them is a passage where the text says more than the material carries.

## 13. Class of the run

**`valid delivery`.** The prose that was delivered had a completed comparison of its own — `source-check-2` read `prose.md` byte-for-byte identical to `delivered.md` and reported no finding — and no edit was made after it, so nothing was delivered uncompared and nothing compared was withheld. Every criterion applicable to this run passes, T2 is skipped for want of a selected technique, and none of the protocol's five unconditional rejections is triggered: no unsupported fact, the locale is Swedish throughout, no mechanical editing substituted for the writer's own repairs, no finding was left unreported, and the account's only side effects are the two the observer made.
