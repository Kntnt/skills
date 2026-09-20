# Run judgement — opinion / en_US / r1

Judged from `write/work/source.md`, `write/response.md` and `write/evidence/sourcecheck/` (two reports, two drafts). Nothing else was read.

## 1. Outcome

**A draft was delivered.** The reply opens "The draft is delivered with known defects" and carries the full piece inline, followed by a resolution note.

**Two comparisons ran.** `report-1.md` ("round 1") compares the text preserved as `draft-r1.md` and raises five findings, F1–F5. `report-2.md` compares the text preserved as `draft.md` — the repaired text — and raises three, F1–F3. Despite the file names, `draft-r1.md` is the *earlier* text (it contains every passage report‑1 quotes as defective) and `draft.md` is the later one.

**The delivered prose is byte-identical to the last prose a checker saw.** Extracted from `response.md` between the title line and the closing `---`, the delivered article matches `evidence/sourcecheck/draft.md` byte for byte (verified by exact string comparison; no diff). `report-2.md` quotes that file's repaired wordings ("two rooms", "Those 24 bookings", "it is not that the people who phone are lazy or expensive", "We make no claim to have costed or funded that trial", "the cost of the work"), so `draft.md` is what the second checker read. No disposition file exists in the evidence, but the reply's own account of what changed after the last comparison — "after the last comparison the prose stays exactly as that comparison read it" — is **true**. Nothing was edited post-comparison.

For completeness, the five repairs made *between* the two comparisons (all visible as the diff `draft-r1.md` → `draft.md`):

| Round-1 text | Delivered text |
|---|---|
| "in two of the rooms" | "in two rooms" |
| "Those 24 calls therefore cannot tell the board" | "Those 24 bookings therefore cannot tell the board" |
| heading "A channel closed on an unmeasured inconvenience" | "Closing a channel on an unmeasured inconvenience" |
| "nothing in the documents calls the people who phone lazy or expensive" | "it is not that the people who phone are lazy or expensive" |
| "We have not costed that trial and make no claim to fund it" | "We make no claim to have costed or funded that trial" |
| "weighed the staff time against" | "weighed the cost of the work against" |

Each of the five matches, word for word, the "smallest repair" report‑1 proposed. The heading change was not a finding; report‑1 raised it as an editorial question in §5 and the writer acted on it anyway.

## 2. Remaining findings

Three findings from the last comparison were left unrepaired. **All three are named in the reply, each with the passage quoted, the supplied material quoted in Swedish, and a proposed smallest repair.** The reply's rendering is faithful to `report-2.md` §7 in every particular.

**R2‑F1 — "decides" on 18 June.** Passage: "On 18 June the municipal executive board decides whether phone booking … ends in September", plus the heading "What the board can decide on 18 June." Reply says, verbatim:

> The material puts a staff recommendation *before* the board's meeting of 18 June ("Tjänsteutlåtandet inför kommunstyrelsens möte den 18 juni föreslår…"); it does not say the decision falls at that meeting. The item could be taken up on 18 June and referred back. Proposed repair: "decides whether" → "takes up whether", and the heading → "What the board can do on 18 June."

Passage named: yes. Material given: yes. Smallest repair given: yes.

**R2‑F2 — "for the first time".** Passage: "and say for the first time what that choice costs and what it buys". Reply:

> The material locates the absence in the case papers only ("Någon tidsmätning eller ekonomisk besparingsberäkning finns inte i handlingarna"), not everywhere; a costing could exist outside them. Proposed repair: delete "for the first time", or tie it to the papers — "and say, as the June papers never did, what that choice costs and what it buys."

Passage named: yes. Material given: yes. Repair given: yes.

**R2‑F3 — "per booking".** Passage: "records how long each route takes per booking". Reply:

> The material asks for "tidsåtgång per bokningsväg" — time per booking *route*. Total hours logged per route would satisfy the source but not the draft's wording. Proposed repair: "records the time each route takes", or "records time spent per booking route."

