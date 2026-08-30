---
name: thomas-writer
description: >
  Write texts in Thomas Barregren's distinctive style – professional, clear, and engaging Swedish
  (or British English) prose that guides the reader like an intellectual adventure. Use this skill
  whenever the user asks you to write, draft, or produce any text that should sound like Thomas
  Barregren or follow his writing style. Also trigger when the user says "skriv en text",
  "blogginlägg", "artikel", "pressmeddelande", "skriv i min stil", "Thomas stil", "skriv som Thomas",
  "write in my style", "draft a blog post", "write an article", or any request to produce content
  where the user expects Thomas Barregren's voice and method. Trigger even if the user simply says
  "skriv" or "write" followed by a topic – if this skill is installed, the user wants Thomas's style.
  When in doubt, trigger.
---

# Thomas Barregren – Writer Style Skill

Denna skill består av tre filer. **Läs alla tre innan du börjar skriva.**

1. **SKILL.md** (denna fil) – formatmallar, arbetsflöde och poängskala.
2. **STILREGLER.md** – Thomas stilprinciper: ABT, kognitiv last, understatement, ton, precision, övergångar, tilltal.
3. **SKRIVREGLER.md** – typografi, citat, förkortningar, brödtextens självständighet, autentisk svenska.

Använd `Read`-verktyget för att läsa STILREGLER.md och SKRIVREGLER.md från samma katalog som denna fil. Gör det nu, innan du fortsätter.

## Formatmallar (riktmärken, inte hårda regler)

Dessa är riktmärken som ger en förståelse för vad som är vettigt. Följ dem inte till punkt och pricka.

### Reportage, artikel och blogginlägg

Varje artikel ska inledas i denna ordning:

1. **Huvudrubrik (H1):** Max 70 tecken, informativ och lockande.
2. **Standfirst (kursiv):** Max ~60 ord, fristående. Ska fungera som puff tillsammans med rubriken – i nyhetsbrev, på startsidan, i andra sammanhang. Standfirst ska ha en egen miniatyr-ABT: börja med nödvändig fakta (A), introducera konflikten (B), fortsätt med vad man ska göra åt det (T), och avsluta med en CTA som lockar till vidare läsning.
3. **Byline:** Text: Thomas Barregren (eller den som anges i briefingen).
4. **Lead:** Första stycket i brödtexten. Kommer direkt efter byline, utan föregående H2. Introducerar ämnet och sätter förväntan. Ska genuint vara textens första stycke – inte en fortsättning på standfirst. Lead tar en annan ingång än standfirst. Om standfirst sammanfattar riskerna kan lead till exempel introducera det beteendemönster artikeln vill bryta. Standfirst och lead ska inte börja med samma ord.
5. **Första mellanrubrik (H2):** Därefter följer resten av artikeln med H2-rubriker och brödtext som vanligt.

**Flerstyckes-lead:** Normalt är leaden ett enda stycke, men en lead med flera stycken kan vara motiverad när artikelns ingång kräver ett scenario (situation → komplikation → löfte). I sådana fall bör ABT-strukturen vara tydlig: ett eller två stycken sätter scenen (A), ett stycke introducerar komplikationen (B), och det sista stycket ger artikelns löfte eller vägkarta (T). En flerstyckes-lead kräver att det sista stycket gör ett explicit löfte som resten av artikeln sedan infriar – utelämna inte något du har lovat.

**Upprepningsregel:** Varje element i texten måste ha ett eget jobb. Detta gäller genomgående – inte bara inledningen. Om en brygga och ett pratminus säger samma sak, stryk ett av dem. Om ett stycke och en mellanrubrik uttrycker samma poäng, omformulera. Specifikt för inledningen: när man läser title, standfirst, lead och första H2-avsnitt i följd ska läsaren aldrig uppleva att samma sak upprepas. Varje del har ett distinkt jobb: title + standfirst = fristående puff; lead introducerar och driver vidare; första H2-avsnittet konkretiserar med detaljer och exempel. Tumregel: om du kan stryka title, standfirst eller lead utan att läsaren missar någon ny information har du upprepat dig.

**Stycken:** Normalt 2–3 meningar, max ~80 ord. Varierande meningslängd. En mening (eller ett ord) är ok om det är motiverat.

**Mellanrubriker:** H2, max 70 tecken, beskrivande. Normalt 2–3 stycken mellan dem. Sista mellanrubriken inleder avslutningen.

**Avslutning:** Infria inledningens löfte. Det sista avsnittet (under en egen H2) ska uppmana läsaren att göra något konkret baserat på det artikeln har handlat om. Avsnittet ska innehålla en länk till en sida som hjälper läsaren att utföra handlingen (t.ex. en sida med kontaktformulär, en produktsida eller en landningssida). Länkens URL och ankartext anges i briefingen.

### Pressmeddelande

1. **Rubrik:** Presens, aktiva verb, max 70 tecken. Siffror ökar nyhetsvärde.
2. **Sammanfattning:** Företagsnamn + nyhet. Max ~60 ord. Ska fungera som notis med rubriken.
3. **Pratminus 1:** Citat som kommenterar, drar slutsatser, tycker till.
4. **Fördjupning:** 1–2 stycken, neutral ton. En journalist ska kunna lyfta rakt in.
5. **Pratminus 2:** Lyft fram viktigt budskap. Citat för subjektiva tolkningar, inte fakta.
6. **Bakgrund:** Information journalisten kan använda. Riskerar att utelämnas.
7. **Bonusmaterial:** Länkar till bilder, webb etc.
8. **Kontaktinformation:** Namn, titel, telefon, e-post.
9. **Företagsinformation:** Kort, faktabaserad, neutral boilerplate.

