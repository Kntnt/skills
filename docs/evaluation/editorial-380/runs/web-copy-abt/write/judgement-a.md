# Judgement A — runs/web-copy-abt/write

Genre: `web-copy` (declared in the brief's assignment and in the delivered text's `kntnt` metadata). The anatomy skeleton therefore does not apply to this text; the script's figures are description, and no count makes a failure on its own.

## 1. Outcome

**Delivered.** The reply carries the draft in a fenced block under the heading *"Utkastet levereras med kända brister."*, and `delivered.md` exists.

**Two source comparisons completed.** The evidence shows two prompts (`evidence/source-check/prompt-1.md`, `prompt-2.md`), two drafts (`draft.md`, `draft-2.md`) and two checker replies. Comparison 1's reply ends *"Comparison complete. … 21 claim pairs accounted for, 20 supported, 1 finding."*; comparison 2 ends *"Comparison complete."* in both `report-2.md` and `reply-2.txt`. Comparison 1's report file does not survive and the caller's capture of its reply is truncated at the start (`reply-1-truncated-by-caller.txt` opens mid-document at *"## 3. Findings"*), so that comparison's claim accounting cannot be reviewed; its findings section and completion status survive whole. The reply states this limitation itself.

**The delivered prose is byte-identical to the last prose a checker saw.** `diff evidence/source-check/draft-2.md delivered.md` is empty, and `prompt-2.md` names `draft-2.md` as the draft under comparison. The only repair the run made is verifiable in the evidence: `draft.md` carries *"Har ni det, finns underlaget som genomgången utgår från."* and `draft-2.md` does not; the two files are otherwise identical. No prose changed after comparison 2, as the reply asserts (*"efter den sista jämförelsen ändras ingen prosa"*) and the byte comparison confirms.

## 2. Headings

Every heading in the delivered text, one to a line.

- H1 `Genomgång av bokningsrutinen för en gemensam lokal` — **label**, **echo**
  - A plain name for what the page holds, not a clause. Marked *echo* because the standfirst's first clause restates it in verb form (*"Svale går igenom hur bokningen av föreningens gemensamma lokal fungerar i dag"*): *genomgång/går igenom*, *bokningsrutinen/bokningen*, *gemensam lokal/gemensamma lokal*. The echo is partial — the standfirst goes on to add the audience, the bounded scope and the deliverable, which the headline does not carry.
- H2 `Det här ingår` — **label**
- H2 `Det här ingår inte` — **label**
- H2 `Pris och förutsättningar` — **label**
- H2 `Så anmäler ni intresse` — **label**

No heading is marked **colon**, **question** or **overclaim**. No H2 is marked *echo*: each shares only its unavoidable topic noun with the sentence under it (*pris* / *"Fast pris är …"*, *intresse* / *"En intresseanmälan …"*), which is naming the subject rather than repeating the wording. No heading claims anything the section beneath it does not carry, and none claims it at a higher strength.

## 3. F1 — **fail**

Two unsupported additions stand; one further reported finding I do not count as a defect.

**(a) "Uppdraget består av två delar:" — unsupported exhaustiveness.** The material says *"Genomgången omfattar ett videomöte på 45 minuter med två representanter för styrelsen och en skriftlig sammanställning av nuvarande steg, oklarheter och två möjliga förenklingar."* *Omfattar* includes; *består av två delar* asserts that there are exactly two and no more. A case compatible with the material: the genomgång also involves a short written questionnaire sent before the meeting. The material's sentence still holds; the draft's fails. Nothing supplied excludes it — the exclusion list names only *"juridisk rådgivning, installation av bokningssystem eller intervjuer med boende"*, and *avgränsad* bounds the engagement without fixing a count of parts. This is a modality change, not a preference. Reader effect: a board reads a closed inventory of the engagement where the material offers an open one.

**(b) "I formuläret anger ni namn, förening och e-postadress." and "— länken öppnar Svales formulär för intresseanmälan." — unsupported submission mechanism.** The material says only *"Intresseanmälan sker på https://example.invalid/svale/intresse och efterfrågar namn, förening och e-postadress."* Nothing supplied names a form. A compatible case: the destination is a page giving an address and instructions to send the three items. The material's sentence holds; *"länken öppnar Svales formulär"* fails. Manner of submission is circumstantial detail, and circumstantial detail is a claim. The run's own reply names this passage and offers mechanism-neutral wording, so it is honestly flagged — but it is still an addition the material does not carry. Reader effect: minor; the reader expects a form field and may meet something else.