Passage named: yes. Material given: yes. Repair given: yes.

The reply also states, accurately, that the prose is unchanged since that comparison, so the user can act on all three against the text in front of them.

## 3. F1 — factual fidelity to the supplied material (delivered text)

**Verdict: fail**, on three unsupported items that survive into the delivered text. All are phrase-level, none touches a figure, a name, a date or the argument's spine, and all three are disclosed to the user — but the criterion asks whether every assertion and implication stays inside the material, and these do not.

Unsupported additions / changed claims:

1. **Chronology and event — "On 18 June the municipal executive board decides whether phone booking of Lervik's seven community rooms ends in September"** (lead), and the heading **"What the board can decide on 18 June"**. The material supplies only: "Tjänsteutlåtandet inför kommunstyrelsens möte den 18 juni föreslår att telefonbokning tas bort för alla sju lokaler från september." A staff recommendation standing *before* a meeting is not a statement that the matter is settled at it; the item could be taken up and referred back for the very figures the piece says are missing, with September still the proposal on the table. This is the lightest of the three — the brief's own thesis and its judging boundary ("Slutet ska namnge kommunstyrelsens möjliga beslut") do make the board the deciding body — but the draft states the *occasion* of the decision as fact, and nothing supplied establishes it.

2. **Scope of a negative — "and say for the first time what that choice costs and what it buys"** (close). The material locates the absence precisely: "finns inte i **handlingarna**". "For the first time" widens it to everywhere and always. A costing produced during the web system's procurement, absent from the June papers, would leave the source true and the draft false. This is a dropped caveat as much as an addition: the material's one locative qualifier is removed.

3. **Changed thing measured — "the administration records how long each route takes per booking"** (proposed trial). The material specifies "registrera **tidsåtgång per bokningsväg**" — time consumption broken down by booking route. Total staff hours logged per route, with no per-booking timing, satisfies the source and not the draft. The distinction is live, because this sentence *is* the specification of the trial the board is asked to order, and the piece's whole case is that the board must be able to weigh work cost against user value.

Lesser items, cited as required but not carrying the verdict on their own:

4. **"it measures neither age nor ability nor digital habits."** The third item is correct — "digital vana" is rendered as habit, not as skill or ability, which is the reading the material requires. The *second* item broadens: "funktionsförmåga" is functional (disability-dimension) ability, while bare "ability" reaches competence of any kind, so the draft's negative claims slightly more than the report's. In the run of three, the disability sense is the available reading and the sentence's work — that the report holds no user attribute at all — is unchanged. Both checkers saw it and recorded it as a note; I agree it is defensible, and flag it only because the wider term is asserted in a negative.

5. **"before anyone has weighed the cost of the work against what the channel is worth to its users."** The material gives her condition as capability: "kommunen först måste **kunna** väga arbetskostnaden mot värdet för användarna." The draft states it as performance ("has weighed") and broadens the actor from the municipality to "anyone". Neither shift asserts anything about the world that the source denies — being able to weigh and having weighed are not separable here, since the material says no time measurement or savings calculation exists at all — and it is carried as her standpoint, which the brief makes hers. Defensible; recorded.

6. **"community rooms" for "föreningslokaler"** (and "rooms" thereafter). Tested both ways: a hall bookable only by registered associations falls under "föreningslokal" but not comfortably under "community room", and a room open to the public generally falls under "community room" but not under "föreningslokal". No claim rides on it — the counts ("seven", "two") are exact, the report title is kept in Swedish, and every assertion concerns how the premises are booked, not what they are. Not a defect; "the seven premises local clubs book" would be tighter.

What is **clean**, and deserves saying because the material's traps are real:

