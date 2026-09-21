# Judgement B — opinion-sv-r1, Redline

Genre in the text's `kntnt` block is `opinion`, one of the four article genres, so the anatomy's skeleton applies as written and its counted requirements are judged on the script's figures.

## 1. Changes

Three differences between `redline/work/input.md` and `redline/delivered.md`.

1. Standfirst, sentence 4. Before: "Öppna beslut vill att kommunstyrelsen prövar båda vägarna ett halvår först." After: "Föreningen Öppna beslut vill att kommunstyrelsen prövar båda vägarna ett halvår först." **Repair of a visible defect.** The standfirst has to stand alone, and on first mention the bare "Öppna beslut" reads as an ordinary Swedish noun phrase ("open decisions") rather than as an organisation; the byline below it is not available to a reader meeting the standfirst on its own. No claim changes: same actor, same request, same modality. Standfirst words 42 → 43 (script), both inside the 60-word requirement.

2. Section 1, paragraph 1, opening sentence. Before: "Under åtta veckor prövades bara två av de sju lokalerna." After: "Förslaget vilar på ett försök där bara två av de sju lokalerna prövades under åtta veckor." **Repair of a visible defect, with a cost.** The defect is a real one: the section opens on a detached passive statement of scope with nothing tying the trial to the proposal the lead has just named, so the reader has to supply the link that carries the whole argument. The repair supplies it. The cost is that the new sentence now paraphrases the standfirst's second sentence ("Bakom förslaget ligger åtta veckors försök i två av sju lokaler") closely, spending 6 extra words (29 → 35, script) on information already given. No claim changes: "Förslaget vilar på ett försök" asserts exactly what that standfirst sentence already asserted, at the same strength.

3. Section 2 subheading. Before: "Invändningen är verklig, men handlingarna saknar siffror". After: "Dubbelarbetet är verkligt, men handlingarna saknar siffror". **Repair of a visible defect.** "Invändningen" is a bare anaphor with no antecedent above it, and in a piece that is itself one long objection it points the wrong way; a subheading has to be understood on its own. "Dubbelarbetet" names the administration's objection concretely, and the section's own first sentence ("personalen ska slippa föra in uppgifter i två flöden") carries it. Characters 56 → 58 (script), both inside the 70-character requirement. Claim strength unchanged: the input asserted the same reality of the objection, only of an unnamed referent.

No mechanical corrections, no removals, no changes of taste to a passage that already worked. Frontmatter is byte-identical; the four `kntnt` values are untouched.

## 2. Headings

**Input.**

- `# Underlaget räcker inte för att stänga telefonbokningen` — statement
- `## Siffrorna räknar bokningar, inte människor` — statement
- `## Invändningen är verklig, men handlingarna saknar siffror` — statement
- `## Ett halvår med mätning ger kommunstyrelsen underlag` — statement
- `## Mät först, besluta sedan` — label

**Returned text.**

- `# Underlaget räcker inte för att stänga telefonbokningen` — statement
- `## Siffrorna räknar bokningar, inte människor` — statement
- `## Dubbelarbetet är verkligt, men handlingarna saknar siffror` — statement
- `## Ett halvår med mätning ger kommunstyrelsen underlag` — statement
- `## Mät först, besluta sedan` — label

Notes on the marks. No headline or subheading uses a colon for a verb and none is a question. No **echo**: the headline's "Underlaget räcker inte" appears nowhere in the standfirst, which states the same case through different words ("I handlingarna finns varken tidsmätning eller besparingsberäkning"), and no subheading repeats the words or the phrasing of the first sentence under it — "Siffrorna räknar bokningar, inte människor" paraphrases the *second* paragraph's opening ("Rapporten räknar bokningar, inte unika personer"), which the echo mark does not reach, and "Mät först, besluta sedan" is picked up by the *second* paragraph's "Men mät först", not the first sentence. No **overclaim**: "Dubbelarbetet är verkligt" is carried by the section's own statement that staff enter the same data in two flows, and "Ett halvår med mätning ger kommunstyrelsen underlag" restates the proposal the section sets out.

## 3. Criteria on the returned text

### G1 — pass

The opinion does its job for a Lervik resident and for the committee it addresses. The position is stated early and plainly — "Vi i föreningen Öppna beslut menar att beslutet kommer för tidigt. Inte för att digital bokning är fel, utan för att underlaget inte visar vad bytet är värt" — and the angle holds through every section: not *whether* to digitise, but whether this evidence can settle it. The reader learns what the trial actually covered (two of seven premises, eight weeks, 96 web bookings against 24 by phone), what the report cannot tell anyone ("Rapporten räknar bokningar, inte unika personer"), and what is missing from the papers ("varken tidsmätning eller beräkning av vad borttagandet sparar"). The craft is a debate writer's: figures attributed to the named report and its date, an opponent's motive stated in the opponent's own terms, and a concrete alternative. The reader can consider a decision they could not otherwise weigh, and the committee member can act on it.

