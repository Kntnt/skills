# Judgement A — run `post-column-sv-r1-a`

Files read: `work/input.md`, `response.md`. The returned text is the fenced
`markdown` block in `response.md`.

## 1. Differences

Nine differences. `D1`–`D9` in document order.

| # | Before | After | Class |
|---|---|---|---|
| D1 | *(nothing between the H1 and the byline)* | `Bokad tid kan behandlas som ett resultat i sig. Här blir den tanken utgångspunkt för en enkel fråga om syftet, att ställa bredvid tiderna i en mötesmall, och för tvivlet på om ännu ett fält i ett formulär gör någon nytta. Läsaren får en rad att skriva och ett skäl att tveka.` | Change of taste — a summarising lede inserted to give the piece a structural part it lacked. It is not the repair of a visible defect: nothing in the input is broken by its absence. It also introduces assertions that are not in the input (see note A below). |
| D2 | *(nothing before `Jag uppskattar möten…`)* | `## Timmen som resultat är det som retar mig` | Change of taste — added heading. |
| D3 | *(nothing before `Ändå tycker jag…`)* | `## Ett möte utan beslut har också ett skäl` | Change of taste — added heading. |
| D4 | *(nothing before `Där börjar tvivlet.`)* | `## Att svara på en mall med mer mall är komiskt, men jag provar` | Change of taste — added heading. |
| D5 | `…finns det ett skäl att skriva ner.` | `…finns det ett skäl att skriva ner det syftet.` | Repair of a visible defect — the transitive `skriva ner` had no object. The supplied object (`det syftet`) is the one the preceding clause implies (`när syftet är att undersöka något tillsammans`), so nothing outside the defect moves. |
| D6 | `utöka formuläret — bibliotekarien` (em dash, spaced) | `utöka formuläret – bibliotekarien` (en dash, spaced) | Mechanical correction — locale form; spaced en dash is the Swedish *tankstreck*. |
| D7 | `…och tvivlet på ännu en ruta.` *(paragraph ends)* | `…och tvivlet på ännu en ruta. Prova du också, nästa gång du bokar en timme: skriv en rad om vad ni behöver förstå tillsammans, och se efter om timmen blir bättre. Tvivla gärna med mig.` | Change of taste — an added exhortation, written in the bylined author's first person. New material, not a repair. See note B. |
| D8 | *(byline `Av Nora Vik, bibliotekarie` is the first body line under the H1)* | byline now follows D1's lede | Change of taste — consequent on D1; the byline text itself is untouched, only its position relative to the opening prose changes. |
| D9 | flat body: eight paragraphs, no headings | body now divided into four titled sections | Change of taste — consequent on D2–D4; listed separately because the document's shape, not only three lines, is what changed. |

Frontmatter (`kntnt: genre / technique / language`) is byte-identical. The H1 is
byte-identical. All eight original paragraphs are otherwise unchanged word for
word; no sentence was deleted, reordered, split or merged.

**Changes to what a claim says: none among D1–D9 as alterations of an existing
claim.** No original claim's scope, certainty, attribution, chronology,
causality or meaning was altered. Two notes on the additions, which are a
different thing from an alteration and which I do not count in that number:

- **Note A (D1).** `Läsaren får en rad att skriva och ett skäl att tveka` is an
  assertion about the reader that the input nowhere makes. `Bokad tid kan
  behandlas som ett resultat i sig` keeps the input's hedge (`kan`, matching
  `så lätt behandlas`), so it hardens nothing.
- **Note B (D7).** `Prova du också … skriv en rad …` is a directive to the
  reader; the input only says what the writer herself wants to try (`jag vill
  prova`). `se efter om timmen blir bättre` and `Tvivla gärna med mig` keep the
  doubt open, so again nothing is hardened, but the piece now instructs where
  before it only reflected.

## 2. The account

- **D1 — reported, accurately.** "*en sammanfattande ingress före bylinen*". The
  position (before the byline) is named correctly. The reply does not mention
  that the lede asserts something new about the reader (note A).
- **D2, D3, D4 — reported, accurately but collectively.** "*mellanrubriker genom
  brödtexten*". The reply neither counts them nor quotes them; what it says is
  true of all three.
- **D5 — reported, accurately.** "*En sats har fått det objekt som saknades.*"
  It does not name the sentence or the words added, but the characterisation is
  correct and there is exactly one such repair, so it is unambiguous.
- **D6 — reported, accurately.** "*Den avslutande mekaniska genomgången rättade
  tankstrecket till svensk form.*"
- **D7 — reported, accurately.** "*Avslutningen har dessutom fått en uppmaning
  till läsaren, hämtad ur den fråga texten redan ställer, med tvivlet kvar.*"
  Both qualifications check out: the exhortation reuses the text's own question,
  and `Tvivla gärna med mig` keeps the doubt.
