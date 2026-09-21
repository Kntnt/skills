# Judgement A — `runs/article-abt/write`

Genre: `article` (brief: "Skriv en pedagogisk webbartikel"; frontmatter `genre: article`). The anatomy
skeleton therefore applies in full; the script's figures are requirements where the reference states a
plain requirement, and evidence elsewhere.

## 1. Outcome

**Delivered.** `delivered.md` holds a complete draft and `response.md` carries it inside a fenced
markdown block with a delivery account above it.

**Two source comparisons completed.** The evidence shows both dispatches and both returns:
`evidence/srccheck/task-1.md` points a checker at `draft.md`, and `report-1.md` ends "Comparison
complete… **Unresolved findings: 3**"; `task-2.md` points a fresh checker at `draft-2.md`, and
`report-2.md` ends "Comparison complete… **Unresolved findings: 1**". Each task file says "Work only
from what is given below and from the two files named", names the material file as the whole of the
material, and carries no suggested findings — so each is a self-contained comparison, not a
continuation. The reply's *Comparisons* section states the same count, and the evidence bears it out
rather than my having to take its word.

**The delivered prose is byte-identical to the last prose a checker saw.** `diff
evidence/srccheck/draft-2.md delivered.md` reports one hunk only, `0a1,7`: the seven-line `kntnt`
frontmatter block (`genre`, `technique`, `language`) prepended at delivery. Every prose line —
headline, standfirst, byline, lead, all five sections — is unchanged. The frontmatter is the handoff
metadata the reply's configuration table declares ("Handoff metadata | on"), not prose, so no prose
was touched after comparison two.

**Repairs, and when they were made.** No separate disposition file survives under `evidence/`; the
dispositions are given in the reply's *Comparisons* section, and the draft-to-draft diff corroborates
them exactly. `diff draft.md draft-2.md` shows four changed lines, all between the two comparisons,
and each one answers a report-1 finding:

- lead: "redovisar vad givarna registrerade – och vad de inte kunde registrera." → "redovisar vad
  givarna registrerade. Vad de inte mätte avgör hur långt siffrorna räcker." (finding 1)
- subheading: "Placeringen dokumenterades men jämfördes aldrig" → "Placeringen jämfördes aldrig
  experimentellt" (finding 2)
- body: "placeringarna ställdes aldrig mot varandra i försöket" → "placeringarna aldrig ställdes mot
  varandra i ett kontrollerat upplägg" (finding 2)
- close: "med schemat bredvid kurvan, inte med en justering av styrningen" → "lägg tiderna då rummen
  faktiskt används bredvid kurvan, innan du rör styrningen" (finding 3)

Nothing was repaired after comparison two. `report-2.md`'s single finding is unrepaired and is the
finding the reply reports at the top of the delivery.

For completeness: `evidence/srccheck/material.md` is byte-identical to `work/source.md`, so both
checkers had the whole brief and the whole material and nothing else.

## 2. Headings

Quoted from `delivered.md`; the level-1 headline and each level-2 subheading, one to a line.