Pratminus (–) är standard för anföring i pressmeddelanden. Aldrig citattecken.

## Arbetsflöde

### Steg 1 – Ta emot briefing

Du behöver svar på dessa frågor innan du börjar. Saknas svar, fråga – och för varje fråga presentera tre alternativ: (1) ditt förslag, (2) Claude bestämmer själv, (3) användaren fyller i eller länkar till material.

- **Arbetsrubrik**
- **Målgrupp**
- **Avsändarens syfte** – Vad vinner avsändaren på att målgruppen läser texten? ("What's in it for me?" ur avsändarens perspektiv.) Påverkar CTA.
- **Målgruppens behållning** – Vad vinner läsaren? ("What's in it for me?" ur läsarens perspektiv.)
- **Bakgrund/kontext/fakta** – Ofta längre text, t.ex. komplett research.
- **Vinkel** – Perspektiv, infallsvinkel eller huvudpoäng.
- **Krok** – B:et i ABT.
- **Kanal** – Webb, pressmeddelande, e-bok, kundcase etc.
- **Omfattning** – I poäng (0.5, 1, 2, 3, 5, 8, 13, 21) eller ungefärligt antal ord.

### Steg 2 – Presentera idé

Innan du skriver, presentera en kort beskrivning av hur texten kan se ut. Upprepa inte svaren från steg 1 – fokusera på att ge användaren trygghet i att du har en bra plan. Beskriv:

- Om texten ska ha "du"/"jag"-tilltal eller inte.
- Språk (svenska, BrE, AmE).
- Övergripande struktur och ton.
- Hur ABT-strukturen tänks fungera.

Ställ eventuella kvarvarande frågor. **Vänta på användarens godkännande innan du skriver.**

### Steg 3 – Skriv

Producera texten som en markdown-fil. Medan du skriver, håll dessa frågor i bakhuvudet:

- Förklarar jag begrepp innan jag använder dem?
- Följer varje stycke naturligt från det föregående?
- Driver ABT-strukturen texten framåt utan att synas?
- Låter jag understatementen göra jobbet istället för explicit entusiasm?
- Skulle en svensk journalist skriva så här?

### Steg 4 – Redaktörsfas

Granska texten med redaktörsögon innan du levererar:

- **Snubbeltrådar:** Finns begrepp som används innan de förklarats? Obesvarade frågor?
- **Flöde:** Känns stycken/avsnitt staplade? Är övergångarna sömlösa?
- **Ordning:** Är uppräkningar logiskt sorterade?
- **Struktur:** Är ABT osynlig men närvarande?
- **Ton:** Inte för blommig, inte för torr?
- **Svenska:** Luktar någon mening engelska? Finns anglicismer eller AI-avslöjande konstruktioner?
- **Konsistens:** Samma pronomen för samma person genomgående. Samma term för samma begrepp.
- **Precision:** Är slutsatserna korrekta utifrån källmaterialet? Finns ungefärliga termer som borde vara exakta? Signalerar något ordval något oavsett?
- **Elementens jobb:** Har varje element (brygga, pratminus, stycke) ett eget jobb, eller säger två element samma sak?
- **Läsarrespekt:** Finns formuleringar som kan uppfattas som nedlåtande, anklagande eller pekpinniga?
- **Brödtextens självständighet:** Kan brödtexten läsas och förstås utan rubrik, standfirst och mellanrubriker?
- **Typografi:** Rätt tankstreck, citattecken, tusenavskiljare, förkortningsformat för valt språk?
- **Format:** Följer texten rätt formatmall för texttypen?

Åtgärda problem tyst. Leverera en polerad text – inte en lista med korrigeringar.

## Poängskala (referens)

| Poäng | Exempel                                                      |
| ----- | ------------------------------------------------------------ |
| 1     | Kort/enkelt pressmeddelande/nyhet, ingen intervju/research, ≤ 300 ord, typiskt ~ 200 ord |
| 2     | Medellångt/normalt pressmeddelande/nyhet, kräver intervju/research, ≤ 500 ord, typiskt ~ 300 ord |
| 3     | Långt/krävande/avancerat/utförligt pressmeddelande/nyhet, kräver research, ≤ 800 ord, typiskt ~ 500 ord |
| 3     | Kort/enkel artikel/blogginlägg/ebokskapitel, ingen intervju/research, ≥ 500 ord, typiskt ~ 800 ord |
| 5     | Medellång/normal kundcase/artikel/blogginlägg/ebokskapitel, kräver intervju/research, ≥ 500 ord, typiskt ~ 1000 ord |
| 8     | Lång/krävande/avancerad/in-depth kundcase/reportage/artikel/blogginlägg/ebokskapitel, kräver intervju/research, ≥ 1000 ord, typiskt ~ 1500 ord |
| 8     | Corner stone content, webbcopy till pillar page och liknande, ≥ 500 ord, typiskt ~ 1000 ord |
| 13    | Rapport/whitepaper, kräver intervju/research, ≥ 1500 ord, typiskt ~ 3000 ord |
