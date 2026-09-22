# Judgement — case-study-sv-r1

Judged from `work/source.md`, `response.md`, `delivered.md` and everything under `evidence/`. No other file was read. Checker approvals and the writer's own dispositions are weighed as argument, never as evidence; every verdict below is taken from the material myself.

---

## 1. Outcome

**Delivered.** The reply hands over the full text and says so in its first line, while declaring one known unrepaired defect.

**Two comparisons ran.** `evidence/source-check/` holds draft-1 with `report-1.md` (six source-support findings, no translation findings) and draft-2 with `report-2.md` (one source-support finding, S1, no translation findings). Both were full comparisons by a fresh checker against the whole material.

**Delivered prose is identical to the last prose a checker saw.** `diff draft-2.md delivered.md` returns exactly one hunk: the seven-line `kntnt` YAML frontmatter block prepended at the top. Not one word of the body, the headline, the standfirst, the byline, the four headings, the three quotations or the closing paragraph differs. The reply's claim on this point is true.

Body length 399 words against a brief asking for approximately 400.

---

## 2. F1 — source fidelity

**Fail.** One defect is decisive; a second is cited and is a defect the checkers were instructed not to look at; the rest are recorded as examined-and-cleared so the judgement is visible rather than silent.

### 2.1 Decisive: the median heading drops the measured interval

> `## Mediantiden var lägre under testet – orsaken är öppen`

Material: "Median time **from report to assignment** was two working days during the trial and three in the preceding eight-week period." And: "There are no cost, resident-satisfaction or **completion-time** measurements." And, in the judging note: "Do not turn assignment time into completion time."

The material measures exactly one interval. The heading says *Mediantiden* — definite, unqualified, and the draft's first mention of any median, so the definite article has no antecedent in the text to attach itself to. Read as a heading is read, standing alone in a feed or under a scanning eye, it says the median time of the repair process was lower during the trial.

A concrete case compatible with the material, in which the sourced statement holds and the draft's fails: during the trial the team assigned jobs faster but, on a heavier or differently composed workload, took longer to finish them — median completion time rose from six working days to nine. Report-to-assignment still fell from three to two, so the material's sentence is true in that case; *mediantiden var lägre under testet* is false in it. The converse case stands too, so neither statement entails the other. No supplied statement rules the case out: the nearest candidate, the absence of completion-time measurements, does the opposite — it establishes that the material cannot know, which is precisely why the qualifier had to survive.

The base contract in `evidence/source-check/context.md` settles this rather than leaving it to taste: "This boundary holds in the title, summary, headings and body alike. Preserve chronology, scope and qualifications wherever a claim appears." A scope qualifier is dropped in a heading, at the one place the material's own judging note names as the drift to avoid. This is an F1 failure.

The body beneath it is clean — `Tiden från anmälan till tilldelning var i median två arbetsdagar under testet och tre under de åtta veckorna dessförinnan` carries the interval, the statistic, both figures, the unit by the same ellipsis the source uses, and both periods. The failure is the heading alone, and the repair was four words.

### 2.2 A named author where the material says there is none

> `Av Thomas Barregren`

The brief states: "No author name supplied." The draft supplies one, a named human being, as the byline of a piece the material says carries no author name. An attribution is a claim, and this one is outside the supplied material.

Both checkers were told to exempt it — report-1's scope note ("The byline `Av Thomas Barregren` comes from the invocation, not the material, and is not assessed") and report-2's opening line say so in nearly identical words — so neither is at fault for missing it. The reply discloses the mechanism and warns that the line must be changed before publication. That is honest and mitigates, but the delivered text still asserts an authorship the material denies having. I record it as a defect of the delivered artefact and as a configuration question rather than a writing failure, and I do not rest the F1 verdict on it.

### 2.3 Cited, minor: the checklist given an owner the brief withholds

> `Svale Systems implementeringschecklista är ett dokument att läsa igenom: https://example.invalid/svale/checklist`

