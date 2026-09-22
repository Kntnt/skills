Texten är granskad, en korrigeringsrunda är spenderad, och den mekaniska genomgången är körd sist. Här är artefakten som den står nu.

```markdown
---
kntnt:
  genre: case-study
  technique: none
  language: sv
---

# Elm Quay lät två skift dela samma reparationslogg

Åtta veckor, två fastigheter och en logg som skulle visa status för varje reparation. Så såg testet ut när bostadsföretaget Elm Quay Housing prövade Svale Systems. Här är vad underhållsteamet gjorde, vad den interna testanteckningen visar och vad arbetsledaren Maya Lind skulle avsätta mer tid för nästa gång.

Av Thomas Barregren

Hos Elm Quay Housing, ett bostadsföretag som förvaltar 640 lägenheter, förvarades felanmälningarna per telefon på ett ställe och per e-post på ett annat. I september 2025 beslutade det egna underhållsteamet att pröva en gemensam reparationslogg i två av fastigheterna. Testet pågick i åtta veckor och dokumenterades i en intern anteckning.

## Elm Quay valde Svale, som konfigurerade loggen

Underhållsteamet utformade kategorierna självt och lät de boende fortsätta anmäla fel per telefon. Svale Systems konfigurerade loggen och utbildade sex medarbetare vid två tillfällen.

Teamet valde Svale efter att ha undersökt om loggen kunde visa status för varje reparation. Någon jämförelse med någon annan leverantör redovisas inte. Maya Lind, arbetsledare för underhållet, beskriver i en intervju via e-post vad teamet var ute efter.

– Vi ville att kvällsskiftet skulle se vad morgonskiftet redan hade gjort. Kategorierna var våra. Svale hjälpte oss att lägga in dem i loggen, säger hon.

## Siffrorna gäller tid till tilldelning, inte orsak

I Elm Quays interna testanteckning, daterad den 4 december 2025, står att 31 felanmälningar registrerades under testet. Akuta ärenden och arbete som beställts innan testet började räknas inte in. Mediantiden från anmälan till tilldelning var två arbetsdagar under testperioden och tre under de åtta veckorna dessförinnan.

Perioderna hade olika arbetsbelastningar, och anteckningen tillskriver uttryckligen inte skillnaden till programvaran. Det finns inga mätningar av kostnader, de boendes nöjdhet eller färdigställandetid.

## Teamet ska kontrollera kategorierna för större reparationer

Testet har ännu inte utvidgats. Teamet ska först kontrollera hur kategorierna fungerar för större reparationer.

– Vi lade mer tid på att enas om kategorierna än på att registrera de första anmälningarna. Den tiden skulle jag avsätta innan nästa fastighet drar i gång, säger Maya Lind.

## Maya Lind skulle testa igen men rekommenderar inte Svale till alla

– Jag skulle välja att göra testet igen. Att ha en samlad bild av anmälningarna hjälper oss, men jag skulle lägga in en extra vecka för förberedelser, säger Maya Lind.

Hon rekommenderar inte Svale till alla bostadsföretag.

Vill ni pröva samma sak hos er? Börja med [Svale Systems implementeringschecklista](https://example.invalid/svale/checklist). Den här kundberättelsen publiceras av Svale Systems.
```

## Så lästes texten

Genre `case-study`, språk `sv`, ingen teknik. Alla tre stod i dokumentets `kntnt`-block. Värdet `none` för teknik säger att ingen teknik tillämpas, så genrens egen anvisning om vilken båge en kundberättelse normalt skrivs med lämnades därhän; `case-study` anvisar för övrigt ingen. Artikelanatomins räknade krav är maskinmätta, och texten uppfyller dem.

## Kvarstående iakttagelser

Båda är olösta, och båda är skapade av den här körningens egen rättelse. Det är därför slingan stannade: nästa runda hade rättat vad rundan före den gjorde, och vad som ska stå i de två mellanrubrikerna är en fråga för en människa.

**Mellanrubriken "Teamet ska kontrollera kategorierna för större reparationer" upprepar meningen under den.** Avsnittets andra mening lyder "Teamet ska först kontrollera hur kategorierna fungerar för större reparationer." En mellanrubrik och texten under den ska komplettera varandra, inte säga samma sak, och den som skummar får här samma mening två gånger på två rader. Rubriken kom till när körningen rättade den tidigare rubriken "Beslutet kommer efter en kontroll av kategorierna", som stod i bestämd form utan att något beslut hade införts i texten, som påstod att ett beslut kommer, och som gjorde om avsnittets eget verb till substantiv. Den rättelsen tog bort de felen och lade upprepningen i stället.

**Mellanrubriken "Maya Lind skulle testa igen men rekommenderar inte Svale till alla" säger i förväg vad avsnittet säger.** Direkt under den står citatet "– Jag skulle välja att göra testet igen" och strax därefter "Hon rekommenderar inte Svale till alla bostadsföretag." En rubrik som föregriper citatet under sig tar udden av citatet, och kundberättelsens form vill att en brygga förbereder ett citat i stället för att säga det först. Rubriken kom till när körningen rättade den tidigare rubriken "Läs checklistan innan ni sätter i gång", som bara beskrev avsnittets sista stycke och som växlade till en uppmaning riktad till läsaren från leverantörens håll, mitt i den del där kundens eget omdöme står.

## Påståenderedovisning

Rättelsen av mellanrubriken "Beslutet kommer efter en kontroll av kategorierna" tog bort rubrikens påstående att ett beslut kommer efter kontrollen. Iakttagelsen pekade ut just det påståendet som felet: texten säger att testet ännu inte har utvidgats och att teamet först ska kontrollera hur kategorierna fungerar för större reparationer, men inte att ett beslut följer på kontrollen. Borttagandet står därför kvar, och det redovisas här.

Inget annat påstående togs bort. Inget påstående lämnades kvar med ändrad räckvidd, säkerhet, källa, kronologi, orsak eller innebörd. De meningar som avgränsar vad texten hävdar — att ingen jämförelse med någon annan leverantör redovisas, att anteckningen uttryckligen inte tillskriver skillnaden till programvaran, att kostnader, nöjdhet och färdigställandetid inte är mätta, att Maya Lind inte rekommenderar Svale till alla bostadsföretag, och att Svale Systems publicerar berättelsen — står alla kvar ordagrant.