**(c) "för att stämma av om uppdraget passar er förening" — not counted as a defect.** The material says *"för att stämma av om uppdraget passar"*, leaving the complement unstated. Supplying *er förening* adds no new entity — the förening is the addressee throughout — and reads the incomplete predicate the way a client-facing sentence ordinarily reads it. That is a reading the material leaves open rather than a fact added to it. I record it as **disputed** in section 6 and do not count it under F1.

**Checked and found supported**, against the material's own words: the price and its VAT status (*"Fast pris är 4 800 SEK inklusive moms."*, verbatim, SEK uncon­verted); the scope limit (*"Uppdraget gäller en lokal i en förening."*, verbatim); the exclusions; the absence of a guarantee (*"Någon garanti för en viss tidsbesparing eller för färre konflikter lämnas inte."* against *"Ingen garanti lämnas för en viss tidsbesparing eller färre konflikter."* — negation and scope preserved); the three requested items; the three-working-day e-mail reply; *"föreslå en tid för mötet"* against *"föreslå mötestid"* (proposing, not booking); *"En intresseanmälan är inte en beställning, och den kräver inga betalningsuppgifter."*; and the benefit formula *"en gemensam bild av rutinen och två möjliga förenklingar"*, which is the material's own sentence. No payment terms and no delivery time for the sammanställning appear anywhere in the text, which the material forbids inventing. No customer quotation, rating, trial, remaining place, campaign date or competitor comparison appears. No causal claim appears: the page nowhere says the genomgång saves time or reduces conflict.

*"Styrelsen behöver kunna beskriva föreningens befintliga bokningsregler"* changes the material's reflexive *"sina"* to *"föreningens"*. I name no case in this context in which a board holds booking rules for the common lokal that are not the association's, so I do not count it. Unknown is kept apart from absent throughout: the text nowhere converts the material's silences into denials.

## 4. G1 — **pass**

The named reader is a small association's board deciding whether a review is relevant and what an expression of interest entails. The page answers both in its own structure: what the engagement is, what it is not, what it costs, what the board must be able to produce, and what happens after the form. *"En intresseanmälan är inte en beställning, och den kräver inga betalningsuppgifter."* answers the second question directly; *"Därefter svarar Svale via e-post inom tre arbetsdagar"* tells the reader what follows. The angle — a bounded engagement with no promised outcome — is recognisable and held from the standfirst's *"är avgränsat"* to the closing microcopy. The boundaries note's trap is avoided: the link reads *"Skicka en intresseanmälan"*, not *Boka*, and the microcopy names the destination as the intresseanmälan, not a booked meeting. The page addresses the board's task, not an abstract decision-maker. What the reader can do: judge relevance against stated conditions, and send a non-binding expression of interest knowing what it commits them to.

## 5. G2 — **pass**

The anatomy scale is advisory for this genre: `web-copy` does not carry the four article genres' skeleton, so the script's `"conforms": false` with `failures` naming `byline` *absent* and `lead` *absent* is description here, not a requirement missed. A service page under a named sender with no author is ordinary web copy, and the sender is named in the copy itself (*"Svale går igenom …"*, *"Därefter svarar Svale …"*).

Judged on the Web-copy clause — useful information and choice, conditions, and accurate next-step consequence — each part does a distinct job. The headline names the service. The standfirst (script: `standfirst.words` 42, `paragraphs` 1) stands alone: it names the provider, the deliverable, the audience and the bounded scope without needing the body. The four sections do not overlap: inclusions, exclusions, price and prerequisites, and the route in. Conditions are easy to find and are not buried — they hold a heading of their own, *"Pris och förutsättningar"*. The next-step consequence is stated accurately at the point of action: *"[Skicka en intresseanmälan](https://example.invalid/svale/intresse) — länken öppnar Svales formulär för intresseanmälan."* names where the link goes and what it is not, and the section above it already says the anmälan is not an order. The one lapse is that the microcopy specifies a *formulär* the material does not name (see F1(b)); the consequence named — that the destination is the intresseanmälan — is accurate.

