# Reading load — #331–337

Whitespace-delimited word counts, baseline `8ae4c21` versus the integrated candidate. Counts describe context cost, not quality targets. Language scopes are counted alone, as the resolver returns them. No rules have been displaced into this report.

## Authored resources

| Resource | Before | After |
|---|---:|---:|
| editorial/base.md | 2720 | 579 |
| editorial/base.review.md | 2559 | 324 |
| editorial/web-craft.md | 0 | 283 |
| editorial/web-craft.review.md | 0 | 133 |
| editorial/genres/article.md | 1461 | 206 |
| editorial/genres/article.review.md | 1938 | 131 |
| editorial/genres/case-study.md | 1369 | 251 |
| editorial/genres/case-study.review.md | 1668 | 130 |
| editorial/genres/column.md | 1183 | 201 |
| editorial/genres/column.review.md | 1445 | 126 |
| editorial/genres/opinion.md | 1223 | 194 |
| editorial/genres/opinion.review.md | 1435 | 116 |
| editorial/genres/web-copy.md | 1440 | 224 |
| editorial/genres/web-copy.review.md | 1472 | 148 |
| editorial/techniques/abt.md | 1049 | 251 |
| editorial/techniques/abt.review.md | 1753 | 123 |
| editorial/techniques/pac.md | 899 | 198 |
| editorial/techniques/pac.review.md | 1858 | 143 |

## Complete ordinary editorial contract paths

Each Write column includes base + selected genre + its ordinary technique (ABT before, none after) + composition scope, and candidate web-craft. Each review/correction column adds all applicable review halves, shared anti-slop and the language review/anti-slop scopes. Correction loads that same complete contract.

| Genre / locale | Write before | Write after | Review/correction before | Review/correction after |
|---|---:|---:|---:|---:|
| article / sv | 5796 | 1634 | 13916 | 4092 |
| article / en_GB | 5488 | 1326 | 13280 | 3456 |
| article / en_US | 5422 | 1256 | 13206 | 3378 |
| case-study / sv | 5704 | 1679 | 13554 | 4136 |
| case-study / en_GB | 5396 | 1371 | 12918 | 3500 |
| case-study / en_US | 5330 | 1301 | 12844 | 3422 |
| column / sv | 5518 | 1629 | 13145 | 4082 |
| column / en_GB | 5210 | 1321 | 12509 | 3446 |
| column / en_US | 5144 | 1251 | 12435 | 3368 |
| opinion / sv | 5558 | 1622 | 13175 | 4065 |
| opinion / en_GB | 5250 | 1314 | 12539 | 3429 |
| opinion / en_US | 5184 | 1244 | 12465 | 3351 |
| web-copy / sv | 5775 | 1652 | 13429 | 4127 |
| web-copy / en_GB | 5467 | 1344 | 12793 | 3491 |
| web-copy / en_US | 5401 | 1274 | 12719 | 3413 |

## Operational instructions and complete stage loads

The table above is the full prose contract, not the entire invocation. Add these operational files to each stage; the next table gives the resulting range across the 15 normal combinations. Correction brief counts exclude the user artifact/findings inserted into it. The invitation engine output and resolved-language JSON wrapper vary by path and are not prose-resource word counts.

| File | Before | After |
|---|---:|---:|
| skills/editorial/write/SKILL.md | 1852 | 1896 |
| skills/editorial/redline/SKILL.md | 3366 | 3449 |
| skills/editorial/redline/references/correction.md | 1236 | 1288 |
| skills/editorial/proofread/SKILL.md | 1961 | 1961 |
| skills/kntnt/library/references/delivery.md | 1721 | 1721 |
| skills/kntnt/library/references/editorial/mechanics.md | 2015 | 2015 |
| skills/kntnt/library/references/invocation-envelope.md | 950 | 950 |
| skills/editorial/write/references/quotations.md | 619 | 619 |

| Complete stage | Before range | After range |
|---|---:|---:|
| Write | 8717–9369 | 4861–5296 |
| Redline review | 17522–19003 | 8521–9306 |
| Correction | 13671–15152 | 4639–5424 |

Each Redline run additionally executes the installed Proofread stage once: its SKILL.md + delivery contract + shared mechanics + one language mechanics scope. This load is unchanged. The full cumulative pipeline is the Write stage plus Redline review plus that Proofread stage, and one correction stage per round actually used. Repeated reads are counted at each agent boundary rather than hidden by deduplication.

Conditional loads: quotation guidance when Write quotes speech; invocation-envelope guidance when contextual instructions are supplied. No other genre is loaded. Explicit ABT/PAC adds its base to Write and base/review pair to review/correction; the authored-resources table supplies these exact deltas. Genre inference considers only each opening, and help is not part of a writing/review invocation.
