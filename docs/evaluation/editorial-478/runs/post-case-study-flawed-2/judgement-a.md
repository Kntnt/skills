# Judgement a

## 1. Differences

None. I took the text out of the fenced block in `response.md` and compared it with `work/input.md` using `diff`. The two are byte-identical. That covers the heading, the standfirst, the lead, both subheadings, both quotations, the result paragraph, the closing quotation and the publisher line. Neither file has frontmatter. The formatting (the `#` and `##` headings, the bold standfirst and the en-dash quotation marks) is the same in both.

The run made no mechanical corrections, no repairs, no changes of taste and no changes to any claim.

## 2. The account

The run made no changes, so it has no changes to report. The reply describes the result accurately:

- "Texten levereras oförändrad."
- "Den levererade texten är byte för byte identisk med den som kom in. Inget påstående har tagits bort, ändrats eller lagts till."

The reply also describes a correction round that it rejected and fully reverted. One example it gives is the replacement heading "Elm Quay prövade Svales programvara i åtta veckor". It states that "Inget från försöket finns kvar i den levererade texten", and the diff confirms this.

## 3. The frozen expectation

**Detect first-person supplier praise/rescue: met.**
- Finding 3: "”Vi på Svale är världsledande på att skapa framgång” och ”kunden stod hjälplös innan vi kom” saknar stöd i texten. Båda är skrivna med leverantörens vi och gör kunden till en passiv part."
- Finding 1 covers the heading: "”Vår” är leverantörens vi i berättelsen, och ”fantastiska” är uppblåst värdering", and "inget i den visar att Elm Quay behövde räddas."

**Detect the pre-echoed quote: met.**
- Finding 4: "Mellanrubriken ”Kunden fick en gemensam bild” och citatbryggan ”Maya Lind säger att det hjälper att ha en gemensam bild av ärendena.” säger båda citatets omdöme i förväg. Läsaren möter därför citatet som något redan sagt."

**Detect the duplicate standfirst/lead: met.**
- Finding 2: "Den består av samma mening två gånger, ”Elm Quay registrerade 31 ärenden.”, och ingången börjar med samma mening en tredje gång."

**Detect the causal contradiction: met.**
- Finding 6: "”Vår programvara orsakade därför hela förbättringen.” drar en orsaksslutsats som meningen före uttryckligen avvisar, och ”därför” påstår ett samband som texten motsäger."

**No byline, reported as missing and left unfilled: met.**
- Finding 8: "Ingen författare namnges i texten eller i anropet, så den har inte skrivits in."
- The anatomy section repeats it: "Bylinen saknas, och mätskriptet rapporterar den som frånvarande."
- The returned text has no byline.

**Two subheadings, neither describing its section: partly met.**
- The second subheading is met, together with the clause about it claiming a conclusion the note declines to draw. Finding 5: "Mellanrubriken ”Resultatet bevisar allt”: Den påstår motsatsen till avsnittet under den, där anteckningen säger att arbetsbelastningen var olika och att skillnaden inte kan tillskrivas programvaran."
- The first subheading, "Kunden fick en gemensam bild", is flagged in finding 4, but on a different ground: it pre-echoes the quotation. The finding does not say that the subheading fails to describe its section. For example, it does not say that the subheading leaves out the customer's reservation about the extra week of preparation. The defect is detected, but not for the reason the expectation names.

**No ending section or call to action, reported rather than invented: met.**
- Finding 7: "Det avslutande innehållet står inuti det avsnittet i stället för i ett eget avsnitt med egen mellanrubrik", and "En uppmaning till handling saknas helt. Texten ger inget erbjudande, ingen länk och ingen kontaktväg att bygga en på."
- The run invented no call to action.

**Keep the customer's reservation: met.**
- Preserved verbatim: "– Att ha en gemensam bild av ärendena hjälper oss, men jag skulle lägga till en vecka för förberedelser, säger Maya Lind, arbetsledare hos kunden."

**Keep the factual measures: met.**
- Preserved verbatim: "registrerades 31 ärenden under åtta veckor, med akuta ärenden undantagna. Tiden till tilldelning var två arbetsdagar jämfört med tre tidigare. Anteckningen säger att arbetsbelastningen var olika och att skillnaden inte kan tillskrivas programvaran."
- Finding 6 also asks for the note's caveat to be kept: "bör stå kvar som den är".

**Report unavailable support: met.**
- Finding 3: "saknar stöd i texten".
- Finding 9: "Texten säger inte vad Elm Quay är, vilka ärenden det gäller, vad programvaran gör eller varför försöket gjordes. Det går inte att fylla i utan nytt underlag."
- Finding 1 makes the same point about the rescue claim.

**Rejections:**
- The run invented no byline, no call to action and no support.
- It removed or weakened no preserved claim.
- It did not rewrite for taste.
- It did not claim to have verified anything against a source.

## 4. R1

**Pass.**

**Why it passes:**
- Every visible defect named in the frozen expectation is reported in a finding.
- The first subheading is reported on a pre-echo ground rather than as failing to describe its section.
- Every claim, every quotation and the voice are preserved, because the text is returned byte-identical.
- Nothing is invented.
- Missing support is reported, not filled.

The corpus scores detection and preservation apart from the quality of the final text. The deciding passages are therefore findings 1–9 together with "Den levererade texten är byte för byte identisk med den som kom in."

**Caveat for final-text quality, which R1 does not score.** The run discarded its whole correction round over one defect it had introduced itself, the replacement heading. That also threw away repairs that needed no new facts:

- removing "Vår programvara orsakade därför hela förbättringen."
- removing the duplicated standfirst sentence
- replacing "Resultatet bevisar allt"

The reason it gave for the rejection is also questionable. It preferred the original heading because that heading "angav ett [resultat], om än utan stöd". That means it chose a result claim without support over a heading with support.
