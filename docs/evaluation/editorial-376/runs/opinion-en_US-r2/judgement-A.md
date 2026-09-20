# Judgement A — run `opinion-en_US-r2`

Judged from `write/work/source.md`, `write/response.md` and the five files under `write/evidence/source-check/`. Nothing else read. The checkers' and the writer's own approvals are weighed as arguments; every verdict below is taken from the supplied material directly.

---

## 1. Outcome

**A draft was delivered.** It arrives in the reply itself, in full, inside a fenced block, preceded by an explicit disclaimer of fidelity for one named passage.

**Two comparisons ran.** `report-1.md` → `validation-1.md` (one finding, repaired) → `report-2.md` → `validation-2.md` (one finding, accepted, not repaired). `validation-2.md` states the rule applied: "After the final comparison no prose changes, not even into the repair the checker proposed."

**Is the delivered prose byte-identical to the last prose a checker saw?** **Yes.** I extracted the fenced block from `response.md` and diffed everything from `# Lervik should not hang up the phone in September` onward against `write/evidence/source-check/draft.md`: identical, byte for byte, to the closing full stop. The only difference in the delivered block is a YAML header the evidence file does not carry —

```
---
kntnt:
  genre: opinion
  technique: none
  language: en_US
---
```

— which is metadata about the run, not prose, and asserts nothing about Lervik. The dispositions corroborate the diff: `validation-2.md` records the second finding as "**Not repaired**… The draft is delivered exactly as this comparison read it," and lists no other post-comparison edit. The single draft file in the evidence is the repaired draft (it carries "The documents don't measure what the change saves"), and `report-2.md` quotes that heading as the text it read, so the file is the state comparison 2 saw, not a later overwrite.

The reply's arithmetic also checks out: body 408 words, 452 with headline, byline and headings, against a brief asking for "ungefär 400 ord".

---

## 2. Remaining findings from the last comparison

The last comparison raised exactly one finding. It was not repaired.

**Finding (report-2 §2, Finding 1)** — the closing paragraph's *"What the six months themselves cost, we have not calculated, and we do not pretend otherwise."*

| Does the reply… | | |
|---|---|---|
| name the passage? | **Yes** | It quotes it verbatim in bold and locates it: "(closing paragraph)". |
| say what the supplied material carries instead? | **Yes** | It quotes the Swedish: "the material carries only that the association makes no claim to have costed it (*"Föreningen gör inget anspråk på att ha finansierat eller kostnadsberäknat försöket"*), which leaves open a costing the association simply does not put forward." |
| give a proposed smallest repair? | **Yes** | "replace *we have not calculated* with *we make no claim to have calculated*, leaving the rest of the sentence untouched." That is the checker's own proposal, reproduced accurately from `report-2.md` §2. |

The reply also says why it was not applied: "I did not apply it. It came out of the second and final comparison, and prose changed after the last comparison is prose no comparison has read." And it opens by asserting no fidelity for that passage.

**One gap in the account.** The reply describes the first comparison as having "found one defect" and does not mention that comparison 1 had already reached this same passage and filed it as an editorial question with no repair proposed (`report-1.md` §5.2, endorsed by `validation-1.md`). A reader of the reply would take the defect for something the second checker turned up fresh; in fact both checkers reached it and the first one talked itself out of it. `validation-2.md` records this ("The first comparison reached the same gap and recorded it as an editorial question"), but that file never reached the user. Nothing in the reply is false; something material to how confident a reader should be is missing.

No other finding stands unrepaired: `report-2.md`'s Observations A–G are explicitly "not findings; no repair required", and I agree with leaving each of them (see §5).

---

## 3. F1 — source fidelity of the delivered text

**Fail**, narrowly, on one passage; every other claim in the piece holds.

### The defect

**Draft:** "What the six months themselves cost, we have not calculated, and we do not pretend otherwise."
**Material:** "Föreningen gör inget anspråk på att ha finansierat eller kostnadsberäknat försöket."

The material states what the association *claims*; the draft states what the association *did*. A non-claim is turned into an asserted negative fact, in the first person. The counter-case is live and nothing supplied excludes it: the association may hold a rough internal costing it has chosen not to put forward in this debate, in which case the Swedish sentence holds and the English one is false. This is exactly the criterion's "Keep unknown apart from absent", and it is a dropped caveat — "gör inget anspråk på" is the caveat, and it is gone. That the overstatement runs *against* the speaker's interest, and that the boundary "med kostnadsosäkerheten bevarad" is still satisfied by the surrounding sentences, make it a small defect; they do not make it not a defect. The repair costs five words and nothing else in the sentence.

