# Judgement B — opinion-sv-r2 / write

Genre `opinion` (brief: "Skriv en debattartikel"; frontmatter `genre: opinion`). The fixed anatomy applies, with its three strengths read as the brief directs.

## 1. Outcome

**Delivered.** The reply carries a complete fenced draft and `delivered.md` holds it.

**Two source comparisons completed.** `evidence/source-check/` and `evidence/source-check-2/` each hold a prompt, the material, the compared prose, the Claims contract and a report. Report 1 ends "**Unresolved findings: 4, all source-support, none translation.**"; report 2 ends "Comparison complete… **Source-support findings: none. Translation findings: none. Unresolved findings: none.**" Both prompts point at a fresh comparison with no conversation history, and the two `material.md` files are byte-identical to `work/source.md`.

**The delivered prose is byte-identical to the last prose a checker saw.** `delivered.md`, `evidence/draft-final.md` and `evidence/source-check-2/prose.md` all hash to `69533c7f0af918ff8df9c70bbf07f80d`; `diff` is empty in both directions. The five differences between `source-check/prose.md` and `source-check-2/prose.md` are exactly the four repairs report 1 proposed plus the one tightening it raised as an editorial question, so every repair was made before the second comparison and none after it. The reply's own account agrees: "Texten är levererad exakt som den jämförelsen läste den."

One inaccuracy in the account itself, not in the prose: it lists four source-support objections and then introduces the heading tightening as "En fjärde punkt", when it is the fifth item discussed. The reader can still match each item to report 1.

Side effects: the account states the working directory was restored to `source.md` plus an empty `scratch/`. The files this brief lets me read do not let me verify that either way, so I record it as unsettled rather than judging it.

## 2. Headings

- `# Kommunstyrelsen bör pröva båda bokningsvägarna ett halvår` — **statement**
- `## Pilotrapporten mäter inte vem som inte kan boka digitalt` — **statement**
- `## Handlingarna saknar mätning av vad det dubbla arbetet kostar` — **statement**
- `## Ett halvår med båda vägarna ger underlaget` — **statement**
- `## Kommunstyrelsen kan pröva först och besluta sedan` — **statement**, **echo**

The echo is narrow: the heading and the first sentence beneath it open on the same two words, "Kommunstyrelsen kan". What follows differs — the heading states the sequence (trial first, decision after), the sentence names the opposite option (approving the proposal in September) — so the repetition is a cadence, not a restatement.

No heading is a label, none uses a colon for a verb, none is a question, and none repeats the standfirst. On overclaim I weighed `## Ett halvår med båda vägarna ger underlaget` closely: read flatly it promises that the trial yields the decision basis, while the section's own mechanism has a voluntary limb ("ber användarna frivilligt ange varför de väljer telefon eller webb"). It falls short of the mark because the unconditional half of the trial — "registrerar förvaltningen tidsåtgången per bokningsväg" — is precisely the item the previous section establishes as missing, and the qualification stands in the sentence directly under the heading. It is the author's advocacy for her own proposal, at the strength the section carries.

## 3. F1 — pass

I compared every claim in `delivered.md` against `work/source.md` myself. No unsupported addition, changed term, changed subject, changed scope, date, modality or certainty, no dropped caveat, no invented event or personal attribute.

The load-bearing passages and their support:

