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
# Elm Quay testade Svales programvara i åtta veckor

**Tiden till tilldelning var två arbetsdagar mot tre tidigare under Elm Quays försök med Svales programvara. Arbetsbelastningen var dock olika, och enligt kundens anteckning kan skillnaden inte tillskrivas programvaran. Arbetsledaren Maya Lind berättar vad som hjälper och vad hon skulle ändra.**

Elm Quay har prövat programvara från leverantören Svale i ett försök under åtta veckor. Kundcaset beskriver vad försöket visade och hur kunden själv bedömer det.

## Arbetsledaren Maya Lind om arbetet med ärendena

– Att ha en gemensam bild av ärendena hjälper oss, men jag skulle lägga till en vecka för förberedelser, säger Maya Lind, arbetsledare hos kunden.

## Snabbare tilldelning som inte kan tillskrivas programvaran

Enligt kundens försöksanteckning registrerades 31 ärenden under åtta veckor, med akuta ärenden undantagna. Tiden till tilldelning var två arbetsdagar jämfört med tre tidigare. Anteckningen säger att arbetsbelastningen var olika och att skillnaden inte kan tillskrivas programvaran.

## Maya Lind ser tillbaka på försöket

– Jag skulle välja att göra försöket igen, säger Lind.

Kundcaset publiceras av leverantören Svale.
````

**The reply.** This is everything the run is about to say about the two texts:

````markdown
**Konfiguration:** genre `casestudy` och språk `sv` (båda från anropet). Ingen teknik: genren casestudy anger att den normalt skrivs utan teknik. Ingen brief användes. Texten har ingen `kntnt`-karta och fick ingen.

## Fynd

**Åtgärdade**

1. **Rubriken** "Vår fantastiska lösning räddade Elm Quay" påstod en räddning och ett orsakssamband som texten inte bär – försöksanteckningen säger att skillnaden inte kan tillskrivas programvaran. Den använde också leverantörens vi-form i berättelsen och en uppblåst värdering, "fantastiska". Rubriken lyder nu "Elm Quay testade Svales programvara i åtta veckor".
2. **Ingressen** bestod av samma mening två gånger, "Elm Quay registrerade 31 ärenden", och samma mening öppnade ingången. Den sade inte vad texten handlar om och gav antalet utan period och undantag. Ingressen är omskriven av textens eget innehåll.
3. **Ingången** innehöll "Vi på Svale är världsledande på att skapa framgång", ett ostött överlägsenhetspåstående i leverantörens vi-form, och "kunden stod hjälplös innan vi kom", en ostödd räddningsberättelse. Båda är borttagna. Ingången presenterar nu försöket och nämner leverantören i tredje person.
4. **Citatbryggan** "Maya Lind säger att det hjälper att ha en gemensam bild av ärendena." sade citatets omdöme i förväg och är borttagen. Talare och roll står kvar i anföringen.
5. **Mellanrubriken** "Kunden fick en gemensam bild" sade i sak och med samma ord vad citatet under den säger. Den lyder nu "Arbetsledaren Maya Lind om arbetet med ärendena".
6. **Mellanrubriken** "Resultatet bevisar allt" påstod motsatsen till avsnittets eget förbehåll. Den lyder nu "Snabbare tilldelning som inte kan tillskrivas programvaran".
7. **Meningen** "Vår programvara orsakade därför hela förbättringen." drog en orsaksslutsats som meningen före uttryckligen avvisar. Den är borttagen. Den avgränsande meningen om arbetsbelastningen och programvaran står kvar oförändrad.
8. **Avslutningen** saknade ett eget avsnitt: kundens avslutande omdöme stod i avsnittet som redovisar resultatet. Det har nu ett eget avsnitt under mellanrubriken "Maya Lind ser tillbaka på försöket". Citatet och raden om att Svale publicerar kundcaset står där oförändrade.

**Olösta**

- **Uppmaningen till handling saknas.** Texten ger inga erbjudanden, länkar eller kontaktvägar att bygga den av, så den är inte skriven.
- **Bylinen saknas.** Ingen författare namnges.
- **Kundbakgrund och genomförande saknas.** Texten säger inte vad Elm Quay är eller gör, vad som föranledde försöket, vad programvaran gör eller hur försöket gick till. Det kräver uppgifter som texten inte har.

