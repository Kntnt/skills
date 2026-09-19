# #331 Gör svensk skrivtradition och webbkrav till en gemensam, faktiskt laddad skrivgrund

## What to build

Del av #329.

Inför en kort gemensam skrivgrund för exakt de fem genrer som samlingsissuen #329 omfattar. Använd den källkarta och matris som #330 levererar.

Kvalitetsribban är svensk journalistisk tradition på nivån SvD/DN/DI, Fokus/Ny Teknik och Filter/Forskning & Framsteg för de fyra redaktionella genrerna, respektive erfaren svensk copywriter och UX-skribent för web-copy. Samtliga skrivs för webben. Detta gäller på varje målspråk: svensk tradition styr vinkel, disposition, berättarteknik, tilltal och ton; ordval, idiom, syntax, skiljetecken och typografi är helt målspråkets, utan svensk eller engelsk interferens.

Låt kraven ha en enda hemvist i levererade editorial-resurser, med tydliga hänvisningar från alla fem genrebasfiler. Ett gemensamt stödpar under `skills/kntnt/library/references/editorial/` är lämpligt; filnamnet får inte bli en ny valbar genre eller teknik. Grunddelen anger utfall för skrivandet, review-delen bara diagnostik för samma krav. Lägg inte dessa fem genrers profil på exempelvis general, report eller press-release.

Gör grunden konkret: en relevant vinkel och läsaruppgift, begriplig progression, begrepp innan de används i resonemang, precis saklighet, fungerande övergångar, rytm och korta sammanhållna stycken, rubriker som hjälper den aktuella genrens läsare och varje ord med en uppgift. Originalens 30–70 tecken för rubriker, cirka 60 ord för ingress och cirka 80 ord som övre riktvärde för stycken är orientering för webbens lässkala, med motiverade avsteg för språk, genre och innehåll. De är inte universella minimikrav, felgränser eller krav på att alla texter ska ha ingress. Normalfallet 2–3 meningar per stycke och 2–3 stycken per avsnitt får inte skapa ett mekaniskt rutnät.

Avgränsa journalistisk berättarröst från web-copy och UX. Svensk tradition får inte bli krav på svensk meningsbyggnad eller pronomanvändning i andra språk. Resolved Language Resource äger språkdräkten; dess generella beskrivning av exempelvis amerikansk framställning får samtidigt inte upphäva vald genres svenska hantverk. Ändra bara språkscope där en faktisk motsägelse eller ett språkberoende fel behöver rättas, inte genom att kopiera den gemensamma regeln till varje språk.

Säkra laddningen i `skills/editorial/write/SKILL.md`, `skills/editorial/redline/SKILL.md` och `skills/editorial/redline/references/correction.md`. En länk som de nuvarande instruktionerna ”load ... and nothing besides it” förbjuder att följa är ingen fungerande lösning. Write får den gemensamma grunddelen; Redline och varje färsk korrigeringsagent får grunden och dess review-del. Loadingen ska vara uttrycklig och snäv, utan att läsa andra ovalda genrer eller införa generell rekursiv länkladdning.

Gör ingressens uppgift nåbar utan att ladda teaser som en andra genre: en ingress är fristående, konkret och får ge det centrala resultatet. Den får locka genom relevans, inte krävas hålla inne svaret. Samordna motsvarande påståenden i `teaser.md` och dess review-del så att de inte fortsätter att likställa varje ingress med en oavslutad klickbåge. Detta är en gränsdragning för ingressen, inte en full omskrivning av teaser.

Harmonisera `base.md`/`base.review.md`, editorial-README och direkt berörda hjälpsidor i den utsträckning de annars motsäger detta. Granska särskilt generella regler om dramaturgi, bildspråk, retoriska frågor, repetition och rubriker: lärarens konkreta förklaring och krönikans motiverade grepp ska få utrymme, utan fabricerade fakta, scener eller stöd. En lokal upprepning kan behövas för en webbsektion eller för ingressens självständighet; onödig omtagning är fortfarande ett fel.

Redline bedömer endast texten och rapporterar synliga brister. Ta bort anvisningar i de gemensamma review-resurserna om att gå tillbaka till frånvarande källmaterial eller fylla på från det. Bevara Source Fidelity hos Write, Redlines claim-bevarande och slutlig Proofread-pass. De fem genrernas fullständiga omskrivningar sker i egna blockerade tickets.