- "96 bokningar via webben och 24 via telefon" — "Under försöket gjordes 96 bokningar via webb och 24 via telefon." The added "Under de åtta veckorna… i de två lokalerna" is the trial's own stated extent ("ett åtta veckor långt försök i två lokaler"). No count is called high, low or modest, which the Claims contract would require a comparison for.
- "Rapporten räknar bokningar, inte unika personer." — verbatim.
- "Tjugofyra telefonbokningar kan vara tjugofyra invånare eller betydligt färre som ringt flera gånger." — the modality `kan vara` asserts neither end. "Invånare" sits inside the possibility, so a non-resident caller falsifies nothing.
- "Därför säger den ingenting om hur stor andel av invånarna som inte kan boka digitalt." — the source scopes this to the phone bookings ("Telefonbokningarna kan därför inte användas…"), and the draft says it of the report. The widening is closed by the adjacent supplied sentence "Den mäter inte ålder, funktionsförmåga eller digital vana": a share of residents unable to book digitally can only come from those variables, and the report has none of them. Supported, though this is the one widening in the text that needed a second premise to carry it.
- "Att en bokning går via telefon är inte ett bevis… Det är ett skäl att ta reda på varför telefonen fortfarande används." — word for word the supplied ståndpunkt, which "får citeras eller refereras". Set unquoted in the running voice of the person the material attributes it to, who is this article's bylined author, so nobody's words are absorbed by another speaker.
- "Handlingarna saknar mätning av vad det dubbla arbetet kostar" and "Men varken en tidsmätning eller en ekonomisk besparingsberäkning finns i handlingarna." — "Någon tidsmätning eller ekonomisk besparingsberäkning finns inte i handlingarna." Scope held to the one document set in the heading as well as the body, which is where the earlier draft failed.
- "Den är verklig och handlar om personalens arbetstid, inte om att de som ringer skulle vara lata eller dyra." — "Förvaltningens verkliga invändning… är dubbel administration, inte att telefonanvändare är lata eller dyra", with the labour reading fixed by "personalen ska slippa föra in uppgifter i två flöden" and by "väga arbetskostnaden mot värdet för användarna". No magnitude is asserted, and the counterfactual "skulle vara" keeps the lazy/expensive view as something the material denies rather than something anyone is said to hold.
- "Vi gör inget anspråk på att ha kostnadsberäknat eller finansierat försöket." — "Föreningen gör inget anspråk på att ha finansierat eller kostnadsberäknat försöket." The unclaimed stays unclaimed; only the order of the two verbs moves.
- "Vad ett halvår med båda vägarna kostar måste kommunstyrelsen ta ställning till." — "Kostnaden behöver kommunstyrelsen ta ställning till." `måste` and `behöver` are the same necessity here, and no figure, range or direction is attached. The boundary "med kostnadsosäkerheten bevarad" holds to the last section.
- "Öppna beslut motsätter sig inte digital bokning." — the material states this of Sanna Ek ("Hon motsätter sig inte digital bokning"). The subject moves to the association. It is carried independently by the association's own supplied proposal, which keeps the web route in all seven lokaler and then leaves the kommunstyrelse free to remove, change or keep a channel; and the brief makes her its talesperson. Supported.
- "Under försöket registrerar förvaltningen tidsåtgången per bokningsväg…" — the material's prescriptive "ska registrera" becomes a present indicative, but the governing sentence before it is "Öppna beslut föreslår ett sex månader långt försök", and "Under försöket" names a trial that does not exist, so the present states the proposal's content, not an ongoing practice. "Frivilligt" survives.

Two term checks in both directions:

- "räknar bokningar, inte människor" (standfirst) against "bokningar, inte unika personer". Something could fall under the source's term and not the draft's only if the report carried a non-unique headcount as well; nothing supplied puts any people-count in the report, and the exact form is restored one section later. Defensible; unknown is kept apart from absent here because the draft never says the report shows no people use the service, only what it counts.
- "vägarna" against the material's "kanalerna". The material itself uses "bokningsvägarna" for the same two routes in the association's proposal, so nothing in this context falls under one and not the other.

Boundaries: no lagkrav, protest, diskrimineringsfall, partipolitiskt motiv or besparing is asserted anywhere. The savings calculation appears only as an absence. The figures that bear the argument sit under "Pilotrapporten" in the heading and beside "Rapporten" in the next sentence, which meets "Siffror ska tillskrivas rapporten där de bär argumentet" — the figure sentence is itself agentless, exactly as the material's own is.

The brief's "ungefär 400 ord" cannot be checked here: the script reports words per part but no total, so the document's length is not measured. The reply's "omkring 457 ord" is its own claim, not evidence.

## 4. G1 — pass

The genre does its job for residents of Lervik. The reader learns the pilot's extent and unit ("bygger på åtta veckor i två lokaler och räknar bokningar, inte människor"), what is proposed ("telefonbokningen… försvinna i alla sju lokaler från september"), on what motive, and what the decision papers do not contain. The angle is recognisable and held throughout: not that digital booking is wrong, but that the basis for removing a channel is not in the papers — "Vi motsätter oss att frågan avgörs innan de två uppgifterna ligger på bordet."

