# Judgement B — web-copy-sv / write

## 1. Outcome

**Delivered.** `delivered.md` is present and the reply carries the draft in a fenced block.

**Two source comparisons, both completed.** `evidence/source-check/` holds `task-1.txt` and `task-2.txt` (identical but for the report path), `report-1.md` and `report-2.md`, and `dispositions-1.md` and `dispositions-2.md`. Each report ends with a completion status: report 1, "Comparison complete. All 20 factual and attributed claims in the draft … are accounted for"; report 2, "Comparison complete. The full draft … has been accounted against `material.md`". Each report is a full claim accounting over the whole text, not a spot check, and each has a matching disposition file that checks coverage before ruling. The reply agrees: "Två fullständiga källkontroller, båda av färska granskare utan samtalshistorik." The two reports quote different prose — report 1 quotes "I formuläret anger du …", "två förenklingar", "den instruktion som de boende har i dag"; report 2 quotes "Den efterfrågar namn …", "två möjliga förenklingar", "nuvarande instruktion till de boende" — which confirms the second comparison read the repaired text, not the first draft.

**Byte-identical: yes.** `evidence/source-check/draft.md` is the file both tasks name as the draft, and it holds the repaired prose the second comparison read. Stripping the seven-line `kntnt` frontmatter from `delivered.md` leaves a file that compares byte-for-byte equal to `evidence/source-check/draft.md` (`cmp` reports no difference). `evidence/source-check/draft-v1.md` differs from it in exactly the three lines repaired after report 1. No repair was made after the last comparison: `dispositions-2.md` states "This one is final, so no prose changes after it; only the Handoff Metadata and the delivery wrapper were added", and the diff bears that out — the only addition is the frontmatter, which is metadata and not prose.

**Side effects.** `evidence/source-check/material.md` is identical to `work/source.md` (`diff` reports no difference), so the supplied material was not modified. Whether the run's scratch files were removed as the reply claims is not settleable from the files I am permitted to read; I record it as unverified rather than estimating.

## 2. Headings

Level-1 headline:

- `Genomgång av bokningsrutinen för föreningens gemensamma lokal` — **label**, **echo**, **overclaim**
  - *label*: a noun phrase naming what the page holds, understandable on its own.
  - *echo*: the standfirst's first clause restates it in fuller form — "en avgränsad genomgång av hur bokningen av en gemensam lokal fungerar i er förening" carries *genomgång*, *bokning*, *gemensam lokal* and *förening* over again. The echo is partial: the standfirst does add the two proposals and the addressee.
  - *overclaim*: the definite genitive presupposes the reader's förening has one common lokal. The text itself carries only the indefinite — "av en gemensam lokal" in the standfirst, "Uppdraget gäller en lokal i en förening" in the price section. This is a presupposition, not an assertion, and the body states the indefinite twice; see F1 and §7.

Level-2 subheadings:

- `Det här ingår i genomgången` — **label**
- `Det här ingår inte i genomgången` — **label**
- `Pris och omfattning` — **label**
- `Förutsättningar` — **label**
- `Så anmäler ni intresse` — **label** (clause-shaped, but it names the step the section holds rather than asserting a proposition)

No subheading carries a colon, a question, an echo of its own first sentence, or an overclaim. Where a heading and the sentence under it share a word — *Pris* / "Fast pris är …", *intresse* / "En intresseanmälan …" — that is the section's topic term, not a repetition of the sentence's phrasing, so it is not marked *echo*.

These marks are evidence for G2 and W1 below, not verdicts.

## 3. F1 — pass

I compared every assertion in `delivered.md` against `work/source.md` myself.

Carried exactly, with figures, qualifiers and prohibitions intact:

