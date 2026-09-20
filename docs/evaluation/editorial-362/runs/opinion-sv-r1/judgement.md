# Judgement — opinion-sv-r1

Judged from `write/work/source.md`, `draft.md`, `write/response.md` and the four files under `write/evidence/`. The checkers' and the writer's own approvals are treated as arguments, not as evidence; every pairing below was re-derived from the source.

## 1. Outcome

**Delivered.** Two comparisons ran (`report.md`, `report-2.md`), each followed by a validation/disposition file (`dispositions.md`, `dispositions-2.md`).

**Delivered prose is identical to the last prose a checker saw.** `write/evidence/draft-2.md` and the body of `draft.md` are byte-identical apart from one blank line after the frontmatter; the only addition is the `kntnt` handoff map, which is metadata, not prose. `dispositions-2.md` records a rejection with no prose change following from it, and the diff confirms no post-comparison repair was made.

One evidence-integrity note: `write/evidence/draft.md` is byte-identical to `draft-2.md`, i.e. it is the **post-repair** draft, not the draft the first checker read. The pre-repair first draft is not retained anywhere in the run. Round one is therefore judgeable only through the passages `report.md` quotes (it cites "Rapporten räknar bokningar, inte personer" at l. 9 and "Vi har varken kostnadsberäknat eller finansierat försöket. Det påstår vi inte heller." at l. 23, neither of which exists in any retained file). Those quotations are internally consistent and match the repairs described, so the round is judgeable, but the stored `draft.md` misrepresents what round one compared.

## 2. F1 — source support: **PASS**

Every assertion in the delivered draft traces to the supplied material, and every caveat the material carries survives into the text. Checked item by item:

| Delivered passage | Source | Verdict |
|---|---|---|
| "Den 18 juni ska kommunstyrelsen ta ställning till att telefonbokningen … tas bort från september." | "Tjänsteutlåtandet inför kommunstyrelsens möte den 18 juni föreslår att telefonbokning tas bort för alla sju lokaler från september." | Date, body, object, month match. "ska ta ställning till" is the modality of an item before a meeting, not a settled removal, and the close names three open outcomes. Supported. |
| "pilotrapport … daterad den 8 april 2026 … åtta veckor … två lokaler" | Verbatim but for "daterad" | Supported. |
| "96 bokningar via webben och 24 via telefon" | Verbatim | Supported. |
| "Rapporten räknar bokningar, inte unika personer." | Verbatim | Supported (repaired in round one). |
| "Den mäter varken ålder, funktionsförmåga eller digital vana." | "Den mäter inte ålder, funktionsförmåga eller digital vana." | Same list, same negation scope. Supported. |
| "Av de 24 telefonbokningarna går det därför inte att utläsa hur stor andel av invånarna som inte kan boka digitalt." | "Telefonbokningarna kan därför inte användas för att säga hur stor andel av invånarna som inte kan boka digitalt." | Same impossibility, same population, same inferential marker. The central caveat is preserved, not softened. Supported. |
| "Siffrorna visar att telefonen används — inte av vem, och inte varför." | The two counting/measuring limits; Ek: "ett skäl att ta reda på varför telefonen fortfarande används" | A claim about what the figures show, not about what anyone knows. Supported. |
| "Motivet är att personalen ska slippa föra in uppgifter i två flöden." | "Motivet i utlåtandet är …" | Attribution held by the preceding subject "Tjänsteutlåtandet". Supported. |
| "Men i handlingarna finns varken en tidsmätning eller en beräkning av vad kommunen sparar." | "Någon tidsmätning eller ekonomisk besparingsberäkning finns inte i handlingarna." | Location scope "i handlingarna" carried intact. Supported. |
| "Kommunstyrelsen ska alltså ta bort en kanal utan att veta vad kanalen kostar." | As above | Marked "alltså" as inference from the sentence before it; the knowledge attributed is what the handlingar carry. Supported. |
| "Vi föreslår ett sex månader långt försök i alla sju lokaler, med både telefon och webb kvar." | "Öppna beslut föreslår ett sex månader långt försök i alla sju lokaler, med båda bokningsvägarna kvar." | "Vi" is licensed by the byline. Supported. |
| "Att en bokning går via telefon är inte ett bevis … varför telefonen fortfarande används." | Ek's supplied stance, character for character | Reproduced verbatim, unmarked because the byline is Ek's own; the material licenses quoting or referring. Nothing narrowed, widened, hedged or de-hedged. Supported. |
| "Vi gör inget anspråk på att ha kostnadsberäknat eller finansierat försöket." | "Föreningen gör inget anspråk på att ha finansierat eller kostnadsberäknat försöket." | Order of the two items reversed; disclaimer strength identical. Supported (repaired in round one). |
| "Vad ett halvår med två kanaler kostar är något kommunstyrelsen behöver ta ställning till." | "Kostnaden behöver kommunstyrelsen ta ställning till." | Cost uncertainty preserved, as the boundary requires. Supported. |
| "Jag motsätter mig inte digital bokning." | "Hon motsätter sig inte digital bokning." | Person shift licensed by the byline; the draft drops a gender feature rather than adding one, and asserts the same stance. Supported. |
| "Men innan en väg in stängs måste kommunen kunna väga arbetskostnaden mot värdet för användarna" | "Hon menar att kommunen först måste kunna väga arbetskostnaden mot värdet för användarna." | Same two quantities, same necessity, and the source's attribution to her is carried by the byline. Supported. |
| "och det underlaget finns inte i dag." | As above, plus the report's stated measurement gaps | See §4; supported in Ek's own voice, because the source's "först måste kunna väga" is itself her claim that the weighing cannot be made now. |
| "bifalla tjänsteutlåtandet, avslå det eller skjuta upp bytet och besluta om ett halvårsförsök" | Boundary: "Slutet ska namnge kommunstyrelsens möjliga beslut" | Modality "kan"; no outcome asserted. Supported. |
| "Då har styrelsen tidsåtgången per bokningsväg och användarnas egna skäl framför sig när den avgör om en kanal ska tas bort, ändras eller behållas." | "Under försöket ska förvaltningen registrera tidsåtgång … Därefter kan den avgöra om en kanal ska tas bort, ändras eller behållas." | Three dispositions verbatim; conditional on the trial, which "Då" makes explicit. Supported. |
| "*Sanna Ek, talesperson för föreningen Öppna beslut*" | Brief | Supplied byline only. Supported. |

