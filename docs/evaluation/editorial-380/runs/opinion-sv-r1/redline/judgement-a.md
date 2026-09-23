# Judgement A — opinion-sv-r1 / redline

Genre from the text's own `kntnt` block: `opinion` — one of the four article genres, so the anatomy's skeleton applies and its counted requirements are judged on the script's figures. `technique: none`.

## 1. Changes

Three differences between `redline/work/input.md` and `redline/delivered.md`. Nothing was removed.

1. Standfirst, last sentence — before: "Öppna beslut vill att kommunstyrelsen prövar båda vägarna ett halvår först." / after: "Föreningen Öppna beslut vill att kommunstyrelsen prövar båda vägarna ett halvår först." — **repair of a visible defect**: the standfirst must stand alone, and "Öppna beslut" unprefixed reads as a common-noun phrase ("open decisions") on first encounter; the added "Föreningen" fixes the referent. The claim itself is untouched. Standfirst words 42 → 43 (`anatomy-input.json` `parts.standfirst.words` 42; `anatomy-delivered.json` 43), both far inside the 60-word requirement.
2. First paragraph of section 1 — before: "Under åtta veckor prövades bara två av de sju lokalerna." / after: "Förslaget vilar på ett försök där bara två av de sju lokalerna prövades under åtta veckor." — **repair of a visible defect**: the section opened with a bare restatement and no transition from the lead; the new opening names what the figures bear on. It is also the weakest of the three, because it now reproduces the standfirst's "Bakom förslaget ligger åtta veckors försök i två av sju lokaler" more closely than the sentence it replaced. Paragraph words 29 → 35 (`parts.sections[0].paragraphs[0].words`), sentences 2 → 2; no norm is crossed (`norms: []` in both files).
3. Subheading of section 2 — before: "Invändningen är verklig, men handlingarna saknar siffror" / after: "Dubbelarbetet är verkligt, men handlingarna saknar siffror" — **repair of a visible defect, and a change to what the claim's subject is**: a subheading must be understood on its own, and "Invändningen" has no antecedent for a reader who arrives at the H2 (the objection is named only in the sentence below it). Naming it "Dubbelarbetet" makes the heading self-contained. The predicate's strength is unchanged ("är verklig" → "är verkligt"), but the thing asserted to be real moves from the objection to the double entry itself. Subheading characters 56 → 58 (`parts.sections[1].subheading.characters`), inside the 70-character requirement; words 7, inside the eight-word norm.

No change of taste, no mechanical-only correction, no removal, no reordering, no metadata edit.

## 2. Headings

**Input** (`redline/work/input.md`)

- H1 "Underlaget räcker inte för att stänga telefonbokningen" — statement
- H2 "Siffrorna räknar bokningar, inte människor" — statement
- H2 "Invändningen är verklig, men handlingarna saknar siffror" — statement, overclaim (mild: the text says only "Den invändningen tar vi på allvar", a lower strength than asserting the objection is real)
- H2 "Ett halvår med mätning ger kommunstyrelsen underlag" — statement
- H2 "Mät först, besluta sedan" — statement

**Returned text** (`redline/delivered.md`)

- H1 "Underlaget räcker inte för att stänga telefonbokningen" — statement
- H2 "Siffrorna räknar bokningar, inte människor" — statement
- H2 "Dubbelarbetet är verkligt, men handlingarna saknar siffror" — statement, overclaim (mild: the section reports the double entry as the *motive stated in the tjänsteutlåtande* and says the writers take it seriously; it does not itself assert the double work is real)
- H2 "Ett halvår med mätning ger kommunstyrelsen underlag" — statement
- H2 "Mät först, besluta sedan" — statement

No colon, question or echo mark applies anywhere. Two near-repetitions fall outside the echo definition and are noted as evidence, not as labels: section 1's subheading is repeated almost verbatim by its *second* paragraph ("Rapporten räknar bokningar, inte unika personer"), and the closing subheading by its *second* paragraph ("Men mät först"); the echo mark is defined against the standfirst and the first sentence under the subheading, and neither first sentence repeats its heading.

## 3. G1 — pass

The genre does an opinion piece's job for a Lervik resident reading a local debate page. The reader gets the position within the lead — "Vi i föreningen Öppna beslut menar att beslutet kommer för tidigt. Inte för att digital bokning är fel, utan för att underlaget inte visar vad bytet är värt" — and a single angle held to the end: the decision basis, not digital booking, is what is being attacked. The craft is the journalistic kind the genre asks for: figures attributed to their document ("Kommunens rapport *Bokning av föreningslokaler* från den 8 april 2026 redovisar 96 bokningar via webben och 24 via telefon"), the opposing motive stated in its own terms before it is answered, and a self-imposed limit ("Öppna beslut gör inget anspråk på att ha kostnadsberäknat eller finansierat försöket"). The reader can act: tell the kommunstyrelsen, before 18 June, to keep both routes for a six-month measured trial.

## 4. G2 — pass

The parts appear in the anatomy's order and each does its own job; `anatomy-delivered.json` reports `conforms: true`, `failures: []`.