(The same sentence also drops "finansierat". That subtracts half a disclaimer and adds no claim; not a defect.)

### What I checked and found clean

- **Dates, figures, scopes.** April 8 2026; eight weeks; two facilities; 96 web and 24 phone bookings; seven facilities; September; six months; June 18 — each matches the material, each is attributed to the report, the memo or the proposal as the material assigns it, as the boundary "Siffror ska tillskrivas rapporten där de bär argumentet" requires. The pilot's figures are never extended to the seven facilities.
- **The third unmeasured thing.** The criterion is explicit that it must be habit, familiarity or experience, not skill or ability. The draft writes "digital habits" for "digital vana" — correct. "funktionsförmåga" → "functional ability" is the second item and is the right pairing; neither term is swapped into the other's slot.
- **The epistemic limit.** "So those 24 bookings cannot tell us what share of Lervik's residents are unable to book digitally" carries "Telefonbokningarna kan därför inte användas för att säga hur stor andel av invånarna som inte kan boka digitalt" without strengthening it into a claim that no such residents exist. Unknown stays unknown.
- **Count-size judgement.** "Eight weeks in two facilities is thin ground for a permanent change in seven" is evaluative, and its comparison sits in the same sentence out of supplied numbers (2 against 7, eight weeks against permanent). The boundary licenses the author to "kritisera beslutsunderlaget skarpt".
- **The administration's motive.** "the administration is not claiming that people who call are lazy or costly" reproduces "inte att telefonanvändare är lata eller dyra" as a denial rather than an imputation — the boundary's "utan falska motiv" is honoured, in the one place a lesser draft would have broken it.
- **Absences kept where the material puts them.** "the documents contain no time measurement and no savings calculation" and the repaired heading "The documents don't measure what the change saves" both stay inside *handlingarna*. The heading is the version comparison 1 forced; the version comparison 1 found ("Nobody has measured what the change saves") would have failed F1, and the repair is exactly right.
- **The supplied statement of position.** Rendered unquoted, which the material permits ("Detta får citeras eller refereras"), by the person who said it. Meaning, indefinite scope ("någon" → "someone"), certainty ("inte ett bevis" → "no proof") and the agentless passive ("används" → "is still being used") all survive. Both directions tested: nothing falls under "no proof that someone can't use the web" that does not fall under the Swedish, or the reverse.
- **Boundary sweep.** No legal requirement, no protest, no discrimination case, no party-political motive, no savings figure. No invented expert, study, scene or personal attribute. No commercial CTA. No claim that the two pilot facilities are or are not among the seven. No claim the association would fund the trial.
- **Term crossings, both directions.** *kommunstyrelsen*/"municipal executive board", *tjänsteutlåtande*/"staff memo", *förvaltningen*/"the administration", *handlingarna*/"the documents", *bokningsväg*/"booking route", *dubbel administration*/"double administration" — in this context nothing falls under the English and not the Swedish, or the reverse.

### Borderline, examined and cleared

- "the report was not built to tell the difference" states purpose where the material states practice ("räknar bokningar, inte unika personer"). The asserted content a reader takes — this report cannot separate 24 callers from a handful — is supplied outright. Cleared.
- "enter the same information in two flows" adds "same" to "uppgifter"; "dubbel administration" in the next supplied sentence is what sameness names. Cleared.
- "records how much time a booking takes by each route" commits the trial to per-booking timing where "tidsåtgång per bokningsväg" would tolerate a per-route aggregate. With 96 and 24 bookings the per-booking reading is the only useful one and the payoff sentence holds either way. Cleared, thinly.
- "the board can remove the phone route, change it, or keep it" narrows "en kanal" to the phone route — fewer options than the material allows the board, never more, and the sentence excludes nothing. Cleared.
- "will consider a staff memo" on June 18, from "inför kommunstyrelsens möte den 18 juni". A memo written for a dated meeting is that meeting's item, and the brief's own ending boundary presupposes the board deciding there. Cleared.
- "without being told what keeping it costs" moves from an absence in the papers to an absence in what the board hears. It follows directly on the correctly scoped sentence and reads as the argument from it. Cleared.
- "Six months would give the board what the current documents lack" substitutes "the board" for the material's "kommunen"; the board is the body the same material puts the cost decision on. A narrowing. Cleared.