### G2 — pass

Every required part is present, in the anatomy's order, and each does its own job. Headline: 54 characters, 7 words (script), inside the 20–70-character requirement, and it states the angle without claiming more than the body claims. Standfirst: 43 words in 1 paragraph (script), inside the at-most-60-word requirement, and it stands alone — after change 1 it names the actor ("Föreningen Öppna beslut"), the proposal, the evidence and the ask, needing nothing above or below it. Byline: present and naming the author the text names, "Av Sanna Ek, talesperson för föreningen Öppna beslut", so the missing-byline report the contract demands of a source-blind Redline run is not owed here. Lead: 1 paragraph, 49 words (script), before the first H2, and it begins the work by fixing the date, the decision and the position. Four sections, each with at least one paragraph (script: 3, 2, 2, 2). Opinion's own parts: the position is early (lead), the support is the report's figures and their stated limits, the real objection is met on its merits ("Motivet i tjänsteutlåtandet är att personalen ska slippa föra in uppgifter i två flöden. Den invändningen tar vi på allvar"), and the ending is the change asked for, with an identifiable actor — "Låt telefonbokningen vara kvar under försöket, och avgör därefter om en bokningsväg ska tas bort, ändras eller behållas", addressed to a kommunstyrelse named in the lead. The ending meets the lead's expectation: the lead says the decision comes too early, the ending says what to do instead. No commercial call to action intrudes.

### P1 — pass

The chain is followable end to end for a resident with no special knowledge: the trial's scope, then what the report counts and does not count, then why a phone booking is not evidence of incapacity, then the administration's objection, then what the papers lack, then the alternative and what it would produce. The institutional terms a Swedish municipal reader may not carry — "tjänsteutlåtandet", the report's title and date — are introduced with enough context to be used. The transitions are real, not decorative: "Men handlingarna innehåller varken tidsmätning..." turns the conceded objection into the gap, and "Då kan arbetskostnaden vägas mot värdet för dem som bokar" states what the proposal would buy. The conclusions stay inside the visible support: the text says the phone figure "säger därför ingenting om hur stor andel av invånarna som kan eller inte kan boka digitalt" rather than claiming anybody is excluded, and it disclaims what it has not done — "Öppna beslut gör inget anspråk på att ha kostnadsberäknat eller finansierat försöket." The technical substance — what a booking count can and cannot support — survives in full.

### W1 — pass

The script measures 11 paragraphs of which 10 run to two or three sentences, and 4 sections of which 4 run to two or three paragraphs. Read across the whole text, as *most* must be, both are met. No *should* is departed from: the longest paragraph is 39 words (script), well under 80; no section exceeds three paragraphs; no heading goes below the second level; the headline is 7 words and 54 characters (script), inside 8 words and 60 characters; and standfirst and lead open on different first words ("Från" against "Den"). Standfirst and lead complement rather than duplicate — the standfirst gives the proposal and the evidentiary gap, the lead gives the meeting, the date and the position — and the body covers everything the standfirst promises, including the six-month alternative. The subheadings orient a scanner on their own: after change 3 all four name the thing their section is about. The only density cost anywhere is the new overlap between section 1's opening sentence and the standfirst, noted in Changes; it costs the reader six words, not the thread.

### L1 — pass

The Swedish is native and professionally written, with no translated cadence. Idiomatic constructions carry the argument: "Den invändningen tar vi på allvar", "Kommunstyrelsen ombeds alltså fatta ett permanent beslut om en arbetskostnad som underlaget inte sätter några siffror på", "Då vilar beslutet på det som faktiskt är mätt", "det är hela poängen". The register is the Swedish debate page's — declarative, flat, unornamented — and it is steady from the headline to the last sentence. Both clauses the Skill wrote are in the same voice: "Förslaget vilar på ett försök där..." and "Dubbelarbetet är verkligt" are ordinary Swedish, not calques, and neither breaks the surrounding rhythm.

### L2 — pass

The resolved locale is `sv` and it governs throughout. Dates take the Swedish form with no comma and a lower-case month: "den 8 april 2026", "Den 18 juni". Numerals are used for the figures that carry the argument ("96 bokningar via webben och 24 via telefon") and spelled-out forms for quantities in prose ("åtta veckors", "sju lokaler", "sex månaders"), which is standard Swedish practice. No currency and no converted figure appears anywhere, so nothing is invented. Punctuation is Swedish: "i stället" written apart, no serial comma, the report title set in italics rather than in quotation marks. No spelling or inflection error survives, consistent with the reply's statement that the final mechanical pass found nothing to correct.

## 4. T2 — skipped

