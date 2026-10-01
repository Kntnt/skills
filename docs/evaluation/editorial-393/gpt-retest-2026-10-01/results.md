# GPT quotation retest results

The bounded retest is complete. On the frozen product, Swedish Redline negatives produced **two agreed repairs, three mandatory-finding failures and one disputed unresolved report**. All three new Swedish Write drafts delivered an idiomatic, source-supported preparation quotation. The positive target phrases survived in seven of eight runs; one response-target English control unnecessarily expanded a working quotation. These are quotation results, not whole-artifact passes.

Thomas's contextual judgement of the original three Swedish phrases remains the [maintainer decision](owner-decision.md). Neither judge was asked to overturn it. No product or historical evidence changed, no candidate ran, and no tracker action was published.

## What ran

Product and corpus: `fb16908712c4d47a36fc6ee9dfb3eb2714a19e65`. Native Codex CLI `0.159.3`, inherited `gpt-6.1-sol/xhigh`, verified in every counted parent, child and judge context. The twenty substantive sessions contain twenty parents and fifty-four fresh children. Five original construction refusals, eight unsent original turns and two void attempts are recorded separately. Two independent judges completed without service errors; twenty-nine native invocations and eighty-six native sessions are retained in total, including non-counted attempts and judges.

The [plan](plan.md), [owner decision](owner-decision.md), full inputs, criteria and initial runner were committed before the first invocation. The historical identifier `case-study` was no longer installed, so committed [Write](construction-repair-plan.md) and [metadata](metadata-construction-plan.md) construction annexes used the installed `casestudy` identifier, leaving every source/input byte unchanged. Five original invocations refused before operation; the eight known-invalid turns were not sent. These are construction outcomes, not language failures. One Write was void at the original 1,800-second boundary and one British control was capacity-void; [the timeout note](timeout-note.md) preserves those attempts and the fixed same-seat replacements. The longest counted Write took 2,109.82 seconds.

Shared `main` independently advanced to `fe2587b70f57c3cfc63903b0be6d9fa4819a4827` during the retest and to clean `5db2ec75a4145eda3449e7646eac5fc6162b85a0` before handoff, after #477/#479/#480. [Initial drift](environment-drift.json) and [the final snapshot](environment-drift-final.json) record this; every native run still exported `fb169087` with `git archive`. These results do not measure either later revision. History used CLI `0.155.1` and `gpt-6-astra/high`; the retest isolates no cause of a difference from that history.

## Target quotation outcomes

| Full negative input | First replay | Second replay |
| --- | --- | --- |
| sv-control | **fail** — original phrase unchanged, obstruction unreported (`r01`) | **pass** — adds “använda loggen”, idiom and support agreed (`r02`) |
| sv-artefact | **fail** — original phrase unchanged, obstruction unreported (`c03`) | **fail** — same mandatory miss (`c04`) |
| ellipsis-sv | **disputed** — unchanged; reported warehouse/quantity referents may concern a different obstruction (`c05`) | **pass** — adds “till det nya systemet”, idiom and support agreed (`c06`) |

The two successful repairs are judged from their complete inputs. No prescribed replacement was supplied. Both judges accept institutional shorthand in the repaired warehouse sentence; the maintainer decision condemns the original defective expression, not every institutional actor in Swedish.

Judge B uses its raw `Q` label for preserved content in some unchanged negatives while separately failing their `L1` and mandatory `R1`. The three unchanged/unreported failures above follow the frozen Q-negative criterion, not that content-only label. Both complete raw judgements remain in [semantic-judgements.json](semantic-judgements.json). For `c05`, A says the report does not identify the transition obstruction; B counts the quotation report while expressly noting its different diagnosis. That split remains disputed. It does not rescore the original Swedish as idiomatic.

| Positive target | Response | Explicit new file |
| --- | --- | --- |
| en-positive | **fail** — “before the next building starts” unnecessarily expanded to “before the trial in the next building starts” (`c07`) | **pass** — working preparation quotation preserved (`c08`) |
| en-us-r1 | **pass** for preparation target (`c09`); a different quotation loses its visible marks in Proofread | **pass** — preparation target preserved (`c10`) |
| metonymy-sv | **pass** — “terminen drog i gång” and “expeditionen märkte skillnaden” preserved (`c11`) | **pass** — both preserved (`c12`) |
| rhythm-en_GB | **pass** — “before the winter” and “the depot stopped ringing round” preserved (`r13-rerun`) | **pass** — both preserved (`r14`) |

