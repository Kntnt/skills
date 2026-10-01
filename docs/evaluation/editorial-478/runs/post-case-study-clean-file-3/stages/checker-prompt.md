You are checking one reply against the two texts it describes. You did not write the reply and you did not make the changes it reports; you know only what is below, which is what the reply's own reader will know. Find what the reply gets wrong about the texts, and only that: whether a change was a good one, whether a finding was worth making and how the text reads are questions for somebody else.

**The text as it arrived.** This is the complete text the run received:

````markdown
# Gemensam ärendebild hjälper, säger Elm Quay om loggförsöket

**Elm Quay Housing provade en gemensam reparationslogg i två hus under åtta veckor. Arbetsledaren Maya Lind vill göra om försöket, men skulle avsätta mer tid för förberedelser. Här är vad gruppen gjorde, vad anteckningarna visar och vad hon skulle ändra.**

Text: Iris Falk

Att se samma information över skiftgränserna var vad underhållsgruppen på Elm Quay Housing ville få ut av sin gemensamma reparationslogg. Försöket pågick i åtta veckor och omfattade två hus. Vad det krävde, och vad det gav, går att följa i gruppens egna anteckningar.

## Gruppen enades om kategorierna först

Kategorierna i loggen var underhållsgruppens egna. Leverantören Svale konfigurerade loggen efter dem och utbildade sex medarbetare.

– Vi lade mer tid på att enas om kategorierna än på att lägga in de första ärendena. Den tiden skulle jag avsätta innan nästa hus börjar, säger Maya Lind, arbetsledare på Elm Quay.

## Två perioder med olika arbetsbelastning

Enligt Elm Quays interna försöksanteckning från den 4 december 2025 registrerades 31 ärenden under åtta veckor. Akuta ärenden och tidigare beställda arbeten ingick inte. Mediantiden från anmälan till tilldelning var två arbetsdagar. Under de föregående åtta veckorna var den tre.

Perioderna hade olika arbetsbelastning, och anteckningen tillskriver därför inte skillnaden programvaran.

## Arbetsledaren ser tillbaka på försöket

– Jag skulle välja att göra försöket igen. Att ha en gemensam bild av ärendena hjälper oss, men jag skulle lägga till en vecka för förberedelser, säger Lind.

