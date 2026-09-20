## What to build

Få Write att låta en kunds citat bära sitt eget omdöme, med en brygga som ger relevant sammanhang utan att omedelbart sammanfatta hela svaret. Denna ticket ersätter återstående #361 och motsvarande begränsade genrekrav i #329. Det är en avgränsad kvarstående kompositionsbrist; genrebriefarna ska inte skrivas om från början.

### Felet och den redan verifierade nedströmsrättningen

På produkt `5ecadb76`, kompletterande `case-question-en_GB-r1`, introducerar Write sista citatet med:

> Asked about choosing the system again and what to change, Vale’s endorsement was specific to new jobs, with more time allowed before extending its use:

Citatet direkt därefter är:

> I would use it again for new jobs. I would allow another week to check the status names before adding the backlog.

Bryggan föregriper båda omdömespoängerna som citatet ska förmedla. Den tillför här ingen ny förståelse. **F1 passerar:** frågan och svarsinnehållet finns i underlaget. **G2 underkänns:** berättarröst och citat gör samma arbete två gånger. Det är inte det tidigare #352-felet med en uppdiktad intervjufråga; här är den verkligt ställd och ska få behållas.

Det separata källblinda Redline-provet på samma revision rättar bryggan till:

> Asked about choosing the system again and what to change, Vale said:

Hela citatet och texten i övrigt bevaras. Den faktiska frågan finns kvar, inget påstående går förlorat, och full privat Proofread-överföring passerar. Det är en godkänd kedjereparation, men Write-utkastets ursprungliga G2-fel består. Rättningen är **ett exempel, ingen föreskriven formulering**.

### Nuvarande kontrakt och vad som redan är gjort

`skills/kntnt/library/references/editorial/genres/case-study.md` säger redan att citaten bär kundens erfarenhet och omdöme, berättarrösten ger sammanhang/progression, och ”A bridge should prepare a quotation rather than pre-say it.” Genrebriefen är kort och anger ingen citatkvot. `case-study.review.md` läser bryggan tillsammans med citatet och tar bort redundant förhandsåtergivning med bevarad attribution och särskild sakuppgift. Den grenen fungerar i detta Redline-prov.

I tidigare original-US finns också en tydlig omdömesparafras som Redline rättar. Den senare ledtråden ”Lind’s assessment includes a reservation about preparation” är mindre tydligt redundant: en ämnesintroduktion är inte automatiskt ett facitfel bara för att ämnet återkommer i citatet. Bevara den distinktionen i positivkontrollerna. Inget generellt förbud mot citatbryggor eller kort ämnesorientering har stöd här.

Den färska källkontrollen ger inga sakfynd för GB-utkastet eftersom påståendena faktiskt är stödda. Det är korrekt avgränsning. Lösningen ska inte smyga in allmän genregranskning eller extra Proofread i Writes källjämförelse. Nuvarande slutprodukt och oberoende resursgranskning visar inget belagt motsägande krav i själva kompositionsinstruktionen. Därför har ingen ytterligare runtime-regel redan lagts till för detta exempel.

### Hypoteser och lämplig första diagnos

- Undersök om det vanliga skrivflödet eller en annan samtidigt laddad instruktion fördelar samma information till både berättarröst och citat. Kravet finns redan; en upprepning av samma regel är inte en förklaring.
- Pröva om en kortare/tydligare ansvarsfördelning vid kompositionen fungerar bättre, eller om en befintlig överstyrning kan tas bort. Bevara en självständig informativ ingress, naturlig brygga, faktisk intervjuattribution, kundperspektiv och den kvalificerade bedömningen.
- Använd fulltextkontraster: redundant återgivning av båda svarspoängerna, en legitim ämnes-/attributionsbrygga och en brygga med en unik nödvändig sakuppgift. Detta kan skilja funktion från en mekanisk regel som tar bort alla bryggor. Ingen sådan ny lösning har ännu verifierats.

### Evidens och reproduktion

- Fullständig källa och underkänt utkast: `F/runs/account-candidate/case-question-en_GB-r1/write/{supplied-input.md,artifact.md,response.txt}`. Båda finns även inline nedan.
- Verkligt anrop: `/write --genre=case-study --language=en_GB --output=response source.md`. Källa och prompt är oförändrade från den kompletterande frysta korpusen `bf14dc2`.
- Det separata anropet `/redline --output=response input.md` med hela levererade artefakten/metadata finns i samma pars `redline/`. Det får inte källan eller denna felbeskrivning.
- `F/reviews/account-new-judgements.json`, `account-new-verification.json`, `account-new.md` och `account-independent-observations.md` skiljer Write-fel från Redline-reparation.
- Formella records: `docs/evaluation/records/write-gpt-2026-09-20-344-account-new.md` och `redline-gpt-2026-09-20-344-account-new.md`.
- Den tydliga tidigare US-förhandsåtergivningen och rättningen: `F/runs/final-delivery-original/case-study-en_US-r1/`; dess separata källfel får inte räknas som ett G2-fynd. Full historik finns i `reviews/final-delivery-original.md`.