---

## 4. G2 and L1 on the delivered text

### G2 — do the required parts do distinct useful jobs? **Pass.**

- **Early position.** Sentence two of the lead: "The board should postpone that switch and first run six months with both phone and web booking in place," sharpened by the two short sentences after it. The reader knows the ask before the first heading.
- **Support.** Two sections carrying different loads, not one argument twice. "The pilot counted bookings, not people" attacks what the evidence *can* show; "The documents don't measure what the change saves" attacks what the evidence *does not contain*. Remove either and the case is weaker in a different way.
- **A relevant real objection, met.** "Double administration is a real objection, and I will be precise about it: the administration is not claiming that people who call are lazy or costly." This is the strongest thing the other side actually has, named as theirs, conceded rather than caricatured — and then answered three paragraphs later, since the trial's time recording is what would let double administration be priced. That is the objection doing work, not a token nod.
- **Identifiable action and actor.** "What the board can decide on June 18" / "Postpone the permanent switch and start the trial." The actor is the municipal executive board, the moment is dated, and the action is two verbs. The later decision is kept separate from this one, so the reader is not asked for two things at once.

Reader effect: a resident finishes knowing who decides, when, what to ask them for, and what the piece is *not* claiming. Nothing in the five sections is ornamental.

### L1 — professional en_US prose? **Pass.**

Idiom and syntax are native throughout, and no Swedish phrasing is imported. "hang up the phone in September" carries the whole thesis in a headline idiom that has no Swedish original. "Eight weeks in two facilities is thin ground for a permanent change in seven" is compressed English of a kind a translator rarely produces. "what removing it would free up", "making the choice blind", "both ways in" are all AmE. The contractions ("don't", "can't", "It's") sit at the right register for a signed op-ed and are used sparingly enough not to slide into chattiness. The fronted object in "What the six months themselves cost, we have not calculated" is marked but grammatical English topicalisation, and reads as rhetoric rather than as Swedish word order. Paragraph lengths vary; no sentence has to be read twice.

Residual blemishes, none disqualifying:

- **"association facilities"** for *föreningslokaler* is the one near-calque. In AmE "association" first suggests a homeowners' or trade association; "community facilities" or "club rooms" would land more naturally. It is used consistently and is never ambiguous in context.
- **"functional ability"** is administrative register rather than op-ed register — but it is naming what a report measures, so the register is arguably the report's, not the author's.
- **"the administration"** for *förvaltningen* faintly evokes a presidential administration to an American ear; "city staff" is the more American term. Consistent use plus "The memo's stated motive" anchors it.
- **"weighing it is still a better decision than making the choice blind"** is loose logic in an otherwise precise piece: weighing is not itself a decision. The sentence still reads cleanly aloud.

None of these is a Swedish construction in English clothing; they are ordinary choices an English-first editor might question.

---

## 5. Intermediate — every checker finding, and its disposition

