Granskad som **case-study** på **svenska**, utan teknik (`none`). Alla tre värdena kom ur textens egen `kntnt`-karta i frontmattern, inte ur anropet; `none` är där ett värde och inte en lucka, så genrens arc tillämpades inte. Genren `case-study` namnger för övrigt själv ingen teknik. Kartan stämde redan med det som löstes ut, så inget i frontmattern ändrades. Korrigeringsbudgeten var den förvalda, 1.

Texten som den står efter rundan och det mekaniska slutpasset:

```markdown
---
kntnt:
  genre: case-study
  technique: none
  language: sv
---

# Elm Quay provade samlad logg i åtta veckor

Elm Quay Housing testade en gemensam logg för felanmälningar i två byggnader. Underhållsteamet ville ge olika arbetsskift tillgång till samma information och utformade själva kategorierna. Underhållsansvariga Maya Lind skulle göra om försöket, men avsätta mer tid för förberedelser. Något beslut om att utöka försöket har ännu inte fattats.

Tidigare kom Elm Quay Housings felanmälningar in via telefon och mejl, och anmälningarna från de två kanalerna förvarades separat. Bolaget förvaltar 640 lägenheter. I september 2025 beslutade bolagets eget underhållsteam att prova en gemensam logg i två byggnader. Försöket pågick i åtta veckor.

## Skiften skulle arbeta ur samma logg

Teamet valde Svale Systems efter att ha testat om loggen kunde visa statusen för varje reparation. Underlaget innehåller ingen jämförelse med någon annan leverantör.

– Vi ville att kvällsskiftet skulle se vad morgonskiftet redan hade gjort. Kategorierna var våra; Svale hjälpte oss att lägga in dem i loggen, berättar underhållsansvariga Maya Lind i en mejlintervju.

## Svale konfigurerade loggen med teamets kategorier

Underhållsteamet tog fram kategorierna och behöll möjligheten för de boende att felanmäla via telefon. Svale konfigurerade loggen och utbildade sex medarbetare vid två tillfällen.

Lind beskriver hur tiden fördelades:

– Vi lade mer tid på att komma överens om kategorierna än på att registrera de första felanmälningarna. Jag skulle avsätta den tiden innan nästa byggnad kommer i gång.

## Kortare tid till tilldelning under försöket

Enligt Elm Quays interna försöksanteckning, daterad den 4 december 2025, registrerades 31 felanmälningar. Akuta ärenden och arbeten som beställts före försöket ingår inte i underlaget.

Mediantiden från felanmälan till tilldelning var två arbetsdagar under försöket, jämfört med tre under den föregående åttaveckorsperioden. Arbetsbelastningen skilde sig mellan perioderna. Anteckningen tillskriver uttryckligen inte programvaran skillnaden.

Mätningen gäller alltså tiden tills ett ärende tilldelades, inte tills reparationen var klar. Det saknas mätningar av kostnader, hur nöjda de boende var och tiden till slutförd reparation.

## Lind vill ha en extra vecka nästa gång

Lind gör en egen bedömning av försöket:

– Jag skulle välja att göra om försöket. Det hjälper oss att ha en samlad bild av felanmälningarna, men jag skulle avsätta en extra vecka för förberedelser.

## Kategorierna ska prövas på större reparationer

Försöket har ännu inte utökats. Teamet ska först kontrollera hur kategorierna fungerar för större reparationer och därefter fatta beslut.

För dig som vill läsa vidare finns [Svale Systems checklista för införande](https://example.invalid/svale/checklist).

*Den här kundberättelsen publiceras av leverantören Svale Systems.*

```

## Kvarstående brister

**Olösta från granskningen**

1. **Bylinen saknas.** Anatomin kräver en byline efter den inledande sammanfattningen. Varken texten, dess frontmatter eller anropet namnger någon författare, så bylinen rapporteras som saknad och lämnas ofylld — att fylla den skulle kräva att en författare hittades på. Detta är den enda räknade anatomiregel som fortfarande faller.

2. **"Anteckningen tillskriver uttryckligen inte programvaran skillnaden" har två läsningar.** Adverbets placering avgör om anteckningen uttryckligen avstår från att tillskriva programvaran skillnaden, eller om den bara inte gör det uttryckligen. Texten ger inget att avgöra saken med, och läsaren kan därför inte veta hur starkt förbehållet är. Varje reparation väljer åt anteckningen vilket av två påståenden den gör. Meningen står orörd.

3. **Rubriken och sammanfattningen säger fortfarande samma sak.** De delar inte längre några ord, men "Elm Quay provade samlad logg i åtta veckor" säger en delmängd av sammanfattningens första mening plus försökets längd. Rubrik och sammanfattning ska komplettera varandra, inte upprepa varandra. Bara till hälften löst.

**Nya brister som rundans egen reparation skapade**

4. **Rubriken namnger varken resultat eller nytta för kunden.** Genren kräver att rubriken gör det. Den gamla rubriken gjorde det men slog fast mer än texten bär; den nya tar bort övertolkningen genom att ta bort påståendet. Texten har ett resultat som bär på egen styrka — den kortare mediantiden till tilldelning under försöket, som mellanrubriken över den sektionen redan formulerar med rätt försiktighet. *Följer av reparationen av brist 6 (att rubriken slog fast ett utfall).*

5. **Rubriken ger saken ett tredje namn.** Den kallar den "samlad logg" där sammanfattningen, ingressen och brödtexten genomgående säger "en gemensam logg", och Linds citat dessutom säger "en samlad bild". Läsaren möter tre namn på samma sak. *Följer av samma reparation.*

