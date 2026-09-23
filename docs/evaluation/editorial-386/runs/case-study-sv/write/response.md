**Utkastet levereras med kända brister.** Den avslutande källkontrollen lämnade två kvarstående anmärkningar, båda om källstöd. De är kontrollantens påståenden om texten och avgörs av redaktören, inte fastställda fel. Prosan levereras exakt som den sista kontrollen läste den, så ingen av dem är åtgärdad.

- **Ingressens "31 anmälningar registrerades" saknar undantagen och sin källa.** Underlaget säger att Elm Quays interna testanteckning anger 31 anmälningar, och att akuta ärenden och arbeten som beställts före testet inte räknas in. Ingressen ger siffran utan de två undantagen och utan att den är anteckningens. Fallet som står: om akuta ärenden också fördes in i loggen men hölls utanför anteckningens räkning, stämmer underlaget medan ingressens ord inte gör det — underlaget säger att räkningen utesluter dem, inte att de hölls utanför loggen. Brödtexten bär undantagen, men ingressen läses för sig. Minsta föreslagna lagning: "31 anmälningar registrerades, akuta ärenden och tidigare beställda arbeten oräknade, och arbetsledaren skulle göra om testet …".
- **Ledets "Telefonanmälningar på ett ställe, e-post på ett annat" påstår ett ställe per kanal.** Underlaget säger bara att telefonanmälningar och e-post förvarades var för sig. Fallet som står: om telefonanmälningarna antecknades i varsin pärm i de två husen och e-posten låg i enskilda medarbetares inkorgar, är de fortfarande förvarade var för sig, men ingen av kanalerna hade ett ställe. Minsta föreslagna lagning: "Telefonanmälningar för sig, e-post för sig." Resten av meningen står kvar.

---

```markdown
---
kntnt:
  genre: case-study
  technique: none
  language: sv
---

# Elm Quay testade gemensam logg i två hus

Hösten 2025 prövade bostadsbolaget Elm Quay Housing en gemensam felanmälningslogg i ett test som varade åtta veckor. 31 anmälningar registrerades, och arbetsledaren skulle göra om testet – men med mer tid för förberedelser. Här är vad testet krävde och vad siffrorna inte säger.

Av Thomas Barregren

Telefonanmälningar på ett ställe, e-post på ett annat. Så förvarades felanmälningarna hos Elm Quay Housing, ett bostadsbolag med eget underhållslag som förvaltar 640 lägenheter. I september 2025 bestämde sig laget för att pröva en gemensam logg i två hus.

## Så kom systemet på plats i de två husen

Laget testade om loggen kunde visa status för varje reparation och valde därefter Svale Systems. Någon jämförelse med en annan leverantör finns inte.

– Vi ville att kvällsskiftet skulle se vad morgonskiftet redan hade gjort. Kategorierna var våra; Svale hjälpte oss att lägga in dem i loggen, skriver Maya Lind, arbetsledare för underhållet, i en mejlintervju.

De boende kunde fortsätta anmäla fel per telefon under testet. Svale konfigurerade loggen och utbildade sex medarbetare vid två tillfällen.

## Siffrorna säger inget om orsaken

Testet pågick i åtta veckor. Enligt Elm Quays interna testanteckning från 4 december 2025 registrerades 31 felanmälningar i loggen, och då är akuta ärenden och arbeten som beställts före testet inte inräknade.

Mediantiden från anmälan till tilldelad åtgärd var två arbetsdagar under testet och tre under de åtta veckorna dessförinnan. Arbetsbelastningen skilde sig mellan perioderna, och anteckningen tillskriver uttryckligen inte skillnaden programvaran. Kostnader, de boendes nöjdhet och tiden fram till avslutad åtgärd mättes inte.

– Vi lade mer tid på att komma överens om kategorierna än på att registrera de första anmälningarna. Den tiden skulle jag avsätta innan nästa hus drar i gång, skriver Maya Lind.

## Beslutet om fler hus återstår

Testet har ännu inte utvidgats. Laget vill först se hur kategorierna fungerar för större reparationer, och Lind rekommenderade inte Svale till varje bostadsbolag.

– Jag skulle välja att göra om testet. Att ha en samlad bild av anmälningarna hjälper oss, men jag skulle lägga in en extra vecka för förberedelser, skriver hon.

För den som överväger ett liknande test finns Svale Systems [checklista för införande](https://example.invalid/svale/checklist) att läsa igenom. Den här kundberättelsen är publicerad av Svale Systems och är alltså inte oberoende journalistik.
```

---

**Vad som lästes ut av anropet.** Genren är `case-study`, vald i anropet. Ingen teknik är tillämpad: genren anger själv att den här sortens text ordinarie skrivs utan någon, så texten har ingen påbjuden båge — bara den ordning ämnet kräver. Språket är svenska, valt i anropet och kontrollerat mot de installerade språkresurserna. Bilagd metadata är på, som standard, och `kntnt`-kartan ovan bär genren, tekniken och språket och ingenting annat.

**Vart utkastet gick.** Till det här svaret, som anropet begärde. Inget skrevs till filsystemet: arbetsfilerna och kontrollmapparna är borttagna och `source.md` är orörd. Ett undantag finns, begärt utanför uppdraget av den som observerar körningen: kopiorna av utkasten och de två kontrollrapporterna ligger kvar i `evidence/source-check/` i körningsmappen.

**Bylinen bär ditt namn.** Uppdraget namnger ingen författare, så författaren är du. Ska texten gå osignerad eller under någon annans namn måste raden ändras före publicering.

**Var materialet tog slut.** Uppdraget bad om omkring 400 ord "as material allows"; utkastet är omkring 380. Det som saknas för att fylla ut är sådant som inte finns i underlaget, och som därför inte kan skrivas fram:

- Inga mätningar av kostnad, de boendes nöjdhet eller tid fram till avslutad åtgärd. Sådana siffror skulle ge en egen sektion.
- Ingen jämförelse med någon annan leverantör, så valet kan bara redovisas som ett kapacitetstest och ett beslut.
- Anteckningen tillskriver uttryckligen inte skillnaden i mediantid programvaran, och underlaget förbjuder varje orsakspåstående. Texten ställer därför siffrorna bredvid varandra utan slutsats.
- Intervjun skedde via mejl, och inget scenmaterial, ingen känsla och ingen återgiven replik finns. Därför finns ingen miljöskildring, och citaten är införda med "skriver".
- Länken `https://example.invalid/svale/checklist` hämtades inte — domänen är reserverad som icke-upplösbar — så destinationen beskrivs bara som uppdraget beskriver den: en checklista för införande att läsa igenom. Ska texten säga vad checklistan innehåller krävs checklistan själv.

**Kontroller som gjordes.** Artikelanatomin är maskinmätt och uppfyller varje räknat krav. Två fullständiga källjämförelser gjordes av färska kontrollanter. Den första lämnade sex anmärkningar — ägandeskap kontra förvaltning, ingressens siffra, ett påstått val av vilka två hus, vad som testades i loggen, vem som konstaterar skillnaden i arbetsbelastning, och en översättningsanmärkning om "innan nästa hus börjar" — och alla sex lagades. Den första kontrollantens rapport kunde inte skrivas till fil, eftersom harnesset stoppar rapportfiler från underagenter; den kom i stället i svaret och sparades då av körningen. Den andra kontrollen läste den lagade texten, fann inga översättningsanmärkningar och lämnade de två anmärkningar som redovisas överst. Den är den sista kontrollen, och efter den har ingen prosa ändrats.
