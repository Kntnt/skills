# Judgement B — runs/web-copy-abt/write

Judged from `work/source.md`, `response.md`, `delivered.md`, `anatomy-delivered.json` and everything under `evidence/`. All counted lines quote `anatomy-delivered.json`.

## 1. Outcome

**Delivered.** `delivered.md` exists and `response.md` carries the draft in a fenced block under an opening paragraph that states the delivery explicitly: "**Utkastet levereras med kända brister.**"

**Two source comparisons completed.** The evidence shows two distinct prompt/reply pairs against two distinct drafts:

- Round 1: `evidence/source-check/prompt-1.md` names `draft.md` and `report-1.md`. No `report-1.md` exists; `reply-1-truncated-by-caller.txt` begins mid-document at "## 3. Findings", so the claim accounting of round 1 cannot be inspected. The surviving tail nevertheless carries that checker's own completion statement — "Comparison complete… 21 claim pairs accounted for, 20 supported, 1 finding" — and ends `EXIT=0`. The reply describes this same partial uptake: "kontrollanten skrev ingen rapportfil, och mitt eget upptag av svaret klippte rapportens början".
- Round 2: `prompt-2.md` names `draft-2.md`, `report-2.md` exists in full and ends "Comparison complete… **Unresolved findings: 2 (F1, F2)**", and `reply-2.txt` matches it.

So round 1 completed as a comparison but reached the run only in part, and round 2 completed and was received in full. Round 2 is the last comparison.

**The delivered prose is byte-identical to the last prose a checker saw.** `diff evidence/source-check/draft-2.md delivered.md` reports no difference — frontmatter, headings, bullets and microcopy all identical. Round 1's single disposition is visible by diffing `draft.md` against `draft-2.md`: the sentence "Har ni det, finns underlaget som genomgången utgår från." was deleted and nothing else changed, and that repair precedes the second comparison. No repair was made after the last comparison; the reply states the rule it followed — "efter den sista jämförelsen ändras ingen prosa, inte heller till en rättelse kontrollanten själv föreslagit" — and the diff bears that out. No separate dispositions file survives under `evidence/`; the reply is the only disposition record, and the drafts corroborate it.

## 2. Headings

Genre is `web-copy` (`kntnt: genre: web-copy` in the delivered frontmatter and "Skriv en tjänstesida" in the brief), so these marks are evidence about the copy's orientation, not measurements against an article skeleton.

