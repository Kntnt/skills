# Judgement a

The only differences between `input.md` and `delivered.md` are two passages. One is the third sentence of the standfirst (line 3): "vad gruppen gjorde, vad anteckningarna visar" became "vad underhållsgruppen gjorde, vad gruppens anteckningar visar". The other is the first sentence of the lead (line 7): "Att se samma information över skiftgränserna var vad underhållsgruppen på Elm Quay Housing ville få ut av sin gemensamma reparationslogg." became "Underhållsgruppen på Elm Quay Housing prövade sin gemensamma reparationslogg för att kunna se samma information över skiftgränserna."

## 1. The checker's items

`check.md` lists one item, and it lists nothing under "Claim changes the account misses".

**Item 1.** "Utöver detta ändrades två saker. Inledningens första mening byggdes om från en kluven konstruktion till en rak huvudsats. Hänvisningar som bara ingressen förklarade, eller som inget förklarade, gjordes tydliga i ingressen och inledningen." The checker says that "Utöver detta" tells the reader there were changes beyond findings 1–3, and that no such changes exist.

- **The item is right about the texts.** The diff shows only the two passages above. Findings 1–3 already report both of them, and the "två saker" describe the same two changes again.
- **What `response.md` did:** **corrected.** In its place `response.md` says: "Sammanfattat ändrades två slags saker, och båda redovisas ovan." It keeps the two following sentences word for word. The new sentence presents the paragraph as a summary of changes already reported, and the texts agree with that: one change rebuilt a sentence (the lead's first sentence) and the other clarified references (the standfirst's "gruppen"/"anteckningarna" and the lead's "Försöket"). Both are reported in findings 1–3.

## 2. What changed after the check

Changes of formatting alone are ignored here: the colon added before the quotation in finding 1, and the four requirements in paragraph 4 moved into a bullet list.

1. "Texten är granskad som kundcase (`casestudy`) på svenska (`sv`), som anropet angav."
   - Replaces: "Texten är granskad som kundcase (`casestudy`) på svenska (`sv`), båda angivna i anropet."
   - Called for by `check.md`: no.
   - Contradicted by the text: no. This describes how the run was invoked. The only part a text could check is the language, and `delivered.md` is in Swedish.

2. "Ingen berättarteknik användes, eftersom genren inte anger någon."
   - Replaces: "Ingen berättarteknik tillämpades: genren `casestudy` anger ingen teknik som den normalt skrivs med."
   - Called for by `check.md`: no.
   - Contradicted by the text: no. This is about the run, not the content of either text.

3. "Resultatet är skrivet till den nya filen `output.md`, och `input.md` är orörd."
   - Replaces: "Den granskade texten är skriven till `output.md`, som är en ny fil." The clause "och `input.md` är orörd" is added.
   - Called for by `check.md`: no.
   - Contradicted by the text: no. This is about files, not about what either text says, and nothing in the texts contradicts it.

4. "Budgeten var ett korrigeringsvarv och det användes. Därefter återstår inga anmärkningar."
   - Replaces: "Ett korrigeringsvarv användes av budgeten på ett, och efter det återstår inga anmärkningar." The draft's one sentence is split into two.
   - Called for by `check.md`: no.
   - Contradicted by the text: no. This is about the run.

5. "Ingressen stod inte på egen hand. Varken ”gruppen” eller ”anteckningarna” presenterades där, så den som bara ser ingressen visste inte vilken grupp eller vilka anteckningar som avsågs."
   - Replaces: "Ingressen var inte självbärande: varken ”gruppen” eller ”anteckningarna” introducerades där, så den som bara ser ingressen visste inte vilken grupp eller vilka anteckningar som avsågs." The sentence is split, "självbärande" becomes "stod inte på egen hand", and "introducerades" becomes "presenterades".
   - Called for by `check.md`: no.
   - Contradicted by the text: no. The standfirst in `input.md` reads "Här är vad gruppen gjorde, vad anteckningarna visar". Neither a group nor notes are introduced earlier in the standfirst. The first part of the statement ("stod inte på egen hand") is a quality judgement.

6. "Det var bara ingressen som förklarade vad ”Försöket” syftade på."
   - Replaces: "”Försöket” fick sin referent bara från ingressen."
   - Called for by `check.md`: no.
   - Contradicted by the text: no.
   - In `input.md` the lead's first sentence never mentions a trial ("ville få ut av sin gemensamma reparationslogg"). The standfirst says "provade en gemensam reparationslogg i två hus under åtta veckor".
   - The headline's "om loggförsöket" also names the trial. However, it uses the definite form and assumes the reader already knows the trial; it does not explain it. The claim is the same one the draft made.

7. "Läst utan ingress sa brödtexten aldrig att loggen prövades."
   - Replaces: "Läst utan ingress sade brödtexten aldrig att loggen prövades." Only "sade" becomes "sa".
   - Called for by `check.md`: no.
   - Contradicted by the text: no. The body text of `input.md` speaks of "Försöket", "försöksanteckning" and "göra försöket igen", but never says that the log was what was being trialled.

8. "Inledningens första mening säger nu att underhållsgruppen prövade loggen."
   - Replaces: "Därför säger inledningens första mening nu att underhållsgruppen prövade loggen." The word "Därför" is dropped.
   - Called for by `check.md`: no.
   - Contradicted by the text: no. `delivered.md` line 7 reads: "Underhållsgruppen på Elm Quay Housing prövade sin gemensamma reparationslogg".

9. "Konstruktionen ”Att se … var vad … ville få ut av …” är formad efter engelska och gjorde brödtextens öppning tung och översättningsaktig."
   - Replaces: "Den engelskformade konstruktionen ”Att se … var vad … ville få ut av …” gjorde brödtextens öppning tung och översättningsaktig."
   - Called for by `check.md`: no.
   - Contradicted by the text: no. The elided quotation matches `input.md` line 7. The rest is a judgement of quality.

10. "Den är nu en rak huvudsats med underhållsgruppen som subjekt."
    - Replaces: "Nu är den en rak huvudsats med underhållsgruppen som subjekt."
    - Called for by `check.md`: no.
    - Contradicted by the text: no. "Underhållsgruppen på Elm Quay Housing prövade …" is a main clause, and "Underhållsgruppen" is its subject.

11. "Tidigare sa inledningen att underhållsgruppen ville få ut samma information över skiftgränserna ur sin gemensamma reparationslogg."
    - Replaces: "Inledningen sade tidigare att underhållsgruppen ville få samma information över skiftgränserna ut av sin gemensamma reparationslogg."
    - Called for by `check.md`: no.
    - Contradicted by the text: no. `input.md` reads "Att se samma information över skiftgränserna var vad underhållsgruppen … ville få ut av sin gemensamma reparationslogg." Both the draft and the response paraphrase "att se" (to see) as getting the information out. The reword does not change what the statement says.

12. "Inledningen säger också att det var underhållsgruppen som prövade den, medan ingressen säger att Elm Quay Housing gjorde det."
    - Replaces: "Det är också underhållsgruppen som prövade den, medan ingressen säger att Elm Quay Housing gjorde det."
    - Called for by `check.md`: no.
    - Contradicted by the text: no.
      - The lead in `delivered.md` reads "Underhållsgruppen … prövade sin gemensamma reparationslogg".
      - The standfirst reads "Elm Quay Housing provade en gemensam reparationslogg".
    - The new wording names which passage says it, and that is more exact than the draft.

13. "Mätskriptet godkänner den levererade texten: rubriken har 59 tecken och ingressen 41 ord."
    - Replaces: "Skriptets räknade krav håller i den levererade texten: rubriken har 59 tecken och ingressen 41 ord."
    - Called for by `check.md`: no.
    - Contradicted by the text: no.
      - The headline "Gemensam ärendebild hjälper, säger Elm Quay om loggförsöket" has 59 characters.
      - The standfirst in `delivered.md` has 41 words.
    - Whether the script passed the text is about the run, not about either text.

14. "De krav som skriptet inte räknar har jag kontrollerat genom läsning: ingressen står på egen hand / inledningen presenterar allt den nämner / mellanrubrikerna beskriver sina avsnitt / sista avsnittet är ett avslut med en uppmaning till läsaren."
    - Replaces: "Kraven som skriptet inte räknar har granskats genom läsning: att ingressen står på egen hand, att inledningen introducerar det den nämner, att mellanrubrikerna beskriver sina avsnitt och att sista avsnittet är ett avslut med en uppmaning till läsaren."
    - Apart from the list format, the reword makes three changes: the passive becomes "har jag kontrollerat", "introducerar det den nämner" becomes "presenterar allt den nämner", and the "att"-clauses lose their "att".
    - Called for by `check.md`: no.
    - Contradicted by the text: no.
      - In the lead of `delivered.md`, "Försöket" now follows "prövade sin gemensamma reparationslogg", and "gruppens egna anteckningar" follows "Underhållsgruppen".
      - The last section ends with "Den som står inför samma förberedelser kan börja i [Svales checklista för införandet]".
      - The other two requirements are judgements of quality.

15. "Sammanfattat ändrades två slags saker, och båda redovisas ovan."
    - Replaces: "Utöver detta ändrades två saker."
    - Called for by `check.md`: yes, item 1.
    - Contradicted by the text: no. The two changes in the diff are a rebuilt sentence (lead, line 7) and clarified references (standfirst, line 3, and lead, line 7). Both are reported in findings 1–3.

## 3. Made false

none

## 4. Removed

- **"Utöver detta" in "Utöver detta ändrades två saker."** The response no longer says that these changes came in addition to the findings. Removing this was called for by item 1 of `check.md`, and statement 15 replaces it.
- **The causal "Därför" in finding 2.** The draft said the lead's first sentence now says the group trialled the log *because* the body never said so. The response states the two facts without linking them. No item of `check.md` called for this.
- No other statement about either text is missing from `response.md`. All the others survive, either in the draft's words or reworded as listed under heading 2.
