# Candidate Redline — column, opinion and web-copy

- **record** — `redline-gpt-2026-09-19-338-part-column-opinion-web`
- **date** — `2026-09-19`
- **ticket** — `#338`, parent `#329`
- **skill** — `redline`
- **provider family** — `gpt`
- **model** — `gpt-6-astra`, reasoning `high`; checked against each native rollout
- **harness** — Codex CLI `0.155.1`
- **corpus commit** — `6e531f5fe0b610e046ae58787f246cc6239acbcc`
- **instruction commit** — `d60c4fcc0228ae37b348c57374f4d8c6ead5a0bd`

## Conditions and scope

This is a running record for the ten declared pairs: column, opinion and web-copy on sv/en_GB/en_US, plus explicitly selected web-copy ABT on sv. Entries are appended after their independent criterion assessment. An absent entry while this record is in progress is pending, never passed. The [frozen matrix](../corpus/editorial-quality/README.md) and [protocol](../protocol.md) govern the assessment. No comparison with a baseline or another provider establishes a criterion.

Each invocation uses a fresh native session and the immutable candidate installation. Write receives only the frozen source package as source.md; Redline receives only the complete extracted Text Artifact, including YAML, as input.md. The evaluator retains the full responses separately and removes only delivery commentary from the paired input. The neutral Harness context, inventories, commands and all native parent/child rollouts remain under [candidate runs](../editorial-329/runs/candidate/). Side-effect assessments distinguish observed Skill changes from enumerated Harness changes and evaluator capture. No other provider was invoked or its records consulted.

## `column-sv`

- **fixture** — `column-sv`
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — Correct short no-change status; [final artifact](../editorial-329/runs/candidate/column-sv/final.md) is byte-identical to the input; [response](../editorial-329/runs/candidate/column-sv/redline/response.txt).
- **side effects** — No Skill files or changed input/resources/scratch; 316 Harness-created home entries and one project-trust update, [classification](../editorial-329/runs/candidate/column-sv/redline/side-effects.md). Registered root removed.
- **criteria** —
  - `G1` — `pass` — Nora's self-irony (“formulärtroget”) and hopeful doubt remain intact.
  - `G2` — `pass` — The title/byline and observation-to-reflection movement survive without invented scene or mandatory subheadings.
  - `P1` — `pass` — The distinction between reaching a decision and discovering a shared question remains clear.
  - `W1` — `pass` — Purposeful returns to the form and varied coherent paragraphs are preserved without numerical findings.
  - `L1` — `pass` — Native Swedish phrasing and deliberate fragments remain rather than being neutralised.
  - `L2` — `pass` — One sv mechanics pass finds no objective correction; original typography and YAML remain unchanged.
  - `T1` — `pass` — column/none/sv resolves from metadata; item_8 loads the exact bounded contract and no technique.
  - `R1` — `pass` — Independent before/after comparison is byte-identical: no facts, perspective, uncertainty or voice lost and no invented-source caveat.
  - `R2` — `pass` — Review scopes in item_7; common/genre/web-craft base and review in items 6/8; no correction needed; exactly one installed Proofread invocation in item_11 has flags only, followed by mechanics in items 12/13 and no substantive edit.
  - `O1` — `pass` — Complete inventories and item_14 cleanup check show no remaining Skill side effects.
- **unresolved findings** — `none`
- **defects filed** — `none`; this trace supplies a successful metadata-bearing candidate check for existing #339.
- **notes** — Native context confirms gpt-6-astra/high. No correction-child session exists because no findings required one. Assessed independently before baseline comparison.

## `column-en_GB`

- **fixture** — `column-en_GB`
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — Short no-change status; final.md is byte-identical to the supplied artifact. [Response](../editorial-329/runs/candidate/column-en_GB/redline/response.txt).
- **side effects** — No remaining Skill changes; 318 native-home creations and one trust-config update, enumerated in filesystem-changes.json. Registered root removed.
- **criteria** —
  - `G1` — `pass` — Personal self-irony, reflective focus and admitted doubt remain.
  - `G2` — `pass` — Title/byline and observation-to-reflection movement remain without a forced scene or section template.
  - `P1` — `pass` — Decision, trust and shared discovery retain their distinctions and logical progression.
  - `W1` — `pass` — Coherent paragraphs and purposeful returns are preserved without numerical findings.
  - `L1` — `pass` — Idiomatic British English remains; no neutralising rewrite.
  - `L2` — `pass` — Mechanics pass finds no objective error; punctuation and metadata remain identical.
  - `T1` — `pass` — column/none/en_GB resolves from metadata; item_8 loads no technique.
  - `R1` — `pass` — Byte-identical before/after preserves every claim and voice; unavailable sources are not requested.
  - `R2` — `pass` — item_7 returns scoped composition/review/anti-slop; item_8 loads both base/genre/web-craft halves; exactly one flags-only Proofread invocation in item_11, mechanics in 12/13, no later substantive edit.
  - `O1` — `pass` — Full-root inventories and cleanup-check item_14 establish no surviving Skill files.