- "Ett videomöte på 45 minuter med två representanter för styrelsen" and "En skriftlig sammanställning av nuvarande steg, oklarheter och två möjliga förenklingar" — both verbatim from "Genomgången omfattar …", the qualifier *möjliga* kept.
- "Juridisk rådgivning, installation av bokningssystem och intervjuer med boende" — the same three exclusions; the negation moves into the heading and still negates all three, so *eller* → *och* changes nothing.
- "Fast pris är 4 800 SEK inklusive moms. Uppdraget gäller en lokal i en förening." — verbatim, currency unconverted, thousands separator as the source writes it.
- "Svale lämnar ingen garanti för en viss tidsbesparing eller för färre konflikter." — the source's agentless "Ingen garanti lämnas …" entails it; both qualifiers kept.
- "En intresseanmälan är ingen beställning och kräver inga betalningsuppgifter. Den efterfrågar namn, förening och e-postadress." — both negatives and all three fields from the source.
- "Svale svarar via e-post inom tre arbetsdagar" — channel and deadline verbatim.
- `https://example.invalid/svale/intresse` — character-for-character identical, and the label "Skicka en intresseanmälan" does not claim the meeting is booked, which the brief's boundary requires.
- Absences preserved: no payment terms, no delivery time for the sammanställning, no competitor comparison, no testimonial, rating, trial, vacancy, campaign date or guarantee. Nothing unstated is converted into a claim that it does not exist.

Departures I found, each named and weighed:

1. **"föreningens gemensamma lokal" (headline).** The material has "en gemensam lokal" and "Uppdraget gäller en lokal i en förening". The definite genitive presupposes a single common lokal. A förening with a festlokal and a gästlägenhet is compatible with the material, so the presupposition is unsupported. It is not an asserted fact, the reader meets the source's own indefinite wording twice in the body before any commitment, and the engagement limit is quoted verbatim under *Pris och omfattning*. **Qualitative concern, not a contract rejection.**
2. **"om uppdraget passar er" (Så anmäler ni intresse).** The material's "för att stämma av om uppdraget passar" carries no complement; the draft supplies one and so states whose fit is checked. A case stands in which Svale's own check is what the e-mail is for — the förening wants three lokaler or legal advice and Svale declines. This is a real departure: the draft narrows a described purpose the material leaves open. It invents no fact, figure, date or offer, and it resolves an elided complement in the direction the surrounding sentence ("föreslå mötestid") most supports. **Qualitative concern, and a remaining defect of the text; not a contract rejection.**
3. **"Genomgången vänder sig till styrelsen i en mindre bostadsrättsförening."** The brief fixes the *page's* reader ("Skriv en tjänstesida för mindre bostadsrättsföreningars styrelser"); the draft states whom the *service* addresses. "Vänder sig till" is an addressing statement and excludes nobody, and a sender's page saying whom it is for is the ordinary way a brief's audience enters copy. **Not a defect.** Both checkers reached the same reading independently.
4. **"föreningens befintliga bokningsregler"** for the source's "sina befintliga bokningsregler". In a bostadsrättsförening whose board is the addressed party, the two expressions pick out the same rules; the demand made of the reader is unchanged and "befintliga" is carried. I can name no compatible case in which a board can describe the one set and not the other. **Not a defect.**
5. **"Svale gör"** for "Svale erbjuder", and **"i dag"**. "Gör" is how an offeror's own service page reads, and the material has Svale performing the follow-up itself ("Svale svarar via e-post"); "i dag" rests on "nuvarande steg" and "nuvarande instruktion". **Not defects.**
6. **"Efter genomgången har styrelsen …"** does not invent a *leveranstid*, because the material puts the sammanställning inside the genomgång ("Genomgången omfattar … och en skriftlig sammanställning"). The prohibition "hitta inte på dem" is respected. **Not a defect.**