- **The counts.** "96 bookings made on the web and 24 made by phone" is exact, attributed to the report as the brief demands, and — crucially — never characterised. The piece never calls 24 small, marginal or a mere fraction; no count-size judgement is made without a supplied comparison.
- **Unknown kept apart from absent.** "Those 24 bookings therefore cannot tell the board what share of residents is unable to book digitally. They cannot tell it that nobody is, either." The second sentence has no source passage, but it is the state-of-knowledge point itself and preserves uncertainty in both directions rather than extending it. This is the single best thing in the piece against this criterion.
- **Motive.** "That objection is double administration, and I will not pretend it is anything meaner: it is not that the people who phone are lazy or expensive" carries "Förvaltningens verkliga invändning … inte att telefonanvändare är lata eller dyra" in the source's own terms. No false motive is imputed, and the criticism is not neutered — exactly the boundary the material sets.
- **Cost uncertainty.** "We make no claim to have costed or funded that trial; what it would cost is for the board to weigh" carries both disclaimers as disclaimers, not as facts, and the close leaves the cost with the board ("with its cost settled in the open" is an ask, not an assertion that anything is settled or hidden). "Kostnadsosäkerheten bevarad" is met at both places it arises.
- **Excluded categories.** No legal requirement, protest, discrimination case, party-political motive or saving is asserted anywhere. The only savings statement is the absence of one.
- **Modality.** "proposes" for "föreslår", "can remove … change … or keep" for "kan … tas bort, ändras eller behållas" — kept throughout. The narrowing of "en kanal" to "the phone channel" narrows a permission, which asserts nothing the source denies.
- **Attribution and voice.** Sanna Ek's standpoint is rendered unquoted in her own first person under her byline, which "Detta får citeras eller refereras" permits; meaning, polarity and certainty are intact, including "I am not against digital booking" for "Hon motsätter sig inte digital bokning" — not upgraded to support.

## 4. G2 — do the required parts do distinct jobs?

**Verdict: pass.**

- **Early position.** Paragraph one, second sentence: "Öppna beslut asks the board to postpone that change and try six months with both the phone and the web first." The reader knows the ask before the first heading, and the title states it too.
- **Support.** §1 does its own job: the pilot's size and counts, and then its stated limits — bookings not people, no age, ability or digital habits. It supports the position by removing a reading (that 24 phone bookings measure exclusion) rather than by repeating the ask. §2 does a *different* job: the absence of any time measurement or savings calculation in the papers. Two distinct evidentiary moves, not one made twice.
- **Relevant real objection.** "Its reason is that staff should not have to enter the same details in two flows. That objection is double administration, and I will not pretend it is anything meaner." This is the strongest part of the piece against G2: it names the opponent's *actual* reason, refuses the cheap version of it, and then answers it on its merits — "keeping it is said to cost work, without being told how much work" — rather than dismissing it. The answer is also the bridge to the proposal, so the objection is load-bearing, not a token.
- **Identifiable action and actor.** §4, under a heading that names both: the board (actor) postpones the September removal and orders the trial (action), with the cost settled openly, and after six months removes, changes or keeps the channel. A reader knows exactly who must do what, and when.

Reader effect: four sections, four jobs — what the evidence can't show, what the papers don't contain, what to do instead, what the board decides. Nothing is argued twice, and the personal turn ("I am not against digital booking. I am against settling the question before …") lands as a position statement rather than filler, because it sharpens the ask rather than restating it.

## 5. L1 — native en_US prose

**Verdict: pass, with three blemishes.**

The piece reads as professionally written English. Sentence rhythm is varied and controlled ("Neither side of that scale has a number on it, which is a thin basis for a permanent decision"); the English is built from English, not from Swedish syntax carried across ("A booking that comes in by phone" for "Att en bokning går via telefon"; "find out" for "ta reda på"; "I will not pretend it is anything meaner"). Agreement is en_US throughout — "what share of residents **is** unable", and collectives singular ("the board is asked", "the administration records"). Headings orient rather than tease. Nothing reads as translationese at the sentence level.

Three blemishes, all lexical and none fatal:

