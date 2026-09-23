Granskningen gjordes mot genren `column`, utan teknik och på `sv`. Alla tre värdena stod i artikelns `kntnt`-karta i frontmatter, så ingenting behövde gissas. Att kartan skriver `none` för teknik är ett värde och inte en lucka: det avgör parametern ovanför genrens nivå, så ingen berättarbåge lades på texten. Korrigeringsbudgeten var 1, och en runda användes.

Texten som den står nu:

```markdown
---
kntnt:
  genre: column
  technique: none
  language: sv
---

# Mallen har en ruta för allt utom poängen

Bibliotekets mötesmall vill veta när mötet börjar och slutar, men inte vad det ska vara bra för. Nora Vik vill prova en fråga vid sidan av klockslagen, och är samtidigt inte säker på att fler rutor är lösningen. Du får frågan att ta med till dina egna möten, och tvivlet som följer med den.

Av Nora Vik, bibliotekarie

Jag granskar bibliotekets mötesmall. Där finns rutor för starttid, sluttid, deltagare och dagordning. Någon ruta för det beslut vi ska kunna fatta när vi går därifrån finns inte. Det är dokumentet jag tittar på, inte ett bestämt möte.

## Bokad tid är inte samma sak som uträttat arbete

Jag uppskattar möten där kolleger upptäcker att de har förstått en fråga olika. Den upptäckten kan vara viktigare än att vi snabbt enas. Min tanke är alltså inte att varje samtal ska pressas fram till ett beslut.

Det som retar mig är något annat: att tid i kalendern så lätt behandlas som ett resultat i sig. Timmen är bokad, alltså har något hänt. Jag har inte mätt det här hos andra, och jag påstår inget om möten i allmänhet. Det är min reflektion, med den räckvidd en reflektion har.

## Ett skäl får plats bredvid starttiden

Ändå tycker jag att den som fyller i en mall borde få formulera varför vi behöver just varandras tid. Också när syftet är att undersöka något tillsammans finns det ett skäl som går att skriva ner. Samtal kan skapa förtroende. Samtal kan hitta en fråga vi inte visste att vi behövde ställa. Inget av det kräver ett beslut, men båda delarna tål att motiveras.

Så jag vill prova en enkel fråga bredvid tiden: vad behöver vi förstå tillsammans?

## Ett försök är värt en ruta till

Där börjar tvivlet. Det finns en komik i att försöka lösa ett problem med formulär genom att utöka formuläret – bibliotekarien som svarar på en mall med mer mall. Jag vet inte om ytterligare en ruta gör våra möten bättre. Kanske blir frågan bara en rad till att fylla i.

Jag vill prova den i alla fall, och behålla båda hållningarna så länge: hoppet om frågan och tvivlet på ännu en ruta. Se efter vad din egen mötesmall inte har någon ruta för.
```

## Åtgärdat

Fem fynd åtgärdades. Jag verifierade vart och ett genom att granska den återlämnade texten på nytt och mäta den på nytt med `article_anatomy.py`, som nu avslutar med status 0 och rapporterar `conforms: true`.

1. **Ingressen saknades.** Det finns nu en ingress på 54 ord mellan rubriken och bylinen. Den är byggd av material som redan fanns i texten, och den attribuerar både förslaget och tvivlet till Nora Vik vid namn.
2. **Ledet var sju stycken.** Det är nu ett stycke på 38 ord.
3. **Inga underrubriker, alltså inga avsnitt.** Texten har nu tre avsnitt om två stycken vardera, och det sista är avslutningen. Inget stycke flyttades, delades eller skrevs om för att grupperingen skulle gå ihop.
4. **Avslutningen uppmanade inte läsaren till något.** En mening lades till i slutet: *Se efter vad din egen mötesmall inte har någon ruta för.* Meningen före den står oförändrad, så tvivlet och båda hållningarna står kvar som de stod.
5. **"ett skäl att skriva ner" saknade objekt.** Nu står det *ett skäl som går att skriva ner*.

## Kvarstående fynd

Ett fynd är ouppklarat, och det är rundans eget verk.

**Underrubriken *Ett försök är värt en ruta till* drar en slutsats som texten avstår från.** Avsnittet under den säger *Jag vet inte om ytterligare en ruta gör våra möten bättre* och slutar i att båda hållningarna behålls. Rubriken avgör den frågan till försökets fördel. Rubrikkontraktet kräver att varje slutsats i en rubrik finns i texten med textens egen styrka, och den här gör texten säkrare än den är. Rubriken beskriver inte heller vad styckena under den handlar om: avsnittet handlar om tvivlet, rubriken om ett avgjort värde. Den som skummar de tre underrubrikerna får en prydlig argumentation utan den ovisshet som är kolumnens bärande drag.

Fyndet gäller en mening som inte fanns i texten när den kom in. Underrubriken tillkom som reparation av fynd 3, och en ny runda skulle alltså ha reparerat den föregående rundans arbete. Därför stannade korrigeringen här, och budgeten på 1 var dessutom förbrukad. Vad som behöver avgöras är rubrikens ordalydelse, inte texten under den.

## Anspråksredovisning

Inget anspråk togs bort. De sju ursprungliga styckena kom tillbaka ordagrant med ett undantag, och de fyra meningar som avgränsar vad texten hävdar står kvar oförändrade: *Det är dokumentet jag tittar på, inte ett bestämt möte.*, *Min tanke är alltså inte att varje samtal ska pressas fram till ett beslut.*, *Jag har inte mätt det här hos andra, och jag påstår inget om möten i allmänhet.* och *Det är min reflektion, med den räckvidd en reflektion har.*

Ett anspråk ändrade lydelse: *finns det ett skäl att skriva ner* blev *finns det ett skäl som går att skriva ner*, som reparation av fynd 5. Vad meningen hävdar står kvar med samma räckvidd och samma styrka; det som ändrades var att objektet som saknades nu finns i meningen.

Två partier är nya och kommer från korrigeringsrundan snarare än från den författare texten bär byline för: ingressen och den sista meningen i sista stycket. Båda är byggda av vad texten redan sade, och de bör läsas igenom av författaren just därför.

## Mekanisk slutpassage

Proofread kördes en gång på `sv` och rättade en objektiv sak: tankstrecket i *utöka formuläret — bibliotekarien* var ett em-streck, som hör till engelsk typografi, och är nu ett spatierat en-streck. Inget annat i texten rördes.