**Nothing invented.** No law, protest, discrimination case, party-political motive, established saving, named official, anecdote or personal attribute appears anywhere — the five the boundaries forbid are all absent. No unnamed authority ("studier visar", "experter") is introduced. No causal claim is made; the draft explicitly refuses one twice.

**Unknown kept apart from absent.** The load-bearing epistemic caveats all survive as caveats: the report counts bookings not unique persons; it does not measure age, ability or digital habit; the phone bookings cannot yield a share of residents; the association makes no claim to have costed or funded the trial; the cost is for the committee to decide. None is converted into a claim that the thing is known, and none is dropped.

**Terms checked in both directions.** "beräkning av vad kommunen sparar" ↔ "ekonomisk besparingsberäkning": in this context neither is wider — both pick out a savings calculation in the decision documents. "samtliga sju" ↔ "alla sju": identical. "ett halvår" ↔ "sex månader": identical. "både telefon och webb" ↔ "båda bokningsvägarna": the source itself names the two routes as telefon/webb ("varför de väljer telefon eller webb"), so nothing falls under one and not the other here. "beslutsunderlaget"/"handlingarna": the draft uses the narrower, document-scoped term in the heading and at the sentence that carries the absence.

Two borderline items I record rather than count as failures:

- **"I försöket gjordes fyra av fem bokningar på webben."** This is a derived proportion, not a supplied one: 96/(96+24) = exactly 4/5, and the derivation requires the pilot to have had no third route. The material treats the channels as exactly two ("båda bokningsvägarna", "båda kanalerna", "telefon eller webb"), the ratio is stated of *bookings* rather than people, and no evaluative size word is attached to it, so the count-size requirement is met by a supplied comparison. Supported, but it is the one number in the text the source does not state.
- **"Den invändningen är verklig: dubbel administration är arbete."** Both checkers cleared this on the ground that "the source itself calls the objection 'verklig'". That reasoning is wrong: the source's "Förvaltningens verkliga invändning … är dubbel administration, inte att telefonanvändare är lata eller dyra" *identifies* which objection is the actual one, it does not pronounce it valid. The draft's sentence nonetheless stays inside the material, because it is the author's own concession and the added clause ("dubbel administration är arbete") asserts nothing about Lervik that the material contradicts, while the boundary expressly forbids imputing a false motive. Supported on a different ground than either checker gave.

## 3. G2 and L1 on the delivered draft

**G2 (opinion): PASS.** All four required jobs are done by distinct parts.

- *Early position*: taken by the end of the lead — the title states the thesis and sentences two and three of the lead name the actor and the ask ("Föreningen Öppna beslut anser att beslutet bör vänta. Pröva i stället både telefon och webb i ett halvår, i alla sju lokaler").
- *Support*: two sections of it, and they do different work — one on what the report's figures cannot carry, one on what the decision basis lacks. Neither repeats the other.
- *A relevant real objection*: present and genuinely the opponent's strongest, not a straw man. "Den invändningen är verklig: dubbel administration är arbete" concedes the administration's actual stated motive, and the close concedes the majority case for the other side outright ("I försöket gjordes fyra av fem bokningar på webben", "Jag motsätter mig inte digital bokning"). The reader meets the case against the author's own position before being asked to act.
- *Identifiable action and actor*: the kommunstyrelse, on 18 June, with its three options spelled out and the requested one named ("Vi ber om det sista"). No commercial CTA, as the brief requires.

