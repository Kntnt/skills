# #338 Pröva de fem omskrivna genrerna med Write och Redline på svenska och engelska

## What to build

Del av #329.

Genomför en verklig redaktionell utvärdering när de övriga leveranserna i #329 är integrerade. Använd de källpaket, briefs, kontrolltexter och bedömningsfrågor som #330 frös innan omskrivningen. Läs `docs/evaluation/protocol.md` och `record-template.md` först. Kriterierna får inte mjukas upp för att få den nya instruktionen godkänd.

Kör i en stödd Harness med den utvärderande sessionens egen providerfamilj: Codex endast GPT, Claude endast Claude. Denna ticket kräver en familjs kompletta körning och gör inget påstående om andra familjer. Starta inte den andra providern via verktyg eller underagenter. Ange exakt modell, Harness, corpusrevision och revisionen för instruktionerna. Om en jämförelse i den andra familjen senare önskas hör den hemma i en separat provider-native körning.

Kör Write och därefter Redline som två separata användarinvokationer för alla fem genrer på `sv`, `en_GB` och `en_US`: 15 kombinationer, med både första utkastet och resultatet efter granskningen bevarade av utvärderaren. Normalfallet ska inte namnge teknik, så att nya standarden `none` faktiskt prövas. Kör dessutom matrisens uttryckliga teknik- och metadatakontroller och dess rena/bristfälliga Redline-fall. Redline ska i pipeline-fallet få hela utkastet inklusive eventuell metadata men inte Writes källmaterial.

Ta också ett jämförelseunderlag från tidigare instruktioner på `8ae4c21`: samma fem svenska briefs och minst ett av de engelska fallen, valda i den frysta matrisen före körning. Kör med samma modell/Harness och samma material när detta tekniskt är möjligt, i en isolerad installation som aldrig skriver över aktivt installerade Skills. Baslinjen använder sina ordinarie standarder, även sin automatiska ABT; det är en dokumenterad skillnad, inte något att dölja genom en extra prompt. Bedöm varje resultat självständigt mot matrisen innan kriterieutfall jämförs. En äldre text är inte facit för den nya och likhet med en exempeltext ger inget godkännande. Om baslinjen inte kan köras redovisas den som skipped med konkret skäl, inte som förmodat sämre.

Bedöm mer än formalia: känns hantverket journalistiskt respektive copy/UX-mässigt, är vinkeln och läsaruppgiften tydliga, bär resonemanget, fungerar ingress/lead och webbläsning, är rösten genrespecifik och språket idiomatiskt utan interferens? Bedöm svenskan för engelska kalkeringar och engelskan för svensk syntax/idiom, inte bara för lokal stavning och typografi. Spåra varje bedömning till observerbara passager och skriv vad läsaren vinner eller förlorar.

Granska särskilt övergången från Write till Redline. En granskning ska kunna rätta ett verkligt problem utan att göra en krönika opersonlig, en debattartikel tandlös, kundens röst reklammässig eller web-copy mindre användbar. Jämför påståenden före/efter och uppmärksamma borttappade förbehåll, perspektiv, sakuppgifter och ändrad orsak. Ett rent kontrollfall ska inte skrivas om för att en agent känner behov av att förbättra något.

Spara protokollsenliga records separat för Write och Redline, samt ett kompakt läspaket under `docs/evaluation/` med källa/brief, första utkast, text efter Redline och fynd/olösta frågor. Artefakterna är explicita utvärderingsleverabler som utvärderaren tar hand om; en response-targeted Skill får inte lämna egna filer. Dokumentera verklig laddning i Harness-spåret för gemensam grund, valt språk och endast eventuell vald teknik, inklusive korrigeringsagenten när den används.

Rapportera kvarstående kvalitetsbrister som egna konkreta uppföljningstickets länkade till samlingsissuen. Att utvärderingen är utförd innebär inte att texternas kvalitet är godkänd om fynd återstår. Testsviten kan hålla struktur och kontrakt men kan inte visa att Thomas kommer att vara stolt över texten; läspaketet gör den bedömningen möjlig utan att dölja misslyckade exempel.

## Acceptance criteria

