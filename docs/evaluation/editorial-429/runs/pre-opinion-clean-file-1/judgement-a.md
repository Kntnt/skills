# Judgement a

## 1. Differences

None. `diff work/input.md work/output.md` exits 0: the returned text is byte for byte identical to the input, including the headline, the bold standfirst, the `Text: Sanna Ek, Öppna beslut` byline, the three `##` subheadings, every paragraph and the closing sentence. There is no frontmatter in either file, and no formatting change.

## 2. The account

There are no differences to account for. The reply's claim matches the file: "Den behövde inget arbete, så filen är byte för byte identisk med `input.md`." Its statements "inget fynd fanns gjordes ingen rättningsrunda", "Den avslutande korrekturläsningen hittade inga fel att rätta" and "inget påstående har tagits bort, ändrats eller lagts till" are all accurate against `work/output.md`.

The measurements the reply gives also check out against the input: the headline is 47 characters, the standfirst is 39 words, the subheadings are 40, 33 and 39 characters, and the longest paragraph is 50 words.

## 3. The frozen expectation

**"Conforms to the anatomy."** The expected result is that the run detects nothing. The reply reports: "**Granskning:** inga fynd. Texten följer artikelns anatomi utan avvikelser." Met.

**Preserve the polemical final sentence.** Preserved: "Ett antagande blir inte ett beslutsunderlag för att kalendern säger september."

**Preserve the early thesis.** Preserved: "Kommunstyrelsen i Lervik bör skjuta upp bytet till enbart digital bokning av föreningslokaler, ett byte som kan ske i september."

**Preserve the attribution.** Preserved. The byline "Text: Sanna Ek, Öppna beslut" is kept, and so is the source attribution in the body: "Kommunens pilotrapport från den 8 april 2026 räknar 96 webbokningar och 24 telefonbokningar …"

**Preserve the real administrative objection.** Preserved: "Förvaltningen vill slippa dubbel administration. Det är en relevant invändning."

**Preserve the cost uncertainty.** Preserved: "Att behålla två kanaler kostar arbete, och hur mycket behöver vägas mot vad användarna får." and "ta ställning till dess ännu okända kostnad".

**Preserve the ending's named decision for the council.** Preserved: "Kommunstyrelsen bör därför säga ja till halvåret med båda bokningsvägarna, ta ställning till dess ännu okända kostnad och ge förvaltningen i uppdrag att mäta tidsåtgången samt fråga användarna varför de väljer sin bokningsväg."

**Do not flatten to neutral exposition or add generic hedges.** Not done. The text is unchanged, so nothing was flattened and no hedge was added.

**Rejections:**
- A finding against the 47-character headline: not made. The reply lists "rubriken har 47 tecken och 6 ord" as a limit that holds.
- A finding against the 39-word standfirst: not made ("ingressen har 39 ord i ett stycke").
- A finding against the 33–40-character subheadings: not made ("varje mellanrubrik har högst 40 tecken").
- A finding resting on the single-paragraph section ("Mät också arbetet med två kanaler"): not made.
- A finding resting on the one-sentence closing paragraph: not made.
- A finding resting on the four-sentence paragraph: not made.
- A finding against the Swedish `Text:` byline form: not made.

The run made none of the named mistakes.

## 4. R1

**Pass.** This is a clean control. R1 says "Clean texts may not be rewritten to satisfy taste or numerical guidelines", and the returned text is byte for byte identical to the input. The run raised no finding against any limit the text meets, and it did not check anything against a source it does not have. The reply's account ("filen är byte för byte identisk med `input.md`"; "inget påstående har tagits bort, ändrats eller lagts till") is accurate. Every voice element, argument and claim the expectation names survives verbatim.
