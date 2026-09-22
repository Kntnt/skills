# Judgement — w-c401ce

Judged draft: `delivered.md` (Swedish, `sv`, 365 words of body text).

## 1. Outcome

**Delivered.** Two comparisons ran. The first returned two source-support findings, both accepted and repaired; the second read the repaired prose and returned no findings.

The delivered prose **is identical** to the last prose a checker saw: `evidence/source-check2/draft.md` differs from `delivered.md` only by the `kntnt` frontmatter block. The two drafts in the evidence differ exactly by the two repairs (indefinite *felanmälningar* in headline and standfirst; *säger* → *skriver … i ett mejlsvar* / *skriver hon* / *skriver Maya Lind*), which matches what the response says was done.

## 2. F1 — source support: **pass**

No forbidden inference and no invention. The software is never credited with the shorter assignment time — *Perioderna hade olika arbetsbelastning, och noteringen tillskriver uttryckligen inte programvaran skillnaden* stands in the same sentence as the medians, and no causal verb or causal hedge appears anywhere, headings included. Assignment time is never turned into completion time; *tiden till färdigt arbete har inte mätts* closes that door explicitly. No cost, satisfaction or rescue claim appears. The count is given with both exclusions and without any evaluative characterisation. *Någon jämförelse med en annan leverantör redovisas inte* claims less than "No comparison … is available", which keeps the state of knowledge safe. *Försöket har ännu inte utvidgats* keeps "not yet" open. The customer's reservation survives twice, inside Q3 and in *Hon rekommenderar inte Svale till alla bostadsföretag*, where Swedish *inte … alla* is partial negation and does not become a recommendation against.

Four items to cite, none of which I judge grave enough to fail the criterion:

- **Tense shift.** *Hon rekommenderar inte Svale till alla bostadsföretag.* The material says "Lind **did not** recommend Svale to every housing company" — a description of what she did in the interview. The present tense converts it into a standing position she holds now. The material's "Her final quotation **is** her actual, qualified assessment" makes the reading defensible, but it is the draft, not the material, that puts her in the present.
- **Dropped agent.** *Försöket pågick i åtta veckor, och telefonanmälan hölls öppen för de boende.* The material names the agent: "The maintenance team … kept telephone reporting open for residents." The s-passive asserts nothing false, but in a piece whose brief requires the customer to remain the acting party, the one act that shows the team protecting its residents' channel is left agentless.
- **A supplied customer action is absent from the narration entirely.** "The maintenance team designed its categories" appears nowhere in the draft's own voice; the reader learns it only from inside Lind's quotation (*Kategorierna var våra*). This is an omission rather than a misstatement, but it is what creates the reading stop in §5 below.
- **Ownership reading.** *från två av sina hus* (standfirst). The material says only that Elm Quay "manages 640 flats". *Sina hus* in ordinary Swedish covers a managed portfolio, and the lead's *som förvaltar 640 lägenheter* (not *äger*) settles it; thin, but excluded for the reader.

Also noted and not charged: *Av Thomas Barregren*. The brief says "No author name supplied", so this attribution comes from outside the material; it is a production element, G2 requires a byline, and the response discloses it and tells the user to change it before publishing.

Nothing else — no changed term, no changed subject, no changed date, no dropped caveat, no invented event and no invented personal attribute.

## 3. G2 — required parts and their jobs: **fail**

All the parts are present and in order — headline, standfirst, byline, lead, three sections, ending — and most of the account's jobs are done: the situation (separate storage), the action (decided, tested, chose, trained, kept the phone line open), the results (31 entries with exclusions, two medians with the non-attribution, three things unmeasured), the appraisal (Q3 plus the withheld blanket recommendation), a truthful publisher stance (*Den här kundberättelsen publiceras av Svale Systems*), the customer as acting party, and a call to action built from the one supplied route and described as a document to read.

It fails on one dimension, narrowly but plainly: **the standfirst and the lead do not do distinct jobs.**

> Standfirst: "**Telefonanmälningar och mejl lagrades var för sig.** Hösten 2025 prövade Elm Quay Housing under åtta veckor att samla felanmälningar från två av sina hus i en gemensam logg från Svale Systems."
> Lead: "I september 2025 bestämde sig underhållsgruppen hos Elm Quay Housing … för att pröva en gemensam logg för felanmälningar i två av husen. **Telefonanmälningar och mejl hade dittills lagrats var för sig.**"