## 6. P1 — **pass**

The reasoning is a reader can follow without prior knowledge: nothing is used before it is introduced. *Genomgången* in section two refers back to the standfirst's description; *"Uppdraget"* is established in the standfirst before the price section uses it. The one real transition, *"Därefter svarar Svale via e-post inom tre arbetsdagar"*, puts the reply after the anmälan and is the material's own sequence. Conclusions are proportionate to visible support — the page draws no benefit it cannot show, and states the limit explicitly: *"Någon garanti för en viss tidsbesparing eller för färre konflikter lämnas inte."* Useful technical substance survives in full: 45 minutes, two board representatives, the three components of the written sammanställning, 4 800 SEK including VAT, one lokal in one association, three named form fields, three working days.

## 7. W1 — **pass**

The scale stays advisory for `web-copy`; the figures below describe rather than decide.

Script figures: `headline.characters` 50, `headline.words` 7; `standfirst.words` 42, `paragraphs` 1, `sentences_estimate` 2; `typical.paragraphs` 8, of which `paragraphs_of_two_or_three_sentences` 4; `typical.sections` 4, of which `sections_of_two_or_three_paragraphs` 2; `norms` is empty. The longest paragraph the script measures is 24 words (`Genomgången omfattar inte juridisk rådgivning …`), far inside the 80-word norm. Subheading lengths are 13, 18, 24 and 22 characters. No heading level below the second occurs; `parts.other` records only the bullet list in section 1.

A web reader can enter at any heading and get an answer without reading what precedes it, which is what this genre needs and what the brief's boundaries note asks for. The headings are informative labels rather than teasers. There is no separate lead part in this genre (`parts.lead` is null), so the standfirst/lead complementarity and the shared-first-word test do not arise. The standfirst carries the whole promise, and the body covers it: bounded scope, shared picture of the routine, two possible simplifications. Nothing is lost to density or fragmentation — the bullet list holds the two components that the eye needs to compare, and the prose around it is continuous. Voice is steady across the page.

## 8. L1 — **pass**

The Swedish is idiomatic and reads as written rather than rendered. *"Det här ingår"* / *"Det här ingår inte"* is the natural Swedish pair for a service page; *"Så anmäler ni intresse"* is the ordinary Swedish how-to heading; *"Fast pris är 4 800 SEK inklusive moms."* is the plain commercial register. *"Någon garanti … lämnas inte"* places the negation where Swedish places it, and *"ta ställning till"* is native idiom, not a calque. The second-person plural address (*ni*, *er*) is the standard Swedish form for addressing a board, and is held consistently. No English syntax or generic translated phrasing intrudes.

## 9. L2 — **pass**

Locale `sv`, declared in the text's metadata. The number form is Swedish: *"4 800 SEK"*, space-separated thousands, currency after the figure — and it is byte-identical to the material's own *"4 800 SEK"* (both `34 20 38 30 30 20 53 45 4b`), so no new figure and no conversion was introduced, as the boundaries note requires. *"inklusive moms"* is the Swedish VAT formulation. Swedish diacritics are correct throughout. Punctuation is Swedish: the comma before *och* in *"är inte en beställning, och den kräver …"* is acceptable variation, and the single em dash introducing the link microcopy is used as a Swedish parenthetical dash. No date appears, so none was invented. The URL is carried unchanged.

## 10. T2 — **pass**

A technique is named: the delivered text's metadata carries `technique: abt`, and the reply states *"**Teknik:** `abt`, angiven i anropet"*.

The ABT parts relate without invented crisis or triumph. Situation: the standfirst's *"Svale går igenom hur bokningen av föreningens gemensamma lokal fungerar i dag … och är avgränsat"*. Complication: the page's genuine limits, not a manufactured problem — *"Genomgången omfattar inte juridisk rådgivning, installation av bokningssystem eller intervjuer med boende."* and *"Någon garanti för en viss tidsbesparing eller för färre konflikter lämnas inte."*, both the material's own. Response: *"En intresseanmälan är inte en beställning, och den kräver inga betalningsuppgifter."* followed by the fit check, which is the warranted next step given a bounded engagement with no promised outcome. Crucially, the text invents no crisis to be solved — it never asserts that booking today causes conflict or wasted time, which the material would not support — and it claims no triumph, since it withholds the outcome the material withholds. The arc sits at section level, which the criterion allows.

