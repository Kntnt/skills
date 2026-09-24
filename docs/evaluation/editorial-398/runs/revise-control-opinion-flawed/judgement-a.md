# Judgement a

## 1. Differences

None. The returned text (the fenced block in `response.md`, lines 4–18) is byte for byte identical to `work/input.md`: title, byline, the four body paragraphs, both subheadings and the closing line. There is no frontmatter in either, and no formatting change. The Skill ran one correction round and rejected it in full. Its changes are described in the reply, but none of them reached the returned text.

## 2. The account

No differences to account for. The reply's claim to have delivered the text unchanged is accurate: "Den levererade texten är byte för byte identisk med den som kom in. Inget påstående har tagits bort, ändrats eller lagts till." I verified this with a diff. The reply also lists what the rejected round changed ("tog bort andra meningen i inledningen", "ändrade 20 procent av invånarna till 20 procent av bokningarna", "tog bort 'Därför kostar det ingenting …'", "skrev nya mellanrubriker och ett nytt avslutande avsnitt"). It states correctly that none of these changes are in the delivered text.

## 3. The frozen expectation

**Detect: unsupported motives.** Detected. Finding 3: "Den hittar på ett motiv hos motståndarsidan." with "'Alla vet' är en källa som saknar namn". Finding 1 covers the motive the title assigns: "'Kommunledningen hatar människor' har inget stöd i texten. Den tillskriver motståndarsidan ett motiv".

**Detect: population inference contradicted by the booking denominator.** Detected. Finding 4: "24 av 120 är 20 procent av bokningarna, inte av invånarna." and "Nästa mening säger att bokningarna inte räknar unika personer och att digital vana inte undersöktes."

**Detect: cost contradiction.** Detected. Finding 5: "Att tiden inte har mätts visar inte att kostnaden är noll. Samma stycke säger dessutom att försökets kostnad inte är beräknad." Finding 3 also flags the "miljoner" claim: "Beloppet har inget stöd, eftersom texten själv säger att försökets kostnad inte är beräknad."

**Detect: vague final exhortation.** Detected. Finding 8: "'Nu är det dags att agera' pekar inte ut någon handling och ingen som ska handla."

**Anatomy: no standfirst.** Detected. Finding 2: "Ingress saknas. Mätningen visar att bylinen kommer direkt efter rubriken, utan någon sammanfattande ingress." The Skill correctly leaves it for the author to write.

**Anatomy: `Bakgrund` and `Diskussion` label the sections instead of describing them.** Detected. Finding 7: "Mellanrubrikerna 'Bakgrund' och 'Diskussion'. De skulle kunna stå i vilken text som helst." The summary line also says that "mellanrubrikerna inte beskriver sina avsnitt".

**Anatomy: no ending section; the exhortation sits inside the last section and names no act.** Detected. Finding 8: "Den står dessutom inne i avsnittet 'Diskussion', som för argumentet vidare. Enligt mallen ska avslutningen vara ett eget avsnitt med egen mellanrubrik".

**Existing action/actor in the body can repair the ending.** Recognised in the finding: "Här kan det vara textens befintliga förslag till kommunstyrelsen." The rejected round wrote a new ending section, but the delivered text keeps the original ending unrepaired. This clause allows a repair; it does not require one. The ending is left unrepaired but is reported with the repair it could take.

**Preserve: qualified facts.** Preserved verbatim: "Det gjordes 96 bokningar på webben och 24 via telefon." / "Kommunens pilotrapport från den 8 april 2026 säger samtidigt att bokningarna inte räknar unika personer och att digital vana inte undersöktes." / "Handlingarna saknar tidsmätning." / "Försökets kostnad är inte beräknad."

**Preserve: the proposal.** Preserved verbatim: "Kommunstyrelsen borde behålla telefonbokning under ett halvårs försök i alla sju lokaler." and "Föreningen vill att förvaltningen mäter tidsåtgång och frågar användarna varför de väljer en bokningsväg."

**Rejections.** The expectation names no specific wrong move beyond losing the qualified facts or the proposal. The run lost neither. It removed nothing and invented nothing.

Other findings, outside the expectation: finding 6 says "Föreningen" has no referent in the body. This is a real visible defect, and the reply correctly calls it irreparable from the text alone.

## 4. R1

**Pass.** The deciding passage is the reply's findings list together with the verified identity of the text: "Alla åtta anmärkningar är olösta." followed by findings 1–8, which name every defect the expectation lists. The delivered text is "byte för byte identisk med den som kom in". The criterion allows a corrected example to keep reported findings. The run changed nothing it had not flagged, altered no claim, lost none of the qualified facts or the proposal, and verified nothing against unavailable sources.

A reservation, which does not decide R1: the Skill rejected the whole round, including correct repairs of findings 3, 4, 5, 7 and 8, over one flaw in the new title (it repeated the lede). The ending, the population claim and the cost claim could all be repaired from what the text itself holds, yet they reach the reader unrepaired. The outcome is sound for detection and preservation but costly for the quality of the final text.
