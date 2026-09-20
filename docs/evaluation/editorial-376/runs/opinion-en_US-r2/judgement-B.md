# Judgement B — opinion, en_US, run r2

Judged from `write/work/source.md`, `write/response.md` and every file under `write/evidence/`. Nothing else was read.

---

## 1. Outcome

**A draft was delivered.** The reply carries the full piece inline in a fenced ````markdown` block, headed by an explicit disclosure that it ships with one known unrepaired defect.

**Two comparisons ran.** This is stated in the reply and corroborated by the evidence: `report-1.md` + `validation-1.md` (comparison 1), `report-2.md` + `validation-2.md` (comparison 2, described in its own validation as "the final comparison").

**Is the delivered prose byte-identical to the last prose a checker saw? Yes.** I extracted the fenced block from `response.md`, stripped the YAML frontmatter, and diffed it against `write/evidence/source-check/draft.md`: identical, byte for byte, with no whitespace difference.

The one difference between the delivered block and the evidence draft file is a metadata header the draft file does not carry:

```
---
kntnt:
  genre: opinion
  technique: none
  language: en_US
---
```

That is metadata, not prose. No sentence, heading, byline or title differs.

The dispositions agree. `validation-2.md` records: "**Not repaired.** This was the second and final comparison. After the final comparison no prose changes, not even into the repair the checker proposed, because a repair no comparison has read is unchecked prose. The draft is delivered exactly as this comparison read it." The diff confirms the claim rather than merely restating it.

One limit on the evidence worth naming: only one draft file is kept, and it is the post-repair draft (its second heading reads "The documents don't measure what the change saves"). The pre-repair draft is not in the evidence; the original heading is known only through the quotations in `report-1.md` and `validation-1.md`. That does not affect the identity check, which concerns the *last* prose a checker saw.

---

## 2. Remaining findings

The last comparison (`report-2.md`) raised exactly one finding. It was not repaired.

**Finding 1 — "What the six months themselves cost, we have not calculated, and we do not pretend otherwise."** (closing paragraph)

The checker's allegation: the material supplies only "Föreningen gör inget anspråk på att ha finansierat eller kostnadsberäknat försöket" — a statement about what the association *claims* — and the draft converts it into a first-person assertion of a negative fact about the association. Proposed smallest repair: "we make no claim to have calculated".

Does the delivered reply discharge the three duties?

- **Names the passage? Yes**, verbatim and with its location: "**\"What the six months themselves cost, we have not calculated, and we do not pretend otherwise.\"** (closing paragraph)".
- **Says what the supplied material carries instead? Yes**, and quotes the Swedish: "the clause states as a fact that Öppna beslut did not cost the trial. The material carries only that the association makes no claim to have costed it (\"Föreningen gör inget anspråk på att ha finansierat eller kostnadsberäknat försöket\"), which leaves open a costing the association simply does not put forward."
- **Gives a proposed smallest repair? Yes**, the checker's own: "replace *we have not calculated* with *we make no claim to have calculated*, leaving the rest of the sentence untouched."
- **Says it was not applied, and why? Yes**: "I did not apply it. It came out of the second and final comparison, and prose changed after the last comparison is prose no comparison has read."

The disclosure is complete and sits at the top of the reply, before the prose, not buried after it. It also states the consequence plainly: "I assert no fidelity for the passage it names."

No other finding from the last comparison is outstanding. `report-2.md`'s Observations A–G are recorded there as "not findings; no repair required", and `validation-2.md` disposes of them as "no change".

---

## 3. F1 — source fidelity, on the text the user received

**Verdict: FAIL — narrowly, on one clause. Every other assertion in the piece stays inside the material.**

### The one unsupported assertion

- **"What the six months themselves cost, we have not calculated"** — changed modality and certainty. Source: "Föreningen gör inget anspråk på att ha finansierat eller kostnadsberäknat försöket." The material states what the association claims; the draft states what the association did. A costing the association holds but does not put forward is compatible with every supplied sentence, and no supplied sentence excludes it. This is exactly the *unknown vs. absent* distinction F1 names. It is mitigated — the assertion runs against the speaker's own interest, the speaker has standing to know her own organisation's work, and the sentence preserves the cost uncertainty the boundary requires ("med kostnadsosäkerheten bevarad") — but mitigation is not support. The criterion asks whether *every* assertion stays within the material. One does not.

### What I checked and found clean

The rest of the draft holds up under my own reading of the source, including the traps the criterion names:

- **The pilot report's third unmeasured item.** The draft says the report "measures nothing about age, functional ability, or digital habits". Source: "Den mäter inte ålder, funktionsförmåga eller digital vana." *Digital vana* is rendered as **habits**, not as skill or ability. Correct.
- **Counts, and no size judgement attached to them.** "96 bookings through the web and 24 by phone", attributed to the report, with no "only", "just", "few" or "a mere". The boundary's "Siffror ska tillskrivas rapporten där de bär argumentet" is met.
- **The epistemic limit kept intact and not inverted.** "those 24 bookings cannot tell us what share of Lervik's residents are unable to book digitally" tracks "Telefonbokningarna kan därför inte användas för att säga hur stor andel av invånarna som inte kan boka digitalt". The draft does not slide into "so nobody is unable to book digitally" — the tempting inversion — and it keeps "may come from 24 different people or from a handful who call often" marked as possibility, which is precisely what a booking count leaves open.
- **Dates, spans and scopes.** April 8, 2026; eight weeks; two facilities; seven facilities; September; June 18; six months. All supplied, none drifted. The draft sets "two facilities" beside "seven" without ever claiming the pilot covered part of the same seven — the material does not say whether it did.
- **The administration's motive, and the refusal to falsify it.** "the administration is not claiming that people who call are lazy or costly" carries "inte att telefonanvändare är lata eller dyra" as a denial rather than as an imputation. The boundary "utan falska motiv" is not merely respected but made explicit in the text.
- **The absence located where the material locates it.** "the documents contain no time measurement and no savings calculation" tracks "finns inte i handlingarna", and the heading above it was repaired into the same scope.
- **The board's options.** "remove the phone route, change it, or keep it" narrows "om en kanal ska tas bort, ändras eller behållas" to the channel actually in question. A narrowing that excludes nothing the source leaves open; the sentence lists what the board can do, not what it cannot.
- **The supplied statement of position**, rendered unquoted in the author's own voice. The material permits it ("Detta får citeras eller refereras") and the speaker is the byline, so nothing is put in a third party's mouth. Meaning, indefinite scope ("någon" → "someone"), certainty ("inte ett bevis" → "no proof") and the agentless passive ("fortfarande används" → "is still being used") all carry.
- **Nothing invented.** No legal requirement, protest, discrimination case, party-political motive or savings figure — the five things the boundary marks as unestablished. No unnamed expert, no study, no scene, no personal attribute of any caller. No commercial CTA.

### Marginal, cited but not counted against F1

- **"Six months would give the board what the current documents lack: a labor cost that can be set against a value for users."** The trial as designed records *tidsåtgång per bokningsväg* (time) and *voluntary reasons*, not a labour cost and not a value. Getting from time to cost needs a rate; getting from voluntary reasons to a value is a further step. The material does supply "arbetskostnaden mot värdet för användarna" as what Sanna Ek wants weighed, and the sentence is conditional advocacy ("would give"), so this is a small inferential step inside the author's own proposal rather than a fabricated fact. Worth naming because **neither checker tested this axis** (see §5).
- **"enter the same information in two flows"** adds *same* to "föra in uppgifter i två flöden". The neighbouring "dubbel administration" supplies the duplication. Defensible.
- **"the report was not built to tell the difference"** states construction where the source states practice. What an ordinary reader takes from it — this report cannot separate 24 callers from a handful — is supplied outright.
- **"without being told what keeping it costs"** is slightly wider than "not in the documents", but the immediately preceding sentence scopes it to the documents.
- **"Eight weeks in two facilities is thin ground for a permanent change in seven"** is an evaluative judgement whose comparison is supplied in the same sentence (both counts, and the permanence), and the boundary licenses sharp criticism of the decision basis.
- **"Double administration is a real objection"**: "verklig invändning" means the *actual* objection; English "a real objection" can also read as *valid*. Either reading is the sender's own concession, and the material does state this is the administration's genuine objection.

---

## 4. G2 and L1, on the same text

### G2 — do the required parts do distinct useful jobs? **PASS.**

- **Early position.** Second sentence of the lead: "The board should postpone that switch and first run six months with both phone and web booking in place." Sentences three and four fence it: "I am not against digital booking. I am against deciding this on the documents now in front of the board." A reader who stops after the first paragraph knows the ask, the timeframe, and what is *not* being argued.
- **Support, in two sections that do different work.** "The pilot counted bookings, not people" attacks what the evidence *can* show; "The documents don't measure what the change saves" attacks what the evidence *fails to contain*. Neither restates the other. The first ends on a comparison (eight weeks, two facilities, against a permanent change in seven); the second ends on what the board is being asked to do without ("remove a booking route without being told what keeping it costs, or what removing it would free up").
- **A relevant real objection, honestly stated and answered.** "Double administration is a real objection, and I will be precise about it: the administration is not claiming that people who call are lazy or costly." This is the strongest thing the other side has, named as theirs, conceded as real, and explicitly protected from caricature — and then answered structurally: the proposed trial produces the very time figures that would let double administration be weighed. A second concession follows at the close (the trial's own cost is unknown). The piece does not knock down a straw man, which is the usual failure of this slot.
- **Identifiable action and actor.** "Postpone the permanent switch and start the trial", under the heading "What the board can decide on June 18". The actor is the municipal executive board, the date is named, and the *later* decision is kept distinct from the one asked for now ("When it ends, the board can remove the phone route, change it, or keep it").

Reader effect: four sections, four jobs, no paragraph that could be cut without losing an argument. The close names the decision, preserves the cost uncertainty, and still lands ("weighing it is still a better decision than making the choice blind").

### L1 — does it read as professionally written American English? **PASS, with named blemishes.**

What works. The syntax is native throughout — no Swedish word order, no calqued constructions, no participial pile-ups. The headline is a real English headline with a working pun ("Lervik should not hang up the phone in September"). The rhythm is op-ed rhythm: short declaratives against longer ones ("I am not against digital booking. I am against deciding this on the documents now in front of the board."), a colon used to land a payoff ("what the current documents lack: a labor cost that can be set against a value for users"), and controlled contractions in the argument's most conversational beat ("is no proof that someone can't use the web. It's a reason to find out why..."). Idioms are chosen, not translated: "thin ground", "what removing it would free up", "making the choice blind", "both ways in". US mechanics are consistent (*labor*, "April 8, 2026").

Where the Swedish shows. Three institutional nouns are carried across literally rather than rendered:

- **"enter the same information in two flows"** (*två flöden*). This is the clearest one. American English here would be *in two systems*, *in two places*, or *twice over*. "Flows" as a countable noun for an administrative process is not native usage, and a natural alternative was available and not taken. A reader pauses on it.
- **"Double administration is a real objection"** (*dubbel administration*). English would say *duplicate work*, *double entry*, *doing the job twice*. As a bare noun phrase opening a topic sentence it reads translated, though the preceding sentence has just glossed what it means, so comprehension does not break.
- **"association facilities"** (*föreningslokaler*). Understandable, and arguably unavoidable for a Swedish municipal institution with no US equivalent — but *community facilities* or *club rooms* would read less like a gloss.

I count these as terminology rendering, not as prose failure. Set against roughly 400 words of otherwise idiomatic argument, they do not make the piece sound translated; a reader would take them for municipal jargon. "Municipal executive board" and "staff memo" for *kommunstyrelsen* and *tjänsteutlåtande* are, by contrast, well chosen — they name the body and the document in their functional roles rather than transliterating them. Verdict stands at pass, with "in two flows" the one line I would change.

---

## 5. Intermediate — every checker finding, and what the writer did

**Comparison 1 (`report-1.md`, disposed in `validation-1.md`)**

| # | Passage | Allegation | Writer's action | Class |
|---|---|---|---|---|
| 1 | Heading "Nobody has measured what the change saves" | Widens an absence the material locates in the decision documents ("finns inte i handlingarna") into a universal negative about the world | Accepted; repaired to "The documents don't measure what the change saves" — the checker's own proposal, nothing else changed | **Supported repair.** The finding is right and the repair is the smallest one that fixes it; it also aligns the heading with the body sentence one line below, which was already correctly scoped |
| §5.1 | "knowing this time what each route costs and why people use it" | The *why* half rests on answers the material makes voluntary ("be användarna frivilligt ange"), so the clause may promise more than the trial yields | Raised as an editorial question, not a defect; no change | **Disputed caution, correctly left.** The clause is conditional advocacy for the author's own proposal, and "voluntarily" is carried four sentences earlier where the mechanism is described |
| §5.2 | "we have not calculated" | "Gör inget anspråk på att ha kostnadsberäknat" is not the same as "has not costed" | Raised as an editorial question, explicitly "No repair proposed"; no change | **Right finding rejected.** Comparison 1 reached the real defect and downgraded it to a non-defect on the ground that weakening the disclaimer would risk the boundary's required cost uncertainty. That reasoning is wrong on its own terms: the proposed repair comparison 2 later supplied ("we make no claim to have calculated") preserves the disclaimer *better*, not worse |
| §5.3 | Boundary sweep | No legal requirement, protest, discrimination case, party-political motive or savings figure asserted; no commercial CTA | No action needed | **Correct.** I verified each against the boundary paragraph |
| §3 | Rendering of the supplied statement of position | No translation findings | No change | **Correct.** I agree: meaning, indefinite scope, certainty and the agentless passive all carry, and the English is idiomatic |

**Comparison 2 (`report-2.md`, disposed in `validation-2.md`)**

| # | Passage | Allegation | Writer's action | Class |
|---|---|---|---|---|
| 1 | "What the six months themselves cost, we have not calculated" | A non-claim turned into an asserted negative fact about the association | **Accepted, and deliberately not repaired** — on the stated rule that prose changed after the final comparison is prose no comparison has read. Carried into the delivery account with its repair | **Right finding rejected in practice.** The finding is correct and I reach it independently under F1. The reason for not repairing is coherent and consistently applied, and the disclosure is full — but the defect reaches the user, and the piece is the poorer for it by one clause |
| A | "the report was not built to tell the difference" | States construction where the source states practice | No change | **Wrong finding rejected (correct).** What the sentence asserts in context is supplied outright |
| B | "enter the same information in two flows" | Adds "the same" to "uppgifter" | No change | **Wrong finding rejected (correct).** "Dubbel administration" in the neighbouring sentence supplies the duplication |
| C | "Double administration is a real objection" | *verklig* = actual; English "real" can be heard as *valid* | No change | **Wrong finding rejected (correct)** on fidelity. The ambiguity is real but both readings are open to the sender; I note it under L1 instead, on different grounds |
| D | "records how much time a booking takes by each route" | Commits the trial to per-booking timing where "tidsåtgång per bokningsväg" would allow an aggregate | No change | **Disputed caution, correctly left.** With 96 and 24 bookings the per-booking reading is the only informative one |
| E | "the board can remove the phone route, change it, or keep it" | Names the channel where "en kanal" is indefinite | No change | **Wrong finding rejected (correct).** A narrowing that excludes nothing |
| F | "will consider a staff memo" on June 18 | The memo is "inför" the meeting, not stated as taken up at it | No change | **Wrong finding rejected (correct).** The brief's own boundary presupposes the item is before the board that day |
| G | "without being told what keeping it costs" | Moves from "not in the documents" to "not told at all" | No change | **Disputed caution, correctly left.** Scoped by the sentence immediately before it |
| §3 | Rendering of the supplied statement | No translation findings | No change | **Correct** |

**Was a real defect I found under F1 seen by no checker?** No. The single defect I cite under F1 is the one comparison 2 raised and comparison 1 had already reached. Both checkers covered title, byline, every heading and every body sentence, and the coverage claims in the validations hold up against the draft.

One axis neither checker tested, offered as the gap in the checking rather than as a defect: whether the proposed trial, as the material describes it, actually yields the two things the draft says six months would give the board — **a labor cost** (the trial records *time*, and converting time to cost needs a rate the material never supplies) and **a value for users** (the trial collects *voluntary reasons*, which are not a value). Report 2's Observation D reaches the time measure but interrogates it on a different question (per-booking vs. aggregate), and report 1 §1.17 passes the sentence without touching the step at all. I do not count it against F1 — "arbetskostnaden mot värdet för användarna" is supplied as what Sanna Ek wants weighed, and the sentence is conditional — but it is the one place where both checkers stopped one question short.

---

## 6. Preservation — what the user is left holding

A draft was delivered, so the preservation question is not load-bearing; nonetheless, what the user holds is complete and honest:

- **The full prose**, inline in the reply, in a fenced block, with its metadata header. This is the only copy: the reply states "No artifact file was written, the run's scratch directory is removed, and `source.md` is untouched." No path is offered because none exists. Adequate, since nothing is elided.
- **The one unrepaired defect**, disclosed *before* the prose rather than after it, with the passage quoted, the Swedish the material actually carries quoted beside it, the smallest repair named, and the reason it was not applied stated. The reply does not soften it: "I assert no fidelity for the passage it names."
- **What was and was not compared.** "Two comparisons ran." The first finding and its repair are described ("a heading that widened an absence in the decision documents into a claim about the world"), the second's residue is the disclosed defect, and the reply states the coverage both reports claim — every draft passage, headline and heading paired with its Swedish source, and no translation finding against the rendering of Sanna Ek's statement.
- **Four honest gaps in the material**, under "Where the material stopped": no cost figure for six months of double booking, no data on who the 24 phone bookings came from, no time measurement to weigh double administration against, and no statement whether the two pilot facilities are among the seven. Each names what evidence would close it. This is the most useful part of the reply for a user who has to decide whether to publish.
- **A length account**: body 408 words against a brief asking for roughly 400, with "Nothing was cut to fit and nothing was added to reach it." I verified the body at 408. (The reply's second figure, 452 including headline, byline and headings, counts 457 by whitespace tokens — a trivial discrepancy in how the em dash and italic markers are counted, not a misstatement.)

The user can publish this piece today, knows the single sentence they should change first, and knows what a stronger version would need that the material could not give.

---

## Verdicts at a glance

| | |
|---|---|
| **Outcome** | Draft delivered; two comparisons; delivered prose byte-identical to the draft the last checker read (frontmatter added, no prose change) |
| **F1** | **Fail** — one clause: "we have not calculated" asserts a negative the material supplies only as a non-claim. Everything else holds, including the *digital vana* → "habits" rendering |
| **G2** | **Pass** — early position, two non-overlapping supports, a real objection conceded and answered without a straw man, a named actor and a dated action |
| **L1** | **Pass** — native syntax and idiom throughout; "in two flows", "double administration" and "association facilities" are literal carry-overs of Swedish institutional nouns, the first being the one I would change |