- **unresolved findings** — No Redline findings. The source-aware #342 defect remains in the input and final artifact; it is not detectable from this text alone and is not a Redline failure.
- **defects filed** — #342 applies to the preceding Write result, not this source-blind review.
- **notes** — Native rollout confirms gpt-6-astra/high. Assessed independently before any baseline comparison.

## `opinion-sv`

- **fixture** — `opinion-sv`
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — Short no-change status; [final](../editorial-329/runs/candidate/opinion-sv/final.md) equals the complete supplied artifact.
- **side effects** — No Skill files remain; 320 native-home creations and trust-config update are enumerated. Registered root removed.
- **criteria** —
  - `G1` — `pass` — The sharp policy position and fair recognition of administrative cost survive.
  - `G2` — `pass` — Early thesis, attribution, objection and concrete municipal-board decision remain.
  - `P1` — `pass` — Booking denominator and missing user/time/cost evidence remain distinct.
  - `W1` — `pass` — Argument-bearing headings and readable coherent paragraphs are preserved.
  - `L1` — `pass` — Natural Swedish argumentative voice is retained, without forced neutralisation.
  - `L2` — `pass` — The sv mechanics pass finds no objective correction; original metadata remains.
  - `T1` — `pass` — opinion/none/sv from metadata; selected genre in item_5 and bounded support in item_7, no technique.
  - `R1` — `pass` — Byte-identical comparison preserves all numbers, reservations, argument and action.
  - `R2` — `pass` — item_6 resolves three editorial scopes, item_7 loads review contract, and item_10 is the sole flags-only installed Proofread invocation; mechanics follows in 11/12 and no substantive edit follows.
  - `O1` — `pass` — Complete inventory and item_13 cleanup check show no source or resource mutations and no surviving Skill scratch.
- **unresolved findings** — `none`
- **defects filed** — `none`
- **notes** — Native rollout confirms gpt-6-astra/high. Assessed independently before any baseline comparison.

## `opinion-en_GB`

- **fixture** — `opinion-en_GB`
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — Short no-change status; [final](../editorial-329/runs/candidate/opinion-en_GB/final.md) is byte-identical to the full input.
- **side effects** — No Skill mutation remains; 318 Harness home creations and project-trust update enumerated. Registered root removed.
- **criteria** —
  - `G1` — `pass` — Argument retains its sharp evidence critique and recognition of staff workload.
  - `G2` — `pass` — Thesis, attributed figures, real objection and board decision remain.
  - `P1` — `pass` — Bookings versus people and the purpose of the proposed measurements stay clear.
  - `W1` — `pass` — Informative headings and coherent paragraphs remain without taste-based rewriting.
  - `L1` — `pass` — Idiomatic British English and accountable first-person argument are preserved.
  - `L2` — `pass` — Single en_GB mechanics pass identifies no change; metadata stays byte-identical.
  - `T1` — `pass` — Metadata selects opinion/none/en_GB; item_7 loads bounded support with no technique.
  - `R1` — `pass` — Exact before/after comparison preserves all claims, reservations and voice; no source-verification request.
  - `R2` — `pass` — item_6 resolves three editorial scopes; item_7 loads review contract; sole installed flags-only Proofread invocation is item_10, mechanics follows in 11/12 and no substantive edit follows.
  - `O1` — `pass` — Complete inventory and item_13 cleanup check show no surviving Skill artifacts.
- **unresolved findings** — No Redline finding; source-aware #343 remains in the unchanged input/final, outside this review's knowledge.
- **defects filed** — #343 belongs to the paired Write run; no new Redline defect.
- **notes** — Native rollout confirms gpt-6-astra/high. Assessed independently before any baseline comparison.

## `web-copy-sv`

- **fixture** — `web-copy-sv`
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — Correct no-change status; [final](../editorial-329/runs/candidate/web-copy-sv/final.md) equals the complete input.
- **side effects** — No remaining Skill changes; 316 native-home creations and trust-config update. Root removed.
- **criteria** —
  - `G1` — `pass` — Board task, purchased output and expression-of-interest consequence remain clear.
  - `G2` — `pass` — Useful service-page structure and truthful link remain; no extra sales template or CTA.
  - `P1` — `pass` — Scope, exclusions, prerequisites and next-step consequences stay distinct.
  - `W1` — `pass` — Section entry points and list retain enough context without needless duplication.
  - `L1` — `pass` — Native Swedish task language and purposeful group/individual address are preserved.
  - `L2` — `pass` — The single sv mechanics pass finds no correction; price and typography remain.
  - `T1` — `pass` — web-copy/none/sv from YAML; bounded resources in items 5/7 and no technique.
  - `R1` — `pass` — Byte-identical final preserves all conditions, figures, exclusions, destination and voice.
  - `R2` — `pass` — Three editorial language scopes in item_6; complete review resources in 5/7; sole installed Proofread invocation in item_10, mechanics in 11/12, no post-pass substantive edit.
  - `O1` — `pass` — Complete inventories show no Skill artifact, source/resource mutation or surviving scratch.
