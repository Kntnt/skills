# Judgement — `case-study-sv-r2`

Judged from `work/source.md`, `delivered.md`, `response.md` and everything under `evidence/`. Nothing else was read. Checker approvals and the writer's own disposition are weighed as argument only; every claim below was checked against the material directly.

---

## 1. Outcome

- **Delivered.** `response.md` hands over the full Markdown text and names one known, unrepaired defect.
- **Two comparisons ran** (`evidence/source-check-1/`, `evidence/source-check-2/`), each with its own fresh checker and its own contract copies (the three contract files are byte-identical between the two rounds).
- **The delivered prose is identical to the last prose a checker saw.** `delivered.md` and `evidence/source-check-2/prose.md` differ in nothing. The response's claim that "det som levereras är exakt den prosa den läste" is true.
- Between round 1 and round 2 the writer changed seven passages: all four of round 1's findings (F1–F4) plus three of its observations (O2 note ownership, O3 *tillskriva* government, O6 *ni* → *du*) and the deletion of the redundant "Testet pågick i åtta veckor." No round-1 disposition file was kept; the dispositions are legible only from the prose diff.
- Length: 351 words of body against "approximately 400 words, as material allows". Within the brief's own escape clause, and `response.md` names what further material would close the gap.

---

## 2. F1 — source fidelity

**Verdict: fail, narrowly.** The substantive core is clean — every figure, every exclusion, the chronology of the two medians, the non-attribution to the software, the survival of the reservation, and the description of the link — but two attributions do not stay inside the material.

### Cited defects

**F1-a — "Telefonanmälan behölls för de boende." (dropped agent; implies the supplier)**

Material: "**The maintenance team** designed its categories and **kept telephone reporting open for residents**." The draft's agentless s-passive removes the agent the material states explicitly, and it stands immediately after "Svale Systems konfigurerade loggen och utbildade sex medarbetare vid två tillfällen", so the nearest available subject a reader carries forward is the supplier. The brief requires that "The customer, Elm Quay Housing, should remain the acting party"; this is the one sentence in the draft where the customer's act is detached from the customer. Round 2's Finding 1 is correct and the delivered text still carries it.

**F1-b — "Av Thomas Barregren" (named byline the material does not supply)**

The brief states "No author name supplied." The draft nonetheless asserts a named human author. Both checkers ruled the byline out of accounting by declaration ("comes from the invocation, not the material"), so neither tested it. Judged from the material alone it is an unsupported attribution. Mitigating: `response.md` discloses it plainly and says the line must be changed before publication if the text is to go unsigned or under another name, and the byline is not a claim about the case. It compounds F1-c below.

**F1-c — no publisher disclosure, in a text whose voice reads as independent journalism**

Material: "The supplier approved publication of this case as supplier-published material; it is not independent journalism." The draft asserts no independence — every figure stays with the internal note, every valuation with Lind, Svale is third person throughout — but it also tells the reader nothing, and it carries a named journalistic byline and ends on the supplier's own link. This is an omission rather than a false assertion, so it is recorded here and treated under G2, not as the ground of the F1 fail.

### Checked and clean

- **640 flats**, **September 2025**, **two buildings**, **eight weeks**, **six staff**, **two sessions**, **31 reports**, **4 December 2025**, **two vs three working days**, **median**, **report-to-assignment**: all exact.
- **Exclusions** ("Akuta ärenden och arbeten som beställts före testet ingår inte") sit attached to the count, where the material attaches them. The count carries **no evaluative characterisation** — no *bara*, *hela*, *redan*, *så många som* — and the material supplies no comparison that would license one.
- **Causal limit held.** "Perioderna hade olika arbetsbelastning, och noteringen tillskriver uttryckligen inte programvaran skillnaden." *Uttryckligen inte* is "explicitly does not", not the weaker "does not explicitly". No causal verb, no causal hedge, in title, standfirst, any heading or the body.
- **Assignment time is never turned into completion time**; "tiden fram till avslutat arbete" is named among the unmeasured.
- **Unknown kept apart from absent.** "någon jämförelse med en annan leverantör finns inte **att tillgå**" preserves the material's availability claim ("is available") instead of asserting non-existence; and where the material *is* absolute ("There are no cost, resident-satisfaction or completion-time measurements") the draft's flat *har inte mätts* is right. This distinction is drawn correctly in both directions — it was round 1's F3, repaired.
- **Modality preserved** at "efter att ha prövat **om** loggen **kunde** visa status" — the test of whether, not a finding that it could.
- **Open state preserved** at "har **ännu inte** utvidgat testet, utan ska **först** se … och beslutar därefter": the check precedes the decision and the decision is left undecided.
- **Link description**: "checklistan för införande" = "implementation checklist"; the verb is *läsa*; URL exact; no booking, demo or trial implied. Round 1's unsupported "som går igenom stegen" was deleted.
- **Forbidden inferences**: none present. No software cause, no money saved, no delighted residents, no rescued helpless customer.