The craft the brief asked for — "sakligt skarp… utan falska motiv eller tandlös neutralisering" — is present in both halves. Sharp: "Ett förslag som tar bort en bokningsväg i sju lokaler bör kunna svara på den frågan." Honest about the other side: "Den är verklig och handlar om personalens arbetstid, inte om att de som ringer skulle vara lata eller dyra." The reader can consider a real choice and can see what the council could do on 18 June. No commercial CTA, as the brief required.

The one discipline I looked for and found is the refusal to argue from the 24 phone bookings: "Den som vill använda telefonsiffran som bevis för att alla klarar webben har lika lite stöd i rapporten som den som hävdar motsatsen." A weaker opinion piece would have made those 24 into a constituency.

## 5. G2 — pass

The parts are present in the anatomy's order and each does its own job. The script's `parts` names `headline`, `standfirst`, `byline`, `lead` and four `sections`, with `other: []`, and reports `conforms: true`, `failures: []`.

- **Headline** (57 characters, 7 words) states the angle and is understood alone; it claims no more than the text argues.
- **Standfirst** (46 words, 1 paragraph) stands alone: pilot, proposal, and what the association wants instead. Under 60 words as the requirement has it.
- **Byline** "Av Sanna Ek, talesperson för föreningen Öppna beslut" names the author the brief names ("Avsändare är Sanna Ek, talesperson för föreningen Öppna beslut"), verbatim. The delivery account does address it, but only obliquely, in the paragraph on the quotation: "hon är artikelns författare, och materialet tillåter både citat och referat." That is enough for a reader to see the byline came from the material, but the account's "Upplöst konfiguration" paragraph names genre, language, technique and output choice and passes the byline over. A qualitative concern, not a contract rejection.
- **Lead** (44 words, 1 paragraph) comes before the first H2 and begins the work: it names the document, the meeting date, the motive, and the two absences the article will argue.
- **Body** is explanatory across four sections: what the report cannot show, what the papers do not contain, what the trial would produce, what the council can do.
- **Ending** meets the lead's expectation exactly. The lead says "två uppgifter som borde ligga på kommunstyrelsens bord saknas i handlingarna"; the last sentence closes on "innan de två uppgifterna ligger på bordet."

Opinion's own parts: the position is early — headline and standfirst both carry it, and the reader has it before the byline. The support is the report's unit and the papers' absences. The real objection is met and conceded rather than knocked down: "Förvaltningens invändning… är den dubbla administrationen. Den är verklig…". The call to action is the change with an identifiable actor: "Den kan också låta båda vägarna stå kvar ett halvår, ta ställning till kostnaden och sedan avgöra om en kanal ska tas bort, ändras eller behållas." The actor is the kommunstyrelse, and the cost question is handed to it undetermined, as the brief required.

## 6. P1 — pass

The reasoning is followable in one pass. The municipal vocabulary a Lervik resident needs — pilotrapport, tjänsteutlåtande, handlingarna, kommunstyrelsen — is either introduced with its content ("Tjänsteutlåtandet inför kommunstyrelsens möte den 18 juni föreslår att…") or common local knowledge for the named reader. The transitions do work rather than decorate: "Ändå" sets the proposal against the report, "Därför" carries the inference the material itself carries, "alltså" draws the consequence of an absence, "Men" marks each of the two concessions.

Conclusions stay proportionate to the visible support. The text never says how many residents need the phone; it says "Tjugofyra telefonbokningar kan vara tjugofyra invånare eller betydligt färre", and then that the report "säger ingenting om hur stor andel". It never says which channel is faster; it says "Hur lång tid en telefonbokning tar jämfört med en webbokning framgår alltså inte."

Useful technical substance remains: 96 and 24, eight weeks, two lokaler against seven, 18 June, September, six months, and the two named measurements the trial would produce.

One friction, a qualitative concern rather than a failure: "uppgifter" carries two senses two sentences apart in the lead — "föra in uppgifter i två flöden" (data entered) and "två uppgifter… saknas i handlingarna" (two items of information) — and the second sense returns in the final sentence. Context resolves it, but the reader resolves it rather than reads past it, and the article's closing ring depends on the second sense landing cleanly. Report 1 noted the same collision and set it aside as outside a source comparison.