The brief says only "the supplied implementation checklist at https://example.invalid/svale/checklist". It never says whose checklist it is. The draft attributes authorship to Svale Systems. The inference is well grounded — supplier-published material pointing at a `/svale/` path — but it is an inference the brief does not make, and `Implementeringschecklistan är ett dokument att läsa igenom` would have cost nothing. Report-2 raised it as editorial question E1 and filed no finding; report-1 did not reach it. A small addition, correctly kept out of the decisive verdict.

The rest of that sentence is exactly right: a document to read, neither a consultation booking nor a product trial, with the URL matching character for character, and the reader address `Planerar du ett liknande test?` presupposing nothing beyond the brief's audience.

### 2.4 Examined and cleared

- **`Hösten 2025` for "In September 2025"** — the material dates the decision, not the trial. An eight-week trial decided in September and reported on in a note of 4 December 2025 cannot fall outside autumn 2025. Entailed, not added.
- **`i två av husen`** for "in two buildings" — the partitive presupposes more than two exist, which "before the next building starts" and the unexpanded trial both carry.
- **`Hos Elm Quay Housing … lagrades telefonanmälningar och mejl var för sig`** — the material says the reports were stored separately and not by whom. The locative is now the company rather than, as in draft-1, the maintenance team; these are the customer's own reports, so the company is the only reading available. Cleared, with a trace of residue. "Previously" survives through the past tense plus the following sentence's date rather than through a word of its own; reading order leaves the prior state unambiguous.
- **`ett bostadsföretag med 640 lägenheter`** — *med* is looser than *förvaltar* and a company can hold flats it does not manage. The standfirst four lines above states `förvaltar 640 lägenheter`, fixing the relation before the appositive compresses it. Defensible.
- **`Syftet var att personal på olika skift skulle se samma information`** — a want of the team rendered as the purpose of the trial, immediately after the team's own decision, with no other party's aim in view. Cleared.
- **`Någon jämförelse med en annan leverantör finns inte att tillgå`** — availability preserved against "is available", which is the distinction draft-1 lost. Note that the draft mirrors the material's two different phrasings distinctly: availability here, flat absence at `mättes inte` for "There are no … measurements". That is a genuinely careful reading.
- **`de boende kunde fortsätta anmäla fel per telefon`** — the material gives the team an act ("kept telephone reporting open for residents"); the draft gives the residents a resulting state. A faint loss of the customer's agency in a piece whose brief requires the customer to act, but the state is what the act consists in, and no agency is transferred to the supplier. Cleared.
- **`orsaken är öppen`** — the material supplies a confound (differing workloads) and a refusal by the note to attribute the difference to the software. *Öppen* denies that a cause has been settled rather than proposing one, and no cause is established anywhere in the material. In a supplier-published case the pairing with a lower median does leave software causation alive in the reader's mind, but that is an editorial nuance and not a claim the draft makes. Cleared.
- **`Maya Lind rekommenderar inte Svale till alla bostadsföretag`** — past ("did not recommend", of the interview) becomes a standing present. A small tense lift; the material presents her position rather than a one-off event, and the negation scopes over the universal in Swedish as in English — not a recommendation *against* Svale. This is also where draft-1's real widening (any recommendation at all, with Svale dropped) was repaired. Cleared.
- **`Beslutet om fler hus dröjer`** — *dröjer* carries "still to come"; "has not yet expanded" plus a stated precondition supports it, and no deadline is supplied against which lateness could be asserted. Cleared, at the edge.
- **`Teamet vill först se hur kategorierna fungerar för större reparationer`** — a stated plan rendered as a wish, with object, scope and position before the decision all preserved.
- **`Den här kundberättelsen är publicerad av Svale Systems och är inte oberoende journalistik`** — both halves stated in the material, publisher named rather than left to the reader.
- **No forbidden inference anywhere.** The software is never said to have shortened anything, hedged or flat; assignment time never becomes completion time in the body; the reservation survives; the supplier is never *vi* outside a quotation, where every *vi* is Lind's.

