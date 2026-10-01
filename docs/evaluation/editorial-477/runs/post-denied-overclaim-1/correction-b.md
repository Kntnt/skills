# Judgement b

Facts checked against the texts: `input.md` headline "Gemensam ärendebild hjälper, säger Elm Quay om loggförsöket" has 59 characters and 8 words. `delivered.md` headline "Gemensam ärendebild hjälper, säger Elm Quays arbetsledare om loggen" has 67 characters and 9 words. `input.md` and `delivered.md` differ only in line 1 (the headline), line 3 (the standfirst) and the last sentence of line 7 (the lead).

## 1. The checker's items

Item 1: **"texten uppfyller anatomin med en avvikelse"**. The checker says the delivered text breaks two norms in the headline, word count and character count, and no hard requirement.

- The item is right about the texts. The delivered headline has 9 words and 67 characters, and the draft itself names both limits it exceeds ("över normerna på högst 60 tecken och högst 8 ord").
- What `response.md` did: **corrected**. In its place it says: "texten följer anatomin med två avvikelser, båda i rubriken." It also says "Avvikelserna är att rubriken nu har 67 tecken och 9 ord. Det är över riktvärdena på högst 60 tecken och högst 8 ord, men inom gränsen på 70 tecken. Avvikelserna kom med ändringen av rubriken."

Under "Claim changes the account misses" the checker lists `none`.

## 2. What changed after the check

The configuration paragraph was reworded ("Konfiguration:" became "Inställningar:", "båda från anropet" became "kommer båda från anropet", "Ingen teknik:" became "Ingen teknik används:", "användes till" became "gick till"). These sentences are about the run's settings, not about either text, so they are not listed below.

1. "alla tre är åtgärdade och inget är olöst"
   - Replaces: "alla tre är åtgärdade, inga kvarstår olösta"
   - Called for by `check.md`: no.
   - Contradicted by the text: no. In `delivered.md`, the lead no longer makes the causal claim, the headline credits the arbetsledare, and the standfirst names "Elm Quays underhållsgrupp" and "gruppens anteckningar".

2. "”loggen kortade tiden från anmälan till tilldelning med en arbetsdag” var ett påstående om orsak som texten inte har stöd för."
   - Replaces: "”loggen kortade tiden från anmälan till tilldelning med en arbetsdag” var ett orsakspåstående som texten inte bär."
   - Called for by `check.md`: no.
   - Contradicted by the text: no. The quotation is exact (input line 7), and line 19 attributes the difference to the workload.

3. "Texten visar bara att mediantiden var två arbetsdagar under försöket och tre under de åtta veckorna före."
   - Replaces the first half of "Texten redovisar bara att mediantiden var två arbetsdagar under försöket mot tre under de föregående åtta veckorna, och avsnittet … säger att …" (the draft sentence was split).
   - Called for by `check.md`: no.
   - Contradicted by the text: no. Input line 17 reads "Mediantiden från anmälan till tilldelning var två arbetsdagar. Under de föregående åtta veckorna var den tre."

4. "Avsnittet ”Två perioder med olika arbetsbelastning” säger dessutom att det enligt anteckningen var arbetsbelastningen och inte programvaran som gav skillnaden."
   - Replaces the second half of the same split draft sentence.
   - Called for by `check.md`: no.
   - Contradicted by the text: no. Input line 19 reads "enligt anteckningen var det arbetsbelastningen och inte programvaran som gav skillnaden", under that heading.

5. "Läsaren fick alltså med sig en effekt som texten längre ned avvisar."
   - Replaces: "Läsaren tog med sig en effekt som texten längre ned avvisar."
   - Called for by `check.md`: no.
   - Contradicted by the text: no. Line 19 denies that the software gave the difference.

6. "”säger Elm Quay” lade omdömet i organisationen Elm Quays mun, men i texten är det arbetsledaren Maya Linds eget (”Att ha en gemensam bild av ärendena hjälper oss”)."
   - Replaces: "”säger Elm Quay” tillskrev organisationen Elm Quay det omdöme som i texten är arbetsledaren Maya Linds eget (…)."
   - Called for by `check.md`: no.
   - Contradicted by the text: no. The input headline reads "säger Elm Quay", and line 23 gives the quotation as Lind's ("säger Lind").

7. "”gruppen” och ”anteckningarna” stod i bestämd form, men standfirsten hade inte nämnt någon grupp eller några anteckningar tidigare."
   - Replaces the first half of "”gruppen” och ”anteckningarna” stod i bestämd form utan att standfirsten hade introducerat någon grupp eller några anteckningar, så den som bara läste standfirsten visste inte vilka som avsågs." (the draft sentence was split).
   - Called for by `check.md`: no.
   - Contradicted by the text: no. The input standfirst (line 3) names only Elm Quay Housing and Maya Lind before "gruppen" and "anteckningarna".