Terms checked in both directions where they changed: *rutinerna för bokning* / *bokningsrutinen* (collective singular denotes the same object; the body's "nuvarande steg" shows the plural is not lost), *möjliga förenklingar* / *förslag på hur rutinen kan förenklas* (the modal *kan* carries the qualifier), *mötestid* / *en tid för mötet* (the definite resolves to the one meeting the material names). No claim crosses a language boundary: brief, material and draft are all Swedish, and the draft contains no quotation.

Unknown is kept apart from absent: the page nowhere says Svale is a firm or a person, nowhere says what form the anmälan takes, and nowhere says when the sammanställning arrives — each of those the material leaves unknown, and the draft leaves them unknown too.

**Verdict: pass.** Nothing is invented, no caveat is dropped, no figure, date, currency or attribution is changed. The text carries one remaining quality problem, item 2, and a marginal presupposition, item 1; both are reported beside the draft.

## 4. G1 — pass

The brief names the reader and the task: boards of smaller bostadsrättsföreningar "som behöver avgöra om en genomgång av bokningsrutinerna är relevant och vad en intresseanmälan innebär".

The reader can decide relevance: they learn what the genomgång is ("Svale gör en avgränsad genomgång av hur bokningen … fungerar i er förening i dag"), what they receive ("Ett videomöte på 45 minuter …", "En skriftlig sammanställning …"), what they do not receive ("Juridisk rådgivning, installation av bokningssystem och intervjuer med boende"), what it costs, what the engagement covers, what is not promised ("Svale lämnar ingen garanti för en viss tidsbesparing eller för färre konflikter") and what they must be able to produce ("Styrelsen behöver kunna beskriva föreningens befintliga bokningsregler och visa nuvarande instruktion till de boende").

The reader can also answer the second question. "En intresseanmälan är ingen beställning och kräver inga betalningsuppgifter" tells them what they are committing to; "Den efterfrågar namn, förening och e-postadress" tells them what it asks; "Svale svarar via e-post inom tre arbetsdagar" tells them what follows.

The brief's boundaries are met. There is no abstract framing of "beslutsfattare i en komplex verklighet" — every sentence is about this service. The link is labelled "Skicka en intresseanmälan", not *Boka*, and implies no direct booking. Terms, price and what happens next each have a section of their own and are easy to find. Sections open directly on their content, with no throat-clearing sentence before the bullets or before "Juridisk rådgivning …", and nothing is repeated unnecessarily.

The one micro-copy point worth naming is that "Skicka" sits on a link whose destination is a page the reader still has to fill in. The section immediately above explains exactly that, so the reader is not misled about the consequence. Angle is recognisable and held: this is a bounded review of one thing, priced, with stated limits.

## 5. G2 — pass

**The scale is advisory for this genre.** The genre is `web-copy`, declared in the text's own metadata (`genre: web-copy`) and set by the brief ("Skriv en tjänstesida"), so the article skeleton does not apply. `anatomy-delivered.json` reports `"conforms": false` with `failures` for `byline` ("absent") and `lead` ("absent"); for web-copy those figures are description, not requirement, and neither makes a failure on its own. A service page carries no byline — the reply states the choice and its reason ("Sidan är avsändarmärkt med Svale, som underlaget anger") and the material's "Avsändare är Svale" supports it — and a service page needs no lead distinct from its opening paragraph.

Judged on the criterion's own words and its `Web-copy` clause — useful information/choice, conditions, and an accurate next-step consequence:

- **Useful information and choice.** The two bullets and the outcome sentence say what the reader gets; the exclusion section says what they do not. Together these let the board choose rather than merely admire.
- **Conditions.** Price, engagement scope, the absence of a guarantee and the two prerequisites each sit under their own heading: "Fast pris är 4 800 SEK inklusive moms. Uppdraget gäller en lokal i en förening." and "Styrelsen behöver kunna beskriva föreningens befintliga bokningsregler …".
- **Accurate next-step consequence.** "En intresseanmälan är ingen beställning och kräver inga betalningsuppgifter" plus "Svale svarar via e-post inom tre arbetsdagar för att stämma av om uppdraget passar er och för att föreslå en tid för mötet", closed by a link whose label names the notification and whose destination is the one the material gives. The consequence is stated before the reader clicks.

Every part does a distinct job: the headline names the service, the opening paragraph states what Svale does and for whom, and no section repeats another. The headline's *overclaim* mark stands (§2), but the two body statements carrying the source's indefinite wording keep the reader correctly informed about the engagement's extent, so it does not defeat this criterion.

## 6. P1 — pass

The reasoning a service page has to carry is a chain of conditions, and the order works: what the service is, then what is in it, then what is not, then price and limit, then what the reader must be able to do, then how to proceed. Nothing is used before it is introduced — "genomgången" is defined in the opening paragraph before five headings rely on the word, and "sammanställningen" is described by its contents at the point it first appears.

Conclusions stay proportionate to visible support. "Efter genomgången har styrelsen en gemensam bild av hur bokningen går till och två möjliga förenklingar att ta ställning till" is exactly what the two deliverables produce, with *möjliga* keeping the proposals as candidates, and the very next section refuses to go further: "Svale lämnar ingen garanti för en viss tidsbesparing eller för färre konflikter." The page draws no benefit it has not bought.

Useful technical substance remains and is not smoothed away: 45 minutes, two board representatives, three contents of the written summary, 4 800 SEK inklusive moms, one lokal in one förening, three named exclusions, two prerequisites, three working days, three requested fields. The transitions between sections are structural rather than rhetorical, which is the right choice for a page a board scans while deciding.

## 7. W1 — pass

**The scale stays advisory for this genre** (`web-copy`), so the script's figures support judgement and no count fails anything on its own.

`anatomy-delivered.json` reports `typical`: `paragraphs` 9, `paragraphs_of_two_or_three_sentences` 3, `sections` 5, `sections_of_two_or_three_paragraphs` 2. Under `norms` it reports the headline at `"61 characters"` against "It should be at most 60 characters", with `parts.headline.words` 7. For web-copy that single character over is description, not a departure to weigh. The standfirst measures `words` 36, `sentences_estimate` 2, `paragraphs` 1. Section paragraph counts, from `parts.sections`, are 1, 1, 2, 1 and 3; the bullet list is recorded under `parts.other` as "section 1".

A web reader orients immediately. Five scannable subheadings — 27, 32, 19, 15 and 22 characters by the script — name the question each section answers, so a board member hunting for the price or the prerequisites finds them without reading the page through. Paragraphs are one or two sentences and carry one idea each, which is the right rhythm here and produces no fragmentation: the short paragraphs are short because the facts are discrete, not because a continuous explanation has been chopped.

There is no separate lead, so the "standfirst and lead opening on different first words" test does not apply; `parts.lead` is `null`. The standfirst does stand alone and does open the work, and the body completes it — it promises a bounded review and two proposals, and both are delivered in the first section.

The one point of actual reader risk is that "Det här ingår i genomgången" and "Det här ingår inte i genomgången" differ by one word, so a fast scanner could take the second for the first. The pairing is a standard and well-understood web-copy convention, the negated word sits early in the heading, and the content under each is unmistakable, so I find no real reader loss. No heading level below the second is used.

## 8. L1 — pass

The Swedish is idiomatic and reads as professionally written service copy, not as translated English. Syntax is native throughout: "Svale gör en avgränsad genomgång av hur bokningen av en gemensam lokal fungerar i er förening i dag, och lämnar två förslag på hur rutinen kan förenklas" uses ordinary Swedish clause order and an ordinary Swedish way of packing two deliverables into one sentence. "Så anmäler ni intresse" is the natural Swedish heading for that step; a translated page would more likely produce *Hur du anmäler ditt intresse*.

Idiom is right at the level of the verb: *lämnar* a guarantee, *stämma av*, *ta ställning till*, *behöver kunna beskriva*. "Efter genomgången har styrelsen en gemensam bild av hur bokningen går till" uses *går till*, which is the idiomatic Swedish for how a procedure works, rather than a calque on *functions*. Address is consistent — *er förening*, *ni*, *er*, with no drift into the singular *du*.

"Den efterfrågar namn, förening och e-postadress" is the most administrative sentence on the page, *efterfrågar* being a shade formal for web copy, but it is the material's own verb and stays within professional register. No anglicisms, no noun-heavy constructions, no imported English phrasing.

## 9. L2 — pass

The resolved locale is Swedish (`language: sv` in the delivered metadata, `sv` in the brief and in `context.md`).

- **Spelling and orthography:** Swedish throughout, with å/ä/ö correct in every position — *Genomgång*, *förening*, *e-postadress*, *förutsättningar*, *rådgivning*.
- **Compounds:** written solid as Swedish requires — *bokningsrutinen*, *bokningssystem*, *intresseanmälan*, *bokningsregler*, *tidsbesparing*, *videomöte*, *bostadsrättsförening*.
- **Numbers:** "4 800 SEK" uses a space as the thousands separator, the Swedish convention, and reproduces the source's own spacing byte for byte. "45 minuter" and "tre arbetsdagar" follow Swedish practice of spelling small numbers.
- **Currency:** SEK is retained and not converted, as the brief's boundary requires ("Engelska utkast behåller SEK och destinationen"); the Swedish page has no reason to convert and does not.
- **Dates:** none appear, and none is invented. No factual date or conversion is introduced anywhere.
- **Punctuation and capitalisation:** Swedish sentence case in every heading; no title case imported. The one comma before *och* in the opening sentence separates two full clauses, which Swedish allows. No quotation marks are used, so no locale quote-mark question arises.

No established variation is disturbed: *Svale* keeps its form, and the URL is unchanged.

## 10. T2 — skipped

No technique was selected. The delivered text's own metadata records `technique: none`, and the reply states it in its own words: "**Teknik:** ingen. Web-copy anger ingen teknik som genren vanligen skrivs med, och ingen teknik kom från anropet, från underlagets frontmatter eller från någon instruktion." Neither ABT nor PAC is named as selected anywhere in the metadata or the reply, so nothing is judged under this criterion. I do not infer a technique from the shape of the prose.

## 11. Checker findings

Findings in `report-1.md` (read against the prose preserved as `evidence/source-check/draft-v1.md`):

| # | Draft passage | What the checker alleged | What the writer did | My class |
|---|---|---|---|---|
| R1-F1 | "I formuläret anger du namn, förening och e-postadress." | "I formuläret" asserts a form as the means; the material says only "Intresseanmälan sker på [URL] och efterfrågar namn, förening och e-postadress" and fixes the location, not the mechanism | ACCEPTED (`dispositions-1.md`); repaired one degree smaller than proposed, to "Den efterfrågar namn, förening och e-postadress" | `supported` |
| R1-F2 | "… och två förenklingar att ta ställning till." | Drops *möjliga*, which the material carries in both places it names the pair, so the sentence asserts the board receives simplifications rather than candidates | ACCEPTED; repaired as proposed to "två möjliga förenklingar att ta ställning till" | `supported` |
| R1-F3 | "… och visa den instruktion som de boende har i dag." | Renames the document from one *addressed to* residents ("nuvarande instruktion till de boende") to one residents *hold*, changing the precondition the reader tests themselves against | ACCEPTED; repaired as proposed, restoring the source's wording | `supported` |

Editorial questions raised by report 1, which that report itself declines to call findings: **Q1**, the headline's definite "föreningens gemensamma lokal" (referred, no change); **Q2**, "du" at line 28 against "ni/er" elsewhere (referred; removed incidentally by the F1 repair).

Findings in `report-2.md`, the final comparison:

| # | Draft passage | What the checker alleged | What the writer did | My class |
|---|---|---|---|---|
| R2-F1 | "Genomgång av bokningsrutinen för **föreningens gemensamma lokal**" | The definite genitive presupposes one common lokal and drops the stated one-lokal limit at the point it is first asserted; a förening with a festlokal and a gästlägenhet is compatible with the material | ACCEPTED as a remaining finding (`dispositions-2.md`); repair not applied, because this was the final comparison and the prose delivered is the prose it read; reported to the user as item 1 | `disputed` |
| R2-F2 | "för att stämma av om uppdraget passar **er**" | The source's "stämma av om uppdraget passar" carries no complement; supplying "er" states whose fit is checked and excludes Svale's own check | ACCEPTED as a remaining finding; repair not applied, same reason; reported to the user as item 2 | `supported` |

Editorial questions raised by report 2, not alleged as defects: **Q1**, "Genomgången vänder sig till styrelsen i en mindre bostadsrättsförening" (the brief fixes the page's reader, not the service's); **Q2**, the shared picture ascribed to the whole board while two representatives attend. Both are carried into the reply under "Två redaktionella frågor", correctly labelled as questions rather than defects.

On R2-F1 I class the allegation `disputed` rather than `supported` because the material settles it neither way and the two checkers, reading independently, split on it — report 1 referred the identical passage as Q1 and report 2 established it as a defect. The reading turns on whether a Swedish generic definite asserts uniqueness, which the material leaves open.

**Did I find a real defect no checker saw?** No. Every departure I identified under F1 was examined by at least one of the two reports — items 1 and 2 as remaining findings, item 3 as Q1 in both reports, items 4 to 6 as cleared rows with reasoning I checked and agree with. The closest thing to an unexamined point is the link label "Skicka en intresseanmälan" on a destination the reader must still fill in; I judge it not a defect, since the section above it states the consequence plainly and the brief's boundary bars only a *Boka* label that implies the meeting is booked. Both reports checked the label against that boundary.

## 12. Remaining findings

The delivery account opens with them, before the draft: "**Utkastet levereras med kända brister.** Den avslutande källkontrollen lämnade två invändningar som inte är åtgärdade i texten."

1. > "Rubriken: 'föreningens gemensamma lokal'. Den bestämda formen förutsätter att föreningen har en enda gemensam lokal."

   **Passage:** the headline, "Genomgång av bokningsrutinen för föreningens gemensamma lokal".
   **What the material carries instead:** "en avgränsad genomgång av rutinerna för bokning av *en gemensam lokal*" and "Uppdraget gäller *en lokal i en förening*" — indefinite in both places, and the second a stated limit that contemplates more than one existing.
   **Proposed repair, as the account gives it:** "Genomgång av bokningsrutinen för en gemensam lokal".
   **Is it a defect?** Marginal. Under F1 I record it as an unsupported presupposition rather than an unsupported assertion: the reader meets the material's own indefinite wording twice in the body, including the engagement limit verbatim, before any commitment. It does not fail F1, and it is the basis of the headline's *overclaim* mark in §2.

2. > "'för att stämma av om uppdraget passar er'. Underlaget skriver 'för att stämma av om uppdraget passar', utan bestämning. Utkastet lägger till vems passform som prövas."

   **Passage:** "Svale svarar via e-post inom tre arbetsdagar för att stämma av om uppdraget passar er och för att föreslå en tid för mötet."
   **What the material carries instead:** "Svale svarar via e-post inom tre arbetsdagar för att stämma av om uppdraget passar och föreslå mötestid" — no complement on *passar*.
   **Proposed repair, as the account gives it:** "stryk 'er'".
   **Is it a defect?** Yes, and it is the text's remaining quality problem. The draft narrows a purpose the material leaves open, and the case in which Svale is checking its own fit and declining stands. It is a narrowing, not an invention, so under F1 it is a qualitative concern rather than a contract rejection.

The account states their status accurately and does not oversell it: "Båda är vad kontrollen hävdar och vad du som redaktör avgör, inte fastställda fel i texten." It also gives the two editorial questions separately, and names the length shortfall against the brief's "cirka 300 ord" with six specific items of material that would close it. Reporting is satisfied; the text is still labelled here as carrying a remaining quality problem at finding 2.

## 13. Class of the run

**`valid delivery`.**

The prose delivered had a completed comparison of its own and was delivered exactly as that comparison read it. Two full comparisons ran; the second read the repaired text (it quotes the repaired wording in 1.4, 1.7 and 1.8) and completed ("Comparison complete … **Unresolved findings: 2.**"). The delivered body is byte-identical to `evidence/source-check/draft.md`, the file that comparison was given, with only the `kntnt` frontmatter added afterwards. The two findings the final comparison left unrepaired are reported beside the draft, each with the passage, the source wording and the smallest supported repair, so nothing mandatory is unresolved and unreported. No unsupported fact is asserted, the locale is right, no substantive mechanical editing was performed in place of the work asked for, and the supplied material is unchanged on disk.