Korrigeringsbudgeten (1) är förbrukad, så de olösta fynden lämnas till dig.

Texten uppfyller inte artikelanatomin, eftersom bylinen och uppmaningen till handling saknas. De övriga anatomikraven är granskade och uppfyllda:
- delarnas ordning
- rubrikens längd (49 tecken, 8 ord)
- ingressens längd (41 ord i ett stycke)
- att ingressen står på egen hand och att ingången för läsaren vidare
- vad varje mellanrubrik beskriver
- att det sista avsnittet avslutar texten

## Påståendena

**Borttagna**
- Att Svales lösning räddade Elm Quay, och värderingen "fantastiska" (rubriken, fynd 1).
- "Elm Quay registrerade 31 ärenden": borttagen två gånger ur ingressen (fynd 2) och en gång ur ingången (fynd 3). Antalet står kvar i brödtexten med sin period och sitt undantag.
- "Vi på Svale är världsledande på att skapa framgång" (fynd 3).
- "kunden stod hjälplös innan vi kom" (fynd 3).
- "Maya Lind säger att det hjälper att ha en gemensam bild av ärendena" (fynd 4). Citatet säger fortfarande detta.
- Att kunden fick en gemensam bild (mellanrubriken, fynd 5). Citatet förutsätter fortfarande att de har en.
- "Resultatet bevisar allt" (fynd 6).
- "Vår programvara orsakade därför hela förbättringen" (fynd 7). Med meningen försvann "därför". Läsaren har inte längre påståendet att programvaran orsakade förbättringen eller att det skulle följa av anteckningen.

**Ändrade**
- **Ingressen** (fynd 2) anger nu tilldelningstiden, två arbetsdagar mot tre tidigare, som resultatet under Elm Quays försök med Svales programvara.
  - Att arbetsbelastningen var olika står nu som berättarens eget påstående, inlett med "dock". Brödtexten tillskriver det anteckningen.
  - Att skillnaden inte kan tillskrivas programvaran tillskrivs även i ingressen kundens anteckning.
- **Mellanrubriken över resultatavsnittet** (fynd 6) påstod att resultatet bevisar allt. Den påstår nu, utan anteckningens attribution, att tilldelningen gick snabbare och att skillnaden inte kan tillskrivas programvaran.

**Tillagda**
- Att försöket gjordes med Svales programvara, i rubriken, ingressen och ingången (fynd 1–3). Texten sade det tidigare bara indirekt, genom leverantörens "Vår programvara".
- Att försöket varade åtta veckor, i rubriken och ingången (fynd 1 och 3). Brödtexten säger att 31 ärenden registrerades under åtta veckor enligt försöksanteckningen.
- I ingressen (fynd 2): "Arbetsledaren Maya Lind berättar vad som hjälper och vad hon skulle ändra". Det sammanfattar hennes citat.
- I ingången (fynd 3): "Kundcaset beskriver vad försöket visade och hur kunden själv bedömer det."
- Mellanrubriken "Arbetsledaren Maya Lind om arbetet med ärendena" (fynd 5) säger att citatet handlar om arbetet med ärendena. Mellanrubriken "Maya Lind ser tillbaka på försöket" (fynd 8) säger att hon blickar tillbaka på försöket.

Utöver påståendena ovan tog körningen bort följande ur berättelsen:
- leverantörens vi-form och reklamvärderingar
- en ordagrant upprepad mening
- en citatbrygga som sade citatet i förväg

