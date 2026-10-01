You are checking one reply against the two texts it describes. You did not write the reply and you did not make the changes it reports; you know only what is below, which is what the reply's own reader will know. Find what the reply gets wrong about the texts, and only that: whether a change was a good one, whether a finding was worth making and how the text reads are questions for somebody else.

**The text as it arrived.** This is the complete text the run received:

````markdown
# Vår fantastiska lösning räddade Elm Quay

**Elm Quay registrerade 31 ärenden. Elm Quay registrerade 31 ärenden.**

Elm Quay registrerade 31 ärenden. Vi på Svale är världsledande på att skapa framgång, och kunden stod hjälplös innan vi kom.

## Kunden fick en gemensam bild

Maya Lind säger att det hjälper att ha en gemensam bild av ärendena.

– Att ha en gemensam bild av ärendena hjälper oss, men jag skulle lägga till en vecka för förberedelser, säger Maya Lind, arbetsledare hos kunden.

## Resultatet bevisar allt

Enligt kundens försöksanteckning registrerades 31 ärenden under åtta veckor, med akuta ärenden undantagna. Tiden till tilldelning var två arbetsdagar jämfört med tre tidigare. Anteckningen säger att arbetsbelastningen var olika och att skillnaden inte kan tillskrivas programvaran. Vår programvara orsakade därför hela förbättringen.

– Jag skulle välja att göra försöket igen, säger Lind.

Kundcaset publiceras av leverantören Svale.
````

**The text as delivered.** This is the complete text the run delivers:

````markdown
# Tilldelningen tog två arbetsdagar i Elm Quays försök

**Kunden Elm Quay registrerade 31 ärenden, akuta ärenden undantagna, under ett åtta veckor långt försök med programvara från leverantören Svale. Tiden till tilldelning blev kortare, men enligt kundens anteckning kan skillnaden inte tillskrivas programvaran.**

Elm Quay förde en anteckning över ärendena under de åtta veckor som kunden provade programvara från leverantören Svale. Den visar hur lång tid det tog innan ärendena tilldelades, och arbetsledaren Maya Lind berättar hur hon ser på försöket.

## Arbetsledaren om ärendena

– Att ha en gemensam bild av ärendena hjälper oss, men jag skulle lägga till en vecka för förberedelser, säger Maya Lind, arbetsledare hos kunden.

## Anteckningen visar kortare tid till tilldelning

Enligt kundens försöksanteckning registrerades 31 ärenden under åtta veckor, med akuta ärenden undantagna. Tiden till tilldelning var två arbetsdagar jämfört med tre tidigare. Anteckningen säger att arbetsbelastningen var olika och att skillnaden inte kan tillskrivas programvaran.

## Maya Lind ser tillbaka på försöket

– Jag skulle välja att göra försöket igen, säger Lind.

Kundcaset publiceras av leverantören Svale.
````

**The reply.** This is everything the run is about to say about the two texts:

````markdown
**Konfiguration:** genre `casestudy` (från anropet), språk `sv` (från anropet), ingen teknik – genren casestudy anger ingen teknik som den vanligen skrivs med. Ingen brief användes. Korrigeringsbudgeten (1) är förbrukad.

[den levererade texten står här, i ett eget kodblock]

## Kvarstående fynd (olösta)

1. **Byline saknas.** Texten, dess metadata och anropet namnger ingen författare, så ingen byline har skrivits. En person behöver ange den.
2. **Uppmaning till handling saknas.** Avslutet uppmanar inte läsaren till något, och texten innehåller inget erbjudande, ingen länk och ingen kontaktväg att bygga en uppmaning av.
3. **Kundbakgrund saknas.** Texten säger inte vad Elm Quay är för verksamhet, vilken sorts ärenden det gäller, vad som föranledde försöket eller hur valen och införandet gick till. Det kan inte fyllas i ur texten.

## Åtgärdade fynd

- **Rubriken** ”Vår fantastiska lösning räddade Elm Quay” drog en orsaksslutsats (”räddade”) som texten själv avvisar, värderade utan stöd (”fantastiska”) och gjorde leverantören till berättare (”Vår”). Den lyder nu ”Tilldelningen tog två arbetsdagar i Elm Quays försök”.
- **Ingressen** bestod av samma mening två gånger, sa inte vad texten handlar om, angav 31 ärenden utan period och undantag och upprepade ingångens första mening ordagrant. Den har skrivits om ur textens eget innehåll.
- **Ingången** innehöll två påståenden utan stöd i texten – att Svale är världsledande och att kunden stod hjälplös – och introducerade varken försöket eller vad läsaren skulle få veta. Påståendena är strukna och ingången introducerar nu försöket, anteckningen och Maya Lind.
- **Första underrubriken** ”Kunden fick en gemensam bild” och meningen före citatet (”Maya Lind säger att det hjälper att ha en gemensam bild av ärendena.”) sa båda citatets poäng i förväg. Meningen före citatet är struken – namn och roll står redan i anföringen – och underrubriken lyder nu ”Arbetsledaren om ärendena”, som namnger talaren och ämnet och lämnar poängen åt citatet.
- **Andra underrubriken** ”Resultatet bevisar allt” påstod mer än avsnittet, som säger att skillnaden inte kan tillskrivas programvaran, och i högre ton än texten. Den lyder nu ”Anteckningen visar kortare tid till tilldelning”.
- **Meningen** ”Vår programvara orsakade därför hela förbättringen.” drog en orsaksslutsats som motsägs av meningen omedelbart före. Den är struken.
- **Avslutet:** Linds omdöme och raden om att Svale publicerar kundcaset stod i avsnittet som redovisar resultatet, så texten saknade ett avslut som eget avsnitt. De står nu oförändrade i ett eget sista avsnitt under den nya underrubriken ”Maya Lind ser tillbaka på försöket”.

