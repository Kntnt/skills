# Judgement A — runs/web-copy-sv/write

Genre: `web-copy`, given by the brief ("Skriv en tjänstesida …") and by the delivered text's own metadata (`genre: web-copy`). The article anatomy therefore does not apply to this text; the script's figures are description, and no count fails anything on its own.

## 1. Outcome

**Delivered.** `delivered.md` is present and carries the full page; `response.md` contains it inside a fenced block under a delivery account.

**Two completed source comparisons.** `evidence/source-check/` holds `report-1.md` and `report-2.md`, each ending with an explicit "Completion status" section stating "Comparison complete", together with `dispositions-1.md` and `dispositions-2.md` and two identical checker task files (`task-1.txt`, `task-2.txt`, differing only in the report path). The reply corroborates: "Två fullständiga källkontroller, båda av färska granskare utan samtalshistorik." The evidence also shows why a second was needed: `dispositions-1.md` ends "Three repairs made, so a second comparison is required on the changed prose", and `draft-v1.md` differs from `draft.md` in exactly those three lines.

**The delivered prose is byte-identical to the last prose a checker saw.** Stripping the seven-line YAML frontmatter from `delivered.md` and diffing against `evidence/source-check/draft.md` — the file report 2 read — produces no difference at all. The only content in the delivered file that report 2 did not see is the `kntnt` map (genre, technique, language), which is metadata and not prose. `dispositions-2.md` states the same: "This one is final, so no prose changes after it; only the Handoff Metadata and the delivery wrapper were added." No repair is claimed or visible after the last comparison. Nothing here is unsettled by the evidence.

## 2. Headings

Every heading in the delivered text, one to a line.

- H1 — "Genomgång av bokningsrutinen för föreningens gemensamma lokal" — **label**, **echo**, **overclaim**.
  - *label*: a plain name for what the page holds (a noun phrase, no finite verb).
  - *echo*: it shares "genomgång", "gemensam lokal" and "förening(ens)" with the standfirst directly under it ("Svale gör en avgränsad genomgång av hur bokningen av en gemensam lokal fungerar i er förening i dag"). On a service page, naming the service in both places is close to unavoidable; the mark is recorded as evidence, not as a reader loss.
  - *overclaim*: the definite genitive "föreningens gemensamma lokal" carries at full strength what the body carries indefinitely — "en gemensam lokal" (standfirst) and "Uppdraget gäller en lokal i en förening" (Pris och omfattning). This is the same passage report 2 raised as its F1.
- H2 — "Det här ingår i genomgången" — **label**.
- H2 — "Det här ingår inte i genomgången" — **label**.
- H2 — "Pris och omfattning" — **label**. (It shares the topic word "pris" with the first sentence under it, "Fast pris är 4 800 SEK inklusive moms." A single topic noun in a two-word label is naming, not echoing phrasing.)
- H2 — "Förutsättningar" — **label**.
- H2 — "Så anmäler ni intresse" — **label**. It names the step without asserting that the meeting is booked, which the brief's boundary requires of a heading, button or link.

No heading is a question, none uses a colon for a verb, and no subheading repeats the first sentence under it or claims more than its section carries.

## 3. F1 — pass

Every figure, term, condition and next step in the delivered page is traceable to `work/source.md`, in the source's own words, and nothing the brief forbids appears.

Checked against the material, passage by passage:

