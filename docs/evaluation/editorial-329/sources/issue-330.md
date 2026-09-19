# #330 Förankra redaktionella kvalitetskrav i originalen och frys en utvärderingsmatris

## What to build

Del av #329.

Skapa underlaget för omskrivningen innan instruktionerna ändras. Läs samlingsissuen #329 och dess hela tråd, de tre Google-originalen där samt den äldre samlingen på den fasta revision som anges där. Nuvarande instruktioner är det som ska prövas, inte facit för vad bra text är.

Kvalitetsribban är svensk journalistisk tradition på nivån SvD/DN/DI, Fokus/Ny Teknik och Filter/Forskning & Framsteg för de fyra redaktionella genrerna, respektive erfaren svensk copywriter och UX-skribent för web-copy. Samtliga skrivs för webben. Detta gäller på varje målspråk: svensk tradition styr vinkel, disposition, berättarteknik, tilltal och ton; ordval, idiom, syntax, skiljetecken och typografi är helt målspråkets, utan svensk eller engelsk interferens.

Samla en kort, källförankrad arbetskarta under `docs/evaluation/`: vilket ursprungligt krav som ska bevaras, förtydligas, avgränsas till en genre eller ersätta en nuvarande regel, samt var det ska få sin enda normativa hemvist. Kartan är genomförande- och utvärderingsunderlag, inte ytterligare instruktioner som Write eller Redline ska läsa vid körning. Ange källdokument, läsdatum och äldre Git-revision. Följ beställarens senare besked om teknikstandard; originalens återhållsamhet var ett skydd mot äldre modellers överdramatisering, inte ett generellt förbud mot ABT.

Bygg självbeskrivande fixtures och en matris i `docs/evaluation/corpus/editorial-quality/`, länkad från corpusindexet. Det behövs ett användbart, tillräckligt rikt källpaket och en brief för var och en av de fem genrerna, plus rena och medvetet bristfälliga texter att ge Redline. Använd tydligt märkt syntetiskt fixturematerial med alla faktauppgifter, attributioner, förbehåll och avsedda röster angivna. Ett kundcase behöver kundens egna uttalanden och ett verkligt uttalat omdöme inom fixturens fiktiva värld; en ghostskriven krönika behöver angivet författarperspektiv utan att nya minnen får hittas på. Web-copy behöver läsaruppgift, erbjudande eller information, villkor och en angiven destination när en länk ska användas.

Bedömningsfrågorna ska bestämmas före nya modellkörningar och vara semantiska: går läsaren att identifiera, hålls vinkeln, kommer begrepp före användning, gör ingress och lead olika jobb, fungerar webbens lässkala, finns genrekaraktären kvar, är språket idiomatiskt och hjälper Redline utan att släta ut eller tappa innehåll? Separera vad som kan kontrolleras mot källmaterialet i Write-utvärderingen från vad Redline kan se i texten. Mätningar av rubriker och stycken stödjer bedömningen; de ersätter den inte.

Ingen utvärdering eller omskrivning av levererade genre-/teknikfiler ingår här. Den senare utvärderingsticketen använder samma frysta matris mot baslinjen `8ae4c21` och mot omskrivningen. Ändra inte äldre utvärderingshistorik.

## Acceptance criteria

- [ ] Källkartan täcker de fem genrerna, den gemensamma webb- och hantverksprincipen, pedagogen i originalen, skillnaden mellan språk och redaktionell tradition samt originalens mått som riktvärden med motiverade avsteg. Historiska bylines, absoluta mått, kvoter för citat och påtvingade scener importeras inte som allmänna krav.
- [ ] Matrisen omfattar alla fem genrer på `sv`, `en_GB` och `en_US`. Minst en svensk källa används för ett engelskt utkast och en engelsk källa för ett svenskt, så att översättningsprägel prövas och inte bara rättstavning.
- [ ] Teknikfallen täcker de fem genrernas nya standard `none`, uttrycklig ABT, uttrycklig PAC och `none` i erkänd metadata/instruktion enligt befintligt kontrakt, plus äldre metadata med en uttryckligt vald teknik. Ingen ny `--technique=none`-flagga förutsätts.
- [ ] Negativa och positiva kontrollfall täcker överdramatisering, korrekt lågmäld ABT, PAC från fakta utan kontroversiell tes, upprepad ingress/lead, kompakt respektive sönderhackad webbtext, språkinterferens, leverantörsreklam i kundcase, påhittad personlig scen, otydlig UX-handling samt välskriven prosa som Redline ska bevara.
- [ ] Varje fixture har material, användning och explicita bedömningsfrågor/felutfall. Källpaketen anger också sådant en modell inte får härleda, exempelvis kausalitet ur tidsföljd eller ett kundomdöme ur enbart resultat.
- [ ] Matrisen skiljer mellan kontraktsfel, kvalitativa bedömningar och metodens begränsningar; flera olika välskrivna texter kan passera. Ingen test kräver exakt modellformulering eller förekomst av ett tidningsnamn i output.
- [ ] Projektets fyra kontroller i `CONTRIBUTING.md` passerar; katalogen regenereras när ändringen berör levererade filer under `skills/`.

---
Written against 8ae4c21


## Comment https://github.com/Kntnt/skills/issues/330#issuecomment-5743994573

## Precisering: kort riktning, självständigt omdöme

Beställarens förtydligande i [samlingsissuens kommentar](https://github.com/Kntnt/skills/issues/329#issuecomment-5743994433) gäller denna ticket och ersätter en mer detaljstyrande tolkning av dess ursprungliga text.

Bedömningsmatrisen ska pröva resultatets kvalitet och de verkliga kraven, med utrymme för flera redaktionellt olika och välfungerande lösningar. Använd positiva kontrollfall som varierar styckeindelning, rubriklängd eller dispositionsval och ändå fungerar för sin läsare. Att ligga utanför ett numeriskt riktvärde är inte i sig ett fel; ange den konkreta läsbarhetsbristen där ett avsteg faktiskt är problematiskt.

Källkarta, analys och fixtureexempel är utvärderingsunderlag. De ska inte kopieras över till genrebeskrivningarna som en heltäckande regelkatalog eller göra en bra modells självständiga val till fel. Matrisen fastställs utifrån beställningen utan ett nytt obligatoriskt kalibrerings- eller godkännandesteg med Thomas.

---
Written against 8ae4c21