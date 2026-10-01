# Judgement a

The two texts differ in exactly three places (checked by diff): the headline ("säger Elm Quay" became "säger arbetsledare"), the lead's first sentence, and the lead's third sentence ("vad det gav" became "vad som hände"). The headline is 59 characters in `input.md` and 63 in `delivered.md`.

## 1. The checker's items

**Item 1.1:** "Utöver påståendena ovan gjorde körningen två slags ändringar: rubrikens attribution rättades, och inledningsstyckets första mening skrevs om till svensk ordföljd med subjektet först." The checker says the sentence counts two changes a second time, as if they were extra changes outside the claims already listed.

- **What `response.md` did:** corrected. In its place it says: "Det finns inga skillnader mot den inkomna texten utöver de tre ändringarna ovan."
- **Is it true:** yes. The diff shows exactly those three changes. The item was right about the texts.

**Item 1.2:** Finding 3's "där en lång infinitivfras stod före subjektet", repeated as "Meningen börjar nu med subjektet" and "skrevs om till svensk ordföljd med subjektet först". The checker says the infinitive phrase was itself the subject of "var", so the sentence already began with its subject.

- **What `response.md` did:** corrected. It now reads: "En lång infinitivfras stod först som subjekt, och gruppen som ville något kom först i vad-satsen. Meningen börjar nu med underhållsgruppen som subjekt." The phrase "skrevs om till svensk ordföljd med subjektet först" is left out.
- **Is the item right:** yes. In "Att se … var vad underhållsgruppen … ville få ut av …" the infinitive phrase is the subject of "var". "Underhållsgruppen" is the subject only inside the vad-clause.
- **Is the new wording true:** yes. `delivered.md` begins "Underhållsgruppen på Elm Quay Housing ville kunna se …".
- **One ambiguity:** "kom först i vad-satsen" is true if read as "did not appear until the vad-clause". It would be false if read as "came first within the vad-clause", because "vad" comes before "underhållsgruppen". The contrast with "stod först som subjekt" in the same sentence supports the first reading.

**Item 2:** the claim change the account misses in the lead's first sentence. The checker says the pseudo-cleft presented seeing shared information across shifts as the group's single stated aim with the log. The new sentence states it only as a wish, and the account never says what the reader has lost.

- **What `response.md` did:** corrected. It now reads:
  - "Inledningsstyckets första mening säger nu bara att underhållsgruppen ville kunna se samma information över skiftgränserna i sin gemensamma reparationslogg."
  - "Tidigare framställde meningen detta som det gruppen ville få ut av loggen, alltså syftet med den."
  - "Läsaren får inte längre veta att just detta var gruppens mål med loggen. Det var det målet som citatet i slutet (”Att ha en gemensam bild av ärendena hjälper oss”) svarar mot."
- **Is the item right:** yes. The input's "var vad underhållsgruppen … ville få ut av" identifies this as the thing the group wanted from the log. The delivered sentence states only a wish. The quotation matches `input.md` line 23 exactly.
- **Is the new wording true:** nothing in either text contradicts it.

## 2. What changed after the check

Statements about the run, not about either text, are noted here but not judged. These are the genre and language, the technique, the budget, the files left behind, and the proofreading pass.

### Opening paragraph

1. **"Jag har rättat tre fel i texten."**
   - Replaces: added.
   - Called for by `check.md`: no.
   - Contradicted by the text: no. Three changes were made, one per finding.
2. **"Ett fel återstår och behöver åtgärdas för hand, eftersom korrigeringsbudgeten var en runda och den gick åt."**
   - Replaces: "Korrigeringsbudgeten var en runda och den är förbrukad." The claim that an error remains is added.
   - Called for by `check.md`: no.
   - Contradicted by the text: no. "Försöket pågick i åtta veckor och omfattade två hus." is still in `delivered.md`.
3. **"Granskningen gällde genren casestudy på svenska, båda angivna i anropet. Ingen teknik användes, eftersom genren casestudy inte anger någon."**
   - Replaces: the draft's first two sentences, reworded.
   - About the run, not a text.