- Headline: "Underlaget räcker inte för att stänga telefonbokningen", 54 characters, 7 words (`parts.headline`) — inside the 20–70-character requirement and the eight-word norm, and it states the angle rather than labelling the topic.
- Standfirst: 42 → 43 words, 1 paragraph (`parts.standfirst.words`, `.paragraphs`) — inside the 60-word requirement and the one-paragraph requirement, and after change 1 it stands alone: the proposal, its evidentiary base, what the documents lack, and who wants what instead.
- Byline: "Av Sanna Ek, talesperson för föreningen Öppna beslut" — present and filled, so the missing-byline report does not arise.
- Lead: 1 paragraph, 49 words (`parts.lead`), placed before the first H2, and it begins the work by fixing the date, the decision and the position.
- Sections: four, each with two or three paragraphs and at least one (`parts.sections`), all four subheadings inside the 70-character requirement (42, 58, 51, 24).
- Ending: "Men mät först. Låt telefonbokningen vara kvar under försöket, och avgör därefter om en bokningsväg ska tas bort, ändras eller behållas" — the change asked for is the call to action, and it meets the lead's expectation that the decision is premature.

Opinion's four demands are met: the position is early (lead), the support is sections 1 and 3, the real objection is faced rather than straw-manned ("Motivet i tjänsteutlåtandet är att personalen ska slippa föra in uppgifter i två flöden. Den invändningen tar vi på allvar"), and the actor is identifiable — kommunstyrelsen i Lervik, meeting 18 June. No commercial call to action intrudes.

The one qualitative concern, not a failure: the returned subheading "Dubbelarbetet är verkligt" asserts as the text's own what the body attributes to the tjänsteutlåtande and merely takes seriously. It is a small strength gap, no larger than the one it replaced, and the body immediately supplies the qualification.

## 5. P1 — pass

Judged on the returned text alone. The chain is followable in one pass: only two of seven rooms were tried, for eight weeks; the report counts bookings rather than people and measures no age, ability or digital habit; therefore the phone figure cannot carry the share of residents who cannot book online. The conclusion is kept to the size of the support — "Telefonsiffran säger därför ingenting om hur stor andel av invånarna som kan eller inte kan boka digitalt", and, on the other side, "Att en bokning går via telefon är inte ett bevis för att någon inte kan använda webben. Det är ett skäl att ta reda på varför telefonen fortfarande används." Municipal terms a resident may not hold — tjänsteutlåtande, kommunstyrelsen — arrive in contexts that say what they are (a document containing figures; a body that meets on 18 June and is asked to decide). Transitions are real, not decorative: "Men handlingarna innehåller varken tidsmätning eller beräkning…" turns the conceded objection into the argument's next step. The technical substance that matters — what the report measures and what it does not — survives intact.

## 6. W1 — pass

`anatomy-delivered.json` reports `conforms: true`, `failures: []`, `norms: []`, so no requirement is missed and no *should* is departed from: no paragraph over 80 words, no section over three paragraphs, no heading below level two, the headline at 54 characters and 7 words. `typical` gives 10 of 11 paragraphs at two or three sentences and 4 of 4 sections at two or three paragraphs — read across the whole text, both are comfortably typical, and the one longer paragraph is not a failure.

Standfirst and lead complement rather than duplicate: the standfirst covers the proposal, the eight-week base, the missing measurements and the counter-proposal, and every one of those is carried out in the body, so the body is complete when the standfirst is. They open on different first words — "Från" against "Den". The four subheadings are informative statements a scanner can navigate by, and after change 3 each is intelligible without reading down into its section.

One reader cost, named and not a failure: change 2 made section 1's opening sentence restate the standfirst's third clause more closely than before, so a reader moving from standfirst to section 1 meets "åtta veckor" and "två av de sju lokalerna" a second time within a few lines. The rest of the paragraph then adds the report's figures, so nothing is lost, only briefly repeated.

## 7. L1 — pass

The Swedish reads as written in Swedish, not translated into it. Idiom and syntax are native throughout: "Öppna beslut föreslår i stället sex månaders försök", "den som bokar får frivilligt ange varför valet blev telefon eller webb", "det är hela poängen". The register is the Swedish debate page's — short declaratives, a conceding "Den invändningen tar vi på allvar", an imperative close. The one rewritten sentence keeps that register: "Förslaget vilar på ett försök där bara två av de sju lokalerna prövades under åtta veckor" uses ordinary Swedish word order with the fronted subject and the passive "prövades", with no English calque. Institutional vocabulary is the real Swedish municipal kind — tjänsteutlåtande, handlingar, förvaltningen, bokningsväg — rather than glossed approximations.

## 8. L2 — pass

Resolved locale `sv`, and the mechanics follow it. Dates are Swedish-formed with lower-case months and no ordinal: "Den 18 juni", "den 8 april 2026". Numbers are plain and unseparated at this magnitude: "96 bokningar", "24 via telefon", "sju lokaler", "åtta veckors försök", "sex månaders försök". Compounds are closed as Swedish requires — "tjänsteutlåtandet", "besparingsberäkning", "bokningsvägarna", "kommunstyrelsen", and in the returned text "Dubbelarbetet". Emphasis on the report title uses Markdown italics, not quotation marks, so no quote-mark form is at issue. No currency figure appears, and no change introduced a date or a conversion that was not already there.

