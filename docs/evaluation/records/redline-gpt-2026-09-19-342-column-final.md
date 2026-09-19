# Column final-resource verification — redline

- **record** — `redline-gpt-2026-09-19-342-column-final`
- **date** — `2026-09-19`
- **ticket** — #342, #338, #329
- **skill** — redline
- **provider family** — gpt
- **model** — gpt-6-astra, high, confirmed in native turn contexts
- **harness** — Codex CLI0.155.1
- **corpus commit** — 6e531f5fe0b610e046ae58787f246cc6239acbcc
- **instruction commit** — f8cac6d5342f72ed91da8c13d96ab092cd5e0ae9

The original [matrix](../corpus/editorial-quality/README.md) and source are unchanged. After #342's first repair still allowed a claim about the author's own thinking, existing column voice/ghostwriting text was clarified to distinguish supplied perspective from invented thoughts or actions. Both earlier failed rounds remain in the338 partsrecord and [342 record](./redline-gpt-2026-09-19-342-column.md). This is a fresh sample per locale at the final resource revision, not deletion or replacement of those outcomes. No claim of guaranteed future reliability follows.

Each invocation is a fresh native session through the unchanged runner. Only Write receives the source; only its full extracted artifact/metadata reaches Redline. No rubric or expected phrasing enters the prompt. Each case is judged before comparisons and without other provider records. Evidence under [rerun-column-final](../editorial-329/runs/rerun-column-final/) covers every writable root, actual loads, all native child sessions, output and cleanup.

## column-en_GB

- **fixture** — column-en_GB
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — none
- **output target** — response
- **observed delivery** — No-change; [artifact](../editorial-329/runs/rerun-column-final/column-en_GB/redline/artifact.md) is byte-identical to input, [response](../editorial-329/runs/rerun-column-final/column-en_GB/redline/response.txt).
- **side effects** — No Skill effect;316 native home entries/config trust update classified in [side-effects](../editorial-329/runs/rerun-column-final/column-en_GB/redline/side-effects.md); root removed.
- **criteria** —
  - G1 — pass — Personal inquiry and gentle form/box humour preserved.
  - G2 — pass — Complete column form retains supplied byline, document observation and uncertain ending.
  - P1 — pass — Decision-only purpose is reconsidered before proposing shared understanding; no unsupported internal leap repaired by invention.
  - W1 — pass — Purposeful variation and continuous paragraphs preserved, without imposed headings or quotas.
  - L1 — pass — Idiomatic English voice retained, including “finding it wanting and proposing more form”.
  - L2 — pass — Actual mechanical pass leaves correct British usage untouched.
  - T1 — pass — Metadata column/none/en_GB and actual items5–7 select column/shared review resources and returned language scopes only; no technique load.
  - R1 — pass — Exact equality preserves all claims, qualifications, reflection and voice; no taste-based edit.
  - R2 — pass — Full scoped review; no correction necessary. Installed Proofread read at item8, invoked exactly once flags-only at item10, mechanics/shared locale at items11–12. No later substantive edit.
  - O1 — pass — Complete inventory and private-directory cleanup prove response-only effects.
- **unresolved findings** — none
- **defects filed** — none
- **notes** — Native gpt-6-astra/high. Source-aware Write assessment is separate; Redline sees no source.

## column-sv