## Acceptance criteria

- [ ] Alla fem genrebasfiler hänvisar uttryckligt till samma levererade kvalitetsgrund. Kraven om webb, de två yrkestraditionerna och helt idiomatiskt målspråk finns där i full mening, även för andra framtida installerade språk än svenska och engelska.
- [ ] Grunden har korta, handlingsnära regler och högst ett fåtal fokuserade exempel. Normer finns i grunddelen; review introducerar inga egna krav och stora argumenterande stycken har inte flyttats till en ny obligatorisk fil.
- [ ] Write, Redline och Redlines korrigeringsbrief har förenliga, explicit avgränsade laddningsinstruktioner. Grunddelen laddas i skrivning, båda delarna i granskning/korrigering och ingen review-del av Write. En granskare kan följa denna väg från varje av de fem genrerna.
- [ ] Genreinferens och hjälp använder fortsatt endast kandidatens rubrik/inledningsstycke; stödresursen syns inte som ett val och läses inte för att inferera genre. Övriga genrer får inte femgenrersprofilen.
- [ ] Ingresskraven nås utan en andra genres fullständiga kontrakt och utan extra teknikval. Artikel/kundcase får ange resultat i ingressen; teaser-relaterade texter hävdar inte motsatsen om dessa ingresser.
- [ ] Riktvärden kan överskridas av språkliga eller redaktionella skäl utan automatiskt Redline-fynd. Innehåll läggs inte till eller tas bort enbart för ett antal; ett verkligt läsbarhetsproblem kan däremot motivera omarbetning.
- [ ] Språkets scopes bestämmer idiom och lokal korrekthet, genren bestämmer hantverk. Eventuella undantag från generella basråd är explicita och snävt avgränsade; Source Fidelity och skyddet mot fabricerade citat/erfarenheter består.
- [ ] Gemensamma review-anvisningar och korrigeringsbrief kräver inte källverifikation eller nytt material av Redline. Korrigering bevarar sakuppgifter, betydelse och fungerande röst, och olösbara fynd rapporteras.
- [ ] Endast mekaniskt verifierbara kontrakt som laddningsgräns, valbarhet och giltiga hänvisningar får riktade automatiska kontroller där det behövs; textkvaliteten verifieras senare med den frysta matrisen.
- [ ] Projektets fyra kontroller i `CONTRIBUTING.md` passerar; katalogen regenereras när ändringen berör levererade filer under `skills/`.

## Blocked by

- #330 — Källkarta, fixtures och kriterier ska vara fastställda innan skrivinstruktionerna ändras.

---
Written against 8ae4c21


## Comment https://github.com/Kntnt/skills/issues/331#issuecomment-5743994743

## Precisering: kort riktning, självständigt omdöme

Beställarens förtydligande i [samlingsissuens kommentar](https://github.com/Kntnt/skills/issues/329#issuecomment-5743994433) gäller denna ticket och ersätter en mer detaljstyrande tolkning av dess ursprungliga text.

Etablera yrkesrollen och den svenska hantverkstraditionen tidigt i den valda genrens läsväg, tillsammans med att språkdräkten fullt ut är målspråkets. Den gemensamma grunden ska vara kort och tydligt skilja faktiska krav från vägledande webbskala.

Förkortningen ska omfatta den samlade läsningen. Granska därför även allmän skrivlära i `base.md` och `base.review.md`: stryk eller kondensera överförklaringar som motverkar denna riktning, samtidigt som saklighet, källtrogenhet och andra nödvändiga gränser bevaras och övriga konsumenter förblir förenliga. Flytta inte den långa instruktionen till ett nytt gemensamt dokument.

Ett välfungerande avsteg från ett riktvärde kräver ingen tillåtelse eller motiveringsrapport. Redline ska kunna ange vad läsaren faktiskt förlorar innan ett riktvärdesavsteg behandlas som en brist. De uppräknade kvalitetsaspekterna i ticketen ska täckas av ett fåtal koncentrerade anvisningar, inte varsin obligatorisk lektion.

---
Written against 8ae4c21