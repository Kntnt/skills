# #337 Skriv om web-copy till precis copy och UX-text som hjälper läsaren att handla

## What to build

Del av #329.

Läs samlingsissuen #329 och dess tråd, arbetskartan från #330 samt den gemensamma grund som #331 inför. Använd originaldokumenten i samlingsissuen och den äldre genrefilen på revisionen `b121cfcb274803193c3b0d60e751429bb0aef67a` som källmaterial, inte som en mall att återställa ordagrant. Grund- och review-filerna i `skills/kntnt/library/references/editorial/genres/` ska skrivas om tillsammans. Grundfilen säger vad texten ska uppnå; review säger hur synliga brister upptäcks och korrigeras utan att tillföra nya normer.

Skriv om `web-copy.md` och `web-copy.review.md` för text av en erfaren svensk copywriter och UX-skribent på den nivå som anlitas av ledande byråer och varumärken. Den ska vara tänkt och skriven på målspråket; varje ord ska göra nytta för läsaren. Svensk kommunikativ tradition styr perspektiv, tilltal, disposition och återhållsamhet, medan målspråket fullt ut styr språkdräkten.

Dagens resurs beskriver främst skumläsning. Gör läsarens uppgift lika tydlig: vad är detta, är det relevant för mig, vad får jag eller behöver jag veta, vilka villkor gäller och vad händer om jag tar nästa steg? Formulera konkreta fördelar som materialet kan stödja, tydliga val, begripliga länkar och knappar när de ingår i uppdraget, och besked som minskar verklig osäkerhet. Innehåll får vara övertygande utan superlativer, påhittade löften, falsk brådska eller generiska påståenden om värde.

Behåll det som fungerar: nyckelbudskap och relevanta ord tidigt, rubriker som deklarerar sitt innehåll, korta stycken som går att skumma och sektioner som kan förstås när läsaren kommer in mitt på sidan. Fokusera på det sammanhang som behövs vid den ingången; duplicera inte hela sidan under varje rubrik. Listor, tabeller och andra element används för informationens struktur och den beställda ytan, inte som dekor.

Anpassa formen efter sidans uppgift, underlag och brief, utan att kräva en universell ordning med hero, tre fördelar, omdömen och kontaktknapp. En ren informationssida får sluta när frågan är besvarad. En tjänstesida behöver tydlig nytta och nästa steg om de finns i uppdraget. Knappar och mikrokopia ska säga vad handlingen gör; inga nya funktioner, priser, villkor, garantier eller destinationer får uppfinnas.

Web-copy ska inte välja ABT automatiskt. Explicit vald teknik ska fortfarande kunna användas enligt #332, på den nivå som hjälper uppgiften och utan att gömma ett svar eller en handling tills läsaren tagit sig genom en berättelse. Skriv inte alla webbtexter som artiklar, men påstå inte heller att artikelns läsare aldrig skummar.

Rätta review-delens överstrikta regel att varje avsnitt måste ha varit uttryckligen beställt: lämplig informationsstruktur får härledas ur briefens mål och befintliga innehåll. Att organisera befintlig information är något annat än att hitta på ett erbjudande eller en funktion.

## Acceptance criteria

- [ ] Första intrycket klargör sida/erbjudande, avsedd läsare och relevant nytta eller information. Läsaren kan förstå nästa steg och dess följd där ett nästa steg ingår i uppdraget.
- [ ] Rubriker, länktexter, knappar och eventuell stödtext är specifika och begripliga i sin kontext. De lovar bara innehåll eller beteende som brief/underlag ger stöd för.
- [ ] Fristående sektioner fungerar vid direkt ingång med precis den kontext som behövs; samma långa introduktion kopieras inte in överallt och det linjära läsflödet fungerar fortfarande.
- [ ] Grund och review tillåter informationsstruktur som rimligen följer av läsaruppgift och innehåll. De kräver ingen artikel-ingress, försäljningsmall, obligatorisk CTA, produktfördel eller funktion som uppdraget inte bär.
- [ ] Ordinarie teknik är `none`. Uttrycklig teknik respekteras enligt #332 utan att sidans centrala svar eller handling hålls tillbaka för dramaturgins skull.
- [ ] Konkreta före/efter-exempel visar skillnaden mellan att beskriva en målgrupp abstrakt och att hjälpa läsaren med en faktisk uppgift. Positiva kontrollfall omfattar både informativ sida och tjänstesida med angivet nästa steg.
- [ ] Instruktionen är ett kort arbetsblad med konkreta regler, vanligen en eller två meningar per regel, och ett fåtal korta exempel som skiljer bra från bristfällig tillämpning. Redovisa ordantal före/efter för grund och review samt hela den obligatoriska läsvägen, så att förkortning inte döljs genom utflyttning. Samma krav dupliceras inte i flera filer.
- [ ] Review diagnostiserar texten som finns framför agenten. Den begär inte originalintervju, brief eller extern källkontroll, inventerar inga fakta och behåller sakuppgifter och fungerande uttryck utanför fyndet. Brister som kräver nytt material rapporteras som olösta.
- [ ] Filnamn, den identifierande inledningen för hjälp/genreinferens, engelska som instruktionsspråk, grund/review-gränsen och sektionen för ordinarie teknik följer editorial-README. Den gemensamma webb- och hantverksgrunden nås uttryckligt; teknikstandard och avval följer #332.
- [ ] Projektets fyra kontroller i `CONTRIBUTING.md` passerar; katalogen regenereras när ändringen berör levererade filer under `skills/`.

## Blocked by

- #331 — Gemensam webb-/hantverksgrund, ingresskontrakt och förenlig laddning måste finnas först.
- #332 — Teknikernas betydelse och de fem genrernas standard none ska vara samordnade före den fullständiga genreomskrivningen.

---
Written against 8ae4c21


## Comment https://github.com/Kntnt/skills/issues/337#issuecomment-5743995686

## Precisering: kort riktning, självständigt omdöme

Beställarens förtydligande i [samlingsissuens kommentar](https://github.com/Kntnt/skills/issues/329#issuecomment-5743994433) gäller denna ticket och ersätter en mer detaljstyrande tolkning av dess ursprungliga text.

Inled med uppdraget för en erfaren svensk copywriter och UX-skribent: genomarbetad webbtext, tänkt och skriven på målspråket, där varje ord gör nytta för läsaren. Ange sedan de få form- och funktionskrav som hjälper modellen förstå uppgiften.

Frågorna om relevans, nytta, villkor och nästa steg ska ge riktning för läsarens uppgift. De är inte obligatoriska innehållsblock på varje sida. Modellen väljer själv disposition, formulering och lämplig omfattning utifrån uppdraget. Funktioner och löften får fortsatt inte uppfinnas.

Korthets- och exempelkraven ska inte skapa kvoter för instruktionerna. Låt corpus bära omfattande jämförelser och håll den levererade resursen och review-delen koncentrerade. Välfungerande variation i rubriker, stycken och avsnitt ska bevaras.

---
Written against 8ae4c21