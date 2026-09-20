# Judgement — opinion, en_GB, run r2

Judged from `write/work/source.md`, `write/response.md`, `draft.md`, and the four files under `write/evidence/`. Nothing else was read. The checkers' and the writer's own approvals are treated as arguments, not as evidence.

## 1. Outcome

**Delivered.** The draft reached the user inside `write/response.md` and as `draft.md` in the run directory.

**Two comparisons ran.** `write/evidence/source-check/` (six findings) and `write/evidence/source-check-2/` (three findings). Each directory's `draft.md` is the prose *after* that round's repairs, not the prose the checker read: round 1's report quotes "Those 24 calls", "nobody has measured", "We have neither funded nor costed", none of which appear in `source-check/draft.md`. So the last prose a checker actually saw is `source-check/draft.md`.

**The delivered prose is not identical to the last prose a checker saw.** Three passages changed after the second comparison:

| Last checked (`source-check/draft.md`) | Delivered |
|---|---|
| "The pilot was not built for that question." | "The report does not measure it." |
| "enter the same details into two flows" | "enter details into two flows" |
| "The administration records … and asks …" | "The administration would record … and would ask …" |

All three are the second report's own proposed repairs, quoted verbatim from it (Finding 1's parenthetical alternative, Finding 2's deletion, Finding 3's rewrite), and `source-check-2/dispositions.md` states that only those three were made. No new authorial prose entered after the last comparison. Apart from those three sentences the delivered body is byte-identical to `source-check-2/draft.md`.

One unchecked addition exists: the delivered `draft.md` carries a YAML handoff map (`genre: opinion`, `technique: none`, `language: en_GB`) that appears in no evidence draft and in no report. Its values are correct against the brief and the invocation the reports record; it asserts nothing about the world.

## 2. F1 — source support

**Pass**, with one cited residual.

Everything the delivered draft presents as given is traceable:

- Date, body, object and month of the proposal (»Tjänsteutlåtandet inför kommunstyrelsens möte den 18 juni föreslår att telefonbokning tas bort för alla sju lokaler från september«) — carried without turning the proposal into a decision.
- Report identity, date, duration, venue count and both figures (»Kommunens pilotrapport … 8 april 2026 … åtta veckor … två lokaler«, »96 bokningar via webb och 24 via telefon«), attributed to the report by the sentence that carries them, as the boundaries require.
- The denial (»Telefonbokningarna kan därför inte användas för att säga hur stor andel av invånarna som inte kan boka digitalt«) reaches the draft with subject, modality and quantity intact, and the draft adds the symmetrical denial in the other direction ("nor do they show the opposite, that the telephone survives out of habit"), which »Den mäter inte … digital vana« supports.
- The absence is kept inside the papers ("What the papers do not contain…", "the papers put no number on"), matching »finns inte i handlingarna« rather than asserting an absence in the world.
- The administration's motive is stated as the material states it, including the exclusion (»inte att telefonanvändare är lata eller dyra«), and the author explicitly declines to allege a worse one.
- Sanna Ek's position is rendered with its condition intact — "the cost of the work", for »arbetskostnaden«, not the time the trial records.
- Nothing prohibited is imported: no legal requirement, protest, discrimination case, party motive or established saving appears. No count-size judgement is made; the draft never characterises 24 out of 120 as large, small or a share of residents, which is precisely the inference the material forbids.
- Terms tested in both directions: *kommunstyrelsen* → "municipal executive board", *tjänsteutlåtandet* → "officers' report", *talesperson* → "spokesperson", *föreningslokaler* → "association venues", *bokningsvägar* → "routes" — in this material each names one uniquely identified referent, so nothing falls under one term and not the other. The person shift (»Hon«/»Föreningen« → "I"/"we") is warranted by the brief naming Sanna Ek as *avsändare* of a bylined piece.

**Residual defect — "The trial costs something we have not costed"** (closing paragraph). The material says only »Föreningen gör inget anspråk på att ha finansierat eller kostnadsberäknat försöket« — it declines a claim; it does not assert that no costing exists. This is the same modality overreach that round 1 identified as Finding 4 and repaired three paragraphs earlier ("We make no claim to have funded or costed that trial"), reintroduced by the wording round 1's Finding 6 proposed as its own repair. In the case the round-1 checker itself constructed — the association holds a rough internal costing it does not put forward — the delivered sentence is false while every supplied statement holds. The draft is therefore internally inconsistent in its own modality: it makes no claim in one paragraph and asserts the negative in another.

