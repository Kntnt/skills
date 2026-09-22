Granskad som `case-study` på `sv`, utan teknik: genre, teknik och språk kom alla ur textens `kntnt`-karta, och kartans `none` avgjorde tekniken, så genrens båge tillämpades inte. Korrigeringsbudgeten var 1 och en runda användes. Loopen stannade där: omgranskningen av den korrigerade texten hittade brister som rundans egen reparation skapade, och budgeten var samtidigt slut.

```markdown
---
kntnt:
  genre: case-study
  technique: none
  language: sv
---

# Bostadsbolaget tillskriver inte loggen kortare tid

Ett bostadsbolag med 640 lägenheter testade en gemensam logg för felanmälningar i två av sina hus under åtta veckor. Mediantiden från anmälan till tilldelning var då kortare än under de åtta veckorna före, men bolagets egen notering skriver inte det på programvarans konto. Arbetsledaren skulle göra om testet, med en vecka till för förberedelser.

Av Thomas Barregren

Telefonanmälningar lagrades för sig, e-post för sig. Hos Elm Quay Housing, ett bostadsbolag som förvaltar 640 lägenheter, bestämde underhållsteamet i september 2025 att testa en gemensam logg för felanmälningar i två av husen. Testet pågick i åtta veckor och är dokumenterat i en intern notering från den 4 december 2025.

## Loggen prövades innan leverantören valdes

Underhållsteamet valde Svale Systems efter att ha prövat om loggen kunde visa status för varje reparation. Någon jämförelse med en annan leverantör redovisas inte.

Maya Lind, arbetsledare för underhållet, säger:

– Vi ville att kvällsskiftet skulle se vad morgonskiftet redan hade gjort. Kategorierna var våra; Svale hjälpte oss att lägga in dem i loggen.

## Kategorierna tog mer tid än de första anmälningarna, säger Lind

Svale Systems konfigurerade loggen och utbildade sex medarbetare vid två tillfällen. Underhållsteamet lät de boende fortsätta anmäla fel per telefon.

Lind säger vad hon skulle göra annorlunda:

– Vi lade mer tid på att enas om kategorierna än på att registrera de första anmälningarna. Den tiden skulle jag avsätta innan starten i nästa hus.

## Noteringen förklarar inte skillnaden med programvaran

Två arbetsdagar var mediantiden från anmälan till tilldelning under testet, mot tre under de åtta veckorna dessförinnan. Perioderna hade olika arbetsbelastningar, och noteringen avstår uttryckligen från att tillskriva programvaran skillnaden.

Under testet registrerades 31 felanmälningar, enligt samma notering. Akuta ärenden och arbeten som beställts före testet är inte medräknade. Kostnader, de boendes nöjdhet och tid till avslutat arbete mättes inte.

## Utvidgningen är inte avgjord än

Lind rekommenderade inte Svale Systems till alla bostadsbolag. Testet har ännu inte utvidgats, och teamet avgör frågan när det har sett hur kategorierna fungerar för större reparationer. Så här sammanfattar hon testet:

– Jag skulle välja att göra testet igen. Att ha en samlad bild av anmälningarna hjälper oss, men jag skulle lägga in en extra vecka för förberedelser.

Texten publiceras av Svale Systems och är inte oberoende journalistik. Vill du gå vidare, är nästa steg att läsa [Svale Systems checklista för införande](https://example.invalid/svale/checklist).
```

## Kvarstående brister

De fyra bristerna som granskningen fann är åtgärdade. De tre nedan är olösta och kom alla ur den enda korrigeringsrundans egna reparationer, så de är kvar för en människa att avgöra.

**1. Rubriken upprepar ingressen och en mellanrubrik.** *Olöst.* Rubriken "Bostadsbolaget tillskriver inte loggen kortare tid" säger samma sak som ingressens andra mening, "bolagets egen notering skriver inte det på programvarans konto", och samma sak som mellanrubriken "Noteringen förklarar inte skillnaden med programvaran". Texten framför nu sitt enda icke-tillskrivande tre gånger, och rubriken namnger inte längre vad reportaget handlar om. Rubrik och ingress ska säga olika saker med olika ord, och en case-studys rubrik ska namnge kundens nytta eller resultat. Bristen följde av reparationen av den tidigare rubriken "Gemensam logg gav överblick över felanmälningarna", som påstod ett resultat i textens egen röst som bara Maya Linds citat bär.

**2. Mellanrubriken säger citatet under den i förväg.** *Olöst.* "Kategorierna tog mer tid än de första anmälningarna, säger Lind" är citatets första mening omskriven: "Vi lade mer tid på att enas om kategorierna än på att registrera de första anmälningarna." Läsaren får samma tanke två gånger, och citatet landar som en bekräftelse i stället för som kundens egen röst. Bristen följde av reparationen av den tidigare mellanrubriken "Boende kunde ringa in felen som tidigare", som bara täckte en bisak i sektionen.

**3. Mellanrubriken står ovanför sin egen omskrivning.** *Olöst.* "Loggen prövades innan leverantören valdes" följs nu direkt av "Underhållsteamet valde Svale Systems efter att ha prövat om loggen kunde visa status för varje reparation." En mellanrubrik och sektionens första mening ska komplettera varandra, inte upprepa varandra. Bristen följde av reparationen av det tredubbla förhandsbeskedet i samma sektion: den mening som tidigare inledde sektionen togs bort, och omskrivningen hamnade direkt under rubriken.

## Påståenden som rundan tog eller flyttade

- **Borttaget:** "Underhållsteamet ville att personal på olika skift skulle se samma uppgifter." Reparationen av det tredubbla förhandsbeskedet tog meningen, som var en av de tre gångerna samma tanke sades. Innehållet finns kvar, men bara som Linds citat, så attributionen flyttade från texten till talaren.
- **Borttaget:** rubrikens påstående att den gemensamma loggen gav överblick över felanmälningarna. Reparationen av rubriken tog det, eftersom bristen namngav just det påståendet. Linds egen värdering, "Att ha en samlad bild av anmälningarna hjälper oss", står oförändrad kvar i slutcitatet.
- **Borttaget:** mellanrubrikens påstående att de boende kunde ringa in felen som tidigare. Reparationen av den mellanrubriken tog det. Sakuppgiften står oförändrad kvar i brödtexten: "Underhållsteamet lät de boende fortsätta anmäla fel per telefon."
- **Ändrat:** bryggan "Lind säger vad hon skulle göra annorlunda inför nästa hus:" blev "Lind säger vad hon skulle göra annorlunda:". Reparationen av motsägelsen mot slutsektionen tog bort "inför nästa hus", så texten påstår inte längre i egen röst att ett nästa hus finns. Påståendet står kvar där det alltid var kvalificerat: i Linds citat och i slutsektionens "Testet har ännu inte utvidgats".

Ingen mening som avgränsar vad texten påstår togs bort eller försvagades. Att ingen jämförelse med en annan leverantör redovisas, att noteringen avstår från att tillskriva programvaran skillnaden, vad som inte är medräknat, vad som inte mättes, att Lind inte rekommenderade Svale Systems till alla bostadsbolag och att texten publiceras av Svale Systems och inte är oberoende journalistik står alla kvar ord för ord.

Inget skrevs till disk: texten levereras här, och `input.md` är oförändrad.