- **unresolved findings** — `none`
- **defects filed** — `none`
- **notes** — Native rollout confirms gpt-6-astra/high. Assessed independently before any baseline comparison.

## `web-copy-en_GB`

- **fixture** — `web-copy-en_GB`
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — No-change status; [final](../editorial-329/runs/candidate/web-copy-en_GB/final.md) preserves the absent-form reference unchanged.
- **side effects** — No surviving Skill mutations; 318 native-home creations and trust update. Root removed.
- **criteria** —
  - `G1` — `pass` — Offer and board decision remain useful and accurately bounded.
  - `G2` — `fail` — **Unresolved mandatory finding not reported:** “using the form below” remains although only an external link exists; no finding is reported.
  - `P1` — `pass` — Service scope, preparation and expression-of-interest consequences otherwise remain connected.
  - `W1` — `fail` — **Unresolved mandatory finding not reported:** direct entry to the last section still points to a nonexistent inline form, #345.
  - `L1` — `pass` — Idiomatic British copy is preserved.
  - `L2` — `pass` — One en_GB mechanics pass finds no objective error; metadata and price remain.
  - `T1` — `pass` — web-copy/none/en_GB from YAML; items 5/7 load the selected contract and no technique.
  - `R1` — `fail` — **Unresolved mandatory finding not reported:** despite loading the genre's stranded-reference diagnostic, review returns no-change and no issue for the absent form. Exact comparison shows no claim loss.
  - `R2` — `pass` — Complete review resources in 5/7, three language scopes in 6, sole flags-only installed Proofread invocation in 10 and mechanics in 11/12; no correction was attempted.
  - `O1` — `pass` — Complete inventories show unchanged input/resources/scratch; native effects are separately enumerated.
- **unresolved findings** — The visible absent-form reference remains and Redline reports none; #345.
- **defects filed** — [#345](https://github.com/Kntnt/skills/issues/345).
- **notes** — Native rollout confirms gpt-6-astra/high. This is a missed visible defect, not a source-verification limitation. No correction-child session was spawned.

## `web-copy-en_US`

- **fixture** — `web-copy-en_US`
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — Short no-change status; [final](../editorial-329/runs/candidate/web-copy-en_US/final.md) equals the entire input.
- **side effects** — No surviving Skill changes; 316 native-home creations plus trust config. Root removed.
- **criteria** —
  - `G1` — `pass` — Concrete offer and reader's decision remain clear.
  - `G2` — `pass` — Accurate interest link, non-order consequence, price and prerequisites are preserved without an embedded-form claim.
  - `P1` — `pass` — Benefits, scope, exclusions and next step remain connected.
  - `W1` — `pass` — Specific headings and short coherent paragraphs remain usable from direct entry.
  - `L1` — `pass` — Native US English task language remains intact.
  - `L2` — `pass` — One US mechanics pass makes no change; currency and metadata remain.
  - `T1` — `pass` — web-copy/none/en_US from metadata; selected genre and support in items 6/8, no technique.
  - `R1` — `pass` — Byte-identical final preserves every condition, number, destination and supported benefit.
  - `R2` — `pass` — Three editorial scopes in item_7 and review contract in 6/8; sole flags-only installed Proofread invocation in 11 and mechanics in 12/13; no post-pass edit.
  - `O1` — `pass` — Full inventories and item_14 establish no remaining Skill files or mutations.
- **unresolved findings** — `none`
- **defects filed** — `none`
- **notes** — Native rollout confirms gpt-6-astra/high. Assessed independently before any baseline comparison.

## Original-batch completion and transfer

Seven original pairs on d60c4fc were completed and assessed: column sv/en_GB, opinion sv/en_GB, and web-copy sv/en_GB/en_US. All fourteen registered private run roots were removed after their evidence was captured. Column-en_US and opinion-en_US were not started on this revision; their first runs belong to corrected-candidate coverage, never an assumed original pass. Explicit web-copy-abt likewise waits for the corrected candidate. The column reruns are owned by the parent evaluator; opinion reruns are in the separate -343-opinion records and web-copy reruns plus the original-draft regression in -345-web-copy records. The failed original outputs and judgement corrections above remain preserved.
