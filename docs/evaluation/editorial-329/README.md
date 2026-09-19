# Redaktionell leverans #329 — läspaket

**Aktuell fortsättning:** #329 har återöppnats för källtrohet och citatidiom. [Uppföljningen](followup/README.md) redovisar implementation, nya kontroller och aktuellt utfall. Avsnitten nedan är den första leveransens historiska läspaket vid `7ff6ec0`; dess issue-status och provantal gäller den tidpunkten.

Implementation och föreskriven utvärdering är genomförda. **Tre kvalitetsfel står kvar öppna: #341, #349 och #352.** Historiska fel och senare försök redovisas sida vid sida; de underkända texterna räknas inte som godkända.

Källor och bedömningsmatris frystes i `6e531f5` före omskrivningen. Baslinjen är `8ae4c21`; varje körning anger sin egen oföränderliga instruktionsrevision i `run.json` och sitt record. Slutliga produktresurser finns i `29ff204`; testavgränsningen rättas i `bda07f7`. Endast native Codex CLI 0.155.1 med faktiskt observerad `gpt-6-astra`, reasoning `high`, används. Inga andra providerresultat ingår.

[Beställning](sources/issue-329.md) · [Källförankring](source-map.md) · [Fryst matris](../corpus/editorial-quality/README.md) · [Läsbelastning](reading-load.md) · [Teknisk granskning](reviews/technical-review.md) · [Redaktionell granskning](reviews/editorial-review.md) · [Källgranskning](reviews/source-audit.md) · [Metod](reviews/harness-setup.md) · [Protokoll- och täckningsgranskning](reviews/protocol-final.md)

## Journalistiska genrer

Här visas de senaste ordinarie proven per språk. Länken till första utkastet innehåller hela texten; sluttexten efter ett korrekt no-change är samma artefakt. Redline får utkast och metadata, aldrig källpaketet. Fullständiga råsvar och leveranskonton finns i körningsmapparna. Tidigare försök finns kvar i [alla records](../records/README.md) och respektive körningskatalog. Alla källor är avsiktligt avgränsade och syntetiska.

| Genre / språk | Källa och brief | Första utkast | Efter Redline |
|---|---|---|---|
| article / sv | [källa](../corpus/editorial-quality/sources/article.md) | [Write](runs/completion-check/article-sv/draft.md) | [Redline](runs/completion-check/article-sv/final.md) |
| article / en_GB | [källa](../corpus/editorial-quality/sources/article.md) | [Write](runs/rerun-341/article-en_GB/write/artifact.md) | [Redline](runs/rerun-341/article-en_GB/redline/artifact.md) |
| article / en_US | [källa](../corpus/editorial-quality/sources/article.md) | [Write](runs/rerun-341/article-en_US/write/artifact.md) | [Redline](runs/rerun-341/article-en_US/redline/artifact.md) |
| case-study / sv | [källa](../corpus/editorial-quality/sources/case-study.md) | [Write](runs/rerun-341-translation/case-study-sv/write/artifact.md) | [Redline](runs/rerun-341-translation/case-study-sv/redline/artifact.md) |
| case-study / en_GB | [källa](../corpus/editorial-quality/sources/case-study.md) | [Write](runs/rerun-341-translation/case-study-en_GB/write/artifact.md) | [Redline](runs/rerun-341-translation/case-study-en_GB/redline/artifact.md) |
| case-study / en_US | [källa](../corpus/editorial-quality/sources/case-study.md) | [Write](runs/rerun-341-translation/case-study-en_US/write/artifact.md) | [Redline](runs/rerun-341-translation/case-study-en_US/redline/artifact.md) |
| column / sv | [källa](../corpus/editorial-quality/sources/column.md) | [Write](runs/completion-check/column-sv/write/artifact.md) | [Redline](runs/completion-check/column-sv/redline/artifact.md) |
| column / en_GB | [källa](../corpus/editorial-quality/sources/column.md) | [Write](runs/rerun-column-final/column-en_GB/write/artifact.md) | [Redline](runs/rerun-column-final/column-en_GB/redline/artifact.md) |
| column / en_US | [källa](../corpus/editorial-quality/sources/column.md) | [Write](runs/rerun-column-final/column-en_US/write/artifact.md) | [Redline](runs/rerun-column-final/column-en_US/redline/artifact.md) |
| opinion / sv | [källa](../corpus/editorial-quality/sources/opinion.md) | [Write](runs/rerun-349-source-check/opinion-sv/artifact.md) | [Redline](runs/rerun-349-source-check/opinion-sv/final.md) |
| opinion / en_GB | [källa](../corpus/editorial-quality/sources/opinion.md) | [Write](runs/rerun-349-source-check/opinion-en_GB/artifact.md) | [Redline](runs/rerun-349-source-check/opinion-en_GB/final.md) |
| opinion / en_US | [källa](../corpus/editorial-quality/sources/opinion.md) | [Write](runs/rerun-349-source-check/opinion-en_US/artifact.md) | [Redline](runs/rerun-349-source-check/opinion-en_US/final.md) |