| # | Passage | Allegation | What the writer did | Class |
|---|---|---|---|---|
| R1 F1 | Heading "Nobody has measured what the change saves" | Widens an absence in *handlingarna* into a universal negative about the world | Accepted; heading replaced with the checker's own proposal "The documents don't measure what the change saves"; nothing else changed (`validation-1.md`) | **Supported repair.** The finding was right — the material says only "finns inte i handlingarna" — and the repair is the smallest one that works and matches the body sentence below it. |
| R1 §5.1 | "knowing this time what each route costs and why people use it" | The *why* half rests on answers the material makes voluntary | Recorded as an editorial question; no change | **Wrong finding rejected (correct).** "voluntarily" is carried four sentences earlier where the mechanism is described, and the clause is conditional advocacy for the author's own proposal. |
| R1 §5.2 | "we have not calculated" | A non-claim ("gör inget anspråk på") stated as an asserted negative | Filed as an editorial question, explicitly "No repair proposed"; no change | **Right finding rejected.** This is a real F1 defect, and comparison 1 had it in hand. The stated reason — that weakening it would endanger the boundary's "kostnadsosäkerheten bevarad" — does not hold: "we make no claim to have calculated" preserves the uncertainty at least as well. Had it been treated as a finding here, comparison 2 would have read a clean draft and the run would have delivered without a known defect. |
| R1 §3 | Rendering of Sanna Ek's supplied statement | — | No translation findings | **Correct.** I reach the same result independently. |
| R2 F1 | "What the six months themselves cost, we have not calculated, and we do not pretend otherwise." | Unclaimed fact turned into an asserted negative | Accepted as correct; **not repaired**, on the rule that prose changed after the final comparison is prose no comparison has read; carried into the delivery account with the proposed repair (`validation-2.md`) | **Supported finding, accepted and left standing.** The finding is right, the reasoning in both directions is right, and the proposed repair is the smallest one. The non-repair is a defensible procedural choice, honestly disclosed — but it is the cost of R1 §5.2 having been rejected. |
| R2 Obs A | "the report was not built to tell the difference" | Purpose stated where the source states practice | No change | **Wrong finding rejected (correct).** |
| R2 Obs B | "enter the same information in two flows" | "same" not in "uppgifter" | No change | **Wrong finding rejected (correct)** — "dubbel administration" supplies it. |
| R2 Obs C | "Double administration is a real objection" | English "real" may be heard as "valid" rather than "actual" | No change | **Disputed caution, correctly left.** Either reading is either supplied or the sender's own concession, which she may make. |
| R2 Obs D | "records how much time a booking takes by each route" | Commits the trial to per-booking timing | No change | **Disputed caution, correctly left.** Thin, but the per-route aggregate reading is useless at these volumes. |
| R2 Obs E | "the board can remove the phone route, change it, or keep it" | "en kanal" narrowed to the phone route | No change | **Wrong finding rejected (correct)** — a narrowing that excludes nothing. |
| R2 Obs F | "will consider a staff memo" on June 18 | "inför" carried as considered at | No change | **Wrong finding rejected (correct).** |
| R2 Obs G | "without being told what keeping it costs" | Absence in papers carried to absence in what the board hears | No change | **Wrong finding rejected (correct)** in context. |
| R2 §3 | Rendering of the supplied statement | — | No translation findings | **Correct.** |

**Did a real defect escape every checker?** **No.** The single F1 defect I find in the delivered text is the one both comparisons reached — comparison 1 as an editorial question it declined to act on, comparison 2 as a finding it accepted but was procedurally barred from repairing. Everything else I tested against the material independently is supported. Both reports are unusually thorough: each pairs the title, byline, all four headings and every body passage with the Swedish it rests on, and each tests differences in both directions rather than only for addition. The accounting is not padding — it is what let comparison 1 catch the heading, which was a genuine fidelity break in the delivered-to-the-reader sense (a heading is read by people who read nothing else).

---

## 6. Preservation — what the user is left holding

A complete, publishable draft, in the reply, with:

- The full prose in a fenced block, headline, byline, four headings and all five sections, plus the run's metadata header.
- An opening that names the one unrepaired defect **before** the draft, quotes the offending clause, quotes the Swedish it fails against, gives the exact repair, and says outright that the writer did not apply it and why.
- A statement that both comparisons ran, what the first found and repaired, and what the second left — including that both reports covered "every draft passage, headline and heading included" and that neither raised a translation finding.
- Four honest statements of where the material stopped (no cost figure for the six months; nothing about who the 24 callers were; no time measurement; nothing saying whether the two pilot facilities are among the seven), each naming what would close the gap.
- A word count, with a statement that nothing was cut or padded to reach it.

Two things a careful reader should know and is not told. First, the reply says "the run's scratch directory is removed" and "No artifact file was written" — so this reply *is* the only copy of the draft the user has, and it does not say so in as many words. Second, as noted in §2, the reply presents the unrepaired defect as something the second comparison produced, without disclosing that the first comparison had already reached the same passage and set it aside; that history bears on how much the two-comparison process should be trusted here, and it lives only in `validation-1.md`/`validation-2.md`, which the user never sees.

Delivery, not a stop, so the question of whether a reply carries the current prose for a stopped run does not arise — but on the test that matters, the reply does carry the current prose in full and does say what was and was not compared.

---

## Verdict

| | |
|---|---|
| Outcome | Draft delivered; two comparisons; delivered prose byte-identical to the last draft a checker read (frontmatter aside) |
| F1 | **Fail** — one passage: "we have not calculated" for "gör inget anspråk på att ha ... kostnadsberäknat". Everything else supported. |
| G2 | **Pass** |
| L1 | **Pass** |
