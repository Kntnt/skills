# Aktuella restärenden efter den redaktionella leveransen

På Thomas begäran den 20 september 2026 ersätts de sex öppna ärendena i #329-familjen med tre självbärande arbetsärenden. Den stora omskrivningen och tidigare verifierade förbättringar är levererade. Återstående fel är avgränsade, men deras lösningssvårighet är inte fastställd.

| Aktiv ticket | Återstående problem | Ersätter |
| --- | --- | --- |
| [#362](https://github.com/Kntnt/skills/issues/362) | Källkontroll: bevara faktisk betydelse, upptäcka variabelbyten och undvika falska kontextfynd | #357, #360 och motsvarande delar av #329 |
| [#363](https://github.com/Kntnt/skills/issues/363) | Citat: idiomatisk svenska och bevarande av fungerande engelska samtidigt | #341, #358 och motsvarande delar av #329 |
| [#364](https://github.com/Kntnt/skills/issues/364) | Write: citatbryggor som inte föregriper hela kundomdömet | #361 och motsvarande delar av #329 |

De gamla sex ärendena har stängts som ersatta (`not_planned` i GitHubs statusfält), **inte som lösta**. Slutkommentarerna pekar vidare. Historiska underkännanden, krav och hela trådar bevaras. Ingen ny samlingsissue behövs; de tre ticketsen beskriver det återstående arbetet och sin samordning. #328 är ett separat återhämtningskontrakt och lämnas oförändrat.

Varje ticket innehåller problem och exakta kontraster, vad som redan fungerar, genomförda försök med utfall, oprövade hypoteser, aktuella laddningsvägar, verkliga anrop, frysta fullständiga källor/exempel, evidensvägar, regressionsgränser och verifierbara acceptanskriterier. Källkontrollen och citatbedömningen har vardera två felriktningar; de ska förbättras tillsammans så att strängare kontroll inte bara skapar fler falska fynd. Citatbryggan är ett separat kompositionsproblem.

Rekommenderad första prioritet är #362:s sakfel. Diagnoser kan ske oberoende, men en integrator behöver samordna överlappande produktändringar och regressionsprovning. Ingen oprövad hypotes är beställd som färdig lösning. De utförliga ticketsen är arbetsunderlag, inte instruktioner att kopiera in i Skillsens korta runtime-resurser.

## Bas och åtkomst

Basen är lokal `main` vid `b004f223634a2de15cf04e73551b1b006e46df62` i `/Users/thomas/Projects/skills`, med oförändrade produktfiler från den utvärderade `5ecadb76`. Evidenscommiten är `12373d80`. Dessa commits är ännu inte pushade; nya agenter ska kontrollera gitobjekten och använda denna checkout/historik, inte anta att en GitHub-klon eller global installation innehåller kandidaten. Ticketsen gör de centrala fallen läsbara även utan de lokala råspåren. Överlämning till en annan maskin behöver inkludera historiken/evidensen för reproduktion.

Ingen produktändring eller ny native-utvärdering görs i denna omorganisation. Inget pushas, releasas eller installeras globalt. Skyddad rework-branch/worktree lämnas orörda.

## Bevarat underlag

- [Källkontrollens tickettext](source-meaning.md).
- [Citatbedömningens tickettext](quotation-judgement.md).
- [Citatbryggans tickettext](quotation-bridge.md).
- [Faktiska trackeråtgärder och kontrollkvitton](tracker-receipt.json).
- [Föregående implementations- och kvalitetsrapport](../completion-report.md).

`*-before.json` bevarar gamla hela trådar före omorganisationen; `*-after.json` bevarar de gamla ärendenas slutstatus. `*-created.json` är de nya publicerade kropparna, och kommentarernas exakta texter finns bredvid. Inlineexemplens SHA-256 kontrollerades mot gitinnehållet vid `b004f223`; tickettexternas publicerade kroppar kontrollerades mot de lokala filerna. Den historiska dispositionen i `../tracker/final-disposition.json` gäller det tidigare kvalitetsavslutet och skrivs inte om.