Kundcaset publiceras av leverantören Svale. Den som står inför samma förberedelser kan börja i [Svales checklista för införandet](https://example.invalid/svale/checklist).
````

**The text as delivered.** This is the complete text the run delivers:

````markdown
# Gemensam ärendebild hjälper, säger Elm Quays arbetsledare om loggen

**Elm Quay Housing provade en gemensam reparationslogg i två hus under åtta veckor. Arbetsledaren Maya Lind vill göra om försöket, men skulle avsätta mer tid för förberedelser. Här är vad Elm Quays underhållsgrupp gjorde, vad gruppens anteckningar visar och vad hon skulle ändra.**

Text: Iris Falk

Underhållsgruppen på Elm Quay Housing ville kunna se samma information över skiftgränserna i sin gemensamma reparationslogg. Försöket pågick i åtta veckor och omfattade två hus. Vad det krävde, och vad det gav, går att följa i gruppens egna anteckningar.

## Gruppen enades om kategorierna först

Kategorierna i loggen var underhållsgruppens egna. Leverantören Svale konfigurerade loggen efter dem och utbildade sex medarbetare.

– Vi lade mer tid på att enas om kategorierna än på att lägga in de första ärendena. Den tiden skulle jag avsätta innan nästa hus börjar, säger Maya Lind, arbetsledare på Elm Quay.

## Två perioder med olika arbetsbelastning

Enligt Elm Quays interna försöksanteckning från den 4 december 2025 registrerades 31 ärenden under åtta veckor. Akuta ärenden och tidigare beställda arbeten ingick inte. Mediantiden från anmälan till tilldelning var två arbetsdagar. Under de föregående åtta veckorna var den tre.

Perioderna hade olika arbetsbelastning, och anteckningen tillskriver därför inte skillnaden programvaran.

## Arbetsledaren ser tillbaka på försöket

– Jag skulle välja att göra försöket igen. Att ha en gemensam bild av ärendena hjälper oss, men jag skulle lägga till en vecka för förberedelser, säger Lind.

Kundcaset publiceras av leverantören Svale. Den som står inför samma förberedelser kan börja i [Svales checklista för införandet](https://example.invalid/svale/checklist).
````

**The reply.** This is everything the run is about to say about the two texts:

````text
Texten är levererad till `output.md`.

Konfiguration: genre `casestudy` och språk `sv`, båda angivna i anropet. Ingen teknik tillämpades: genren casestudy anger ingen teknik som den vanligtvis skrivs med, och ingen annan nivå valde någon. Ingen skrivbrief användes.

## Fynd

Alla tre fynden åtgärdades i en korrigeringsrunda, och inga fynd kvarstår.

1. **Rubriken** tillskrev omdömet Elm Quay som organisation ("säger Elm Quay om loggförsöket"), medan texten bara har en namngiven persons bedömning – arbetsledaren Maya Lind, som dessutom gör en reservation om förberedelsetiden. Den som bara ser rubriken uppfattade ett ställningstagande från bostadsbolaget. Rubriken lyder nu "Gemensam ärendebild hjälper, säger Elm Quays arbetsledare om loggen".
2. **Ingressens sista mening**, "Här är vad gruppen gjorde, vad anteckningarna visar och vad hon skulle ändra", använde "gruppen" och "anteckningarna" i bestämd form utan att ingressen hade introducerat dem, så ingressen var inte självbärande. Den lyder nu "Här är vad Elm Quays underhållsgrupp gjorde, vad gruppens anteckningar visar och vad hon skulle ändra."
3. **Inledningens första mening** var en engelskklingande pseudoklyvning ("Att se samma information över skiftgränserna var vad underhållsgruppen … ville få ut av …") som sköt upp aktören bakom en tung infinitivfras. Nu börjar meningen med aktören: "Underhållsgruppen på Elm Quay Housing ville kunna se samma information över skiftgränserna i sin gemensamma reparationslogg."

## Påståenden

Ändrade:

- **Rubriken** (fynd 1): omdömet att en gemensam ärendebild hjälper tillskrivs nu Elm Quays arbetsledare i stället för Elm Quay. Rubriken säger också att omdömet gäller "loggen" i stället för "loggförsöket", så den som bara läser rubriken får inte längre veta att det rörde sig om ett försök. Att det var ett åttaveckorsförsök i två hus står kvar i ingressen och inledningen.
- **Ingressens sista mening** (fynd 2): anteckningarna som resultaten kommer från tillskrivs nu uttryckligen underhållsgruppen ("gruppens anteckningar"), som inledningen redan gjorde ("gruppens egna anteckningar"). Avsnittet om resultaten hänvisar till "Elm Quays interna försöksanteckning".
- **Inledningens första mening** (fynd 3): gruppen ville kunna se samma information över skiftgränserna i sin reparationslogg. Den tidigare konstruktionen framhöll att det var just detta gruppen ville få ut av loggen; den betoningen är borta.

Inga påståenden togs bort och inga lades till.

## Artikelanatomin

Rubriken följer inte längre två bör-normer: den har 9 ord (normen är tre till åtta) och 67 tecken (normen är högst 60). Kravet på 20–70 tecken uppfylls. Avvikelsen behölls eftersom ingen rubrik inom normerna rymde både den exakta attribueringen, kundens namn och ämnet. Mätskriptet godkänner alla räknade krav i den levererade texten, och de krav det inte räknar granskades genom läsning: ordningen mellan delarna, att ingressen står på egna ben, att inledningen klarar sig utan ingressen, att mellanrubrikerna beskriver sina avsnitt och att sista avsnittet är ett avslut med en uppmaning. Texten följer artikelanatomin, med avvikelse från de två rubriknormerna.

## Vad körningen ändrade

Körningen ändrade rubriken, ingressens sista mening och inledningens första mening; resten av texten är oförändrad. Den avslutande korrekturläsningen hittade inga mekaniska fel och ändrade ingenting.
````

**The measurement of the delivered text.** This is the full output of the collection's measuring script, run on the delivered text. A count or length the reply states about the delivered text is read against it:

```json
{"ok":true,"format":"markdown","conforms":true,"failures":[],"norms":[{"part":"headline","rule":"It should be three to eight words.","measured":"9 words","text":"Gemensam ärendebild hjälper, säger Elm Quays arbetsledare om loggen"},{"part":"headline","rule":"It should be at most 60 characters.","measured":"67 characters","text":"Gemensam ärendebild hjälper, säger Elm Quays arbetsledare om loggen"}],"typical":{"paragraphs":8,"paragraphs_of_two_or_three_sentences":6,"sections":3,"sections_of_two_or_three_paragraphs":3},"parts":{"headline":{"text":"Gemensam ärendebild hjälper, säger Elm Quays arbetsledare om loggen","characters":67,"words":9},"standfirst":{"text":"Elm Quay Housing provade en gemensam reparationslogg i …","words":43,"sentences_estimate":3,"paragraphs":1},"byline":{"text":"Text: Iris Falk","words":3},"lead":{"text":"Underhållsgruppen på Elm Quay Housing ville kunna se …","words":39,"sentences_estimate":3,"paragraphs":1},"sections":[{"subheading":{"text":"Gruppen enades om kategorierna först","characters":36,"words":5},"paragraphs":[{"text":"Kategorierna i loggen var underhållsgruppens egna. Leverantören Svale …","words":16,"sentences_estimate":2},{"text":"– Vi lade mer tid på att enas …","words":33,"sentences_estimate":2}]},{"subheading":{"text":"Två perioder med olika arbetsbelastning","characters":39,"words":5},"paragraphs":[{"text":"Enligt Elm Quays interna försöksanteckning från den 4 …","words":40,"sentences_estimate":4},{"text":"Perioderna hade olika arbetsbelastning, och anteckningen tillskriver därför …","words":11,"sentences_estimate":1}]},{"subheading":{"text":"Arbetsledaren ser tillbaka på försöket","characters":38,"words":5},"paragraphs":[{"text":"– Jag skulle välja att göra försöket igen. …","words":27,"sentences_estimate":2},{"text":"Kundcaset publiceras av leverantören Svale. Den som står …","words":18,"sentences_estimate":2}]}],"other":[]},"heading_pairs":[{"id":"headline-standfirst","kind":"headline-standfirst","heading":"Gemensam ärendebild hjälper, säger Elm Quays arbetsledare om loggen","following":"Elm Quay Housing provade en gemensam reparationslogg i två hus under åtta veckor. Arbetsledaren Maya Lind vill göra om försöket, men skulle avsätta mer tid för förberedelser. Här är vad Elm Quays underhållsgrupp gjorde, vad gruppens anteckningar visar och vad hon skulle ändra.","shared_words":["elm","gemensam","om","quays"]},{"id":"subheading-1","kind":"subheading-first-sentence-estimate","heading":"Gruppen enades om kategorierna först","following":"Kategorierna i loggen var underhållsgruppens egna.","shared_words":["kategorierna"]},{"id":"subheading-2","kind":"subheading-first-sentence-estimate","heading":"Två perioder med olika arbetsbelastning","following":"Enligt Elm Quays interna försöksanteckning från den 4 december 2025 registrerades 31 ärenden under åtta veckor.","shared_words":[]},{"id":"subheading-3","kind":"subheading-first-sentence-estimate","heading":"Arbetsledaren ser tillbaka på försöket","following":"– Jag skulle välja att göra försöket igen.","shared_words":["försöket"]}]}
```

(The four-backtick and three-backtick fences above only delimit the material; they are not part of it.)

**The duties the reply is held to.** Before you read the reply, read two passages and apply them as written: the section *The truth of a report about the text* in `/private/var/folders/cs/vgp_x_353zd9frkjpysp7zdw0000gn/T/kntnt-editorial-388-run-esqsdm2y/home/.claude/skills/kntnt/library/references/delivery.md`, and the sentences of `/private/var/folders/cs/vgp_x_353zd9frkjpysp7zdw0000gn/T/kntnt-editorial-388-run-esqsdm2y/home/.claude/skills/kntnt/library/references/editorial/base.review.md` that say what the claim account holds, from *A claim removed because the finding named that claim itself* to the end of that paragraph. Read nothing else of either file, and no other file.

**First compare the two texts yourself**, passage by passage, frontmatter and headings included, and note every difference, before you read what the reply says about them. The reply's own account is what you are checking, so it is never how you find a difference.

**Then return two lists.**

1. **False statements.** Every statement of the reply that the text it names contradicts, read as *The truth of a report about the text* reads it: a statement about the text as it arrived against that text, and every other statement against the delivered text. A finding's description of a passage, a count, a length, a grammatical label, where a passage stands, what a round did to a passage, a statement that something holds everywhere or nowhere, and every entry and sentence of the claim account are statements the text can contradict. A judgement of quality — that a heading was vague, that a passage read as filler — is not. For each: quote the statement, name the text it is about, quote the passage that contradicts it, and say what is true.
2. **Claim changes the account misses.** Every difference between the two texts that moves a claim and that the claim account leaves out, or reports short of what it did: scope narrowed or widened; a condition, a qualification, a limit or a connective lost; chronology, causality or attribution moved; or the meaning moved, a sense or a double sense lost and an actor, an ordering or a framing added among it. A headline, a standfirst and a subheading carry claims like any other passage. A sentence that says whose a body of content is — that a person tells it, that a document shows it — carries an attribution for all of that content, wherever the content itself stands: where the delivered text gives a person or a source content that the text as it arrived gave to another voice, the narrator's own among them, the attribution has moved even though every fact still stands where it stood. A statement on your first list that gets wrong whose a passage's content is may have a change built on it: read what the delivered text now says about whose that content is, and put that change on this list where the account reports it short. For each: quote the passage before and after, say what the difference did to the claim — for a moved attribution, who the text gave which content to before and whom it gives it to now — and quote what the account says of it, or say that it says nothing. An entry that names one of the voices a moved attribution took content from, and leaves out another, reports it short.

Write `none` under a list with nothing on it. Return the two lists and nothing else, and write no file.