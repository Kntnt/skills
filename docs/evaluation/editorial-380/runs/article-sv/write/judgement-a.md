# Judgement A — article-sv / write

Genre: `article`, from the brief ("Skriv en pedagogisk webbartikel") and the text's own
`kntnt.genre: article`. The four-genre anatomy therefore applies in full; the scale is not
advisory here.

## 1. Outcome

**Delivered.** `delivered.md` is present and carries the complete draft, frontmatter included.

**One source comparison completed.** Everything under `evidence/source-check/` is numbered 1 and
nothing is numbered 2: `task-1.txt`, `report-1.md`, `reply-1.txt`, `validation-1.md`. The validation
file states it outright — "Complete by that route; one comparison ran, and it is the final one" —
and the reply's account agrees: "En fullständig jämförelse genomfördes av en fristående granskare."

**The delivered prose is byte-identical to the last prose a checker saw.** `evidence/source-check/draft.md`
and `delivered.md` are identical (`diff` empty; both md5 `c6bb94798a4be3d1fd7c94dcc1cb3cea`). The
disposition in `validation-1.md` records the one raised item as "accepted as written; no change made,
so no second comparison is triggered", and the reply says the same: "Eftersom ingen prosa ändrades
efter jämförelsen är det exakt den text granskaren läste som levereras här." No repair after the
comparison appears in any file.

Two things I record but cannot settle from the permitted files:

- The checker could not write its own report file. `report-1.md` opens "The report file could not be
  written: the path lies inside `/Users/thomas/Projects/skills/.git/`... The complete report follows",
  and `report-1.md` is byte-identical to `reply-1.txt`. So the report on disk is the checker's reply,
  relayed by the writer. The relay is self-consistent, but nothing in the permitted files
  independently attests that the relayed text is the checker's unaltered words. That is a **method
  limit** of the evidence, not a defect of the run: the comparison itself covers the whole draft, and
  I reach the same verdict on the material myself.
- The material the checker was given (`evidence/source-check/material.md`) is byte-identical to
  `work/source.md`, so the comparison ran against the whole supplied brief and material.
- Side effects: `inventory-before.txt` and `inventory-after.txt` are outside the set of files this
  brief tells me to read, so I did not open them. Beyond the reply's own account — work files removed,
  `source.md` and an empty `scratch/` left, `evidence/` and `response.md` written at the observer's
  request — I make no finding on side effects either way.

## 2. Headings

Level-1 headline and every level-2 subheading, one to a line:

- `# Mätningen i Björkskolan pekar ut lektioner, inte orsaker` — **statement**, **echo**
  (it shares the verb "pekar ut" and the X-but-not-why contrast with the standfirst's second
  sentence, "Rapporten pekar ut 14 av 120 lektionspass ... men förklarar inte varför").
- `## Givaren mäter luften på sin egen plats` — **statement**
  (first sentence under it: "Värden registrerades var femte minut under fyra veckor" — no echo).