**Artikelanatomin:** Den levererade texten har en rubrik på 52 tecken och 8 ord och en ingress på 34 ord. Den enda räknade avvikelsen är att byline saknas. Av de krav som inte räknas har jag läst om ingressen står på egen hand, om underrubrikerna beskriver sina avsnitt och om sista avsnittet är ett avslut. Texten följer ändå inte anatomin fullt ut, eftersom byline och uppmaning till handling saknas.

## Påståenden

**Borttagna**
- ”Vi på Svale är världsledande på att skapa framgång” (ingången). Det togs bort av reparationen av fyndet att påståendet saknar stöd och att leverantören talade i vi-form.
- ”kunden stod hjälplös innan vi kom” (ingången). Det togs bort av reparationen av fyndet om en räddningsberättelse utan stöd.
- ”Vår programvara orsakade därför hela förbättringen.” (resultatavsnittet). Det togs bort av reparationen av fyndet om en orsaksslutsats som motsägs av texten. Meningen om att arbetsbelastningen var olika och att skillnaden inte kan tillskrivas programvaran står kvar ordagrant.
- Meningen före första citatet är struken, men det den sa – att det hjälper att ha en gemensam bild av ärendena – står kvar i Maya Linds citat.

**Ändrade**
- **Rubriken** påstår nu att tilldelningen tog två arbetsdagar i Elm Quays försök. Den påstår inte längre att leverantörens lösning räddade kunden eller att lösningen var fantastisk (rubrikreparationen).
- **Ingressen** påstår nu att kunden Elm Quay registrerade 31 ärenden, akuta ärenden undantagna, under ett åtta veckor långt försök med programvara från Svale, att tiden till tilldelning blev kortare, och att skillnaden enligt kundens anteckning inte kan tillskrivas programvaran (ingressreparationen).
- **Ingången** påstår inte längre att Elm Quay registrerade 31 ärenden; det står kvar i ingressen och i resultatavsnittet. Den säger nu att Elm Quay förde en anteckning över ärendena under de åtta veckor som kunden provade Svales programvara, att anteckningen visar hur lång tid det tog innan ärendena tilldelades, och att arbetsledaren Maya Lind berättar hur hon ser på försöket (ingångsreparationen).
- **Första underrubriken** påstod att kunden fick en gemensam bild. Nu är den en etikett som namnger talaren och ämnet och påstår ingenting om utfallet (reparationen av första avsnittet).
- **Andra underrubriken** påstod att resultatet bevisar allt. Nu påstår den att anteckningen visar kortare tid till tilldelning (reparationen av andra underrubriken).

**Tillagda**
- Att försöket gällde programvara från leverantören Svale står nu uttryckligen i ingressen och ingången. Det är en slutledning ur ”Vi på Svale”, ”Vår programvara” och meningen om att skillnaden inte kan tillskrivas programvaran (ingress- och ingångsreparationerna).
- Den nya tredje underrubriken ”Maya Lind ser tillbaka på försöket” ramar in det sista avsnittet som Linds återblick på försöket (avslutsreparationen).

Utöver det ovanstående har körningen strukit leverantörens vi-form och reklamfraserna, tagit bort upprepningar (ingressens dubbla mening och meningen före det första citatet), skrivit om rubriken och underrubrikerna och gett avslutet ett eget avsnitt. Den avslutande mekaniska korrekturen hittade inget att rätta.
````

**The measurement of the delivered text.** This is the full output of the collection's measuring script, run on the delivered text. A count or length the reply states about the delivered text is read against it:

```json
{
  "ok": true,
  "format": "markdown",
  "conforms": false,
  "failures": [
    {
      "part": "byline",
      "rule": "A text conforms when every part is present in the order shown.",
      "measured": "absent",
      "text": null
    }
  ],
  "norms": [],
  "typical": {
    "paragraphs": 6,
    "paragraphs_of_two_or_three_sentences": 3,
    "sections": 3,
    "sections_of_two_or_three_paragraphs": 1
  },
  "parts": {
    "headline": {
      "text": "Tilldelningen tog två arbetsdagar i Elm Quays försök",
      "characters": 52,
      "words": 8
    },
    "standfirst": {
      "text": "Kunden Elm Quay registrerade 31 ärenden, akuta ärenden …",
      "words": 34,
      "sentences_estimate": 2,
      "paragraphs": 1
    },
    "byline": null,
    "lead": {
      "text": "Elm Quay förde en anteckning över ärendena under …",
      "words": 38,
      "sentences_estimate": 2,
      "paragraphs": 1
    },
    "sections": [
      {
        "subheading": {
          "text": "Arbetsledaren om ärendena",
          "characters": 25,
          "words": 3
        },
        "paragraphs": [
          {
            "text": "– Att ha en gemensam bild av ärendena …",
            "words": 24,
            "sentences_estimate": 1
          }
        ]
      },
      {
        "subheading": {
          "text": "Anteckningen visar kortare tid till tilldelning",
          "characters": 47,
          "words": 6
        },
        "paragraphs": [
          {
            "text": "Enligt kundens försöksanteckning registrerades 31 ärenden under åtta …",
            "words": 36,
            "sentences_estimate": 3
          }
        ]
      },
      {
        "subheading": {
          "text": "Maya Lind ser tillbaka på försöket",
          "characters": 34,
          "words": 6
        },
        "paragraphs": [
          {
            "text": "– Jag skulle välja att göra försöket igen, …",
            "words": 9,
            "sentences_estimate": 1
          },
          {
            "text": "Kundcaset publiceras av leverantören Svale.",
            "words": 5,
            "sentences_estimate": 1
          }
        ]
      }
    ],
    "other": []
  },
  "heading_pairs": [
    {
      "id": "headline-standfirst",
      "kind": "headline-standfirst",
      "heading": "Tilldelningen tog två arbetsdagar i Elm Quays försök",
      "following": "Kunden Elm Quay registrerade 31 ärenden, akuta ärenden undantagna, under ett åtta veckor långt försök med programvara från leverantören Svale. Tiden till tilldelning blev kortare, men enligt kundens anteckning kan skillnaden inte tillskrivas programvaran.",
      "shared_words": [
        "elm",
        "försök"
      ]
    },
    {
      "id": "subheading-1",
      "kind": "subheading-first-sentence-estimate",
      "heading": "Arbetsledaren om ärendena",
      "following": "– Att ha en gemensam bild av ärendena hjälper oss, men jag skulle lägga till en vecka för förberedelser, säger Maya Lind, arbetsledare hos kunden.",
      "shared_words": [
        "ärendena"
      ]
    },
    {
      "id": "subheading-2",
      "kind": "subheading-first-sentence-estimate",
      "heading": "Anteckningen visar kortare tid till tilldelning",
      "following": "Enligt kundens försöksanteckning registrerades 31 ärenden under åtta veckor, med akuta ärenden undantagna.",
      "shared_words": []
    },
    {
      "id": "subheading-3",
      "kind": "subheading-first-sentence-estimate",
      "heading": "Maya Lind ser tillbaka på försöket",
      "following": "– Jag skulle välja att göra försöket igen, säger Lind.",
      "shared_words": [
        "försöket",
        "lind"
      ]
    }
  ]
}
```

**The duties the reply is held to.** Before you read the reply, read two passages and apply them as written: the section *The truth of a report about the text* in `/private/var/folders/cs/vgp_x_353zd9frkjpysp7zdw0000gn/T/kntnt-editorial-388-run-saqtsm__/home/.claude/skills/kntnt/library/references/delivery.md`, and the sentences of `/private/var/folders/cs/vgp_x_353zd9frkjpysp7zdw0000gn/T/kntnt-editorial-388-run-saqtsm__/home/.claude/skills/kntnt/library/references/editorial/base.review.md` that say what the claim account holds, from *A claim removed because the finding named that claim itself* to the end of that paragraph. Read nothing else of either file, and no other file.

**First compare the two texts yourself**, passage by passage, frontmatter and headings included, and note every difference, before you read what the reply says about them. The reply's own account is what you are checking, so it is never how you find a difference.

**Then return two lists.**

1. **False statements.** Every statement of the reply that the text it names contradicts, read as *The truth of a report about the text* reads it: a statement about the text as it arrived against that text, and every other statement against the delivered text. A finding's description of a passage, a count, a length, a grammatical label, where a passage stands, what a round did to a passage, a statement that something holds everywhere or nowhere, and every entry and sentence of the claim account are statements the text can contradict. A judgement of quality — that a heading was vague, that a passage read as filler — is not. For each: quote the statement, name the text it is about, quote the passage that contradicts it, and say what is true.
2. **Claim changes the account misses.** Every difference between the two texts that moves a claim and that the claim account leaves out, or reports short of what it did: scope narrowed or widened; a condition, a qualification, a limit or a connective lost; chronology, causality or attribution moved; or the meaning moved, a sense or a double sense lost and an actor, an ordering or a framing added among it. A headline, a standfirst and a subheading carry claims like any other passage. For each: quote the passage before and after, say what the difference did to the claim, and quote what the account says of it, or say that it says nothing.

Write `none` under a list with nothing on it. Return the two lists and nothing else, and write no file.