### Minor, not counted against the verdict

- **"status för varje ärende"** for "the status of each repair". *Ärende* is in general wider than *repair* — a resident enquiry needing no work is an *ärende*. Inside a *felanmälningslogg*, and against a material that itself writes "31 repair reports" for the same population, the two pick out the same set here; nothing falls under one and not the other in this context. Reverse direction is clean.
- **"Lind rekommenderar inte Svale till alla bostadsföretag."** The material reports the past ("did not recommend"). The Swedish present is the ordinary register for an interviewee's standing position and the draft says *säger* throughout; the scope of the negation (*inte … till alla* = partial, not a refusal to recommend at all) matches "did not recommend … to every" exactly.
- **"Teamet har ännu inte utvidgat testet"** supplies an agent where the material states a state of the trial ("The trial has not yet expanded"). The material names the team as the party that will decide, so no agent is invented.
- **Title scope.** "Elm Quay fick en gemensam bild av felanmälningarna" carries no scope marker; the log ran in two buildings of a 640-flat portfolio. The standfirst on the next line supplies "i två av husen", and headline plus standfirst is read as one unit. Not counted, but the headline alone overstates.
- **"hösten 2025"** is entailed, not added (September decision, eight weeks, note dated 4 December).

---

## 3. G2 — required parts

**Verdict: pass, with one gap.**

| Part | Present | Job it does |
|---|---|---|
| Headline | "Elm Quay fick en gemensam bild av felanmälningarna" | Names the customer and the achieved state; claims no effect on time, cost or satisfaction. |
| Standfirst | "Elm Quay Housing sköter 640 lägenheter…" | Adds size, season, scope (two buildings) and a three-part promise the body then keeps. It does not restate the headline. |
| Byline | "Av Thomas Barregren" | Present as a part; unsupported as a fact (F1-b). |
| Lead | "I september 2025 bestämde…" | Situation and decision, the prior state, the choice of supplier with its missing comparison, and the two things the article will draw on. Distinct from the standfirst. |
| Sections | Three | Distinct jobs: who did what (supplier configures, customer decides), what was and was not measured, the supervisor's verdict. No section repeats another. |
| Ending | "Teamet har ännu inte utvidgat testet…" + link | Leaves the trial open and offers the supplied checklist. |

Customer account requirements: **situation** (640 flats, telephone and email stored separately, shifts not seeing each other's work) ✓; **action** (the team decided, tested whether the log could show status, designed its categories, kept phone reporting) ✓; **results** (31 reports with exclusions, two vs three working days, workload caveat, three things unmeasured) ✓; **appraisal** (Lind's third quotation plus "Lind rekommenderar inte Svale till alla bostadsföretag") ✓, and the reservation survives in two places, once inside her own *men* clause and once in the narrative; **customer as acting party** ✓ everywhere except the telephone sentence (F1-a); **call to action** built from the one supplied offer, described as a document to read ✓.

**The gap:** the required *truthful publisher stance* is carried only negatively. The draft claims no independence, but it also says nothing about being supplier-published, while wearing a named byline and closing on the supplier's link. A reader has nothing to tell them who is publishing. Both checkers saw this (round 1's O8, round 2's 4.6) and both filed it as an omission outside a source comparison — defensible for their scope, but it leaves the stance under-declared here. Passing because nothing false is asserted and the placement of a disclosure line is ordinarily a publishing decision, and because `response.md` puts the choice explicitly to the editor.

Reader effect: the ending is the strongest passage — "Teamet har ännu inte utvidgat testet, utan ska först se hur kategorierna fungerar för större reparationer" refuses the growth curve the genre usually forces, and the CTA that follows is offered to someone weighing the same decision rather than to a buyer.

---

## 4. L1 — professional Swedish

**Verdict: pass.**

