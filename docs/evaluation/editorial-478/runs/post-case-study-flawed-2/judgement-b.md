# Judgement b

## 1. Differences

None. The text the reply delivers in its `markdown` block is identical to `work/input.md` (checked with `diff`, no output). This includes the headline, the bold standfirst, both subheadings, the quotations, the speech dashes and the closing disclosure line. The input has no frontmatter, and the reply adds none.

## 2. The account

There are no differences to account for. The reply says ”Texten levereras oförändrad” and ”Den levererade texten är byte för byte identisk med den som kom in. Inget påstående har tagits bort, ändrats eller lagts till.” Both statements are accurate.

The reply also says that one correction round was made and then rejected in full. Its stated reason is that the new headline ”Elm Quay prövade Svales programvara i åtta veckor” gave no result for the customer. Nothing from that round is in the returned text, so the account is consistent with it.

## 3. The frozen expectation

**Detect: first-person supplier praise/rescue.** Met.
- Finding 1: ”’Vår’ är leverantörens vi i berättelsen, och ’fantastiska’ är uppblåst värdering”, and ”inget i den visar att Elm Quay behövde räddas”.
- Finding 3: ”’Vi på Svale är världsledande på att skapa framgång’ och ’kunden stod hjälplös innan vi kom’ saknar stöd i texten. Båda är skrivna med leverantörens vi och gör kunden till en passiv part.”

**Detect: pre-echoed quote.** Met. Finding 4: ”Mellanrubriken ’Kunden fick en gemensam bild’ och citatbryggan ’Maya Lind säger att det hjälper att ha en gemensam bild av ärendena.’ säger båda citatets omdöme i förväg. Läsaren möter därför citatet som något redan sagt.”

**Detect: duplicate standfirst/lead.** Met. Finding 2: ”Den består av samma mening två gånger, ’Elm Quay registrerade 31 ärenden.’, och ingången börjar med samma mening en tredje gång.”

**Detect: causal contradiction.** Met. Finding 6: ”’Vår programvara orsakade därför hela förbättringen.’ drar en orsaksslutsats som meningen före uttryckligen avvisar”. Finding 1 also ties the headline's causal claim to the same contradiction.

**Anatomy: no byline, reported as missing and left unfilled.** Met. Finding 8: ”Ingen författare namnges i texten eller i anropet, så den har inte skrivits in.” The anatomy section adds: ”Bylinen saknas, och mätskriptet rapporterar den som frånvarande.” No byline appears in the returned text.

**Anatomy: two subheadings, neither describing its section, the second claiming a conclusion the note declines to draw.** Met for the second subheading, partly met for the first.
- Second subheading, met. Finding 5: ”Mellanrubriken ’Resultatet bevisar allt’: Den påstår motsatsen till avsnittet under den, där anteckningen säger … att skillnaden inte kan tillskrivas programvaran.”
- First subheading, partly met. Finding 4 faults ”Kunden fick en gemensam bild” only because it pre-echoes the quotation. It does not say that the subheading fails to describe its section. That section also carries Lind's reservation about a week of preparation, which the subheading leaves out. The defect is identified, but on a narrower ground than the expectation names.

**Anatomy: no ending section or call to action, reported rather than invented.** Met. Finding 7: ”Det avslutande innehållet står inuti det avsnittet i stället för i ett eget avsnitt med egen mellanrubrik” and ”En uppmaning till handling saknas helt. Texten ger inget erbjudande, ingen länk och ingen kontaktväg att bygga en på.” The returned text contains no invented call to action.

**Preserve: the customer's reservation.** Met. The returned text keeps ”– Att ha en gemensam bild av ärendena hjälper oss, men jag skulle lägga till en vecka för förberedelser, säger Maya Lind, arbetsledare hos kunden.”

**Preserve: the factual measures.** Met. The returned text keeps ”31 ärenden under åtta veckor, med akuta ärenden undantagna. Tiden till tilldelning var två arbetsdagar jämfört med tre tidigare. Anteckningen säger att arbetsbelastningen var olika och att skillnaden inte kan tillskrivas programvaran.” Finding 6 explicitly asks for the note's limitation to stay as it is.

**Report unavailable support.** Met.
- Finding 3: ”saknar stöd i texten”.
- Finding 9: ”Texten säger inte vad Elm Quay är … Det går inte att fylla i utan nytt underlag.”
- Finding 8 covers the byline the same way.

**Rejections.** The run made none of the named mistakes:
- It invents no call to action, contact route or byline.
- It does not drop the reservation or change a measure.
- It does not verify anything against unavailable sources.

## 4. R1

**Pass.**

The deciding passage is ”Den levererade texten är byte för byte identisk med den som kom in. Inget påstående har tagits bort, ändrats eller lagts till.” Read together with findings 1–9, it shows the following:
- Every concrete visible defect named in the expectation is detected and reported.
- Voice, arguments, quotations and claims are fully preserved.
- Nothing is invented or verified against unavailable sources.

The corpus scores detection and preservation apart from the quality of the final text. Under that rule, a returned text that still holds reported findings does not fail R1.

There is one caveat that bears on text quality, not on R1. Several defects needed no outside facts to repair:
- the duplicated standfirst sentence;
- the contradicting ”Vår programvara orsakade därför hela förbättringen.”;
- the ”Resultatet bevisar allt” subheading.

They remain because the Skill threw away its whole correction round over a single headline objection. A selective revert would have kept those repairs. That weakens the deliverable but does not breach R1.
