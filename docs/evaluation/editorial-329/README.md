# Redaktionell leverans #329 — läspaket

Arbetsversion: verkliga körningar pågår. Sammanställningen är inte ett slutligt godkännande.

Källmaterialet och måttstocken frystes i `6e531f5` innan omskrivningen. Baslinjen är `8ae4c21`; kandidaten är `d60c4fc`. Båda körs i separata, tillfälliga installationer med native Codex CLI 0.155.1 och den faktiskt observerade modellen `gpt-6-astra`, reasoning `high`. Ingen aktiv installation uppdateras. Endast GPT-familjen prövas.

[Beställning och original](sources/issue-329.md) · [Källförankring](source-map.md) · [Fryst matris](../corpus/editorial-quality/README.md) · [Läsbelastning](reading-load.md) · [Teknisk granskning](reviews/technical-review.md) · [Redaktionell granskning](reviews/editorial-review.md) · [Källgranskning](reviews/source-audit.md) · [Isolering och metod](reviews/harness-setup.md)

## Journalistiska genrer

Varje rad visar den fullständiga källan, första utkastet och Redlines faktiska svar. Ett oförändrat utkast kan vara ett korrekt resultat. Redline får enbart utkastet, inklusive metadata, aldrig källpaketet. Källorna är syntetiska och begränsade med avsikt. Språkets idiom, genrens hantverk och mekanik bedöms separat i de länkade protokollen.

| Genre / språk | Källa och brief | Första utkast | Redlines svar |
|---|---|---|---|
| article / sv | [källa](../corpus/editorial-quality/sources/article.md) | [Write](runs/candidate/article-sv/write/response.txt) | [Redline](runs/candidate/article-sv/redline/response.txt) |
| article / en_GB | [källa](../corpus/editorial-quality/sources/article.md) | [Write](runs/candidate/article-en_GB/write/response.txt) | [Redline](runs/candidate/article-en_GB/redline/response.txt) |
| article / en_US | [källa](../corpus/editorial-quality/sources/article.md) | [Write](runs/candidate/article-en_US/write/response.txt) | [Redline](runs/candidate/article-en_US/redline/response.txt) |
| case-study / sv | [källa](../corpus/editorial-quality/sources/case-study.md) | [Write](runs/candidate/case-study-sv/write/response.txt) | [Redline](runs/candidate/case-study-sv/redline/response.txt) |
| case-study / en_GB | [källa](../corpus/editorial-quality/sources/case-study.md) | [Write](runs/candidate/case-study-en_GB/write/response.txt) | [Redline](runs/candidate/case-study-en_GB/redline/response.txt) |
| case-study / en_US | [källa](../corpus/editorial-quality/sources/case-study.md) | [Write](runs/candidate/case-study-en_US/write/response.txt) | [Redline](runs/candidate/case-study-en_US/redline/response.txt) |
| column / sv | [källa](../corpus/editorial-quality/sources/column.md) | [Write](runs/candidate/column-sv/write/response.txt) | [Redline](runs/candidate/column-sv/redline/response.txt) |
| column / en_GB | [källa](../corpus/editorial-quality/sources/column.md) | [Write](runs/candidate/column-en_GB/write/response.txt) | [Redline](runs/candidate/column-en_GB/redline/response.txt) |
| column / en_US | [källa](../corpus/editorial-quality/sources/column.md) | [Write](runs/candidate/column-en_US/write/response.txt) | [Redline](runs/candidate/column-en_US/redline/response.txt) |
| opinion / sv | [källa](../corpus/editorial-quality/sources/opinion.md) | [Write](runs/candidate/opinion-sv/write/response.txt) | [Redline](runs/candidate/opinion-sv/redline/response.txt) |
| opinion / en_GB | [källa](../corpus/editorial-quality/sources/opinion.md) | [Write](runs/candidate/opinion-en_GB/write/response.txt) | [Redline](runs/candidate/opinion-en_GB/redline/response.txt) |
| opinion / en_US | [källa](../corpus/editorial-quality/sources/opinion.md) | [Write](runs/candidate/opinion-en_US/write/response.txt) | [Redline](runs/candidate/opinion-en_US/redline/response.txt) |

## Copy och UX

| Genre / språk | Källa och brief | Första utkast | Redlines svar |
|---|---|---|---|
| web-copy / sv | [källa](../corpus/editorial-quality/sources/web-copy.md) | [Write](runs/candidate/web-copy-sv/write/response.txt) | [Redline](runs/candidate/web-copy-sv/redline/response.txt) |
| web-copy / en_GB | [källa](../corpus/editorial-quality/sources/web-copy.md) | [Write](runs/candidate/web-copy-en_GB/write/response.txt) | [Redline](runs/candidate/web-copy-en_GB/redline/response.txt) |
| web-copy / en_US | [källa](../corpus/editorial-quality/sources/web-copy.md) | [Write](runs/candidate/web-copy-en_US/write/response.txt) | [Redline](runs/candidate/web-copy-en_US/redline/response.txt) |

## Bedömningar och bevis

Separata protokoll håller utkast och granskning isär. Varje körningsmapp bevarar exakt invocation, fullständigt svar, den givna indatafilen, observerad modell/revision, hela native-spåret inklusive korrigeringsagenter samt inventering före/efter av alla skrivbara platser. Filer som utvärderaren fångar är uttryckliga leverabler; de räknas inte som tillåtna filer skapade av en response-targeted Skill.

- Artikel och kundcase: [Write](../records/write-gpt-2026-09-19-338-part-article-case.md), [Redline](../records/redline-gpt-2026-09-19-338-part-article-case.md).
- Krönika, debatt och web-copy: [Write](../records/write-gpt-2026-09-19-338-part-column-opinion-web.md), [Redline](../records/redline-gpt-2026-09-19-338-part-column-opinion-web.md).
- Baslinje: [Write](../records/write-gpt-2026-09-19-338-baseline.md), [Redline](../records/redline-gpt-2026-09-19-338-baseline.md).

## Slutsatser och begränsningar

Slutsatser fylls i först efter genomförd matris och separat bedömning. En körning per cell i en native konfiguration är observerad täckning, ingen garanti för framtida litterär kvalitet. Andra providerfamiljer och språk är inte prövade. Misslyckade försök och omkörningar ska ligga kvar, med konkreta defekter länkade och olösta textproblem synliga.