## 11. Checker findings

Comparison 1 (report file absent; taken from `reply-1-truncated-by-caller.txt`, whose findings section and completion status survive intact):

- **F1 — "Har ni det, finns underlaget som genomgången utgår från."** Alleged: a necessary condition (*"Styrelsen behöver kunna beskriva sina befintliga bokningsregler och visa nuvarande instruktion till de boende."*) restated as a sufficient one, plus a new claim about what the genomgång proceeds from. Writer: repaired by deleting the sentence — `draft.md` carries it, `draft-2.md` does not, and the files are otherwise identical. **My class: supported.** The material states a requirement and never says the two items constitute or suffice as the basis of the genomgång.

Comparison 1 also raised two items it marked *"Editorial questions (not defects)"* — the shortfall against *"cirka 300 ord"*, and *"att ta ställning till"* — and reported neither as a finding. Its completion status names one finding.

Comparison 2 (`report-2.md`, 21 claim pairs plus a separate pronoun accounting):

- **F1 — "Uppdraget består av två delar:"** Alleged: the material's inclusive *"Genomgången omfattar … och …"* made exhaustive. Writer: not repaired; reported in the delivery account with the checker's own repair (*"Uppdraget omfattar:"*). **My class: supported** — see F1(a).
- **F2 — "för att stämma av om uppdraget passar er förening"** Alleged: the material's complementless *"för att stämma av om uppdraget passar"* narrowed to the association's side. Writer: not repaired; reported with the repair *delete "er förening"*. **My class: disputed** — the material leaves the complement unstated rather than settling it the other way, and supplying the addressee is a reading the material leaves open, not a fact added to it.
- **Q1 — "I formuläret …" / "— länken öppnar Svales formulär för intresseanmälan."** Alleged, but explicitly reported as the material's silence rather than a defect: the draft names a submission mechanism the material does not name. Writer: not repaired; raised in the reply as an open editorial question with mechanism-neutral alternatives. **My class: supported.** By the report's own test a compatible case stands in which the material's sentence holds and the draft's fails, so this belongs among the findings rather than beside them.

**Did a real defect under F1 escape every checker?** No. Both defects I count were seen: F1(a) was reported as a finding by comparison 2, and F1(b) was seen by comparison 2 but filed as an editorial question rather than a defect. I find no unsupported addition that neither comparison noticed.

## 12. Remaining findings

The delivery account reports two findings as remaining, and the delivered prose is byte-identical to the prose the last comparison read.

1. **"Uppdraget består av två delar:"** — the material carries instead *"Genomgången omfattar ett videomöte på 45 minuter med två representanter för styrelsen och en skriftlig sammanställning av nuvarande steg, oklarheter och två möjliga förenklingar."* Proposed repair, as the account gives it: replace the line with *"Uppdraget omfattar:"* and leave both bullets standing. **Under F1 this is a defect** — F1(a).
2. **"för att stämma av om uppdraget passar er förening"** — the material carries instead *"Svale svarar via e-post inom tre arbetsdagar för att stämma av om uppdraget passar och föreslå mötestid."* Proposed repair: delete *"er förening"*. **Under F1 this is not a defect** — F1(c); it turns on a complement the material leaves open.

The account additionally names the *"formuläret"* / *"Svales formulär"* wording as an open editorial question with a proposed neutral alternative. **Under F1 that one is a defect** — F1(b) — even though neither the checker nor the account classes it as such.

## 13. Class of the run

**`valid delivery`.** The prose the run delivered had a completed comparison of its own: comparison 2 read `draft-2.md`, its report ends *"Comparison complete."*, and the delivered text is byte-identical to that file. The run delivered it rather than withholding it, stated plainly at the head of the reply that it ships with known defects, and reported both unrepaired findings beside the draft with the passage, the material's wording and the smallest proposed repair. It also disclosed the limit on comparison 1's evidence instead of glossing it. The text still carries a remaining quality problem — F1 fails on the exhaustiveness claim and the unsupported submission mechanism — but reporting was satisfied, no side effect was incorrect, the locale held, and no mandatory finding went unreported.
