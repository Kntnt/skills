# Resultat av fortsättningen på #329

**Senare trackeromorganisation:** Restarbetet ligger nu i [#362–364](supersession/README.md). #329, #341, #357, #358, #360 och #361 har stängts som ersatta, inte som lösta. Rapporten nedan är kvalitetsredovisningen vid `b004f223`, före denna omorganisation; dess öppna/stängda tillstånd är historiska. Inga underkända texter har godkänts i efterhand.

Alla deklarerade körningsplatser är nu redovisade. Produktversionen är fryst vid `5ecadb76`; underlaget nedan skiljer verifierade förbättringar från kvarstående fel. **#329 är inte kvalitetsmässigt färdigt och ska förbli öppet.** De verifierade ändringarna och hela evidenspaketet är integrerade i lokal `main`. Åtta uppfyllda ärenden är avslutade på GitHub; fem underärenden och samlingsärendet är fortsatt öppna.

## Vad implementationen ändrar

Write låter en färsk, källmedveten agent jämföra hela utkastet med hela underlaget. Granskningen omfattar även påståendens räckvidd, omständigheter och förutsättningar, utan att bli en allmän redaktionell granskning. Författaren kontrollerar både redovisningen av påståendena och anmälda fel mot den verkliga texten. En rättning eller bestridd rapport medför en andra färsk jämförelse. Två jämförelser är gränsen; kvarstående verkliga fel eller en ofullständig jämförelse stoppar utkastet. Författarens avvisande av ett obelagt fynd beskrivs inte som granskarens godkännande.

Det gemensamma leveranskontraktet skiljer nu korrekt mellan oförändrad text utan fynd, oförändrad text med kvarstående fynd och de olika leveransmålen. Opinion-granskningen skiljer ett uttryckligen osäkert förslag från ett faktiskt löfte om genomförbarhet. Redlines enda avslutande Proofread-pass får hela den accepterade texten i en privat fil och skriver ett separat fullständigt resultat, även när inget ändrats. Föräldern läser det resultatet före leverans.

Försöket med en separat citatgranskare i Redline togs bort. Det förbättrade vissa svenska citat men ändrade också fungerande engelska och ökade läsning och samordning. Återgången minskar den kostnaden, men är inte en verifierad lösning på citatproblemen: slutversionen uppvisar fortfarande både missad svensk idiomatik och onödig engelsk omskrivning.

## Avslutade ärenden

Följande åtta ärenden är verifierat stängda: [#344](https://github.com/Kntnt/skills/issues/344) om dateringar, [#349](https://github.com/Kntnt/skills/issues/349) om okänt kontra belagt frånvarande arbete, [#352](https://github.com/Kntnt/skills/issues/352) om påhittade intervjufrågor, [#353](https://github.com/Kntnt/skills/issues/353) om leveransmål, [#354](https://github.com/Kntnt/skills/issues/354) om kvalificerade förslag, [#355](https://github.com/Kntnt/skills/issues/355) om dokumentets respektive källpaketets räckvidd, [#356](https://github.com/Kntnt/skills/issues/356) om obelagda personattribut och [#359](https://github.com/Kntnt/skills/issues/359) om den mekaniska överföringen.

Varje ärende har en egen slutkommentar med avgränsad slutsats, faktisk evidens, lokal commit och kvarstående begränsningar. [Tracker-kvittot](tracker/final-disposition.json) innehåller kommentarernas länkar och verifierade tillstånd. Slutlig hierarkikontroll visar 32 underärenden, varav 27 stängda och de fem nedan öppna; inga ytterligare undernivåer finns.

## Konkreta kvarstående fel

- **#341:** Redline lämnar fortfarande det oförändrade svenska originalprovet med ”innan nästa hus börjar”. Kontexten gör betydelsen möjlig att räkna ut, men formuleringen uppfyller inte kravet på professionell svensk idiomatik.
- **#358:** Två gamla engelska kontrolltexter bevaras, men ett nytt amerikanskt kundcase får åter en obehövlig utbyggnad av ett fungerande engelskt citat. Återgången till förälderns citatgranskning räcker alltså inte för avslut.
- **#357:** Krönikans källkontroll läser en pågående reflektion som ett påstående om hur tanken historiskt uppstod. Författaren godtar fyndet och stryker övergången. Frånvaro av leveransstopp uppfyller därför inte ensam ärendets krav på rättvisande kontextläsning.
- **#360:** Den sista amerikanska debattartikeln byter rapportens ”digital vana” mot ”digital proficiency”. Båda jämförelserna och författaren godtar det felaktigt. Detta är ett sakfel, även om samma text klarar #349:s skillnad mellan okänt och belagt frånvarande kostnadsarbete.
- **#361:** Det brittiska kundcaset sammanfattar kundens omdöme precis före citatet som återger samma två poänger. Utkastet är källtrogen text men underkänns på genrekravet om citatets uppgift. Det parade Redline-provet rättar bryggan och bevarar frågan och hela citatet; Write-provet blir inte godkänt i efterhand.

Detta är påvisade kvalitetsfel under oförändrade krav, inte ett resonemang om att hundraprocentig perfektion är omöjlig. Det finns inget påvisat externt hinder. Flera prövade kontrollmetoder har däremot missat fel eller skapat falska fynd; ingen ytterligare belagd instruktionskonflikt har hittats som motiverar ännu ett generellt regellager. De misslyckade försöken finns kvar i underlaget. Ingen lyckad selektiv omkörning ersätter ett misslyckat prov.

## Slutprovning på produktversion 5ecadb76

Den sista källmatrisen omfattar åtta Write-platser med var sitt efterföljande Redline-prov när ett utkast levereras. Sju utkast levereras: sex klarar F1, ett missar F1. Det svenska kundcaset hålls inne för en verklig idiombrist och dess beroende Redline hoppas över. Ett stoppat utkast räknas inte som en källtrogen leverans.

| Prov | Write | Separat källblind Redline |
| --- | --- | --- |
| Kundcase, original US r1 | F1 och hantverk godkända | Onödig citatändring: #358; F1 bevaras |
| Kundcase, original US r2 | F1 och hantverk godkända; felaktig startdatering rättas | Godkänt, oförändrat |
| Kundcase, original sv | Giltigt leveransstopp för #341 | Överhoppat; ingen levererad text |
| Debatt, original US | F1 underkänt: #360; #349:s gräns bevaras | Källblind granskning godkänd; källfelet kvar |
| Krönika, original sv | F1 och hantverk godkända; kvarstående falskt kontrollfynd #357 | Godkänt, oförändrat |
| Artikel, original sv | F1 och hantverk godkända | Godkänt, oförändrat |
| Kundcase med faktisk fråga, GB | F1 godkänt; citatbrygga underkänd: #361 | Bryggan rättas, frågan och citatet bevaras |
| Debatt med belagd frånvaro, GB | F1 och hantverk godkända | Godkänt; ett frivilligt sakpåstående stryks med uttrycklig redovisning |

Fullständiga delbedömningar: [originalprov](reviews/account-original.md), [kompletterande fall och övriga genrer](reviews/account-new.md), [tidigare originalartefakter](reviews/final-delivery-original.md), [övriga tidigare artefakter](reviews/final-delivery-new.md) och [mekaniska kontroller](reviews/final-mechanical-controls.md).

Dessutom körs elva separat fastställda Redline-prov på oförändrade tidigare artefakter och mekaniska kontroller. Nio klarar källblind granskning; två svenska citatprov missar #341. Det gamla amerikanska provets dolda dateringsfel kvarstår trots att Redline nu bevarar citatet. De nya proverna ersätter inte de tidigare misslyckandena.

Det blir **26 verkliga Skill-invokationer av 27 planerade platser**, med ett redovisat beroendehopp. Slutrevisionens 49 native-sessioner omfattar även granskare, korrigerare och mekaniska underagenter. Alla 18 Redline-invokationer har en faktisk avslutande Proofread-pass och verifierad privat filöverföring.

Hela fortsättningen innehåller **212 Skill-invokationer: 90 Write och 122 Redline**, plus **33 neutrala diagnoser**. De omfattar 439 native-sessioner. Den första leveransens 119 Skill-invokationer ligger kvar som separat historik. [Slutlig körningsräkning](reviews/invocation-census-final.json) bevarar varje körning, revision, identitet och städkvitto; samtliga 245 körningsrötter är borta och ingen körning saknar slutresultat. Alla exekveringar slutar utan processfel eller timeout, vilket inte gör underkända texter godkända.

## Granskning, kostnad och gränser

[Den oberoende kontraktsgranskningen](reviews/final-contract-review.md) och [den separata redaktionella helhetsgranskningen](reviews/final-whole-resource-editorial.md) läser hela de berörda resurserna. Deras konstaterade kontraktskonsekvens är inte ett godkännande av samtliga provtexter. [Kravkartan](completion-map.md) skiljer varje ärendes krav från hela artefaktens kvalitet.

Slutproduktens fyra CONTRIBUTING-kontroller passerar, inklusive **1 873 tester**. Kommandon, loggar och städning finns i [valideringsunderlaget](validation/integration/test-results.json). Dessa tester kontrollerar implementation och kontrakt, inte textkvalitet.

Källkontrollen kostar mer läsning och tid. Den obligatoriska resursmängden för Write ökar med 884 ord jämfört med fortsättningens startversion, före källor, utkast, granskningsrapporter och underagenternas läsning. Citatpolicyn tillkommer när den behövs. Slutprovningens Write-körningar tar 282–641 sekunder, median 616 sekunder; Redline tar 71–213 sekunder, median 86 sekunder. Urvalen innehåller olika fall och är ingen kontrollerad jämförelse av merkostnad. [Den samlade belastningsberäkningen](reviews/combined-load-contract.json) skiljer dokumentord från faktisk körning; inga kausala latenstal eller allmänna tillförlitlighetsprocent härleds ur dessa olika prov.

Native körningar använder observerad, ärvd `gpt-6-astra/high` i Codex CLI 0.155.1, utan modellöverskrivning. Fullständiga artefakter bedöms mot källor och frysta kriterier oberoende av granskarens eget besked. Krypterade dispatchdelar förblir uttryckligen overifierade där senare fullständiga filavläsningar inte ger insyn. Den gamla felstavningens exakta uppkomststeg är fortfarande okänt; den nya privata filöverföringen är däremot direkt observerbar.

Produkt och fullständig evidens integrerades med fast-forward i lokal `main` vid `12373d807e7f872e88ea4bb795af9b065c075dc5`. Den efterföljande dokumentationscommiten registrerar de faktiskt genomförda trackeråtgärderna. Arbetsbranchen `editorial-source-fidelity` är borttagen efter integration; dess commits finns i `main`. Skyddad `rework` och dess worktree är orörda vid `4dbe937bd3d9bb940bbc23b001d4e59d337f03ed`. Alla egna utvärderingsprocesser är avslutade och tillfälliga körningsmiljöer städade; handoff och evidens är bevarade. Ingen push, release eller global installation har gjorts.
