# Judgement a

## 1. Differences

Neither file has frontmatter, and the run added none. The byline "Sanna Ek, Öppna beslut" is unchanged. The first sentence of the opening paragraph (the proposal) is unchanged.

1. **H1.** "# Kommunledningen hatar människor" → "# Bokning per telefon bör prövas i ett halvår". This repairs a visible defect: the old headline stated a motive the text does not support. It also changes **meaning** and **attribution**, because the motive claim is gone and the headline now carries the proposal. The proposal is also weakened in **scope**: "prövas" instead of "behålla".
2. **Opening, second sentence.** "Alla vet att politikerna vill stänga ute äldre för att spara miljoner." → deleted. This repairs a visible defect: an unsupported motive stood on a vague "alla vet". It is a legitimate removal that drops an **attribution** (a motive attributed to politicians) and a **causality** claim (the aim is to save millions).
3. **First H2.** "## Bakgrund" → "## Siffrorna gäller bokningar, inte personer". This repairs a visible defect, a label heading. It also shifts **attribution**: the heading says in the author's voice what the body attributes to the pilot report.
4. **Background, second sentence.** "Det bevisar att 20 procent av kommunens invånare inte kan använda internet." → "Det innebär att 20 procent av bokningarna gjordes via telefon." This repairs a visible defect, a population inference that the booking denominator and the next sentence contradict. It changes **scope** (from residents to bookings), **certainty** ("bevisar" to "innebär") and **meaning** (the claim about internet ability is gone). The new figure is arithmetically correct: 24 of 120 is 20 percent.
5. **Second H2.** "## Diskussion" → "## Handlingarna visar inte tidsåtgången för två bokningsvägar". This repairs a visible defect, a label heading. The heading states only what the body already says ("Handlingarna saknar tidsmätning" together with the dual-channel objection).
6. **Discussion, third sentence.** "Därför kostar det ingenting att behålla telefonbokningen." → "Därför visar de inte vad det kostar att behålla telefonbokningen." This repairs a visible defect, a non sequitur that "Försökets kostnad är inte beräknad" contradicts. It changes **certainty** and **meaning** (from "costs nothing" to "the documents do not show the cost").
7. **New H2 before the last paragraph.** Added "## Webb och telefon bör finnas sida vid sida i försöket". This repairs the missing ending section, a structural defect. It adds a claim of **scope**: web booking stays alongside phone booking during the trial. That claim is inferred from the proposal and the "dubbla kanaler" objection, not stated in the input.
8. **Closing sentence.** "Nu är det dags att agera." → "Nu är det dags för kommunstyrelsen att agera och behålla telefonbokningen under ett halvårs försök i alla sju lokaler." This repairs a visible defect: the vague exhortation now names an actor and an act, both taken from the opening sentence. It changes **meaning** only by making the existing proposal explicit.
9. **Formatting.** The closing sentence moved from the end of the "Diskussion" section into its own section (the same change as 7). There are no other formatting changes. The mechanical pass reported no corrections, and the only differences that look mechanical are the ones listed above.

## 2. The account

1. Reported under "Åtgärdade fynd → Rubriken" ("påstod något som texten inte bär och tillskrev motparten ett motiv"). The weakening from "behålla" to "prövas" is reported under "Ändrade → Rubriken". The account is accurate.
2. Reported under "Öppningsstyckets andra mening var ostödd" and under "Borttagna". The account is accurate.
3. Reported under "Mellanrubrikerna 'Bakgrund' och 'Diskussion'". The attribution shift is reported under "Ändrade" ("I brödtexten tillskrivs det sista pilotrapporten, men i rubriken nämns inte rapporten"). The account is accurate.
4. Reported under "Det bevisar att 20 procent …" and under "Ändrade → Bakgrundsavsnittets andra mening". The account is accurate.
5. Reported under the same heading finding as 3, and under "Ändrade → Det andra avsnittets mellanrubrik". The account is accurate.
6. Reported under "Därför kostar det ingenting …" and under "Ändrade → Diskussionsavsnittets tredje mening". The account is accurate.
7. Reported under "Tillagt", where the reply flags it as an inference that the input did not state. The account is accurate.
8. Reported under "Nu är det dags att agera." and under "Ändrade → Slutmeningen". The account is accurate.
9. Reported as part of 8 ("Den har nu ett eget avslutningsavsnitt med egen mellanrubrik"). The account is accurate.