Körningen skrev också om rubriken, ingressen, ingången och två mellanrubriker. Den delade det sista avsnittet så att avslutningen fick ett eget avsnitt med egen mellanrubrik. Den avslutande korrekturläsningen gjorde inga ändringar.
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
      "text": "Elm Quay testade Svales programvara i åtta veckor",
      "characters": 49,
      "words": 8
    },
    "standfirst": {
      "text": "Tiden till tilldelning var två arbetsdagar mot tre …",
      "words": 41,
      "sentences_estimate": 3,
      "paragraphs": 1
    },
    "byline": null,
    "lead": {
      "text": "Elm Quay har prövat programvara från leverantören Svale …",
      "words": 25,
      "sentences_estimate": 2,
      "paragraphs": 1
    },
    "sections": [
      {
        "subheading": {
          "text": "Arbetsledaren Maya Lind om arbetet med ärendena",
          "characters": 47,
          "words": 7
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
          "text": "Snabbare tilldelning som inte kan tillskrivas programvaran",
          "characters": 58,
          "words": 7
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
      "heading": "Elm Quay testade Svales programvara i åtta veckor",
      "following": "Tiden till tilldelning var två arbetsdagar mot tre tidigare under Elm Quays försök med Svales programvara. Arbetsbelastningen var dock olika, och enligt kundens anteckning kan skillnaden inte tillskrivas programvaran. Arbetsledaren Maya Lind berättar vad som hjälper och vad hon skulle ändra.",
      "shared_words": [
        "elm",
        "programvara",
        "svales"
      ]
    },
    {
      "id": "subheading-1",
      "kind": "subheading-first-sentence-estimate",
      "heading": "Arbetsledaren Maya Lind om arbetet med ärendena",
      "following": "– Att ha en gemensam bild av ärendena hjälper oss, men jag skulle lägga till en vecka för förberedelser, säger Maya Lind, arbetsledare hos kunden.",
      "shared_words": [
        "lind",
        "maya",
        "ärendena"
      ]
    },
    {
      "id": "subheading-2",
      "kind": "subheading-first-sentence-estimate",
      "heading": "Snabbare tilldelning som inte kan tillskrivas programvaran",
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

**The duties the reply is held to.** Before you read the reply, read two passages and apply them as written: the section *The truth of a report about the text* in `/private/var/folders/cs/vgp_x_353zd9frkjpysp7zdw0000gn/T/kntnt-editorial-388-run-x0nd324r/home/.claude/skills/kntnt/library/references/delivery.md`, and the sentences of `/private/var/folders/cs/vgp_x_353zd9frkjpysp7zdw0000gn/T/kntnt-editorial-388-run-x0nd324r/home/.claude/skills/kntnt/library/references/editorial/base.review.md` that say what the claim account holds, from *A claim removed because the finding named that claim itself* to the end of that paragraph. Read nothing else of either file, and no other file.

**First compare the two texts yourself**, passage by passage, frontmatter and headings included, and note every difference, before you read what the reply says about them. The reply's own account is what you are checking, so it is never how you find a difference.

**Then return two lists.**

1. **False statements.** Every statement of the reply that the text it names contradicts, read as *The truth of a report about the text* reads it: a statement about the text as it arrived against that text, and every other statement against the delivered text. A finding's description of a passage, a count, a length, a grammatical label, where a passage stands, what a round did to a passage, a statement that something holds everywhere or nowhere, and every entry and sentence of the claim account are statements the text can contradict. A judgement of quality — that a heading was vague, that a passage read as filler — is not. For each: quote the statement, name the text it is about, quote the passage that contradicts it, and say what is true.
2. **Claim changes the account misses.** Every difference between the two texts that moves a claim and that the claim account leaves out, or reports short of what it did: scope narrowed or widened; a condition, a qualification, a limit or a connective lost; chronology, causality or attribution moved; or the meaning moved, a sense or a double sense lost and an actor, an ordering or a framing added among it. A headline, a standfirst and a subheading carry claims like any other passage. A sentence that says whose a body of content is — that a person tells it, that a document shows it — carries an attribution for all of that content, wherever the content itself stands: where the delivered text gives a person or a source content that the text as it arrived gave to another voice, the narrator's own among them, the attribution has moved even though every fact still stands where it stood. A statement on your first list that gets wrong whose a passage's content is may have a change built on it: read what the delivered text now says about whose that content is, and put that change on this list where the account reports it short. For each: quote the passage before and after, say what the difference did to the claim — for a moved attribution, who the text gave which content to before and whom it gives it to now — and quote what the account says of it, or say that it says nothing. An entry that names one of the voices a moved attribution took content from, and leaves out another, reports it short.

Write `none` under a list with nothing on it. Return the two lists and nothing else, and write no file.