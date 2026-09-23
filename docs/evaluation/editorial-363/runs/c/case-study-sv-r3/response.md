**Utkastet levereras med kända brister.** Den avslutande källkontrollen lämnade fyra invändningar om källstöd. Ingen av dem är åtgärdad: den kontrollen är den sista som läst texten, och det som levereras är exakt den text den läste.

1. **"Någon jämförelse med en annan leverantör finns inte."** Underlaget säger *"No comparison with another supplier is available"* — att ingen jämförelse finns att tillgå, inte att ingen gjorts. Minsta föreslagna rättelse: "Någon jämförelse med en annan leverantör finns inte **redovisad**."
2. **"… redovisar 31 felanmälningar under de åtta veckorna."** Underlaget säger att de 31 anmälningarna *lades in* (*"were entered"*). Utan den bestämningen kan siffran läsas som alla anmälningar under perioden. Minsta föreslagna rättelse: "… redovisar 31 felanmälningar **i loggen** under de åtta veckorna."
3. **"Teamet ska först se efter hur kategorierna fungerar för större reparationer."** Underlaget säger att teamet ska *ta ställning* efter kontrollen (*"will decide"*). Med "först" läser en läsare utvidgningen som inplanerad i stället för oavgjord. Minsta föreslagna rättelse: "… för större reparationer **och därefter ta ställning**."
4. **"status på varje ärende"** (mindre). Underlaget säger *"the status of each repair"*, och *ärende* är i fastighetsförvaltning vidare än *reparation*. Minsta föreslagna rättelse: "status på varje **reparation**."

Den första kontrollen läste punkt 1 och 4 som korrekta; den andra invänder mot dem. Alla fyra är invändningar som du avgör, inte konstaterade fel i texten.

```markdown
---
kntnt:
  genre: case-study
  technique: none
  language: sv
---

# Elm Quay testade gemensam felanmälningslogg i två hus

Elm Quay Housing förvaltar 640 lägenheter. Under åtta veckor hösten 2025 provade underhållsteamet ett nytt sätt att hålla ihop felanmälningarna, med Svale Systems som leverantör. Utfallet finns i en intern notering, och arbetsledaren har redan en sak hon skulle göra annorlunda.

Av Thomas Barregren

Telefonanmälningar och mejl sparades var för sig hos Elm Quay Housing, ett bostadsbolag med 640 lägenheter. I september 2025 bestämde underhållsteamet att prova en gemensam logg i två av husen, och försöket pågick i åtta veckor.

## Så förbereddes försöket i de två husen

Teamet valde Svale Systems efter att ha testat om loggen kunde visa status på varje ärende. Någon jämförelse med en annan leverantör finns inte.

Telefonanmälan höll teamet öppen för de boende. Svale konfigurerade loggen och utbildade sex medarbetare vid två tillfällen. Vad loggen skulle lösa hade teamet redan bestämt.

– Vi ville att kvällsskiftet skulle se vad morgonskiftet redan hade gjort. Kategorierna var våra, och Svale hjälpte oss att lägga in dem i loggen, säger Maya Lind, arbetsledare för underhållet.

## Siffrorna säger inget om orsaken

Den interna noteringen från den 4 december 2025 redovisar 31 felanmälningar under de åtta veckorna. Akuta ärenden och arbete som beställts före försöket är inte medräknade.

Mediantiden från anmälan till tilldelning var två arbetsdagar under försöket och tre under de åtta veckorna dessförinnan. Arbetsbelastningen skilde sig mellan perioderna, och noteringen kopplar uttryckligen inte skillnaden till programvaran.

Kostnader, nöjdhet hos de boende och tid till avslutat arbete mättes inte.

## Kategorierna ska prövas mot större reparationer

Försöket har ännu inte utvidgats till fler hus. Teamet ska först se efter hur kategorierna fungerar för större reparationer.

– Vi lade mer tid på att enas om kategorierna än på att lägga in de första anmälningarna. Den tiden skulle jag avsätta innan nästa hus kommer igång, säger Lind.

## Omdömet gäller inte varje bostadsbolag

– Jag skulle välja att göra om försöket. Att ha en samlad bild av anmälningarna hjälper oss, men jag skulle lägga in en extra vecka för förberedelser, säger hon.

Hon rekommenderar däremot inte Svale till alla bostadsbolag. Står du inför samma fråga i ditt eget bestånd, är [införandechecklistan](https://example.invalid/svale/checklist) ett dokument att läsa igenom först. Texten publiceras av Svale Systems, som var leverantör i försöket, och intervjun med Maya Lind gjordes via mejl.
```

**Så löstes anropet.** Genre: `case-study`, från anropet. Teknik: ingen — genren anger själv att den inte skrivs med någon, så ingen berättarteknik ligger under texten. Språk: svenska (`sv`), från anropet; underlaget är på engelska, och citaten är översatta, vilket underlaget uttryckligen tillåter. Utdata: svaret. Ingenting har skrivits till disk, och inga filer finns kvar efter körningen.

**Bylinen bär ditt namn.** Uppdraget namnger ingen författare, så författaren är du: "Av Thomas Barregren". Ska texten gå osignerad eller under annat namn behöver raden ändras före publicering.

**Två kontroller kördes**, båda mot hela underlaget och hela utkastet. Den första ledde till fyra ändringar, som alltså redan är gjorda: bylinens sammanfattning tillskrev teamet en ståndpunkt som bara arbetsledaren uttalar i första person singular; en mellanrubrik påstod en ordningsföljd ("innan loggen togs i bruk") som underlaget inte fastställer; citatet "innan nästa hus börjar" stannade en svensk läsare på verbet; och två s-passiver lämnade Svale som enda utpekade aktör i ett avsnitt där kunden ska vara den handlande. Den andra kontrollen läste den ändrade texten och lämnade de fyra punkterna ovan. Den första kontrollen fick köras om: rapportfilen kunde inte skrivas under `.git/`, och svaret som bar rapporten kapades på vägen, så den ofullständiga rapporten räknades inte som en genomförd jämförelse.

**Där underlaget tar slut.** Uppdraget ber om ungefär 400 ord; utkastet är 377. Underlaget är helt använt, och den stående längden är vad materialet bär. Det som skulle sluta gapet är mer material, inte mer text: mätningar av kostnad, boendenöjdhet eller tid till avslutat arbete, en jämförelse med någon annan leverantör, utfallet av kontrollen mot större reparationer, eller en andra röst vid sidan av arbetsledaren. Ingen effekt av programvaran kan påstås: noteringen kopplar uttryckligen inte skillnaden i mediantid till programvaran, och perioderna hade olika arbetsbelastning.

Texten mättes också mot artikelanatomin och uppfyllde varje räknat krav, både före och efter rättelserna.
