**Utkastet levereras med kända brister.** Den avslutande källjämförelsen lämnade två invändningar som inte åtgärdades, eftersom körningens två jämförelser då var förbrukade. Texten nedan är exakt den prosa som den sista jämförelsen läste.

1. **"Uppdraget består av två delar:"** — underlaget säger "Genomgången omfattar ett videomöte på 45 minuter med två representanter för styrelsen och en skriftlig sammanställning av nuvarande steg, oklarheter och två möjliga förenklingar". Det räknar upp utan att säga att uppräkningen är allt. Utkastet gör den uttömmande och anger ett antal som underlaget inte anger. Minsta föreslagna rättelse: byt raden mot "Uppdraget omfattar:" och låt båda punkterna stå kvar.
2. **"för att stämma av om uppdraget passar er förening"** — underlaget säger "för att stämma av om uppdraget passar", utan att säga vad det ska passa. Utkastet snävar in avstämningen till föreningens sida, när den lika gärna kan gälla uppdragets egen omfattning. Minsta föreslagna rättelse: stryk "er förening".

Båda invändningarna är kontrollantens påståenden om texten och redaktörens att avgöra. Jag delar dem, men efter den sista jämförelsen ändras ingen prosa, inte heller till en rättelse kontrollanten själv föreslagit.

```markdown
---
kntnt:
  genre: web-copy
  technique: abt
  language: sv
---

# Genomgång av bokningsrutinen för en gemensam lokal

Svale går igenom hur bokningen av föreningens gemensamma lokal fungerar i dag och sammanställer rutinen skriftligt. Uppdraget vänder sig till styrelser i mindre bostadsrättsföreningar och är avgränsat: ni får en gemensam bild av rutinen och två möjliga förenklingar att ta ställning till.

## Det här ingår

Uppdraget består av två delar:

- Ett videomöte på 45 minuter med två representanter för styrelsen.
- En skriftlig sammanställning av nuvarande steg, oklarheter och två möjliga förenklingar.

## Det här ingår inte

Genomgången omfattar inte juridisk rådgivning, installation av bokningssystem eller intervjuer med boende. Någon garanti för en viss tidsbesparing eller för färre konflikter lämnas inte.

## Pris och förutsättningar

Fast pris är 4 800 SEK inklusive moms. Uppdraget gäller en lokal i en förening.

Styrelsen behöver kunna beskriva föreningens befintliga bokningsregler och visa den nuvarande instruktionen till de boende.

## Så anmäler ni intresse

En intresseanmälan är inte en beställning, och den kräver inga betalningsuppgifter. I formuläret anger ni namn, förening och e-postadress.

Därefter svarar Svale via e-post inom tre arbetsdagar, för att stämma av om uppdraget passar er förening och föreslå en tid för mötet.

[Skicka en intresseanmälan](https://example.invalid/svale/intresse) — länken öppnar Svales formulär för intresseanmälan.
```

## Så löstes körningen ut

- **Genre:** `web-copy`, angiven i anropet.
- **Teknik:** `abt`, angiven i anropet. Genren `web-copy` anger själv ingen teknik den ordinarie skrivs med, så arcen kommer från anropet och inte från genren. Den ligger på sektionsnivå: varje avsnitt svarar på en egen läsarfråga, och den genomgående båren är att erbjudandet är avgränsat och utan utlovat resultat, varför vägen in är en icke bindande intresseanmälan.
- **Språk:** `sv`, angivet i anropet och verifierat mot installerad språkresurs.
- **Kntnt-karta:** på, som standard. Underlaget hade ingen frontmatter, så ingen konfiguration hämtades därifrån. Ingen kontextuell instruktion gavs.
- **Destination:** svaret. Ingen av körningens egna filer finns kvar i arbetskatalogen, som nu innehåller `source.md` och en tom `scratch`-katalog.

## Var materialet tog slut

Briefen bad om cirka 300 ord "om materialet bär det". Sidan landar på drygt 200 ord, och resten bär underlaget inte utan att något hittas på.

Det som skulle sluta gapet: betalningsvillkor och leveranstid för sammanställningen — båda uttryckligen inte angivna i underlaget och därför inte skrivna — vad de 45 minuterna går igenom steg för steg, vad som händer efter att sammanställningen är levererad, och vilka situationer genomgången passar för.

Briefen ber läsaren kunna avgöra om en genomgång är relevant. Underlaget ger inga kriterier för den bedömningen utöver förutsättningarna och avgränsningen, så sidan säger vad som ingår, vad som inte ingår, vad det kostar och vad som krävs, och lämnar bedömningen till styrelsen.

## Vilka jämförelser som kördes

Två jämförelser mot underlaget kördes, var och en i en ny agent med eget kontextfönster och utan samtalshistorik.

Den första rapporten nådde körningen bara delvis: kontrollanten skrev ingen rapportfil, och mitt eget upptag av svaret klippte rapportens början, så anspråksredovisningen kunde inte granskas. Dess enda invändning — att "Har ni det, finns underlaget som genomgången utgår från" gjorde ett villkor till en garanti och påstod något om vad genomgången utgår från — åtgärdades genom att meningen ströks.

Den andra jämförelsen läste prosan ovan, redovisade 21 anspråkspar plus en egen redovisning av pronomenens person, numerus och genus, och avslutades med fullständig status. Den är körningens sista jämförelse, och de två invändningarna överst kommer från den.

En öppen redaktionell fråga, som kontrollanten inte rapporterar som brist: orden "formuläret" och "Svales formulär" namnger en inlämningsmekanism som underlaget inte namnger — underlaget säger bara att intresseanmälan sker på adressen och efterfrågar tre uppgifter. Ett mekanismneutralt alternativ, om det föredras, är "På sidan anger ni namn, förening och e-postadress." och "— länken öppnar Svales intresseanmälan."

Ingen översättningsinvändning uppstod: underlag och utkast är båda på svenska, och utkastet innehåller inga citat.

---

*Noteringar utanför Skillens leverans, på observatörens begäran:* källkontrollens scratch-katalog är kopierad i sin helhet till `evidence/` i körkatalogen, inklusive den avklippta första svarstexten, och detta svar är sparat som `response.md` där.
