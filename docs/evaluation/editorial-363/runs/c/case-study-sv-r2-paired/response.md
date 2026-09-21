Granskad och korrigerad. Texten i sin helhet:

```markdown
---
kntnt:
  genre: case-study
  technique: none
  language: sv
---

# Elm Quay samlade felanmälningar i två hus

Telefonsamtal på ett ställe, mejl på ett annat. Så såg det ut hos bostadsföretaget Elm Quay Housing innan underhållsteamet prövade en delad logg hösten 2025. Här är vad teamet gjorde under åtta veckor, vad den interna testanteckningen visar – och vad arbetsledaren Maya Lind skulle göra annorlunda nästa gång.

Av Thomas Barregren

Elm Quay Housing förvaltar 640 lägenheter. I september 2025 bestämde företagets eget underhållsteam att testa en gemensam felanmälningslogg i två av husen. Dittills hade telefonanmälningar och mejl lagrats var för sig, och teamet ville att personal på olika skift skulle se samma information.

## Elm Quay tog in Svale och behöll sina egna kategorier

Teamet undersökte om loggen kunde visa var varje felanmälan låg, och valde Svale Systems efter det. Någon jämförelse med en annan leverantör redovisas inte.

Svale konfigurerade loggen och utbildade sex medarbetare vid två tillfällen. Teamet höll telefonanmälan öppen för de boende.

– Vi ville att kvällsskiftet skulle se vad morgonskiftet redan hade gjort. Kategorierna var våra; Svale hjälpte oss att få in dem i loggen, skriver Maya Lind, arbetsledare för underhållet.

## Mediantiden gäller tilldelning, inte färdigt arbete

Enligt Elm Quays interna anteckning från den 4 december 2025 registrerades 31 felanmälningar under testet. Akuta ärenden och arbeten som beställts dessförinnan är undantagna.

Mediantiden från anmälan till tilldelning var två arbetsdagar under testet och tre under de åtta veckor som föregick det. Perioderna hade olika arbetsbelastning, och anteckningen tillskriver uttryckligen inte programvaran skillnaden. Kostnader, boendenöjdhet och tid till färdigt arbete har inte mätts.

## Beslutet om fler hus dröjer

Ännu har försöket inte utvidgats. Teamet ska först kontrollera hur kategorierna fungerar för större reparationer och därefter bestämma sig.

Lind beskriver vad som tog tid.

– Vi lade mer tid på att komma överens om kategorierna än på att mata in de första anmälningarna. Den tiden skulle jag avsätta innan nästa hus drar i gång, skriver hon.

## Lind skulle göra om testet med en extra förberedelsevecka

Lind lämnar sitt eget omdöme om testet.

– Jag skulle välja att göra om testet. Att ha en samlad bild av anmälningarna hjälper oss, men jag skulle lägga in en extra vecka för förberedelser, skriver hon.

Någon rekommendation som gäller alla bostadsföretag ger hon inte. Funderar du på samma sak hos dig, kan du börja med att läsa igenom [Svales implementeringschecklista](https://example.invalid/svale/checklist).
```

**Upplösning.** Genren `case-study`, språket `sv` och tekniken `none` kommer alla tre från `kntnt`-kartan i textens frontmatter. `none` är ett värde och ingen lucka: det säger att ingen teknik valdes, så genrens vanliga båge tillämpades inte. Korrigeringsbudgeten var standardvärdet 1.

**Fynd.** Sex fynd, alla åtgärdade i en runda. Omgranskningen av den korrigerade texten lämnar inga fynd kvar, och inget är olöst.

**Borttagna påståenden.** Inga.

**Ändrade påståenden.** Två reparationer lämnade ett påstående kvar men flyttade det.

1. *”Samma kategorier är det Lind pekar på när hon beskriver vad som tog tid.”* blev *”Lind beskriver vad som tog tid.”* Fyndet gällde den omvända klyvningen och att bryggan sa citatet i förväg. Med den gick brödtextens uttryckliga samband förlorat: den säger inte längre att det Lind pekar på är samma kategorier som teamet hade. Sambandet vilar nu på den bestämda formen *kategorierna* inne i citatet.

2. *”Sitt eget omdöme om testet lämnar Lind med en reservation inbyggd.”* blev *”Lind lämnar sitt eget omdöme om testet.”* Fyndet gällde spetsställningen och kollokationen *med en reservation inbyggd*. Med den gick brödtextens egen uppgift om att omdömet har ett förbehåll förlorad. Förbehållet står kvar i sin helhet på tre andra ställen: i Linds citat (*”men jag skulle lägga in en extra vecka för förberedelser”*), i meningen efter citatet (*”Någon rekommendation som gäller alla bostadsföretag ger hon inte”*) och i den nya mellanrubriken.

Inga siffror, datum, attributioner, citat eller förbehåll i övrigt är ändrade, och ingenting inuti ett citat är rört.