---

## 3. G2 — required parts, distinct jobs

**Pass, with one real weakness.**

All parts are present and in order: headline (`# Elm Quay testade gemensam logg i två hus`), standfirst (the paragraph beneath it), byline (`Av Thomas Barregren`), lead (`Hos Elm Quay Housing … lagrades telefonanmälningar och mejl var för sig`), four sections, and an ending.

The customer-account jobs are all done and are done by the right party:

- **Situation** — telephone reports and emails stored separately; staff on different shifts unable to see the same information.
- **Action** — the team decided to trial, tested whether the log could show status, chose Svale, designed its own categories, kept telephone reporting open.
- **Results** — 31 reports with their exclusions, two working days against three, and an explicit list of what was not measured.
- **Appraisal** — `Maya Lind rekommenderar inte Svale till alla bostadsföretag` followed by her qualified final quotation.
- **Publisher stance** — truthful and in the draft's own voice: published by Svale Systems, not independent journalism.
- **Customer as acting party** — Elm Quay or its team is the grammatical subject of every act reported. Svale configures and trains, and nothing else.
- **Call to action** — built from the one supplied link, described as the brief describes it.

**The weakness: the standfirst and the lead overlap heavily.** Standfirst sentence 1, `Elm Quay Housing förvaltar 640 lägenheter`, and lead clause `ett bostadsföretag med 640 lägenheter` give the reader the same number twice in four lines. Worse, standfirst sentence 2 —

> Hösten 2025 testade underhållsteamet en gemensam logg för felanmälningar i två av husen.

— and lead sentence 2 —

> I september 2025 bestämde underhållsteamet sig för att testa en gemensam logg för felanmälningar i två av husen.

— differ only in the date form and in *bestämde sig för att*. Nine words run verbatim. Two of the standfirst's three sentences are consumed by the lead, leaving only the roadmap sentence doing work the lead does not. In a 399-word piece that is a measurable share of the budget spent saying one thing twice, and the reader feels it as a stall on the way in. The parts still hold distinct jobs — the standfirst promises three things the lead does not, the lead supplies the prior state and the purpose the standfirst does not — so this is a craft failure inside a passing structure, not a missing job.

The ending carries reader address, next step and publisher stance in one paragraph; it closes the piece rather than merely stopping.

---

## 4. L1 — professional Swedish

**Pass**, and comfortably.

The structural tells of English-into-Swedish are absent. V2 holds under every fronting: `I september 2025 bestämde underhållsteamet sig`, with the reflexive correctly behind the subject; `Hösten 2025 testade underhållsteamet`; `Efter den prövningen valde teamet Svale Systems`. The topicalised object in `Kategorierna i loggen tog underhållsteamet fram själv` splits the particle verb the way a Swedish writer does and an English draft never would. The s-passive is used where Swedish uses it (`lagrades`, `mättes inte`, `räknas inte in`) rather than a *bli*-construction.

Compounds are solid throughout: *kvällsskiftet*, *morgonskiftet*, *underhållsteamet*, *felanmälningar*, *arbetsbelastning*, *implementeringschecklista*, *testnotering*. Double definiteness is marked where it is required: *de åtta veckorna*, *de första anmälningarna*, *den interna testnoteringen*. Genitives are right in both hard cases: *Elm Quays* on a name not ending in a sibilant, and nothing at all on *Svale Systems implementeringschecklista*. Reported speech takes the speech dash rather than quotation marks. *Du* addresses the reader; *man* appears nowhere, which is where a translated draft's *you* and passives usually land.

Vocabulary sits where a Swedish professional reader expects it: *felanmälan*, *akuta ärenden*, *arbetsledare*, *avsätta*, *dessförinnan*, *drar i gång*. The headings are compact in the Swedish manner rather than the English (`Svale konfigurerade, teamet bestämde indelningen`).