### Utgångsläge och sådant som redan är levererat

Detta är en renodlad fortsättning på #329, på Thomas uttryckliga begäran att ersätta den stora historiska ärendefamiljen med få självbärande restärenden. De gamla ärendena stängs som **ersatta, inte lösta**. Deras fel och evidens står kvar. Ingen fullständig redaktionell kvalitetsacceptans följer av omorganisationen. Uppgiften är att diagnostisera och verifierat rätta beteendet nedan; en dokumenterad teori ensam är inte avslut.

De fem genrebriefarna, deras review-delar, gemensam grund/webbhantverk, ABT/PAC, faktisk laddning, leveransregler och mekanisk filöverföring är redan implementerade och oberoende granskade. Behåll den leveransen; börja inte om med hela genreprojektet. #344, #349, #352–356 och #359 har verifierat avgränsade rättningar. #328 är ett separat, ännu öppet projektövergripande återhämtningskontrakt och ingår inte här.

**Arbetsbas:** lokal `main` i `/Users/thomas/Projects/skills` vid `b004f223634a2de15cf04e73551b1b006e46df62`. Produktfilerna är samma som den faktiskt utvärderade `5ecadb766ee1f9984a22d1702eb0e21ab2279971`; `12373d80` innehåller full slutevidens och `b004f223` tracker-kvittona. Dessa commits är ännu **inte pushade**. Kontrollera gitobjekten före arbete; en färsk GitHub-klon eller global Skill-installation kan ha äldre kod. På annan maskin behövs denna lokala historik/evidens innan samma baslinje kan återskapas. Exemplen nedan gör felet läsbart även utan den. Ingen push, release eller global installation är beställd genom denna ticket. Skyddad `rework` och dess worktree förblir orörda.

`F` nedan betyder `docs/evaluation/editorial-329/followup/`. Börja med `F/completion-report.md`, `F/reviews/final-technical-protocol-disposition.md` och `F/reviews/final-whole-resource-editorial.md`; läs sedan den konkreta evidens som hör till denna ticket. Hela den äldre historien behöver inte rekonstrueras för att förstå kraven här. Originalkorpus är fryst vid `6e531f5`; kompletterande källor vid `bf14dc2`. Fulla prompts, källor, rapporter, utkast, resultat och inventeringar ligger i respektive körningsmapp.

### Gemensamma krav som följer med från #329

Svenskt professionellt journalistiskt hantverk styr vinkel och disposition; målspråket styr idiom, syntax och typografi. Genreanvisningarna ska ge kort riktning och redaktionellt handlingsutrymme. Webbens mått är riktvärden, utan utfyllnad eller skadlig kapning. Ingen teknik väljs automatiskt för de fem genrerna; befintliga explicita val gäller. Behåll parser och publika anropsformer.

Write levererar ett första utkast med källtrohet; den källmedvetna jämförelsen är ingen allmän redaktionell eller mekanisk granskning. Redline ser hela textartefakten men inte Writes källpaket, granskar och korrigerar inom befintlig budget och avslutar med en faktisk installerad Proofread-pass. Mekaniken får inte göra redaktionella ändringar. Citat, metadata, destinationer och källfiler ska bevaras enligt respektive kontrakt.

De långa problembeskrivningarna här är arbetsunderlag för byggaren, **inte text att kopiera in i runtime-instruktionerna**. En ny allmän regel behöver en belagd orsak. Förenkling, borttagning eller annan processutformning får prövas; en viss tidigare implementation är inte facit. En eventuell ändring av det nuvarande kontrollantalet ska vara ett uttalat, diagnostiskt motiverat försök, med ny verifiering av leveransspärren och kostnaden.

### Utvärdering och leverans

Följ `docs/evaluation/protocol.md` och de ursprungliga kriterierna i `docs/evaluation/corpus/editorial-quality/README.md`. F1 betyder källtrogenhet, G2 genrens uppbyggnad, L1 målspråkets idiom och R1 korrekt granskning/bevarande. Bedöm alla tillämpliga kriterier, inte bara ticketens exempel. Bevara historiska underkännanden och varje ny körning. Skilj stödd rättning, omtvistad försiktighetsändring, felaktigt fynd, giltigt stopp, falskt stopp och levererad text. Ett stopp är aldrig ett godkänt utkast, och en Redline-reparation godkänner inte ett tidigare Write-utkast i efterhand.

