# Oberoende redaktionell granskning — #329

Granskad 2026-09-19: arbetskopian på `editorial-329`, med `6e531f5fe0b610e046ae58787f246cc6239acbcc` som HEAD och pågående implementation ovanpå. Kravbas: [#329 med senare förtydliganden](../sources/issue-329.md) samt hela #330–338 med kommentarer. Startrevisionen är `8ae4c21`; corpus är fryst vid `6e531f5`. Detta är en instruktionsgranskning, inte ett godkännande av den ännu pågående praktiska utvärderingen.

## Fynd E1 — svensk review drar slutsats om osedd citatkälla

**Resurs:** `skills/kntnt/library/references/languages/sv.md:54`, Review-stycket som börjar ”Check reported speech against the mark it is set in”. Det säger att välformulerat tal inom citattecken har reparerats och att citatmarkeringen därför är fel. Resursen laddas av både Redline och dess korrigeringsagent.

**Kravkälla:** [#331](../sources/issue-331.md) avgränsar granskningen till synliga brister; [#334](../sources/issue-334.md) förbjuder att underkänna ett trovärdigt citat för att intervjun inte kontrollerats. Samma gräns finns nu i `editorial/base.review.md`, `genres/case-study.review.md` och Redlines steg 6.

**Påverkan:** Ett verkligt ordagrant, välformulerat kunduttalande kan få ett falskt fynd och byta citatmarkering. Prosan visar inte om talaren uttryckte sig flytande eller om skribenten reparerade den. Instruktionen återinför därmed just den proveniensbedömning som de nya gemensamma resurserna tar bort.

**Minimal rättning:** Ersätt slutsatsen om reparerat tal med diagnostik som kräver belägg i själva texten. Bevara citatets markering när enda misstanken är att orden är välformulerade. Detta ändrar inte Writes citatpolicy eller svensk typografi.

**Disposition — rättat och verifierat 2026-09-19:** Review-stycket kräver nu textintern inkonsekvens, säger uttryckligen att flytande språk inte belägger ett reparerat citat och tillåter att skilda markeringar fyller skilda funktioner. Den rättningen undanröjer E1 utan att lägga till en annan provenienskontroll. Fyndet är stängt.

## Helhetsbedömning

Efter rättningen av E1 kvarstår ingen blockerande redaktionell motsägelse i det lästa paketet. Basen, webbgrunden, de fem genrerna och teknikerna är koncentrerade och lämnar vinkelns utförande, rytm och retoriska val åt skribenten. Webbskalan är uttryckligen vägledande. Artikelns form, kundens eget omdöme, krönikans personliga perspektiv, debattartikelns ståndpunkt och webbcopyns läsaruppgift är åtskilda utan nya block- eller citatkvoter.

Svenskt hantverk och målspråkets uttryck hålls isär. `none` är ordinarie teknik i femgruppen; explicit ABT/PAC har fortsatt en begriplig uppgift. Ingressen nås utan teaser-laddning. Write, Redline och den färska korrigeringsagenten har förenliga och avgränsade laddningsvägar. Source Fidelity, innehållsbevarande och en avslutande Proofread-pass kvarstår.

Läst: AGENTS.md, dokumentregler, writing-for-agents, editorial- och språk-README; hela base/web-craft och reviews; alla fem genrepar; båda teknikpar; anti-slop; sv/en_GB/en_US; Write/Redline inklusive hjälpsidor, correction och quotations; Proofread och mechanics. Även de tre sparade originaldokumenten, teaser-gränsen, aktiva corpusbeskrivningar och redovisningen av läsbelastning kontrollerades. Inga implementeringsfiler ändrades. Faktiskt textutfall och slutlig utvärdering återstår att granska när läspaketet är färdigt.
