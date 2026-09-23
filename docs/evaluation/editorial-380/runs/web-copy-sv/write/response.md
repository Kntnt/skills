**Utkastet levereras med kända brister.** Den avslutande källkontrollen lämnade två invändningar som inte är åtgärdade i texten. En åtgärd som ingen fullständig jämförelse har läst är okontrollerad text, och det som levereras är den text den sista jämförelsen läste.

1. **Rubriken: "föreningens gemensamma lokal".** Den bestämda formen förutsätter att föreningen har en enda gemensam lokal. Underlaget skriver "en avgränsad genomgång av rutinerna för bokning av *en gemensam lokal*" och "Uppdraget gäller *en lokal i en förening*" — en gräns som förutsätter att det kan finnas fler. En förening med både festlokal och gästlägenhet är förenlig med underlaget, och inget led i underlaget utesluter den. Minsta belagda åtgärd, enligt kontrollen: "Genomgång av bokningsrutinen för en gemensam lokal".

2. **"för att stämma av om uppdraget passar er".** Underlaget skriver "för att stämma av om uppdraget passar", utan bestämning. Utkastet lägger till vems passform som prövas. Avstämningen kan lika gärna vara Svales egen prövning av om ärendet ryms i erbjudandet — föreningen vill ha tre lokaler genomgångna, eller juridisk rådgivning, och Svale tackar nej. Minsta belagda åtgärd, enligt kontrollen: stryk "er".

Båda är vad kontrollen hävdar och vad du som redaktör avgör, inte fastställda fel i texten.

```markdown
---
kntnt:
  genre: web-copy
  technique: none
  language: sv
---

# Genomgång av bokningsrutinen för föreningens gemensamma lokal

Svale gör en avgränsad genomgång av hur bokningen av en gemensam lokal fungerar i er förening i dag, och lämnar två förslag på hur rutinen kan förenklas. Genomgången vänder sig till styrelsen i en mindre bostadsrättsförening.

## Det här ingår i genomgången

- Ett videomöte på 45 minuter med två representanter för styrelsen.
- En skriftlig sammanställning av nuvarande steg, oklarheter och två möjliga förenklingar.

Efter genomgången har styrelsen en gemensam bild av hur bokningen går till och två möjliga förenklingar att ta ställning till.

## Det här ingår inte i genomgången

Juridisk rådgivning, installation av bokningssystem och intervjuer med boende.

## Pris och omfattning

Fast pris är 4 800 SEK inklusive moms. Uppdraget gäller en lokal i en förening.

Svale lämnar ingen garanti för en viss tidsbesparing eller för färre konflikter.

## Förutsättningar

Styrelsen behöver kunna beskriva föreningens befintliga bokningsregler och visa nuvarande instruktion till de boende.

## Så anmäler ni intresse

En intresseanmälan är ingen beställning och kräver inga betalningsuppgifter. Den efterfrågar namn, förening och e-postadress.

Svale svarar via e-post inom tre arbetsdagar för att stämma av om uppdraget passar er och för att föreslå en tid för mötet.

[Skicka en intresseanmälan](https://example.invalid/svale/intresse)
```

## Så löstes körningen ut

- **Genre:** web-copy, angiven i anropet.
- **Teknik:** ingen. Web-copy anger ingen teknik som genren vanligen skrivs med, och ingen teknik kom från anropet, från underlagets frontmatter eller från någon instruktion. Sidan har därför ingen påbjuden båge, bara den disposition sidans uppgift kräver.
- **Språk:** svenska (`sv`), angivet i anropet och verifierat mot installerad språkresurs.
- **Utdata:** svaret. Inget skrevs till filsystemet. Arbetsfilerna för källkontrollen är borttagna, och `source.md` är oförändrad.
- **Frontmatter:** på, som är grundvärdet. Kartan `kntnt` bär genre, teknik och språk och inget annat.
- **Byline:** ingen. Sidan är avsändarmärkt med Svale, som underlaget anger, så inget författarnamn har lagts till.

## Där underlaget tog slut

Briefen ber om cirka 300 ord "om materialet bär det". Brödtexten är cirka 200 ord. Underlaget bär inte mer utan påhitt: det säger uttryckligen att betalningsvillkor och leveranstid för sammanställningen inte är angivna, och det utesluter kundcitat, betyg, provperioder, lediga platser, kampanjdatum, garantier och jämförelser med konkurrenter.

Det här skulle stänga gapet:

- betalningsvillkor, och när sammanställningen levereras efter mötet
- vad de 45 minuterna går igenom, steg för steg
- i vilken form sammanställningen kommer och ungefär hur lång den är
- vem hos Svale som gör genomgången
- vad som händer efter att sammanställningen är levererad
- vilka slags oklarheter en genomgång brukar hitta

## Två redaktionella frågor

Kontrollen lämnade dem som frågor till dig, inte som brister, och föreslog ingen åtgärd för någon av dem.

- "Genomgången vänder sig till styrelsen i en mindre bostadsrättsförening." Briefen fastställer vem sidan är skriven för, inte en begränsning av vem som kan köpa genomgången.
- Den gemensamma bilden tillskrivs hela styrelsen, fast två representanter deltar i mötet. Så uttrycker briefen det själv ("vad styrelsen faktiskt får"), och det bärs som Svales egen utsaga.

## Vilka jämförelser som kördes

Två fullständiga källkontroller, båda av färska granskare utan samtalshistorik. Den första lämnade tre invändningar, alla godtagna och åtgärdade: kvalifikationen "möjliga" återställdes i meningen om vad styrelsen får, "nuvarande instruktion till de boende" återställdes till underlagets bestämning, och ett obelagt "formulär" togs bort ur intresseanmälan. Den andra läste den rättade texten och lämnade de två invändningar som står överst. Jämförelserna gällde källtäckning och översatta citat; allmän redaktionell granskning och språkmekanik ingick inte i dem.