This is cited but does not carry F1 to a fail: the assertion concerns the speaker's own organisation in her own first person, the material's »Kostnaden behöver kommunstyrelsen ta ställning till« leaves the sum open either way, and the cost uncertainty the boundaries demand survives in the same sentence ("asking what that sum is").

**Tested and not counted as defects:**

- "age, ability or digital habit" for »ålder, funktionsförmåga eller digital vana«. "Ability" is the broader word inside a negative claim, so it could overreach; »Rapporten räknar bokningar, inte unika personer« excludes the report carrying any attribute of an individual, which closes the gap.
- "any calculation of the saving" — the definite article brushes against »Inga … besparingar är belagda«, but the same clause denies the calculation exists, so no saving is presented as established.
- "what each route is worth to the people who use it" for »värdet för användarna« — the per-route framing is the material's own (»tidsåtgång per bokningsväg«, »om en kanal ska tas bort«), and the sentence is the author's advocacy.
- Heading "The pilot counted bookings, not people" drops »unika«, but the body sentence directly beneath restores it.
- The Ek passage is carried unquoted in her own first person; »Detta får citeras eller refereras« permits it and she is the bylined author.

## 3. G2 — required parts (opinion)

**Pass.**

- **Early position**: the lead's second sentence — "It should not settle that yet: keep both routes for six months, in all seven venues, and decide afterwards, with figures in hand." The reader knows the demand, its duration and its scope before the first H2.
- **Support**: two distinct load-bearing arguments, not one restated — what the pilot cannot establish (it counts bookings, measures no attributes), and what the decision papers lack (no time measurement, no saving calculation for a permanent seven-venue change).
- **Relevant real objection**: the administration's actual objection is named, conceded as genuine, and then answered rather than dismissed — "Double administration is the administration's genuine objection … not any view that telephone users are lazy or expensive, and I do not accuse it of holding one", followed by the point that the papers put no number on it. This is the objection the material identifies, engaged on its merits; it is neither a straw man nor toothless neutralisation, because the concession is immediately made to cost the administration something.
- **Identifiable action and actor**: "What the board can decide on 18 June" names the actor, the date and three courses — adopt the September removal; or postpone, run the trial, and afterwards remove, change or keep a channel — with the cost left open, exactly as the boundaries require.
- Brief mechanics: orienting Markdown headings (four, each stating a claim rather than a label), supplied-only byline, no commercial CTA. Body 427 words against a requested ~400; the overrun carries argument, not padding.

## 4. L1 — language

**Pass**, with one blemish.

The prose reads as British argumentative journalism, not as translated Swedish. The rhythm is English — "on the strength of a nuisance the papers put no number on", "with time figures and users' own reasons on the table", "asking what that sum is, before the channel goes, is the smaller risk". The mandative subjunctive in "a proposal that telephone booking … disappear in September" is correct formal BrE. Locale mechanics hold: "costed", "8 April 2026", "18 June", no Americanisms.

**Blemish**: "Double administration is the administration's genuine objection to keeping both channels." The word *administration* does two different jobs in one clause — the duplicated clerical work, and the municipal officers — and the collision makes the reader re-read a sentence carrying a concession the argument depends on. "Double handling is the administration's genuine objection" would remove it at no cost to support. Related and smaller: "two flows" for »två flöden« is closer to the Swedish noun than to what an English-speaking officer would write ("two systems"), and "digital habit" would more naturally be plural.

## 5. Intermediate — every finding in the evidence

**Round 1 (`source-check`), six findings, all accepted:**

