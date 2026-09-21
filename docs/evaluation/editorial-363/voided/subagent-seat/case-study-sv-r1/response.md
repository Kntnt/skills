**Utkastet levereras med en känd brist.**

Fyndet som står kvar efter den avslutande jämförelsen gäller källtäckning:

- **Passagen:** ”Här är vad de mätte, vad mätningen inte kan svara på …” i ingressen.
- **Problemet:** *de* är plural, men ingen plural referent står i texten. Närmast före pronomenet står *Svale Systems* och *sex medarbetare*, så meningen kan läsas som att leverantören eller de utbildade utförde mätningen.
- **Vad materialet bär i stället:** siffrorna kommer ur Elm Quays interna testnotering den 4 december 2025. Materialet säger ingenstans att Svale har mätt något.
- **Minsta reparation som granskaren föreslog:** byt *de* mot *Elm Quay* — ”Här är vad Elm Quay mätte, …”.

Reparationen är inte införd. Prosan levereras ord för ord som den avslutande jämförelsen läste den, eftersom en ändring efter den jämförelsen hade lämnat ogranskad text i utkastet.

```markdown
---
kntnt:
  genre: case-study
  technique: none
  language: sv
---

# Elm Quay samlade felanmälningar i en gemensam logg

Under åtta veckor hösten 2025 prövade Elm Quay Housing en gemensam logg för felanmälningar i två av sina hus. Underhållsteamet byggde sina egna kategorier, Svale Systems konfigurerade loggen och utbildade sex medarbetare. Här är vad de mätte, vad mätningen inte kan svara på och vad arbetsledaren skulle göra annorlunda nästa gång.

Av Thomas Barregren

Elm Quay Housing förvaltar 640 lägenheter. I september 2025 bestämde bostadsföretagets eget underhållsteam att pröva en gemensam logg för felanmälningar i två hus. Tidigare förvarades telefonanmälningar och e-post var för sig, och teamet ville att personal på olika skift skulle se samma uppgifter.

## Kategorierna kom från teamet, inte från leverantören

Elm Quay valde Svale Systems efter att ha prövat om loggen kunde visa status för varje reparation. Någon jämförelse med en annan leverantör redovisas inte.

Underhållsteamet utformade sina kategorier och höll telefonanmälan öppen för de boende. Svale konfigurerade loggen och utbildade sex medarbetare vid två tillfällen.

— Vi ville att kvällsskiftet skulle se vad morgonskiftet redan hade gjort. Kategorierna var våra; Svale hjälpte oss att lägga in dem i loggen, säger Maya Lind, arbetsledare för underhållet.

## Siffrorna visar en skillnad men förklarar den inte

Enligt Elm Quays interna testnotering den 4 december 2025 registrerades 31 felanmälningar under de åtta veckorna. Noteringen utesluter akutärenden och arbete som beställts före testet.

Mediantiden från felanmälan till tilldelning var två arbetsdagar under testet och tre under de åtta veckorna dessförinnan. Perioderna hade olika arbetsbelastning, och noteringen avstår uttryckligen från att tillskriva programvaran skillnaden.

Det finns inga mätningar av kostnader, de boendes nöjdhet eller hur lång tid arbetena tog att slutföra.

## Kategorierna ska prövas mot större reparationer

Testet har ännu inte utvidgats. Teamet ska ta ställning när det har kontrollerat hur kategorierna fungerar för större reparationer.

— Vi lade mer tid på att enas om kategorierna än på att registrera de första anmälningarna. Den tiden skulle jag avsätta innan nästa hus drar igång, säger Maya Lind.

## Arbetsledaren säger ja – med förbehåll

— Jag skulle välja att göra testet igen. Att ha en samlad bild av anmälningarna hjälper oss, men jag skulle lägga till en extra vecka för förberedelser, säger Maya Lind. Någon rekommendation av Svale till alla bostadsföretag ger hon inte.

Den som överväger ett eget test kan läsa igenom implementeringschecklistan på https://example.invalid/svale/checklist innan beslutet tas.
```

**Så löstes körningen upp**

- Genre: `case-study`, angivet i anropet.
- Teknik: ingen. Genren case-study anger själv att den inte skrivs med någon teknik, så ingen berättarbåge har lagts på texten.
- Språk: svenska (`sv`), angivet i anropet. Brief och material är på engelska, och de tre citaten är översatta.
- Utdata: svaret. Ingen fil har skrivits som textens destination, och körningens egna arbetsfiler är borttagna.

**Bylinen**

Uppdraget namnger ingen författare, så bylinen bär användarens namn: *Av Thomas Barregren*. Ska texten publiceras osignerad eller under någon annans namn måste raden ändras före publicering.

**Jämförelserna**

Den första jämförelsen lämnade tre fynd om källtäckning — ”finns inte” om en jämförelse som materialet bara säger är otillgänglig, en för vid formulering av Linds förbehåll, och en rubrik som bar siffran 31 utan noteringens undantag — och alla tre reparerades. Den reparerade texten lästes därefter av två granskare, var för sig och på samma ordalydelse. Den ena rapporten skrevs till en annan plats än den anvisade och hittades först i efterhand; den lämnade inga fynd. Den sista fullständiga jämförelsen är den som lämnade fyndet ovan, och det är den rapporten som är prövad här. Ingen av jämförelserna lämnade något fynd om översättningen av citaten.

**Var materialet tar slut**

Uppdraget ber om ungefär 400 ord ”as material allows”. Brödtexten ligger på 389 ord, så längden är nådd utan att något har lagts till.

Materialet bär inte: någon jämförelse med någon annan leverantör, några mätningar av kostnad, av de boendes nöjdhet eller av tiden till färdigt arbete, någon röst utöver Maya Linds tre citat, något om hur kategorierna är utformade, något om de två husen, och inget utfall av kontrollen mot större reparationer.

Det som skulle bära en längre text är alltså: kategoriernas utformning, uppgifter om de två husen, citat från fler i teamet eller från någon boende, resultatet av kontrollen mot större reparationer, och mätningar av det som i dag inte är mätt.

**En redaktionell fråga, inte ett fel**

Materialet säger att fallet publiceras av leverantören och inte är oberoende journalistik. Utkastet gör inget anspråk på oberoende, men det säger heller inte vem som publicerar. Om texten ska bära en sådan upplysning är ett publiceringsbeslut.