Each positive ran once per target; none was repeated to improve its result. Preservation is established from the actually delivered response fence or captured output file. All eight controls delivered text, but successful target quotation preservation coexists with other changes and faults described below.

| Fresh composition | Preparation quotation | Source-blind pair on exact delivered artifact |
| --- | --- | --- |
| `w01-rerun` | **pass** — “innan det är dags för nästa hus” | `p01`: exact unchanged artifact delivered; target preserved |
| `w02` | **pass** — “innan nästa byggnad börjar använda loggen” | `p02`: exact unchanged artifact delivered; target preserved |
| `w03` | **pass** — “innan försöket startar i nästa byggnad” | `p03`: short no-change status, no delivered artifact; text-dependent criteria **skipped** |

All three quotations preserve the source's experience, conditional stance and preparation qualification; both judges agree. Every draft includes the commissioned quotation, so the frozen translation-wave criterion passes. The full [source integrity](source-integrity.json) and [pair inputs](paired-inputs.json) establish unchanged corpus source and byte-exact pairing. Each pair received only the delivered artifact, including its metadata: neither the English source nor the Write reply was supplied.

Both judges label `p03` a missing artifact. That is an observation, not an output-contract failure: the shipped delivery contract allows a short no-change response, and the current evaluation protocol forbids using the supplied input or private closing output as proof of delivered preservation. The reply is Swedish, and no source-blind mandatory finding is established from its input/reply/inventory. `O1` passes; dependent text criteria remain skipped. A reply checker is expressly unnecessary for that short status.

## Whole-artifact results and ownership

[Each protocol record](../../records/redline-gpt-2026-10-01-393.md) and [Write record](../../records/write-gpt-2026-10-01-393.md) gives every criterion and retains splits. The records do not merge the following observations into quotation counts:

- Both judges fail `F1` for `w03`: no author is supplied, yet the draft says “Av användaren” and the reply confirms that inference. This is an unsupported authorship fact. All three drafts were actually delivered; two reported known source ambiguities, which the current Write contract permits. Their proposed wording was outside the checked delivered prose.
- For `w01-rerun`, both judges dispute whether expansion wording implies a decision already made (`F1/P1`). For `w02`, both dispute whether “tilldelning av arbetet” over-specifies the source's assignment measure (`F1`). These are uncertainties, not agreed invented introduction activities. Both preparation translations pass independently.
- Both judges fail `F1/R1` for `c11/c12`: deleting the workgroups' specific design agency leaves only the broader school attribution. Both fail `F1` for `c05`'s broadened headline without “i det nya systemet”; `P1` is split. These are preservation observations related to #377/#383 and immediate round acceptance under #389. No later-round restoration clause was reached: the default budget remained one throughout.
- Both judges fail whole-review `R1` in the four English case-study controls: removing explicit qualifying quotation bridges solely as a pre-echo lacks an established reading obstacle. The preparation targets still pass in three of those four. `c06` has a split over an additional heading change (`R1`).
- In `c09`, both judges fail `L2` and whole-quotation preservation because the final mechanical pass removes quotation marks from the last assessment without blockquote formatting. The private mechanical input/output hashes establish that this happened in Proofread, not in the substantive correction round. This is an impermissible substantive mechanical edit; the preparation target remains untouched.
- `W1` splits where an author was unavailable but correctly left unfilled and reported. The English historical controls also retain unheaded body/ending sections that both judges fail as artifact form. Reported input deficits are kept separate from a run inventing an author or concealing a mandatory finding. No new defect is inferred merely from a properly reported missing author.

The numerical anatomy limits pass for all nineteen delivered artifacts. The semantic packet had complete articles and replies; both judges actually read every exact source/input/artifact/reply field, verified against returned native tool material. Their inventories show no work/scratch writes, delegation or external resource access. No third judge or quality retry ran.

## Trace, transport and limits

[Trace verdicts](trace-verdicts.json), [fresh-agent evidence](fresh-agent-evidence.json) and each run's complete native rollouts distinguish what the trace establishes from what a run said:

- All seventeen Redline sessions retained distinct complete private mechanical input/output paths, frozen input and actually read full output. Delivered text matches the closing output where an artifact exists. `p03` has no publication-byte comparison. `p02` follows the nested Proofread Skill in its parent session; the contract does not require a fresh mechanical child. Every observed correction stayed within the unchanged default budget.
- All three Write deliveries exactly match the last source-checked prose after excluding only leading handoff metadata. Two fresh source comparisons, their reports and recorded dispositions are retained. This establishes transport and the process, not correctness of every source judgement.
- `c07` fails `O1`: the parent removed the harness's pre-existing empty cache/data/tmp/uv-cache directories. The actual removal and inventories establish an incorrect side effect. Other counted sessions honour their targets and leave no unauthorised final work/scratch artifact; sources and staged product remain unchanged. Native private-home cache/plugin/config/session effects are harness state, fully inventoried, not a global installation. This foreign-directory removal is distinct from #476's closed permission-blocked owned-cleanup behaviour.
- Reply-checker scope fails in `c08`, `c09`, `c12` and `p01`. All read the prescribed excerpts, but actually returned 52 preceding words from `base.review`; the latter three also returned the next delivery heading “Refusals”. These are four observed excerpt-boundary violations, not evidence of a broader semantic fault. Exact passages, session IDs and ordinals are in `reply-scope-facts.json`.
- Required core loading is proved in complete actual returned text for the other measured parent/correction sets. Proof gaps remain for `r14`'s parent language scopes, parts of `c06` and `r13-rerun` correction reads, and incoming composition/quotation guidance in encrypted Write source-check dispatches. Their dependent lines are skipped, with the missing material named. A truncated returned batch or absent exact match does not prove a missing read.
- All fifty-four child starts have `fork_turns=none`, distinct IDs and completed lifecycles. Whole filled dispatch messages remain encrypted by the native harness. Freshness and individual actual material reads pass where established; complete-brief R2 stays skipped. External 100-ms file capture can miss a shorter-lived file. No self-report or path glob fills a gap.

There is one additional judging limit outside the target quotation question. Both judges object to `2 140` becoming `2,140`, saying no supplied rule demands commas. The neutral packet did not include the frozen `en_GB` mechanics passage, which explicitly specifies comma as the thousands separator. Their dependent `L2/R1` normalization verdict cannot establish a product defect against that omitted contract. Those lines are **skipped**, with both raw failures preserved. The positive British target phrases pass independently. No packet, criterion or judge result was rewritten, and no extra round or new rule followed this limit.

## Observed cost and verification

| Counted native task/target | Count | Median seconds | Range seconds |
| --- | ---: | ---: | ---: |
| Redline response | 13 | 1,137.96 | 311.97–1,699.20 |
| Redline new file | 4 | 1,155.82 | 941.36–1,301.76 |
| Write response | 3 | 1,780.24 | 1,507.69–2,109.82 |

Construction refusals and the two voids total 2,600.52 additional native seconds. Blind judges took 900.89 and 1,469.58 seconds. Concurrency means sums of invocation durations are not elapsed wall time.

The eleven mandatory Redline case-study editorial resources contain 7,575 words; the three returned Swedish scopes add 1,323, giving 8,898 words per completely verified review/correction core. English case-study cores total 8,195; a completely verified British article core totals 8,109. Every Write parent actually read its five composition resources plus Swedish composition scope, totalling 3,491 core words. Operational Skill/delivery/checker guidance is separate from these core sets. [Cost and loading](cost-and-loading.json) gives each actual named resource, session-level unique volume, mandatory-set comparison and proof gap. Reply excerpts count separately only when their containing complete file is not already credited. Encrypted incoming guidance is unknown volume, never zero-cost evidence. Word counts describe returned material, not model comprehension, billing or a cost-benefit decision.

The evidence branch passed the repository's full ruff, format, specified mypy and pytest checks before late evidence arrived; pytest reported 2,725 passes. Final helper/evidence validation is retained under [validation](validation/results.json). No shipped file changed and no catalog regeneration is needed. Cleanup preserves every deliverable and removes only owned temporary roots and neutral staging after byte-verified evidence copies; [the cleanup ledger](cleanup.json) and [evidence locations](evidence-locations.json) make that handoff inspectable.

## Recommended disposition

Accept the new owner decision and this bounded measurement as completion of #393's human-context/GPT-retest request. It establishes translation success in this wave and remaining Redline quotation misses; it does not justify a product-pass claim, an ADR rewrite or another wording round. Prepare precise `needs-triage` followups for the remaining measured misses and independently owned faults, using [the local tracker comment](tracker-comment.md) and [proposed followups](proposed-followups.md). Thomas/root decides publication and closing; nothing has been posted or closed here.
