# Candidate Write — column, opinion and web-copy

- **record** — `write-gpt-2026-09-19-338-part-column-opinion-web`
- **date** — `2026-09-19`
- **ticket** — `#338`, parent `#329`
- **skill** — `write`
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
- **invocation** — `/write --genre=column --language=sv --output=response source.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — Complete column with YAML and separate account; [artifact](../editorial-329/runs/candidate/column-sv/artifact.md), [response](../editorial-329/runs/candidate/column-sv/write/response.txt).
- **side effects** — No remaining Skill files or changed source/resources; 318 Harness-created private-home entries and one trust-config update; [exact classification](../editorial-329/runs/candidate/column-sv/write/side-effects.md). Registered root removed after capture.
- **criteria** —
  - `F1` — `pass` — The opening stays with the supplied form observation; reflection preserves non-decision conversation, trust, hope and doubt without inventing a meeting, memory, statistic or effect.
  - `G1` — `pass` — “nästan generande formulärtroget” carries Nora's supplied self-irony rather than a campaign against meetings.
  - `G2` — `pass` — Title/byline, observation, widening reflection and uncertain close fulfill the personal column brief without a mandatory scene or H2.
  - `P1` — `pass` — The initially attractive decision box is reconsidered through the value of differing understanding, leading to the supported shared-question proposal.
  - `W1` — `pass` — Coherent short paragraphs and purposeful returns to the box guide the reader without fragmentation or redundant subsection labels.
  - `L1` — `pass` — “varför vi behöver just varandras tid” and “formulärtroget” read as native reflective Swedish, not English syntax.
  - `L2` — `pass` — Swedish compounds, clause order and punctuation are consistent; no numerical/date conversion arises.
  - `T1` — `pass` — YAML declares column/none/sv; item_4 reads column/base/web-craft and no technique resource is loaded.
  - `R2` — `pass` — item_5 returns composition-only sv; no review half, mechanics scope or peer editorial pass appears in the trace.
  - `O1` — `pass` — Complete inventories show unchanged work/scratch/source; temporary resolver directories are cleaned and independently checked in item_6.
- **unresolved findings** — None; the delivery notes the source's unknown effect without inventing it.
- **defects filed** — `none`
- **notes** — Native turn_context confirms gpt-6-astra/high. Judged independently before any baseline comparison.

## Assessment correction: `column-sv` F1

The earlier F1 pass above is superseded by **fail — unsupported fact / altered author perspective**, filed as [#342](https://github.com/Kntnt/skills/issues/342). On comparing the English manifestation with the Swedish source, “åtminstone i mitt sätt att tänka kring mötesplanering” is the same personal self-attribution: it relocates the criticised tendency into Nora's own thinking. The source supplies a reflection that calendar time easily gets treated as a result; it does not supply a personal admission that she does so. This is more than a stylistic qualification of her perspective. Other recorded criteria stand. The earlier assessment remains visible to make this correction auditable; neither output nor frozen criterion changed.

## `column-en_GB`

- **fixture** — `column-en_GB`
- **invocation** — `/write --genre=column --language=en_GB --output=response source.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — Complete British English column and account; [artifact](../editorial-329/runs/candidate/column-en_GB/artifact.md), [response](../editorial-329/runs/candidate/column-en_GB/write/response.txt).
- **side effects** — No Skill files remain; 318 Harness home entries plus trust-config change, [classification](../editorial-329/runs/candidate/column-en_GB/write/side-effects.md); root removed.
- **criteria** —
  - `F1` — `fail` — **Unsupported fact / altered author perspective:** “I find myself regarding time in the calendar as a result in itself” invents Nora's own practice from her supplied critical reflection; #342. No invented meeting or statistic was otherwise found.
  - `G1` — `pass` — “a modest comedy ... proposing a larger template” carries the supplied personal self-irony and reflective purpose.
  - `G2` — `pass` — Title/byline, document observation, widening reflection and uncertain close fulfill the genre; no forced scene or campaign.
  - `P1` — `pass` — Decision-making is qualified by trust and discovery before the proposed question, without a false causal claim about results.
  - `W1` — `pass` — Clear short paragraphs allow scanning while recurrent box/question imagery connects the reflection.
  - `L1` — `pass` — “squeeze either into one” and “one another's time” are idiomatic English; no Swedish clause structure is carried across.
  - `L2` — `pass` — Single outer quotation marks and British phrasing are consistent; no factual locale conversion.
  - `T1` — `pass` — column/none/en_GB in YAML; item_4 loads only selected genre/base/web-craft, no technique.
  - `R2` — `pass` — Composition-only resolver in item_5, no review halves or peer editorial pass.
  - `O1` — `pass` — Complete inventories and item_6 scratch inspection establish no surviving Skill artifacts or mutations.
