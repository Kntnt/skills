# #333 Skriv om article till ett konkret arbetsblad för journalistiska webbtexter

## What to build

Del av #329.

Läs samlingsissuen #329 och dess tråd, arbetskartan från #330 samt den gemensamma grund som #331 inför. Använd originaldokumenten i samlingsissuen och den äldre genrefilen på revisionen `b121cfcb274803193c3b0d60e751429bb0aef67a` som källmaterial, inte som en mall att återställa ordagrant. Grund- och review-filerna i `skills/kntnt/library/references/editorial/genres/` ska skrivas om tillsammans. Grundfilen säger vad texten ska uppnå; review säger hur synliga brister upptäcks och korrigeras utan att tillföra nya normer.

Skriv om `article.md` och `article.review.md` för en saklig, pedagogisk eller rapporterande artikel som en skicklig svensk journalist skulle skriva för en krävande webbläsare. Kvalitetsribban är svensk journalistisk tradition på nivån SvD/DN/DI, Fokus/Ny Teknik och Filter/Forskning & Framsteg för de fyra redaktionella genrerna, respektive erfaren svensk copywriter och UX-skribent för web-copy. Samtliga skrivs för webben. Detta gäller på varje målspråk: svensk tradition styr vinkel, disposition, berättarteknik, tilltal och ton; ordval, idiom, syntax, skiljetecken och typografi är helt målspråkets, utan svensk eller engelsk interferens.

Återför den tydliga formen från originalen: en informativ H1, en fristående ingress, byline när ett namn är givet och en egen lead före första H2, följt av brödtext med relevanta mellanrubriker. HTML respektive Markdown ska uttrycka samma hierarki enligt beställt format. Ingressen berättar vad texten ger och får avslöja resultatet; leaden börjar själva framställningen. De ska inte säga samma sak två gånger eller öppna med samma formulering. Nödvändig saklig överlappning är tillåten när båda delarna behöver fungera självständigt.

Vinkeln ska komma tidigt och styra urvalet. Bygg begrepp och samband i den ordning läsaren behöver dem, från kort relevant kontext till det konkreta, utan att alltid börja med allmän bakgrund. Låt fakta, logik och relevanta människor/citat bära intresset. ABT behöver ingen dramatisk scen, konfliktretorik eller cliffhanger. En informativ rubrik och ett klart svar tidigt är förenliga med en sammanhängande ABT-båge i förklaringen.

Avslutningen infriar artikelns löfte: en förståelse, en belagd slutsats eller ett konkret användbart nästa steg. En kommersiell CTA hör bara hemma när beställning, ämne och underlag motiverar den; ingen kontaktlänk uppfinns. Byline anges bara när författaren är given, aldrig med Thomas som global standard.

Återför originalens webbskala som riktvärden enligt den gemensamma grunden, med avsteg som tjänar ämne och målspråk. Sluta beskriva en artikel som något vars läsare förutsätts läsa allt i ordning; skumläsning, tydliga ingångar och verklig sammanhängande förklaring ska fungera tillsammans. Krönikans personliga reflektion och debattartikelns tesdrivna argumentation förblir egna genrer.

En konkret konflikt att rätta i dagens review är att en saknad byline pekas ut som fel även när grundfilen säger att inget namn ska uppfinnas. Andra är källkontroller och råd att fylla texten ur material som Redline inte har.

## Acceptance criteria

- [ ] Artikelns fullständiga form och de olika uppgifterna för rubrik, ingress, lead, brödtext och avslutning är enkla att identifiera. Ingressen kan fungera separat utan att vara en konstgjord teaser; första H2 kommer efter leaden.
- [ ] Fallet utan författarnamn fungerar utan påhittad byline och utan krav på att Redline skaffar ett namn. Ett uttryckligt utdrag eller avsnitt får inte påtvingas en hel artikels förtext.
- [ ] En teknisk förklaring utan scen kan uppfylla genren fullt ut: begrepp är begripliga före användning, sakliga samband håller och varje avsnitt för vinkeln framåt. Tillgänglighet betyder inte att relevant tekniskt innehåll stryks.
- [ ] Originalens mått och avsnittsskala hänvisar till gemensamma riktvärden. En tät text kan få ett motiverat fynd; en välfungerande längre mening eller ett längre sammanhållet stycke får inte ett fynd bara för sitt antal.
- [ ] Avslutningen skiljer på en användbar konsekvens och en påklistrad sälj-CTA. Rubrik/ingress/lead prövas tillsammans utan förbud mot den upprepning som deras olika lässituationer faktiskt kräver.
- [ ] Fixtures från #330 kan användas för att skilja en artikel från neutral ämnesuppräkning, en dramatisk berättelse utan pedagogiskt värde och ett pressmeddelande. Review har ett kort fungerande exempel och ett fel som får en avgränsad korrigering.
- [ ] Instruktionen är ett kort arbetsblad med konkreta regler, vanligen en eller två meningar per regel, och ett fåtal korta exempel som skiljer bra från bristfällig tillämpning. Redovisa ordantal före/efter för grund och review samt hela den obligatoriska läsvägen, så att förkortning inte döljs genom utflyttning. Samma krav dupliceras inte i flera filer.
- [ ] Review diagnostiserar texten som finns framför agenten. Den begär inte originalintervju, brief eller extern källkontroll, inventerar inga fakta och behåller sakuppgifter och fungerande uttryck utanför fyndet. Brister som kräver nytt material rapporteras som olösta.
- [ ] Filnamn, den identifierande inledningen för hjälp/genreinferens, engelska som instruktionsspråk, grund/review-gränsen och sektionen för ordinarie teknik följer editorial-README. Den gemensamma webb- och hantverksgrunden nås uttryckligt; teknikstandard och avval följer #332.
- [ ] Ordinarie teknik är `none`. En artikel med naturlig berättelsebåge men utan valt teknikvärde får inte bli föremål för ABT-diagnostik.
- [ ] Projektets fyra kontroller i `CONTRIBUTING.md` passerar; katalogen regenereras när ändringen berör levererade filer under `skills/`.

## Blocked by

- #331 — Gemensam webb-/hantverksgrund, ingresskontrakt och förenlig laddning måste finnas först.
- #332 — Teknikernas betydelse och de fem genrernas standard none ska vara samordnade före den fullständiga genreomskrivningen.

---
Written against 8ae4c21


## Comment https://github.com/Kntnt/skills/issues/333#issuecomment-5743994988

## Precisering: kort riktning, självständigt omdöme

Beställarens förtydligande i [samlingsissuens kommentar](https://github.com/Kntnt/skills/issues/329#issuecomment-5743994433) gäller denna ticket och ersätter en mer detaljstyrande tolkning av dess ursprungliga text.

Inled med genrens uppdrag och svenska journalistiska hantverk, realiserat på målspråket. Ge därefter den nödvändiga formen och några vägledande webbprinciper. Låt modellen själv välja vinkelns utförande, rytm, övergångar och pedagogiska grepp.

Ticketens krav på ett ”kort arbetsblad”, meningar per regel och exempel ska läsas som önskan om koncentration, inte som en ny formmall för instruktionen. Funktionerna hos rubrik, ingress och lead består; pröva deras funktion och meningsfulla skillnad, inte en mekanisk regel om överlappande ord. Måtten är riktvärden som en välfungerande text kan avvika från utan tillstånd eller rapportering. Ordantal före/efter är beslutsunderlag, inget optimeringsmål.

Exempel som behövs för verifiering kan ligga i corpus. Review-filen behöver bara den korta diagnostik som hjälper den att upptäcka verkliga brister och bevara bra redaktionella val.

---
Written against 8ae4c21