- H1 — "Björkskolans mätning visar när, inte varför" — **statement**. Not **colon** (the comma is a
  contrastive ellipsis, not a colon standing in for a verb), not **question**, not **overclaim** (the
  text carries both halves: the report gives lesson periods and Rask says "Vi vet när vi behöver
  titta närmare" / "Vi vet ännu inte varför"). Not **echo** at word level — it shares only "varför"
  with the standfirst, and "mätning/Mätningen" — though it restates the standfirst's second
  sentence's proposition in different words. I record the overlap as conceptual, not verbal.
- H2 — "Placeringen jämfördes aldrig experimentellt" — **statement**. No echo of its first sentence
  ("Två av givarna stod nära ytterväggar, fyra på innerväggar"), no overclaim: the material reads
  "Givarnas placering dokumenterades men jämfördes inte experimentellt".
- H2 — "Försöket mätte varken luftdrag eller strålning" — **statement**. No echo of "En
  temperaturgivare svarar på en fråga i taget…". Not overclaim: draught is in the material's
  not-measured list and radiation follows from "försöket mätte bara lufttemperatur", which the
  section itself carries as "I Björkskolan registrerades bara lufttemperaturen".
- H2 — "Rapporten säger hur ofta, inte hur länge" — **statement**. No echo of "Av sammanlagt 120
  registrerade lektionspass…". Not overclaim: "hur ofta" is a count of periods, never called high or
  low, and the body gives it with its "minst en mätning" exclusion.
- H2 — "Effekten av eventuella justeringar är inte mätt" — **statement**. No echo of "Driftteknikern
  Elin Rask gick efter mätperioden…". Not overclaim: "eventuella" is cautious where the material
  never says an adjustment was made, and dropping the material's "ännu" weakens rather than
  strengthens.
- H2 — "Lägg användningstiderna bredvid temperaturserien" — **statement** (an imperative clause that
  states the section's point). No echo of "Fyra veckors registrering i sex rum…". Not overclaim: the
  body attributes the recommendation to Rask by name, as the material does.

No heading is a **label**, a **colon** or a **question**; no heading is an **echo** or an
**overclaim**. `parts.other` in the script's output is `[]`, so there is no heading below level 2.

## 3. F1 — **fail**

One unsupported addition, and one only. Everything else in the draft stays inside the material.

**The defect.** "En temperaturgivare svarar på en fråga i taget: hur varm är luften där utrustningen
sitter?" The material carries two separate statements: "En givare mäter temperaturen där den sitter"
— silent on which quantity — and, about this trial alone, "försöket mätte bara lufttemperatur". The
draft moves the air-only fact off this trial and makes it a general property of every temperature
sensor. A case compatible with the material stands: a globe thermometer, or a sensor clamped to a
wall surface, is a temperature sensor, measures the temperature where it sits, and does not answer
how warm the air is there. The material excludes no such case; it never says what a sensor responds
to. This is a **scope change**, the F1 category of a changed subject, and it lands on exactly the
distinction the section exists to teach a reader the brief describes as one who "kan värmesystem men
inte mätteknik". Small, but a defect rather than a preference. It is reported in the delivery account
(see §7), which satisfies the reporting duty and does not cure the text.

Everything else I checked and found supported:

- "Under fyra veckor registrerade Lerviks fastighetskontor temperaturen i sex klassrum" — "Fiktiva
  Lerviks fastighetskontor satte i januari 2026 temperaturgivare i sex klassrum i Björkskolan";
  "Värden registrerades var femte minut under fyra veckor". Agent shifted from sensors to the office
  that installed them; no change of thing measured, scope or time.
- "Mätningen pekar ut vilka lektionspass som kan undersökas närmare" — "Rapporten redovisar därför
  lektionspass i stället för ett enda dygnsmedelvärde" plus "Vi vet när vi behöver titta närmare".
  Per-period reporting is supplied; the aggregate-only case is excluded.
- "Bakgrunden var klagomål på kall luft" — presupposed by "Kontoret ville veta om klagomål på kall
  luft sammanföll med låga temperaturer under lektionstid", which is the only purpose the material
  gives. Circumstantial background, but the material's own.
- "Av sammanlagt 120 registrerade lektionspass innehöll 14 minst en mätning under 20 grader Celsius"
  — verbatim in substance, including denominator, the "minst en mätning" qualification, the threshold
  and the unit. **No evaluative characterisation anywhere**: the count is never called high, low or
  modest, which the judging note forbids.
- "Gränsen på 20 grader var kontorets egen arbetsgräns för försöket, inte ett påstående om ett
  rättsligt krav" — the material's sentence, with the legal disclaimer intact.
- "Hur länge temperaturen låg under arbetsgränsen framgår inte" / "Rapporten säger heller ingenting
  om huruvida eleverna frös" — the report's silence is preserved as silence, never converted into
  "eleverna frös inte". `Unknown` is kept apart from `absent` throughout.
- "Effekten av eventuella justeringar är inte mätt"; "Driftteknikern Elin Rask gick efter
  mätperioden…" — "efter försöket" entails "efter mätperioden", so the draft is weaker, not wider.
  Title, the two systems, and the caretaker all match.
- "Ett nytt försök planeras till november… Finansieringen är inte beslutad" — modality preserved
  ("planeras", not "genomförs"); no year asserted, as the material asserts none.
- The quotation "— Vi vet när vi behöver titta närmare. Vi vet ännu inte varför det blev kallt just
  då, säger Elin Rask." — character-for-character the material's utterance, both sentences, the hedge
  "ännu" and the deictic "just då" intact. Source and target language are both Swedish, so no
  translation is in play; "sade" → "säger" is the ordinary Swedish quoting present and relocates
  nothing.
- **Forbidden inferences, swept:** no saving, no health claim, no cause of the cold, no effect
  attributed to the sensors, and no legal rule appears anywhere. Causal limits hold in headline,
  standfirst, lead, subheadings and body alike.
- **Author perspective:** "Vad de inte mätte avgör hur långt siffrorna räcker", "Vad som hände vid
  just de tidpunkterna ligger utanför vad utrustningen kunde fånga" and the closing advice are the
  author's argument resting on supported material; the facts inside them are the material's, and
  "utrustningen" is scoped to this trial's sensors rather than to sensors in general.

**Both directions on the translated-term test** do not arise: source and target language are both
Swedish. Within Swedish I ran the same both-ways test on the one term pair the run changed —
"experimentellt" against "ett kontrollerat upplägg" — and nothing in this context falls under one and
not the other, since it is the same comparison at issue.

## 4. G1 — **pass**

The brief names the reader ("kommunala fastighetsförvaltare som kan värmesystem men inte mätteknik")
and the angle ("vad ett kort mätförsök kan och inte kan säga om värmen i en skola"). The article holds
that angle from the headline to the close and never drifts into a story about a cold school.

What the reader learns: that 14 of 120 lesson periods contained at least one reading under 20 °C, and
that the 20 °C line was the office's own working limit rather than a legal one. What the reader sees
the trial could not do: "Ventilation, luftdrag och upplevd temperatur ingick inte i mätningen",
placements never set against each other, duration unrecorded, whether pupils were cold unrecorded.
What the reader can do: "Rask rekommenderar att temperaturserierna kopplas till användningstiderna
innan styrningen ändras. Har du egna serier liggande är det där du börjar."

Journalistic craft for a web explainer is present: a named source, a dated report, a quotation that
carries the argument rather than decorating it, and technical substance kept rather than smoothed away
(five-minute interval, outer versus inner wall, operative temperature, the daily-average problem). The
brief's "Ingen kommersiell uppmaning" is honoured — the close sells nothing.

## 5. G2 — **pass**

The genre is `article`, so the anatomy applies. The script reports `"conforms": true`, `"failures":
[]`, `"norms": []`.

Parts, in the anatomy's order, each doing its own job:

- **Headline** — "Björkskolans mätning visar när, inte varför", `characters: 43`, `words: 6`. It
  states the angle of the whole text, is understood standing alone, claims nothing the text does not
  claim, and does not repeat the standfirst's words.
- **Standfirst** — `words: 54`, `paragraphs: 1`, well inside the 60-word requirement. It stands alone:
  a reader who saw only it would know who measured what, for how long, what it points at and what it
  will not answer.
- **Byline** — "Av Thomas Barregren", `words: 3`. The brief says "Ingen byline är given", so the
  anatomy puts the invoking user there, and the reply's *Byline* section states exactly that: "the
  anatomy makes the author the user when the brief names none… your name, taken from the invocation
  and not from the material." A Write run's duty to state this in the delivery account is discharged.
- **Lead** — `words: 51`, `paragraphs: 1`, and it sits above the first `##`, as the script's `parts`
  placement shows. It begins the work rather than summarising it, and its last sentence ("Vad de inte
  mätte avgör hur långt siffrorna räcker") sets the expectation the body then meets.
- **Sections** — five, each with a subheading and, per the script, 2, 2, 3, 3 and 2 paragraphs; every
  section has at least one paragraph. The body is explanatory throughout: each section takes one thing
  the trial could or could not establish and explains why.
- **Ending as a call to action** — "Lägg användningstiderna bredvid temperaturserien" and "lägg
  tiderna då rummen faktiskt används bredvid kurvan, innan du rör styrningen". For the `article`
  genre this must be the useful next step the explanation supports, commercial only where the
  assignment warrants: it is exactly the step the five sections build to, it is Rask's own supplied
  recommendation, and it is non-commercial, as the brief requires. It also shows the lead's
  expectation met — the numbers reach as far as timing, and no further.

## 6. P1 — **pass**

Every unfamiliar concept is introduced before it is used. "Operativ temperatur är ett annat mått, som
väger in både luftens temperatur och värmestrålningen från omgivande ytor" defines the term at first
use. The daily-average problem is explained before the reader is told why the report chose lesson
periods: "Ett medelvärde för hela dagen kan dölja variation under lektionerna. Rapporten redovisar
därför lektionspass i stället för ett enda dygnsmedelvärde." "Arbetsgräns" is defined where it first
appears and is then used in the short form "arbetsgränsen" one paragraph later, which the reader can
resolve.

Transitions are real rather than connective filler: "Vad de inte mätte avgör hur långt siffrorna
räcker" is the hinge from what was recorded to what was not, and "Men eftersom placeringarna aldrig
ställdes mot varandra i ett kontrollerat upplägg går det inte att läsa ut vad väggen betydde för ett
enskilt värde" carries an actual inference.

Conclusions are proportionate to visible support — conspicuously so. The article draws no cause, no
saving and no health effect, and where the material stops the text stops with it. Useful technical
substance remains rather than being smoothed into generality: the five-minute sampling interval, the
two-outer/four-inner split, the "minst en mätning" qualification, and the air-versus-operative
distinction all survive into the delivered prose.

## 7. W1 — **pass**

Judged against the script's figures.

Counted requirements, all met: headline `characters: 43`; standfirst `words: 54`, `paragraphs: 1`;
lead `paragraphs: 1`; subheadings at `characters` 43, 46, 40, 47 and 48, every one inside 70; every
section carries at least one paragraph (2, 2, 3, 3, 2). `"failures": []` confirms it.

Norms, none departed from: `"norms": []`. Specifically, no paragraph passes 80 words — the longest the
script records is 37; no section passes three paragraphs; `parts.other` is `[]`, so no heading drops
below level 2; the headline is `words: 6` and `characters: 43`, inside eight words and 60 characters.
Nothing here needs the "possible, and no better for it" test, because nothing departed.

*Most* statements, read across the whole text as they must be: `paragraphs: 14` of which
`paragraphs_of_two_or_three_sentences: 12`, and `sections: 5` of which
`sections_of_two_or_three_paragraphs: 5`. Both hold across the text; I fail no single paragraph or
section on them.

Standfirst and lead are complementary rather than duplicative: the standfirst says what the trial
points at and what it will not answer, the lead gives the who, when and which report. They open on
different first words — "Under" and "I". The body completes what the standfirst promises: "vad ett
kort mätförsök… avgör" (sections 3 and 4), "vad det lämnar öppet" (sections 1, 2 and 4), "vad som
rimligen blir nästa steg" (section 5).

Headings are informative in the way an article needs: each states the angle of its own section, so a
reader scanning the five subheadings alone gets the argument. No density or fragmentation loss — the
short opening paragraph of section 1 (17 words) reads as a deliberate data drop before the
interpretation, not as a fragment.

## 8. L1 — **pass**

The resolved language is Swedish, and the prose reads as written in it rather than assembled in it.
Native syntax throughout: the fronted conditional "Har du egna serier liggande är det där du börjar"
is an idiomatic Swedish inversion no translator would produce by default; "Var givarna satt är
dokumenterat" fronts a subordinate clause the way Swedish does; "svarar på en fråga i taget" and "ger
ett underlag som pekar ut tidpunkter värda en närmare granskning" are ordinary Swedish collocations.
No generic translated-English cadence, no English calque, and the compound nouns
("temperaturserierna", "användningstiderna", "dygnsmedelvärde", "arbetsgräns") are formed as Swedish
forms them rather than as spaced phrases. The quotation is idiomatic spoken Swedish and untouched.

## 9. L2 — **pass**

Swedish locale mechanics hold, and no fact of date or number was invented.

- Dates: "12 mars 2026", "I januari 2026", "till november" — Swedish day-month-year order, month names
  lower case, exactly as Swedish requires, and every one taken from the material.
- Numbers and units: "20 grader Celsius", "var femte minut", "Fyra veckors registrering", "sammanlagt
  120 registrerade lektionspass" — no decimal or thousands separator arises, so no separator
  convention is at risk, and no figure is converted.
- No currency appears anywhere, so no conversion was invented.
- Punctuation: the quotation uses the Swedish talstreck ("— Vi vet när…, säger Elin Rask"), and the
  parenthetical break in the close uses an en dash ("det där du börjar – lägg tiderna…"). Two
  different marks for two different jobs, each used consistently; both are established Swedish
  practice, so this is preserved variation, not an error.
- Capitalisation of proper nouns ("Lerviks fastighetskontor", "Björkskolan", "Mätförsök i
  Björkskolan") follows the material.

## 10. T2 — **pass**

A technique **is** named: `delivered.md`'s `kntnt` metadata carries `technique: abt`, and the reply's
configuration table gives "Technique | `abt` | the invocation". So T2 is judged.

- **And** — the situation, supplied and unembellished: the office installed sensors in six classrooms
  in January 2026, recorded values every five minutes for four weeks, and produced a dated report.
- **But** — a genuine complication, and the material's own rather than a manufactured one: "Vad de
  inte mätte avgör hur långt siffrorna räcker", then four sections of it — placement never compared
  experimentally, draught and radiation unmeasured, duration unrecorded, whether pupils were cold
  unrecorded, the effect of any adjustment unmeasured. This is a real question (how far do the numbers
  reach?), not an invented crisis: nothing says the school is cold, nobody is blamed, and 14 of 120 is
  never dramatised as high.
- **Therefore** — a supported response, not a triumph: put usage times beside the temperature series
  before touching the control, which is Rask's supplied recommendation, plus the November trial whose
  funding is explicitly undecided. The article claims no fix and no result.

The three relate rather than merely follow one another: the headline states the arc in miniature
("visar när, inte varför"), the lead's closing sentence is the pivot into the But, and the Therefore
is the direct consequence of what the But established. No invented crisis, no invented triumph.

## 11. Checker findings

Every finding in both reports, one line each, with my own class of the finding.

**Report 1** (on `draft.md`):

1. Lead, "Rapporten Mätförsök i Björkskolan… redovisar vad givarna registrerade – och vad de inte
   kunde registrera." — alleged: it credits the report with an account of its own limits, where the
   material records only the report's silence ("Den säger inte hur länge…", "Den säger heller inte om
   eleverna frös"). Writer: **repaired**, to "redovisar vad givarna registrerade. Vad de inte mätte
   avgör hur långt siffrorna räcker." My class: **supported** — nothing supplied says the report
   discusses what it could not capture, and "inte kunde" added an incapacity claim too.
2. Subheading "Placeringen dokumenterades men jämfördes aldrig" and body "placeringarna ställdes
   aldrig mot varandra i försöket" — alleged: the material's qualifier "experimentellt" is dropped,
   widening the exclusion from one kind of comparison to all comparison. Writer: **repaired**, to
   "Placeringen jämfördes aldrig experimentellt" and "aldrig ställdes mot varandra i ett kontrollerat
   upplägg". My class: **supported** — "Givarnas placering dokumenterades men jämfördes inte
   experimentellt" qualifies its denial precisely, and a non-experimental side-by-side is compatible
   with it.
3. Close, "med schemat bredvid kurvan" — alleged: "schemat" (planned use) substituted for the supplied
   "användningstider" (actual use). Writer: **repaired**, to "lägg tiderna då rummen faktiskt används
   bredvid kurvan". My class: **supported** — the material glosses the term as "när rummen används"
   and treats notes on actual use as something the next trial must add, so the distinction is live.

**Report 2** (on `draft-2.md`):

4. "En temperaturgivare svarar på en fråga i taget: hur varm är luften där utrustningen sitter?" —
   alleged: a fact about this trial is stated as a general property of temperature sensors. Writer:
   **not repaired**, and reported in the delivery account, on the stated ground that the contract
   allows at most two comparisons and forbids changing prose after the final one. My class:
   **supported** — this is the F1 defect above; the globe-thermometer case stands and nothing supplied
   sets it aside.
5. §5 editorial question — "Rapporten säger heller ingenting om huruvida eleverna frös" against the
   material's "Den säger heller inte om eleverna frös". Raised as a question, not a defect, with no
   repair required. Writer: **left as written**, and named in the reply among the two editorial
   questions. My class: **disputed** — it turns on how strictly Swedish "ingenting om huruvida" is
   read, which the material leaves open.
6. §5 editorial question — "Bakgrunden var klagomål på kall luft", where the material supplies the
   complaints only inside the office's purpose. Raised as "defensible as written", no repair proposed.
   Writer: **left as written**, and named in the reply. My class: **false** — the material's
   "Kontoret ville veta om klagomål på kall luft sammanföll…" presupposes the complaints and gives the
   office no other stated reason, so the passage was defensible as written.

**Did a real defect escape every checker?** No. The one F1 defect I found is item 4, which checker 2
caught. Worth recording, though, that checker 1 saw the same sentence in `draft.md` and cleared it
("'luften' is warranted by the combination of the two supplied statements… Not a finding"), so it was
the second, fresh comparison that caught it — which is the two-comparison arrangement doing the work
it exists to do.

## 12. Remaining findings

The reply reports one finding as remaining, with the passage, the material and a repair:

- **Passage:** "En temperaturgivare svarar på en fråga i taget: hur varm är luften där utrustningen
  sitter?"
- **What the material carries instead:** "En givare mäter temperaturen där den sitter." and,
  separately about this trial, "försöket mätte bara lufttemperatur."
- **Why it stands, as the account puts it:** "utkastet gör ett förhållande som gäller det här försöket
  till en allmän egenskap hos temperaturgivare. En globtermometer eller en givare fäst mot en yta
  mäter också temperaturen där den sitter, men svarar inte på hur varm luften är."
- **Proposed repair:** "hur varmt är det där utrustningen sitter" — the account adds that "I
  Björkskolan registrerades bara lufttemperaturen" two clauses later already carries the air point,
  and that this is where it belongs.
- **Not applied**, and the account says why: "Rättelsen är inte införd, av skäl som står under
  *Comparisons* nedan" — the prose delivered is byte for byte the prose the second comparison read,
  and a repair no comparison has read would be unchecked prose.

**Is it a defect of the text?** Yes — §3 fails F1 on this passage and on nothing else. Reporting it
discharges the duty to report; it does not make the sentence supported.

The account additionally names the two editorial questions from `report-2.md` §5 ("Rapporten säger
heller ingenting om huruvida eleverna frös" and "Bakgrunden var klagomål på kall luft"), correctly
describing them as "redaktionella frågor snarare än brister, utan förslag till rättelse". Under §3 I
class neither as an F1 defect.

## 13. Class of the run

**`valid delivery`.**

The run completed two comparisons, repaired all three findings from the first, and delivered prose
that is byte-identical to what the second comparison read — so the delivered text is fully compared
prose, not something assembled after the last check. The one finding the second comparison left
unrepaired is reported beside the draft, with the passage, the material, the allegation and the
proposed repair, which is what the contract asks of a finding it cannot repair inside its comparison
budget. Delivering was therefore correct: withholding would have been a false stop, since the prose
had a completed comparison of its own and its single remaining defect was disclosed rather than
buried.

The delivery is not clean, and I do not score it as clean: F1 fails on one scope generalisation, and
the delivered article carries a remaining quality problem the reader of the account is told about.
