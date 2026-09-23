Granskad som **case-study** på **svenska (sv)**, utan teknik: genren slöts ur texten eftersom ingen var angiven, och case-study anger ingen teknik som den sortens text vanligen skrivs med. Korrigeringsbudgeten var 1, och den förbrukades i en runda. Den avslutande mekaniska genomgången ändrade ingenting.

```markdown
# Elm Quay samlade 31 reparationsärenden på åtta veckor

**Elm Quay Housing provade en gemensam reparationslogg i två hus. Arbetsledaren Maya Lind vill göra om försöket, men skulle avsätta mer tid för förberedelser.**

För Elm Quays underhållsgrupp handlade försöket med en gemensam reparationslogg i två hus om att se samma information över skiftgränserna. Gruppen valde loggens kategorier; leverantören Svale konfigurerade loggen och utbildade sex medarbetare.

## Mediantiden sjönk en arbetsdag, men orsaken lämnas öppen

Enligt Elm Quays interna försöksanteckning från den 4 december 2025 registrerades 31 ärenden under åtta veckor. Akuta ärenden och tidigare beställda arbeten ingick inte. Mediantiden från anmälan till tilldelning var två arbetsdagar, jämfört med tre under de föregående åtta veckorna.

Perioderna hade olika arbetsbelastning. Anteckningen tillskriver därför inte skillnaden programvaran.

## Kunden vill ge förberedelserna mer tid

– Vi lade mer tid på att enas om kategorierna än på att lägga in de första ärendena. Den tiden skulle jag avsätta innan nästa hus börjar, säger Maya Lind.

– Jag skulle välja att göra försöket igen. Att ha en gemensam bild av ärendena hjälper oss, men jag skulle lägga till en vecka för förberedelser, säger Lind.

Kundcaset publiceras av leverantören Svale. [Läs Svales checklista för införandet](https://example.invalid/svale/checklist).
```

## Kvarstående iakttagelser

Alla tre är olösta. Budgeten tog slut med iakttagelser kvar, och två av dem uppstod ur rundans egen reparation.

1. **Bylinen saknas.** Artikelanatomin kräver en rad som namnger författaren, direkt efter ingressrutan; mätningen rapporterar `byline: absent`. Varken texten, dess metadata eller anropet namnger någon författare, så raden lämnas ofylld i stället för att fyllas med ett påhittat namn. I en kundberättelse som en leverantör publicerar är avsändarskapet just det läsaren vill kunna se.

2. **Ingressens första mening blev tung att läsa.** "För Elm Quays underhållsgrupp handlade försöket med en gemensam reparationslogg i två hus om att se samma information över skiftgränserna." – "handlade" och sitt "om" står nu nio ord isär, och den mellanliggande frasen inleds med "med", så läsaren hinner läsa "handlade … med" som ett eget uttryck innan "om" kommer och ordningen måste tas om. Iakttagelsen följer av rundans reparation av referenterna, som namngav försöket och loggen inne i den befintliga meningen i stället för att ge dem en egen.

3. **Två citat står nu direkt efter varandra i slutavsnittet.** Genren vill att berättande text gör det förbindande arbetet mellan citaten och att en brygga förbereder ett citat i stället för att säga det i förväg; mellan "– Vi lade mer tid …" och "– Jag skulle välja …" finns ingen sådan text. Samtidigt växte slutet från två stycken till tre, där anatomin vill ha ett kort slut. Iakttagelsen följer av rundans reparation av den tvåstyckiga ingressen, som flyttade citatet till det sista avsnittet.

## Ändrade påståenden

Inget stycke och ingen mening togs bort, och meningarna som avgränsar vad texten påstår står ordagrant kvar: "Akuta ärenden och tidigare beställda arbeten ingick inte." samt "Perioderna hade olika arbetsbelastning. Anteckningen tillskriver därför inte skillnaden programvaran." Två påståenden i paratexten ändrades:

- **Rubriken.** "Elm Quay samlade reparationsärendena" blev "Elm Quay samlade 31 reparationsärenden på åtta veckor". Räckvidden är därmed snävare: bestämd form i plural omfattade reparationsärendena som helhet, den nya rubriken bara den siffra och den period brödtexten anger. Ändringen gjordes av reparationen av iakttagelsen att rubriken påstod mer än texten.
- **Den första mellanrubriken.** "Två perioder med olika arbetsbelastning" blev "Mediantiden sjönk en arbetsdag, men orsaken lämnas öppen". Paratexten säger nu vad som mättes och behåller reservationen, medan det tidigare påståendet om periodernas olika arbetsbelastning står kvar oförändrat i avsnittets andra stycke. Ändringen gjordes av reparationen av iakttagelsen att mellanrubriken var en etikett utan verb.

Ingenting skrevs till filsystemet: `input.md` är oförändrad och texten levereras här.