- "Ett videomöte på 45 minuter med två representanter för styrelsen." and "En skriftlig sammanställning av nuvarande steg, oklarheter och två möjliga förenklingar." — verbatim from "Genomgången omfattar …", with the qualifier "möjliga" intact.
- "Juridisk rådgivning, installation av bokningssystem och intervjuer med boende." — the three exclusions verbatim; the negation moves into the heading and all three stay excluded.
- "Fast pris är 4 800 SEK inklusive moms. Uppdraget gäller en lokal i en förening." — identical to the source, including the currency. No conversion, no payment terms, no delivery time for the sammanställning — the two things the brief names as unstated ("hitta inte på dem") are absent.
- "Svale lämnar ingen garanti för en viss tidsbesparing eller för färre konflikter." — the source's agentless "Ingen garanti lämnas …" entails it; both qualifiers are carried.
- "Styrelsen behöver kunna beskriva föreningens befintliga bokningsregler och visa nuvarande instruktion till de boende." — the second conjunct is now the source's own wording. "sina" → "föreningens" changes the possessor's name, but in this material there is only one set of booking rules and the demand made of the reader is unchanged; not a defect.
- "En intresseanmälan är ingen beställning och kräver inga betalningsuppgifter. Den efterfrågar namn, förening och e-postadress." — carried from "Den är inte en beställning och kräver inga betalningsuppgifter" and "efterfrågar namn, förening och e-postadress". The earlier draft's unsupported "I formuläret" is gone.
- "[Skicka en intresseanmälan](https://example.invalid/svale/intresse)" — the destination is character-for-character the supplied one, and the label names the interest notification rather than a booking, as the brief's boundary demands.
- No customer quote, rating, trial, vacancy, campaign date, guarantee or competitor comparison appears — each of which the material states does not exist.
- Unknown is kept apart from absent: the page nowhere converts an unstated term into a claim that no such term exists. The one absence it asserts (no guarantee) is the one the material asserts.

Translated-term check in both directions: none arises. Source and draft are both Swedish, and the page contains no quoted speech.

**On the two findings the delivery account reports as remaining, and whether each is a defect:**

- "om uppdraget passar **er**" **is** a small defect. The source clause is "för att stämma av om uppdraget passar", with no complement; the page supplies one and so states whose fit is being tested. A case compatible with the material stands: Svale checks whether the enquiry falls inside its own bounded offer — three lokaler, or legal advice — and declines. I record it as a genuine unsupported specification. It fails no fact, figure, date, condition or next step, invents no event and drops no caveat, and the reader's actionable expectation (an e-mail reply within three working days, fit checked, meeting time proposed) is unchanged. It is a qualitative concern at the margin of F1, not a contract rejection, and it does not carry F1 to a failure on its own.
- "föreningens gemensamma lokal" in the H1 **is not** a defect I can establish. It is marked *overclaim* above as evidence, and the reading is open: a definite genitive in a Swedish service-page title reads generically, and the one-lokal limit is stated twice in the body, in the source's own words. The material neither establishes nor excludes a förening with several bookable lokaler, so the passage is defensible as written.

Neither finding is an unsupported fact in the protocol's sense, and both are reported openly beside the draft, so the rejection for unresolved findings not reported does not bite. Under the protocol the text is still labelled as carrying a remaining quality problem, on the "passar er" count.

## 4. G1 — pass

The brief names the reader precisely: boards of smaller bostadsrättsföreningar "som behöver avgöra om en genomgång av bokningsrutinerna är relevant och vad en intresseanmälan innebär". The page does exactly those two jobs and nothing else.

Relevance is decidable from what is on the page: "Det här ingår i genomgången" gives the two deliverables; "Det här ingår inte i genomgången" gives the three exclusions in one line; "Förutsättningar" tells the board what it must be able to produce ("beskriva föreningens befintliga bokningsregler och visa nuvarande instruktion till de boende") — a board that cannot do this knows at once the engagement is not for it. What the intresseanmälan entails is answered in its own words: "En intresseanmälan är ingen beställning och kräver inga betalningsuppgifter."

The angle holds throughout and is the brief's own: the benefit is stated as what the board receives — "Efter genomgången har styrelsen en gemensam bild av hur bokningen går till och två möjliga förenklingar att ta ställning till" — not as an abstract portrait of decision-makers, which the brief explicitly rules out. The copy craft the brief asks to be judged is present: direct entry per section, and the microcopy on the call to action ("Skicka en intresseanmälan") matches its destination instead of promising a booking.