Two small marks, neither enough to fail:

- `Här är vad teamet valde, vad den interna testnoteringen visar och …` reads as a calque of "Here's what". It has become common in Swedish journalism, but it is the one place in the text where the English shows through.
- `var i median två arbetsdagar` is stiff where `medianen var två arbetsdagar` would run better. Correct, faintly technical.

---

## 5. Bridges into quotations

Three quotations, in order of appearance.

**Q1 (line 26).**
Bridge, the narrative clause immediately before it: **"Testet pågick i åtta veckor."**
Quotation: **"— Vi ville att kvällsskiftet skulle se vad morgonskiftet redan hade gjort. Kategorierna var våra – Svale hjälpte oss att lägga in dem i loggen, skriver Maya Lind, arbetsledare för underhållet på Elm Quay Housing."**
**Class (c).** The words that put it there: *åtta veckor* — the duration is a fact the quotation does not carry and does not touch.
*This one reads two ways.* On the second reading the bridge is the whole preceding paragraph, whose first sentence is `Kategorierna i loggen tog underhållsteamet fram själv` and whose second is `Svale konfigurerade loggen`. Taken that way, the second half of the quotation — *Kategorierna var våra – Svale hjälpte oss att lägga in dem i loggen* — meets the reader as the bridge said again, which is class (a) for that half. I choose (c) because the brief defines the bridge as the sentence or clause standing **immediately** before the quotation, and that is the eight-week sentence; but the paragraph-level reading is the truer description of the reader's experience, and it is worth saying that the draft's own lead has already delivered the quotation's *other* half too, as `Syftet var att personal på olika skift skulle se samma information`. Q1 therefore adds Lind's voice and her concrete shift-handover image, but very little the reader did not already hold.
The speech tag carries the name, the role and the employer and nothing further: attribution only.

**Q2 (line 28).**
**No bridge at all.** The quotation follows Q1 directly, with no narrative sentence or clause between them. Its tag, **"skriver hon"**, is bare attribution and carries nothing besides. This is the run's strongest quotation placement in one respect — nothing pre-empts it, and the category-agreement cost it reports appears nowhere in the narration — and its weakest in another, since two stacked quotations give the reader no narrative footing between them.

**Q3 (line 40).**
Bridge: **"Teamet vill först se hur kategorierna fungerar för större reparationer, och Maya Lind rekommenderar inte Svale till alla bostadsföretag."**
Quotation: **"— Jag skulle välja att göra testet igen. Att ha en samlad bild av anmälningarna hjälper oss, men jag skulle lägga in en extra vecka för förberedelser, skriver hon."**
**Class (c).** The words that put it there: *rekommenderar inte Svale till alla bostadsföretag* — the quotation never mentions Svale, never mentions other housing companies, and never speaks to whom she would or would not recommend anything. The bridge frames the quotation as qualified, which is what the material asks, and then lets the quotation deliver a reservation of a different kind (an extra week of preparation). This is the draft's best bridge: it earns its place and leaves the quotation something to do.

**Counts.** Class (a): none; class (b): none as a lead-in sentence, though both bare tags and Q1's naming tag are attribution-only; class (c): two; quotations standing with no bridge at all: one.

**Interviewer.** No. No interviewer appears anywhere in the draft, no question is put in an interviewer's mouth, and no utterance is attributed to one. The material supplies none and the draft invents none.

**Unsupported bridge.** No. `Testet pågick i åtta veckor` rests on "The trial lasted eight weeks"; `Maya Lind rekommenderar inte Svale till alla bostadsföretag` rests on "Lind did not recommend Svale to every housing company", with only the small tense lift noted at 2.4.

---

## 6. Quoted speech

All three of the material's "complete usable quotations" are used, and **none the material offers and permits is missing from the draft.**