## Copy och UX

| Genre / språk | Källa och brief | Första utkast | Efter Redline |
|---|---|---|---|
| web-copy / sv | [källa](../corpus/editorial-quality/sources/web-copy.md) | [Write](runs/rerun-345/web-copy-sv/artifact.md) | [Redline](runs/rerun-345/web-copy-sv/final.md) |
| web-copy / en_GB | [källa](../corpus/editorial-quality/sources/web-copy.md) | [Write](runs/rerun-345/web-copy-en_GB/artifact.md) | [Redline](runs/rerun-345/web-copy-en_GB/final.md) |
| web-copy / en_US | [källa](../corpus/editorial-quality/sources/web-copy.md) | [Write](runs/completion-check/web-copy-en_US/draft.md) | [Redline](runs/completion-check/web-copy-en_US/final.md) |

## Teknikval och kontroller

De uttryckliga teknikproven bevarar både teknikens relationer och genrens form. En lyckad sluttext gör inte ett felaktigt första utkast godkänt.

| Prov | Write | Redline | Observerat |
|---|---|---|---|
| article / ABT / sv | [utkast](runs/candidate/article-abt/write/artifact.md) | [sluttext](runs/candidate/article-abt/redline/artifact.md) | Write bytte okänd förekomst mot hur elever frös; Redline rättade endast hur till om (#347). |
| article / PAC / en_GB | [utkast](runs/candidate/article-pac/write/artifact.md) | [svar](runs/candidate/article-pac/redline/artifact.md) | Fakta, analys och begränsad slutsats med tidigt besked. |
| web-copy / ABT / sv | [utkast](runs/rerun-345/web-copy-abt/artifact.md) | [svar](runs/rerun-345/web-copy-abt/final.md) | Fungerande sektionsfrågor; en onödig genredefinitionsläsning registrerad separat (#350). |

[Sju separata urvalskontroller](../records/redline-gpt-2026-09-19-338-selection.md) prövar metadata/instruktion med none, äldre ABT-metadata, flaggans prioritet, namngiven ABT-instruktion, PAC-rapportens tidiga besked och ett artikelutdrag. Faktiska läsningar verifierar urvalet. Report laddar inte femgruppens webbgrund.

[De tio ursprungliga genrekontrollerna](../records/redline-gpt-2026-09-19-338-controls-genres.md) har rena och bristfälliga texter för varje genre. [Kontrollrapporten](reviews/controls-genres.md) länkar alla artefakter och omkörningar: bland annat rättad helmeningsdublett med bevarad ren artikel (#346), fungerande kundcitat som inte misstänkliggörs för sin flytande form och webbsidans korrekta villkor/handling. Den frysta case-study-clean-texten innehåller själv ett citatidiomfel; clean-etiketten är därför en begränsning i kontrollupplägget, aldrig skäl att sätta pass. Den bristen missades även i omkörningen.

## Jämförelse och kvarstående brister

[Baslinjens sex par](reviews/baseline.md) bedömdes före jämförelsen. Fem Redline-körningar kunde inte slutföra Proofread på grund av YAML i parserargumentet (#339); två korrigeringsagenter lämnade UV-filer (#340). Kandidatens metadataöverföring och korrigeringsstädning har verifierats i verkliga körningar. Baslinjens ofullbordade sluttexter markeras som skipped, inte som godkända eller förmodat sämre.

Väsentliga påvisade rättningar omfattar krönikans författarperspektiv (#342), debattörens faktiska ståndpunkt (#343), länkad kontra inbäddad formulärfunktion (#345), redaktionellt ansvar för hela dubblerade meningar (#346) och giltig svensk gemen efter kolon (#348). Varje rättning har bevarade före/efter-prov. Den senare ändringen i citatreglerna undanröjer en faktiskt motsägande ord-för-ord-regel; textutfallet bedöms separat.

**Källtrohetsfelet #349 är ännu inte verifierat rättat.** Frånvaron av ett anspråk på kostnadsberäkning/finansiering blir i flera debattutkast ett påstående att arbetet inte har gjorts. Det förekommer också i baslinjen. Tidigare felaktiga pass-bedömningar har fått synliga, överordnade fail-tillägg; originalen är kvar. Förtydligad kunskapsgräns och källkontroll under skrivandet har hittills inte undanröjt felet. En källblind Redline kan inte återställa den osedda uppgiften.

Kundcitatets svenska kalkering (#341) återkommer även i sista Write-provet. Där reparerar Redline den lokala referensen till ”innan försöket börjar i nästa byggnad”, med kundens betydelse och reservationer bevarade. Tidigare Redline-prov, även omkörningen av den frysta case-study-clean-texten, missade bristen. Writes L1-fel och de tidigare missarna står kvar; en lyckad korrigering gör dem inte godkända. Utvärderingen räknar inte nya synonymer, kortare stycken eller likhet med en mall som förbättring.

**Även #352 står öppet:** sista amerikanska kundcase-utkastet tillskriver mejlintervjun frågan ”Asked to assess the experience”, som källan inte belägger. Det är ett separat F1-fel trots i övrigt korrekta citat och fakta.

## Vad evidensen visar

Den frysta matrisens **65 invokationer** är genomförda: 15 ordinarie Write→Redline-par, tre teknikpar, sex baslinjepar och 17 separata Redline-kontroller. Totalt **119 invokationer** omfattar även 54 riktade omkörningar och bevarade tidigare försök. [Täckningsaudit](reviews/packet-coverage.json) identifierar varje obligatorisk cell. Antalet är täckning, inte antal godkända texter.

Varje körningsmapp innehåller exakt invocation, fullständigt svar, given indata, revisions-/modellidentitet, native-spår för förälder och barn samt inventering före/efter av samtliga skrivbara rötter. Utvärderarens fångade artefakter är deklarerade leverabler. Response-targeted Skills får inte själva lämna dem efter sig. Privat installation, autentiseringskopians förändringsflagga, scratch, arbetskopia och resurser kontrolleras separat; native klientbootstrap klassificeras som Harness-effekt.

Native dispatchmeddelandets råa brödtext är krypterad i vissa spår. Där kan hela briefens bytes inte granskas direkt. Färsk start, faktisk barnmodell, lästa resurser, fullständig returtext, antal korrigeringsrundor och avslutande enda Proofread-pass går däremot att följa. Begränsningen är uttrycklig i records.

Källpaketen innehåller tydliga briefs och faktagränser. Proven visar hur hela instruktionen fungerar tillsammans med dessa briefs, inte vad genrefilen ensam kan åstadkomma. Enstaka prover i en modellkonfiguration ger ingen generell kvalitetsgaranti och säger inget om oprövade språk eller andra providerfamiljer. Projektets gröna kodsvit är separat teknisk evidens, inte ett betyg på prosan. Framtida användarerfarenhet är inte ett väntande godkännandesteg i detta uppdrag.

## Lokal leverans

Leveransen är integrerad genom fast-forward i lokal `main`, med komplett implementations- och evidenscommit `579ec85ee9d49c0ec65039e96d005c11fb7c98ac`. Arbetsbranchen `editorial-329` finns kvar som spårbar leverans. [De fyra slutkontrollerna](validation/final-results.json) passerar, inklusive **1 873 tester**; produktresurser, testkod och frysta källor har verifierats oförändrade efter respektive granskad revision.

[Det kontrollerade trackerutfallet](tracker/final-state.json) visar **#329 och 20 uppfyllda underärenden avslutade**. [#341](https://github.com/Kntnt/skills/issues/341), [#349](https://github.com/Kntnt/skills/issues/349) och [#352](https://github.com/Kntnt/skills/issues/352) är öppna. Varje ärende har en konkret slutkommentar med lokal commit och evidens; [kvittot](tracker/operations.json) länkar kommentarerna. Att ursprungsleveransen är avslutad innebär inte att de tre kvalitetsfelen är rättade.

Alla 119 privata körmiljöer är borttagna, egna processer avslutade och kvarvarande egen testscratch städad. Skyddad `rework` och dess worktree är orörda. Inget har pushats, releasats eller uppdaterats i aktiv global installation. [Arbetsloggen](WORKLOG.md) bevarar besluten och hela genomförandets historia.
