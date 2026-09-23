# Judgement A — opinion-sv-r1 / write

Genre: `opinion` (the brief asks for "en debattartikel"; the delivered text's `kntnt` metadata says `genre: opinion`). The four-genre skeleton therefore applies, and the script's counts are requirements where the anatomy states them plainly.

## 1. Outcome

**Delivered.** `delivered.md` is present, and `response.md` carries the same text in a fenced `markdown` block beneath the delivery account.

**Two source comparisons completed.** `evidence/source-check-1/report.md` ends "Comparison complete … **Unresolved findings: 3.**" and `evidence/source-check-2/report.md` ends "Comparison complete … **Findings: 1 source-support finding (F1), unresolved.**" Each directory holds its own `draft.md`, `material.md`, `claims.md`, `quotations.md` and `task.txt`, and the two `task.txt` files point the checker at its own scratch directory. `evidence/validation.md` records both dispositions, and the reply says "Två källkontroller kördes, båda av en ny agent utan samtalshistorik."

**The delivered prose is byte-identical to the last prose a checker saw.** `delivered.md` and `evidence/source-check-2/draft.md` are the same bytes (md5 `bdae9acd0e9d31af181b7cb61651f63c` for both; `diff` is empty), and `anatomy-delivered.json` and `evidence/anatomy2.json` are identical files. The first checker's draft differs (md5 `c1b2b4ae31edae370d624f158b4d7d96`) at four lines — the standfirst, one subheading, one concession sentence and one closing sentence — which are exactly the three repairs and the one voluntary change `validation.md` records between the comparisons.

**No repair was made after the last comparison.** `validation.md` states of comparison 2's F1: "Not repaired: this was the final comparison, and a repair no comparison has read would be unchecked prose. F1 is carried to the delivery account instead." The reply opens on the same statement: "en reparation som ingen kontroll har läst är okontrollerad text". The byte identity above is the independent confirmation.

## 2. Headings

- `# Underlaget räcker inte för att stänga telefonbokningen` — **statement**. Not colon, not question. No **echo**: the standfirst opens "Från september ska föreningslokaler i Lervik …" and shares no phrasing with it. No **overclaim**: it is the thesis the whole text argues and the brief commissions.
- `## Siffrorna räknar bokningar, inte människor` — **statement**; **overclaim (marginal)**. The material says "Rapporten räknar bokningar, inte unika personer", and the section's own second paragraph carries that exact form; the heading drops "unika", which reads fractionally wider than what the text carries. Not an **echo**: the first sentence under it is "Under åtta veckor prövades bara två av de sju lokalerna."
- `## Invändningen är verklig, men handlingarna saknar siffror` — **statement**. "verklig" is the material's own predicate ("Förvaltningens **verkliga** invändning … är dubbel administration"). "saknar siffror" is bound by "men" to the objection just named, so it reads as figures for that objection rather than as an absence of all figures — no **overclaim** on that reading. Not an **echo** of "Motivet i tjänsteutlåtandet är att personalen ska slippa föra in uppgifter i två flöden."
- `## Ett halvår med mätning ger kommunstyrelsen underlag` — **statement**. Forward-looking, but it is the author's advocated claim, proportionate to the proposal set out beneath it. No **echo** of "Öppna beslut föreslår i stället sex månaders försök i alla sju lokaler …"; no **overclaim**.
- `## Mät först, besluta sedan` — **statement** (an imperative pair that states the section's call). Not an **echo** under the definition: the first sentence under it is "Öppna beslut gör inget anspråk på att ha kostnadsberäknat eller finansierat försöket." The later "Men mät först." in the section's second paragraph is a deliberate rhetorical pickup of the heading, not the heading repeating its opening sentence. No **overclaim**.

No colon heading and no question heading occurs. No heading level below the second: the file carries one `#` and four `##` and nothing else.

## 3. F1 — pass

Every factual and attributed claim in the delivered text stays inside `work/source.md`, with one contested implication, reported, which I set out at the end of this section.

Supported, passage by passage:

- "Från september ska föreningslokaler i Lervik enligt tjänsteutlåtandet bara kunna bokas på webben" ← "Tjänsteutlåtandet … föreslår att telefonbokning tas bort för alla sju lokaler från september." The modality is carried by "enligt tjänsteutlåtandet", and the lead immediately states it as a proposal still to be decided ("möter kommunstyrelsen … ett förslag"). The draft names no class of bookers, after comparison 1's finding 3 was repaired.
- "I handlingarna finns varken tidsmätning eller besparingsberäkning" ← "Någon tidsmätning eller ekonomisk besparingsberäkning finns inte i handlingarna." Absence located where the material locates it.
- "Öppna beslut vill att kommunstyrelsen prövar båda vägarna ett halvår först" and "sex månaders försök i alla sju lokaler, med båda bokningsvägarna kvar" ← "Öppna beslut föreslår ett sex månader långt försök i alla sju lokaler, med båda bokningsvägarna kvar."
- "Den 18 juni möter kommunstyrelsen i Lervik ett förslag om att telefonbokningen av föreningslokaler ska tas bort i alla sju lokaler" ← the tjänsteutlåtande sentence, date and scope intact.
- "Kommunens rapport *Bokning av föreningslokaler* från den 8 april 2026 redovisar 96 bokningar via webben och 24 via telefon" ← the report sentence, title and date exact, and the figures attributed to the report as the boundaries demand ("Siffror ska tillskrivas rapporten där de bär argumentet").
- "Rapporten räknar bokningar, inte unika personer. Den mäter varken ålder, funktionsförmåga eller digital vana." ← the material's two sentences, verbatim in substance.
- "Telefonsiffran säger därför ingenting om hur stor andel av invånarna som kan eller inte kan boka digitalt" ← "Telefonbokningarna kan därför inte användas för att säga hur stor andel av invånarna som inte kan boka digitalt." The draft's "kan eller inte kan" is not a widening: the two shares are complements, so a figure that cannot establish one cannot establish the other.
- "Att en bokning går via telefon är inte ett bevis … Det är ett skäl att ta reda på varför telefonen fortfarande används." ← Sanna Ek's supplied words, reproduced exactly, unquoted, by the person the byline names, and the material permits it ("Detta får citeras eller refereras").
- "Motivet i tjänsteutlåtandet är att personalen ska slippa föra in uppgifter i två flöden" ← verbatim. "Den invändningen tar vi på allvar" is the author's stance and matches "Förvaltningens verkliga invändning … är dubbel administration, inte att telefonanvändare är lata eller dyra" — no false motive is imputed, which the boundaries forbid.
- "Kommunstyrelsen ombeds alltså fatta ett permanent beslut om en arbetskostnad som underlaget inte sätter några siffror på" ← the removal is proposed from September with no end, and the brief's own thesis calls it "ett permanent byte"; the missing figures are the material's.
- "Under tiden registrerar förvaltningen tidsåtgången per bokningsväg, och den som bokar får frivilligt ange varför valet blev telefon eller webb" ← "ska förvaltningen registrera tidsåtgång per bokningsväg och be användarna frivilligt ange varför de väljer telefon eller webb", stated inside the proposal's scope.
- "Då kan arbetskostnaden vägas mot värdet för dem som bokar" ← "kommunen först måste kunna väga arbetskostnaden mot värdet för användarna". "användarna" → "dem som bokar" names the same set in this context: the material's users are the users of the two booking routes, and nothing here could be one and not the other.
- "Öppna beslut gör inget anspråk på att ha kostnadsberäknat eller finansierat försöket. Den kostnaden är kommunstyrelsens att ta ställning till." ← "Föreningen gör inget anspråk på att ha finansierat eller kostnadsberäknat försöket. Kostnaden behöver kommunstyrelsen ta ställning till." The withheld claim is preserved as withheld, and the cost uncertainty survives, as the boundaries require.
- "avgör därefter om en bokningsväg ska tas bort, ändras eller behållas" ← "Därefter kan den avgöra om en kanal ska tas bort, ändras eller behållas." The ending names the committee's possible decision, as the boundaries require.
- Byline "Av Sanna Ek, talesperson för föreningen Öppna beslut" ← the brief's "Avsändare är Sanna Ek, talesperson för föreningen Öppna beslut."
- Nothing invented: no legal requirement, protest, discrimination case, party-political motive or established saving appears anywhere in the text, all of which the boundaries exclude.

Two passages I weighed and do not report as defects:

- "två av de sju lokalerna" / "två av sju lokaler". The material says the pilot covered "två lokaler" and that the proposal covers "alla sju lokaler"; it does not state in so many words that the pilot's two are among the seven. Read as an ordinary reader would, a municipal pilot titled *Bokning av föreningslokaler* ran in two of that municipality's föreningslokaler. Defensible as written.
- "Vi i föreningen Öppna beslut". Whether a talesperson is a member is left open by the material. Standard institutional voice; comparison 2 raised it as a question rather than a defect, and I agree.

**The reported implication.** "Bakom förslaget ligger åtta veckors försök i två av sju lokaler" (standfirst), echoed by "i stället för på åtta veckor i två lokaler" (closing). The counts, the duration and the two-of-seven scope are supported; the evidential relation is not stated in the material, which gives the proposal's motive flatly and differently. I class this **disputed** rather than an established defect, and F1 does not fail on it, for three reasons. The brief's boundaries direct the author at "beslutsunderlaget" as one body, and the pilot report is the municipality's own document on precisely this question, dated within the decision's timeline. *Bakom förslaget ligger X* is idiomatically available in Swedish debate prose as "what stands behind this proposal is X", i.e. the evidence available to the committee, not only "the proposal's stated motive is X". And the text itself removes any risk of a reader mistaking it: section two states the motive plainly and attributes it to the tjänsteutlåtande. No fact, figure, date, name, scope or modality is changed anywhere. This is a qualitative concern, not a contract rejection — and it is reported beside the draft, so the "unresolved mandatory findings not reported" rejection does not bite either.

## 4. G1 — pass

The opinion does its job for a resident of Lervik. The reader learns what is proposed and when ("Den 18 juni möter kommunstyrelsen i Lervik ett förslag om att telefonbokningen … ska tas bort i alla sju lokaler"), what the evidence behind it is and is not ("Rapporten räknar bokningar, inte unika personer. Den mäter varken ålder, funktionsförmåga eller digital vana"), what the administration's case is, taken seriously rather than caricatured ("Motivet i tjänsteutlåtandet är att personalen ska slippa föra in uppgifter i två flöden. Den invändningen tar vi på allvar"), and what the association asks for instead. The angle stays recognisable from headline to close: the decision material does not show what the change is worth. The criticism is sharp — "Kommunstyrelsen ombeds alltså fatta ett permanent beslut om en arbetskostnad som underlaget inte sätter några siffror på" — without the toothless neutralisation the brief warns against, and without the false motives it forbids. No commercial call to action appears, as the brief requires.

## 5. G2 — pass

The anatomy's parts are present in order, and `anatomy-delivered.json` reports `"conforms": true`, `"failures": []`, `"norms": []`.

Counted requirements, every figure the script's:

- Headline 54 characters (`parts.headline.characters` = 54) — inside 20–70.
- Standfirst 42 words (`parts.standfirst.words` = 42) — at most 60 — in one paragraph (`parts.standfirst.paragraphs` = 1).
- Lead one paragraph (`parts.lead.paragraphs` = 1), 49 words, placed before the first H2 — the script records it as `parts.lead`, outside `parts.sections`.
- Subheadings 42, 56, 51 and 24 characters (`parts.sections[*].subheading.characters`) — each at most 70.
- Every section has at least one paragraph: 3, 2, 2 and 2 (`parts.sections[*].paragraphs`).
- Byline present (`parts.byline.text` = "Av Sanna Ek, talesperson för föreningen Öppna beslut").

Each part does its own job. The headline states the angle and is understood alone. The standfirst stands alone: it gives the September change, the size of the trial behind it, the missing figures and the association's counter-proposal, and a reader who stops there has the argument. The byline names the author the brief names, and the delivery account states where it came from — "Bylinen är Sanna Ek, talesperson för föreningen Öppna beslut. Den kommer ur underlaget, inte ur anropet." The lead begins the work rather than repeating the standfirst, and puts the position early, as the genre requires: "Vi i föreningen Öppna beslut menar att beslutet kommer för tidigt. Inte för att digital bokning är fel, utan för att underlaget inte visar vad bytet är värt."

The opinion's own parts: **early position** in the lead's second sentence, above. **Support** in sections one and two, resting on attributed figures and on the stated absence of others. **A relevant real objection**, met rather than dodged — the administration's double-entry burden is named in the material as its "verkliga invändning", and the text concedes it ("Den invändningen tar vi på allvar") before answering it on the figures. **The change as the call to action, with an identifiable actor**: "Låt telefonbokningen vara kvar under försöket, och avgör därefter om en bokningsväg ska tas bort, ändras eller behållas", addressed to kommunstyrelsen, which the preceding sentence names as the body that must settle the cost. The ending shows the lead's expectation met: the lead said the decision comes too early because the underlag does not show what the change is worth; the close says measure first, then decide, "Då vilar beslutet på det som faktiskt är mätt".

No subheading repeats the first sentence under it, and none claims more than its section carries, with the marginal compression at "Siffrorna räknar bokningar, inte människor" noted in §2 — the section's own second paragraph restores "inte unika personer" two lines below, so no reader is left with the wider claim. That is an editorial compression, not a failure of the part's job.

## 6. P1 — pass

The reasoning is followable in one pass by a resident with no prior knowledge. The sequence is: here is what is proposed, here is what the only trial can and cannot tell you, here is the administration's real objection and what the papers do not put figures on, here is what six months with both routes would produce, therefore decide afterwards. Each unfamiliar element is introduced before it is used: the tjänsteutlåtande and its date in the lead before the criticism; the report, with its title and date, before its figures are leant on; the distinction between counting bookings and counting people before the conclusion drawn from it.

The transitions are real, not decorative: "Rapporten räknar bokningar, inte unika personer … Telefonsiffran säger därför ingenting om …" turns a measurement property into a limit on inference; "Men handlingarna innehåller varken tidsmätning eller beräkning av vad borttagandet sparar" turns a conceded objection into the gap that carries the argument; "Då kan arbetskostnaden vägas mot värdet för dem som bokar. Den avvägningen går inte att göra i dag, och det är hela poängen" names why the proposal follows.

Conclusions stay proportionate to visible support. The text never claims that residents cannot book digitally — the strongest thing it says is that the figure cannot tell you. It never claims a saving or a cost, only that the papers carry neither. The technical substance a reader needs survives: what was measured, over how long, in how many premises, what the report excludes, and what the proposed trial would record.

## 7. W1 — pass

A web reader can orient and enter. The four subheadings each state their section's point and are informative on their own, which this genre needs; the reader scanning them gets the argument in order.

Counted, the script's figures: `typical.paragraphs` = 11, of which `paragraphs_of_two_or_three_sentences` = 10; `typical.sections` = 4, of which `sections_of_two_or_three_paragraphs` = 4. The *most* statements are therefore met across the whole text, and the single paragraph outside the two-or-three band is not a failure — *most* is never read against one paragraph.

No *should* is departed from: `"norms": []`. Specifically, the script reports no paragraph over 80 words (the longest part it measures is the lead at 49 words, and the longest body paragraph 39 words), no section over three paragraphs (3, 2, 2, 2), the headline at 7 words and 54 characters — inside eight words and 60 characters — and no heading level below the second. Standfirst and lead open on different first words: "Från september …" against "Den 18 juni …".

Standfirst and lead are complementary rather than duplicative: the standfirst is the situation and the ask, the lead is the moment of decision and the position. The body is complete when the standfirst is covered — each of its four clauses (the September change, the eight weeks in two of seven, the missing figures, the six-month proposal) has a section that carries it out. Rhythm is even and the paragraphs are coherent units, each on one point; the two-sentence close of section three, "Den avvägningen går inte att göra i dag, och det är hela poängen", lands the argument without density. I find no reader loss to density or fragmentation.

## 8. L1 — pass

The prose reads as professionally written Swedish debate writing, not as translated English. Idiom and syntax are native throughout: "personalen ska slippa föra in uppgifter i två flöden", "Den invändningen tar vi på allvar", "det är hela poängen", "Mät först, besluta sedan", "Den kostnaden är kommunstyrelsens att ta ställning till". Administrative vocabulary is used correctly and unforced — tjänsteutlåtande, handlingar, förvaltningen, kommunstyrelsen, bokningsväg. Word order is Swedish where an import would show, including the inversions "Under åtta veckor prövades bara två av de sju lokalerna" and "Då kan arbetskostnaden vägas mot värdet för dem som bokar". No English calque, no generic translated register.

## 9. L2 — pass

The resolved locale is Swedish (`kntnt.language: sv`; the source material is Swedish). Dates take Swedish form — "den 8 april 2026", "den 18 juni", "Från september" — with lower-case month names, and no new date is invented: both are the material's. No currency or converted amount appears anywhere, which is correct, since the material supplies none. Figures are plain integers, "96" and "24", so no separator question arises. Spelling and diacritics are Swedish throughout ("föreningslokaler", "tidsåtgången", "avgör", "väger"). Punctuation is Swedish: no quotation marks are used at all, the report title is set in italics rather than quoted, and comma use before "och"-coordination and in the "varken … eller" constructions is idiomatic. No mechanical rewriting of established variation.

## 10. T2 — skipped

No technique is named in the text's metadata or in the reply as having been selected. The delivered front matter reads `technique: none`, and the reply states "Ingen teknik tillämpades: `opinion` anger uttryckligen att den inte skrivs med någon". I infer nothing from the shape of the prose and judge nothing under this criterion.

## 11. Checker findings

Comparison 1 — `evidence/source-check-1/report.md`, three findings:

1. **Finding 1** — draft passage "Bakom förslaget ligger åtta veckors försök i två av sju lokaler, **utan mätning av arbetstid och utan besparingsberäkning**". Alleged: the modifier relocates a documented absence from the papers to the trial itself, so the draft asserts that no working time was measured during the eight weeks. Writer: accepted and repaired — the standfirst now carries "I handlingarna finns varken tidsmätning eller besparingsberäkning" as its own sentence. My class: **supported**. The material locates the absence only in the handlingar ("Någon tidsmätning eller ekonomisk besparingsberäkning finns inte i handlingarna"), and nothing supplied excludes a trial that logged time without the log reaching the papers.
2. **Finding 2** — draft passage "Vad ett halvår med båda vägarna kostar **har vi inte räknat på**, och **vi finansierar det inte**". Alleged: a withheld claim is turned into a positive denial, with a forward-looking commitment the material never supplies. Writer: accepted and repaired to the material's own form, "Öppna beslut gör inget anspråk på att ha kostnadsberäknat eller finansierat försöket". My class: **supported**. "Gör inget anspråk på att ha X" declines to claim X; it does not assert not-X, and it says nothing about future financing.
3. **Finding 3** — draft passage "Från september ska **föreningar i Lervik** enligt tjänsteutlåtandet bara kunna boka lokaler på webben". Alleged: the subject is changed — the material never says who books the premises, naming the affected only as "invånarna" and "användarna", while "föreningslokaler" names a kind of premises. Writer: accepted and repaired to "ska föreningslokaler i Lervik … bara kunna bokas på webben". My class: **supported**. The material does name the affected people only as invånarna/användarna, and the draft's most prominent factual sentence had converted a kind of premises into a class of bookers.

Comparison 2 — `evidence/source-check-2/report.md`, one finding:

4. **F1** — draft passage "Bakom förslaget ligger åtta veckors försök i två av sju lokaler", echoed by "i stället för på åtta veckor i två lokaler". Alleged: the counts, duration and scope are supported but the evidential relation is not; the material states the proposal's motive flatly and differently and nowhere says the tjänsteutlåtande draws on, cites or was prompted by the pilot. Writer: accepted as unresolved and deliberately not repaired, because repairing after the final comparison would deliver prose no checker had read; carried to the delivery account instead. My class: **disputed**. The material settles it neither way — it neither states the link nor excludes it — and the reading turns on whether *bakom förslaget ligger X* asserts the proposal's grounds or names the evidence that stands behind the decision, which the brief's own framing of "beslutsunderlaget" leaves open. My reasoning is set out in full under F1.

The editorial questions both reports raise are recorded as questions, not findings, and I agree with that classification in all four cases: comparison 1's A (whether "verkligt" is predicated of the objection or of the double work — acted on voluntarily, and the repaired subheading now matches the material's "verkliga invändning") and B (no quotation marks occur, so the quotation guidance has nothing to act on); comparison 2's "människor" for "unika personer" and "Vi i föreningen" from a talesperson.

**Did a real defect I found under F1 go unseen by every checker?** No. I found no unsupported addition, changed term, changed subject, changed scope, date, modality or certainty, dropped caveat, invented event or invented personal attribute that no checker saw. The two passages I weighed on my own — the inference that the pilot's two premises are among the seven, and the standfirst's compressed modality, which "enligt tjänsteutlåtandet" carries and the lead immediately makes explicit — are defensible as written, not defects. Both remaining open questions in the text were seen.

## 12. Remaining findings

The delivery account reports exactly one finding as remaining.

- **Passage:** "Bakom förslaget ligger åtta veckors försök i två av sju lokaler" in the standfirst, with the echo "i stället för på åtta veckor i två lokaler" in the final paragraph.
- **What the account says is wrong:** "antalen, längden och omfattningen är belagda, men *kopplingen* är det inte. 'Bakom förslaget ligger X' påstår att förslaget vilar på X."
- **What the material carries instead:** "Motivet i utlåtandet är att personalen ska slippa föra in uppgifter i två flöden." The account adds: "Ingenstans sägs att tjänsteutlåtandet bygger på, hänvisar till eller föranleddes av pilotrapporten."
- **Proposed repair, as reported:** in the standfirst, "Det enda försök som gjorts är åtta veckor i två av sju lokaler"; in the close, "i stället för på handlingar utan en enda siffra för tid eller kostnad".

**Is it a defect of the text?** Under F1 I class it **disputed**, not an established defect: the material neither states nor excludes the relation, and the text itself states the proposal's actual motive plainly in its second section, so the reader is not misled about what the tjänsteutlåtande argues. The account's own framing — "Det är vad kontrollen hävdar och vad du som redaktör avgör, inte en fastslagen defekt i texten" — matches what the material supports. The text is nonetheless labelled as carrying a reported open question at this passage, and the proposed repair is small and leaves the thesis untouched.

## 13. Class of the run

**`valid delivery`.**

The run completed two comparisons and delivered. The prose delivered had a completed comparison of its own: comparison 2 read exactly these bytes (md5 `bdae9acd0e9d31af181b7cb61651f63c` on both `evidence/source-check-2/draft.md` and `delivered.md`), reported "Comparison complete", and no repair followed it. The one finding that comparison left unrepaired is reported beside the draft, at the top of the reply, with the passage, the allegation, what the material carries instead and the proposed repair — which satisfies the reporting requirement, so the "unresolved mandatory findings not reported" rejection does not apply.

None of the five unconditional rejections is triggered. No unsupported fact survives into the delivered text; the locale is Swedish throughout, as resolved; no substantive mechanical editing occurred; the remaining finding is reported; and the reply states the output form was the response itself, with nothing written to disk, so no side effect was claimed beyond the delivery.
