# Candidate Redline genre controls — editorial #338

- **record** — `redline-gpt-2026-09-19-338-controls-genres`
- **date** — `2026-09-19`
- **ticket** — `#338`, parent `#329`
- **skill** — `redline`
- **provider family** — `gpt`
- **model** — `gpt-6-astra`, reasoning `high`, observed native turn contexts
- **harness** — native Codex CLI `0.155.1`
- **corpus commit** — `6e531f5fe0b610e046ae58787f246cc6239acbcc`
- **instruction commit** — `f8cac6d5342f72ed91da8c13d96ab092cd5e0ae9`

## Conditions

The frozen [matrix](../corpus/editorial-quality/README.md) precedes every run. Each control has a fresh native session, immutable private installation and only its supplied artifact as input.md. No rubric, original source, baseline result or other provider record reaches the model. The ten controls are sequential; correction agents use the inherited observed model/effort. The neutral Harness dispatch identifies local SKILL.md and does not replace its workflow. Complete before/after inventories include work, resource copies, scratch and private native state. Side-effect classifications distinguish Skill work from Harness bootstrap/log/database changes. Each control is judged on its own before comparisons.

## `article-clean`

- **fixture** — `article-clean`, sv
- **invocation** — `/redline --genre=article --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — Successful no-change status; [final text](../editorial-329/runs/controls-genres/article-clean/final.md) is byte-identical to the input.
- **side effects** — No surviving Skill effects; all work/resources/input/scratch unchanged. 318 native private-home entries and the project-trust config update are classified Harness effects. Full inventories and cleanup evidence are preserved in the run.
- **criteria** —
  - `G1` — `pass` — Preserves calm explanation of what the readings establish and cannot establish, rather than replacing it with promotion or crisis.
  - `G2` — `pass` — Short informative H1, independent result-bearing ingress, explanatory lead, supported ending and absence of an unavailable byline all survive without manufactured findings.
  - `P1` — `pass` — Sensor placement precedes interpretation; the local threshold, missing duration and missing experience measures constrain the conclusion.
  - `W1` — `pass` — The short heading and useful section entries remain; no numerical length rule provokes a rewrite.
  - `L1` — `pass` — Native Swedish explanatory wording is preserved, including “pekar ut tillfällen att undersöka”.
  - `L2` — `pass` — Swedish quotation marks, date and number forms remain correct after the mechanics pass.
  - `T1` — `pass` — Default none is resolved, and no technique resource is loaded despite the text's question/answer shape.
  - `R1` — `pass` — No change to working facts, voice, quotations, limits or ending; no taste-only correction.
  - `R2` — `pass` — Actual local Skill, base/genre review, web-craft halves, anti-slop and sv composition/review scopes are read. No correction is needed. Installed Proofread is invoked once with separate formal flags and the in-memory artifact; mechanics and sv mechanics resolve successfully. No substantive edit follows.
  - `O1` — `pass` — Full-root inventories establish source preservation and no remaining Skill-created artifacts.
- **unresolved findings** — none
- **defects filed** — none
- **notes** — The initial shell trap command was automatically rejected before execution. The agent adapted to Python try/finally cleanup and completed the invocation; this did not alter the editorial instructions or input.
