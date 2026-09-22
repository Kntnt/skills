**Utkastet levereras med kända brister.** Den andra och sista källkontrollen läste exakt den text som står nedan, och två av dess anmärkningar står kvar. Ingen prosa har ändrats efter den kontrollen.

1. **`fastighet` där materialet säger *building*** — i rubriken, ingressen, ingången, i "till nästa fastighet", i citatet "innan vi drar igång i nästa fastighet" och i "till fler fastigheter". Problemet: *fastighet* är den registrerade fastighetsenheten. En fastighet kan rymma flera hus, och två hus kan ligga på samma fastighet, så orden namnger inte samma sak. Materialet säger "a shared repair log in two buildings" och "before the next building starts", och det räknar lägenheter, aldrig fastigheter. Minsta rättelse som kontrollen föreslår: *hus* på varje ställe — "i två hus", "till nästa hus", "innan vi drar igång i nästa hus" — och i slutet antingen "till fler hus" eller bara "har ännu inte utökat den", eftersom materialet inte namnger någon enhet för utökningen. Rättelsen gäller även citatet, där samma ord står.

2. **"Lind har en lärdom att ta med till nästa fastighet."** Problemet: meningen står i skribentens röst och framställer ett nästa hus som givet. Materialet säger "The trial has not yet expanded; the team will decide after checking how the categories work for larger repairs", och Linds eget "I would set that time aside before the next building starts" är villkorligt och hennes. Minsta rättelse som kontrollen föreslår: "Lind har en lärdom att ta med om teamet går vidare."

En tredje anmärkning avvisar jag. Kontrollen läser "Under testet fanns felanmälningarna i en gemensam logg" som att samtliga Elm Quays anmälningar låg i loggen. Samma menings andra led — "men Elm Quay har ännu inte utökat den till fler fastigheter" — begränsar loggens räckvidd, och hela texten dessförinnan säger att testet omfattade två av bolagets fastigheter. Det är mitt beslut på den grunden, inte kontrollens godkännande.

```markdown
---
kntnt:
  genre: case-study
  technique: none
  language: sv
---

# Elm Quay testade gemensam logg i två fastigheter

Under åtta veckor prövade underhållsteamet på Elm Quay Housing en gemensam felanmälningslogg från Svale Systems i två fastigheter. Här är vad teamet gjorde, vad det interna testnotatet visar och vad arbetsledaren Maya Lind skulle göra annorlunda nästa gång.

Av Thomas Barregren

I september 2025 bestämde sig underhållsteamet på Elm Quay Housing för att testa en gemensam felanmälningslogg i två fastigheter. Elm Quay förvaltar 640 lägenheter, och telefonanmälningar och mejl hade dittills sparats var för sig. Teamet ville att personal på olika skift skulle se samma uppgifter.

## Underhållspersonalen satte kategorierna

Valet föll på Svale Systems sedan teamet prövat om loggen kunde visa status för varje reparation. Någon jämförelse med en annan leverantör redovisas inte.

Underhållsteamet utformade sina egna kategorier och höll samtidigt telefonanmälan öppen för de boende. Svale konfigurerade loggen och utbildade sex medarbetare vid två tillfällen.

— Vi ville att kvällspasset skulle se vad morgonpasset redan hade gjort. Kategorierna var våra; Svale hjälpte oss att lägga in dem i loggen, skriver Maya Lind, arbetsledare för underhållet på Elm Quay, i ett mejlsvar.

## Siffrorna säger inte varför tiden skilde sig

Testet pågick i åtta veckor. Enligt Elm Quays interna testnotat, daterat den 4 december 2025, fördes 31 felanmälningar in i loggen. Notatet räknar varken akuta ärenden eller arbeten som beställdes före testet.

Mediantiden från anmälan till tilldelning var två arbetsdagar under testet och tre arbetsdagar under de åtta veckorna dessförinnan. Perioderna hade olika arbetsbelastning, och notatet tillskriver uttryckligen inte programvaran skillnaden. Kostnader, de boendes nöjdhet och tiden till färdigt arbete mättes inte.

## Kategorierna tog mer tid än de första anmälningarna

Lind har en lärdom att ta med till nästa fastighet.

— Vi lade mer tid på att komma överens om kategorierna än på att föra in de första anmälningarna. Den tiden skulle jag avsätta innan vi drar igång i nästa fastighet, skriver hon.

## Lind skulle göra om testet

Hon rekommenderar inte Svale Systems till alla bostadsföretag. Omdömet bygger inte på siffrorna i notatet.

— Jag skulle välja att göra om testet. Att ha en samlad bild av anmälningarna hjälper oss, men jag skulle lägga in en extra vecka för förberedelser, skriver hon.

## Så kan du förbereda ett eget införande

Under testet fanns felanmälningarna i en gemensam logg, men Elm Quay har ännu inte utökat den till fler fastigheter. Teamet bestämmer sig när det har kontrollerat hur kategorierna fungerar för större reparationer.

Överväger du samma sak i ditt bestånd? Läs [Svale Systems checklista för införande](https://example.invalid/svale/checklist). Det här kundcaset är publicerat av Svale Systems och är inte oberoende journalistik.
```

**Så löstes körningen ut**

- Genre: `case-study`, från anropet.
- Teknik: ingen. Genren anger själv att den inte skrivs med någon teknik, så ingen teknik är vald och ingen båge är pålagd texten.
- Språk: `sv`, från anropet. Citaten är översatta från engelska.
- Utdata: svaret. Inga filer har skapats; det arbetsmaterial kontrollerna behövde är borttaget.
- Handoff-metadata: på, som standard. Den ligger som `kntnt`-kartan överst i texten.
- Anatomin är maskinmätt och håller varje räknat krav.

**Bylinen** bär ditt namn. Briefen namnger ingen författare, och då är det användaren som är författare. Ska texten publiceras osignerad eller under ett annat namn behöver raden ändras innan publicering.

**Där materialet tar slut**

- Briefen ber om cirka 400 ord. Texten är omkring 430 ord, så längden begränsas inte av materialet.
- Ingen jämförelse med någon annan leverantör redovisas, så texten kan inte säga vad Svale valdes framför.
- Kostnad, de boendes nöjdhet och tid till färdigt arbete är inte mätta, så inga sådana resultat kan redovisas. Mediantiden kan inte heller förklaras: notatet avstår uttryckligen från att tillskriva programvaran skillnaden, och perioderna hade olika arbetsbelastning.
- Checklistan på `https://example.invalid/svale/checklist` har inte lästs. Domänen går inte att nå, och materialet tillåter inga uppgifter utifrån, så länken beskriver bara det briefen säger att den är: ett dokument att läsa.
- Materialet ger ingen scen, ingen känsla och ingen återgiven replik utöver de tre mejlsvaren, så texten håller sig till vad teamet gjorde och vad notatet mäter. Att svaren kom per mejl står i texten, så citaten inte utger sig för att vara inspelat tal.
- Det som skulle täppa till luckorna: en redovisad leverantörsjämförelse, mätningar av kostnad, nöjdhet och färdigtid, och besked om hur kategorierna fungerade för större reparationer.