## 9. T2 — skipped

No technique is named in the text's metadata or in the reply: the returned text's `kntnt` block reads `technique: none`, and the reply states "**utan teknik** … `none` där är ett val och ingen lucka: genrens vanliga berättelsebåge har alltså inte tillämpats". Nothing is judged under this criterion, and no technique is inferred from the prose.

## 10. R1 — pass

**Defects addressed.** All three changes hit a visible defect rather than taste, and each is the kind the anatomy names: a standfirst that must stand alone but left "Öppna beslut" without its noun; a section opening that restated without transition; a subheading whose subject existed only below it. None of the three was made against a requirement the text already met — the script reports `conforms: true` and `failures: []` for the input too, and the Skill correctly did not manufacture a counted failure where none existed. None was made against a *most* read at a single paragraph or section, and none against a *should* the text had reason to leave: `norms: []` in `anatomy-input.json`.

**Preservation.** Nothing was removed. The quoted position survives verbatim — "Att en bokning går via telefon är inte ett bevis för att någon inte kan använda webben. Det är ett skäl att ta reda på varför telefonen fortfarande används." Every figure is unchanged (96, 24, eight weeks, two of seven, six months, 18 June, 8 April 2026), as are the report title, the byline, the metadata block, the section order and the closing call. The voice — conceding, dry, unhedged — is the same voice on both sides of the review.

**Every changed claim, against the account.** The reply's account is: "Granskningen gav tre fynd. En korrigeringsrunda reparerade alla tre, omgranskningen lämnade inga fynd kvar, och den avslutande mekaniska genomgången hittade inget att rätta."

- Change 1 (added "Föreningen"): claim unchanged, referent clarified. The account reports a count, not this finding. Accurate as far as it goes, and there is nothing here a reader would need to check.
- Change 2 (section 1 opening rewritten): no claim added that the text does not already carry — the standfirst already says "Bakom förslaget ligger åtta veckors försök i två av sju lokaler". The account does not name it.
- Change 3 (subheading subject moved from "Invändningen" to "Dubbelarbetet"): this is a change to what the claim is about, and it is the one change a reader would want reported, because it puts a proposition in the Skill's words that the body attributes to the tjänsteutlåtande. The account does not name it.

**The reporting gap.** The account states how many findings there were and that all were repaired; it names none of them, gives no before/after, and so leaves change 3 invisible to the reader. This is a real weakness and is recorded as a qualitative concern rather than a contract rejection: the categories R1 requires to be reported — legitimate removals, rejected losses, irreparable findings — are all empty in this run, the three findings were resolved rather than left unresolved, and the mechanical pass is reported as having changed nothing, which the diff confirms (no change originates in punctuation, spelling or inflection).

**Visible defects not addressed.** One: the standfirst's "Från september ska föreningslokaler i Lervik enligt tjänsteutlåtandet bara kunna bokas på webben" states in the indicative a change the lead then presents as a proposal awaiting a decision on 18 June. The inserted "enligt tjänsteutlåtandet" carries it, so the reader is not misled, but the tense reads as settled in a piece whose whole argument is that nothing is settled. Minor, and its repair would have been a legitimate finding.

**Changes of taste to passages that already worked.** None. Change 2 is the closest call — the sentence it replaced was serviceable — but it repaired a missing transition rather than restyling a working passage, and it is scored as a repair with the repetition cost named under W1.

No verification against unavailable sources was attempted or required.

## 11. Source loss

No source loss. `write/work/source.md` is material the Skill never had; none of the three changes removes or weakens anything it required.

- The self-imposed limit survives verbatim in substance. Source: "Föreningen gör inget anspråk på att ha finansierat eller kostnadsberäknat försöket. Kostnaden behöver kommunstyrelsen ta ställning till." Returned text, untouched by any change: "Öppna beslut gör inget anspråk på att ha kostnadsberäknat eller finansierat försöket. Den kostnaden är kommunstyrelsens att ta ställning till."
- The careful formulation about what the phone figure can and cannot show survives untouched. Source: "Telefonbokningarna kan därför inte användas för att säga hur stor andel av invånarna som inte kan boka digitalt." Returned text: "Telefonsiffran säger därför ingenting om hur stor andel av invånarna som kan eller inte kan boka digitalt."
- The quotation the source permits is carried verbatim, and the ending still names the three possible decisions with the cost uncertainty intact ("om en bokningsväg ska tas bort, ändras eller behållas"), as the source's judging boundary asks.
- Change 3 moves *toward* the source rather than away: the source states "Förvaltningens verkliga invändning mot att behålla båda kanalerna är dubbel administration, inte att telefonanvändare är lata eller dyra", which is exactly what the new subheading names. The Skill could not know this, and it is recorded here only as an observation.
