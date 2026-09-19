# #334 Skriv om case-study till ett journalistiskt kundcase som bärs av kundens erfarenhet

## What to build

Del av #329.

Läs samlingsissuen #329 och dess tråd, arbetskartan från #330 samt den gemensamma grund som #331 inför. Använd originaldokumenten i samlingsissuen och den äldre genrefilen på revisionen `b121cfcb274803193c3b0d60e751429bb0aef67a` som källmaterial, inte som en mall att återställa ordagrant. Grund- och review-filerna i `skills/kntnt/library/references/editorial/genres/` ska skrivas om tillsammans. Grundfilen säger vad texten ska uppnå; review säger hur synliga brister upptäcks och korrigeras utan att tillföra nya normer.

Skriv om `case-study.md` och `case-study.review.md` för ett kundcase med svensk journalistisk kvalitet, anpassat till webbläsning. Kundens situation, beslut, arbete, resultat och omdöme är berättelsen; leverantören förekommer i tredje person. Den publicerande leverantörens intresse får inte färga berättarprosan till obestyrkt reklam. Kundcaset får inte samtidigt antyda att det är oberoende rapportering utan en avsändare.

Bevara det värdefulla i den äldre genren: kundens röst bär erfarenheter och bedömningar, skribentens prosa ger sammanhang och progression. Citat ska tillföra något bron före dem inte redan säger och låta som mänskligt tal. Följ Writes befintliga citatgränser och målspråkets konventioner; inga nya ord läggs i kundens mun för att fylla ett formkrav.

Ge läsaren en enkel form att orientera sig i: rubrik om kundens nytta/resultat, en fristående ingress, precis så mycket kundbakgrund som behövs, vad som satte arbetet i gång, val och genomförande, belagda resultat med förbehåll samt kundens eget omdöme. Avsluta med relevant nästa steg när beställningen bär det. Ordningen hjälper förståelsen utan att varje del måste vara en egen H2 eller att ett visst antal citat/pull quotes måste produceras.

Skilj kundens problem från en påtvingad räddningshistoria. Kunden ska framstå som en handlande part. Kvantifiera bara med mått som materialet ger, och gör inte ett tidsmässigt efter till en orsak. Bevara ett nyanserat omdöme, till exempel att kunden skulle göra om satsningen men ändra tidplanen. Finns inget faktiskt kundomdöme eller inga citerbara uttalanden, redovisar Write luckan i leveransen; texten får inte fullbordas med uppfunna citat eller falsk nöjdhet. Redline kan beskriva det som synligt saknas men ska varken begära intervjun eller underkänna ett trovärdigt citat för att den inte har kontrollerat det.

Ingress och kropp ska fungera för en skumläsande webbläsare. Kundcase är inte undantagna från den gemensamma webbskalan eller från kravet på idiomatiskt målspråk.

## Acceptance criteria

- [ ] Kundens perspektiv och egna bedömningar bär texten, medan leverantören beskrivs i tredje person i berättarprosan. En kunds eller leverantörs repliker behåller däremot talarens rätta perspektiv.
- [ ] En kort formbeskrivning skiljer resultatbärande rubrik, ingress, kundbakgrund, utgångsläge, genomförande, resultat, kundomdöme och eventuell nästa handling; den tvingar inte fram en rubrik, en kvot citat eller en säljsektion per del.
- [ ] Ett kundomdöme som innehåller en reservation uppfyller genren utan att reservationen slätas ut. En rekommendation, person, orsak, siffra, scen eller länk som saknas i materialet fabriceras aldrig för att passa formen.
- [ ] Råd om citat skiljer citerbara ord från referat. Citat om erfarenhet och bedömning tillför eget innehåll, medan transportprosa inte förhandsupprepar citatet. Nuvarande citatpolicy och målspråkets typografi förblir styrande.
- [ ] Review har konkreta diagnostiska exempel på leverantörsreklam, räddningsdramaturgi, dekorativa citat och upprepad ingress/lead. Den visar också ett fullt fungerande lågmält kundcase.
- [ ] Materialluckor hanteras enligt respektive Skills ansvar: Write redovisar vad underlaget inte bar; Redline anger en synlig genrebrist utan att jämföra med eller efterfråga källmaterial. Ingen tyst genreväxling eller radering av fungerande sakuppgifter.
- [ ] Instruktionen är ett kort arbetsblad med konkreta regler, vanligen en eller två meningar per regel, och ett fåtal korta exempel som skiljer bra från bristfällig tillämpning. Redovisa ordantal före/efter för grund och review samt hela den obligatoriska läsvägen, så att förkortning inte döljs genom utflyttning. Samma krav dupliceras inte i flera filer.
- [ ] Review diagnostiserar texten som finns framför agenten. Den begär inte originalintervju, brief eller extern källkontroll, inventerar inga fakta och behåller sakuppgifter och fungerande uttryck utanför fyndet. Brister som kräver nytt material rapporteras som olösta.
- [ ] Filnamn, den identifierande inledningen för hjälp/genreinferens, engelska som instruktionsspråk, grund/review-gränsen och sektionen för ordinarie teknik följer editorial-README. Den gemensamma webb- och hantverksgrunden nås uttryckligt; teknikstandard och avval följer #332.
- [ ] Ordinarie teknik är `none`. En naturlig berättelse eller ett logiskt resonemang räknas inte som ett implicit teknikval; uttryckligt vald teknik fungerar fortfarande.
- [ ] Projektets fyra kontroller i `CONTRIBUTING.md` passerar; katalogen regenereras när ändringen berör levererade filer under `skills/`.

## Blocked by

- #331 — Gemensam webb-/hantverksgrund, ingresskontrakt och förenlig laddning måste finnas först.
- #332 — Teknikernas betydelse och de fem genrernas standard none ska vara samordnade före den fullständiga genreomskrivningen.

---
Written against 8ae4c21


## Comment https://github.com/Kntnt/skills/issues/334#issuecomment-5743995235

## Precisering: kort riktning, självständigt omdöme

Beställarens förtydligande i [samlingsissuens kommentar](https://github.com/Kntnt/skills/issues/329#issuecomment-5743994433) gäller denna ticket och ersätter en mer detaljstyrande tolkning av dess ursprungliga text.

Inled med ett journalistiskt kundcase som uppdrag: kundens situation, erfarenhet och röst står i centrum, med målspråkets naturliga språkdräkt. Ange textens nödvändiga delar och citatens funktion kort; låt modellen själv skapa en fungerande berättelse inom dem.

Ticketens uppräkning av delar ska inte växa till en detaljerad sekvens av rubriker, styckekvoter eller krav på ett citat per avsnitt. Behåll gränserna kring kundomdöme, tillskrivning och underlag. Arbetsbladets korthet bedöms på vad instruktionerna tillför, inte ett föreskrivet antal meningar per regel. Webbskalan är vägledande.

De olika positiva och negativa exemplen får ligga i corpus där de verifierar kraven. Den levererade review-filen ska bara innehålla användbar, kort diagnostik och ge utrymme för flera välfungerande kundcase.

---
Written against 8ae4c21