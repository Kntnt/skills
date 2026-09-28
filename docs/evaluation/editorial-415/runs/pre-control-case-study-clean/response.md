Granskningen hittade två fel, båda i rubriker, och inget av dem är åtgärdat. Den enda korrigeringsrunda som anropet tillät underkändes, eftersom den nya rubriken upprepade ingressen. Texten levereras därför som den kom in.

Genre, språk och teknik:
- **Genre:** case-study, angiven i anropet.
- **Språk:** svenska (`sv`), angivet i anropet.
- **Teknik:** ingen, eftersom genren case-study inte anger någon teknik som den normalt skrivs med.

````markdown
# Elm Quay samlade reparationsärendena

**Elm Quay Housing provade en gemensam reparationslogg i två hus under åtta veckor. Arbetsledaren Maya Lind vill göra om försöket, men skulle avsätta mer tid för förberedelser. Här är vad gruppen gjorde, vad anteckningarna visar och vad hon skulle ändra.**

Text: Iris Falk

Att se samma information över skiftgränserna var vad underhållsgruppen på Elm Quay Housing ville få ut av sin gemensamma reparationslogg. Försöket pågick i åtta veckor och omfattade två hus. Vad det krävde, och vad det gav, går att följa i gruppens egna anteckningar.

## Gruppen enades om kategorierna först

Kategorierna i loggen var underhållsgruppens egna. Leverantören Svale konfigurerade loggen efter dem och utbildade sex medarbetare.

– Vi lade mer tid på att enas om kategorierna än på att lägga in de första ärendena. Den tiden skulle jag avsätta innan nästa hus börjar, säger Maya Lind, arbetsledare på Elm Quay.

## Två perioder med olika arbetsbelastning

Enligt Elm Quays interna försöksanteckning från den 4 december 2025 registrerades 31 ärenden under åtta veckor. Akuta ärenden och tidigare beställda arbeten ingick inte. Mediantiden från anmälan till tilldelning var två arbetsdagar. Under de föregående åtta veckorna var den tre.

Perioderna hade olika arbetsbelastning, och anteckningen tillskriver därför inte skillnaden programvaran.

## Kunden vill ge förberedelserna mer tid

– Jag skulle välja att göra försöket igen. Att ha en gemensam bild av ärendena hjälper oss, men jag skulle lägga till en vecka för förberedelser, säger Lind.

Kundcaset publiceras av leverantören Svale. Den som står inför samma förberedelser kan börja i [Svales checklista för införandet](https://example.invalid/svale/checklist).
````

## Olösta fel

1. **Rubriken säger mer än texten.** Rubriken ”Elm Quay samlade reparationsärendena” presenterar en genomförd förändring för hela organisationen: Elm Quay samlade *reparationsärendena*, i bestämd form och utan avgränsning. Texten beskriver ett försök i två hus under åtta veckor. Den som bara läser rubriken tror att förändringen redan gäller hela organisationen. Först i ingressen och brödtexten framgår att det var ett avgränsat försök. Rubriken får inte påstå mer än texten. Felet är olöst.

2. **Sista mellanrubriken föregriper citatet och ger det fel avsändare.** Mellanrubriken ”Kunden vill ge förberedelserna mer tid” står över Maya Linds citat: ”Jag skulle välja att göra försöket igen. Att ha en gemensam bild av ärendena hjälper oss, men jag skulle lägga till en vecka för förberedelser.” Det ger två problem:
   - Mellanrubriken säger redan det citatet medger, att förberedelserna behöver mer tid. Läsaren möter därför citatet som en upprepning.
   - Linds personliga, villkorade bedömning (”jag skulle”) blir en vilja hos hela kunden (”Kunden vill”). En enskild persons bedömning läses då som organisationens ställningstagande.

   En mellanrubrik över ett citat ska lämna citatets poäng åt citatet och i stället nämna ämnet, tillfället eller den som talar. Felet är olöst.

## Den underkända korrigeringsrundan

Anropet tillät en korrigeringsrunda, och den är förbrukad. Rundan skrev om två rubriker:
- Rubriken blev ”Elm Quay samlade reparationsärenden i två hus på försök”.
- Sista mellanrubriken blev ”Maya Lind ser tillbaka på de åtta veckorna”.

Den nya rubriken skapade ett fel som texten inte hade tidigare. Den upprepade ingressens första mening: ”i två hus” ordagrant och ”på försök” i samma betydelse som ”provade”. Rubriken och ingressen ska säga olika saker med olika ord. Rubriken fick också nio ord, fast normen är högst åtta och det hade gått att hålla sig till den.

Hela rundan underkändes därför, även den nya sista mellanrubriken, och texten återställdes till hur den var före rundan. Felet uppstod när rundan försökte åtgärda fel 1, och det avgör en person nu. Det fel rundan skapade finns inte kvar i den levererade texten.

## Artikelanatomi och påståenden

- **Anatomi:** Texten har alla delar i rätt ordning och håller sig inom de gränser som mätts maskinellt. Övriga krav som skriptet inte räknar är granskade och uppfyllda: ingressen står på egen hand, ingressen och inledningen upprepar inte varandra, mellanrubrikerna beskriver sina avsnitt och sista avsnittet fungerar som avslutning med uppmaning. Undantaget är att rubriken och sista mellanrubriken inte är skrivna som rubrikreglerna kräver, enligt fel 1 och 2.
- **Slutkorrektur:** Den avslutande korrekturläsningen hittade inga mekaniska fel.
- **Påståenden:** Den levererade texten är identisk med den som kom in. Inget påstående har tagits bort, ändrats eller lagts till.