No technique is named in the text's metadata or in the reply. The `kntnt` block carries `technique: none`, and the reply states the same and treats it as a choice ("`none` där är ett val och ingen lucka"). Nothing is judged under this criterion, and no technique is inferred from the shape of the prose.

## 5. R1 — pass

All three changes address concrete visible defects, and everything outside them is preserved byte for byte. The argument, the figures, the attributions, the concession to the administration and the author's own formulation ("Att en bokning går via telefon är inte ett bevis för att någon inte kan använda webben") stand untouched.

**Removals.** None. No sentence, clause, figure, attribution or caveat is gone from the returned text.

**Changed claims.** None. Taken one by one against the brief's test — strength, subject, scope, modality — change 1 changes only the name of an actor already named in the byline; change 2 asserts what the standfirst already asserted, at the same strength; change 3 replaces an unanchored subject with the concrete one the section's own first sentence supplies, at the strength the input's subheading already used. Nothing became more certain, broader or differently attributed. Because there is no removal and no changed claim, the categories the contract makes mandatory to report are empty, and no unresolved finding was left unreported.

**Reporting.** This is where the run is weakest, and it is a qualitative concern rather than a contract rejection. The account is "Granskningen gav tre fynd. En korrigeringsrunda reparerade alla tre, omgranskningen lämnade inga fynd kvar, och den avslutande mekaniska genomgången hittade inget att rätta." It is accurate — three findings, three changes in the text, and no mechanical error remains that I can see — but it is a count, not an account. A reader is told how many things changed and not one word about which, where or why, so they cannot check a single one of the Skill's judgements without diffing the two texts themselves. Two of the three changes were worth defending in a sentence each; the third, discussed below, needed defending. Nothing here trips the protocol's rejections: no unsupported fact was introduced, the locale is right, the mechanical pass made no substantive edit, no unresolved mandatory finding went unreported, and there are no side effects — the frontmatter and its three values are byte-identical. But the account falls short of what the contract describes, and this run passes on the substance of its edits rather than on the transparency of its report.

**Visible defects not addressed.** I find none of consequence. The one candidate is the standfirst's fourth sentence ("Föreningen Öppna beslut vill att kommunstyrelsen prövar båda vägarna ett halvår först") sitting close to the lead's third; but the standfirst must stand alone and the two are worded differently, so leaving it is right, not an omission. The subheading "Siffrorna räknar bokningar, inte människor" paraphrases the second paragraph's opening sentence, which is not the echo the anatomy forbids and reads as deliberate emphasis; leaving it is a defensible editorial call, not a missed defect.

**Changes of taste to passages that already worked.** None that fails the criterion, but change 2 is the one to name. The input sentence was correct, clear and inside every count; what justified touching it was the missing link between the trial's scope and the proposal, which is a visible defect and not a matter of preference. The repair is nevertheless the least clearly profitable of the three, because it buys that link with a closer restatement of the standfirst. It is one borderline edit among three; it does not make this a clean text rewritten to taste. No finding was made against a count the text met — the script reports `conforms: true`, `failures: []` and `norms: []` for both the input and the returned text — and no *most* statement was read against a single paragraph or section.

## 6. Source loss

No loss. None of the three changes removes or alters anything `write/work/source.md` required.

The source's caveats all survive verbatim in the returned text. "Rapporten räknar bokningar, inte unika personer. Den mäter inte ålder, funktionsförmåga eller digital vana" is carried as "Rapporten räknar bokningar, inte unika personer. Den mäter varken ålder, funktionsförmåga eller digital vana." The source's limit "Telefonbokningarna kan därför inte användas för att säga hur stor andel av invånarna som inte kan boka digitalt" is carried as "Telefonsiffran säger därför ingenting om hur stor andel av invånarna som kan eller inte kan boka digitalt." The financing disclaimer "Föreningen gör inget anspråk på att ha finansierat eller kostnadsberäknat försöket. Kostnaden behöver kommunstyrelsen ta ställning till" stands as its own paragraph in the final section, and the ending still names the committee's three possible decisions with the cost uncertainty intact, as the source's judging note requires. The figures remain attributed to the named report and its date.

The two changes that touch claims move toward the source rather than away from it. Change 3 replaces "Invändningen är verklig" with "Dubbelarbetet är verkligt", and the source states "Förvaltningens verkliga invändning mot att behålla båda kanalerna är dubbel administration, inte att telefonanvändare är lata eller dyra" — the returned subheading names precisely the objection the source says is the real one. Change 2 writes "Förslaget vilar på ett försök där bara två av de sju lokalerna prövades under åtta veckor", which restates the source's "ett åtta veckor långt försök i två lokaler" and the input's own standfirst; it introduces no new attribution of motive and no figure the source lacks. The Skill could not know any of this, and nothing above bears on the criteria.
