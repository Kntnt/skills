*Prepared by Codex for the commissioned GPT retest. Local draft; publication awaits Thomas's decision.*

## GPT-omprovet är genomfört

Sex färska `/write`-körningar (tre `en_US`, tre `en_GB`) och sex kompletta checkerprov av oförändrad `p3-document-scope`, mot frysta `fb16908712c4d47a36fc6ee9dfb3eb2714a19e65`, main vid start. Faktisk seat: `gpt-6.1-sol/xhigh`, native Codex CLI `0.159.3`, samma för föräldrar, barn och blinda domare. Historiska `gpt-6-astra/high`/CLI `0.155.1` är ingen baslinje. Main avancerade senare till `fe2587b7`; provet bytte inte revision.

Plan och kriterier committades före körning. Full evidens: `docs/evaluation/editorial-362/gpt-retest-2026-10-01/README.md`; nya records: `docs/evaluation/records/write-gpt-2026-10-01-362.md` och `source-check-gpt-2026-10-01-362.md`. Gamla planer, underkännanden och evidens står orörda.

**Beställningens utfall:**

- Levererat utkast, exakt sista jämförda prosa med full redovisning av kvarstående fynd, samt okänt/frånvarande: **6/6 pass** på vardera.
- Digital vana uttrycks i alla sex. **5/6 råbedömningar pass**, GB första fail på räckvidden i “familiarity with digital technology”. US tredje och GB tredje domarna accepterar samma uttryck i sina texters kontext. Alla läsningar bevaras; ingen önskad ombedömning har valts.
- F1 på artikeln: **4/6 pass**. F1 på hela leveranssvaret: **2/6 pass**, eftersom US andra och GB tredje accepterar falska checkerfynd och beskriver dem som kända defekter i leveransredovisningen. G2: **5/6 pass**, med standfirstens fristående funktion underkänd i US tredje. L1 och övriga semantiska/locale/teknikvalskriterier passerar alla sex.
- Elva genomförda källjämförelser: **17 stödda, 4 falska, 0 omstridda formella fynd**. Två separata redaktionella försiktighetsanmärkningar är omstridda. Varje rapportversion, mellanliggande rättning och disposition bedöms; lågt fyndantal innebär inget godkännande.
- Dokumentgränsen upptäcks korrekt **4/6** gånger och missas **2/6**. Båda missarna ser/diskuterar förskjutningen men avfärdar den. Inga andra, falska eller omstridda formella fynd. Det är samma missandel som det historiskt parkerade Claude-resultatet, som en separat mätning på annan seat/revision. Det belägger inte att en extra checker hjälper.

Två kapacitetsavbrutna checkerförsök är void och har ersatts på samma seat. De partiella upptäckterna räknas inte. Ett separat stagingfel startade ingen native-domare. Full traceaudit hittar inga serviceavbrott i räknade körningar eller domare.

**Spårens begränsningar:** krypterade checkerbriefingar är overifierade. R2 har två verkliga valideringsfel och fyra skips på återstående hela-certifiering; faktisk laddning, färska kontexter, budget, barnens avslut och prosafrysning är belagda. De första rådomarnas krav på Proofread i Write är ett tillämpningsfel: Write förbjuder det och Redline har det avslutskravet. Rårapporterna är bevarade och felaktig tillämpning förklarad. GB första O1 saknar full attribuering av HOME-effekter; källbevarande och ingen kvarvarande Skill-scratch är belagda på alla sex.

| Ursprungligt checklistkrav | Vad detta GPT-prov faktiskt uppfyller |
| --- | --- |
| 1 | Bevarande och separat redovisning av gamla/nya fel, rapportfel och oenigheter uppfyllt. |
| 2 | Leverans, skarp källstödd kritik och okänt/frånvarande uppfyllt; variabelutfall 5/6, med nämnd känslighet. Svensk kontroll och ny kausal före-/eftermätning ingår inte. |
| 3 | Krönika och svensk debatt inte beställda här. Alla engelska mellanled bedömda; två falska fynd accepterade. |
| 4 | Dokumentgräns 4/6; datum- och personattributkontroller inte beställda. Den parkerade frågan återgår till Thomas. |
| 5 | Write-antal, leverans och byteidentitet uppfyllt; inga nya Redline-par, stopp- eller beroendeprov beställda. |
| 6 | Aktuell fryst integrerad produkt har oberoende bedömts på alla tillämpliga kriterier; kvalitetsmissar och metodluckor står kvar. Historiska förhandskontraster kan inte skapas i efterhand. |
| 7 | Nya lokala records/evidens/commits färdiga, inga produkt- eller katalogändringar behövs. Ruff check/format, mypy och **2725 pytest-tester** passerar. |

Unik kärnresursläsning: 12314 ord plus 188 US/258 GB composition-ord; faktiska upprepade läsningar finns i spåren. Write tar 14,9–33,2 minuter, median 24,6. Checkerprov tar 9,7–13,6 minuter, median 12,0, med rapporter på 3994–5981 ord. Detta är aktuella mått, ingen kausal prestandajämförelse.

**Rekommenderad trackeråtgärd:** registrera omprovet som utfört, behåll `ready-for-human` tills Thomas avgör utslagen och följdärendena. Två konkreta lokala defektförslag gäller falskt accepterat fynd/falsk leveransredovisning respektive standfirstens fristående funktion. Ett tredje lokalt förslag återger den parkerade dokumentgränsfrågan som en avgränsad mätning före eventuell extra checker. Ingen produktändring följer automatiskt av resultaten och inget ärende har publicerats genom detta prov. Ett avslut av beställningen ska beskrivas som slutfört omprov, aldrig som godkännande av alla ursprungliga kvalitetskrav.
