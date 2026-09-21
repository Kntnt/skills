Granskningen utgick från genren `case-study`, ingen teknik och språket `sv`. Alla tre värdena kom ur den `kntnt`-karta som texten själv bär i sin frontmatter. Värdet `none` för tekniken är ett val och inte en lucka: det avgör parametern där det står, ovanför genrens nivå, så genrens egen uppgift om vilken teknik en kundberättelse normalt skrivs med kom aldrig i fråga. Kartan stämmer med det granskningen kom fram till, och frontmattern är därför oförändrad.

Korrigeringsbudgeten var 1, förvalet, och den räckte till en omgång. Slingan stannade av två skäl samtidigt: budgeten var förbrukad med fynd kvar, och omgranskningen reste två fynd som omgångens egna reparationer hade skapat. Artikelanatomins räknade gränser är maskinmätta, både före och efter omgången.

```markdown
---
kntnt:
  genre: case-study
  technique: none
  language: sv
---

# Elm Quay prövade gemensam logg i åtta veckor

Elm Quay Housing testade en gemensam logg för felanmälningar i två byggnader. Underhållsteamet ville ge olika arbetsskift tillgång till samma information och utformade själva kategorierna. Underhållsansvariga Maya Lind skulle göra om försöket, men avsätta mer tid för förberedelser. Något beslut om att utöka försöket har ännu inte fattats.

Bolaget Elm Quay Housing förvaltar 640 lägenheter. Tidigare kom felanmälningar in via telefon och mejl och förvarades var för sig. I september 2025 beslutade bolagets eget underhållsteam att prova en gemensam logg. Försöket pågick i åtta veckor.

## Skiften skulle få samma information

Teamet valde Svale Systems efter att ha testat om loggen kunde visa statusen för varje reparation. Underlaget innehåller ingen jämförelse med någon annan leverantör.

– Vi ville att kvällsskiftet skulle se vad morgonskiftet redan hade gjort. Kategorierna var våra; Svale hjälpte oss att lägga in dem i loggen, berättar underhållsansvariga Maya Lind i en mejlintervju.

## Sex medarbetare utbildades vid två tillfällen

Underhållsteamet tog fram kategorierna och behöll möjligheten för de boende att felanmäla via telefon. Svale konfigurerade loggen och utbildade sex medarbetare vid två tillfällen.

För Lind gav arbetet en erfarenhet att ta med till nästa byggnad:

– Vi lade mer tid på att komma överens om kategorierna än på att registrera de första felanmälningarna. Jag skulle avsätta den tiden innan nästa byggnad kommer i gång.

## Kortare tid till tilldelning under försöket

Enligt Elm Quays interna försöksanteckning, daterad den 4 december 2025, registrerades 31 felanmälningar. Akuta ärenden och arbeten som beställts före försöket ingår inte i underlaget.

Mediantiden från felanmälan till tilldelning var två arbetsdagar under försöket, jämfört med tre under den föregående åttaveckorsperioden. Arbetsbelastningen skilde sig mellan perioderna. Anteckningen tillskriver uttryckligen inte programvaran skillnaden.

Mätningen gäller alltså tiden tills ett ärende tilldelades, inte tills reparationen var klar. Det saknas mätningar av kostnader, hur nöjda de boende var och tiden till slutförd reparation.

## Lind skulle avsätta mer tid för förberedelser

Linds egen bedömning av försöket rymmer ett förbehåll:

– Jag skulle välja att göra om försöket. Det hjälper oss att ha en samlad bild av felanmälningarna, men jag skulle avsätta en extra vecka för förberedelser.

## Teamet ska kontrollera kategorierna före beslut

Försöket har ännu inte utökats. Teamet ska först kontrollera hur kategorierna fungerar för större reparationer och därefter fatta beslut.

För dig som vill läsa vidare finns [Svale Systems checklista för införande](https://example.invalid/svale/checklist).

*Den här kundberättelsen publiceras av leverantören Svale Systems.*

```

## Åtgärdade fynd

Omgranskningen bekräftar att åtta fynd är borta.

