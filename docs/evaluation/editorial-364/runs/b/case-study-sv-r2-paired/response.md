Granskad som `case-study` på `sv`, utan teknik. Alla tre värdena kommer från dokumentets egen `kntnt`-karta, och kartans `technique: none` säger att ingen teknik är vald — därför tillämpas ingen berättelseform, varken en vald eller den genren annars skrivs med. Korrigeringsbudgeten var 1 och den är spenderad i en runda.

```markdown
---
kntnt:
  genre: case-study
  technique: none
  language: sv
---

# Elm Quay testade en ärendelogg i två hus

Elm Quay Housing sköter 640 lägenheter och prövade hösten 2025 en gemensam felanmälningslogg i två av husen. Här får du veta vad underhållsteamet gjorde, vilka siffror den interna testnoteringen stöder och vad arbetsledaren skulle lägga mer tid på nästa gång.

Av Thomas Barregren

I september 2025 beslutade Elm Quay Housings eget underhållsteam att på prov samla felanmälningarna från två av husen i en enda logg. Dittills hade telefonanmälningar och mejl sparats var för sig. Teamet valde Svale Systems efter att ha prövat om loggen kunde visa status för varje ärende, och någon jämförelse med en annan leverantör finns inte att tillgå. Efter åtta veckors test fanns både en testnotering med siffror och en arbetsledare med en bedömning.

## Underhållsteamet bestämde hur felanmälningarna skulle sorteras

Svale Systems konfigurerade loggen och utbildade sex medarbetare vid två tillfällen. Telefonanmälan behölls för de boende.

– Vi ville att kvällsskiftet skulle se vad morgonskiftet redan hade gjort. Kategorierna var våra; Svale hjälpte oss att lägga in dem i loggen, säger Maya Lind, arbetsledare för underhållet.

– Vi lade mer tid på att enas om kategorierna än på att registrera de första anmälningarna. Den tiden skulle jag avsätta innan nästa hus drar i gång, säger hon.

## Tilldelningstiden mättes, inte kostnad eller nöjdhet

Elm Quays interna testnotering från den 4 december 2025 redovisar 31 registrerade anmälningar. Akuta ärenden och arbeten som beställts före testet ingår inte.

Mediantiden från anmälan till tilldelning var två arbetsdagar under testet och tre under de åtta veckorna dessförinnan. Perioderna hade olika arbetsbelastning, och noteringen tillskriver uttryckligen inte programvaran skillnaden.

Kostnader, de boendes nöjdhet och tiden fram till avslutat arbete har inte mätts.

## Arbetsledarens omdöme kommer med villkor

– Jag skulle välja att göra testet igen. Att ha en samlad bild av anmälningarna hjälper oss, men jag skulle lägga in en extra vecka för förberedelser, säger Maya Lind.

Lind rekommenderar inte Svale till alla bostadsföretag. Teamet har ännu inte utvidgat testet, utan ska först se hur kategorierna fungerar för större reparationer och beslutar därefter. Väger du samma beslut kan du läsa [checklistan för införande](https://example.invalid/svale/checklist).
```

**Åtgärdade fynd**

- Rubriken påstod ett avslutat resultat för hela Elm Quay, medan texten stöder ett åtta veckor långt test i två av husen som teamet ännu inte har utvidgat.
- Mellanrubriken före tredje avsnittet sa citatet under den i förväg, med nästan samma ord: *göra om testet* mot *göra testet igen*, *mer förberedelse* mot *en extra vecka för förberedelser*.
- Mellanrubriken före första avsnittet upprepade avsnittets första mening ordagrant i *konfigurerade* och sa med egna ord det som citatet säger med talarens.
- Brödtextens första mening återgav ingressens formulering ordagrant i sju ord (*en gemensam felanmälningslogg i två av husen*).

**Kvarstående fynd**

1. **Testets omfattning går inte att bedöma.** *Oåtgärdat sedan granskningen.* Texten säger aldrig hur många hus Elm Quay Housing har, och antalet lägenheter står bara i ingressen, som brödtexten ska vara begriplig utan. *Två av husen* saknar därmed nämnare, och läsaren kan varken bedöma hur stor del av beståndet testet omfattade eller vad de 31 anmälningarna täcker. Uppgiften finns inte i texten, så fyndet kräver material att hämta den ur.
2. **Rubriken inför ett ord texten inte använder.** *Nytt fynd, skapat av rundans reparation av rubriken.* Den nya rubriken säger *ärendelogg*, medan resten av texten säger *felanmälningslogg* och *loggen*. Läsaren möter två namn på samma sak och det namn rubriken använder återkommer aldrig. Rubriken ligger dessutom nära ingressens första led, och rubrik och ingress ska säga olika saker med olika ord.
3. **Mellanrubriken före tredje avsnittet håller inne svaret.** *Nytt fynd, skapat av rundans reparation av samma mellanrubrik.* *Arbetsledarens omdöme kommer med villkor* säger att omdömet är villkorat men inte vad det är. Den som skummar texten får veta att det finns förbehåll, men inte att arbetsledaren skulle göra om testet — och en mellanrubrik ska ge svaret, inte begära att avsnittet läses för att bli begriplig.

**Varför granskningen stannade här**

Budgeten på en korrigering var spenderad, och omgranskningen av den korrigerade texten fann två fynd som rundans egen reparation hade skapat (2 och 3 ovan). En runda till hade reparerat det föregående rundan gjorde, så den togs inte. Vad rubriken och den tredje mellanrubriken ska säga är det du som avgör.

**Påståenden**

Inget påstående i brödtexten togs bort, och inget står kvar med ändrad räckvidd, säkerhet, källa, kronologi, orsak eller innebörd. Alla avgränsande meningar är orörda: att ingen jämförelse med en annan leverantör finns att tillgå, att noteringen uttryckligen inte tillskriver programvaran skillnaden, att kostnader, nöjdhet och tid till avslutat arbete inte har mätts, och att Lind inte rekommenderar Svale till alla bostadsföretag.

Ett påstående ändrades, och det är rubrikens. *Elm Quay fick en gemensam bild av felanmälningarna* finns inte kvar någonstans i texten; rubriken säger nu att Elm Quay testade en logg i två hus. Fynd 1 namngav rubrikens räckvidd som defekten, så ändringen står — men den nämns här eftersom rubriken var enda stället där texten sa att bolaget hade fått en gemensam bild. Det som den gamla mellanrubriken före första avsnittet sa — att leverantören konfigurerade och att teamet bestämde kategorierna — står oförändrat kvar i avsnittets första mening och i Maya Linds citat.
