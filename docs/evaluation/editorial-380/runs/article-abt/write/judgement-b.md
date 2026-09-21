# Judgement B — article-abt / write

Genre: `article` (the draft's `kntnt` metadata and the brief, "Skriv en pedagogisk webbartikel"). The
anatomy therefore applies in full, and every counted line below quotes `anatomy-delivered.json`.

## 1. Outcome

**Delivered.** `delivered.md` exists and the complete draft is inside the reply in a fenced block, under
a delivery account that opens "Utkastet levereras med en känd brist."

**Two source comparisons completed.** `evidence/srccheck/` holds two checker tasks and two reports. The
tasks are identical but for the draft they point at and the report they write: `task-1.md` names
`draft.md` and `report-1.md`, `task-2.md` names `draft-2.md` and `report-2.md`. Both reports end with an
explicit completion status — report 1 "Comparison complete … **Unresolved findings: 3**", report 2
"Comparison complete. … **Unresolved findings: 1.**" The reply's *Comparisons* section agrees: two, the
second required because the first led to changes.

**The delivered prose is byte-identical to the last prose a checker saw.** `diff` of
`evidence/srccheck/draft-2.md` against `delivered.md` from its first prose line reports a single
difference: the delivered file additionally carries the four-line `kntnt` frontmatter block and one blank
line ahead of the headline. No prose byte differs — headline, standfirst, byline, lead, all five sections
and the closing paragraph are the same bytes report 2 read. The frontmatter is declared handoff metadata
in the reply's configuration table and carries no assertion about the material, so it is not a repair.

Consistent with this, report 2's one finding is not repaired in the delivered text: the sentence it names,
"En temperaturgivare svarar på en fråga i taget: hur varm är luften där utrustningen sitter?", stands
unchanged in `delivered.md`, and the reply reports it beside the draft rather than applying the repair.

## 2. Headings

- `# Björkskolans mätning visar när, inte varför` — **statement**. No colon, no question, no overclaim
  (the text's own standfirst gives the same antithesis: "pekar ut vilka lektionspass … men svarar inte på
  varför"). Not an **echo**: the standfirst shares no wording with it and states the contrast in other
  terms, though it does restate the antithesis — a mild redundancy noted under W1, not a word echo.
- `## Placeringen jämfördes aldrig experimentellt` — **statement**. No overclaim: the body carries the
  same qualification ("aldrig ställdes mot varandra i ett kontrollerat upplägg"). First sentence under it
  is "Två av givarna stod nära ytterväggar, fyra på innerväggar" — no echo.
- `## Försöket mätte varken luftdrag eller strålning` — **statement**. No overclaim: the section states
  that only air temperature was registered and that ventilation, draught and perceived temperature were
  outside the measurement. No echo of the sentence beneath it.
- `## Rapporten säger hur ofta, inte hur länge` — **statement**. No overclaim: the first paragraph gives
  the count with its "minst en mätning" exclusion and the last states that the duration is not given.
  No echo.
- `## Effekten av eventuella justeringar är inte mätt` — **statement**. No overclaim; "eventuella" leaves
  open whether any adjustment was made, which is all the text claims. No echo.
- `## Lägg användningstiderna bredvid temperaturserien` — **statement** (an imperative clause stating the
  section's recommendation). No overclaim: the section attributes the recommendation to Rask and then
  gives it as advice. No echo of the first sentence under it.

None is a **label**, a **colon** heading or a **question**.

## 3. F1 — fail

One unsupported addition survives into the delivered text. Everything else checks out against
`work/source.md`; I set out both below.

**The defect.**

- Draft (§3, first sentence): "En temperaturgivare svarar på en fråga i taget: hur varm är luften där
  utrustningen sitter?"
- Material: "En givare mäter temperaturen där den sitter." and, separately and about this trial,
  "Operativ temperatur är ett annat mått som tar hänsyn till både luftens temperatur och värmestrålningen
  från omgivande ytor; försöket mätte bara lufttemperatur."
- What differs: scope and the thing measured. The material says of a sensor that it measures *the
  temperature* where it sits, and says of *this trial* that only air temperature was measured. The draft
  states as a general property of temperature sensors that what they answer is how warm *the air* is.
  A case compatible with the material stands: a globe thermometer, or a sensor clamped against a surface,
  is a temperature sensor and measures the temperature where it sits, yet does not answer how warm the air
  is there. Nothing supplied excludes it — and the material's own contrast between air temperature and
  radiation from surrounding surfaces is what makes the case live. This matters for the named reader, who
  knows heating but not measurement technique and is being taught here what an instrument can say.
- Smallest supported repair, as report 2 gives it: "hur varmt är det där utrustningen sitter", leaving
  "I Björkskolan registrerades bara lufttemperaturen" two clauses later to carry the air point about
  this trial, where the material puts it.

This is the finding the reply reports (see §8 below), so it does not trip the protocol's "unresolved
mandatory findings not reported" rejection. It remains a defect of the delivered text, and F1 fails on it.

**Everything else is within the material.** Checked in both directions and clean:

- "Under fyra veckor registrerade Lerviks fastighetskontor temperaturen i sex klassrum i Björkskolan" —
  the office is the only actor the material gives; recording interval and duration verbatim.
- "Bakgrunden var klagomål på kall luft, och kontoret ville veta om klagomålen sammanföll med låga
  temperaturer under lektionstid" — the second clause is the supplied purpose with its scope ("under
  lektionstid") and modality ("ville veta om") intact; the first names that same purpose as the
  background rather than adding a separate history. Defensible as written.
- "Vad de inte mätte avgör hur långt siffrorna räcker" — the author's own argument on the supported
  limitation list; presents no new fact. (The earlier draft's "och vad de inte kunde registrera", which
  credited the report with an account of its own limits, is gone — see §8.)
- "Placeringen jämfördes aldrig experimentellt" / "aldrig ställdes mot varandra i ett kontrollerat
  upplägg" — carries the material's qualification "experimentellt"; "kontrollerat upplägg" names the same
  comparison in this context. The consequence, "går det inte att läsa ut vad väggen betydde för ett
  enskilt värde", withholds a cause rather than asserting one, as the judging note demands.
- "Av sammanlagt 120 registrerade lektionspass innehöll 14 minst en mätning under 20 grader Celsius" —
  figures, denominator, the "minst en"-qualification, threshold and unit preserved, and the count is
  never called high, low or modest anywhere in the text. The forbidden norm comparison is respected.
- "Gränsen på 20 grader var kontorets egen arbetsgräns för försöket, inte ett påstående om ett rättsligt
  krav" — whose assertion it is, and the legal disclaimer, carried intact.
- "Hur länge temperaturen låg under arbetsgränsen framgår inte" and "Rapporten säger heller ingenting om
  huruvida eleverna frös" — the report's two silences preserved as silences, not converted into denials.
  "Ingenting om huruvida" is marginally wider than "säger heller inte om", but in Swedish idiom it is read
  as giving no answer on the question, which is exactly the material's claim; unknown is kept apart from
  absent. Not a defect.
- "Driftteknikern Elin Rask gick efter mätperioden igenom tiderna för ventilation och värme tillsammans
  med skolans vaktmästare" — "efter mätperioden" is entailed by the supplied "efter försöket", so weaker,
  not wider; title, name, systems and companion unchanged.
- "Ett nytt försök planeras till november … Finansieringen är inte beslutad" — modality preserved
  ("planeras", not "kommer att genomföras"), no year asserted where the material asserts none, funding
  expressly undecided.
- The quotation "— Vi vet när vi behöver titta närmare. Vi vet ännu inte varför det blev kallt just då,
  säger Elin Rask" — character-for-character the supplied utterance, both sentences, the hedge "ännu" and
  the deictic "just då" intact, no referent resolved. Source and target language are the same, so nothing
  crossed languages. Attribution in the conventional Swedish quoting present; whose assertion it is does
  not move.
- Forbidden inferences swept: no saving, no health effect, no cause of the cold, no effect attributed to
  the sensors, no legal rule anywhere in the text.
- Byline "Av Thomas Barregren": the brief says "Ingen byline är given", so this comes from the invocation
  and not from the material, and the reply's *Byline* section says exactly that. Not a source-support
  claim.

## 4. G1 — pass

The article does the job the brief set for municipal facility managers who know heating but not
measurement technique. The reader learns what a sensor gives ("En temperaturgivare svarar på en fråga i
taget"), what a different measure would give ("Operativ temperatur … väger in både luftens temperatur och
värmestrålningen från omgivande ytor"), why the report gives lesson periods rather than a daily mean ("Ett
medelvärde för hela dagen kan dölja variation under lektionerna"), what the count is and is not ("14 minst
en mätning under 20 grader Celsius" … "Hur länge temperaturen låg under arbetsgränsen framgår inte"), and
what to do next ("lägg tiderna då rummen faktiskt används bredvid kurvan, innan du rör styrningen").

The angle the brief named — what a short trial can and cannot say — is recognisable and held from the
headline to the last clause; every section is a piece of it. The journalistic craft is present and
appropriate: a named source with a title, a dated report named in full, one quotation placed where it
earns its keep, and limits given as limits rather than as a complaint. The brief's prohibition ("Ingen
kommersiell uppmaning") is honoured — the ending asks the reader to do something with their own data and
sells nothing.

## 5. G2 — pass

All the anatomy's parts are present, in order, and each does its own job. From
`anatomy-delivered.json`: `"conforms": true`, `"failures": []`, `"norms": []`.

- **Headline** — "Björkskolans mätning visar när, inte varför", `"characters": 43`, `"words": 6`; inside
  the 20–70-character requirement and within the eight-word, 60-character norm. It states the angle of
  the whole text and is understood alone.
- **Standfirst** — `"words": 54` (requirement: at most 60), `"paragraphs": 1`. It stands alone: who
  measured, where, for how long, what the measurement does and does not answer, and what the article will
  cover. It claims nothing the body does not deliver.
- **Byline** — "Av Thomas Barregren". The brief names no author, so the anatomy puts the invoking user
  there, and the Write run states this in its delivery account, as G2 requires: "The brief says 'Ingen
  byline är given', and the anatomy makes the author the user when the brief names none."
- **Lead** — `"words": 51`, `"paragraphs": 1`, and it stands before the first H2. It begins the work
  rather than restating the standfirst, adding the month, the named and dated report, and the hinge the
  rest of the article turns on: "Vad de inte mätte avgör hur långt siffrorna räcker."
- **Sections** — `"sections": 5`, each with a subheading that states its own angle and is understood on
  its own, and each with paragraphs beneath it (the script lists 2, 2, 3, 3, 2). The body is explanatory
  throughout: method, instrument, figure, status, next step.
- **Ending, as the call to action** — "Lägg användningstiderna bredvid temperaturserien" and "Har du egna
  serier liggande är det där du börjar – lägg tiderna då rummen faktiskt används bredvid kurvan, innan du
  rör styrningen." For the `article` genre this is the useful next step the explanation supports: it is
  precisely the step the limits section established as the only one available, it is attributed to Rask
  one sentence earlier, and it is non-commercial as the assignment demands. The lead's expectation — that
  what was not measured decides how far the figures reach — is visibly met.

One qualitative concern, not a failure: the standfirst's opening sentence and the lead's opening sentence
carry the same facts in nearly the same order ("Under fyra veckor registrerade Lerviks fastighetskontor
temperaturen i sex klassrum i Björkskolan" / "I januari 2026 satte Lerviks fastighetskontor
temperaturgivare i sex klassrum i Björkskolan"). Each part still performs its own job — the standfirst
sets the angle, the lead brings the report and the hinge — so the criterion holds, but a reader meets
office, six classrooms and school twice in two consecutive paragraphs.

## 6. P1 — pass

The reasoning is followable end to end for the named reader, and each unfamiliar concept is introduced
before it is used. "Operativ temperatur" is defined at first mention and then contrasted with what the
trial registered. "Arbetsgräns" is established as the office's own limit in §4 before "under
arbetsgränsen" is relied on in the same section. "Kontrollerat upplägg" arrives as the gloss on the
placements never being compared experimentally, in the same sentence that needs it. "Dygnsmedelvärde" is
explained by the sentence that precedes it.

The transitions are real, not decorative: "Men eftersom placeringarna aldrig ställdes mot varandra …",
"Underlaget omfattar dessutom bara …", "Rapporten redovisar därför lektionspass i stället för …".

Conclusions stay proportionate to visible support. The strongest conclusion in the text — "Vad som hände
vid just de tidpunkterna ligger utanför vad utrustningen kunde fånga" — rests on the two preceding
sections about what was not measured and stops short of naming any cause. Useful technical substance
remains rather than being smoothed away: the five-minute interval, two outer-wall and four inner-wall
sensors, 14 of 120 with its "minst en mätning" qualification, lesson periods against a daily mean, and
the undecided funding for the November trial.

## 7. W1 — pass

A web reader can orient and enter without losing the explanation or the voice. From
`anatomy-delivered.json`: `"paragraphs": 14`, `"paragraphs_of_two_or_three_sentences": 12`,
`"sections": 5`, `"sections_of_two_or_three_paragraphs": 5`, `"failures": []`, `"norms": []`.

- **Counted requirements hold.** Headline `"characters": 43` (20–70); standfirst `"words": 54` (at most
  60) in `"paragraphs": 1`; lead in `"paragraphs": 1`; every subheading inside 70 characters — 43, 46,
  40, 47, 48; every section carries at least one paragraph.
- **No *should* is departed from.** The script reports `"norms": []`. The largest paragraph the script
  measures is `"words": 37`, so none passes 80; no section exceeds three paragraphs; the headline is
  `"words": 6` and 43 characters; and the standfirst and the lead open on different first words
  ("Under" / "I"). Nothing to weigh, because nothing departs.
- ***Most* holds across the text**, which is the only way it may be read: 12 of 14 paragraphs run to two
  or three sentences, and all five sections to two or three paragraphs.
- **Headings are informative** where this genre needs them: each of the five states its section's claim,
  and a reader scanning only the headings gets the argument — placement not compared, draught and
  radiation not measured, how often not how long, effects not measured, put usage times beside the series.
- **Standfirst and lead are complementary** in function: the body is complete once the standfirst's
  promise is covered, and the lead adds the month, the report and the hinge. The overlap in their opening
  facts, noted under G2, is density a sharper writer would have cut, but it costs the reader no
  understanding and fragments nothing — a qualitative concern, not reader loss.

Rhythm is varied rather than uniform: the two-sentence paragraphs of §2 and §5 sit against the
three-sentence explanatory paragraph in §3 and the short quotation paragraph that closes §5.

## 8. L1 — pass

The prose reads as Swedish written by a Swede, not as translated English. The syntax is native throughout:
"Vad de inte mätte avgör hur långt siffrorna räcker", "Har du egna serier liggande är det där du börjar",
"Var givarna satt är dokumenterat", "Underlaget omfattar dessutom bara dessa sex rum". The fronted
subordinate clauses and the V2 inversions that follow them are handled correctly in every instance.

Idiom is Swedish rather than calqued: "svarar på en fråga i taget", "väger in", "titta närmare", "rör
styrningen", "ligger utanför vad utrustningen kunde fånga". No anglicism, no imported English word order,
no stranded preposition where Swedish would not have one. The register suits a trade audience — plain,
concrete, unhurried — and the second-person address in the closing paragraph is the ordinary Swedish trade
address rather than a marketing tone.

## 9. L2 — pass

Swedish locale governs throughout. Dates in Swedish form and lower case: "12 mars 2026", "I januari
2026", "planeras till november". The temperature is given as "20 grader Celsius" and "under 20 grader
Celsius", not with an English degree form. "var femte minut" and "Fyra veckors registrering" are Swedish
number-and-noun constructions. No currency appears, and none is invented; no factual date is invented —
both dates in the text are the supplied ones. Spelling and inflection are Swedish throughout, and the
byline uses the Swedish "Av" form.

Punctuation is Swedish where it counts: the parenthetical in the last paragraph uses a spaced en dash
("är det där du börjar – lägg tiderna …"), which is the Swedish tankstreck and exactly the place English
would have set an unspaced em dash, and direct speech is set with a talstreck rather than English
quotation marks. One mechanical inconsistency is worth naming without failing on it: the talstreck at
"— Vi vet när vi behöver titta närmare" is an em dash while the tankstreck in the last paragraph is an en
dash. Both marks are found in Swedish practice and Svenska skrivregler's preference is the en dash, so
this is an inconsistency between two accepted marks rather than an imported form — a qualitative concern
for a proofread, not a locale failure.

## 10. T2 — pass

A technique is named: the delivered text's own metadata carries `technique: abt`, and the reply's
configuration table gives Technique `abt` from the invocation. ABT is therefore judged.

- **And** — the situation, stated without drama: "I januari 2026 satte Lerviks fastighetskontor
  temperaturgivare i sex klassrum i Björkskolan. Bakgrunden var klagomål på kall luft …" Four weeks, six
  rooms, a named and dated report.
- **But** — the genuine complication, and it is genuine rather than manufactured: "Vad de inte mätte
  avgör hur långt siffrorna räcker", opened out across three sections — placement never compared
  experimentally, neither draught nor radiation measured, and "Hur länge temperaturen låg under
  arbetsgränsen framgår inte." The complication is the real limit of the material, not an invented crisis:
  the text never says pupils were cold, never calls 14 of 120 high, and never asserts a cause.
- **Therefore** — the supported response: "Rask rekommenderar att temperaturserierna kopplas till
  användningstiderna innan styrningen ändras", carried into the reader's own next step. It is warranted by
  the But rather than dissolving it, and it claims no triumph — the effect of any adjustment is expressly
  unmeasured and the next trial's funding expressly undecided.

The three relate as an arc rather than as three stacked assertions, and the headline states the arc's
turn ("visar när, inte varför") without overstating either half.

## 11. Checker findings

**`evidence/srccheck/report-1.md` — three findings, all accepted and repaired.**

1. **Lead, "redovisar vad givarna registrerade – och vad de inte kunde registrera."** Checker: the
   material records the report's *silence* on its limits ("Den säger inte hur länge …", "Den säger heller
   inte om eleverna frös"), and the draft converts that silence into an account the report itself gives;
   "inte kunde" also asserts an incapability the material never states. Writer: accepted and repaired —
   the clause is replaced in `draft-2.md` and in the delivered text by "redovisar vad givarna
   registrerade. Vad de inte mätte avgör hur långt siffrorna räcker." My class: **supported**.
2. **Heading "Placeringen dokumenterades men jämfördes aldrig" and body "ställdes aldrig mot varandra i
   försöket."** Checker: the material's qualification "experimentellt" is dropped, widening a denial of
   experimental comparison into a denial of all comparison. Writer: accepted and repaired — heading now
   "Placeringen jämfördes aldrig experimentellt", body now "aldrig ställdes mot varandra i ett
   kontrollerat upplägg". My class: **supported** — the material qualifies its denial precisely, and a
   tabulated outer-wall/inner-wall comparison within the trial is compatible with it.
3. **Closing clause "med schemat bredvid kurvan."** Checker: "schemat" is planned use where the supplied
   "användningstider", glossed by the material as "när rummen används", is actual use. Writer: accepted
   and repaired — "lägg tiderna då rummen faktiskt används bredvid kurvan". My class: **supported** — the
   material makes the distinction live by putting notes on actual use into the *next* trial.

**`evidence/srccheck/report-2.md` — one finding and two editorial questions.**

4. **"En temperaturgivare svarar på en fråga i taget: hur varm är luften där utrustningen sitter?"**
   Checker: a fact about this trial is stated as a general property of temperature sensors; a globe
   thermometer or a surface-mounted sensor measures the temperature where it sits without answering how
   warm the air is. Writer: not repaired, and reported beside the draft in the delivery account, on the
   stated ground that the contract forbids changing prose after the final comparison. My class:
   **supported** — and, per §3, a defect of the delivered text.
5. **"Rapporten säger heller ingenting om huruvida eleverna frös."** Checker: raised in report 2 §5 as an
   editorial question, not a defect — "ingenting om huruvida" negates over all content bearing on the
   question where the material only withholds an answer, but Swedish idiom reads it as the material's
   claim. No repair proposed. Writer: not repaired; named in the reply as an editorial question. My
   class: **disputed** — the material settles it neither way and the reading it turns on is one the
   material leaves open.
6. **"Bakgrunden var klagomål på kall luft."** Checker: report 2 §5, again an editorial question — the
   material supplies the complaints only inside the office's stated purpose, not as separately asserted
   background. No repair proposed. Writer: not repaired; named in the reply. My class: **disputed**.

**A real defect seen by no checker:** none. The one F1 defect I found (§3) is finding 4 above, which
checker 2 caught and stated in the same terms. Nothing else in the delivered text fails F1 in my reading,
so there is no missed defect to report.

## 12. Remaining findings

The reply's delivery account reports exactly one remaining finding, under the heading "**Kvarstående
anmärkning (källtäckning, omfång)**":

- **Passage:** "En temperaturgivare svarar på en fråga i taget: hur varm är luften där utrustningen
  sitter?"
- **What the material carries instead:** "En givare mäter temperaturen där den sitter." and, as a separate
  statement about this trial, "försöket mätte bara lufttemperatur." The reply quotes both, and states the
  case that fells the draft's sentence: "En globtermometer eller en givare fäst mot en yta mäter också
  temperaturen där den sitter, men svarar inte på hur varm luften är."
- **Proposed repair:** "hur varmt är det där utrustningen sitter" — with the reply noting that "Meningen
  'I Björkskolan registrerades bara lufttemperaturen' två satser senare bär redan luftpoängen, och där hör
  den hemma — om just det försöket."
- **Is it a defect?** Yes. §3 judges it a defect of the delivered text on the same grounds, and F1 fails
  on it. Reporting it satisfies the reporting obligation; it does not remove the quality problem, and the
  delivered text carries one.

The reply additionally names the two editorial questions from report 2 §5 (items 5 and 6 above) as
"redaktionella frågor snarare än brister, utan förslag till rättelse". Neither is a defect in my reading;
both are `disputed`.

## 13. Class of the run

**`valid delivery`.**

The run completed two source comparisons; the second read the repaired draft in full and completed
("Comparison complete. … **Unresolved findings: 1.**"); the prose delivered is byte-for-byte the prose
that second comparison read; and the one finding it left unrepaired is quoted in the delivery account with
the material, the checker's case and the proposed repair, ahead of the draft itself. Nothing was changed
after the last comparison, so no unchecked prose reached the reader. The delivered text carries one
remaining quality problem — the unsupported generalisation about temperature sensors — and the run says so
plainly rather than delivering it silently, which is what a valid delivery with a reported finding looks
like.
