**Utkastet levereras med en känd defekt.** Den avslutande jämförelsen lämnade en anmärkning om källtäckning; inga anmärkningar om översättningen av citaten.

- **Passagen i utkastet:** rubriken `# Gemensam logg gav överblick över felanmälningarna`
- **Problemet:** rubriken påstår en uppnådd effekt rakt av, i preteritum och i utgivarens röst, och `felanmälningarna` i bestämd form omfattar felanmälningarna som klass.
- **Vad materialet bär i stället:** en avsikt ("The team wanted staff on different shifts to see the same information"), en förmåga som prövades ("after testing whether the log could show the status of each repair"), Maya Linds egen kvalificerade bedömning i presens ("Having one view of the reports helps us, but I would leave an extra week for preparation") och en räkning på 31 registrerade anmälningar som "excludes emergencies and work ordered before the trial". Materialet säger ingenstans att varje anmälan hamnade i loggen, så akuta ärenden kan ha tagits emot per telefon utan att registreras där.
- **Minsta reparation som kontrollanten föreslog:** `Arbetsledaren: gemensam logg ger oss en samlad bild av anmälningarna`, eller `Gemensam logg prövades i två hus under åtta veckor`.
- **Varför den inte är åtgärdad:** det var den andra och sista jämförelsen. Text som ändras efter den är text som ingen jämförelse har läst, så utkastet levereras exakt som den jämförelsen läste det.

Anmärkningen är vad jämförelsen hävdar och vad du avgör, inte ett fastställt fel i texten. Jag hävdar ingen källtrohet för rubriken.

```markdown
---
kntnt:
  genre: case-study
  technique: none
  language: sv
---

# Gemensam logg gav överblick över felanmälningarna

Ett bostadsbolag med 640 lägenheter testade en gemensam logg för felanmälningar i två av sina hus under åtta veckor. Mediantiden från anmälan till tilldelning var då kortare än under de åtta veckorna före, men bolagets egen notering skriver inte det på programvarans konto. Arbetsledaren skulle göra om testet, med en vecka till för förberedelser.

Av Thomas Barregren

Telefonanmälningar lagrades för sig, e-post för sig. Hos Elm Quay Housing, ett bostadsbolag som förvaltar 640 lägenheter, bestämde underhållsteamet i september 2025 att testa en gemensam logg för felanmälningar i två av husen. Testet pågick i åtta veckor och är dokumenterat i en intern notering från den 4 december 2025.

## Loggen prövades innan leverantören valdes

Underhållsteamet ville att personal på olika skift skulle se samma uppgifter. Det valde Svale Systems efter att ha prövat om loggen kunde visa status för varje reparation. Någon jämförelse med en annan leverantör redovisas inte.

Maya Lind, arbetsledare för underhållet, beskriver vad teamet var ute efter:

— Vi ville att kvällsskiftet skulle se vad morgonskiftet redan hade gjort. Kategorierna var våra; Svale hjälpte oss att lägga in dem i loggen.

## Boende kunde ringa in felen som tidigare

Svale Systems konfigurerade loggen och utbildade sex medarbetare vid två tillfällen. Underhållsteamet lät de boende fortsätta anmäla fel per telefon.

Lind säger vad hon skulle göra annorlunda inför nästa hus:

— Vi lade mer tid på att enas om kategorierna än på att registrera de första anmälningarna. Den tiden skulle jag avsätta innan starten i nästa hus.

## Noteringen förklarar inte skillnaden med programvaran

Två arbetsdagar var mediantiden från anmälan till tilldelning under testet, mot tre under de åtta veckorna dessförinnan. Perioderna hade olika arbetsbelastning, och noteringen avstår uttryckligen från att tillskriva programvaran skillnaden.

Under testet registrerades 31 felanmälningar, enligt samma notering. Akuta ärenden och arbeten som beställts före testet är inte medräknade. Kostnader, de boendes nöjdhet och tid till avslutat arbete mättes inte.

## Utvidgningen är inte avgjord än

Lind rekommenderade inte Svale Systems till alla bostadsbolag. Testet har ännu inte utvidgats, och teamet avgör frågan när det har sett hur kategorierna fungerar för större reparationer. Så här sammanfattar hon testet:

— Jag skulle välja att göra testet igen. Att ha en samlad bild av anmälningarna hjälper oss, men jag skulle lägga in en extra vecka för förberedelser.

Texten publiceras av Svale Systems och är inte oberoende journalistik. Vill du gå vidare, är nästa steg att läsa [Svale Systems checklista för införande](https://example.invalid/svale/checklist).
```

**Så löstes anropet.** Genre `case-study`, språk `sv` och utdata till svaret kommer alla från anropet. Ingen teknik är pålagd: genren anger ingen teknik den vanligen skrivs med, och ingen nivå över den valde någon, så texten har ingen arc utöver sin egen kronologi. Språkväljaren är verifierad mot installerad språkresurs. `kntnt`-kartan i frontmatter är på, vilket är grundvärdet.

**Var utkastet hamnade.** I svaret ovan, och ingen annanstans. Inget skrevs till filsystemet; arbetsfilerna som jämförelserna behövde är borttagna.

**Bylinen bär ditt eget namn.** Uppdraget namnger ingen författare, så raden lyder `Av Thomas Barregren`. Ska texten publiceras osignerad eller under någon annans namn behöver den rättas före publicering.

**Var materialet tog slut.**

- Ingen jämförelse med någon annan leverantör redovisas, så texten kan inte säga varför valet föll på Svale Systems framför något annat alternativ. Ett jämförelseunderlag skulle fylla den luckan.
- Kostnader, de boendes nöjdhet och tid till avslutat arbete är inte uppmätta, så inget av det står i texten. Mätningar av något av dem skulle bära ett stycke till.
- Noteringen tillskriver uttryckligen inte programvaran den kortare mediantiden, och perioderna hade olika arbetsbelastning. Ingen effekt av loggen påstås därför någonstans, och bara en mätning som håller arbetsbelastningen konstant skulle kunna ändra det.
- Materialet placerar inte testet i kalendern annat än genom beslutet i september 2025 och noteringen den 4 december 2025, så texten anger inga start- eller slutdatum för de åtta veckorna.
- Utvidgningen är inte avgjord, så avslutningen kan inte säga hur det gick sedan.

Längden stannar på ungefär de 400 ord uppdraget bad om, så ingen lucka återstår att fylla där. Två jämförelser kördes: den första ledde till sex reparationer, den andra läste den reparerade texten och lämnade anmärkningen ovan.