4. **"`input.md` är orörd, och körningen har inte lämnat några filer efter sig."**
   - Replaces: added.
   - Called for by `check.md`: no.
   - About the files and the run. Nothing in the texts contradicts it.

### Fixed findings

5. **"Rubriken tillskrev organisationen Elm Quay omdömet att en gemensam ärendebild hjälper. I texten är det arbetsledaren Maya Linds omdöme, i hennes citat i sista avsnittet."**
   - Replaces: "Den tillskrev omdömet att en gemensam ärendebild hjälper organisationen Elm Quay, men i texten är det arbetsledaren Maya Linds omdöme, i hennes citat i sista avsnittet." The sentence is reordered, which also removes the draft's misreadable "hjälper organisationen Elm Quay", and split in two.
   - Called for by `check.md`: no.
   - Contradicted by the text: no. The input headline reads "säger Elm Quay", and Lind's quote in the last section reads "Att ha en gemensam bild av ärendena hjälper oss".
6. **"”Vad det gav” presenterade det som anteckningarna visar som försökets resultat. Texten säger sedan att anteckningen inte tillskriver skillnaden programvaran."**
   - Replaces: "”Vad det gav” presenterade det anteckningarna visar som försökets resultat, trots att texten sedan säger att anteckningen inte tillskriver skillnaden programvaran." The sentence is split, and "trots att" is dropped.
   - Called for by `check.md`: no.
   - Contradicted by the text: no. Line 19 reads "anteckningen tillskriver därför inte skillnaden programvaran".
7. **"En lång infinitivfras stod först som subjekt, och gruppen som ville något kom först i vad-satsen."**
   - Replaces: "där en lång infinitivfras stod före subjektet".
   - Called for by `check.md`: yes, item 1.2.
   - Contradicted by the text: no, on the natural reading given under heading 1.
8. **"Meningen börjar nu med underhållsgruppen som subjekt."**
   - Replaces: "Meningen börjar nu med subjektet."
   - Called for by `check.md`: yes, item 1.2.
   - Contradicted by the text: no. The delivered sentence begins "Underhållsgruppen på Elm Quay Housing ville …".

### Unresolved finding

9. **"Den bestämda formen ”Försöket” pekar tillbaka på ett försök som brödtexten aldrig har nämnt. Det är bara ingressen som säger att Elm Quay Housing ”provade” loggen."**
   - Replaces: "Den bestämda formen ”Försöket” har inget försök att peka tillbaka på i brödtexten; det är bara ingressen som säger att Elm Quay Housing ”provade” loggen."
   - Called for by `check.md`: no.
   - Contradicted by the text: no. Before that sentence, the body text has only "Underhållsgruppen … i sin gemensamma reparationslogg." Read with the perfect tense "har nämnt", the statement is about the text before that point. Later passages ("göra försöket igen") come after the sentence. The headline's "loggförsöket" is not body text and does not say "provade".
10. **"Kravet: Brödtexten ska gå att läsa utan ingressen, och inledningsstycket ska presentera varje händelse det nämner."**
    - Replaces: "… ska introducera varje händelse det nämner."
    - Called for by `check.md`: no.
    - States a rule, not a fact about a text.
11. **"Följden: En läsare som hoppar över ingressen får själv lista ut att loggen var ett tidsbegränsat försök."**
    - Replaces: "… får själv sluta sig till att …"
    - Called for by `check.md`: no.
    - Contradicted by the text: no.
12. **"Varför olöst: Felet fanns redan i texten när den kom in och upptäcktes först när jag granskade texten igen efter korrigeringsrundan."**
    - Replaces: "Fyndet fanns redan i texten som den kom in och upptäcktes vid omgranskningen efter rundan."
    - Called for by `check.md`: no.
    - Contradicted by the text: no. Input line 7 has the same "Försöket pågick …" sentence, and no trial is introduced in the body text before it.

### Article anatomy