- **fixture** — column-sv
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — none
- **output target** — response
- **observed delivery** — Complete [final artifact](../editorial-329/runs/rerun-column-final/column-sv/redline/artifact.md); the only textual change is capital V beginning the independent question after a colon. Final trailing blank-line presentation also differs; no content removed.
- **side effects** — No Skill effect;315 native home entries/trust config change, [classification](../editorial-329/runs/rerun-column-final/column-sv/redline/side-effects.md); root removed.
- **criteria** —
  - G1 — pass — Reflective author voice, form humour and uncertainty retained.
  - G2 — pass — Title/byline, observation and developed reflection preserved without a formula.
  - P1 — pass — Every reasoning step and qualification retained.
  - W1 — pass — Coherent variable paragraphs remain intact, no imposed headings or quota repairs.
  - L1 — pass — Idiomatic Swedish expression unchanged.
  - L2 — pass — Final Proofread capitalises the independent question after the colon; no other language or locale change. This mechanical classification is also flagged for independent final review.
  - T1 — pass — column/none/sv from metadata, parent items5–7 selected/shared review contract and three sv scopes, no technique resource.
  - R1 — pass — Before/after diff shows only question-initial case; all facts, stance, wording and structure otherwise remain.
  - R2 — pass — Parent reads installed Proofread then spawns one fresh mechanical_pass with fork_turns=none; native child actually reads Proofread, runs its flags-only shim, reads delivery/shared mechanics and resolves sv mechanics once. Complete child text is final; no substantive edit afterwards.
  - O1 — pass — Whole-root inventory and both sessions' transient-directory commands prove no surviving Skill file or input/resource mutation.
- **unresolved findings** — none
- **defects filed** — none
- **notes** — Both native identities gpt-6-astra/high. Native spawn message bytes are encrypted: direct byte verification of the handed-over brief is unavailable. Child tool actions are visible, it reads no input artifact file, and it returns the complete text, supporting the full-text handoff without claiming direct plaintext evidence.

### Independent reassessment of column-sv — #348

The L2/R1 pass above is superseded by **fail** for this preserved run. Independent review identified that the unquoted question can be read as a closely integrated specification after the colon; the supplied lowercase is a valid variant. Proofread therefore made an unnecessary preference edit. No fact, voice or stance changed, but preserving valid mechanical variants is part of the frozen contract. [Defect and primary-source check](../editorial-329/defects/swedish-colon-variant.md). The original artifact and trace remain untouched. A language-resource clarification and exact-input replay are recorded separately; they do not turn this outcome into a pass.

## column-en_US

- **fixture** — column-en_US
- **instruction commit** — 1a4f65b3da64fc4f94e82de519ef8b5a18ae56dd
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — none
- **output target** — response
- **observed delivery** — [No-change response](../editorial-329/runs/rerun-column-final/column-en_US/redline/response.txt); [artifact](../editorial-329/runs/rerun-column-final/column-en_US/redline/artifact.md) equals complete input bytes.
- **side effects** — 318 native home entries and trust config; no work/export/scratch changes, authentication unchanged. [Full classification](../editorial-329/runs/rerun-column-final/column-en_US/redline/side-effects.md). Root already absent at explicit cleanup attempt; actor not verified, inventories/trace captured before disappearance.
- **criteria** —
  - G1 — pass — Personal reflection and form/box humour remain.
  - G2 — pass — Title, supplied author, document observation, reflection and uncertain ending form a column.
  - P1 — pass — Distinction between meeting duration and useful shared understanding remains coherent.
  - W1 — pass — Intentional paragraph variation remains; no formulaic headings added.
  - L1 — pass — Natural American expression retained, with no source translation calques.
  - L2 — pass — Explicit American mechanics scope and shared contract read; correct text left unchanged.
  - T1 — pass — Metadata column/none/en_US; only selected column, base, web-craft pairs, anti-slop and returned language scopes loaded. Directory filename listing is discovery, not unselected content reading.
  - R1 — pass — Full byte equality preserves all source-limited claims, voice and wording.
  - R2 — pass — Full review, no correction needed; installed Proofread read and flags-only shim invoked exactly once, shared/en_US mechanics loaded. No later substantive edit.
  - O1 — pass — Full writable-root inventory supports response-only delivery; absence of final temporary root verified.
- **unresolved findings** — none
- **defects filed** — none
- **notes** — One native session, gpt-6-astra/high confirmed in turn context. No rubric or source supplied to Redline; source-aware assessment is in the separate Write record.

### Cleanup attribution follow-up

The global session-cleanup log subsequently confirmed automatic start-hook deletion of the completed en_US root, rather than an unknown actor. Its exact registered/deleted events are retained in [automatic-cleanup-events.json](../editorial-329/reviews/automatic-cleanup-events.json). This resolves the earlier attribution uncertainty; it does not change the captured run inventories or text assessment.