- H1 `Genomgång av bokningsrutinen för en gemensam lokal` — **label**; **echo** (partial: shares "Genomgång"/"går igenom" and "gemensamma lokal" with the standfirst's first sentence, which is the service's own name rather than a repeated phrasing). Not overclaim: the script gives the headline 50 characters, 7 words, and nothing in it asserts an outcome the body withholds.
- H2 `Det här ingår` — **label**. First sentence under it is "Uppdraget består av två delar:"; no shared wording, so no echo. Not overclaim in itself: the heading is inclusive, and the exhaustiveness problem is in the sentence beneath it, not in the heading.
- H2 `Det här ingår inte` — **label**. First sentence is "Genomgången omfattar inte juridisk rådgivning…"; the negation is carried by a different verb, so no echo.
- H2 `Pris och förutsättningar` — **label**; **echo** (partial: the topic noun "pris" recurs as the first word of the section's first sentence, "Fast pris är 4 800 SEK inklusive moms.").
- H2 `Så anmäler ni intresse` — **label**; **echo** (partial: "intresse" recurs in "En intresseanmälan är inte en beställning…"). Reads as a plain name for the section's job rather than a clause that states an angle.

No heading is a **statement**, none uses a **colon**, none is a **question**, and none **overclaims**. The set is a plain signposting scheme: four labels a scanning reader can enter directly at, which is what the brief asks for ("Bedöm direktingång i sektioner").

## 3. F1 — fail

I checked every factual and attributed claim against `work/source.md` myself. The great majority are carried exactly, several verbatim:

- "Ett videomöte på 45 minuter med två representanter för styrelsen." — source: "ett videomöte på 45 minuter med två representanter för styrelsen". Duration, medium and number all carried.
- "En skriftlig sammanställning av nuvarande steg, oklarheter och två möjliga förenklingar." — verbatim, including "två".
- "Fast pris är 4 800 SEK inklusive moms. Uppdraget gäller en lokal i en förening." — verbatim; currency neither converted nor restated in another unit.
- "Genomgången omfattar inte juridisk rådgivning, installation av bokningssystem eller intervjuer med boende." — verbatim but for the resolved subject.
- "Någon garanti för en viss tidsbesparing eller för färre konflikter lämnas inte." — the source's negation, with its scope over both items intact. The page nowhere asserts a saving or fewer conflicts, which the brief's boundary polices.
- "Därefter svarar Svale via e-post inom tre arbetsdagar" — actor, channel and deadline exact.
- "[Skicka en intresseanmälan](https://example.invalid/svale/intresse)" — destination unchanged, and the label names the intresseanmälan rather than a booking, so the brief's explicit prohibition ("En knapp/länk får inte heta Boka och antyda att mötet bokas direkt") is respected.
- The material's silences are respected: no payment terms, no delivery time for the sammanställning, no competitor comparison, no quotations, ratings, trials, places, campaign dates or guarantees. The reply names what is missing rather than filling it ("betalningsvillkor och leveranstid för sammanställningen — båda uttryckligen inte angivna i underlaget och därför inte skrivna"), which is what the material demands ("hitta inte på dem").

One passage nevertheless leaves the material, and it is why this fails:

- **"Uppdraget består av två delar:"** The material says "Genomgången omfattar ett videomöte på 45 minuter … och en skriftlig sammanställning av nuvarande steg, oklarheter och två möjliga förenklingar." *Omfattar* states that these are included; *består av två delar* states that there are exactly two and no more, and supplies a count the material never gives. Nothing supplied excludes a third component — the exclusion list is specific and names only legal advice, system installation and resident interviews, and "avgränsad" bounds the engagement without fixing the number of its parts. This is the state of knowledge turned around: what the material leaves unclaimed the page turns into claimed absence, on a service page where a board is deciding what 4 800 SEK buys. It is a strengthening of modality rather than an invented fact, and its reader harm is small, but it is an addition the material does not carry, and F1 admits no threshold below which an addition stops counting.

Two further passages I looked at closely and do **not** count as defects:

- **"för att stämma av om uppdraget passar er förening"** against "för att stämma av om uppdraget passar". Fit is relational, and the material leaves the complement unstated rather than stating a different one; in an e-mail to a named förening about its own lokal, "passar er förening" is a natural reading of the open phrase, not a contradiction of it. The material settles it neither way. Unknown, not absent — I record it as unsettled, not as a dropped caveat.
- **"I formuläret anger ni namn, förening och e-postadress." / "länken öppnar Svales formulär för intresseanmälan."** The material says the anmälan "sker på" the URL and "efterfrågar" three items; it names no form. "Formulär" is a manner detail the material does not supply, and manner is a claim. But the material also does not exclude it, the destination was not visited, and the three items and the non-binding character are exactly carried. Unsettled rather than refuted; worth the neutral alternative the reply itself offers.
- **"föreningens befintliga bokningsregler"** for the source's reflexive "sina befintliga bokningsregler" shifts the possessor from the board to the association. In a bostadsrättsförening the board's rules for the common lokal are the association's rules, and the modality "behöver kunna" is unchanged. Defensible as written.
- **"ni får en gemensam bild av rutinen och två möjliga förenklingar att ta ställning till"** rests on "Beskriv nyttan i termer av vad styrelsen faktiskt får: en gemensam bild av rutinen och två möjliga förenklingar." "att ta ställning till" adds no property the material withholds — "möjliga" already frames them as options, and no further act by Svale is implied.

**Verdict: fail**, on "Uppdraget består av två delar:" alone. This is a contract rejection (unsupported addition) rather than a qualitative concern, though a narrow one. It is the same passage the second comparison reported, and the reply names it with its repair, so the separate rejection for unresolved findings not reported is **not** triggered; the text still carries the remaining quality problem.

## 4. G1 — pass

The brief's reader is the board of a smaller bostadsrättsförening that "behöver avgöra om en genomgång av bokningsrutinerna är relevant och vad en intresseanmälan innebär". The page answers both. What the reader gets: the deliverables ("Ett videomöte på 45 minuter…", "En skriftlig sammanställning…"); what is excluded; what it costs and on what basis ("Fast pris är 4 800 SEK inklusive moms. Uppdraget gäller en lokal i en förening."); what the board must be able to produce ("Styrelsen behöver kunna beskriva föreningens befintliga bokningsregler och visa den nuvarande instruktionen till de boende."); and what the next step is and is not ("En intresseanmälan är inte en beställning, och den kräver inga betalningsuppgifter… Därefter svarar Svale via e-post inom tre arbetsdagar").

The angle is recognisable and consistent: a bounded errand with a named output and no promised result. The brief's warning is heeded — nowhere does the page address "beslutsfattare i en komplex verklighet"; every sentence is about this task. Copy/UX craft is present in the microcopy: the link label and the trailing clause tell the reader exactly where the click lands.

The one limit is inherent to the material: the page gives the board no criteria for judging *relevance* beyond scope and prerequisites, because the material supplies none. The reply says so rather than inventing them ("Underlaget ger inga kriterier för den bedömningen utöver förutsättningarna och avgränsningen"). That is a method limit of the assignment, not a craft failure. Total length against the brief's "cirka 300 ord om materialet bär det" is **not measured** by the script — it reports per-part word counts only — so I do not score it.

## 5. G2 — pass

**The anatomy scale is advisory for this genre.** The genre is `web-copy`, so the four-genre skeleton does not apply, and the script's two `failures` entries — `byline` "absent" and `lead` "absent", each against the rule "A text conforms when every part is present in the order shown" — are description of a shape this text does not owe, not requirements it breaks. `"conforms": false` accordingly decides nothing here. A service page carries no byline, and the delivery account names no author; nothing fails on that. The script lists `"norms": []`.

Judged on the `Web-copy` clause — useful information and choice, conditions, and an accurate next-step consequence — the parts do distinct jobs:

- Headline (script: 50 characters, 7 words) names the service.
- Opening paragraph (script: standfirst, 42 words, 1 paragraph) states who does what, for whom, and what the reader gets, and stands alone.
- "Det här ingår" / "Det här ingår inte" split scope from exclusion instead of leaving the reader to infer the boundary.
- "Pris och förutsättningar" carries conditions where the brief requires them to be easy to find ("Villkor, pris och vad som händer sedan behöver vara lätta att hitta").
- "Så anmäler ni intresse" is the next step with its consequence stated accurately: "En intresseanmälan är inte en beställning, och den kräver inga betalningsuppgifter", then the reply time, then the link. The call to action is built from the supplied route and nothing else.

No section duplicates another's job. The only blemish in the next-step copy is the unsupported word "formulär" discussed under F1, which describes the mechanism rather than misstating the consequence.

## 6. P1 — pass

The reader can follow the page end to end. Every term that could stop a board is introduced before it is relied on: "intresseanmälan" is defined by what it is not before the link asks for a click; "sammanställning" is given its contents where it first appears. The one real transition, "Därefter svarar Svale via e-post inom tre arbetsdagar", places the reply after the anmälan and carries the sequence the material itself gives.

Conclusions stay proportionate to visible support. The page draws no inference from the review to an outcome — no time saved, no conflicts reduced — and instead states the absence of a guarantee outright. Useful technical substance survives in full: 45 minutes, two representatives, three named form fields, three working days, 4 800 SEK inclusive of VAT, one lokal per engagement, three named exclusions. Nothing is thinned to generality.

## 7. W1 — pass

**The scale stays advisory for this genre**, so none of the figures below can fail the text on its own; they describe it.

Orientation is the page's strength: four labelled H2s, no heading level below the second, bullets for the two deliverables, and sections a reader can enter directly at — which is what the brief asks to be assessed ("Bedöm direktingång i sektioner och tydlig mikrokopia utan att kräva onödig upprepning"). Rhythm, by the script: 8 paragraphs, of which 4 are of two or three sentences; 4 sections, of which 2 are of two or three paragraphs. The shortest paragraphs are the deliberate ones — "Uppdraget består av två delar:" (script: 5 words) introduces the bullets, and the link line (script: 9 words) is the call to action. No paragraph figure in `parts` approaches a density problem: the largest is 24 words ("Genomgången omfattar inte juridisk rådgivning…").

The opening paragraph and the body complement rather than repeat: the opening promises "en gemensam bild av rutinen och två möjliga förenklingar", and the body is complete when that promise is covered — what it contains, what it excludes, what it costs, how to ask. The opening paragraph's first word is "Svale" and the headline's is "Genomgång", so the two do not open alike. There is no separate lead (`"lead": null`), which for web-copy is a shape, not a loss.

I find no actual reader loss to density or fragmentation. The repetition that exists — "intresseanmälan" three times in the last section — is the fixed name of the thing being asked for, and swapping in synonyms would blur exactly the distinction ("inte en beställning") the section exists to make.

## 8. L1 — pass

The resolved language is Swedish, and the prose reads as natively written rather than translated. The idiom is Swedish throughout: "stämma av om uppdraget passar", "ta ställning till", "Så anmäler ni intresse", "Någon garanti … lämnas inte". Word order is native, including the fronted adverbial in "I formuläret anger ni namn, förening och e-postadress." with correct V2 inversion, and the participial "Fast pris är …" of Swedish price copy. The second-person plural address ("ni", "er") is the right register for a service page speaking to a board as a body.

No English syntax is imported — no stranded prepositions, no possessive-of constructions, no calqued discourse markers. The compounds are properly closed ("bokningsrutinen", "bokningssystem", "betalningsuppgifter", "intresseanmälan", "bostadsrättsföreningar"), which is where translated Swedish usually breaks.

## 9. L2 — pass

The locale is Swedish and it governs throughout. Spelling and inflection are Swedish with correct definiteness ("den nuvarande instruktionen", "föreningens gemensamma lokal"). Headline and subheadings use sentence case, as Swedish requires, not title case. The number form is Swedish: "4 800 SEK" with a space as thousands separator and the currency code after the figure — and it is the material's own form, unconverted, which the brief requires ("Engelska utkast behåller SEK och destinationen; de omvandlar inte valuta"). The separator is a plain space rather than a non-breaking one, which is the source's own character too; that is a typographic preference, not a locale error. "e-post" and "e-postadress" carry the Swedish hyphenated form. The spaced em dash before the link microcopy is established Swedish practice.

No date is invented, no currency is converted, and no figure is restated in another unit. "tre arbetsdagar" is carried as a duration, not turned into a date.

## 10. T2 — pass

A technique is named: the delivered text's own metadata carries `technique: abt`, and the reply states "**Teknik:** `abt`, angiven i anropet", so T2 is judged rather than skipped.

The ABT parts relate without invented crisis or triumph, which is the test that matters on a commercial page:

- **Situation:** "Svale går igenom hur bokningen av föreningens gemensamma lokal fungerar i dag och sammanställer rutinen skriftligt." — the standing offer, stated plainly.
- **Genuine complication:** the limits, carried in the material's own terms rather than manufactured. "Genomgången omfattar inte juridisk rådgivning, installation av bokningssystem eller intervjuer med boende. Någon garanti för en viss tidsbesparing eller för färre konflikter lämnas inte." A board reads this as the real question: this is bounded, and no result is promised. No pain point is invented — the page never asserts that booking is currently chaotic or conflict-ridden, which is the failure mode the material would have made easy.
- **Supported response:** because the engagement is bounded and unguaranteed, the entry is deliberately non-binding — "En intresseanmälan är inte en beställning, och den kräver inga betalningsuppgifter." The therefore follows from the but.

The reply describes the same arc and places it at section level ("Den ligger på sektionsnivå: varje avsnitt svarar på en egen läsarfråga"), which the criterion expressly allows. No triumph is claimed anywhere: the strongest benefit sentence stays at "en gemensam bild av rutinen och två möjliga förenklingar att ta ställning till", the material's own formulation.

## 11. Checker findings

Round 1 — `reply-1-truncated-by-caller.txt` (no report file survives; the reply's start was cut, so any finding stated before "## 3. Findings" cannot be seen):

| # | Draft passage | Alleged | Writer's disposition | My class |
|---|---|---|---|---|
| R1-F1 | "Har ni det, finns underlaget som genomgången utgår från." | A necessary condition ("Styrelsen behöver kunna beskriva… och visa…") turned into a sufficient one, plus a new claim about what the genomgång proceeds from | Repaired by deletion: the sentence is in `draft.md` and absent from `draft-2.md`; the reply says "åtgärdades genom att meningen ströks" | `supported` — the material states a requirement on the board and nowhere says those two items constitute or suffice as the basis of the review |
| R1-Q (length) | Whole draft against "cirka 300 ord om materialet bär det" | Raised as an editorial question, not a defect: the draft is short, correctly so, but does not name what would close the gap | Addressed in the reply's section "Var materialet tog slut", which names the missing material | not a finding as raised; I concur it is none |
| R1-Q ("att ta ställning till") | "två möjliga förenklingar att ta ställning till" | Raised and dismissed as defensible | none needed | not a finding as raised; I concur |

Round 2 — `report-2.md`:

| # | Draft passage | Alleged | Writer's disposition | My class |
|---|---|---|---|---|
| R2-F1 | "Uppdraget består av två delar:" | The material's inclusive "Genomgången omfattar … och …" is made exhaustive and given a count | Not repaired; the run's two comparisons were spent. Reported first in the delivery account with the repair "Uppdraget omfattar:" | `supported` — nothing supplied excludes a further component, and the exclusion list names only three specific things |
| R2-F2 | "för att stämma av om uppdraget passar er förening" | The material's complement-less "om uppdraget passar" is narrowed to the förening's side | Not repaired; reported in the delivery account with the repair "stryk 'er förening'" | `disputed` — the material leaves the complement open rather than stating another one, and in context the draft's reading is one the open phrase admits |
| R2-Q1 | "I formuläret anger ni namn, förening och e-postadress."; "länken öppnar Svales formulär för intresseanmälan." | "Formulär" names a submission mechanism the material does not name | Reported in the reply as an open editorial question, with the checker's mechanism-neutral alternative quoted | `disputed` — the material neither names a form nor excludes one, and the destination was not visited |

**Was a real defect I found under F1 seen by no checker?** No. The single passage I fail F1 on — "Uppdraget består av två delar:" — is R2-F1, found by the second comparison and reported in the delivery account with its repair. The two passages I treated as unsettled were also both raised. I found nothing the checkers missed.

## 12. Remaining findings

The delivery account opens by declaring them: "**Utkastet levereras med kända brister.** Den avslutande källjämförelsen lämnade två invändningar som inte åtgärdades, eftersom körningens två jämförelser då var förbrukade. Texten nedan är exakt den prosa som den sista jämförelsen läste." The last clause is true — `draft-2.md` and `delivered.md` are identical.

1. **"Uppdraget består av två delar:"** — the account states the material carries "Genomgången omfattar ett videomöte på 45 minuter med två representanter för styrelsen och en skriftlig sammanställning av nuvarande steg, oklarheter och två möjliga förenklingar", and that it "räknar upp utan att säga att uppräkningen är allt". Proposed repair: "byt raden mot 'Uppdraget omfattar:' och låt båda punkterna stå kvar." **This is a defect of the text**, and it is the passage F1 fails on.
2. **"för att stämma av om uppdraget passar er förening"** — the account states the material carries "för att stämma av om uppdraget passar", "utan att säga vad det ska passa". Proposed repair: "stryk 'er förening'." **This is not a defect on my reading**; the material settles the complement neither way, and the wording is defensible as written. Reporting it costs nothing and is the safer disclosure.

The account also carries, separately and correctly labelled as not a reported defect, the open editorial question about "formuläret"/"Svales formulär", with the neutral alternative spelled out. I likewise do not count it as a defect.

The account's own framing of what it did with them — "efter den sista jämförelsen ändras ingen prosa, inte heller till en rättelse kontrollanten själv föreslagit" — matches the evidence exactly: the delivered prose is the compared prose.

## 13. Class of the run

**`valid delivery`.**

The run produced a draft, had it compared, repaired the one supported defect that comparison found, had the repaired prose compared again in full ("Comparison complete… Unresolved findings: 2"), and delivered that exact prose — byte-identical to `draft-2.md` — with both remaining findings quoted, each with its material passage and its smallest repair, and with the open editorial question disclosed beside them. No prose moved after the last comparison, so the delivered text is the compared text, and the reporting obligation is met. The text is nonetheless labelled as carrying a remaining quality problem: the unsupported exhaustiveness in "Uppdraget består av två delar:", on which F1 fails.

Of the protocol's five unconditional rejections: unsupported facts — one narrow instance, reported; wrong locale — none; substantive mechanical editing — not applicable to a Write run, and the only prose change made was a checker-supported deletion; unresolved mandatory findings not reported — none, both are reported; incorrect side effects — the reply's account of the working directory ("innehåller `source.md` och en tom `scratch`-katalog") is consistent with the evidence, which the observer copied out, and I see no side effect beyond it.

## Verdicts

| ID | Verdict |
|---|---|
| F1 | fail |
| G1 | pass |
| G2 | pass |
| P1 | pass |
| W1 | pass |
| L1 | pass |
| L2 | pass |
| T2 | pass |

Outcome: delivered, two comparisons, prose byte-identical to the last compared draft. Class of the run: `valid delivery`.
