# Corrected candidate Write — opinion

- **record** — `write-gpt-2026-09-19-343-opinion`
- **date** — `2026-09-19`
- **ticket** — `#343`, evaluation `#338`, parent `#329`
- **skill** — `write`
- **provider family** — `gpt`
- **model** — `gpt-6-astra`, reasoning `high`; checked against each native rollout
- **harness** — Codex CLI `0.155.1`
- **corpus commit** — `6e531f5fe0b610e046ae58787f246cc6239acbcc`
- **instruction commit** — `2bd2afe34f6ec5d9d6587c33b1c16eeaf241579f`

## Conditions

The [frozen matrix](../corpus/editorial-quality/README.md) and [protocol](../protocol.md) remain unchanged. Each invocation is a fresh native session with the same exact user prompt/material and immutable local Skills; no model/effort override is introduced. Write receives source.md alone; Redline receives the complete extracted artifact including YAML, without source material or Write commentary. Exact context, prompts, responses, traces including child sessions and full inventories are retained under runs/rerun-343; artifacts are evaluator captures. Original failures under runs/candidate and their initial records remain unchanged. Each result is judged independently before comparison, with no other provider's records read.

This record is in progress. Missing planned entries are pending, never passed. Web-copy covers three locales, explicit ABT and the extra Redline-only regression using the original missed British draft; opinion covers three locales. Side effects are established from inventories and executed commands, not the agent's own account.

## Revision boundary

The #345 Redline-only regression and the already-started complete web-copy-sv pair use `2bd2afe34f6ec5d9d6587c33b1c16eeaf241579f`. All remaining pairs (web-copy-en_GB, web-copy-en_US, web-copy-abt, opinion-sv, opinion-en_GB, opinion-en_US) use `1a4f65b3da64fc4f94e82de519ef8b5a18ae56dd`. This changes only base review duplicate-sentence guidance and case-study review idiom guidance; Write-loaded bytes remain unchanged. Each native run retains its exact commit in run metadata.
