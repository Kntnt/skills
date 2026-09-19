# Swedish colon-variant verification — Redline

- **record** — redline-gpt-2026-09-19-348-colon
- **date** — 2026-09-19
- **ticket** — #348, #338, #329
- **skill** — redline
- **provider family** — gpt
- **model / harness** — gpt-6-astra, high, independently observed in both native sessions; Codex CLI 0.155.1
- **corpus commit** — 6e531f5fe0b610e046ae58787f246cc6239acbcc
- **instruction commit** — 7022c80

The original column-sv final run unnecessarily capitalised a valid integrated question after a colon. Its initial pass assessment is explicitly superseded by L2/R1 fail in the [original record](redline-gpt-2026-09-19-342-column-final.md), and its artifact/trace remain unchanged. The Swedish Mechanics clarification describes the locale boundary rather than mandating one style. The frozen criteria are unchanged.

## Exact replay: column-sv

- **fixture** — Complete Write artifact from final column-sv, byte-identical to the original failed Redline input, including metadata.
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — none
- **output target** — response
- **observed delivery** — [No-change response](../editorial-329/runs/rerun-348-exact/column-sv/redline/response.txt); evaluator's [artifact](../editorial-329/runs/rerun-348-exact/column-sv/redline/artifact.md) equals input bytes.
- **side effects** — 316 native-home entries and project-trust config addition; authentication unchanged; no work/export/scratch effect. [Inventories and classification](../editorial-329/runs/rerun-348-exact/column-sv/redline/side-effects.md). Private root explicitly removed after capture.
- **criteria** —
  - G1 — pass — Personal inquiry and supplied irritation preserved.
  - G2 — pass — Column form, author, observation and reflective ending unchanged.
  - P1 — pass — Reasoning about decisions versus shared understanding remains intact.
  - W1 — pass — Purposeful paragraph variation remains, no quota correction.
  - L1 — pass — Natural Swedish and distinctive voice retained.
  - L2 — pass — Valid lowercase `vad` after the colon preserved after the actual Swedish Mechanics scope was loaded.
  - T1 — pass — column/none/sv metadata used; only selected column and shared pairs, anti-slop and resolved language scopes read; no technique.
  - R1 — pass — Complete artifact byte equality proves claim, qualification and voice preservation.
  - R2 — pass — Full editorial review, no correction needed; installed Proofread read and invoked once with flags only, shared/sv Mechanics actually loaded; no substantive edit afterward.
  - O1 — pass — All writable roots inventoried, no surviving Skill file, input/instructions unchanged.
- **unresolved findings** — none
- **defects filed** — #348 is the antecedent; no new defect.
- **notes** — Source-blind Redline, fresh native session, no expected wording or criterion supplied. A successful replay supports this repair without guaranteeing every future choice.

## Supplementary accidental prompt variant

An evaluator initially selected the metadata-none control prompt `/redline --output=response input.md -- Use ABT.` for the same artifact. The run is preserved [separately](../editorial-329/runs/rerun-348/column-sv/redline/) and is not represented as the exact replay. It also delivered no change, loaded no technique because explicit metadata none outranks the contextual ABT instruction, performed one actual installed Proofread pass and preserved lowercase `vad`. G1/G2/P1/W1/L1/L2/R1 pass by identical complete artifact; T1/R2 pass by actual invocation/resolver/resource trace; O1 pass by full inventories (316 native-home entries/config trust only, no Skill effect). All criteria are the frozen ones. Private root explicitly removed after capture. The accidental run adds selection evidence; it does not replace the prescribed exact replay.
