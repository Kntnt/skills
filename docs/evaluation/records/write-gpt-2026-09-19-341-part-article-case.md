# Affected reruns — translated quotations and customer chronology

- **record** — `write-gpt-2026-09-19-341-part-article-case`
- **date** — `2026-09-19`
- **ticket** — #341 and #344, evaluation #338, part of #329
- **skill** — `write`
- **provider family** — `gpt`
- **model** — `gpt-6-astra`, inherited `high`, verified against native turn contexts
- **harness** — Codex CLI 0.155.1, fresh isolated invocation per stage
- **corpus commit** — `6e531f5fe0b610e046ae58787f246cc6239acbcc`
- **instruction commits** — `1a4f65b3da64fc4f94e82de519ef8b5a18ae56dd` for article-en_GB; `7022c804dfbda4332723bf96b6a9857c24e63b6e` for article-en_US; `93758f485614c3b0e79b1bcce9fb8080de755d08` for case-study-sv. Changes across these revisions are Swedish colon variants and the base clarification that unknown/unclaimed does not mean known absent; each pair uses one immutable revision.
- **method** — Same frozen matrix and source packages, no added prompt hints. New runs preserve the earlier d60 failures. No other provider's records consulted. Chronology is already covered by Source Fidelity: an observed pass on this revision is not proof of a targeted fix or future reliability.

## article-en_GB

- **fixture** — article-en_GB, affected translation rerun
- **instruction commit** — 1a4f65b3da64fc4f94e82de519ef8b5a18ae56dd
- **invocation** — `/write --genre=article --language=en_GB --output=response source.md`
- **contextual instruction** — none
- **output target** — response
- **observed delivery** — Full British article and separate account in `editorial-329/runs/rerun-341/article-en_GB/write/`.
- **side effects** — No work/export/scratch changes; scoped temporary directories removed. Native private-home effects inventoried, authentication unchanged, evaluator root removed.
- **criteria** —
  - F1 — pass — Counts, duration/comfort/placement limits, local threshold and funding uncertainty remain exact; translated Rask quote retains “don’t yet know”.
  - G1 — pass — Focused measurement interpretation serves municipal property managers without promotion.
  - G2 — pass — H1, standalone ingress, deployment lead, explanatory body and earned next step perform distinct jobs; no byline invented.
  - P1 — pass — Sensor locality and operative temperature explain what the trial cannot establish, before recommending further investigation.
  - W1 — pass — Three informative sections and connected paragraphs allow scanning without fragmenting the explanation.
  - L1 — pass — “take a closer look”, “within its limits” and “remains open” provide idiomatic British expression; quotation translation keeps voice/meaning.
  - L2 — pass — British date, draughts, pupils/caretaker, spaced en dash and single quotes consistent.
  - T1 — pass — Article/none/en_GB metadata and actual loading agree; no technique resource.
  - R2 — pass — Updated quotation policy and full bounded writing contract loaded, no review half or peer pass.
  - O1 — pass — Input untouched, no enduring Skill artifact in all inventories.
- **unresolved findings** — none
- **defects filed** — none; no regression observed in the translation-policy affected path.
- **notes** — Independent judgment before Redline; no expected phrasing or defect hint in invocation. Native identity checked in consolidated audit.

## article-en_US

- **fixture** — article-en_US, affected translation rerun
- **instruction commit** — 7022c804dfbda4332723bf96b6a9857c24e63b6e
- **invocation** — `/write --genre=article --language=en_US --output=response source.md`
- **contextual instruction** — none
- **output target** — response
- **observed delivery** — Full article and separate delivery account in `editorial-329/runs/rerun-341/article-en_US/write/`.
- **side effects** — No enduring work/export/scratch changes; native home effects inventoried, authentication unchanged, root removed.
- **criteria** —
  - F1 — pass — Exact 14/120 lesson-unit count, duration unknown, local threshold, placement limitations, unmeasured comfort/effects and undecided funding; translated quote preserves uncertainty.
  - G1 — pass — Useful measurement interpretation for property managers, no promotional claims.
  - G2 — pass — H1, standalone ingress, concrete deployment lead and connected explanation end in a warranted next step.
  - P1 — pass — Differentiates point readings, lesson counts and operative temperature; does not infer cause or student experience.
  - W1 — pass — Three descriptive H2s divide readable explanatory paragraphs without unnecessary lists.
  - L1 — pass — Natural American wording throughout, including “take a closer look” and “Connect the readings to room use”.
  - L2 — pass — American date, drafts/students/custodian, double quotes and unspaced em dashes consistent.
  - T1 — pass — Article/none/en_US metadata agrees with selected resources; no technique loaded.
  - R2 — pass — Full Write bounded contract and composition scope loaded, no review resources or delegated pass.
  - O1 — pass — Source unchanged, no enduring Skill file in complete inventories.
- **unresolved findings** — none
- **defects filed** — none
- **notes** — Judgment before Redline; inherited model/effort confirmed in native turn contexts.

## case-study-sv

- **fixture** — case-study-sv, affected quotation-translation rerun
- **instruction commit** — 93758f485614c3b0e79b1bcce9fb8080de755d08
- **invocation** — `/write --genre=case-study --language=sv --output=response source.md`
- **contextual instruction** — none
- **output target** — response
- **observed delivery** — Full customer case/metadata and separate account in `editorial-329/runs/rerun-341/case-study-sv/write/`.
- **side effects** — No work/export/scratch change; native home effects inventoried, authentication unchanged, root removed.
- **criteria** —
  - F1 — pass — Decision remains September; exact 640/31/two-building/eight-week facts, six staff/two sessions, exclusions, assignment rather than completion, noncausality and qualified appraisal preserved.
  - G1 — pass — Customer-led account for operations managers, supplier in third person with explicit publication context.
  - G2 — pass — Headline/ingress introduce shared visibility and preparation reservation; choices, results and customer's own assessment develop coherently; checklist is a document link.
  - P1 — pass — Contrasting periods retain workload caveat; cost/satisfaction/completion gaps prevent overstating utility. The proposed expansion remains undecided.
  - W1 — pass — Coherent short narrative with readable paragraph jobs; absence of H2s is not a quota failure in this case form.
  - L1 — fail — “innan nästa byggnad kommer i gång” still transfers the English building-as-starting-unit ellipsis. The reader must reconstruct that it is the trial/use in the next building that starts. #341's visible idiom defect remains despite a different verb; this is the contract's mandatory target-language requirement, not an exact-wording comparison.
  - L2 — pass — Swedish dates, speech dashes, compounds and punctuation consistent; the L1 referent issue is not mechanical.
  - T1 — pass — Case-study/none/sv metadata and actual selected/shared resources agree; no technique loaded.
  - R2 — pass — Full Write base, case, web-craft, updated quotation translation policy and sv composition actually read; no review half or peer pass.
  - O1 — pass — Full inventories establish preserved source/resources and no enduring Skill files.
- **unresolved findings** — #341 persists in this Write artifact; unchanged source-blind paired Redline will test the visible problem separately.
- **defects filed** — #341, existing defect; rerun outcome added without replacing earlier failure.
- **notes** — All other prose reads naturally. No strengthened evaluation prompt or expected phrase was supplied. A fluent synonym for the source verb does not by itself establish idiomatic translation of the referent.

## case-study-en_GB — planned earlier-revision rerun not started

Skipped at this revision: before invocation, the final quotation-boundary revision became available. The chronology rerun is performed as part of all three case-study locale pairs in the separate `341-translation-part-article-case` record. The original d60 chronology failure remains unchanged; no missing run is counted as a pass here.
