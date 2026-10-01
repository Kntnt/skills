**Konfiguration:** genre `casestudy` (från anropet), språk `sv` (från anropet), ingen teknik. Genren casestudy anger ingen teknik som den vanligen skrivs med, så ingen berättarbåge har tillämpats.

```markdown
# Gemensam ärendebild hjälper, säger Elm Quay om loggförsöket

**Elm Quay Housing provade en gemensam reparationslogg i två hus under åtta veckor. Arbetsledaren Maya Lind vill göra om försöket, men skulle avsätta mer tid för förberedelser. Här är vad gruppen gjorde, vad anteckningarna visar och vad hon skulle ändra.**

Text: Iris Falk

Att se samma information över skiftgränserna var vad underhållsgruppen på Elm Quay Housing ville få ut av sin gemensamma reparationslogg. Försöket pågick i åtta veckor och omfattade två hus.

## Gruppen enades om kategorierna först

Kategorierna i loggen var underhållsgruppens egna. Leverantören Svale konfigurerade loggen efter dem och utbildade sex medarbetare.

– Vi lade mer tid på att enas om kategorierna än på att lägga in de första ärendena. Den tiden skulle jag avsätta innan nästa hus börjar, säger Maya Lind, arbetsledare på Elm Quay.

## Två perioder med olika arbetsbelastning

Enligt Elm Quays interna försöksanteckning från den 4 december 2025 registrerades 31 ärenden under åtta veckor. Akuta ärenden och tidigare beställda arbeten ingick inte. Mediantiden från anmälan till tilldelning var två arbetsdagar. Under de föregående åtta veckorna var den tre.

Perioderna hade olika arbetsbelastning, och anteckningen tillskriver därför inte skillnaden programvaran.

## Arbetsledaren ser tillbaka på försöket

– Jag skulle välja att göra försöket igen. Att ha en gemensam bild av ärendena hjälper oss, men jag skulle lägga till en vecka för förberedelser, säger Lind.

Kundcaset publiceras av leverantören Svale. Den som står inför samma förberedelser kan börja i [Svales checklista för införandet](https://example.invalid/svale/checklist).
```

**Fynd**

1. **Inledningsstycket, tredje meningen:** "Vad det krävde, och vad det gav, går att följa i gruppens egna anteckningar."
   - Meningen lovade att anteckningarna visar vad försöket gav. Avsnittet "Två perioder med olika arbetsbelastning" säger däremot att anteckningen inte tillskriver skillnaden programvaran.
   - Det försöket krävde, alltså tiden för att enas om kategorierna, berättar Maya Lind. Anteckningen säger inget om det.
   - Meningen sa också om ingressens "Här är vad gruppen gjorde, vad anteckningarna visar" med andra ord i stället för att föra texten framåt.
   - **Åtgärdat:** meningen är struken.

Inga fynd återstår.

**Påståenden**

- **Borttaget:** påståendet att det försöket krävde och det det gav går att följa i gruppens egna anteckningar.
  - Det ströks av rättelsen av fynd 1, som pekade ut just det påståendet som felet.
  - Den som läser inledningsstycket får inte längre veta där att redogörelsen bygger på gruppens anteckningar.
  - Brödtexten anger fortfarande källan som Elm Quays interna försöksanteckning från den 4 december 2025. Meningen om att anteckningen inte tillskriver skillnaden programvaran står kvar oförändrad.
- Utöver det borttagna påståendet ovan har inget påstående ändrats eller lagts till.

**Artikelanatomi:** Texten följer artikelanatomin utan avvikelse.
- Mätskriptet godkänner de räknade kraven för den levererade texten. Inledningsstycket är nu ett stycke på 29 ord.
- De krav skriptet inte räknar har jag granskat genom läsning:
  - ingressen står på egen hand
  - inledningsstycket inleder ämnet, börjar med andra ord än ingressen och för texten framåt
  - mellanrubrikerna beskriver sina avsnitt
  - sista avsnittet är ett avslut med uppmaning.

Utöver påståendet ovan har körningen strukit en mening i inledningsstycket. Därmed försvann inledningsstyckets omtagning av ingressens "Här är vad gruppen gjorde, vad anteckningarna visar". Inledningsstycket nämner fortfarande ingressens uppgifter om två hus, åtta veckor och en gemensam reparationslogg. Den avslutande korrekturläsningen gjorde inga rättelser.