**Q1** — "We wanted the evening shift to see what the morning shift had already done. The categories were ours; Svale helped us put them into the log." The pluperfect survives as *redan hade gjort*; the ownership assertion survives with its emphasis intact as *Kategorierna var våra*; Svale remains the helper and is not allowed to become the doer. The semicolon becomes a speech dash, which is how Swedish sets this juxtaposition in reported speech, and the second half stays an acknowledgement rather than hardening into a concession or a contrast. Nothing additive. **Unmoved.**

**Q2** — "We spent more time agreeing on the categories than entering the first reports. I would set that time aside before the next building starts." The comparison keeps both terms and their order; *avsätta* is exactly "set aside" in the sense of reserving time; the conditional *skulle* keeps the advice conditional. Fronting *Den tiden* is Swedish V2 emphasis, not English word order. *Drar i gång* sits about one step below "starts" in register and reproduces the source's own ellipsis — a building does not literally start in either language. A preference, not a movement of meaning. **Unmoved.**

**Q3** — "I would choose to do the trial again. Having one view of the reports helps us, but I would leave an extra week for preparation." This is the quotation the material protects most explicitly ("Her final quotation is her actual, qualified assessment. It is not an inference from the figures"), and the draft keeps all three of its moves in order: the conditional endorsement, the present-tense benefit scoped to her own organisation (*hjälper oss*, not *hjälper bostadsföretag*), and the *men* that attaches the reservation to the endorsement rather than trailing it as an afterthought. *En samlad bild av anmälningarna* for "one view of the reports" was tested in both directions: in a context where the log exists so the evening shift can see the morning shift's work, a consolidated view in one place is what "one view" names, and I can find no case here falling under one and not the other. She is not made to say the trial succeeded. **Unmoved.**

Stance, degree of certainty, reservation and voice are what the source carries in all three. No hedge removed, no hedge added, no two remarks welded into one, no self-correction disturbed.

---

## 7. Intermediate — every finding in the evidence

`report-1.md` on draft-1, six findings, all applied by the writer between draft-1 and draft-2 (confirmed by diff):

| # | Passage | Allegation | What the writer did | My class |
|---|---|---|---|---|
| F1 | `underhållsansvariga Maya Lind`; `underhållsansvarig på Elm Quay Housing` | Role raised from supervising to holding responsibility for the function, against "maintenance supervisor" | Applied: `arbetsledaren`, `arbetsledare för underhållet` | **Supported repair.** The finding is right — *underhållsansvarig* names the head of the function and the material places nobody at its head — and *arbetsledare* is the correct Swedish term for a supervisor |
| F2 | `någon rekommendation till alla bostadsföretag ger Maya Lind inte` | Reservation widened from Svale to any recommendation at all, dropping the named product the brief requires to survive | Applied: `Maya Lind rekommenderar inte Svale till alla bostadsföretag` | **Supported repair.** Draft-1 withheld every recommendation from every housing company, which the material does not say; the repair restores the object |
| F3 | `ett dokument att läsa igenom innan arbetet börjar` | A time of use the brief does not supply | Applied: clause deleted | **Supported repair.** The brief settles what the destination is and says nothing about when it is read; an implementation checklist may well be worked through during the implementation |
| F4 | `Någon jämförelse … finns inte.` | "is available" turned into non-existence | Applied: `finns inte att tillgå` | **Supported repair.** The contract's own rule — what is unclaimed is not thereby known not to have happened |
| F5 | `säger Maya Lind`, `säger hon` ×2 | Written email answers attributed as speech | Applied: `skriver` in all three tags | **Supported repair**, and the sharpest catch in either report. "All interviews occurred by email" rules the manner out outright, and manner is a claim |
| F6 | `Hos underhållsteamet på Elm Quay Housing … lagrades` | The separate storing placed at the maintenance team, which the material does not state | Applied: `Hos Elm Quay Housing …` | **Supported repair**, with residue: the repaired text still supplies a locative the material does not state, but the company is the only reading available for the customer's own reports |

`report-2.md` on draft-2, one finding:

| # | Passage | Allegation | What the writer did | My class |
|---|---|---|---|---|
| S1 | `## Mediantiden var lägre under testet – orsaken är öppen` | The heading drops "från anmälan till tilldelning", the only interval the material measures, at the exact point the judging note guards | **Nothing.** Delivered unrepaired, with the defect disclosed in the reply and the checker's proposed wording quoted there | **Right finding, not acted on.** Of the offered classes this falls nearest *right finding rejected*: the writer agreed with it in words and let the text go out carrying it, which for the reader is the same outcome as rejection. See §2.1 and §8 |

The reply mentions no finding for which a report file is absent; every disposition it describes is traceable to a report in `evidence/`, and the reply's account of what the two reports said matches them.

**Did a real defect go unseen by every checker?** Yes, one: the byline `Av Thomas Barregren` against the brief's "No author name supplied" (§2.2). Both checkers were instructed in their scope notes to leave the byline unassessed, so this is a hole in what the comparison was asked to cover rather than a checker's oversight. A second item, the attribution of the checklist to Svale Systems (§2.3), was seen by the second checker but filed as an editorial question rather than a finding; I would have filed it as a small finding with a one-word repair. Everything else I found under F1 or under §5 was either raised by a checker or explicitly examined and set aside by one, and on those set-asides I agree with them.

Both reports are, on my reading, substantively sound: no wrong finding was accepted, no right finding was rejected on the merits, and neither report invented a defect. The second report's single finding is correct.

---

## 8. Stop or delivery

**A delivery that should not have happened.**

The run held, at the moment of delivery, a validated source-support finding it agreed with, against a claim the material's own judging note names as the drift to avoid, with the smallest repair already written out for it — four words inserted into a heading, requiring no new material, touching no other sentence, and leaving the body untouched by the checker's own account. It delivered anyway, and said in its first line that for that heading it asserts no source fidelity.

The argument the reply makes for itself is real and worth stating: both comparisons were spent, and applying S1 would have produced prose no checker had read, breaking the guarantee that delivered prose equals checked prose. That guarantee is worth something.

It does not survive the comparison, for three reasons. First, the choice was never between a checked defect and an unchecked repair alone — stopping without delivering was available, and a stop is what a validated, unrepaired defect calls for when the repair cannot be verified. Second, repairing a supported defect is not a comparison; the ceiling of two constrains how often a fresh checker may read the draft, not whether the writer may act on what a checker found. Applying a repair the checker itself specified verbatim is the loop working, not the loop being circumvented. Third, the guarantee was preserved in the one respect that mattered least — the reader receives prose a checker read — and broken in the respect that mattered most, since what the reader receives is prose that the run itself says is not supported by the source.

The disclosure is honest, specific and well written, and it is the difference between this and a silent failure. It mitigates. It does not cure: the delivered artefact carries an unsupported claim in a heading, plus a named author the brief says was not supplied, and a reader of the case gets both without the reply attached.

---

## 9. Summary

| Criterion | Verdict |
|---|---|
| Outcome | Delivered; two comparisons; delivered prose identical to the last checked prose (frontmatter aside) |
| F1 | **Fail** — unqualified `Mediantiden` in a heading, against the only measured interval and against the material's named drift; plus a byline the brief says was not supplied, and the checklist given an owner the brief withholds |
| G2 | **Pass** — every part present, in order, each with a job; customer acts throughout, publisher stance truthful, CTA built from the one supplied link. Weakened by near-verbatim duplication between standfirst and lead |
| L1 | **Pass** — V2, compounds, double definiteness, s-passive, genitives and speech dashes all native; one calque (`Här är vad …`) and one stiff phrase (`var i median`) |
| Bridges | (a) 0, (b) 0 as lead-in sentences, (c) 2, no bridge 1; no interviewer invented; no unsupported bridge |
| Quoted speech | All three quotations faithful in meaning, stance, certainty and voice; none missing |
| Delivery | A delivery that should not have happened |