- **V2 is respected throughout**, including where fronting invites the English order: "Dittills **hade** telefonanmälningar och mejl sparats var för sig", "Efter åtta veckors test **fanns** både en testnotering…", "Väger du samma beslut **kan** du läsa…", and inside the quotation "Den tiden **skulle** jag avsätta". No instance of the fronted-adverbial-plus-subject tell.
- **Compounds are single words**: *felanmälningslogg*, *underhållsteam*, *testnotering*, *kvällsskiftet*, *morgonskiftet*, *arbetsbelastning*, *bostadsföretag*, *telefonanmälningar*.
- **Double definiteness** is marked on both members: *den interna testnoteringen*, *de första anmälningarna*, *de åtta veckorna*, *de boendes nöjdhet*.
- **Genitive** without apostrophe: *Elm Quays interna testnotering*, *Elm Quay Housings eget underhållsteam*.
- **Verb government is Swedish, not English**: *tillskriver uttryckligen inte **programvaran skillnaden*** takes the thing credited directly rather than following the English "attribute … to". This was round 1's O3, corrected in round 2 — the single clearest sign the draft is written in Swedish rather than carried over.
- **Address** is *du* throughout after the round-2 fix; the earlier *ni* to a single reader, which reads as a translation artefact, is gone.
- **Sentence length and subordination** stay inside Swedish tolerance: main clauses with fronted adverbials rather than long relative chains, verbs rather than nominalisations ("när… bestämde", not "vid beslutsfattandet").
- **Speech is set with a speech dash**, the ordinary Swedish marking, not quotation marks.

Reader effect: it reads as a Swedish trade-press case, not as a translated one. The one sentence that reads a shade less than professional is "Teamet har ännu inte utvidgat testet, utan ska **först se** … **och beslutar** därefter", where the finite *beslutar* after *ska först se* sits awkwardly against the modal (*och besluta därefter*, or a separate main clause, would be cleaner). *Sköter* where the sector says *förvaltar*, and *Väger du samma beslut* where one ordinarily *står inför* a decision, are register preferences rather than errors. None imports English phrasing.

---

## 5. Bridges into quotations

Three quotations, in order.

**Q1 — "— Vi ville att kvällsskiftet skulle se vad morgonskiftet redan hade gjort. Kategorierna var våra; Svale hjälpte oss att lägga in dem i loggen, säger Maya Lind, arbetsledare för underhållet."**

*Bridge:* **none.** The trailing tag "säger Maya Lind, arbetsledare för underhållet" carries name and role and nothing else, so it is attribution, not a bridge. The sentence standing immediately before it, across a paragraph break, is "Telefonanmälan behölls för de boende." — a different subject (the phone channel) that does not lead into shifts or categories at all.
*Ambiguity, both readings:* read strictly by position, "Telefonanmälan behölls för de boende." is the immediately preceding sentence and would be **class (c)** — it carries a fact (telephone reporting kept open for residents) that the quotation nowhere carries. I choose **no bridge**, because the sentence neither introduces the speaker nor points forward: it closes the preceding paragraph's own business and the quotation begins cold.

**Q2 — "— Vi lade mer tid på att enas om kategorierna än på att registrera de första anmälningarna. Den tiden skulle jag avsätta innan nästa hus drar i gång, säger hon."**

*Bridge:* **none.** What stands immediately before is Q1, another quotation, not narrative. The trailing "säger hon" is bare attribution. Nothing in the draft's own voice prepares this remark, and nothing pre-empts it: the relative time cost of agreeing categories against entering reports appears nowhere else in the text.

**Q3 — "— Jag skulle välja att göra testet igen. Att ha en samlad bild av anmälningarna hjälper oss, men jag skulle lägga in en extra vecka för förberedelser, säger Maya Lind."**

*Bridge:* **"## Arbetsledaren skulle göra om testet med mer förberedelse"** — the heading is the only text between the previous section and the quotation, and it does lead the reader in.
*Class:* **(a).** The words that put it there are *skulle göra om testet* and *med mer förberedelse*: they deliver in advance both halves of what the quotation is there to deliver — she would do it again, and she would add preparation time. A reader who has read the heading meets "Jag skulle välja att göra testet igen … men jag skulle lägga in en extra vecka för förberedelser" as the heading said again, in her voice.
*Ambiguity, both readings:* a heading is not a narrative sentence in the body flow, and on that reading Q3 also stands with **no bridge**. I choose **(a)** because the brief's test is the reader's, not the typographer's: this is the text immediately before the quotation and the reader arrives having already been given its payload. The residue the quotation still adds is one clause the heading does not carry — "Att ha en samlad bild av anmälningarna hjälper oss" — which keeps the quotation from being pure echo, but does not change the class of the bridge.
*No checker tested this.* Round 2's 1.28 asserted that no quotation "restates its neighbouring paragraph", which is true and beside the point: the heading, not the paragraph, is what pre-empts Q3.

