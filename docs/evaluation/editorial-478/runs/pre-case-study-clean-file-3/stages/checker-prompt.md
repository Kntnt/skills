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
# Gemensam ärendebild hjälper, säger Elm Quay om loggförsöket

**Elm Quay Housing provade en gemensam reparationslogg i två hus under åtta veckor. Arbetsledaren Maya Lind vill göra om försöket, men skulle avsätta mer tid för förberedelser. Här är vad gruppen gjorde, vad anteckningarna visar och vad hon skulle ändra.**

Text: Iris Falk

Underhållsgruppen på Elm Quay Housing gjorde ett försök med en gemensam reparationslogg och ville att den skulle visa samma information över skiftgränserna. Försöket pågick i åtta veckor och omfattade två hus. Vad det krävde, och vad det gav, går att följa i gruppens egna anteckningar.

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

(The fences above only delimit the texts; they are not part of them.)

**The reply.** This is everything the run is about to say about the two texts:

````text
Granskad text är skriven till output.md.

Konfiguration: genre casestudy och språk sv, båda från anropet. Ingen teknik: anropet angav ingen, och genren casestudy anger att den inte skrivs med någon teknik. Korrigeringsbudgeten (1) användes till en korrigeringsrunda.

Fynd – båda åtgärdade, inga kvarstår:

1. Inledningsstyckets första mening, ”Att se samma information över skiftgränserna var vad underhållsgruppen på Elm Quay Housing ville få ut av sin gemensamma reparationslogg.”, var byggd som en engelsk pseudoklyvning: en framflyttad infinitivfras med ny information stod först, och först därefter fick läsaren veta vem som ville något. Brödtextens första mening lästes därför som översatt. Åtgärd: meningen börjar nu med underhållsgruppen, sedan loggen och sist målet.

2. Inledningsstyckets andra mening, ”Försöket pågick i åtta veckor och omfattade två hus.”, använde bestämd form, ”Försöket”, fast bara ingressen hade sagt att loggen provades i ett försök. Den som läser brödtexten utan ingressen fick inte veta att loggen var ett tidsbegränsat försök. Åtgärd: inledningsstycket säger nu självt att gruppen gjorde ett försök med loggen. Meningen om försöket står kvar ordagrant.

Påståenderedovisning:

- Ändrat påstående (fynd 1): Gruppens mål uttrycks nu som att gruppen ”ville att den [loggen] skulle visa samma information över skiftgränserna”. Tidigare var målet att se samma information över skiftgränserna, och det var vad gruppen ville ”få ut av” loggen. Nu är det loggen som ska visa informationen, och ”sin gemensamma reparationslogg” har blivit ”en gemensam reparationslogg”.
- Påstående som nu står i brödtexten (fynd 2): Inledningsstycket säger nu att underhållsgruppen på Elm Quay Housing ”gjorde ett försök med en gemensam reparationslogg”. I den mottagna texten sa bara ingressen detta (”Elm Quay Housing provade …”), med företaget som aktör. Brödtexten förutsatte det med ”Försöket”.
- Inget påstående har tagits bort. Ingen begränsning har försvunnit: meningarna om att akuta ärenden och tidigare beställda arbeten inte ingick och om att anteckningen inte tillskriver skillnaden programvaran står kvar ordagrant. Utöver de två posterna ovan har inget påstående ändrats eller lagts till.

Artikelanatomi: texten uppfyller anatomin utan avvikelse. Den levererade texten mättes efter den avslutande korrekturläsningen. Rubriken har 59 tecken, ingressen 40 ord och inledningsstycket 45 ord, och inget räknat krav brister. De krav som skriptet inte räknar har också granskats: att ingressen står på egen hand, att inledningsstycket varken upprepar ingressen eller pekar tillbaka på den, att mellanrubrikerna beskriver sina avsnitt och att sista avsnittet är ett avslut med en uppmaning som följer av innehållet.

Utöver påståendena ovan skrev körningen om en enda mening, inledningsstyckets första: aktören står nu först och försöket nämns i brödtexten. Den avslutande korrekturläsningen hittade inga mekaniska fel och ändrade ingenting. Rubrik, ingress, byline, mellanrubriker, citat och övriga stycken är oförändrade.
````

**The measurement of the delivered text.** This is the full output of the collection's measuring script, run on the delivered text. A count or length the reply states about the delivered text is read against it:

```json
{
  "ok": true,
  "format": "markdown",
  "conforms": true,
  "failures": [],
  "norms": [],
  "typical": {
    "paragraphs": 8,
    "paragraphs_of_two_or_three_sentences": 6,
    "sections": 3,
    "sections_of_two_or_three_paragraphs": 3
  },
  "parts": {
    "headline": {"text": "Gemensam ärendebild hjälper, säger Elm Quay om loggförsöket", "characters": 59, "words": 8},
    "standfirst": {"text": "Elm Quay Housing provade en gemensam reparationslogg i …", "words": 40, "sentences_estimate": 3, "paragraphs": 1},
    "byline": {"text": "Text: Iris Falk", "words": 3},
    "lead": {"text": "Underhållsgruppen på Elm Quay Housing gjorde ett försök …", "words": 45, "sentences_estimate": 3, "paragraphs": 1},
    "sections": [
      {"subheading": {"text": "Gruppen enades om kategorierna först", "characters": 36, "words": 5},
       "paragraphs": [{"text": "Kategorierna i loggen var underhållsgruppens egna. Leverantören Svale …", "words": 16, "sentences_estimate": 2},
                      {"text": "– Vi lade mer tid på att enas …", "words": 33, "sentences_estimate": 2}]},
      {"subheading": {"text": "Två perioder med olika arbetsbelastning", "characters": 39, "words": 5},
       "paragraphs": [{"text": "Enligt Elm Quays interna försöksanteckning från den 4 …", "words": 40, "sentences_estimate": 4},
                      {"text": "Perioderna hade olika arbetsbelastning, och anteckningen tillskriver därför …", "words": 11, "sentences_estimate": 1}]},
      {"subheading": {"text": "Arbetsledaren ser tillbaka på försöket", "characters": 38, "words": 5},
       "paragraphs": [{"text": "– Jag skulle välja att göra försöket igen. …", "words": 27, "sentences_estimate": 2},
                      {"text": "Kundcaset publiceras av leverantören Svale. Den som står …", "words": 18, "sentences_estimate": 2}]}
    ],
    "other": []
  },
  "heading_pairs": [
    {"id": "headline-standfirst", "kind": "headline-standfirst", "heading": "Gemensam ärendebild hjälper, säger Elm Quay om loggförsöket", "following": "Elm Quay Housing provade en gemensam reparationslogg i två hus under åtta veckor. Arbetsledaren Maya Lind vill göra om försöket, men skulle avsätta mer tid för förberedelser. Här är vad gruppen gjorde, vad anteckningarna visar och vad hon skulle ändra.", "shared_words": ["elm", "gemensam", "om", "quay"]},
    {"id": "subheading-1", "kind": "subheading-first-sentence-estimate", "heading": "Gruppen enades om kategorierna först", "following": "Kategorierna i loggen var underhållsgruppens egna.", "shared_words": ["kategorierna"]},
    {"id": "subheading-2", "kind": "subheading-first-sentence-estimate", "heading": "Två perioder med olika arbetsbelastning", "following": "Enligt Elm Quays interna försöksanteckning från den 4 december 2025 registrerades 31 ärenden under åtta veckor.", "shared_words": []},
    {"id": "subheading-3", "kind": "subheading-first-sentence-estimate", "heading": "Arbetsledaren ser tillbaka på försöket", "following": "– Jag skulle välja att göra försöket igen.", "shared_words": ["försöket"]}
  ]
}
```

**The duties the reply is held to.** Before you read the reply, read two passages and apply them as written: the section *The truth of a report about the text* in `/private/var/folders/cs/vgp_x_353zd9frkjpysp7zdw0000gn/T/kntnt-editorial-388-run-9zzi_y6e/home/.claude/skills/kntnt/library/references/delivery.md`, and the sentences of `/private/var/folders/cs/vgp_x_353zd9frkjpysp7zdw0000gn/T/kntnt-editorial-388-run-9zzi_y6e/home/.claude/skills/kntnt/library/references/editorial/base.review.md` that say what the claim account holds, from *A claim removed because the finding named that claim itself* to the end of that paragraph. Read nothing else of either file, and no other file.

**First compare the two texts yourself**, passage by passage, frontmatter and headings included, and note every difference, before you read what the reply says about them. The reply's own account is what you are checking, so it is never how you find a difference.

**Then return two lists.**

1. **False statements.** Every statement of the reply that the text it names contradicts, read as *The truth of a report about the text* reads it: a statement about the text as it arrived against that text, and every other statement against the delivered text. A finding's description of a passage, a count, a length, a grammatical label, where a passage stands, what a round did to a passage, a statement that something holds everywhere or nowhere, and every entry and sentence of the claim account are statements the text can contradict. A judgement of quality — that a heading was vague, that a passage read as filler — is not. For each: quote the statement, name the text it is about, quote the passage that contradicts it, and say what is true.
2. **Claim changes the account misses.** Every difference between the two texts that moves a claim and that the claim account leaves out, or reports short of what it did: scope narrowed or widened; a condition, a qualification, a limit or a connective lost; chronology, causality or attribution moved; or the meaning moved, a sense or a double sense lost and an actor, an ordering or a framing added among it. A headline, a standfirst and a subheading carry claims like any other passage. For each: quote the passage before and after, say what the difference did to the claim, and quote what the account says of it, or say that it says nothing.

Write `none` under a list with nothing on it. Return the two lists and nothing else, and write no file.