## 7. W1 — pass

A web reader can orient and enter without losing the explanation or the voice. The five headings are informative statements that map the argument, and the anatomy's counted requirements all hold on the script's figures: `conforms: true`, `failures: []`. Headline 57 characters and 7 words; standfirst 46 words in 1 paragraph; lead 44 words in 1 paragraph; subheadings 56, 60, 42 and 49 characters; every section has at least one paragraph.

No *should* is departed from: `norms: []`. The longest paragraph the script measures is 57 words, under the 80-word norm; no section exceeds three paragraphs; no heading level goes below the second; the headline is inside 8 words and 60 characters. Standfirst and lead open on different first words — "Lerviks" against "Tjänsteutlåtandet".

The *most* statements are read across the whole text and hold there: `paragraphs: 10`, `paragraphs_of_two_or_three_sentences: 9`, `sections: 4`, `sections_of_two_or_three_paragraphs: 3`. The two texts outside the pattern are the closing section, a single paragraph of 57 words in 4 sentences. Under the scale this brief sets, that is not a failure of that section or that paragraph, and as writing it is the right place to break the pattern: the four decisions the council faces belong in one uninterrupted block at the end.

Standfirst and lead are complementary, and the body is complete when the standfirst is covered: all three of the standfirst's promises — the pilot's limits, the proposal, the association's alternative with time figures — get a section each. The one cost I record is redundancy at the seam: the standfirst's "Ändå föreslås telefonbokningen av föreningslokaler försvinna i alla sju lokaler från september" and the lead's "föreslår att telefonbokningen av föreningslokaler tas bort i alla sju lokaler från september" are nearly the same sentence, and the reader meets it twice within about forty words. The lead does add the document, the date and the motive, so this is a qualitative concern, not reader loss, and not a departure from any stated norm.

## 8. L1 — pass

The prose reads as Swedish written by a Swede, not as translated English. Idiom and syntax are native throughout: "Motivet är att personalen ska slippa föra in uppgifter i två flöden", "betydligt färre som ringt flera gånger" with the auxiliary properly dropped, "har lika lite stöd i rapporten som den som hävdar motsatsen", "innan de två uppgifterna ligger på bordet". The debate-article register is right for the genre — plain, declarative, no anglicisms, no calques, and no generic translated flatness.

The voice is consistent and is the author's: the third person for the documents, "Vi" for the association from the moment the association's own proposal enters, and the supplied ståndpunkt set in the same voice without a seam. "Ett förslag som tar bort en bokningsväg i sju lokaler bör kunna svara på den frågan" personifies a proposal, which is ordinary in Swedish debate prose and reads as deliberate.

## 9. L2 — pass

Swedish locale mechanics govern throughout. Month names are lower case, Swedish style: "den 18 juni", "från september", "i september". The date form is the Swedish "den 18 juni", not an imported form, and no year is invented where the material gives none for the meeting. No currency figure appears anywhere, and none is converted — the cost is left as a question, which is also what the material requires.

Number style is Swedish and consistent: digits for the report's figures, "96" and "24"; the spelled-out "Tjugofyra" at the head of a sentence rather than a leading digit; and small quantities written out in words — "åtta veckor", "två lokaler", "sju lokaler", "sex månader", "ett halvår". Punctuation is plain and correct; the one colon in the earlier draft ("Rapporten är tydlig med vad siffrorna är:") went out with the repair, and no quotation marks are used, which is consistent with setting the ståndpunkt in the author's own voice. "Öppna beslut" keeps sentence-case capitalisation as a Swedish organisation name.

## 10. T2 — skipped

The delivered text's `kntnt` metadata reads `technique: none`, and the reply states "Ingen teknik är upplöst: varken anropet eller materialet anger någon." No technique was selected, so nothing is judged under T2. I did not infer one from the shape of the prose.

## 11. Checker findings

**`evidence/source-check/report.md` — four findings (§3).**