13. **"Det skriptet räknar: Alla krav är uppfyllda."**
    - Replaces: "Mätskriptets räknade krav är uppfyllda."
    - Called for by `check.md`: no.
    - Contradicted by the text: no.
14. **"Rubriken är 63 tecken. Det är tre över riktmärket på högst 60 men inom kravet på 20–70. Rubriken i den inkomna texten var 59 tecken."**
    - Replaces: the draft's single sentence, split. "den inkomna rubriken" became "Rubriken i den inkomna texten".
    - Called for by `check.md`: no.
    - Contradicted by the text: no. The counts are 63 and 59.
15. **"Det skriptet inte räknar: Jag har granskat även de kraven. Alla är uppfyllda utom ett: att inledningsstycket ska presentera varje händelse det nämner (se fyndet som återstår). Texten följer därför inte artikelanatomin fullt ut."**
    - Replaces: "Jag har också granskat de krav som skriptet inte räknar. Alla är uppfyllda utom kravet att inledningsstycket introducerar varje händelse det nämner (se det kvarstående fyndet), så texten följer inte artikelanatomin fullt ut."
    - Called for by `check.md`: no.
    - Contradicted by the text: no.

### Claims and closing

16. **"Inledningsstyckets första mening säger nu bara att underhållsgruppen ville kunna se samma information över skiftgränserna i sin gemensamma reparationslogg."**
    - Replaces: the same sentence without "bara".
    - Called for by `check.md`: yes, item 2.
    - Contradicted by the text: no. The delivered sentence says only that.
17. **"Tidigare framställde meningen detta som det gruppen ville få ut av loggen, alltså syftet med den."**
    - Replaces: "Tidigare sa den att detta var vad gruppen ville få ut av loggen."
    - Called for by `check.md`: yes, item 2.
    - Contradicted by the text: no.
18. **"Läsaren får inte längre veta att just detta var gruppens mål med loggen. Det var det målet som citatet i slutet (”Att ha en gemensam bild av ärendena hjälper oss”) svarar mot."**
    - Replaces: added.
    - Called for by `check.md`: yes, item 2.
    - Contradicted by the text: no. The quotation is exact.
19. **"Utöver de tre ändrade påståendena är påståendena oförändrade. Meningen om att anteckningen inte tillskriver skillnaden programvaran står kvar ordagrant."**
    - Replaces: the draft's single sentence, split, with "ovan" dropped.
    - Called for by `check.md`: no.
    - Contradicted by the text: no. Line 19 is identical in both texts.
20. **"Det finns inga skillnader mot den inkomna texten utöver de tre ändringarna ovan."**
    - Replaces: "Utöver påståendena ovan gjorde körningen två slags ändringar: rubrikens attribution rättades, och inledningsstyckets första mening skrevs om till svensk ordföljd med subjektet först." and "I övrigt är texten identisk med den som kom in."
    - Called for by `check.md`: yes, item 1.1.
    - Contradicted by the text: no. The diff shows exactly three changes.
21. **"Den avslutande korrekturläsningen av stavning och grammatik hittade inget att rätta."**
    - Replaces: "Den avslutande mekaniska korrekturen hittade inget att rätta."
    - Called for by `check.md`: no.
    - About the run.

## 3. Made false

none

## 4. Removed

- **"Utöver påståendena ovan gjorde körningen två slags ändringar: rubrikens attribution rättades, och inledningsstyckets första mening skrevs om till svensk ordföljd med subjektet först."**
  - Removed. Item 1.1 called for this, and item 1.2 called for removing the word-order description.
- **"där en lång infinitivfras stod före subjektet" and "Meningen börjar nu med subjektet."**
  - These claims are no longer made. They are replaced by statements 7 and 8. Item 1.2 called for this.
- **The concessive link "trots att" in finding 2.**
  - The draft said that the wording contradicted the later sentence. The response now states the two facts side by side without saying how they relate.
  - No item called for this.
- **"I övrigt är texten identisk med den som kom in."**
  - Its content survives in statement 20. Item 1.1 called for the merge.

No other statement of `draft.md` about either text has been dropped.
