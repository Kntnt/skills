# Judgement a

## 1. Differences

None. The returned text (the fenced block in `response.md`, lines 11–25) matches `work/input.md` byte for byte. The title, byline, both section headings, every sentence and the closing line are the same. `input.md` has no frontmatter and the reply adds none. The formatting (heading levels, paragraph breaks) is also unchanged.

## 2. The account

With no differences, nothing needs reporting. The reply's account matches the text:

- "Texten nedan är därför exakt den du skickade in" is accurate.
- "Den levererade texten är identisk med den som kom in … Inget påstående har tagits bort, ändrats eller lagts till" is accurate.
- The reply says the proofreading pass found no mechanical errors. Nothing mechanical changed, which is consistent with that.
- The reply reports one correction round that was rejected in full. It says why: the round's new heading "Bokningarna via webb och telefon räknar inte unika personer" moved a caveat that the text attributes to the pilot report into the writer's own voice. That would have been an attribution change, and rejecting it is the correct call. The returned text keeps no trace of the round, which confirms the rollback.

## 3. The frozen expectation

**Detect unsupported motives.** Met. Finding 3: "\"Alla vet\" är en tom källhänvisning. Motivet är påhittat … Läsaren får ett obelagt motiv serverat som allmänt känt." Finding 1 also flags the headline motive: "den tillskriver motparten ett motiv."

**Detect the population inference contradicted by the booking denominator.** Met. Finding 4: "24 av 120 bokningar är 20 procent av bokningarna, inte av invånarna. Nästa mening säger dessutom att bokningarna inte räknar unika personer … Texten underkänner alltså själv sin slutsats."

**Detect the cost contradiction.** Met. Finding 5: "Att tidsmätning saknas visar inte att kostnaden är noll, och \"Försökets kostnad är inte beräknad\" säger emot." Finding 3 also catches "\"Spara miljoner\" motsägs av textens eget \"Försökets kostnad är inte beräknad\"."

**Detect the vague final exhortation.** Met. Finding 7: "Slutet \"Nu är det dags att agera.\" nämner varken handling eller vem som ska handla."

**Anatomy: no standfirst.** Met. Finding 2: "Ingress saknas. Artikelanatomin kräver ett självbärande ingressstycke …"

**Anatomy: `Bakgrund` and `Diskussion` label the sections instead of describing them.** Met. Finding 6: "Mellanrubrikerna \"Bakgrund\" och \"Diskussion\" är rena etiketter," followed by what each section actually covers.

**Anatomy: no ending section; the exhortation sits inside the last section and names no act.** Met. Finding 7: "raden står sist i avsnittet som bär argumentet, så texten saknar ett eget avslutande avsnitt med egen mellanrubrik."

**An existing action and actor in the body can repair the ending.** Recognised but not applied. Finding 7 names the repair material: "Förslaget finns redan i texten: kommunstyrelsen behåller telefonbokningen under ett halvårs försök, och förvaltningen mäter tidsåtgången och frågar användarna." The only correction round was rolled back, so the delivered ending still reads "Nu är det dags att agera." That affects the quality of the final text, which the corpus scores separately. It is not a detection failure.

**Keep the qualified facts.** Met. The returned text keeps "Kommunens pilotrapport från den 8 april 2026 säger samtidigt att bokningarna inte räknar unika personer och att digital vana inte undersöktes," "Handlingarna saknar tidsmätning," and "Försökets kostnad är inte beräknad." Finding 4 also says outright that the pilot-report sentence "ska stå kvar."

**Keep the proposal.** Met. The returned text keeps "Kommunstyrelsen borde behålla telefonbokning under ett halvårs försök i alla sju lokaler" and "Föreningen vill att förvaltningen mäter tidsåtgång och frågar användarna varför de väljer en bokningsväg."

**Rejections.** The expectation names no explicit rejection. The run did not rewrite the clean parts for taste, did not claim to verify anything against unavailable sources, and changed no claim. The one loss it could have made, the attribution shift in the rejected heading, it caught and rejected.

## 4. R1

**Pass.**

Two passages decide it. The findings list shows every visible defect was detected: motive (3), population inference (4), cost non sequitur (5), vague exhortation and missing ending (7), missing standfirst (2), label headings (6). Together they cover all detection clauses. The closing account then shows that nothing outside the findings was lost: "Den levererade texten är identisk med den som kom in … Inget påstående har tagits bort, ändrats eller lagts till." The diff confirms this.

The run also reported a rejected loss accurately. The heading that would have moved the pilot report's caveat into the writer's voice was caught and rolled back ("påstod det som skribentens eget faktum utan rapporten som källa").

One caveat, which does not count against R1 because the corpus scores detection and preservation apart from final-text quality: none of the defects was repaired. That includes the ending, which could have been repaired from material already in the body, and the cost non sequitur, which needs no outside facts. The cause is the budget of one correction round being spent on a round that had to be rolled back.