The reader is told the same two facts twice within four lines, one of them in nearly the same words. The standfirst also opens on the old state rather than on the news, which is the lead's job, and the lead then has to repeat the trial framing to get moving. The effect is a piece that seems to start twice.

Two smaller structural wobbles reinforce it: the section *Så sattes den gemensamma loggen upp* opens with *Någon jämförelse med en annan leverantör redovisas inte*, which belongs with the choice of supplier in the lead and not under a setup heading; and both of Lind's first two quotations are stacked in that one section while the middle section carries none, so the reader gets the supervisor's voice twice in a row and then not at all for nine sentences.

Minor: the closing link is a bare URL rather than a Markdown link, in a brief that asked for Markdown.

## 4. L1 — Swedish prose: **pass**

Native syntax and idiom, no English phrasing showing through. V2 holds after every fronted element (*Hösten 2025 prövade …*, *I september 2025 bestämde sig …*, *Från anmälan till tilldelning var mediantiden …*). The particle verb in the subheading is correctly split (*Så sattes den gemensamma loggen upp*), *Valet föll på Svale Systems, sedan gruppen testat …* uses the supine after *sedan* the way a Swedish desk would, and *Nästa hus får vänta på ett besked* is a genuinely idiomatic Swedish headline rather than a translated one.

Blemishes worth naming:

- *Här får du veta vad förvaltningens underhållsgrupp gjorde* — *förvaltningens* introduces an entity the reader has not met; the company has been named, its "förvaltning" has not.
- *tiden till färdigt arbete* for completion time — a coined, slightly wooden phrase where *tiden till färdig reparation* or *hur lång tid reparationerna tog* would read naturally.
- *tre under de åtta veckorna före* — *dessförinnan* or *närmast före* would sit better than a stranded *före*.

Mechanics, excluded from L1 by the criterion but recorded: the speech marker is an em dash (—) where Swedish typography uses the talstreck (–).

## 5. Quoted speech

**Q1 — `— Vi ville att kvällsskiftet skulle se vad morgonskiftet redan hade gjort. Kategorierna var våra; Svale hjälpte oss att lägga in dem i loggen, skriver Maya Lind, arbetsledare för underhållet, i ett mejlsvar.`**
Renders: "We wanted the evening shift to see what the morning shift had already done. The categories were ours; Svale helped us put them into the log."
*Not one pass.* The Swedish reader stops at **Kategorierna**. The definite form promises categories already met, and nothing in the article has mentioned any: the preceding paragraph runs *Någon jämförelse … Svale konfigurerade loggen och utbildade sex medarbetare … telefonanmälan hölls öppen för de boende.* The reader has to supply, from outside the text, that the log was built on categories somebody defined — and only then can they read *var våra* as the claim it is. The clause four words later (*lägga in dem i loggen*) lets them bridge without rereading the sentence, so the stop is brief; it is still a reference the article never introduces, and it exists because the supplied narration clause "The maintenance team designed its categories" was left out.
*Meaning, stance, certainty, voice:* intact. Ownership is asserted as she asserted it, Svale's part stays help, the source semicolon is preserved, nothing is hedged, unhedged or sharpened.

**Q2 — `— Vi lade mer tid på att enas om kategorierna än på att mata in de första anmälningarna. Den tiden skulle jag avsätta innan vi börjar i nästa hus, skriver hon.`**
Renders: "We spent more time agreeing on the categories than entering the first reports. I would set that time aside before the next building starts."
*One pass.* *Den tiden* is settled by the sentence before it, the fronted object with V2 inversion is ordinary Swedish, and *innan vi börjar i nästa hus* needs nothing supplied.
*Meaning, stance, certainty, voice:* intact, with one defensible rendering decision. The source's "before the next building **starts**" is a metonymy Swedish has no ready equivalent for — *innan nästa hus börjar* would be a verb its subject cannot perform — so the draft makes the agent explicit as *vi*. Lind speaks as the team's *vi* throughout, so the supplied context settles it; the comparison, its two terms and the conditional *skulle* all survive.