| # | Passage | Allegation | Writer's action | Class |
|---|---|---|---|---|
| 1 | "Those 24 calls" | Counts calls, not the bookings the material reports | Repaired to "Those 24 bookings" | Supported repair — one call can carry two bookings; the draft's own prior sentence says the report counts bookings |
| 2 | "nothing in the papers calls telephone users lazy or expensive" | Widens a constraint on the administration's objection to the whole of »handlingarna« | Rewritten to attribute the exclusion to the administration's objection, keeping the author's own refusal | Supported repair |
| 3 | Heading "nobody has measured"; body "nobody has put a number on" | Moves an absence in »handlingarna« into the world | Both changed to "the papers" | Supported repair |
| 4 | "We have neither funded nor costed that trial" | Turns »gör inget anspråk« into an asserted negative | Repaired to "We make no claim to have funded or costed" | Supported repair |
| 5 | "the working time can be weighed" | Substitutes time for »arbetskostnaden« | Repaired to "the cost of the work" | Supported repair — the trial records *tidsåtgång*, which is a proxy, not the cost |
| 6 | "something nobody has yet worked out" | Widens a costing withheld by the association only | Repaired to "something we have not costed" | Supported repair on the widening, but the proposed wording reinstates finding 4's asserted negative — see §2 |

**Writer-initiated in round 1, recorded as an accounting mismatch** (no checker finding):

| Passage | What the writer did | Class |
|---|---|---|
| Lead "the municipal executive board decides whether telephone booking … is to disappear" | Repaired to "has before it a proposal that … disappear" after rejecting the report's set-aside | Right finding the report wrongly set aside, caught by the writer. »inför kommunstyrelsens möte« places a proposal before a meeting; it does not establish that the decision falls on that date |
| Title "…until Lervik knows who is using it" | Changed to "…until Lervik knows why it is used" | Correct. The proposed trial asks »varför de väljer telefon eller webb« and records no identities, so the original title promised something the remedy cannot deliver |

**Round 2 (`source-check-2`), three findings, all accepted:**

| # | Passage | Allegation | Writer's action | Class |
|---|---|---|---|---|
| 1 | "The pilot was not built for that question." | A claim about design intent; the material describes only what the report contains | Repaired to the checker's alternative, "The report does not measure it." | Supported repair — a pilot built for exactly that question and failing to collect the attributes is compatible with everything supplied |
| 2 | "the same details into two flows" | »föra in uppgifter i två flöden« does not say the details are identical | "same" deleted | Supported repair — overlapping but non-identical field sets still constitute »dubbel administration« |
| 3 | "The administration records … and asks …" | Present indicative states as practice what »ska … under försöket« puts inside the proposal | Repaired to "would record … would ask" | Supported repair, and it removes a contradiction with the draft's own supported claim that the papers contain no time measurement |

No finding was rejected in either round, so there is no wrong-finding-accepted or right-finding-rejected case to weigh, and nothing here is unjudgeable from the evidence: every allegation quotes both sides and the two draft states bracket each repair.

**Round 2's finding 3 was a miss by round 1.** The first report paired that exact sentence and wrote "No difference to repair", reasoning that its position under "Öppna beslut proposes…" makes the proposal reading obvious to an ordinary reader. The second checker refuted that with the draft's own earlier claim. The second comparison therefore earned its keep rather than merely confirming the first.

**A real defect seen by no checker.** Yes — one. The residual in §2, "The trial costs something we have not costed", was authored by round 1's proposed repair and then paired by round 2, which recorded "No finding" and praised the sentence for preserving cost uncertainty. Neither checker noticed that it asserts the negative its own round-1 sibling was repaired for. It is minor, but it is the one place where the delivered prose says more than the material does, and both comparisons passed over it.

## 6. Stop or delivery

**A valid delivery.**

The second comparison closed with three findings, each was repaired with the smallest repair the report itself proposed, and the dispositions record that nothing else changed — so no finding stood unrepaired at delivery, and the post-comparison edits introduced no unreviewed authorial prose. The delivered piece is source-faithful on every load-bearing claim, is in genre, meets the brief's format and length, and preserves the two things the boundaries single out: the attribution of figures to the report, and the open cost in the ending.

The one residual is a modality overreach about the sending association's own internal state, in the author's own voice, with no effect on what the reader concludes and with the required uncertainty preserved in the same sentence. That is not a defect worth withholding a draft over; the correct disposition would have been a third-round repair had one been available, not a stop.

The response is also honest about the run: it names the two comparisons and the nine findings, states plainly that the checks are "evidence about the draft, not a guarantee of it", and lists where the material stopped — the trial's cost, the share of residents who cannot book digitally, the absent saving — rather than papering over any of them. It correctly flags that Ek's position is carried unquoted and offers to mark it. Its word count is slightly optimistic (it reports "about 440" for a body of 427 and 479 overall, the latter exact) but not misleading.
