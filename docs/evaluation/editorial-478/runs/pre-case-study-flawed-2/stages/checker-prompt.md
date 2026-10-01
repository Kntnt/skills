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

(In both blocks above, the fence lines are not part of the text.)

**The reply.** This is everything the run is about to say about the two texts:

````text
Konfiguration: genre casestudy (från anropet), ingen teknik (genren casestudy anger ingen teknik som den vanligen skrivs med), språk sv – svenska (från anropet). Texten har ingen frontmatter och därmed ingen kntnt-karta, och ingen har lagts till.

Korrigeringsrundan förkastades. En korrigeringsrunda gjordes (budget 1) och förkastades vid granskningen efteråt. Rundan strök meningen ”Vår programvara orsakade därför hela förbättringen.” och flyttade uppgiften om att programvaran är Svales till ingressen (”Svales programvara”). Därmed saknade ”programvaran” i meningen ”Anteckningen säger att arbetsbelastningen var olika och att skillnaden inte kan tillskrivas programvaran.” referent i brödtexten: bara ingressen sa vilken programvara det gällde, och artikelanatomin kräver att brödtexten går att läsa utan ingressen. Det felet hade texten inte när den kom in, så hela rundan förkastades och texten återställdes som den var. Inget av rundans ändringar finns i den levererade texten – inte heller dess omskrivna rubrik, ingress och underrubriker. Det som en människa behöver avgöra är reparationen i fynd 8: var i brödtexten det ska stå, i tredje person, att programvaran är Svales när orsakspåståendet stryks. Budgeten är förbrukad.

Den avslutande korrekturläsningen hittade inga mekaniska fel. Den levererade texten är därför byte för byte identisk med input.md.

Fynd – alla olösta:

1. Rubriken ”Vår fantastiska lösning räddade Elm Quay” påstår mer än texten bär. ”Räddade” motsägs av försöksanteckningen, som säger att skillnaden inte kan tillskrivas programvaran, och texten beskriver ingen kris. ”Fantastiska” är en värdering utan stöd, och ”Vår” gör leverantören till berättare i vi-form, där ett kundcase nämner leverantören i tredje person. Läsaren vilseleds om vad texten visar, och tonen är reklamens.

2. Ingressen består av samma mening två gånger: ”Elm Quay registrerade 31 ärenden.” Den säger inte vilka ärenden det gäller, under vilken period eller i vilket försök, och inte vad texten handlar om eller vad läsaren får ut av den. Läsaren får ingen presentation av texten, och dubbleringen läses som ett fel.

3. Ingressen och inledningsstycket öppnar på samma mening, ”Elm Quay registrerade 31 ärenden.” (mätningen: båda börjar på ”Elm”). Inledningen möter läsaren som ingressen sagd igen, och siffran 31 upprepas tre gånger innan något nytt sägs.

4. ”Vi på Svale är världsledande på att skapa framgång” i inledningsstycket är ett ogrundat överlägsenhetspåstående i leverantörens vi-form. Inget i texten stöder det, och det försvagar förtroendet för resten av texten.

5. ”och kunden stod hjälplös innan vi kom” gör kunden hjälplös i en räddningsberättelse. Det enda texten säger om läget före försöket är att tiden till tilldelning var tre arbetsdagar. Läsaren får en bild av kunden som texten inte bär.

6. Underrubriken ”Kunden fick en gemensam bild” och bryggan ”Maya Lind säger att det hjälper att ha en gemensam bild av ärendena.” säger båda i förväg citatets omdöme, och underrubriken delar formuleringen ”en gemensam bild” med meningen under den. Läsaren möter Maya Linds citat som något som redan sagts två gånger.

7. Underrubriken ”Resultatet bevisar allt” påstår motsatsen till avsnittet under den, som säger att skillnaden inte kan tillskrivas programvaran. Den är högre i tonen än texten och säger inte vad avsnittet handlar om. Läsaren vilseleds om vad resultaten visar.

8. ”Vår programvara orsakade därför hela förbättringen.” drar en orsaksslutsats som meningen direkt före den motsäger, och ”därför” påstår ett samband som texten inte etablerar. Meningen står dessutom i leverantörens vi-form. Texten säger emot sig själv. Meningen ”Anteckningen säger att arbetsbelastningen var olika och att skillnaden inte kan tillskrivas programvaran.” avgränsar vad texten påstår och ska stå kvar; uppgiften om att programvaran är Svales behöver finnas kvar i brödtexten i tredje person om orsakspåståendet stryks (se den förkastade rundan ovan).

9. Byline saknas (mätningen: byline absent). Ingen författare namnges i texten eller anropet, så den är inte ifylld.

10. Avslutningsavsnitt och uppmaning till handling saknas. Sista avsnittet, ”Resultatet bevisar allt”, lägger fram resultaten och är inget avslut, och texten innehåller inget erbjudande, ingen länk och ingen kontaktväg som en uppmaning kan bygga på. Delarna är inte skrivna.

11. Kundbakgrund, anledning och genomförande saknas. Texten säger inte vad Elm Quay är, vad försöket gick ut på eller vad Svale levererade, och inledningen ger därför ingen tydlig förväntan. Det kräver material som texten inte innehåller.