6. **"Svale konfigurerade loggen med teamets kategorier" lyfter fyra ord ordagrant ur meningen under sig.** Det är samma upprepning som brist 7 namngav, flyttad en mening ned. *Följer av reparationen av brist 7.*

7. **Samma mellanrubrik gör leverantören till den handlande.** Den står över en sektion vars egen första mening har kunden som handlande ("Underhållsteamet tog fram kategorierna"), och genren håller kunden som handlande part. Det är textens enda rubrik med leverantören som subjekt. *Följer av reparationen av brist 7.*

8. **"Lind vill ha en extra vecka nästa gång" är skarpare än texten.** Lind säger "jag skulle avsätta en extra vecka" — villkorligt, om försöket görs om — och texten säger uttryckligen att beslutet om att utöka inte är fattat. "Vill ha" gör det villkorliga till en nuvarande önskan, och "nästa gång" gör en nästa gång till något avgjort. *Följer av reparationen av brist 8 och 10.*

9. **Samma mellanrubrik levererar citatets poäng före citatet.** Den förhandsägning som togs bort ur bryggan står nu i rubriken ovanför den. *Följer av samma reparation.*

10. **"Skiften skulle arbeta ur samma logg" beskriver bara sektionens andra stycke.** Det första handlar om valet av Svale Systems och om att underlaget saknar jämförelse med andra leverantörer. Rubriken orienterar inte läsaren i det den står över. *Följer av reparationen av brist 2, där ingressens tre stycken delades och de två överflödiga blev en ny sektion.*

11. **"Kategorierna ska prövas på större reparationer" lyfter sin formulering ur meningen under sig**, och namnger bara den kontroll som återstår i stället för det avslutningen gör. *Följer av reparationen av brist 4.*

**Varför loopen stannade.** Budgeten på 1 är förbrukad. Omgranskningen reste dessutom brister som rundans egen reparation skapade, vilket stoppar loopen på egen hand: en ny runda skulle reparera det den föregående gjorde. Elva av femton ursprungliga brister reparerades.

## Anspråksredovisning

**Borttagna anspråk.** Vart och ett var självt den brist som namngavs.

- Rubrikens påstående att Elm Quay **"fick en gemensam överblick över felanmälningarna"**. Borttaget av reparationen av brist 6. Sakinnehållet finns kvar i Linds citat, "Det hjälper oss att ha en samlad bild av felanmälningarna", där det står på textens egen styrka.
- Bryggans påstående att arbetet **"gav Lind en erfarenhet att ta med till nästa byggnad"**. Borttaget av reparationen av brist 9. Innehållet finns kvar i citatet under den.
- Bryggans påstående att Linds bedömning **"rymmer ett förbehåll"**. Borttaget av reparationen av brist 10. Förbehållet finns kvar i citatet under den.
- De gamla mellanrubrikerna **"Teamet utformade kategorierna"** och **"Lind skulle avsätta mer tid för förberedelser"**. Borttagna av reparationerna av brist 7 och 8. Vad de påstod står kvar i meningen respektive citatet under dem.

**Ändrade anspråk.** Dessa står kvar, men med flyttad innebörd.

- "Tidigare förvarades felanmälningar via telefon och mejl separat" blev **"Tidigare kom Elm Quay Housings felanmälningar in via telefon och mejl, och anmälningarna från de två kanalerna förvarades separat."** Reparationen av brist 14 löste upp tvetydigheten, men avgjorde därmed också en läsning som originalet höll öppen. Det är nu två uttryckliga påståenden: att anmälningarna kom in via de två kanalerna, och att de förvarades åtskilt.
- Attributionen "berättar Maya Lind" blev **"berättar underhållsansvariga Maya Lind"**. Befattningen är textens egen, hämtad ur sammanfattningen. Reparationen av brist 12.
- "prova en gemensam logg" blev **"prova en gemensam logg i två byggnader"**. Omfattningen är textens egen, hämtad ur sammanfattningen och flyttad in i brödtexten. Reparationen av brist 13.

Inget annat anspråk ändrades. Alla tre citaten står ordagrant som de kom. Varje mening som avgränsar vad texten påstår står ordagrant kvar — "Underlaget innehåller ingen jämförelse med någon annan leverantör", "Akuta ärenden och arbeten som beställts före försöket ingår inte i underlaget", "Arbetsbelastningen skilde sig mellan perioderna", "Anteckningen tillskriver uttryckligen inte programvaran skillnaden", "Mätningen gäller alltså tiden tills ett ärende tilldelades, inte tills reparationen var klar" och "Det saknas mätningar av kostnader, hur nöjda de boende var och tiden till slutförd reparation". Sektionen "Kortare tid till tilldelning under försöket" är helt orörd.

Det mekaniska slutpasset kördes en gång, genom den installerade Proofread-färdigheten, på svenska. Inga objektiva mekaniska fel hittades, och texten kom igenom oförändrad.

---

**One operational note, outside the review.** The correction subagent reported that a cleanup command of its own ran with `TMPDIR` still holding the system value and attempted `rm -rf` on the macOS per-user temp directory `/var/folders/cs/vgp_x_353zd9frkjpysp7zdw0000gn/T/`. It said nearly all of it was refused by permissions. I checked afterwards: that directory is intact and populated, `input.md` is byte-identical to how it arrived, and nothing of this run's was lost. Unrelated files of yours that happened to be in that directory may have been removed, so it is worth knowing about. Nothing was written to your filesystem by this run — the scratch files and the mechanical pass's two private files have been removed, and the only file in the working directory is the `input.md` you supplied.