- [ ] Alla 15 genre/språk-kombinationer har verkligt körts genom Write och därefter Redline, eller redovisats som skipped med konkret tekniskt hinder. En utebliven kombination räknas aldrig som passerad; leveransen säger uttryckligt vilken täckning som faktiskt uppnåtts.
- [ ] Matrisens explicit valda ABT/PAC, `none` i metadata/instruktion, äldre ABT-metadata, språkbyte från källan samt positiva och negativa kontrollfall är redovisade separat. De nya standarderna respekteras i såväl rapporterad konfiguration som faktisk resursladdning.
- [ ] Baslinjens fem svenska fall och minst ett engelskt fall är bedömda med samma kriterier; modell-/Harness-skillnader eller ett omöjligt baselineförsök redovisas. Jämförelsen avser observerade kriterieutfall, inte överensstämmelse med en referenstext.
- [ ] Records anger i förväg bestämda kriterier, utfall, konkret evidens, modell, Harness, båda revisionerna, invocation/context och verkliga filbiverkningar. Bedömningen är gjord utan tillgång till den andra providerfamiljens resultat och påstår inget om denna.
- [ ] Läspaketet visar källmaterial, första utkast och korrigerad text för varje körd kombination. De fyra journalistiska genrerna kan bedömas separat från copy/UX, och idiom, berättartradition och mekanisk korrekthet bedöms som skilda aspekter.
- [ ] Redlines innehålls- och röstbevarande, rapportering av olösta fynd och eventuella borttagna påståenden är kontrollerade mot före/efter-texten, inte bara agentens egen rapport. Trace visar dess avslutande enda Proofread-pass där körningen gått så långt.
- [ ] Observerade kontraktsfel och kvalitetsbrister har uppföljningstickets med exempel och reproducerbar brief, länkade till samlingsissuen. Fel göms inte genom ändrade kriterier, borttagna körningar eller enbart lovande exempel.
- [ ] Utvärderingens sammanställning skiljer klart mellan konstaterade förbättringar, oförändrade problem, regressioner, skipped och den subjektiva slutbedömning som läspaketet lämnar åt läsaren. Ingen generell kvalitetsgaranti dras av enstaka körningar.
- [ ] Inga aktiva installationer, ursprungliga fixtures eller användarfiler har skrivits över av försöken. Endast deklarerade records/läsprover levereras; isolerade testmiljöer och egna processer städas enligt sessionens regler.
- [ ] Projektets fyra kontroller i `CONTRIBUTING.md` passerar; katalogen regenereras när ändringen berör levererade filer under `skills/`.

## Blocked by

- #333 — Den nya artikeln och dess review-kontrakt behövs för pipelineutvärderingen.
- #334 — Det nya kundcaset och dess review-kontrakt behövs för pipelineutvärderingen.
- #335 — Den nya krönikan och dess review-kontrakt behövs för pipelineutvärderingen.
- #336 — Den nya debattartikeln och dess review-kontrakt behövs för pipelineutvärderingen.
- #337 — Den nya web-copy-resursen och dess review-kontrakt behövs för pipelineutvärderingen.

---
Written against 8ae4c21


## Comment https://github.com/Kntnt/skills/issues/338#issuecomment-5743995810

## Precisering: kort riktning, självständigt omdöme

Beställarens förtydligande i [samlingsissuens kommentar](https://github.com/Kntnt/skills/issues/329#issuecomment-5743994433) gäller denna ticket och ersätter en mer detaljstyrande tolkning av dess ursprungliga text.

Bedöm uttryckligen om den samlade instruktionen lämnar utrymme för skickligt självständigt skrivande. De i förväg fastställda kvalitetsfrågorna gäller resultatet, medan numeriska riktvärden inte får fungera som automatiska felgränser. Positiva kontrollfall med välmotiverad variation ska bevaras även av Redline; inget krav på att utkastet självt motiverar varje avsteg införs.

Vid ett återkommande problem, pröva först om en otydlig yrkesroll, en motsägelse eller överstyrning i den befintliga instruktionen förklarar det. En uppföljningsticket ska motivera det faktiska behovet av en ny anvisning; ett enstaka mindre lyckat stilval är inte automatiskt skäl för ännu en generell regel.

Provtexterna är evidens för att instruktionerna fungerar, inte malltexter framtida utkast ska efterlikna. Utvärderingen och redovisningen kvarstår utan ett nytt obligatoriskt personligt godkännande eller tidig kalibrering med Thomas.

---
Written against 8ae4c21

## Comment https://github.com/Kntnt/skills/issues/338#issuecomment-5744023542

## Utvärderingen ingår i den sammanhängande leveransen

Följ genomförandebeskedet i [samlingsissuens kommentar](https://github.com/Kntnt/skills/issues/329#issuecomment-5744023422). Genomför och redovisa denna tickets praktiska utvärdering som en del av implementationen, utan att invänta Thomas personliga provläsning eller stilgodkännande.

Läspaketet är en leverabel som Thomas kan återkomma till. Hans återkoppling efter några veckors faktisk användning är underlag för senare förbättringstickets, inte ett saknat acceptanskriterium i denna ticket. Befintliga krav på verkliga körningar, ärlig redovisning av täckning och fynd samt uppföljning av konkreta brister består.

---
Written against 8ae4c21