**Counts.** One bridge of class (a) (Q3's heading), none of class (b), none of class (c); two quotations stand with no bridge at all (Q1, Q2) — and on the strict-position reading of Q1 the count would be one (a) and one (c).

**Interviewer.** The draft attributes no question or utterance to an interviewer anywhere; no interviewer exists in the text, and no question mark appears in it.

**Unsupported bridge assertions.** The one bridge, the Q3 heading, is fully supported by Lind's own quotation and is attributed inside the heading itself to *arbetsledaren*, so the standpoint stays hers. If Q1's preceding sentence is counted as a bridge, its content is supported but its agent is not stated — the F1-a defect, reached by a second route.

---

## 6. Quoted speech

All three quotations the material offers and permits are used; **none is missing**. Each is used whole, none is welded to another, none is split across a paragraph break, none is trimmed.

| Source | Draft | Meaning | Stance | Certainty | Reservation | Voice |
|---|---|---|---|---|---|---|
| "We wanted the evening shift to see what the morning shift had already done. The categories were ours; Svale helped us put them into the log." | "Vi ville att kvällsskiftet skulle se vad morgonskiftet redan hade gjort. Kategorierna var våra; Svale hjälpte oss att lägga in dem i loggen." | Same. *Redan* carries "already"; the pluperfect carries the sequence. | Same: a past intention, not a claim it was achieved. | Unchanged. | n/a | Kept, including the two-beat semicolon and the flat possessive *var våra*; Svale stays in the helping role, not the deciding one. |
| "We spent more time agreeing on the categories than entering the first reports. I would set that time aside before the next building starts." | "Vi lade mer tid på att enas om kategorierna än på att registrera de första anmälningarna. Den tiden skulle jag avsätta innan nästa hus drar i gång." | Same comparison, same two terms, same direction. *Enas om* is reaching agreement, as "agreeing on" is. | Same. | *Skulle* renders "would" with no hedge added or removed. | n/a | Fronted *den tiden* puts her emphasis where "that time" puts it. **One drift:** *drar i gång* is spoken-register where "starts" is neutral — a small lift in colouring, no change of meaning, stance or certainty. The English ellipsis (what the next building starts) is left elliptical rather than filled in, which is right. |
| "I would choose to do the trial again. Having one view of the reports helps us, but I would leave an extra week for preparation." | "Jag skulle välja att göra testet igen. Att ha en samlad bild av anmälningarna hjälper oss, men jag skulle lägga in en extra vecka för förberedelser." | Same. *En samlad bild* is the ordinary Swedish for "one view" of scattered records. | Same, and not upgraded: *hjälper oss* stays "helps us", not an endorsement. | Both conditionals kept. | **Intact.** *Men* carries the pivot and the reservation after it is neither softened nor moved out of her mouth. | Her slightly deliberate "I would choose to do" is kept as *skulle välja att göra* rather than smoothed to *skulle göra om*; *lägga in* is deliberately a different verb from *avsätta* in Q2, matching the source's own two verbs. |

The material's "Lind did not recommend Svale to every housing company" is correctly rendered as narrative, not promoted into quotation marks. The material's note that her final quotation "is her actual, qualified assessment … not an inference from the figures" is honoured: the quotation sits in its own section, away from the medians, and the narrative sentence beside it presents her position as hers.

*Säger* is used for answers the material says came by email. Swedish journalistic usage applies *säger* to written statements as readily as spoken ones, and the draft honours what the email origin actually forbids: no physical scene, no emotion and no remembered dialogue appears anywhere. Not counted as a drift.

---

## 7. Intermediate — every checker finding

### Round 1 (`evidence/source-check-1/report.md`), four findings, no disposition file kept

| # | Passage | Allegation | What the writer did | Class |
|---|---|---|---|---|
| F1 | "…[checklistan för införande](…), **som går igenom stegen**." | The relative clause describes the destination's contents; the material describes only its purpose and what it is not. | Deleted the clause. | **Supported repair.** The finding is right — nothing supplied says the checklist walks through steps — and the brief names this among its judging criteria. |
| F2 | "**Åtta veckor senare** fanns både en testnotering … och en arbetsledare med en bedömning." | Places the 4 December note eight weeks after a September start, and puts the (undated) interview at that same moment. | Rewrote to "Efter åtta veckors test fanns…". | **Supported repair.** Right finding: only a start around 9 October would make the original true, and nothing supplied requires that. The replacement asserts sequence without an offset and is supported. |
| F3 | "någon jämförelse med en annan leverantör **finns inte**" | Turns "is available" into non-existence. | Added *att tillgå*. | **Supported repair.** Right finding, and the material's own contrast proves it: where it means absolute absence it writes "There are no … measurements". |
| F4 | Heading "teamet bestämde **innehållet**" | Widens "its categories" to the log's content. | Changed to "teamet bestämde **kategorierna**". | **Supported repair.** Right finding; the material grants the team the categories and the telephone channel and nothing further. |

Round 1 also recorded eight observations as explicitly not findings. The writer acted on three anyway — O2 (added "Elm Quays" to the note), O3 (*tillskriver … programvaran skillnaden*), O6 (*ni* → *du*) — and deleted the now-redundant "Testet pågick i åtta veckor." All four changes are supported by the material and improve the text; none introduces a new claim. They are visible only in the prose diff, since no round-1 disposition file was kept, which makes the writer's reasoning for them **not judgeable from the evidence** even though their result is sound.

### Round 2 (`evidence/source-check-2/report.md` + `disposition.md`), one finding

| # | Passage | Allegation | What the writer did | Class |
|---|---|---|---|---|
| 1 | "Telefonanmälan behölls för de boende." | The material names the maintenance team as the agent; the agentless s-passive drops it, immediately after a Svale-subject sentence, so the supplier is the nearest available subject. | Validated the finding, accepted it, and did **not** repair it, on the rule that prose is not changed after the final comparison. Carried the checker's exact repair ("Teamet behöll telefonanmälan för de boende.") into `response.md` for the editor. | **Right finding, accepted and disclosed, not repaired.** Not one of the named classes: it was neither rejected nor disputed, but the defect stands in the delivered text. The finding is correct — see F1-a. |

Round 2's section 4 lists eight items considered and not reported (title scope, *ärende*, *säger* by email, *har inte mätts*, past→present, missing disclosure, *programvaran* on first mention, material in the source not in the draft). The disposition reviewed and agreed with all eight. I agree with seven of them. The eighth, **4.6 — the missing supplier-published disclosure** — is correctly outside a source comparison's scope but is a genuine shortfall under G2, so treating it as settled understates it.

`response.md` additionally claims an anatomy measurement that "uppfyllde varje räknat krav, utan kvarstående avvikelse". **No report file exists for it**, and it names no finding, so there is nothing to classify; the claim itself is unevidenced in the run directory.

### Defects no checker saw

Three:

1. **The byline** (F1-b). Both rounds excluded it from accounting by declaration in their opening lines, so neither tested whether the material supports a named author. It does not.
2. **The Q3 heading as a class (a) bridge** (point 5). Round 2 checked quotations against their neighbouring *paragraphs* and concluded each contributes experience the prose does not state; neither round checked the heading immediately above Q3, which delivers that quotation's payload in advance.
3. **The publisher stance as a required part** (§3). Both rounds saw the missing disclosure and both classed it as an omission outside their scope. Against G2 it is a gap in a required job, not merely something left out.

---

## 8. Stop or delivery

**A valid delivery.** Two comparisons ran, both complete; the delivered prose is exactly what the second checker read; the one finding the second checker raised is real, is disclosed in the reply with the checker's exact repair, and is left to the editor rather than fixed silently after the final comparison. The residual defect is narrow — one dropped agent in one sentence — and touches nothing the brief forbids: no causal claim about the software, no money saved, no delighted residents, no rescued customer, no assignment time turned into completion time, and the customer's reservation survives twice over. Delivering with a named, repairable defect and an honest account of it is better for the editor than either a silent post-check edit or a stop.

Two things would have made the delivery stronger without breaching the no-edit-after-final-comparison rule: the byline should have been left for the editor rather than filled with a name the material does not supply (and, having been filled, should have been put to the checkers rather than declared out of scope), and the missing supplier-published disclosure should have been raised in the reply as a decision the editor must make, as the byline was, rather than mentioned as a passing note.
