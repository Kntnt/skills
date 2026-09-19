# Oberoende redaktionell granskning — #329

Granskad 2026-09-19: arbetskopian på `editorial-329`, med `6e531f5fe0b610e046ae58787f246cc6239acbcc` som HEAD och pågående implementation ovanpå. Kravbas: [#329 med senare förtydliganden](../sources/issue-329.md) samt hela #330–338 med kommentarer. Startrevisionen är `8ae4c21`; corpus är fryst vid `6e531f5`. Detta är en instruktionsgranskning, inte ett godkännande av den ännu pågående praktiska utvärderingen.

## Fynd E1 — svensk review drar slutsats om osedd citatkälla

**Resurs:** `skills/kntnt/library/references/languages/sv.md:54`, Review-stycket som börjar ”Check reported speech against the mark it is set in”. Det säger att välformulerat tal inom citattecken har reparerats och att citatmarkeringen därför är fel. Resursen laddas av både Redline och dess korrigeringsagent.

**Kravkälla:** [#331](../sources/issue-331.md) avgränsar granskningen till synliga brister; [#334](../sources/issue-334.md) förbjuder att underkänna ett trovärdigt citat för att intervjun inte kontrollerats. Samma gräns finns nu i `editorial/base.review.md`, `genres/case-study.review.md` och Redlines steg 6.

**Påverkan:** Ett verkligt ordagrant, välformulerat kunduttalande kan få ett falskt fynd och byta citatmarkering. Prosan visar inte om talaren uttryckte sig flytande eller om skribenten reparerade den. Instruktionen återinför därmed just den proveniensbedömning som de nya gemensamma resurserna tar bort.

**Minimal rättning:** Ersätt slutsatsen om reparerat tal med diagnostik som kräver belägg i själva texten. Bevara citatets markering när enda misstanken är att orden är välformulerade. Detta ändrar inte Writes citatpolicy eller svensk typografi.

**Disposition — rättat och verifierat 2026-09-19:** Review-stycket kräver nu textintern inkonsekvens, säger uttryckligen att flytande språk inte belägger ett reparerat citat och tillåter att skilda markeringar fyller skilda funktioner. Den rättningen undanröjer E1 utan att lägga till en annan provenienskontroll. Fyndet är stängt.

## Första helhetsbedömningen

Efter rättningen av E1 noterades då ingen blockerande redaktionell motsägelse i det lästa paketet. Den senare omprövningen E2 nedan bevaras separat. Basen, webbgrunden, de fem genrerna och teknikerna är koncentrerade och lämnar vinkelns utförande, rytm och retoriska val åt skribenten. Webbskalan är uttryckligen vägledande. Artikelns form, kundens eget omdöme, krönikans personliga perspektiv, debattartikelns ståndpunkt och webbcopyns läsaruppgift är åtskilda utan nya block- eller citatkvoter.

Svenskt hantverk och målspråkets uttryck hålls isär. `none` är ordinarie teknik i femgruppen; explicit ABT/PAC har fortsatt en begriplig uppgift. Ingressen nås utan teaser-laddning. Write, Redline och den färska korrigeringsagenten har förenliga och avgränsade laddningsvägar. Source Fidelity, innehållsbevarande och en avslutande Proofread-pass kvarstår.

Läst: AGENTS.md, dokumentregler, writing-for-agents, editorial- och språk-README; hela base/web-craft och reviews; alla fem genrepar; båda teknikpar; anti-slop; sv/en_GB/en_US; Write/Redline inklusive hjälpsidor, correction och quotations; Proofread och mechanics. Även de tre sparade originaldokumenten, teaser-gränsen, aktiva corpusbeskrivningar och redovisningen av läsbelastning kontrollerades. Inga implementeringsfiler ändrades. Faktiskt textutfall och slutlig utvärdering återstår att granska när läspaketet är färdigt.

## Senare riktade instruktioner

Följande ändringar granskades självständigt medan den praktiska utvärderingen pågick:

- Column avgränsar författarens tillskrivna tankar, känslor, erfarenheter och handlingar till underlaget; en observation om en praxis blir inte en egen bekännelse. Uttryck, rytm och reflektion förblir skribentens redaktionella val.
- Opinion skiljer skarp framställning från ändrad faktisk hållning. Att inte motsätta sig något får inte göras till aktivt stöd. Det är en precisering av sakligt innehåll, ingen retorisk mall.
- Quotations skiljer idiomatisk tillåten översättning från nytillkommet innehåll. En implicit referent får förtydligas bara när kontexten avgör den. Det tydliggör avsikten utan att tillåta uppfinning. En senare omprövning fann dock att den absoluta ordalydelsen i Anything additive fortfarande konkurrerar med detta undantag; se E2 nedan.
- Base.review fördelar ansvaret för upprepade hela meningar/passager till redaktionell granskning, medan Proofread äger dubblerade ord. Nästa styckes skydd av funktionell repetition och kravet på faktisk läsarförlust kvarstår.
- Case-study.review gör ett synligt referentproblem i citerat målspråk granskningsbart. Endast omgivande text får bära ett förtydligande; övriga luckor rapporteras. Basens och korrigeringsbriefens skydd för betydelse, säkerhet och särpräglad röst gäller fortfarande.
- Base Claims skiljer okänt eller opåstått från känt frånvarande. Det preciserar den befintliga saklighetsgränsen utan att kräva försiktigare språk där säkerhet är belagd; #349:s kvarvarande modellfel måste därför redovisas som utfallsfel, inte döljas av att instruktionen är förenlig.
- Svensk Mechanics tillåter gemen efter kolon när en fullständig mening är en nära specificering, inklusive en integrerad fråga, och skiljer det från anföring respektive flera efterföljande meningar. Avgränsningen kontrollerades mot [Språkrådets svar om kolon](https://frageladan.isof.se/faqs/25422). Reglerna för bevarande av etablerad variation ligger fortsatt i det gemensamma mechanics-kontraktet.

Ingen av dessa riktade ändringar införde en ny dispositions-, exempel- eller stilkvot eller krävde frånvarande källmaterial av Redline. De praktiska utfallen redovisas separat i de daterade Write-/Redline-recorden; en förenlig instruktion är inte i sig bevis för felfria texter.

## Fynd E2 — absolut ordtilläggsförbud konkurrerar med tillåten översättning

**Resurs:** Write `references/quotations.md`, bullet **Anything additive**, granskad på `d0b2c99`. Efter det nya översättningsstycket säger bulleten fortfarande ”No word” och att allt inom citatmarkeringen måste ha sagts. Den senare absoluta regeln avser ord, inte bara sakligt innehåll.

**Kravkälla:** #334 och #337 kräver bevarad kundröst i idiomatiskt målspråk; Writes Source Fidelity kräver bevarad betydelse och kvalifikationer. Tillåten översättning kan kräva ett ord som gör en entydig implicit referent uttrycklig.

**Påverkan:** En läsare av det samlade kontraktet får två olika signaler om sådana ordtillägg. Den tidigare bedömningen att ingressundantaget ensamt undanröjde konflikten omprövas. Det kvarvarande #341-utfallet visar ett praktiskt problem men bevisar inte ensamt vilken instruktion som orsakade modellvalet.

**Minimal rättning:** Formulera tilläggsförbudet som förbud mot ny betydelse, fakta, hållning, säkerhet, namn, siffror eller samband. Bind ordändringar till tillåtna reparationer och översättningar som återger samma betydelse. Behåll övriga skydd för särpräglad röst och den uttömmande reparationslistan. Inga produktfiler ändrade av granskaren.

**Disposition E2 — rättat och verifierat vid `29ff2047ad2dac330dd705feccdb3f2d0778831b`:** Bulletspråket förbjuder nu ny betydelse och binder ordändring till *permitted repair or translation*. Översättningens kontextvillkor och skydden för betydelse, hållning, säkerhet och särpräglad röst står kvar. Den konkurrerande absoluta ordregeln är därmed borttagen; praktisk verifiering följer i separata tre språkpar och är inte förutsatt av dispositionen.

Writes färdigkriterium i `d0b2c99` kräver också att sakliga och tillskrivna påståenden kontrolleras mot underlaget som del av skrivandet. Det gör befintlig Source Fidelity verksam i samma utkaststeg; det laddar ingen review-resurs, inför ingen redaktionell eftergranskning och använder ingen annan Skill. Öppningens och leveransstegets gräns mot en separat review-/Proofread-pass förblir förenlig.

## Oberoende läsning av kompletterande utvärdering

Läst hela root-column-källan och de tre slutliga Write-artefakterna under `rerun-column-final`, båda `342-column-final`-recorden och `348-colon`-recordet. Deras åtskillnad mellan källstödd personlig reflektion och uppfunnen egen vana håller i de faktiska texterna. Den svenska kolonkorrigeringens äldre pass är uttryckligen ersatt av fail, medan exakt replay redovisas separat; det är korrekt bevisföring. Även hela senare `completion-check/column-sv/write/response.txt` lästes mot källan: den generiska kalenderillustrationen ”Vi har avsatt en timme” påstår ingen identifierbar mötesepisod eller författarvana och är tillåten reflekterande gestaltning, F1 pass.

Läst hela `338-selection`-recordet, de fem selektionskontrollernas gemensamma artikeltext, report-pac före/efter samt excerpt-texten. Faktisk diff och teknik-/Proofread-kommandon stöder utfallet: none och äldre metadata prioriteras som dokumenterat, PAC ersätter bara den formellt överstyrda teknikmetadata, tidigt svar står kvar i rapporten och utdrag får ingen påhittad helartikelform. Rapportens tre lokala referensförtydliganden har stöd i befintlig text och dess särskilda genrekrav. Detta är en oberoende text- och recordgranskning, inte en ny körning av dessa kontrollceller.

Läsbelastningsredovisningen har också lästs. Den skiljer den korta redaktionella briefen från den större operativa laddningen, de tre språkens scopes, faktisk korrigering och den avslutande Proofread-passen. Ordminskningen är kontextkostnad, inte ett kvalitetsmått; textutfallen avgör vilka kriterier som faktiskt passerar.
