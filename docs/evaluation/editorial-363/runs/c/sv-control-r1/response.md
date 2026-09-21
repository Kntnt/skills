Granskad som **case-study** på **svenska** (`sv`), utan teknik.

- Genren slöts till ur texten själv: anropet angav ingen, och texten bär ingen `kntnt`-karta.
- Ingen teknik tillämpades. Case-study-resursen anger att genren inte skrivs med någon, så genrens nivå lämnade parametern öppen och standardvärdet stod kvar.
- Korrigeringsbudgeten var 1 (standard) och är förbrukad.

```markdown
# Elm Quay samlade reparationsärendena

**Elm Quay Housing provade en gemensam reparationslogg i två hus. Arbetsledaren Maya Lind skulle göra om försöket, men avsätta mer tid för förberedelser.**

För Elm Quays underhållsgrupp handlade försöket med en gemensam reparationslogg om att se samma information över skiftgränserna. Gruppen valde ärendekategorierna; leverantören Svale konfigurerade loggen och utbildade sex medarbetare.

## Mediantiden var två arbetsdagar mot tre veckorna före

Enligt Elm Quays interna försöksanteckning från den 4 december 2025 registrerades 31 ärenden under åtta veckor. Akuta ärenden och tidigare beställda arbeten ingick inte. Mediantiden från anmälan till tilldelning var två arbetsdagar, jämfört med tre under de föregående åtta veckorna.

Perioderna hade olika arbetsbelastning. Anteckningen tillskriver därför inte programvaran skillnaden.

## Kunden skulle göra om försöket

– Vi lade mer tid på att enas om kategorierna än på att lägga in de första ärendena. Den tiden skulle jag avsätta innan nästa hus börjar, säger arbetsledaren Maya Lind.

– Jag skulle välja att göra försöket igen. Att ha en gemensam bild av ärendena hjälper oss, men jag skulle lägga till en vecka för förberedelser, säger Lind.

Kundcaset publiceras av leverantören Svale. [Läs Svales checklista för införandet](https://example.invalid/svale/checklist).
```

## Kvarstående fynd

Tre fynd står kvar, och alla tre är olösta.

**1. Bylinen saknas.** Artikelanatomin kräver en byline mellan ingressen och brödtexten. Mätningen rapporterar `byline: absent`. Varken texten, dess metadata eller anropet namnger någon författare, och en byline som ingen kan namnge rapporteras som saknad och lämnas ofylld — den som lämnar in en text för granskning antas inte ha skrivit den. I en genre där utgivaren är leverantören är det just författaruppgiften som låter läsaren väga texten, så raden behöver fyllas i för hand.

**2. Mellanrubriken `Mediantiden var två arbetsdagar mot tre veckorna före` läser inte på ett svep, och är mer allmän än brödtexten.** Läsaren tar först *tre veckorna* som en tidrymd och måste backa för att lägga till det bortlämnade *arbetsdagar* efter *tre* och läsa om *veckorna före* som tidsangivelse. Rubriken skriver dessutom *Mediantiden* utan avgränsningen *från anmälan till tilldelning* som brödtexten sätter; Headlines kräver att varje ord i en rubrik bärs av texten i textens egen styrka, aldrig mer allmänt. Den som skummar tar med sig en mediantid för reparationen i stället för för sträckan anmälan–tilldelning. Repareras genom att skriva om enbart mellanrubriken.

**3. Mellanrubriken `Kunden skulle göra om försöket` upprepar ingressen och täcker inte sin sektion.** Den säger nästan ordagrant om ingressens andra mening (*Arbetsledaren Maya Lind skulle göra om försöket*) och namnger bara en del av vad som står under den. Sektionens första och största stycke är citatet om var tiden gick och vad Lind skulle avsätta inför nästa hus — förberedelsetiden, som är textens behållning och ingressens andra halva — och den tråden syns nu inte i någon mellanrubrik. Headlines kräver att en mellanrubrik formuleras ur hela sin sektion och kompletterar det som följer i stället för att upprepa det. Repareras genom att skriva om enbart mellanrubriken.

## Varför korrigeringen stannade

Budgeten på 1 förbrukades av en runda. Omgranskningen av den korrigerade texten reste dessutom fynd 2 och 3, och båda är fel som den rundans egna reparationer förde in — texten hade dem inte när den kom in. Fynd 2 följer av omskrivningen av den första mellanrubriken, som svarade på att den gamla rubriken angav avsnittets förbehåll i stället för dess vinkel. Fynd 3 följer av omskrivningen av den sista mellanrubriken, som svarade dels på att rubriken skrev *vill* där brödtexten bara bär *skulle*, dels på att den sa citatet under den i förväg. En ny runda skulle alltså ha reparerat vad rundan före den gjorde. Vart och ett av de två villkoren hade stannat loopen för sig.

Fyra fynd ur den första granskningen är åtgärdade och kom rena genom omgranskningen: ledet är nu ett stycke, brödtexten läses fullständig utan ingressen, förbehållsmeningens ledföljd är återställd, och *kategorierna* heter *ärendekategorierna*.

## Anspråksredovisning

Inget anspråk togs bort. Varje mening, siffra, datum, avgränsning, citat och attribution som texten kom in med finns kvar. Sju anspråk står kvar men har flyttats:

1. **Ingressen**: *Maya Lind vill göra om försöket, men skulle avsätta mer tid* → *skulle göra om försöket, men avsätta mer tid*. Visshetsgraden flyttades tillbaka till talarens egen konditionalis. Flyttad av reparationen av fyndet att *vill* var starkare än brödtexten bär.
2. **Sista mellanrubriken**: *Kunden vill ge förberedelserna mer tid* → *Kunden skulle göra om försöket*. Samma reparation; både visshetsgraden och själva påståendet ändrades.
3. **Första mellanrubriken**: *Två perioder med olika arbetsbelastning* → *Mediantiden var två arbetsdagar mot tre veckorna före*. Påståendet byttes från avsnittets förbehåll till dess mätresultat. Flyttad av reparationen av fyndet att rubriken angav förbehållet i stället för vinkeln. Att det nya påståendet är mer allmänt än brödtextens är fynd 2 ovan.
4. **Attributionen i första citatet**: *säger Maya Lind* → *säger arbetsledaren Maya Lind*. Rollen hämtad ur ingressen, inte tillagd. Flyttad av reparationen som gjorde brödtexten läsbar utan ingressen.
5. **Ledet**: *handlade försöket om* → *handlade försöket med en gemensam reparationslogg om*. Samma reparation; syftningen namngiven med ingressens egna ord.
6. **Ledet**: *kategorierna* → *ärendekategorierna*. Syftningen preciserad till det texten redan säger att loggen innehåller. Flyttad av reparationen av fyndet att bestämd form stod före det den hörde till.
7. **Placeringen av första citatet**: det stod före den första mellanrubriken och står nu först i sista sektionen. Ordalydelsen är oförändrad och ordningen mot det andra citatet bevarad. Flyttat av reparationen av fyndet att ledet var två stycken.

Förbehållsmeningen — *Perioderna hade olika arbetsbelastning. Anteckningen tillskriver därför inte programvaran skillnaden.* — är den mening som avgränsar vad texten hävdar om programvarans verkan. Den står kvar oförsvagad; bara ledföljden inne i den ändrades, så att svenskan sätter den som tillskrivs först.

Den avslutande mekaniska genomgången hittade inga objektiva fel och ändrade ingenting.

Skillen skapade ingen fil och lämnade ingen kvar. Leveransen är texten i det här svaret, och `input.md` är oförändrad.
