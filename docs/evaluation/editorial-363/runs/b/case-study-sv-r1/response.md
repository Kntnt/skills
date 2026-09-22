Utkastet levereras med en känd brist. Den står först, före allt annat om texten.

**Kvarstående anmärkning efter den avslutande jämförelsen** (källstöd, i textens egen berättarröst — inget citat berörs):

- Passage i utkastet: "De boende kunde fortsätta anmäla fel per telefon under hela försöket."
- Problemet: underlaget säger att telefonanmälan hölls öppen för de boende, men ingenting om hur länge. "Under hela försöket" lägger till en varaktighet som underlaget inte bär.
- Vad underlaget bär i stället: "kept telephone reporting open for residents" — utan tidsangivelse.
- Minsta reparation som granskaren föreslog: stryk "hela", alltså "De boende kunde fortsätta anmäla fel per telefon under försöket."

Reparationen är inte införd. Den avslutande jämförelsen läste prosan precis som den står här, och prosa som ingen fullständig jämförelse har läst levereras inte. Anmärkningen är vad granskningen påstår om texten; avgörandet är ditt.

**Avvisad anmärkning, med belägg.** Granskaren ifrågasatte också "därefter" i "Försöket pågick i åtta veckor, och därefter sammanfattade bolaget det i en intern anteckning", med fallet att anteckningen den 4 december skulle vara en delrapport mitt i ett pågående försök. Underlaget utesluter det fallet: anteckningen redovisar "Median time from report to assignment was two working days during the trial and three in the preceding eight-week period" — hela försöksperioden ställd mot de åtta veckorna före. En anteckning som redovisar hela perioden är skriven efter den.

```markdown
---
kntnt:
  genre: case-study
  technique: none
  language: sv
---

# Elm Quay testade gemensam logg för felanmälningar

Ett bostadsföretag som förvaltar 640 lägenheter lät under åtta veckor två hus arbeta i ett och samma system för felanmälan. Här är vad Elm Quay Housing gjorde, vad den interna anteckningen faktiskt visar och vad arbetsledaren skulle göra annorlunda nästa gång. Underlag för dig som funderar på ett eget försök.

Av Thomas Barregren

I september 2025 bestämde underhållsteamet på Elm Quay Housing att pröva en gemensam logg för felanmälningar i två hus. Fram till dess sparades telefonanmälningar och mejl var för sig. Försöket pågick i åtta veckor, och därefter sammanfattade bolaget det i en intern anteckning.

## Valet föll på Svale efter ett statustest

Elm Quay Housing förvaltar 640 lägenheter, och initiativet till försöket kom från det egna underhållsteamet. Inför valet testade bolaget om loggen kunde visa status för varje reparation, och valde därefter Svale Systems. Någon jämförelse med andra leverantörer redovisas inte.

— Vi ville att kvällsskiftet skulle se vad morgonskiftet redan hade gjort. Kategorierna var våra. Svale hjälpte oss att lägga in dem i loggen, skriver Maya Lind, arbetsledare för underhållet, i ett mejl.

## Elm Quay behöll telefonanmälan och byggde egna kategorier

Svale Systems konfigurerade loggen och utbildade sex medarbetare vid två tillfällen. De boende kunde fortsätta anmäla fel per telefon under hela försöket. Förberedelserna är det Maya Lind återkommer till.

— Vi lade mer tid på att komma överens om kategorierna än på att registrera de första felanmälningarna. Den tiden skulle jag avsätta innan nästa hus börjar, skriver hon.

## Siffrorna knyter inte den kortare tiden till programvaran

Den interna anteckningen är daterad den 4 december 2025. Under försöket registrerades 31 felanmälningar i loggen. Siffran utesluter akuta ärenden och arbeten som beställts före försöket.

Mediantiden från anmälan till tilldelning var två arbetsdagar under försöket och tre under de åtta veckorna dessförinnan. Perioderna hade olika arbetsbelastning, och anteckningen tillskriver uttryckligen inte programvaran skillnaden. Kostnader, boendenöjdhet och färdigställandetid har inte mätts.

## Elm Quay har inte bestämt om loggen ska breddas

Något beslut om fler hus har försöket ännu inte lett till. Teamet tar ställning när det har kontrollerat hur kategorierna fungerar för större reparationer. Maya Lind rekommenderade inte Svale till alla bostadsbolag.

— Jag skulle välja att göra om försöket. Att ha en samlad bild av felanmälningarna hjälper oss, men jag skulle lägga in en extra vecka för förberedelser, skriver hon.

Vill du förbereda ett eget försök kan du läsa [Svale Systems införandechecklista](https://example.invalid/svale/checklist) innan du börjar. Fallet är publicerat av leverantören och är inte oberoende journalistik.
```

**Så löstes körningen.** Genre `case-study`, språk `sv` och utdata till svaret kommer alla tre från anropet. Teknik: ingen. Genren `case-study` anger själv att den ordinarie tekniken är "None", så ingen teknik valdes och ingen teknikens båge har lagts på texten — framdriften är berättelsens egen. Handoff-metadata är påslagen enligt förval och ligger som `kntnt`-karta i frontmatter.

**Var utkastet hamnade.** I det här svaret. Ingenting skrevs till disk: arbetsfilerna för källkontrollen är borttagna, och arbetskatalogen innehåller bara `source.md` som förut.

**Byline.** Uppdraget namnger ingen författare, så bylinen bär ditt eget namn, Thomas Barregren. Ska texten gå osignerad eller under någon annans namn måste raden ändras före publicering.

**Granskningar.** Två fullständiga källjämförelser kördes, var och en av en ny agent utan samtalshistorik. Den första lämnade fyra anmärkningar — feldaterad anteckning, för vid formulering av Linds reservation, undantagen knutna till loggen i stället för till siffran, och "säger" om svar som kom per mejl. Alla fyra reparerades. Den andra jämförelsen läste den reparerade texten och lämnade två; en är avvisad ovan med belägg, en kvarstår. Inga översättningsanmärkningar lämnades: de tre citaten bär samma innebörd, hållning, säkerhet och egenart på idiomatisk svenska. Artikelanatomin mättes maskinellt och höll utan avsteg.

**Var underlaget tog slut.**

- Genren vill att rubriken namnger kundens nytta eller resultat. Underlaget bär ingen nytta som kan tillskrivas leverantören — anteckningen avstår uttryckligen från att koppla den kortare mediantiden till programvaran — så rubriken namnger i stället vad kunden gjorde. För en resultatrubrik behövs en mätning som knyter utfallet till loggen.
- Kostnader, boendenöjdhet och färdigställandetid är inte mätta. Texten säger att de saknas i stället för att antyda något om dem.
- Ingen jämförelse med annan leverantör redovisas, så texten kan inte säga vad Svale valdes framför.
- Intervjuerna gjordes per mejl, och underlaget ger ingen miljö, känsla eller återgiven dialog. Därför har texten ingen scen, och citaten attribueras med "skriver".
- Försöket omfattar två hus och åtta veckor. Ska texten bära ett bredare resultat behövs underlag från fler hus eller en längre period — och för frågan om utvidgning: teamets kontroll av hur kategorierna fungerar för större reparationer.
- Längden landar på omkring 400 ord, vilket underlaget räckte till.