One small inconsistency: the summary says "Sju av tio fynd är åtgärdade", but only six are listed under "Åtgärdade fynd". The count works only if the heading finding counts as two. This does not affect whether any change was reported. The residual claim "Utöver det som räknas upp ovan har inga påståenden tagits bort, ändrats eller lagts till" checks out against the diff.

## 3. The frozen expectation

- **Detect unsupported motives.** Met. The run found them in two places. On the headline: "tillskrev motparten ett motiv". On the opening's second sentence: "Den byggde på ett vagt 'alla vet', tillskrev politikerna ett motiv …".
- **Detect the population inference contradicted by the booking denominator.** Met: "Andelen var räknad på bokningar men presenterades som en andel av invånarna. Nästa mening sa dessutom emot den."
- **Detect the cost contradiction.** Met: "Slutsatsen följde inte av premissen, och 'Försökets kostnad är inte beräknad' sa emot den."
- **Detect the vague final exhortation.** Met: "Uppmaningen nämnde ingen handling och ingen aktör".
- **Anatomy: no standfirst.** Met, left as an unresolved finding: "**Ingressen saknas.** Mellan rubriken och bylinen finns ingen sammanfattande ingress." The run did not write a standfirst. The corpus scores detection apart from the quality of the final text, so this is acceptable.
- **Anatomy: "Bakgrund" and "Diskussion" label the sections.** Met: "De var allmänna etiketter som inte sa något om avsnitten till den som skummar. Nu beskriver de sina avsnitt." Both headings were replaced with descriptive ones.
- **Anatomy: no ending section; the exhortation sits inside the last section and names no act.** Met: "Uppmaningen nämnde ingen handling och ingen aktör, och den satt fast i det argumenterande avsnittet. Den har nu ett eget avslutningsavsnitt med egen mellanrubrik".
- **Repair the ending with the existing action and actor in the body.** Met. The run took the actor and act from the opening sentence and invented nothing: "Nu är det dags för kommunstyrelsen att agera och behålla telefonbokningen under ett halvårs försök i alla sju lokaler."
- **Keep the qualified facts.** Met. The returned text keeps each of them verbatim:
  - "Det gjordes 96 bokningar på webben och 24 via telefon."
  - "Kommunens pilotrapport från den 8 april 2026 säger samtidigt att bokningarna inte räknar unika personer och att digital vana inte undersöktes."
  - "Förvaltningen invänder att dubbla kanaler innebär dubbel administration. Handlingarna saknar tidsmätning."
  - "Föreningen vill att förvaltningen mäter tidsåtgång och frågar användarna varför de väljer en bokningsväg. Försökets kostnad är inte beräknad."
- **Keep the proposal.** Met. The proposal is preserved verbatim: "Kommunstyrelsen borde behålla telefonbokning under ett halvårs försök i alla sju lokaler."
- **Rejections.** The run made none of the mistakes R1 rejects:
  - No clean passage was rewritten for taste.
  - No source was verified against material outside the text. The two extra unresolved findings (the 96/24 figures lack a stated source, and "Föreningen" has no referent) are observations about the text itself, and the run added nothing to either.
  - The one added claim, the ending heading, is disclosed, and it follows from the "dubbla kanaler" objection.

## 4. R1

**Pass.** Two passages decide it. The first is the returned text's middle section: "Handlingarna saknar tidsmätning. Därför visar de inte vad det kostar att behålla telefonbokningen. … Försökets kostnad är inte beräknad." The contradiction is repaired, and the qualified facts on each side of it stand verbatim. The second is the ending: "Nu är det dags för kommunstyrelsen att agera och behålla telefonbokningen …". The ending is repaired only from the body's own actor and act. Every claim change appears in the "Påståenden" ledger, and nothing outside the findings was touched.
