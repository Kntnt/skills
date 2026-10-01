# Judgement b

## 1. The checker's items

**Item 1.** "**"Den nya rubriken … ger omdömet som en arbetsledares."** … Nothing in it fixes the number to one supervisor. … What is true: the headline credits the view to "Elm Quays arbetsledare", with number left open."

- The item is right about the text. The delivered headline is "Elm Quays arbetsledare anser att gemensam ärendebild hjälper". "arbetsledare" has the same form in singular and plural, and nothing else in the headline fixes the number.
- **Corrected.** `response.md` now says: "Den är en hel sats och ger omdömet till Elm Quays arbetsledare, utan att det framgår om det är en eller flera." This is true of the delivered headline.

**Item 2.** "**"två bestämda former i ingressen byttes mot namn som motsvarar brödtextens"** … "en intern försöksanteckning" is not a name. It is an indefinite noun phrase. … It also doesn't match the body's wording."

- The item is right about the text. The delivered standfirst has "en intern försöksanteckning", which is indefinite. The body has "Elm Quays interna försöksanteckning" (delivered.md line 17).
- **Corrected.** `response.md` now says: "I ingressen byttes de bestämda formerna ”gruppen” och ”anteckningarna” mot ”Elm Quays underhållsgrupp” och den obestämda beskrivningen ”en intern försöksanteckning”." The claims about "names" and about matching the body are gone. Both old forms appear in input.md line 3 and both new forms appear in delivered.md line 3, so the sentence is true.

`check.md` section 2 ("Claim changes the account misses") reads `none`, so there is nothing to handle there.

## 2. What changed after the check

I left out statements about the run rather than about either text. These cover the configuration, the correction budget and whether the round was accepted ("Ändringarna godtogs efter en ny granskning" replaces "den godtogs efter förnyad granskning"). The added "`input.md` är orörd" is a statement about the file, and input.md is present as the arriving text. Nothing in the texts contradicts it.

1. "`input.md` är orörd." Added. No check item called for it. No text contradicts it.

2. "den levererade texten följer anatomin, med ett undantag: rubriken (se anmärkning 1)."
   - Replaces: "Den levererade texten följer artikelanatomin: … Avvikelsen är rubriken, se anmärkning 1."
   - Not called for by the check. It is a judgement plus a pointer, and no text contradicts it.

3. "Rubriken har 60 tecken och 8 ord, och ingressen har 44 ord i ett stycke."
   - Replaces the parenthetical "(rubriken 60 tecken och 8 ord, ingressen 44 ord i ett stycke)". It was a report of the script's result and is now asserted directly.
   - Not called for by the check.
   - True: the delivered headline counts 60 characters and 8 words, and the standfirst is one paragraph of 44 words.

4. "Granskningen läste också de krav skriptet inte räknar: att ingressen står på egna ben, hur den förhåller sig till inledningen, …"
   - Replaces: "… ingressens självständighet och förhållande till inledningen, …"
   - Not called for by the check. It describes the review's scope, and no text contradicts it.

5. "”Gemensam ärendebild hjälper, säger Elm Quay om loggförsöket” lade arbetsledaren Maya Linds omdöme (”Att ha en gemensam bild av ärendena hjälper oss …”) i munnen på organisationen Elm Quay, i formen ”X, säger Y”."
   - Replaces: "Rubriken ”Gemensam ärendebild hjälper, säger Elm Quay om loggförsöket” lade …"
   - Only the word "Rubriken" moved into a bold label. Not called for by the check.
   - True: input.md lines 1 and 23 bear it out.

6. "Den är en hel sats och ger omdömet till Elm Quays arbetsledare, utan att det framgår om det är en eller flera."
   - Replaces: "Den nya rubriken … är en hel sats och ger omdömet som en arbetsledares."
   - Called for by check item 1.
   - True: the headline is a full clause, and "arbetsledare" leaves the number open.

7. "”arbetsledare” har samma form i singular och plural."
   - Split from the draft's "Olöst" sentence, in the same words. Not called for by the check.
   - True.

8. "Den som bara ser rubriken kan därför läsa det som att flera av Elm Quays arbetsledare anser det, medan texten ger omdömet till en enda arbetsledare, Maya Lind."
   - Replaces: "så den som bara ser rubriken kan läsa den som att Elm Quays arbetsledare i plural anser det, medan texten ger omdömet till en arbetsledare, Maya Lind."
   - Not called for by the check.
   - "flera av Elm Quays arbetsledare" ("several of") is narrower than the draft's "Elm Quays arbetsledare i plural". The plural reading credits Elm Quay's supervisors as a group. That entails that more than one of them holds the view, so the plural reading does not contradict the statement.
   - "en enda arbetsledare, Maya Lind" is true. The body gives the view to Lind alone: "Att ha en gemensam bild av ärendena hjälper oss …, säger Lind" (delivered.md line 23).
   - Not false.

9. "”gruppen” och ”anteckningarna” var bestämda former utan referent i ingressen. Den som bara läser ingressen visste inte vilken grupp eller vilka anteckningar det gällde."
   - Split from one draft sentence ("…, så den som bara läser …"). Not called for by the check.
   - True: input.md line 3 names no group and no notes before "gruppen" and "anteckningarna".

10. "”Elm Quays underhållsgrupp” och ”en intern försöksanteckning”. De motsvarar det brödtexten kallar underhållsgruppen och Elm Quays interna försöksanteckning."
    - Split from "Nu står ”…” och ”…”, som motsvarar …". Not called for by the check.
    - True as a statement about what the phrases refer to. The body has "underhållsgruppen" (line 7) and "Elm Quays interna försöksanteckning" (line 17).

11. "Den hävdar nu att Elm Quays arbetsledare anser att en gemensam ärendebild hjälper. Tidigare tillskrevs omdömet Elm Quay som organisation."
    - Split from one draft sentence. Not called for by the check.
    - True.

12. "Rubriken säger inte längre att omdömet gäller loggförsöket, eftersom ”om loggförsöket” togs bort. Den som bara läser rubriken får alltså inte veta att texten handlar om ett försök med en gemensam reparationslogg."
    - Replaces the draft's dash construction ("– ”om loggförsöket” togs bort – så …"), which is now an "eftersom" clause plus "alltså".
    - Not called for by the check.
    - True: the delivered headline mentions neither the trial nor the log.

13. "den säger nu att det som visas kommer från en intern försöksanteckning, i stället för från ospecificerade ”anteckningarna”. Den säger också att det är Elm Quays underhållsgrupp, inte en ospecificerad ”grupp”, vars arbete beskrivs."
    - Split from one draft sentence, with "också" added. Not called for by the check.
    - True: delivered.md line 3.

14. "I ingressen byttes de bestämda formerna ”gruppen” och ”anteckningarna” mot ”Elm Quays underhållsgrupp” och den obestämda beskrivningen ”en intern försöksanteckning”."
    - Replaces: "två bestämda former i ingressen byttes mot namn som motsvarar brödtextens."
    - Called for by check item 2.
    - True: compare input.md line 3 with delivered.md line 3.

## 3. Made false

none

## 4. Removed

- "[Den nya rubriken] ger omdömet som en arbetsledares." Removed and replaced. Check item 1 called for it.
- "två bestämda former i ingressen byttes mot namn som motsvarar brödtextens". The parts claiming "names" and a match with the body's wording are gone. Check item 2 called for it.

Every other statement in `draft.md` about either text is still made in `response.md`, reworded or split as listed under heading 2.