The closing paragraph also carries the required cost uncertainty forward rather than quietly resolving it. Reader effect: someone in Lervik finishes knowing who decides, when, what the three choices are, and what the author wants — which is what an opinion piece owes.

**L1 (Swedish): PASS.** The prose reads as written in Swedish, not translated into it. Compound and adjectival constructions are native ("ett åtta veckor långt försök", "ett sex månader långt försök", "tidsåtgången per bokningsväg", "Öppna besluts förslag"); the genitive of the association's name is formed correctly. The cleft at "Det är underlaget som är för tunt, inte avsikten bakom det" and the elliptical "Siffrorna visar att telefonen används — inte av vem, och inte varför" are both idiomatic Swedish rhetorical moves rather than calques. No anglicism, no English word order, no generic translated register. Headings orient in ordinary Swedish, as the brief asks.

One small idiom wobble, not enough to fail: **"ta ställning till att telefonbokningen … tas bort"** in the lead. Native usage takes a position *on whether* something should happen — "ta ställning till om telefonbokningen ska tas bort" or "till förslaget att ta bort telefonbokningen". The "till att" + clause construction reads slightly stiff at the very first sentence, where it is most visible. Everything after it is clean.

## 4. Intermediate — every checker finding

| # | Passage | Allegation | What the writer did | Class |
|---|---|---|---|---|
| R1-F1 | "Vi har varken kostnadsberäknat eller finansierat försöket. Det påstår vi inte heller." | Source says the association *makes no claim* to have costed or funded it; the draft turned an absence of claim into a claim of absence | Accepted; replaced both sentences with "Vi gör inget anspråk på att ha kostnadsberäknat eller finansierat försöket." | **Supported repair.** The finding is right and the repair is exactly the source's own assertion, no wider and no narrower. |
| R1-F2 | "Rapporten räknar bokningar, inte personer." | The qualifier "unika" was dropped, widening the negation from *distinct individuals* to *persons at all* | Accepted; restored "unika" | **Supported repair.** Right, and load-bearing: the "andel av invånarna" inference three sentences later turns on repeat bookers, i.e. on uniqueness. Without the word the draft also denied something the material never says. |
| R2-F1 | "…och det underlaget finns inte i dag." | Widens an absence the material places "i handlingarna" to the present state of the world | Rejected with reasons: "det underlaget" is anaphoric to the whole weighing named in the same sentence (arbetskostnad *and* värde för användarna), so the checker's case supplies only one half and the weighing still cannot be made | **Wrong finding rejected (correct).** The rejection reaches the right outcome and its anaphora argument is sound. It missed the plainer ground: the source's own "Hon menar att kommunen **först** måste kunna väga arbetskostnaden mot värdet för användarna" is Ek asserting that the weighing cannot be made now, and the draft is signed by Ek. The clause is her view stated in her voice, which the material supplies directly. The writer also correctly noted the report's internal inconsistency — its row #12 sets aside the very case it then relies on at #28. |

Findings the writer's reply mentions with no report file: none. `write/response.md` describes exactly the two accepted and one rejected finding above, and describes them accurately.

Both reports additionally record several passages tested and cleared without becoming findings — R1 rows on "Kommunstyrelsen ska alltså ta bort en kanal…" (l. 41), the present-tense trial design (l. 49) and "det underlaget finns inte i dag" (l. 62, cleared in round one and raised as a finding in round two by the fresh checker); R2 rows #18 and #21 on the same first two. I reach the same conclusions on all of them independently.

**Did a real F1 defect escape every checker?** No. I found no unsupported assertion, changed term, changed scope, altered modality, dropped caveat or invented element in the delivered draft that no checker examined. The one thing both checkers got wrong they got wrong in the *reasoning* rather than the verdict: both cleared "Den invändningen är verklig" by misreading the source's "verkliga invändning" as an endorsement of the objection rather than an identification of it (R1 l. 39, R2 #16). The passage is still supported, for the reason given in §2, so no defect reached the reader — but the clearance was granted on a false premise, and the same misreading applied to a less innocuous sentence would have let a real defect through.

## 5. Stop or delivery

**A valid delivery.** Two comparisons ran, as the cap allows. Round one produced two genuine defects, both repaired minimally and exactly as proposed, with no collateral edits. Round two, by a fresh checker on the repaired text, produced one finding that does not stand, and the writer rejected it on its merits rather than on any checker's approval, recorded the evidence, and changed nothing — so the delivered prose is precisely the prose the second checker compared. Judged from the source myself, the delivered draft is sound under F1, does the opinion form's four distinct jobs under G2, and reads as native Swedish under L1. There was nothing left that should have stopped it.

The response's own accounting is also truthful: it reports two rounds, two repairs and one reasoned rejection, and its word count ("drygt 420 ord") matches the delivered text at 422 words.
