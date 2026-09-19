# #332 Förenkla ABT och PAC och ta bort automatiskt teknikval för de fem webbgenrerna

## What to build

Del av #329.

Skriv om `skills/kntnt/library/references/editorial/techniques/abt.md`, `pac.md` och deras review-filer som korta, konkreta beskrivningar av två användbara strukturer. Läs samlingsissuen #329 och dess senare beslut, källkartan från #330 och den gemensamma grunden från #331. Jämför med `lib/techniques/abt.md` och `lib/techniques/pac.md` på den äldre samlingens fasta revision `b121cfcb274803193c3b0d60e751429bb0aef67a`.

**Det uttryckliga beslutet är att ingen av de fem genrerna väljer teknik automatiskt.** Sätt ordinarie teknik till `none` i `article`, `case-study`, `column`, `opinion` och `web-copy`. Inför inte `--technique=none`, `plain` eller någon ny flagga. Val via teknikflaggan, erkänd metadata eller instruktion ska fungera enligt dagens prioritet; ett gammalt dokument med `technique: abt` har fortfarande valt ABT. Teknikstandard för genrer utanför denna uttryckliga femgrupp ändras inte.

ABT ska åter vara lätt att använda: den nödvändiga situationen, ett verkligt hinder/en relevant fråga eller motsättning och det svar/den konsekvens som materialet bär. B behöver inte vara en kris eller logisk motsägelse; en sakligt relevant obesvarad fråga kan driva förklaringen. T behöver inte vara en triumf; ett öppet eller villkorat resultat får vara resultatet. De tre relationerna ska hålla utan etiketter, påklistrade övergångsord, obligatoriska scener eller amerikansk problem–agitation–lösning-retorik.

Beskriv vid behov nästling och iteration kort med när de hjälper förståelsen, inte genom att kräva att alla långa texter delas efter ett ordantal. In medias res är ett möjligt grepp med befintligt material, inte definitionen av god journalistik och inte ett krav på en avslöjande brygga. En ingress kan ge resultatet tidigt samtidigt som texten låter läsaren följa förklaringen. Genrens form, saklighet och webbläsarens uppgift gäller också när tekniken är vald.

Återför PAC till dess användbara analytiska betydelse från den äldre resursen: en faktisk utgångspunkt eller fråga, analys av vad underlaget betyder och en slutsats som följer av analysen. Nuvarande krav att P måste vara en falsifierbar tes förvandlar all analys till hypotesprövning. Hypotesprövning får vara ett tillämpningsfall; beskrivande analys av exempelvis ett verksamhetsutfall ska också fungera. Invändningar och alternativa förklaringar vägs när material och frågeställning ger skäl, inte genom uppfunna motsidor.

Teknik ska forma resonemanget på den nivå genren och uppdraget medger. ABT i web-copy får fungera i självständiga sektioner när de har varsin läsarfråga; den ska inte kräva en artificiell global konflikt som binder ihop en informationssida. Det är fortfarande en verklig tillämpning av det valda kontraktet, inte ett tyst ignorerat val. PAC ska tillåta rapportens inledande besked medan resonemanget utvecklas i avsnitten.

Review-filerna ska diagnostisera de faktiska relationerna i texten, inte granska mot källmaterial som Redline inte har. Korrigering flyttar eller förtydligar befintligt stöd och bevarar påståenden; saknat stöd rapporteras om det inte går att reparera utan uppfinning. Dagens kontrakt får inte återkomma genom kvarvarande exempel, aktiv corpusbeskrivning eller hjälpproser. Ändra relevanta sådana ytor och mekaniskt verifierbara testförväntningar i samma ticket, utan att skriva om historiska records eller återinföra äldre triggerlistor.

## Acceptance criteria

- [ ] De fem uttryckligt namngivna genrerna anger `none` som ordinarie teknik. Övriga genrers standardvärden är bevarade. Filernas tekniksektion följer det befintliga läsbara formatet.
- [ ] Ett tekniklöst Write-/Redline-fall för var och en av femgruppen löser ingen teknik och lastar inga teknikresurser. Naturlig berättelsestruktur i material/text är inte evidens för ett teknikval.
- [ ] Flaggvald `abt`/`pac`, giltig Kntnt-metadata med teknik och namngiven teknik i instruktion fungerar med befintlig prioritet. `none` i metadata/instruktion avstår enligt nuvarande kontrakt; ingen ny grammatik eller tyst omskrivning av äldre metadata införs.
- [ ] ABT innehåller nödvändig situation, relevant komplikation/fråga och belagd konsekvens. Ett kort sakligt exempel visar en lågmäld tillämpning; ett motexempel visar fabricerad dramatik eller ett 'men' som inte motsvarar någon relation.
- [ ] PAC fungerar både för analys från givna fakta och för en prövbar hypotes. Ett fakta–tolkning–slutsats-exempel och ett bristfälligt slutledningssteg gör skillnaden konkret utan att införa ett krav på påhittade invändningar.
- [ ] Förklaringen av teknikens nivå löser tidig ingress/tes, rapportens inledande besked och web-copyns självständiga avsnitt utan ett oförklarat undantag som gör tekniken valfri när den faktiskt valts.
- [ ] Råd om nästling, iteration och in medias res är korta möjligheter kopplade till innehållets behov. Inga obligatoriska dramatiska scener, mekaniska ordtrösklar eller identiska mikrobågar införs.
- [ ] Alla normativa teknikutfall finns i grundfilerna. Review kräver endast diagnostik av den synliga texten, bevarar påståenden och rapporterar det som inte kan rättas. Skillernas befintliga ansvar och korrigeringsbudget består.
- [ ] Berörda aktiva hänvisningar, hjälpsidor, corpusförklaringar och relevanta testförväntningar är förenliga med de nya betydelserna. Grund- och review-filerna är kortare och handlingsnära; redovisa ordantal före/efter.
- [ ] Projektets fyra kontroller i `CONTRIBUTING.md` passerar; katalogen regenereras när ändringen berör levererade filer under `skills/`.

## Blocked by

- #331 — Gemensam webb-/hantverksgrund, ingresskontrakt och förenlig laddning måste finnas först.

---
Written against 8ae4c21


## Comment https://github.com/Kntnt/skills/issues/332#issuecomment-5743994860

## Precisering: kort riktning, självständigt omdöme

Beställarens förtydligande i [samlingsissuens kommentar](https://github.com/Kntnt/skills/issues/329#issuecomment-5743994433) gäller denna ticket och ersätter en mer detaljstyrande tolkning av dess ursprungliga text.

Beskriv kort vad ABT respektive PAC är och vilka samband en vald teknik ska hålla. Låt modellen välja hur den tillämpas inom genrens krav. Råd om nästling, iteration och in medias res är möjligheter, inte ett system av villkor, obligatoriska underformer eller felsökningsfall att ladda varje gång.

Ticketens exempelkrav verifierar skillnaden mellan fungerande och bristfällig tillämpning; de kräver inte separata långa exempelavsnitt i varje levererad fil. Använd ett kort exempel där det löser en verklig oklarhet, och håll övriga exempel i utvärderingsmaterialet. Review ska bedöma sambanden utan att skriva om en annan fungerande tillämpning till sin föredragna mall. Beslutet om `none` för femgruppen och oförändrad flagggrammatik kvarstår.

---
Written against 8ae4c21