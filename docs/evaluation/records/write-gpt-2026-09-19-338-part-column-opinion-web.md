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