## 5. G2 — pass

The scale is advisory for this genre: `web-copy` carries no fixed skeleton, so the script's `conforms: false` with `failures` for an absent `byline` and an absent `lead` measures this text against parts it is not required to have, and neither absence is a failure here. The script's `norms` entry — headline "61 characters" against a *should* of at most 60 — is likewise description, not requirement, for `web-copy`.

Judged on the `Web-copy` clause — useful information and choice, conditions, and an accurate next-step consequence:

- **Useful information and choice**: the included/excluded pair lets the board choose. The two bullets and the three exclusions are the whole of what is and is not bought.
- **Conditions**: gathered and findable. Price and engagement scope in "Pris och omfattning"; the no-guarantee statement immediately beneath it, in the same section rather than buried; the board's own obligations in "Förutsättningar". The brief demands "Villkor, pris och vad som händer sedan behöver vara lätta att hitta" and all three sit under their own headings.
- **Accurate next-step consequence**: "En intresseanmälan är ingen beställning och kräver inga betalningsuppgifter" states what submitting does not commit the reader to, and "Svale svarar via e-post inom tre arbetsdagar för att stämma av om uppdraget passar er och för att föreslå en tid för mötet" states what follows. The link label is "Skicka en intresseanmälan", not "Boka", and its destination is the supplied interest-notification URL — the brief's explicit boundary, honoured.

The parts that are present do distinct work: the headline names the service, the standfirst says who does what and for whom, and each section answers one question a deciding board has. No section repeats another. The delivery account also states the byline decision and its ground — "**Byline:** ingen. Sidan är avsändarmärkt med Svale, som underlaget anger" — which the brief names Svale as the sender; a service page carrying its sender rather than an author's name is the right solution for this genre.

## 6. P1 — pass

The reader can follow the page without effort, and the one term that carries weight is defined before it is leaned on. "Genomgången" is fixed by the inclusion section (a 45-minute video meeting plus a written sammanställning) before the outcome sentence uses it: "Efter genomgången har styrelsen …". Because the sammanställning is inside "genomgången", that sentence asserts no delivery date, which is the term the material says is unstated.

"Intresseanmälan" is introduced with its negative definition first — "är ingen beställning och kräver inga betalningsuppgifter" — then its content ("namn, förening och e-postadress"), then its consequence (the reply within three working days), in that order. That is the order a deciding reader needs.

Conclusions stay proportionate to the visible support. The outcome sentence keeps "möjliga" on the simplifications, so it promises candidates to decide on, not realised improvements; and the no-guarantee line sits beside the price rather than at the foot, so nothing on the page implies a saving it then withdraws. The useful substance — duration, participant count, the three contents of the sammanställning, the exclusions, price, preconditions — survives in full.

## 7. W1 — pass

The scale stays advisory for `web-copy`; the figures below are the script's and support the judgement without failing anything.

Orientation is the strength of this page. Five sections, each with its own plain subheading, measured by the script at 27, 32, 19, 15 and 22 characters; the headline at 61 characters and 7 words; the standfirst at 36 words in 1 paragraph. A board scanning for price stops at "Pris och omfattning"; one scanning for what it must supply stops at "Förutsättningar". That is the direct entry per section the brief asks to be judged, achieved without repeating any section's content in another.

Rhythm: the script measures 9 paragraphs, of which 3 run to two or three sentences, and 5 sections, of which 2 run to two or three paragraphs. So most units here are single-sentence or single-paragraph. On an article that pattern would read as fragmentation; on a service page whose job is to be scanned, each short unit is a complete answer to the heading above it, and I can name no actual reader loss. The one fragment — "Juridisk rådgivning, installation av bokningssystem och intervjuer med boende." — is a list answering "Det här ingår inte i genomgången", and reads as intended.

Standfirst and headline are complementary and open on different first words: "Genomgång …" against "Svale gör …". The body covers what the standfirst promises — the review, the two proposals, the intended board — and adds the conditions and the next step the standfirst does not attempt. No heading level below the second is used. Density is low, not high; the page is nowhere dense enough to lose a reader.