1. `## Ingen har mätt vad det dubbla arbetet kostar` — alleged that the heading widens the material's "finns inte i handlingarna" from one document set to the world. Writer repaired it to `## Handlingarna saknar mätning av vad det dubbla arbetet kostar`. **supported** — the material scopes the absence explicitly, and a measurement made and not published would satisfy the source while falsifying the heading.
2. "Vi har inte kostnadsberäknat försöket och gör inget anspråk på att ha finansierat det." — alleged that the costing half turns an unclaimed into a negative fact. Writer repaired it to "Vi gör inget anspråk på att ha kostnadsberäknat eller finansierat försöket." **supported** — the material says only "gör inget anspråk på att ha finansierat eller kostnadsberäknat", and the contract's "what is unknown or unclaimed is not thereby known not to have happened" is exactly this case.
3. "…och siffror på vad varje bokningsväg kostar" (standfirst) — alleged that cost replaces the proposal's "tidsåtgång per bokningsväg" and moves the cost question off the council's table. Writer repaired it to "…och siffror på hur lång tid varje bokningsväg tar." **supported** — the proposal names only time, and the material assigns cost to the kommunstyrelse; the draft's own body kept the distinction the standfirst had lost.
4. "Rapporten är tydlig med vad siffrorna är: bokningar, inte unika personer." — alleged that "är tydlig med" credits the report with a disclosure the material does not establish. Writer repaired it to "Rapporten räknar bokningar, inte unika personer." **supported** — the material states what the report counts, never what it discloses about its own unit, and the credit sat in a passage otherwise criticising the beslutsunderlag.

**`evidence/source-check/report.md` — §5, reported as editorial questions, not findings.**

5. `## Sex månader med båda vägarna ger svaren` — raised as an unsettled standpoint-versus-prediction question, with a tightening offered rather than a repair required. Writer tightened it anyway, to `## Ett halvår med båda vägarna ger underlaget`. **disputed** — the material leaves it open: "be användarna frivilligt ange varför" limits what the trial can deliver, while the brief carries the proposal as the association's own thesis, which a heading may argue.
6. "räknar bokningar, inte människor" (standfirst) — noted only because the contrast term is not the material's word; judged defensible as written. Writer left it. **disputed** — nothing supplied puts any people-count in the report, but nothing supplied rules one out either; the exact form is restored one section later, so no reader is misled.
7. Listed "for the record" and not raised: the report's title and date omitted, the material's "först" omitted from the weighing sentence, and the two senses of "uppgifter" in the lead. Writer changed none. The first two are omissions, not changed claims. The third is the friction I record under P1.

**`evidence/source-check-2/report.md` — no findings.** §5 reads "**None.**" and §6 "Source-support findings: none. Translation findings: none. Unresolved findings: none." Four divergences and two further checks were tested in both directions and set aside (§3.1–§3.6). I reached the same result on each independently, including the two I weighed hardest: the widening at "Därför säger den ingenting om…" and the subject move at "Öppna beslut motsätter sig inte digital bokning."

**Was a real F1 defect seen by no checker?** No. I found no unsupported passage in the delivered text, so there is nothing the checkers missed. The four defects report 1 found were real, and all four are gone from the delivered prose.

## 12. Remaining findings

**None.** The delivery account reports no remaining finding: "Den andra och slutgiltiga jämförelsen läste den lagade texten och rapporterade inga kvarstående invändningar, varken om källstöd eller om översättning." That matches report 2 and the byte-identity above, so there is no reported finding to weigh as a defect under F1, and the run does not fall under the rejection for unresolved mandatory findings left unreported.

The account's "Där materialet tar slut" section names three things the material does not bear — how many residents need the phone, what the double work costs, what the association's own trial costs — and what further material would close each gap. These are limits of the material honoured in the text, not findings against it, and they match what I found: the text states each of the three as an absence rather than filling it.

## 13. Class of the run

**`valid delivery`.** The prose delivered had a completed comparison of its own — the second one, which read exactly the bytes that were delivered and reported nothing unresolved — and it was delivered rather than withheld. Every defect the first comparison found was repaired before that second comparison, and nothing was changed after it. None of the five unconditional rejections is triggered: no unsupported fact (F1 pass), the locale is Swedish throughout (L2 pass), no mechanical editing question arises for a Write run, no unresolved finding went unreported, and the files I am permitted to read show no incorrect side effect, though they do not let me confirm the account's claim about the working directory either way.
