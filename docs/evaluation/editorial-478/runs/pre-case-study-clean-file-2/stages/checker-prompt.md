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
# Gemensam ärendebild hjälper gruppen, säger arbetsledaren på Elm Quay

**Elm Quay Housing provade en gemensam reparationslogg i två hus under åtta veckor. Arbetsledaren Maya Lind vill göra om försöket, men skulle avsätta mer tid för förberedelser. Här är vad gruppen gjorde, vad anteckningarna visar och vad hon skulle ändra.**

Text: Iris Falk

Att se samma information över skiftgränserna var vad underhållsgruppen på Elm Quay Housing ville få ut av sin gemensamma reparationslogg. Försöket pågick i åtta veckor och omfattade två hus. Det krävde förberedelser, och hur ärendena registrerades och tilldelades går att följa i en intern försöksanteckning.

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
Den granskade texten är skriven till `output.md`. `input.md` är orörd.

Konfiguration: genren casestudy och språket sv kommer från anropet. Ingen teknik tillämpades, eftersom genren casestudy anger att den vanligen skrivs utan teknik. Ingen skrivbrief användes. Korrigeringsbudgeten var 1 och gick åt till en korrigeringsrunda.

Fynd (båda åtgärdade, inga kvarstår)

1. Rubriken ”Gemensam ärendebild hjälper, säger Elm Quay om loggförsöket” tillskrev organisationen Elm Quay ett omdöme som är arbetsledaren Maya Linds, i hennes citat i sista avsnittet. Den klippte också citatets ”hjälper oss” till ”hjälper”, så att rubriken inte sa vad eller vem den gemensamma bilden hjälper, och ”loggförsöket” förutsatte ett försök som den som bara ser rubriken inte har mött. Läsaren tog en arbetsledares bedömning för bostadsbolagets officiella omdöme. Rubriken är omskriven.

2. Ledets tredje mening, ”Vad det krävde, och vad det gav, går att följa i gruppens egna anteckningar.”, lovade ett utfall som försöket åstadkommit och hänvisade till anteckningarna för det, fast den enda källa brödtexten anger – Elm Quays interna försöksanteckning – uttryckligen inte tillskriver skillnaden i mediantid programvaran. Meningen tillskrev dessutom hela redogörelsen, även vad försöket krävde, ”gruppens egna anteckningar”, medan brödtexten hänvisar till försöksanteckningen enbart för siffrorna. Meningen är omskriven.

Påståendeförteckning

Ändrade påståenden
- Rubriken (fynd 1) påstår nu att arbetsledaren på Elm Quay säger att en gemensam ärendebild hjälper gruppen. Tidigare påstod den att Elm Quay säger att en gemensam ärendebild hjälper, om loggförsöket. Omdömet tillskrivs nu en person i stället för organisationen, och vem det hjälper anges som ”gruppen” – rubrikens tolkning av ”oss” i Linds citat. Den som bara ser rubriken får inte längre veta att texten handlar om ett försök med en logg.
- Ledets tredje mening (fynd 2) påstår nu att försöket krävde förberedelser, utan att hänvisa till några anteckningar för det. Tidigare påstod den att vad försöket krävde går att följa i gruppens egna anteckningar.
- Ledets tredje mening (fynd 2) påstår nu att hur ärendena registrerades och tilldelades går att följa i en intern försöksanteckning. Tidigare angavs källan som ”gruppens egna anteckningar”.

Borttagna påståenden
- ”vad det gav […] går att följa i gruppens egna anteckningar” togs bort av korrigeringen av fynd 2, som pekade ut just det påståendet som bristen. Läsaren av ledet har inte längre löftet att texten visar vad försöket gav. Reservationen ”Perioderna hade olika arbetsbelastning, och anteckningen tillskriver därför inte skillnaden programvaran.” står kvar ordagrant.

Tillagda påståenden: inga.

Utöver rubriken och ledets tredje mening är texten ordagrant densamma som den kom in: ingressen, bylinen, ledets två första meningar, mellanrubrikerna, citaten och övriga stycken är oförändrade.