8. "Den som bara läste standfirsten kunde inte veta vilka som avsågs."
   - Replaces the second half of the same split draft sentence ("visste inte vilka som avsågs").
   - Called for by `check.md`: no.
   - Contradicted by the text: no.

9. "meningen säger nu att mediantiden från anmälan till tilldelning var en arbetsdag kortare under försöket än under de åtta veckorna före."
   - Replaces: "meningen säger nu att mediantiden från anmälan till tilldelning under försöket var en arbetsdag kortare än under de föregående åtta veckorna."
   - Called for by `check.md`: no.
   - Contradicted by the text: no. Delivered line 7 reads "under försöket var mediantiden från anmälan till tilldelning en arbetsdag kortare än under de föregående åtta veckorna."

10. "omdömet att en gemensam ärendebild hjälper läggs nu i munnen på Elm Quays arbetsledare i stället för Elm Quay."
    - Replaces: "omdömet att en gemensam ärendebild hjälper tillskrivs nu Elm Quays arbetsledare i stället för Elm Quay."
    - Called for by `check.md`: no.
    - Contradicted by the text: no. The delivered headline reads "säger Elm Quays arbetsledare".

11. "Det sägs också om loggen i stället för om loggförsöket, så omdömet knyts till loggen snarare än till försöket."
    - Replaces: "Det sägs nu dessutom om loggen i stället för om loggförsöket, så omdömet knyts till loggen snarare än till försöket."
    - Called for by `check.md`: no.
    - Contradicted by the text: no. The input headline reads "om loggförsöket", and the delivered headline reads "om loggen".

12. "texten följer anatomin med två avvikelser, båda i rubriken."
    - Replaces: "texten uppfyller anatomin med en avvikelse."
    - Called for by `check.md`: yes, item 1.
    - Contradicted by the text: no. The delivered headline has 9 words and 67 characters, which breaks both limits the reply names.

13. "Mätskriptet visar att de räknade kraven håller."
    - Replaces: "De räknade kraven håller enligt mätskriptet".
    - Called for by `check.md`: no.
    - Contradicted by the text: no. The checker also reports no failures of hard requirements.

14. "Jag har också granskat kraven som skriptet inte räknar, och de håller också:" followed by the list "standfirsten fungerar på egen hand / ingressen för texten framåt / brödtexten fungerar utan standfirsten / mellanrubrikerna beskriver sina avsnitt / sista avsnittet avslutar texten med en uppmaning".
    - Replaces: "de krav skriptet inte räknar – att standfirsten står på egen hand, att ingressen för texten framåt, att brödtexten klarar sig utan standfirsten, att mellanrubrikerna beskriver sina avsnitt och att sista avsnittet är ett avslut med en uppmaning – har granskats och håller."
    - Called for by `check.md`: no.
    - Contradicted by the text: no. These are largely quality judgements. Where the text can be checked, it agrees: the three subheadings match their sections, and the last section ends with "Den som står inför samma förberedelser kan börja i [Svales checklista …]".

15. "Avvikelserna är att rubriken nu har 67 tecken och 9 ord."
    - Replaces: "Avvikelsen: rubriken är nu 67 tecken och 9 ord".
    - Called for by `check.md`: yes, item 1 (the plural).
    - Contradicted by the text: no. The counts are 67 characters and 9 words.

16. "Det är över riktvärdena på högst 60 tecken och högst 8 ord, men inom gränsen på 70 tecken."
    - Replaces: "över normerna på högst 60 tecken och högst 8 ord men inom gränsen på 70 tecken."
    - Called for by `check.md`: no.
    - Contradicted by the text: no. 67 is more than 60 and less than 70, and 9 is more than 8.

17. "Avvikelserna kom med ändringen av rubriken."
    - Replaces: "Den avvikelsen kom med reparationen av rubriken."
    - Called for by `check.md`: yes, item 1 (the plural).
    - Contradicted by the text: no. The input headline has 59 characters and 8 words, inside both limits, so both deviations arrived with the change.

18. "körningen har bara ändrat rubriken, standfirsten och ingressens sista mening."
    - Replaces: "körningen har ändrat rubriken, standfirsten och ingressens sista mening och inget annat i texten."
    - Called for by `check.md`: no.
    - Contradicted by the text: no. The diff of `input.md` against `delivered.md` touches only line 1, line 3 and the last sentence of line 7.

## 3. Made false

none

## 4. Removed

None. Every statement about either text in `draft.md` is still made in `response.md`, either in the draft's words or reworded as listed under heading 2. The draft's "och inget annat i texten" now lives on as "bara" in statement 18. The only removal is the false count "med en avvikelse", which became "med två avvikelser" as `check.md` item 1 called for.
