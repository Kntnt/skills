# Composition source-check regression — redline, column

- **record** — redline-gpt-2026-09-19-349-source-check-column
- **date** — 2026-09-19
- **ticket** — #349, #342, #338, #329
- **skill** — redline
- **provider family** — gpt
- **model / harness** — gpt-6-astra/high, confirmed in native turn_context; Codex CLI 0.155.1
- **corpus commit** — 6e531f5fe0b610e046ae58787f246cc6239acbcc
- **instruction commit** — d0b2c99

The Write completion condition now operationalises existing Source Fidelity as part of composition. This is affected coverage for a reflective genre, under the unchanged frozen matrix, not evidence that every source-check succeeds. All previous failures remain in their records. Both invocations are fresh sessions; only Write receives the source and only its full artifact reaches Redline. No expected result or rubric is supplied, and no other-provider record informs judgment.

## column-sv

- **fixture** — column-sv
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — none
- **output target** — response
- **observed delivery** — No-change response; evaluator artifact equals complete supplied input bytes, [artifact](../editorial-329/runs/completion-check/column-sv/redline/artifact.md), [response](../editorial-329/runs/completion-check/column-sv/redline/response.txt).
- **side effects** — 316 native-home entries and private trust-config update; authentication unchanged. No work/export/scratch mutation survives. [Classification](../editorial-329/runs/completion-check/column-sv/redline/side-effects.md) and cleanup saved; temporary root removed.
- **criteria** —
  - G1 — pass — The self-ironic form solution and reconsideration give the author a personal reflective voice.
  - G2 — pass — Headline, supplied byline, concrete document opening and developed reflection form a column without a campaign or mandatory headings.
  - P1 — pass — Missing decision field leads to questioning a decision-only purpose, then the broader shared-understanding question, with doubt retained.
  - W1 — pass — Coherent varied paragraphs and a short question give the web reader orientation without enforcing numeric quotas.
  - L1 — pass — Natural Swedish phrasing, including “rutornas fortbestånd”, carries useful humour without a translated metaphor or generic moral.
  - L2 — pass — Swedish punctuation, byline and question-initial case are valid. Write may choose valid capitalisation; Redline preserves that choice.
  - T1 — pass — Recognised column/none/sv metadata; only selected column, shared base/web-craft pairs, anti-slop and correct language scopes load. Filename discovery reads no other genre content.
  - R1 — pass — Byte-identical artifact preserves every claim, qualification, personal perspective and rhetorical return; no taste rewrite.
  - R2 — pass — Full actual scoped review, no correction required, installed Proofread read/invoked once flags-only and shared/sv Mechanics loaded. No substantive edit follows.
  - O1 — pass — Full-root inventories show no surviving Skill effect or mutation of input/instructions.
- **unresolved findings** — none
- **defects filed** — none in this sample; #349 motivates the process regression but concerns the separate opinion samples.
- **notes** — This successful column result does not overturn failures in other genres or earlier columns. Source support and expressive latitude are assessed semantically, not by phrase matching.