Artikelanatomin: mätningen av den levererade texten visar att inget räknat krav brister. Rubriken har 68 tecken och 9 ord, vilket ligger inom kravet på 20–70 tecken men över normerna på högst 60 tecken och tre till åtta ord. Rubriken som kom in hade 59 tecken och 8 ord. Överskridandet är inte redovisat som ett fynd: en rubrik inom normerna med samma attribuering skulle behöva släppa kundens namn eller ordet ärendebild. Den som vill hålla normen får korta rubriken själv. De krav som skriptet inte räknar – att ingressen står på egen hand, att ledet introducerar allt det nämner och för texten framåt, att mellanrubrikerna beskriver sina avsnitt och att sista avsnittet är ett avslut med en uppmaning – är granskade, och texten följer anatomin med avvikelse från de två rubriknormerna.

Utöver påståendeförteckningen: rubriken och ledets tredje mening skrevs om för att rätta de två fynden. Den avslutande korrekturläsningen gjorde inga mekaniska ändringar.
````

**The measurement of the delivered text.** This is the full output of the collection's measuring script, run on the delivered text. A count or length the reply states about the delivered text is read against it:

```json
{"ok": true, "format": "markdown", "conforms": true, "failures": [], "norms": [{"part": "headline", "rule": "It should be three to eight words.", "measured": "9 words", "text": "Gemensam ärendebild hjälper gruppen, säger arbetsledaren på Elm Quay"}, {"part": "headline", "rule": "It should be at most 60 characters.", "measured": "68 characters", "text": "Gemensam ärendebild hjälper gruppen, säger arbetsledaren på Elm Quay"}], "parts": {"headline": {"text": "Gemensam ärendebild hjälper gruppen, säger arbetsledaren på Elm Quay", "characters": 68, "words": 9}, "lead": {"words": 45, "sentences_estimate": 3, "paragraphs": 1}}, "note": "abridged by the run to the parts above; the arriving text's headline measured 59 characters and 8 words in an earlier run of the same script"}
```

**The duties the reply is held to.** Before you read the reply, read two passages and apply them as written: the section *The truth of a report about the text* in `/private/var/folders/cs/vgp_x_353zd9frkjpysp7zdw0000gn/T/kntnt-editorial-388-run-szuvvnft/home/.claude/skills/kntnt/library/references/delivery.md`, and the sentences of `/private/var/folders/cs/vgp_x_353zd9frkjpysp7zdw0000gn/T/kntnt-editorial-388-run-szuvvnft/home/.claude/skills/kntnt/library/references/editorial/base.review.md` that say what the claim account holds, from *A claim removed because the finding named that claim itself* to the end of that paragraph. Read nothing else of either file, and no other file.

**First compare the two texts yourself**, passage by passage, frontmatter and headings included, and note every difference, before you read what the reply says about them. The reply's own account is what you are checking, so it is never how you find a difference.

**Then return two lists.**

1. **False statements.** Every statement of the reply that the text it names contradicts, read as *The truth of a report about the text* reads it: a statement about the text as it arrived against that text, and every other statement against the delivered text. A finding's description of a passage, a count, a length, a grammatical label, where a passage stands, what a round did to a passage, a statement that something holds everywhere or nowhere, and every entry and sentence of the claim account are statements the text can contradict. A judgement of quality — that a heading was vague, that a passage read as filler — is not. For each: quote the statement, name the text it is about, quote the passage that contradicts it, and say what is true.
2. **Claim changes the account misses.** Every difference between the two texts that moves a claim and that the claim account leaves out, or reports short of what it did: scope narrowed or widened; a condition, a qualification, a limit or a connective lost; chronology, causality or attribution moved; or the meaning moved, a sense or a double sense lost and an actor, an ordering or a framing added among it. A headline, a standfirst and a subheading carry claims like any other passage. For each: quote the passage before and after, say what the difference did to the claim, and quote what the account says of it, or say that it says nothing.

Write `none` under a list with nothing on it. Return the two lists and nothing else, and write no file.