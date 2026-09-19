# Reading load — #331–337

Whitespace-delimited words: baseline `8ae4c21c203fa44f9782c3c0db2c85a5d805c3a6` versus candidate `93758f4`. These are context costs, not quality targets or new rules. Reproduce with `python3 docs/evaluation/editorial-329/harness/reading_load.py`. The three language resources supply all scopes directly; scope counts match the resolver's body-only output. JSON wrappers, invocation results, supplied texts and findings are excluded because their lengths vary by run.

## Authored editorial resources

| Resource | Before | After |
|---|---:|---:|
| editorial/base.md | 2720 | 597 |
| editorial/base.review.md | 2559 | 347 |
| editorial/web-craft.md | 0 | 283 |
| editorial/web-craft.review.md | 0 | 133 |
| editorial/genres/article.md | 1461 | 206 |
| editorial/genres/article.review.md | 1938 | 131 |
| editorial/genres/case-study.md | 1369 | 251 |
| editorial/genres/case-study.review.md | 1668 | 167 |
| editorial/genres/column.md | 1183 | 214 |
| editorial/genres/column.review.md | 1445 | 126 |
| editorial/genres/opinion.md | 1223 | 208 |
| editorial/genres/opinion.review.md | 1435 | 116 |
| editorial/genres/web-copy.md | 1440 | 240 |
| editorial/genres/web-copy.review.md | 1472 | 166 |
| editorial/techniques/abt.md | 1049 | 251 |
| editorial/techniques/abt.review.md | 1753 | 123 |
| editorial/techniques/pac.md | 899 | 198 |
| editorial/techniques/pac.review.md | 1858 | 143 |

## Complete ordinary editorial contracts

Write includes base, selected genre, language composition and ordinary ABT before / shared web-craft without a technique after. Review and correction also include every applicable review half, shared anti-slop and language review/anti-slop. No rule has been moved into this report.

| Genre / locale | Write before | Write after | Review/correction before | Review/correction after |
|---|---:|---:|---:|---:|
| article / sv | 5796 | 1652 | 13916 | 4122 |
| article / en_GB | 5488 | 1344 | 13280 | 3497 |
| article / en_US | 5422 | 1274 | 13206 | 3419 |
| case-study / sv | 5704 | 1697 | 13554 | 4203 |
| case-study / en_GB | 5396 | 1389 | 12918 | 3578 |
| case-study / en_US | 5330 | 1319 | 12844 | 3500 |
| column / sv | 5518 | 1660 | 13145 | 4125 |
| column / en_GB | 5210 | 1352 | 12509 | 3500 |
| column / en_US | 5144 | 1282 | 12435 | 3422 |
| opinion / sv | 5558 | 1654 | 13175 | 4109 |
| opinion / en_GB | 5250 | 1346 | 12539 | 3484 |
| opinion / en_US | 5184 | 1276 | 12465 | 3406 |
| web-copy / sv | 5775 | 1686 | 13429 | 4191 |
| web-copy / en_GB | 5467 | 1378 | 12793 | 3566 |
| web-copy / en_US | 5401 | 1308 | 12719 | 3488 |

## Operational instructions and full stage costs

The editorial contract alone is not the full invocation. Write and review each add their SKILL.md and delivery contract. Each correction adds its complete correction brief. The final installed Proofread adds its SKILL.md, delivery, shared mechanics and the selected language's mechanics. Reads are counted again at each stage/agent boundary; incidental duplicate reads inside a stage are not contractual requirements and actual traces remain authoritative about run-specific overreads.

| File | Before | After |
|---|---:|---:|
| skills/editorial/write/SKILL.md | 1852 | 1896 |
| skills/editorial/redline/SKILL.md | 3366 | 3449 |
| skills/editorial/redline/references/correction.md | 1236 | 1288 |
| skills/editorial/proofread/SKILL.md | 1961 | 1961 |
| skills/kntnt/library/references/delivery.md | 1721 | 1721 |
| skills/kntnt/library/references/editorial/mechanics.md | 2015 | 2015 |
| skills/kntnt/library/references/invocation-envelope.md | 950 | 950 |
| skills/editorial/write/references/quotations.md | 619 | 676 |

| Complete stage / pipeline | Before range | After range |
|---|---:|---:|
| Write | 8717–9369 | 4891–5314 |
| Review | 17522–19003 | 8576–9373 |
| Correction | 13671–15152 | 4694–5491 |
| Pipeline | 32215–34967 | 19445–21345 |

| Final Proofread | Before | After |
|---|---:|---:|
| sv | 6595 | 6658 |
| en_GB | 6038 | 6038 |
| en_US | 5976 | 5976 |

Pipeline means ordinary Write → Redline review → one Proofread, before any correction rounds. Add the complete Correction cost for each actual round. Conditional quotation guidance and invocation-envelope guidance are listed above, not hidden in an ordinary no-quotation/no-context total. A quoted Write adds its quotation guidance. An invocation with contextual instructions adds the envelope. Explicit ABT/PAC adds its base to Write and base/review pair to review and correction; exact deltas are in the resource table. Inference may read installed genre openings only when the genre is unresolved. Help is outside these invocation paths.

The reductions concern instruction volume, not proof of better prose. Operational and language contracts still account for much of the load. The evaluation records distinguish expected paths from observed failures such as the unnecessary genre-opening scan in #350.