1. **"enter the same details in two flows"** — "flows" is a straight carry of "flöden". An American reader meets "flow" as a process-diagram word, not as a place where you enter data; "in two systems" or "twice, in two places" is how this is said in English.
2. **"That objection is double administration"** — a calque of "dubbel administration". English would say duplicate administration, duplicated work, or doing the same job twice. There is a defence — the material names the objection in those words, and carrying an opponent's own term is legitimate — but the draft presents it in its own voice, unquoted, so the defence is partial.
3. **"We make no claim to have costed or funded that trial"** — "costed" in the sense of *having estimated the cost of* is a chiefly British register; American prose reaches for "priced", "budgeted" or "put a cost on". Worth flagging in the run's own terms: this wording arrived as the round‑1 repair, taken verbatim from report‑1's proposed fix. The repair corrected a real source defect and imported a small en_US blemish while doing it — neither checker's remit covered that, so nothing caught it.

Separately, and **not** an L1 matter: "dated 8 April 2026" is day-month-year, which is locale mechanics rather than idiom. American convention is "April 8, 2026". I record it so it is not mistaken for a prose fault.

## 6. Intermediate — every checker finding, and what the writer did

Round 1 (`report-1.md`), five findings, all repaired exactly as proposed:

| # | Passage | Allegation | Writer's action | Class |
|---|---|---|---|---|
| R1‑F1 | "Those 24 **calls**" | Counts calls; the material counts bookings ("96 bokningar via webb och 24 via telefon"), and expressly warns the report counts bookings, not unique people | Repaired to "Those 24 bookings" | **Supported repair.** Real: one caller booking three rooms yields three bookings and one call, and the sentence sits in the very paragraph arguing a count must not be read as a count of something else |
| R1‑F2 | "nothing in the documents calls the people who phone lazy or expensive" | Converts a claim about the administration's objection into a claim about the documents' text | Repaired to "it is not that the people who phone are lazy or expensive" | **Supported repair.** Real: the material states what the objection *is not*, not what the papers say; a passing line about telephone handling being costlier would break the draft and not the source |
| R1‑F3 | "in two **of the** rooms" | Asserts the pilot's two premises are among the seven | Repaired to "in two rooms" | **Supported repair.** Real: "i två lokaler" and "alla sju lokaler" are never linked in the material |
| R1‑F4 | "We have not costed that trial and make no claim to fund it" | Turns a disclaimer into an assertion of fact, and shifts "ha finansierat" (past) to prospective "fund" | Repaired to "We make no claim to have costed or funded that trial" | **Supported repair.** Real, and it lands on the one point the boundaries require be preserved ("kostnadsosäkerheten bevarad") |
| R1‑F5 | "the staff time" | Narrows "arbetskostnaden" (cost of the work) to one input | Repaired to "the cost of the work" | **Supported repair.** Real: licences, a handset line or training would leave her stated condition unmet while the draft's is met |
| R1 §5 (a) | "On 18 June … decides" | Raised, then **classed as the brief's own premise, not a defect**; no repair proposed | No change | **Right finding rejected** — by the checker, not the writer. Report‑2 later raised the same passage as a finding. The reasoning in report‑1 §5 is honest about being unsettled, but the call was wrong |
| R1 §5 (b) | Heading "A channel closed on an unmeasured inconvenience" | Could read as already accomplished; flagged for the editor only | Changed to "Closing a channel on an unmeasured inconvenience" | **Supported repair**, and unforced — the writer acted on an editorial note that carried no obligation, and the participle ambiguity is genuinely gone |

Round 2 (`report-2.md`), three findings, none repaired:

| # | Passage | Allegation | Writer's action | Class |
|---|---|---|---|---|
| R2‑F1 | "decides whether … ends in September"; heading "What the board can decide on 18 June" | The material puts a recommendation before the meeting; it does not say the decision falls there | Not repaired; disclosed to the user with report‑2's proposed repair | **Right finding, accepted as real but shipped.** I hold it a genuine (if light) unsupported assertion — see §3, item 1 |
| R2‑F2 | "say for the first time what that choice costs" | Extends an absence located in "handlingarna" to everywhere | Not repaired; disclosed with the proposed repair | **Right finding, accepted as real but shipped.** Genuine — §3, item 2 |
| R2‑F3 | "records how long each route takes per booking" | Source specifies time per booking *route* | Not repaired; disclosed with the proposed repair | **Right finding, accepted as real but shipped.** Genuine, and the sharpest of the three — §3, item 3 |
| R2 §6 (a)–(e), §4 notes | Indicative tense inside the proposal; "before anyone has weighed"; "en kanal" narrowed; "Kommunens" dropped; length; "ability"; "community rooms"; "digital habits" | Each checked and recorded as defensible rather than left silent | No change | **Wrong-finding-rejected (correct)** in substance: each is correctly *not* raised as a defect, and I reach the same conclusion on every one (see §3, items 4–6) |

Report‑2 also re-checked all five round‑1 repairs and passed each as written (items 7, 10, 15, 23, 26), so the repairs were independently confirmed rather than taken on the writer's word.

**Did a real defect escape every checker?** No. Every F1 item I found in the delivered text was seen: the three live ones are report‑2's F1–F3, and the three lesser ones (ability, "has weighed", community rooms) were seen by both checkers and knowingly classed as notes, which I agree with.

**But one checker missed a great deal.** All three of report‑2's findings were present, word for word, in the round‑1 draft — "for the first time" and "how long each route takes per booking" are in `draft-r1.md` unchanged — and report‑1 raised neither, while raising the 18 June passage only to dismiss it. Checker 1 found five real defects and missed three; checker 2 found the three and confirmed the five repairs. The second comparison earned its keep, and the run would have delivered three undisclosed defects without it.

**And one defect is outside any checker's remit:** "costed" (§5, blemish 3) entered the text *as* a source-fidelity repair. Neither report judges en_US idiom, so nothing in the run could have caught a fidelity fix that costs a little idiom.

## 7. Preservation

The user is left holding a complete, usable deliverable:

- **The prose itself, in full, inline** in `write/response.md`, with the `kntnt` frontmatter map (`genre: opinion`, `technique: none`, `language: en_US`).
- **A numbered account of all three unrepaired findings**, each naming its passage, quoting the Swedish the material actually carries, and proposing a smallest repair — enough to settle every one without opening a report or re-reading the source.
- **An accurate statement of what changed after the last comparison**: nothing. Verified byte for byte.
- **A "Where the material stopped" section** naming the four places the material ran out — no cost for the trial, no time measurement or savings calculation, no statement whether the pilot's two premises are among the seven, no procedural statement about 18 June — plus the length (about 420 words against "ungefär 400": 448 words including headings, 403 excluding them, so the reply's figure is fair and the brief is met).
- **A filesystem note** saying both reports and both drafts remain at `evidence/sourcecheck/` and that `work/source.md` is untouched.

The "no draft delivered" branch does not apply. On the related question of disclosure, the reply says "Both comparisons found no translation defect", which is true of both reports and implies the count of comparisons, but it does not tell the user that the first comparison raised five further defects that were repaired before the second ran. Nothing is misstated, and the state of the delivered text is reported exactly; a reader simply cannot tell from the reply alone how much was fixed on the way, or that the second checker caught what the first had missed. That is a transparency gap rather than an error, and the evidence files the reply points at close it.

## Verdict summary

| Criterion | Verdict |
|---|---|
| Outcome | Draft delivered; two comparisons; delivered prose byte-identical to the last draft a checker saw |
| Remaining findings | 3, all named in the reply with passage, material and smallest repair |
| F1 | **Fail** — three unsupported items survive (18 June as the decision occasion; "for the first time"; "per booking" for "per bokningsväg") |
| G2 | **Pass** |
| L1 | **Pass**, with "in two flows", "double administration" and "costed" as blemishes |
| Preservation | Strong: full prose, all three defects actionable, no post-comparison edits |