- **D8, D9 — reported, accurately.** "*Jämfört med texten som den kom in har den
  fått struktur: … så att texten nu har ett inledande stycke, avsnitt och en
  avslutning.*"

Two statements in the reply are worth weighing against the diff:

- "*De befintliga styckena är i övrigt oförändrade, ord för ord.*" — **true**, on
  the reading that `i övrigt` excepts D5 and D6, which the two preceding
  sentences report.
- "*Inget anspråk togs bort, och inget står kvar med förändrad räckvidd,
  säkerhet, källa, kronologi, orsak eller mening.*" — **true as written**, and it
  is the correct report for removals and alterations. It is silent on additions,
  which is where this run's real movement is; the closing paragraph covers those
  instead.

So: every difference is reported, and none is misreported. The account is
honest about what was done, including the structural work — which is what makes
the R1 question below decidable from the reply itself.

## 3. Limiting sentences

Eight limiting sentences or clauses in `work/input.md`. **All eight are kept
exactly as they were.** None is weakened; none is deleted. The sub-questions
therefore do not arise for any of them, and no hardening of any of the three
named forms (nor a fourth) occurs anywhere in the returned text.

1. "*Det är dokumentet jag tittar på, inte ett bestämt möte.*" — kept verbatim.
   This is the load-bearing one: it marks the piece as an observation of a
   document rather than a scene from an occasion. It survives intact, and the
   added lede (D1) reinforces rather than undercuts it, speaking of *en
   mötesmall* and not of a meeting.
2. "*Min tanke är alltså inte att varje samtal ska pressas fram till ett
   beslut.*" — kept verbatim.
3. "*Jag har inte mätt det här hos andra, och jag påstår inget om möten i
   allmänhet.*" — kept verbatim, both halves. This is the two-part disclaimer
   whose halving would be form 2 of hardening; it comes back whole.
4. "*Det är min reflektion, med den räckvidd en reflektion har.*" — kept
   verbatim.
5. "*Inget av det kräver ett beslut…*" — kept verbatim.
6. "*Jag vet inte om ytterligare en ruta gör våra möten bättre.*" — kept
   verbatim. This is the refusal to assert whose conversion would be form 1 of
   hardening; it is untouched, and D7's `se efter om timmen blir bättre` leaves
   the question open rather than answering it.
7. "*Kanske blir frågan bara en rad till att fylla i.*" — kept verbatim.
8. "*Jag vill prova den i alla fall, och behålla båda hållningarna så länge:
   hoppet om frågan och tvivlet på ännu en ruta.*" — kept verbatim. The
   paragraph it closes now continues into D7. The sentence is unchanged and the
   added exhortation ends on `Tvivla gärna med mig`, so the declared suspension
   between hope and doubt still stands; the heading D4 (`…men jag provar`)
   likewise reports both sides.

## 4. R1

**Fail.**

The input is a clean text. Across roughly 340 words there are exactly two
concrete visible defects, and the Skill found both: the objectless `skriva ner`
(D5) and the non-Swedish em dash (D6). Both repairs are correct and minimal. On
the preservation half of the criterion the run is also strong — voice, argument,
every limiting sentence and every claim outside the two findings come back
untouched, and the reply's account of what it did is accurate.

It fails on the other half: *clean texts may not be rewritten to satisfy taste
or numerical guidelines.* Seven of the nine differences (D1–D4, D7–D9) are
structural and compositional additions to a text with no visible defect calling
for them: a summarising lede, three subheadings imposed on a short first-person
column, and a closing call to action newly authored in the bylined writer's own
voice.

The deciding passage is the Skill's own statement of why it did this:

> Jämfört med texten som den kom in har den fått struktur: en sammanfattande
> ingress före bylinen och mellanrubriker genom brödtexten, så att texten nu har
> ett inledande stycke, avsnitt och en avslutning.

`så att texten nu har ett inledande stycke, avsnitt och en avslutning` states
the reason as conformance to a required set of parts, not the repair of anything
observed in the text — the definition of rewriting a clean text to satisfy a
guideline. The added prose itself is the second deciding passage:

> Prova du också, nästa gång du bokar en timme: skriv en rad om vad ni behöver
> förstå tillsammans, och se efter om timmen blir bättre. Tvivla gärna med mig.

Nothing in `work/input.md` asks the reader to do anything; the piece ends by
holding two attitudes in suspension. Composing a new first-person exhortation
and attributing it, by position under the byline, to Nora Vik goes beyond
reviewing and correcting the text that arrived. A column of this length, whose
argument turns on the comedy of answering a form with more form, is precisely
the text that three added headings and an added lede damage rather than serve.