Frys en proportionerlig matris med positiva och negativa kontroller och upprepningsantal före kandidatprovning. De centrala oförändrade källfallen ska köras mer än en gång; välj inte om bara misslyckade rader tills de passerar. Lägg till nya kontrastfall före produktändringen, med oberoende kriterier och utan en kanonisk formulering. En neutral diagnos som hittar felet motiverar ett försök men ersätter inte verkliga kandidat-Write→färsk-källblind-Redline-anrop. Ge aldrig utvärderarens fynd eller önskade ersättningsord till den provade Skillen.

Tidigare körningar använde native Codex CLI 0.155.1, observerad `gpt-6-astra/high`, utan modellöverskrivning. Följ protokollets providerisolering och ärv aktuell sessions identitet; registrera faktisk miljö och varje skillnad från baslinjen. Den historiska GPT-harnessen `docs/evaluation/editorial-329/harness/run.py` exporterar en oföränderlig revision till isolerad HOME/CODEX_HOME/work/scratch och vägrar skriva över resultat. Den innehåller historiska maskin-/sessionsvägar, bland annat `NATIVE_CODEX`, `PARENT_ROLLOUT`, `AUTHENTICATION` och `CLEANUP`: verifiera/anpassa evaluatorns miljö och identitetsfångst, inte produkt eller testkriterier, innan den används i en ny session. I en annan providerfamilj behövs dess eget stödda native-harness; styr inte Codex från en Claude-utvärdering eller tvärtom. En fristående semantisk bedömare får frysta kriterier och artefakter utan modellidentitet eller tidigare familjers omdömen. Publicera aldrig autentiseringsinnehåll.

Spara fullständiga in-/utdata, faktiska resursläsningar, rapporter, förälderns ställningstaganden, modellidentiteter, före-/efterinventeringar och städkvitton. Krypterade dispatchdelar är overifierade om ingen fullständig filavläsning ger separat insyn. Bedöm texten oberoende av granskarens eget godkännande. Använd fristående teknisk och redaktionell granskning av hela den berörda laddningskedjan, inte bara diffen. Integrera lokalt, verifiera den integrerade produktversionen och dokumentera vad som faktiskt uppfyllts. Om flera restärenden arbetas samtidigt måste en integrator samordna överlappande resursändringar och slutlig regressionsprovning.

Om en gemensam resurs ändras omfattar regressionen även de andra genrer och språk som faktiskt påverkas. Bevara tidigare godkända fall för källgränser, kundens aktörskap, författarståndpunkt, teknikval, webbformat och leverans; välj täckning efter diffen i stället för att göra om hela historiken.

Den tidigare fortsättningen innehåller 212 Skill-invokationer och 33 diagnoser, inte ett krav att göra om alla. Slutversionen hade 26 faktiska invokationer och ett beroendehopp. Fyra tekniska kontroller och 1 873 tester passerade. Dessa är historiska belägg, ingen textkvalitetsgaranti för nästa ändring. Mät samlad obligatorisk läsning och faktisk körningstid; Write hade redan fått 884 extra resursord och tog i sista urvalet median 616 sekunder. Slumpmässiga fallskillnader gör detta olämpligt som ett kausalt prestandamått.

<details>
<summary>Fullständig workshopkälla med de verkliga frågorna — fullständigt bevarat underlag</summary>

Proveniens: `docs/evaluation/editorial-329/followup/runs/account-candidate/case-question-en_GB-r1/write/supplied-input.md` vid `b004f223`; SHA-256 `75160dbc12d41294eccfc615f4a8e1b2df1b5202185f5ba1f24a2f3d5fd69afc`. Filbytesen i repo är auktoritativa vid återspelning.

````text
# Case-study brief and source

SYNTHETIC EVALUATION MATERIAL. Every name, event, quotation and document below is fictional. This is the complete source package. Source language: English.

## Brief

Write a journalistic customer case in British English for independent repair workshop managers. The publisher is scheduling software supplier Benchline; the customer is Fenwick Instrument Repairs. Approximately 250–300 words, in Markdown. Show what the customer changed, what the trial established and what its manager would approach differently. No author name or call to action is supplied.

## Material

Fenwick Instrument Repairs services brass and woodwind instruments. In January 2026 the workshop team began a six-week trial of a shared bench schedule. Previously, jobs awaiting parts and jobs ready for work appeared on separate paper sheets. The team chose Benchline after checking that it could distinguish these statuses.

The workshop defined the statuses and decided who would update them. Benchline configured those choices and trained four staff in one online session. The team continued to use telephone calls to discuss collection arrangements with customers.