**Q3 — `— Jag skulle välja att göra försöket igen. Att ha en samlad bild av anmälningarna hjälper oss, men jag skulle lägga in en extra vecka för förberedelser, skriver Maya Lind.`**
Renders: "I would choose to do the trial again. Having one view of the reports helps us, but I would leave an extra week for preparation."
*One pass.*
*Meaning, stance, certainty, voice:* intact. The endorsement stays conditional, the benefit stays first person plural (*hjälper oss*, not widened to housing companies generally), and the reservation stays attached by *men* inside the same sentence rather than being stranded in a following one.

**Missing quotations:** none. All three usable quotations are used, none is welded to another, and no words are attributed to Lind that she did not supply.

**One sentence:** No — Q2 and Q3 read on one pass with the source's meaning, stance, reservation and voice intact, but Q1 stops the reader at *Kategorierna*, a reference the article never introduces because the supplied clause naming the team as the categories' author was dropped from the narration.

## 6. Intermediate — the checkers' findings

| # | Passage | Allegation | What the writer did | Class |
|---|---|---|---|---|
| R1-F1 | Headline *Elm Quay samlade **felanmälningarna** från två hus* and the same definite in the standfirst | The Swedish definite plural claims the two buildings' fault reports as a closed set; the material supports only 31 entries with emergencies excluded | Accepted; both changed to indefinite *felanmälningar* | **Supported repair.** Fine-grained — headline Swedish often takes the definite loosely — but the repair costs nothing and removes a totality the material does not carry |
| R1-F2 | *säger Maya Lind …*, *säger hon*, *säger Maya Lind* | Attributes emailed answers as speech; the material says "All interviews occurred by email" | Accepted; changed to *skriver … i ett mejlsvar*, *skriver hon*, *skriver Maya Lind* | **Supported repair.** The manner of a statement is a claim, the material states it, and naming the channel once tells the reader what the material is |
| R2-obs 1 | *… och telefonanmälan hölls öppen för de boende* | Agent dropped by the s-passive where the material names the maintenance team; recorded as an "agency observation", explicitly not a defect | Nothing | **Right finding rejected.** The checker's reasoning (nothing false is asserted, and *försöket* intervenes as subject) is fair as far as source support goes, but the brief makes the customer the acting party and the material names that party; the repair was one clause |
| R2-obs 2 | *Kategorierna var våra* | The definite arrives with no prior mention because the narration omits "The maintenance team designed its categories"; judged to bridge from *loggen* and "not to stop a reader" | Nothing | **Right finding rejected.** I agree that the bridge is available; I do not agree that no reader stops. See §5 — and the same restored clause would have closed this and the previous item together |
| R2 §4 | *Hon rekommenderar inte …* (present tense) | Raised and set aside as supported by "Her final quotation **is** her actual, qualified assessment" | Nothing | **Disputed caution** — the argument is reasonable; the shift from a past act to a standing stance is still the draft's, not the material's |
| R2 §4 | *två av sina hus*; *redovisas inte*; *är undantagna*; *har inte mätts* | Each tested and set aside with a supplied statement that excludes the case | Nothing | **Wrong findings rejected (correct)** in each instance; I reach the same conclusions independently |

**Did a real defect escape every checker?** Under F1 and point 4, no — both of the items I would repair (the dropped agent, the missing antecedent for *Kategorierna*) were seen by the second checker and classed as non-defects. The defect nothing in this run looked for is the G2 one: the standfirst and lead saying the same thing twice. The comparisons are scoped to source support and translation and cannot be faulted for missing it; the anatomy measurement the response cites counts parts rather than judging whether they do different work, so it could not catch it either.

## 7. Delivery

**A valid delivery.** The material supported a draft, both findings raised against it were repaired with supplied material rather than invention, the repaired prose was read again and cleared, and nothing carried forward that would justify stopping: no unsupported claim, no forbidden inference, the customer's reservation intact twice, and the publisher named. The response is honest about the shortfall against the requested length (365 words against "approximately 400, as material allows"), names what further material would close it, and discloses that the byline comes from the invocation rather than the material.

What was delivered nonetheless carries two defects worth a second pass before publication: the standfirst/lead duplication in §3, and the missing narration clause that leaves *Kategorierna* without an antecedent in §5. Neither is a reason to have stopped; both are reasons the draft is not finished prose.