- **unresolved findings** — The unsupported personal admission remains in the delivered draft; the source-blind Redline must not be credited with detecting it.
- **defects filed** — [#342](https://github.com/Kntnt/skills/issues/342), linked as a native sub-issue of #329.
- **notes** — Native identity confirms gpt-6-astra/high. The full unrepaired artifact is passed to Redline. Parent owns the three-locale corrected-column reruns; column-en_US in this original batch is not started and is not counted as passed.

## `opinion-sv`

- **fixture** — `opinion-sv`
- **invocation** — `/write --genre=opinion --language=sv --output=response source.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — Complete attributed debate article with early position and three informative H2s; [artifact](../editorial-329/runs/candidate/opinion-sv/artifact.md).
- **side effects** — No surviving Skill changes; 316 native-home creations plus one project-trust update. Registered root removed.
- **criteria** —
  - `F1` — `pass` — 96/24 bookings, eight weeks/two rooms, seven-room proposal, missing demographic/time/cost evidence and voluntary reasons remain; no motives, legal duty or savings invented.
  - `G1` — `pass` — “Det är för tunt för ett permanent beslut” gives accountable policy criticism while accepting the real administrative objection.
  - `G2` — `pass` — Early thesis, attributed figures, fair objection and explicit municipal-board decision identify author, actor and desired change.
  - `P1` — `pass` — Booking counts are distinguished from residents' abilities; missing evidence motivates measurement before the permanent decision.
  - `W1` — `pass` — Informative H2s expose argument steps; paragraphs retain qualifications beside the claims they constrain.
  - `L1` — `pass` — “Den begränsningen måste också vi ... respektera” is idiomatic, pointed Swedish rather than translation or sales language.
  - `L2` — `pass` — Swedish dates, compounds and punctuation are consistent.
  - `T1` — `pass` — opinion/none/sv in YAML; item_4 loads selected genre/base/web-craft with no technique.
  - `R2` — `pass` — item_5 resolves composition only; quotation policy in item_6, no review/Proofread pass.
  - `O1` — `pass` — Full inventories and cleanup-check item_6 establish no enduring Skill files.
- **unresolved findings** — `none`
- **defects filed** — `none`
- **notes** — Native rollout confirms gpt-6-astra/high. Assessed independently before any baseline comparison.

## `opinion-en_GB`

- **fixture** — `opinion-en_GB`
- **invocation** — `/write --genre=opinion --language=en_GB --output=response source.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — Complete debate article in British English with metadata, attributed author and account; [artifact](../editorial-329/runs/candidate/opinion-en_GB/artifact.md).
- **side effects** — No surviving Skill changes; 318 native-home entries plus project-trust update. Registered root removed.
- **criteria** —
  - `F1` — `fail` — **Unsupported attributed stance:** “I support digital booking” strengthens the source's “Hon motsätter sig inte digital bokning” into an endorsement. Figures, scope and cost uncertainty otherwise remain; #342 evidence comment records the distinction.
  - `G1` — `pass` — Firm criticism of decision evidence and acknowledgement of staff workload maintain debate-article craft.
  - `G2` — `pass` — Early proposal, Sanna attribution, real administrative objection and concrete board decision fulfill the form.
  - `P1` — `pass` — “bookings, not people” prevents population inference; the trial measures the uncertainties used in the argument.
  - `W1` — `pass` — Three informative headings expose the reasoning; qualifications remain beside figures and costs.
  - `L1` — `pass` — “Double administration deserves a measured answer” and “costed” are idiomatic British English, with no Swedish word-order residue.
  - `L2` — `pass` — 8 April 2026, judgement and British conventions are consistent; no invented currency/date conversion.
  - `T1` — `pass` — opinion/none/en_GB in YAML; item_4 loads selected genre/base/web-craft only.
  - `R2` — `pass` — item_5 returns composition alone; item_6 reads quotation policy, no editorial review or mechanical pass.
  - `O1` — `pass` — Whole-root inventory and cleanup checks establish no retained Skill files.
- **unresolved findings** — The strengthened stance remains in the delivered draft and the unmodified Redline input.
- **defects filed** — [#342](https://github.com/Kntnt/skills/issues/342#issuecomment-5744415506), additional supplied-position evidence.
- **notes** — Native rollout confirms gpt-6-astra/high. The evaluative distinction is stance, not preferred wording; source-blind Redline cannot verify it.

## Tracking clarification: opinion stance

The opinion-en_GB failure is tracked separately as [#343](https://github.com/Kntnt/skills/issues/343), a native sub-issue of #329. The earlier comment on #342 remains as history; #342 is restricted to column self-attribution. Root will provide corrected instructions for the opinion reruns. Opinion-en_US under d60c4fc is not started or counted as passed.

## `web-copy-sv`

- **fixture** — `web-copy-sv`
- **invocation** — `/write --genre=web-copy --language=sv --output=response source.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — Complete service page, metadata and separate account; [artifact](../editorial-329/runs/candidate/web-copy-sv/artifact.md).
- **side effects** — No surviving Skill changes; 320 native-home creations and trust-config update enumerated; root removed.
- **criteria** —
  - `F1` — `pass` — 45-minute/two-representative meeting, written summary/two possible simplifications, price/VAT, one-room scope, exclusions, no guarantee and three-day email response all stay supported; payment/delivery terms are not invented.
  - `G1` — `pass` — The page answers board relevance, purchased deliverables and how an expression of interest works.
  - `G2` — `pass` — Information structure follows task, with clear price/conditions and an accurate interest link rather than a booking or sales template.
  - `P1` — `pass` — Deliverables lead to prerequisites and then action consequences; exclusions distinguish adjacent services.
  - `W1` — `pass` — Each H2 names its content and establishes local context; the list helps scan the summary contents.
  - `L1` — `pass` — Natural Swedish task language; group Ni addresses the board and du addresses the individual filling the form.
  - `L2` — `pass` — 4 800 kr, Swedish compounds and spaced en dash follow Swedish form without currency conversion.
  - `T1` — `pass` — web-copy/none/sv in YAML; item_4 loads selected genre/base/web-craft and no technique.
  - `R2` — `pass` — item_5 resolves composition only; no review half, mechanics or peer Skill.
  - `O1` — `pass` — Full inventories and item_6 check prove unchanged source/resources/scratch and no retained Skill files.
- **unresolved findings** — Account correctly names absent payment terms and summary-delivery time.
- **defects filed** — `none`
- **notes** — Native rollout confirms gpt-6-astra/high. Assessed independently before any baseline comparison.

## `web-copy-en_GB`

- **fixture** — `web-copy-en_GB`
- **invocation** — `/write --genre=web-copy --language=en_GB --output=response source.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — Complete British service page and account; [artifact](../editorial-329/runs/candidate/web-copy-en_GB/artifact.md).
- **side effects** — No remaining Skill changes; 318 native-home creations and trust-config update. Root removed.
- **criteria** —
  - `F1` — `pass` — Price SEK 4,800/VAT, scope, 45 minutes/two representatives, deliverables, exclusions, no guarantee and response time remain; missing payment/delivery terms stay unspecified.
  - `G1` — `pass` — The offer serves board understanding and the decision whether to express interest, without inflated benefits.
  - `G2` — `fail` — **Qualitative UX concern:** “using the form below” describes a form on this page, but only a link to a separate form is supplied. This is a stranded interface reference; the link otherwise names the truthful interest action.
  - `P1` — `pass` — Offer, prerequisites, exclusions and non-order consequence are logically separated.
  - `W1` — `fail` — **Qualitative UX concern:** a reader entering the final section is directed to an absent inline form; “the linked form” would match the actual surface. Other headings/paragraphs support scanning.
  - `L1` — `pass` — Clear idiomatic British service language; domain-specific tenant-owner association preserves the Swedish service context.
  - `L2` — `pass` — SEK and destination retained, English thousands separator and British forms used without conversion.
  - `T1` — `pass` — web-copy/none/en_GB in YAML; item_4 loads only selected genre/base/web-craft.
  - `R2` — `pass` — item_5 resolves composition only; no review halves or peer editorial pass.
  - `O1` — `pass` — Complete inventories and item_6 show no remaining Skill output or scratch.
- **unresolved findings** — The absent-form reference remains in the unrepaired artifact passed to Redline; it is a qualitative usability defect, not one of the protocol's five unconditional source/mechanics/side-effect rejections.
- **defects filed** — Pending triage of the concrete interface-reference concern; no new rule inferred from one stylistic sample.
- **notes** — Native rollout confirms gpt-6-astra/high. Assessed before Redline, independently of baseline. The form/link distinction concerns observable navigation, not preferred phrasing.

## Defect registration: web-copy-en_GB

The absent-form interface reference is filed as [#345](https://github.com/Kntnt/skills/issues/345), a native sub-issue of #329. Its paired Redline outcome is recorded separately; the initial Write judgement stands even if the pipeline repairs it.

## `web-copy-en_US`

- **fixture** — `web-copy-en_US`
- **invocation** — `/write --genre=web-copy --language=en_US --output=response source.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — Complete American English service page with metadata and account; [artifact](../editorial-329/runs/candidate/web-copy-en_US/artifact.md).
- **side effects** — No remaining Skill changes; 316 native-home creations and trust-config update. Root removed.
- **criteria** —
  - `F1` — `pass` — Scope, meeting, summary, two possible simplifications, price/VAT, exclusions and no-guarantee conditions remain; no payment or delivery terms invented.
  - `G1` — `pass` — Board relevance, deliverables and interest consequences are concretely explained.
  - `G2` — `pass` — Price, preparation and next step are accessible; interest form is described without claiming it is embedded, with a truthful supplied link.
  - `P1` — `pass` — Defined service and exclusions lead clearly to the no-order/no-payment next step.
  - `W1` — `pass` — Four specific headings create usable entry points and list the actual summary contents.
  - `L1` — `pass` — Natural American task language, including “take stock” and “three business days”, without Swedish syntax.
  - `L2` — `pass` — 4,800 SEK and American list punctuation preserve amount/currency and destination.
  - `T1` — `pass` — web-copy/none/en_US in YAML; item_4 loads selected base/genre/web-craft only.
  - `R2` — `pass` — item_5 resolves composition only, no review half or peer editorial pass.
  - `O1` — `pass` — Complete inventories and item_6 inspection show no surviving Skill changes.
- **unresolved findings** — Account accurately notes unspecified payment terms and summary delivery timeframe.
- **defects filed** — `none`
- **notes** — Native rollout confirms gpt-6-astra/high. Assessed independently before any baseline comparison.

## Original-batch completion and transfer

Seven original pairs on d60c4fc were completed and assessed: column sv/en_GB, opinion sv/en_GB, and web-copy sv/en_GB/en_US. All fourteen registered private run roots were removed after their evidence was captured. Column-en_US and opinion-en_US were not started on this revision; their first runs belong to corrected-candidate coverage, never an assumed original pass. Explicit web-copy-abt likewise waits for the corrected candidate. The column reruns are owned by the parent evaluator; opinion reruns are in the separate -343-opinion records and web-copy reruns plus the original-draft regression in -345-web-copy records. The failed original outputs and judgement corrections above remain preserved.

## Historical reassessment — opinion source knowledge, #349

The original candidate opinion-sv F1 pass is superseded by **fail** after consistent comparison of the already-frozen source. Its `runs/candidate/opinion-sv/artifact.md` says “Vi har varken kostnadsberäknat eller finansierat försöket.” The source only says the association makes no claim to have done those things. The earlier judgement preserved practical cost uncertainty but overlooked this stronger assertion of unperformed work. The original assessment and artifact remain visible; neither the fixture nor the criterion changed.

The original opinion-en_GB F1 already failed for #343 (“I support digital booking”). It also independently fails #349: “Öppna beslut has neither costed nor secured funding for the trial.” The source establishes neither absent costing nor an absence of secured funding. This added finding does not replace the original stance defect.

The same absence claim has now also been identified in the baseline opinion-sv sample by the root reviewer. This is therefore a pre-existing quality failure; these observations do not establish that #329 introduced it. Source-blind Redline assessments remain unchanged: the artifacts themselves do not disclose this external mismatch.