1. **Rubriken påstod mer än texten bär.** "Elm Quay fick en gemensam överblick över felanmälningarna" sade att bolaget hade fått en gemensam överblick — ett avslutat och bolagsövergripande resultat. Texten säger något annat: försöket omfattade två byggnader, pågick i åtta veckor, har ännu inte utökats, och telefonanmälan behölls. Rubriken lyder nu "Elm Quay prövade gemensam logg i åtta veckor" och håller sig till försöket och dess längd.
2. **Leadet var tre stycken.** Artikelanatomin kräver ett enda stycke mellan bylinen och den första mellanrubriken; mätningen rapporterade `lead: 3 paragraphs`. Citatet och stycket om leverantörsvalet ligger nu under en egen mellanrubrik, och leadet är ett stycke.
3. **Maya Linds roll fanns bara i ingressen.** Brödtexten ska läsas fullständig med ingressen övertäckt, eftersom ingressen ofta visas för sig eller hoppas över. Den läsaren fick aldrig veta vem Maya Lind var. Attributionen lyder nu "berättar underhållsansvariga Maya Lind i en mejlintervju".
4. **"Svale" nämndes första gången inuti ett citat.** Berättarrösten presenterade "Svale Systems" först i stycket därefter. Stycket om leverantörsvalet står nu före citatet, så läsaren möter leverantören i tredje person innan citatet nämner den.
5. **"Tidigare förvarades felanmälningar via telefon och mejl separat."** Felanmälningar förvaras inte via en telefon, och läsaren fick själv lägga till det led meningen saknade. Meningen lyder nu "Tidigare kom felanmälningar in via telefon och mejl och förvarades var för sig".
6. **Mellanrubriken "Teamet utformade kategorierna" upprepade meningen under sig** ("Underhållsteamet tog fram kategorierna och behöll möjligheten för de boende att felanmäla via telefon"). Rubriken är utbytt — men se det första av de nya fynden nedan.
7. **Ingressen och leadet inleddes med samma ord**, båda med "Elm" (`both open on "elm"`). Leadet börjar nu på "Bolaget".
8. **Sista avsnittet höll fem stycken** mot normens högst tre (`section 3: 5 paragraphs`), och avslutningen ska dessutom vara kort. Avsnittet är delat: Linds omdöme står kvar under sin rubrik, och status, uppmaning och utgivaruppgift bildar ett eget avslutande avsnitt.

## Kvarstående fynd

**Bylinen saknas.** Artikelanatomin kräver att varje del finns i den ordning den anger, och bylinen är en av dem. Mätningen rapporterar fortfarande `byline: absent`, och det är den enda räknade brist som står kvar. Ingen författare namnges i texten, i dess metadata eller i anropet, och en byline som ingen kan namnge rapporteras som saknad i stället för att fyllas i. Läsaren får alltså ingen avsändare för den redaktionella texten, vilket väger tyngre i en kundberättelse som leverantören själv publicerar. Raden behöver fyllas i innan texten publiceras.

## Fynd som omgångens egen reparation skapade

Båda följer av reparationer i den enda omgång budgeten räckte till, och ingen av dem fanns i texten när den kom in.

**Mellanrubriken "Sex medarbetare utbildades vid två tillfällen"** kom av reparationen av fynd 6 ovan. Den tar bort upprepningen, men den anger inte längre avsnittets vinkel. Avsnittet handlar om att underhållsteamet tog fram kategorierna och behöll telefonanmälan, och citatet under rubriken handlar uteslutande om den tid kategorierna tog. Utbildningen av sex medarbetare är avsnittets minst betydelsefulla uppgift, och rubriken upprepar dessutom avsnittets andra mening nästan ordagrant. S-passiven döljer därtill vem som utbildade, i ett avsnitt vars poäng är kundens eget arbete. En rubrik som utgår från kategorierna, i andra ord än den första meningens, löser båda sakerna.

**Mellanrubriken "Skiften skulle få samma information"** kom av reparationen av fynd 2 och 4. Den beskriver bara avsnittets andra stycke — citatet — och säger det som ingressen redan har sagt ("ville ge olika arbetsskift tillgång till samma information"). Avsnittets första stycke, leverantörsvalet och upplysningen att underlaget inte innehåller någon jämförelse med någon annan leverantör, får ingen signal alls till den skannande läsaren.

## Redovisning av påståenden

**Ett påstående togs bort:** rubrikens påstående att Elm Quay fick en gemensam överblick över felanmälningarna. Fynd 1 pekade ut just det påståendet som defekten, så borttagningen står sig, men den ska namnges. Den nya rubriken påstår bara att bolaget prövade en gemensam logg i åtta veckor, vilket texten bär.

**Inget påstående har flyttats** i omfattning, säkerhet, tillskrivning, kronologi, orsak eller innebörd. Alla meningar som avgränsar vad texten hävdar står ordagrant kvar: att underlaget inte innehåller någon jämförelse med någon annan leverantör, att akuta ärenden och arbeten beställda före försöket inte ingår, att arbetsbelastningen skilde sig mellan perioderna, att anteckningen uttryckligen inte tillskriver programvaran skillnaden, att mätningen gäller tiden till tilldelning och inte till avslutad reparation, att mätningar av kostnader, nöjdhet och tid till slutförd reparation saknas, och att försöket ännu inte har utökats. De tre citaten är orörda så när som på att attributionen till det första nu ger Maya Linds befattning.

En omskrivning är värd att nämna för kontrollens skull: "Tidigare förvarades felanmälningar via telefon och mejl separat" blev "Tidigare kom felanmälningar in via telefon och mejl och förvarades var för sig". Båda uppgifterna — kanalen in och att anmälningarna förvarades var för sig — är desamma; reparationen tillförde bara det led som fynd 5 pekade ut som saknat.

Den avslutande mekaniska genomgången hittade inget att rätta.