## 8. L1 — pass

The Swedish reads as Swedish written for this audience, not as translated prose. Idiomatic constructions carry the page: "Det här ingår i genomgången", "Så anmäler ni intresse", "Fast pris är 4 800 SEK inklusive moms", "för att stämma av om uppdraget passar", "ta ställning till". The definite "bokningsrutinen" for the procedure as a whole is ordinary Swedish, as is the genitive in the headline. Nothing imports generic translated English phrasing.

Address is consistent throughout after the first round of repairs: "er förening", "Så anmäler **ni** intresse", "passar er" — second person plural to a board, which is correct for the reader the brief names. The earlier draft's singular "I formuläret anger **du** …" (`draft-v1.md`) is gone, and with it the du/ni mixture report 1 raised as Q2.

## 9. L2 — pass

Swedish locale mechanics hold. The amount is written "4 800 SEK" with a space as the thousands separator and the currency after the figure, exactly as the material writes it and as Swedish convention requires; the currency is neither converted nor renamed, which the brief's boundary demands even of an English draft. "inklusive moms" is carried unchanged. No date appears, so no date form can be wrong, and none is invented. Headings are sentence case, correct for Swedish. Punctuation is Swedish throughout; no quotation marks are needed anywhere in the page. The URL is reproduced character for character.

## 10. T2 — skipped

`T2` — skipped — no technique is named in the text's metadata or in the reply. The delivered frontmatter reads `technique: none`, and the delivery account states "**Teknik:** ingen. Web-copy anger ingen teknik som genren vanligen skrivs med, och ingen teknik kom från anropet …". Nothing is judged under this criterion, and no technique is inferred from the shape of the prose.

## 11. Checker findings

Report 1 (`evidence/source-check/report-1.md`), findings:

- **R1-F1** — "I formuläret anger du namn, förening och e-postadress." — alleged: the material fixes the location and the three items ("Intresseanmälan sker på … och efterfrågar namn, förening och e-postadress") and says nothing about a form, so the means is an unsupported claim of manner. Writer: accepted, repaired one degree smaller than proposed, to "Den efterfrågar namn, förening och e-postadress." My class: **supported** — the material states no mechanism, and a destination that asks for the three items by e-mail is compatible with it.
- **R1-F2** — "… och två förenklingar att ta ställning till." — alleged: "möjliga" is dropped, so the sentence asserts that what the board gets are simplifications rather than candidates. Writer: accepted, repaired as proposed to "två möjliga förenklingar". My class: **supported** — the material carries "två möjliga förenklingar" in both places it names them, including the brief's own instruction on how to describe the benefit, and the draft kept the qualifier in the bullet one line above.
- **R1-F3** — "… och visa den instruktion som de boende har i dag." — alleged: the source identifies the document by currency and addressee ("visa nuvarande instruktion till de boende"), the draft by the residents' possession, which changes the precondition a board tests itself against. Writer: accepted, repaired to the source's wording. My class: **supported** — a current instruction posted on a door is compatible with the material and satisfies the source's condition but not the draft's.
- **R1-Q1** — the headline's definite "föreningens gemensamma lokal" — raised as an editorial question, not alleged as a defect and with no repair proposed. Writer: referred, no change. My class: **disputed** — the material neither establishes nor excludes a förening with more than one bookable lokal, and whether a generic definite in a title presupposes uniqueness is a reading it leaves open.
- **R1-Q2** — "du" at the intresseanmälan against "ni/er" elsewhere — raised as address consistency, expressly outside the comparison. Writer: referred, no change of its own; F1's repair removed it. My class: **disputed** — the mixture was real in `draft-v1.md`, but the allegation is about the draft's internal address, not about what the material supports, so the material bears nothing out either way.

Report 2 (`evidence/source-check/report-2.md`), findings:

- **R2-F1** — "Genomgång av bokningsrutinen för föreningens gemensamma lokal" — alleged: the definite genitive presupposes exactly one common lokal and drops, at its first assertion, the limit "Uppdraget gäller en lokal i en förening". Writer: accepted as a remaining finding, not repaired, because this was the final comparison; reported in the delivery account. My class: **disputed** — as at R1-Q1. The material contemplates more than one lokal, but it does not settle whether this headline asserts uniqueness, and the body states the limit twice in the source's own words.
- **R2-F2** — "för att stämma av om uppdraget passar **er**" — alleged: the source's "stämma av om uppdraget passar" carries no complement, and the draft supplies one, stating whose fit is checked. Writer: accepted as a remaining finding, not repaired, for the same reason; reported in the delivery account. My class: **supported** — the source clause is complement-free, and Svale's own check that the enquiry falls inside its bounded offer is compatible with the material and excluded nowhere in it.
- **R2-Q1** — "Genomgången vänder sig till styrelsen i en mindre bostadsrättsförening." — raised as an editorial question: the brief fixes the page's addressee, not a restriction on who may buy. Writer: referred, carried to the account as a question. My class: **disputed** — the material leaves open whether carrying the page's addressee into the copy states a property of the service, and the sentence does not say the service is refused to others.
- **R2-Q2** — the shared picture ascribed to "styrelsen" although two representatives attend. Raised as the brief's own unevidenced outcome statement. Writer: referred, not carried as a finding. My class: **disputed** — the brief supplies this in its own words ("Beskriv nyttan i termer av vad styrelsen faktiskt får"), so it stands as Svale's statement; whether the whole board thereby shares the picture is left open.

**A real defect seen by no checker:** none. The one defect I establish under F1 — the added "er" — is R2-F2, seen and reported. Every other passage I tested against the material (the possessor change "sina" → "föreningens", "erbjuder" → "gör", the exhaustiveness of the exclusion list, "Efter genomgången" and any implied delivery time, the link label and destination) was itself accounted for in one or both reports, and I reach the same conclusion on each.

## 12. Remaining findings

The delivery account opens with "**Utkastet levereras med kända brister.**" and reports two.

1. **"Rubriken: 'föreningens gemensamma lokal'."** Passage: the H1, "Genomgång av bokningsrutinen för föreningens gemensamma lokal". What the material carries instead: "en avgränsad genomgång av rutinerna för bokning av **en gemensam lokal**" and "Uppdraget gäller **en lokal i en förening**" — indefinite, and a stated limit that contemplates more than one existing. Proposed repair, quoted in the account as the checker's smallest supported one: "Genomgång av bokningsrutinen för en gemensam lokal". Under F1 I do not find this a defect: the reading is open, and the body carries the limit twice.

2. **"'för att stämma av om uppdraget passar er'."** Passage: "Svale svarar via e-post inom tre arbetsdagar för att stämma av om uppdraget passar er och för att föreslå en tid för mötet." What the material carries instead: "för att stämma av om uppdraget passar och föreslå mötestid" — no complement, so whose fit is tested is left open; the avstämning may be Svale's own check that the case falls inside the offering. Proposed repair: strike "er". Under F1 I do find this a defect — a small unsupported specification — and the text is labelled as carrying a remaining quality problem on that count.

The account also states, correctly, that these are "vad kontrollen hävdar och vad du som redaktör avgör", and separately carries the two editorial questions (R2-Q1, R2-Q2) under their own heading rather than as findings, which matches the reports.

## 13. Class of the run

**valid delivery.** The prose the run delivered had a completed comparison of its own: report 2 read `draft.md` in full and closed with "Comparison complete", and the delivered text is byte-identical to that file apart from the added `kntnt` metadata block. The two findings that comparison left standing were not repaired — repairing them would have delivered prose no comparison had read — and both are reported beside the draft with the passage, the source wording and the proposed repair. Nothing was withheld, and nothing uncompared was shipped.