The workshop's trial summary, dated 23 February 2026, records 38 jobs entered in the schedule. It says staff could see which instruments were waiting for parts. It does not measure repair duration, revenue or customer satisfaction. The manager approved continued use for new jobs but postponed adding the backlog until the team had reviewed its status definitions.

The following is a complete extract from an email interview on 2 March 2026 between Benchline's case writer and workshop manager Priya Vale. Publication of the extract was approved by Vale.

Question: “What did the team have to settle before the schedule was useful?”

Vale: “We had to agree what ready for work meant. A part being in the building did not always mean that it had reached the right bench.”

Question: “Would you make the same choice again, and what would you change?”

Vale: “I would use it again for new jobs. I would allow another week to check the status names before adding the backlog.”

The interview took place by email. No workshop visit, spoken exchange, expression or emotional reaction is recorded. The summary and interview establish the team's reported experience, not a measured improvement in repair speed or a recommendation for every workshop.
````

</details>

<details>
<summary>Fullständigt underkänt Write-utkast — fullständigt bevarat underlag</summary>

Proveniens: `docs/evaluation/editorial-329/followup/runs/account-candidate/case-question-en_GB-r1/write/artifact.md` vid `b004f223`; SHA-256 `3d3c89fc9739f46640f92c3dfd464db9bf6244dabc9226e1b3530594df964c20`. Filbytesen i repo är auktoritativa vid återspelning.

````text
---
kntnt:
  genre: case-study
  technique: none
  language: en_GB
---

# Fenwick puts waiting and ready jobs on one schedule

Fenwick Instrument Repairs’ six-week trial of a shared bench schedule recorded 38 jobs and, according to the workshop’s summary, let staff see which instruments were waiting for parts. The manager approved continued use for new jobs, while postponing the backlog pending a review of status definitions.

The brass and woodwind repair workshop began the trial in January 2026. Previously, jobs awaiting parts and those ready for work appeared on separate paper sheets. The team chose Benchline after checking that its software could distinguish the two statuses.

The workshop defined the statuses and decided who would update them. Benchline configured those choices and trained four staff in one online session. Telephone calls remained part of the process for discussing collection arrangements with customers.

In an email interview with Benchline’s case writer on 2 March, workshop manager Priya Vale described what the team had needed to settle:

‘We had to agree what ready for work meant. A part being in the building did not always mean that it had reached the right bench.’

The trial summary, dated 23 February 2026, documents the team’s reported experience. It does not measure repair duration, revenue or customer satisfaction, so it cannot establish whether repairs became faster.

Asked about choosing the system again and what to change, Vale’s endorsement was specific to new jobs, with more time allowed before extending its use:

‘I would use it again for new jobs. I would allow another week to check the status names before adding the backlog.’
````

</details>

## Acceptance criteria

- [ ] Det kompletta tidigare G2-underkännandet och dess separata F1-pass finns kvar, liksom den lyckade källblinda Redline-rättningen. Problemet sammanblandas inte med påhittad fråga eller citatets egna ordval.
- [ ] En diagnostiskt motiverad ändring eller förenkling prövas på oförändrad GB-källa/prompt i fördeklarerade upprepade riktiga Write-körningar. Levererade texter låter citatets omdöme göra eget arbete utan omedelbar full förhandsparafras; flera giltiga bryggor kan passera.
- [ ] Förfrysta positiva kontroller bevarar fungerande ämnes-/attributionsbryggor och unika sakuppgifter. Både källa med riktig fråga och källa utan lämnad fråga ingår; autentisk frågeinramning får inte förbjudas, osupplerad fråga får inte uppfinnas.
- [ ] Kundens aktörskap, ord, förbehåll, fakta, kronologi, metadata och informativa ingress bevaras. Ingen citatkvot, kanonisk mening eller allmän extra genregranskning i källkontrollen införs.
- [ ] Separata källblinda Redline-par bedöms för både rättning och bevarande; mekanisk filöverföring, en faktisk avslutande pass, leveransmål och städning verifieras. Write och sluttext får egna omdömen.
- [ ] Oberoende granskning av hela berörda resurser och verklig integrerad utvärdering visar förbättringen utan att försvaga kriteriet. Om bara den redan befintliga Redline-rättningen fungerar är Write-problemet fortfarande olöst.
- [ ] Berörda dokument/help/deklarationer hålls samstämmiga, katalogen regenereras där det behövs, lokala commits/integration och evidens färdigställs; de fyra aktuella kontrollerna i `CONTRIBUTING.md` passerar.

## Blocked by

Inga saknade implementationer blockerar start. Diagnos och tester är fristående; samordna överlappande case-study-resurser med citatärendet. Bygg inte #328 som sidoarbete och inför ingen ny samlingsissue enbart för att räkna dessa tre restärenden.

---
Written against b004f223 (product 5ecadb76).