Texten uppfyller inte artikelanatomin: byline och avslutningsavsnitt saknas (fynd 9 och 10).

Påståenden: den levererade texten är identisk med den mottagna, så inget påstående har strukits, ändrats eller lagts till i den.
````

**The measurement of the delivered text.** This is the full output of the collection's measuring script, run on the delivered text. A count or length the reply states about the delivered text is read against it:

```json
{"ok": true, "format": "markdown", "conforms": false, "failures": [{"part": "byline", "rule": "A text conforms when every part is present in the order shown.", "measured": "absent", "text": null}], "norms": [{"part": "lead", "rule": "They should begin with different first words, and an everyday word such as *the* or *it* counts like any other.", "measured": "both open on “elm”", "text": "Elm Quay registrerade 31 ärenden. Vi på Svale …"}], "typical": {"paragraphs": 7, "paragraphs_of_two_or_three_sentences": 2, "sections": 2, "sections_of_two_or_three_paragraphs": 2}, "parts": {"headline": {"text": "Vår fantastiska lösning räddade Elm Quay", "characters": 40, "words": 6}, "standfirst": {"text": "Elm Quay registrerade 31 ärenden. Elm Quay registrerade …", "words": 10, "sentences_estimate": 2, "paragraphs": 1}, "byline": null, "lead": {"text": "Elm Quay registrerade 31 ärenden. Vi på Svale …", "words": 21, "sentences_estimate": 2, "paragraphs": 1}, "sections": [{"subheading": {"text": "Kunden fick en gemensam bild", "characters": 28, "words": 5}, "paragraphs": [{"text": "Maya Lind säger att det hjälper att ha …", "words": 13, "sentences_estimate": 1}, {"text": "– Att ha en gemensam bild av ärendena …", "words": 24, "sentences_estimate": 1}]}, {"subheading": {"text": "Resultatet bevisar allt", "characters": 23, "words": 3}, "paragraphs": [{"text": "Enligt kundens försöksanteckning registrerades 31 ärenden under åtta …", "words": 42, "sentences_estimate": 4}, {"text": "– Jag skulle välja att göra försöket igen, …", "words": 9, "sentences_estimate": 1}, {"text": "Kundcaset publiceras av leverantören Svale.", "words": 5, "sentences_estimate": 1}]}], "other": []}, "heading_pairs": [{"id": "headline-standfirst", "kind": "headline-standfirst", "heading": "Vår fantastiska lösning räddade Elm Quay", "following": "Elm Quay registrerade 31 ärenden. Elm Quay registrerade 31 ärenden.", "shared_words": ["elm", "quay"]}, {"id": "subheading-1", "kind": "subheading-first-sentence-estimate", "heading": "Kunden fick en gemensam bild", "following": "Maya Lind säger att det hjälper att ha en gemensam bild av ärendena.", "shared_words": ["bild", "en", "gemensam"]}, {"id": "subheading-2", "kind": "subheading-first-sentence-estimate", "heading": "Resultatet bevisar allt", "following": "Enligt kundens försöksanteckning registrerades 31 ärenden under åtta veckor, med akuta ärenden undantagna.", "shared_words": []}]}
```

**The duties the reply is held to.** Before you read the reply, read two passages and apply them as written: the section *The truth of a report about the text* in `/private/var/folders/cs/vgp_x_353zd9frkjpysp7zdw0000gn/T/kntnt-editorial-388-run-egdro0qi/home/.claude/skills/kntnt/library/references/delivery.md`, and the sentences of `/private/var/folders/cs/vgp_x_353zd9frkjpysp7zdw0000gn/T/kntnt-editorial-388-run-egdro0qi/home/.claude/skills/kntnt/library/references/editorial/base.review.md` that say what the claim account holds, from *A claim removed because the finding named that claim itself* to the end of that paragraph. Read nothing else of either file, and no other file.

**First compare the two texts yourself**, passage by passage, frontmatter and headings included, and note every difference, before you read what the reply says about them. The reply's own account is what you are checking, so it is never how you find a difference.

**Then return two lists.**

1. **False statements.** Every statement of the reply that the text it names contradicts, read as *The truth of a report about the text* reads it: a statement about the text as it arrived against that text, and every other statement against the delivered text. A finding's description of a passage, a count, a length, a grammatical label, where a passage stands, what a round did to a passage, a statement that something holds everywhere or nowhere, and every entry and sentence of the claim account are statements the text can contradict. A judgement of quality — that a heading was vague, that a passage read as filler — is not. For each: quote the statement, name the text it is about, quote the passage that contradicts it, and say what is true.
2. **Claim changes the account misses.** Every difference between the two texts that moves a claim and that the claim account leaves out, or reports short of what it did: scope narrowed or widened; a condition, a qualification, a limit or a connective lost; chronology, causality or attribution moved; or the meaning moved, a sense or a double sense lost and an actor, an ordering or a framing added among it. A headline, a standfirst and a subheading carry claims like any other passage. For each: quote the passage before and after, say what the difference did to the claim, and quote what the account says of it, or say that it says nothing.

Write `none` under a list with nothing on it. Return the two lists and nothing else, and write no file.