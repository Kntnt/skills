Genomgången är klar. Texten är granskad som ett kundcase på svenska, har gått igenom en korrigeringsrunda och avslutats med en mekanisk korrekturläsning, som inte hittade något att rätta.

**Upplöst konfiguration**

- Genre: `case-study`, härledd ur texten — den är en kundberättelse som leverantören själv publicerar.
- Språk: svenska, härlett ur texten.
- Teknik: ingen. Genren `case-study` anger själv att den inte skrivs med någon särskild teknik, så ingen hämtades därifrån.
- Korrigeringsbudget: 1, som är standard, och den är förbrukad.

```markdown
# Elm Quays arbetsledare skulle välja reparationsloggen igen

**Elm Quay Housing provade en gemensam reparationslogg i två hus. Arbetsledaren Maya Lind vill göra om försöket, men skulle avsätta mer tid för förberedelser.**

För Elm Quays underhållsgrupp handlade försöket med en gemensam reparationslogg om att se samma information över skiftgränserna. Gruppen valde kategorierna; leverantören Svale konfigurerade loggen och utbildade sex medarbetare.

## Resultaten redovisas med ett förbehåll

Enligt Elm Quays interna försöksanteckning från den 4 december 2025 registrerades 31 ärenden under åtta veckor. Akuta ärenden och tidigare beställda arbeten ingick inte. Mediantiden från anmälan till tilldelning var två arbetsdagar, jämfört med tre under de föregående åtta veckorna.

Perioderna hade olika arbetsbelastning. Anteckningen tillskriver därför inte loggen skillnaden.

## Kunden väger nyttan mot förarbetet

– Vi lade mer tid på att enas om kategorierna än på att lägga in de första ärendena. Den tiden skulle jag avsätta innan nästa hus börjar, säger arbetsledaren Maya Lind.

– Jag skulle välja att göra försöket igen. Att ha en gemensam bild av ärendena hjälper oss, men jag skulle lägga till en vecka för förberedelser, säger Lind.

Kundcaset publiceras av leverantören Svale. [Läs Svales checklista för införandet](https://example.invalid/svale/checklist).
```

**Kvarstående iakttagelser**

Budgeten är förbrukad, och omläsningen hittade dessutom två iakttagelser som rundans egna reparationer skapade — en runda till hade alltså reparerat föregående rundas arbete. Tre iakttagelser står kvar, alla olösta.

1. **Byline saknas.** Artikelanatomin kräver en byline mellan ingress och inledning, och mätningen rapporterar den som frånvarande både före och efter korrigeringen. Varken texten, dess metadata eller anropet namnger någon upphovsperson, så raden lämnas ofylld i stället för att fyllas med ett påhittat namn. Den behöver du sätta dit.

2. **Rubriken och ingressen säger nu samma sak.** Den nya rubriken, "Elm Quays arbetsledare skulle välja reparationsloggen igen", gör samma påstående som ingressens andra mening, "Arbetsledaren Maya Lind vill göra om försöket". Rubrik och ingress ska komplettera varandra, inte upprepa varandra. Iakttagelsen följer av rundans egen reparation: den gamla rubriken, "Elm Quay samlade reparationsärendena", byttes därför att den i bestämd form plural hävdade mer än texten, som uttryckligen undantar akuta ärenden och tidigare beställda arbeten. Bytet rättar det, men lägger rubriken ovanpå ingressen. Lägg märke till att den nya rubriken också säger att arbetsledaren skulle välja loggen igen, medan citatet säger att hon skulle göra om försöket.

3. **De två citaten från Lind står nu omedelbart efter varandra.** Rundan flyttade det första citatet ned under den sista mellanrubriken för att inledningen skulle bli ett enda stycke, som anatomin kräver. Det löste den saken, men nu följer "Den tiden skulle jag avsätta innan nästa hus börjar" direkt av "men jag skulle lägga till en vecka för förberedelser" — samma poäng två gånger i rad, utan berättande text emellan. Genren vill att berättandet gör kopplingsarbetet mellan citaten. Orden är kundens egna, så det som ska ändras är texten runt dem.

**Ändrade påståenden**

Inget påstående togs bort. Två ändrades:

- Rubriken hävdade tidigare att Elm Quay samlade reparationsärendena; nu hävdar den att Elm Quays arbetsledare skulle välja reparationsloggen igen. Ändringen svarar på iakttagelsen att rubriken hävdade mer än texten.
- "programvaran" blev "loggen" i meningen "Anteckningen tillskriver därför inte loggen skillnaden." Ändringen svarar på iakttagelsen att loggen hade fått ett tredje namn, och på den omvända ordföljden i samma mening. Förbehållet står kvar med full kraft: anteckningen tillskriver fortfarande inte skillnaden någon orsak.
