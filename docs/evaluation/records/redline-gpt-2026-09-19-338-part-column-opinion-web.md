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