- `## Ett värde under gränsen säger inte hur länge` — **statement**
  (first sentence under it: "I rapporten *Mätförsök i Björkskolan*, daterad 12 mars 2026, står att
  14 av totalt 120 ..." — no echo).
- `## Två metodval styr vad siffrorna betyder` — **statement**
  (first sentence under it: "Gränsen på 20 grader var kontorets egen arbetsgräns för försöket" — no echo).
- `## Koppla temperaturen till när rummen används` — **statement**, in the imperative
  (first sentence under it: "Efter försöket gick driftteknikern Elin Rask igenom tiderna ..." — no echo).

No **colon** headings, no **question** headings, no **overclaim**. `parts.other` in the script is
`[]`, so no heading below level two exists to mark.

## 3. F1 — pass

I compared every assertion, attribution and implication in `delivered.md` with `work/source.md`
myself. I find no unsupported addition, no changed subject, scope, date, modality or certainty, and
no dropped caveat. The passages worth showing the work on:

**Tested and supported.**

- "Rapporten pekar ut 14 av 120 lektionspass med minst ett värde under 20 grader" (standfirst) drops
  "totalt ... registrerade" and "Celsius". The body restores them in full before the figure carries
  any weight — "14 av totalt 120 registrerade lektionspass innehöll minst en mätning under 20 grader
  Celsius" — so the wider reading (that 120 was every lesson period held) is foreclosed where it
  would matter. Not a finding.
- "Siffran 14 av 120 är därför ett antal, inte ett omdöme: att avgöra om det är mycket eller lite
  kräver ett jämförelsetal som mätningen inte ger." This is the forbidden inference met head-on:
  the material says "14 av 120 saknar normjämförelse: kalla det inte högt/lågt", and the draft
  neither calls the count high nor low anywhere.
- "Vilken effekt eventuella justeringar har fått är ännu inte mätt" against "Inga justeringars effekt
  har ännu mätts". The draft's "eventuella" keeps open whether any adjustment was made, which the
  material leaves open: it reports only that Rask "gick ... igenom tiderna" with the caretaker, and
  has her recommend linking series to usage times "innan man ändrar styrningen". Unknown is kept
  apart from absent in the right direction — the draft claims strictly less than a flat assertion
  would. Not a finding.
- "Ett medelvärde för hela dygnet kan dölja variation under lektionerna" against "Ett medelvärde för
  hela dagen kan dölja variation under lektionerna". Both directions tested: a daytime-only average
  (07–17, say) falls under the source's "hela dagen" and not under the draft's "hela dygnet", so the
  terms are not interchangeable in general. In this context the material's own next clause names the
  rejected alternative as "ett enda dygnsmedelvärde", which settles that the 24-hour average is the
  one under discussion. The modality "kan dölja" is preserved. Not a finding.
- "Kontoret ville veta om klagomålen på kall luft ..." makes the source's indefinite "klagomål"
  definite. The source sentence already presupposes that complaints existed — an office does not ask
  whether non-existent complaints coincided with anything. Not a finding.
- "Ett enda värde strax under gränsen räknas likadant som en hel lektion under den" is an entailment
  of the counting rule the material states ("innehöll minst en mätning under 20 grader"), not an
  added fact; it asserts nothing about how often either case occurred.
- The quotation "– Vi vet när vi behöver titta närmare. Vi vet ännu inte varför det blev kallt just
  då, säger Elin Rask." is the material's verbatim statement, both sentences, in order, in the same
  language; only "sade" becomes the conventional Swedish present-tense attribution "säger". Meaning,
  stance and certainty ("Vi vet" / "Vi vet ännu inte") are untouched, and the deictic "just då" is
  not resolved to an occasion the material does not settle.
- "Hon rekommenderar att koppla temperaturserierna till användningstiderna innan någon ändrar
  styrningen" narrows the source's indefinite plurals to this trial's series. In a paragraph that has
  just described this trial, that is the ordinary reading, and no case compatible with the material
  makes the draft hold while the source fails.
- Author's-own passages — "Så långt räcker ett kort mätförsök – och så här kan du komplettera det",
  "smalare än det kan se ut, men användbart om du vet vad det mäter", "Ett underlag utesluter
  ingenting som det inte har mätt", "Den skillnaden är värd att ha med sig när siffran förs vidare",
  and the closing advice — present no fact of their own and rest on limits the material states.
- Forbidden inferences swept: no saving, no health claim, no cause of the cold (the headline and the
  quoted "Vi vet ännu inte varför" assert the opposite), no effect of the sensors or of any
  adjustment, no legal rule ("Den är inget påstående om ett rättsligt krav"), no norm comparison.
  The only causal-looking connectives are "därför" at "Siffran 14 av 120 är därför ett antal" —
  inferential, about what the figure is — and "Rapporten redovisar därför lektionspass", which is the
  material's own word. "Sammanföll" is the material's own coincidence verb.

**The one close call, and why it is not a finding.** "En givare mäter temperaturen där den sitter,
och den mäter luft" (and the heading above it, "Givaren mäter luften på sin egen plats"). The first
clause is verbatim from the material; the second continues the material's generic singular while its
support — "försöket mätte bara lufttemperatur" — is stated about this trial. The case against: the
material itself names operative temperature as "ett annat mått ... som tar hänsyn till både luftens
temperatur och värmestrålningen från omgivande ytor", and an instrument for that measure would be
"en givare" that does not measure air alone; nothing in the material excludes one. The case for:
read as an ordinary reader would in context, the paragraph has just described this trial's six
wall-mounted sensors, and the sentence two later says outright "Försöket mätte bara lufttemperatur",
which localises the claim before it can be carried away. The brief also asks for concepts to be
explained before use "utan att kasta bort tekniken", which is what the generic pedagogic singular
does. The generic over-reading is conceivable, not natural, and the draft supplies its own
correction in the same paragraph, so the passage is defensible as written. **Not a finding**, and
the byline is exempt by G2's own rule (see below).

**F1 — pass.**

## 4. G1 — pass

The brief names the reader — "kommunala fastighetsförvaltare som kan värmesystem men inte mätteknik"
— and the angle: "vad ett kort mätförsök kan och inte kan säga om värmen i en skola". The text holds
that angle in every section and never drifts into heating advice the reader already has.

What the reader learns, concretely: that a sensor measures air where it sits and that operative
temperature is a different measure the trial did not capture; that "minst en mätning under 20 grader"
counts a single reading and a whole cold lesson alike, so the figure says nothing about duration;
that the 20-degree limit was "kontorets egen arbetsgräns för försöket", not a legal requirement; and
that a day-average would have hidden exactly the variation the report was after. What the reader can
do: "koppla temperaturserierna till användningstiderna innan någon ändrar styrningen", and
"bestämma redan nu vad som ska noteras vid sidan av temperaturen".

Craft: the technical substance survives — placement near outer and inner walls, the five-minute
interval, the lesson-period reporting choice — while every term the reader is assumed not to know is
explained at first use. The brief's "Ingen kommersiell uppmaning" is honoured; nothing in the text
sells anything.

**G1 — pass.**

## 5. G2 — pass

The genre is `article`, so the anatomy applies as a requirement; the scale is **not** advisory here.

Parts, in the anatomy's order, all present and all parsed by the script: `parts.headline`,
`parts.standfirst`, `parts.byline`, `parts.lead`, four `parts.sections`, and an ending inside the
last section. `parts.other` is `[]`.

- **Headline** — "Mätningen i Björkskolan pekar ut lektioner, inte orsaker": 56 characters, 8 words
  (script `parts.headline`), inside the 20–70-character requirement. It states the angle, is
  understood alone, and claims no cause. Its overlap with the standfirst is the `echo` mark above:
  one shared verb phrase and one shared contrast. The standfirst still carries what the headline does
  not — the six rooms, the four weeks, the figure and the threshold — so this is not a headline that
  repeats the standfirst. A **qualitative concern**, not a contract rejection.
- **Standfirst** — 45 words, 1 paragraph (script `parts.standfirst`), inside the 60-word requirement
  and the one-paragraph requirement. It stands alone: who measured, where, how long, what the report
  found, what it does not explain, and what the article will give the reader.
- **Byline** — "Av Thomas Barregren", 3 words (script `parts.byline`). The brief says "Ingen byline
  är given", so no author is named in the material, and G2 provides for exactly this: the invoking
  user, stated in the delivery account. The account states it and flags it — "Briefen anger ingen
  författare, och då blir användaren författare... Ska texten gå osignerad eller under någon annans
  namn behöver raden ändras innan den publiceras." Requirement met.
- **Lead** — 46 words, 1 paragraph (script `parts.lead`), one paragraph as required, and it stands
  before the first H2 (the script's `parts.lead` is outside `parts.sections`). It begins the work:
  it dates the trial, gives the office's question, and sets up the article's stance on the evidence
  base.
- **Sections** — an explanatory body of four sections, each doing its own job: the instrument, the
  counting rule, the two method choices, the next step. Every subheading is 38, 44, 39 or 43
  characters (script `parts.sections[*].subheading`), each inside the 70-character requirement, and
  each section has 3, 3, 2 and 3 paragraphs — at least one, as required.
- **Ending, and the call to action** — "Planerar du ett eget mätförsök, är det värt att bestämma
  redan nu vad som ska noteras vid sidan av temperaturen", preceded by Rask's recommendation. This is
  the useful next step the explanation supports and nothing more: the article spent three sections
  showing what the trial did not record, and the ending tells the reader to decide that in advance.
  It is not commercial, which the assignment requires. It meets the lead's expectation — the lead
  promised a basis that is "användbart om du vet vad det mäter", and the ending is what knowing that
  is for.

One observation I record without failing it: the last subheading states in the article's own
imperative what the body attributes to Rask two sentences later. The attribution is intact and
immediate, the recommendation is the material's, and the brief commissions a pedagogic article that
tells this reader what to do, so the heading is a legitimate editorial solution rather than an
overclaim.

**G2 — pass.**

## 6. P1 — pass

Every unfamiliar concept is introduced before it is used. "Operativ temperatur" is defined at first
mention — "ett annat mått, som väger in både luftens temperatur och värmestrålningen från omgivande
ytor" — and only then used to mark what the trial missed. The counting rule is unpacked before the
figure is interpreted: "Ett enda värde strax under gränsen räknas likadant som en hel lektion under
den." "Jämförelsetal" is introduced by its function in the same sentence it appears in.

The transitions are real, not decorative: the instrument section ends on what was not measured
("Ett underlag utesluter ingenting som det inte har mätt"), which is the premise the figure section
then applies to the 14 of 120; the method section explains why lesson periods rather than a daily
average, which is what makes the closing recommendation — link series to usage times — follow rather
than arrive.

Conclusions stay proportionate to visible support. The strongest thing the text concludes is that
the figure is "ett antal, inte ett omdöme", which is a statement about what is missing, not a
finding. The technical substance a property manager needs is all still there: interval, placement,
wall type, what the report reports on.

**P1 — pass.**

## 7. W1 — pass

The script reports `conforms: true`, `failures: []` and `norms: []`, so no counted requirement is
outside its range and no *should* was departed from. Checked individually against the *should*
clauses this criterion names:

- Longest paragraph: 50 words (script, section 4 paragraph 3) — under 80.
- Longest section: 3 paragraphs (script `parts.sections`: 3, 3, 2, 3) — not over three.
- No heading below the second level (`parts.other` is `[]`).
- Headline: 8 words and 56 characters (script) — not past eight words or 60 characters.
- Standfirst and lead open on different first words: "Fastighetskontoret ..." and "I januari 2026 ...".

The *most* statements, read across the whole text as they must be: 12 of 13 paragraphs are of two or
three sentences, and 4 of 4 sections are of two or three paragraphs (script `typical`). Both hold
comfortably; neither is read against any single paragraph or section.

A web reader can orient from the headline and standfirst alone, and each subheading says what its
section will settle, so the text can be entered at any of them. The rhythm carries the argument: the
short two-sentence paragraph "Ventilation, luftdrag och upplevd temperatur ingick inte i mätningen.
Ett underlag utesluter ingenting som det inte har mätt" lands the section's point rather than
padding it. The explanation stays continuous across the breaks — nothing is fragmented into
bullet-sized assertions — and the voice is one voice throughout. The body is complete when the
standfirst is covered: the figure, the missing why, and how to complement the trial are all
delivered.

The one reservation, named as the criterion asks for actual reader loss: the lead's first sentence
re-tells the standfirst's first sentence almost fact for fact ("lät temperaturgivare mäta i sex
klassrum på Björkskolan i fyra veckor" / "satte Lerviks fastighetskontor temperaturgivare i sex
klassrum på Björkskolan"). The lead earns its place with what it adds — the January date, the
office's question, and the article's stance on the basis — and the two open on different words, so
the reader loses a beat, not the thread. A **qualitative concern**, not a failure.

**W1 — pass.**

## 8. L1 — pass

The prose reads as Swedish written by a Swede, not as translated Swedish. Idiom throughout:
"lät temperaturgivare mäta", "Så långt räcker ett kort mätförsök", "väger in", "är värd att ha med
sig när siffran förs vidare", "ett val som formar vad underlaget kan visa". The conditional inversion
without "om" in "Planerar du ett eget mätförsök, är det värt att bestämma redan nu ..." is a native
construction that a translation would not produce. The quotation is set with talstreck and a
trailing attribution — "– Vi vet när vi behöver titta närmare ..., säger Elin Rask" — which is the
Swedish convention for reported speech, not an imported English quotation style. Sentence lengths
vary; no calques, no English word order, no generic translated register.

One mild wobble, noted and not failed: "Ett underlag utesluter ingenting som det inte har mätt"
attributes measuring to the evidence base rather than to the measurement, which is a loose
metonymy in an otherwise precise sentence. It is aphoristic by intent and reads cleanly.

**L1 — pass.**

## 9. L2 — pass

The resolved locale is Swedish (`kntnt.language: sv`; the brief and the material are in Swedish).
Mechanics follow it: the date is "12 mars 2026", Swedish day-month-year with an uncapitalised month;
the temperature is "20 grader Celsius", with the unit spelled and capitalised; the interval is
"var femte minut". Numbers follow Swedish practice — small numbers spelled ("sex klassrum", "fyra
veckor", "Två givare"), larger ones in digits ("14 av 120"), and digits with a unit ("20 grader").
Punctuation is Swedish: the spaced en dash in "ett underlag – smalare än det kan se ut", the
talstreck opening the quotation, the semicolon in "när rummen används; finansieringen är inte
beslutad" carried from the material. No currency and no converted figure appears, and no factual
date is invented — "Nästa försök planeras till november" names no year, exactly as the material does
not. The report title is set in italics rather than in quotation marks, which is a permitted
Swedish typographic choice.

**L2 — pass.**

## 10. T2 — skipped

`T2 — skipped — no technique is named in the text's metadata or in the reply`. The delivered text's
`kntnt` map reads `technique: none`, and the reply states "Teknik: ingen." Nothing is judged under
this criterion, and I infer no technique from the shape of the prose.

## 11. Checker findings

`evidence/source-check/report-1.md` (identical to `reply-1.txt`) reports, in its own words:
"Findings: none. Unresolved findings: none." So there is no finding line to write for an alleged
defect. The one item the report raises is filed by the checker itself as a question rather than a
finding, and it is listed here because the run acted on it:

- **Draft passage:** "En givare mäter temperaturen där den sitter, och den mäter luft."
  **What the checker alleged:** report section 3, an editorial question, not a finding — the second
  clause "continues the material's generic singular while the support for it — 'försöket mätte bara
  lufttemperatur' — is stated about this trial", with the concrete case that "a globe sensor for
  operative temperature is also 'en givare'". It proposed no repair and judged the passage
  "defensible as written".
  **What the writer did with it:** left the prose unchanged. `validation-1.md`: "accepted as written;
  no change made, so no second comparison is triggered", with the context reasoning; the reply
  repeats it and states the checker "föreslog ingen ändring och bedömde meningen som försvarbar som
  den står."
  **My class of the item itself:** `disputed` — the material settles it neither way. It never says
  that every sensor measures air alone, and it never says that an instrument for operative
  temperature was or could be used here; the question turns on whether "en givare" reads generically
  or as this trial's instrument, which the material leaves open. My own reading, given in F1, is that
  the sentence two later localises the claim and the passage is defensible.

**Was a real defect I found under F1 seen by no checker?** No. I found no defect under F1, so there
is nothing the checker missed.

## 12. Remaining findings

The reply's delivery account reports **none**: "**Inga avvikelser återstår.** Inga
översättningsavvikelser heller: källa och måltext är båda på svenska, och citatet är ordagrant
återgivet." It reports the editorial question above as raised and settled, not as remaining, and
states that no prose changed after the comparison.

Nothing is therefore carried into the delivery as an unrepaired finding, and the text is not labelled
as having a remaining quality problem. The two concerns I name of my own accord — the headline's
`echo` of the standfirst's verb phrase, and the lead's overlap with the standfirst's first sentence —
are qualitative concerns inside passing criteria, not findings the account owed a report on.

## 13. Class of the run

**`valid delivery`.**

One complete source comparison ran against the whole draft and the whole supplied material, it
returned no accepted defect, the writer changed nothing afterwards, and the text delivered is
byte-identical to the text that comparison read (`diff` empty, md5 `c6bb94798a4be3d1fd7c94dcc1cb3cea`
on both). The prose the run held had been compared in full and was delivered, which is what a valid
delivery is. None of the protocol's five unconditional rejections is triggered: no unsupported fact,
the locale is Swedish throughout, no mechanical editing was substituted for the work, no mandatory
finding went unreported because none was raised, and the only side-effect evidence available to me is
the reply's own account, which reports the work directory restored.

Verdicts: F1 pass, G1 pass, G2 pass, P1 pass, W1 pass, L1 pass, L2 pass, T2 skipped.
