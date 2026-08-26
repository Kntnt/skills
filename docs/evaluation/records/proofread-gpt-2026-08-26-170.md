- **record** — `proofread-gpt-2026-08-26-170`
- **date** — `2026-08-26`
- **ticket** — `#170`
- **skill** — `proofread`
- **provider family** — `gpt`
- **model** — `gpt-5.6-sol`
- **harness** — Codex CLI `0.149.1`
- **corpus commit** — `d0ec602`

## Run conditions

These two focused re-runs used separate project-scoped installations copied from the ticket worktree after the scoped resolver stopped returning Language Resource paths. Each installation held only Proofread, the Manager and its Collection Library, and one copy of `flawed-en-US`; the Harness ran from that isolated directory with no global Skill or project instructions in context. The corpus fixture is byte-identical to `d0ec602`. Judging used each run's JSONL Harness trace and the staged filesystem, before opening any earlier provider record.

The loading verdict is intentionally independent of the delivered artifact. For each run, the trace was read command by command: the Skill body, its invocation-envelope section, the delivery contract, the `resolve --scope=mechanics` process and its JSON response, and `editorial/mechanics.md`. A read of any Language Resource file or any composition, review, anti-slop, base, genre, or technique resource would fail the criterion even if the returned prose remained mechanically correct.

## `flawed-en-US` — model trigger by proofreading term

- **fixture** — `flawed-en-US`
- **invocation** — `Proofread the specific text at corpus/flawed-en-US.md.`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — The Harness loaded Proofread and returned a mechanically corrected artifact in the response.
- **side effects** — `none`
- **criteria** —
  - `narrow trigger` — `pass` — A specific Text Artifact and a proofreading term started Proofread without invocation by name.
  - `same path` — `pass` — The Harness trace entered the Skill's numbered steps, ran the dependency check, read the shared delivery contract, and resolved American English through the same command the named invocation specifies.
  - `rule loading` — `pass` — The Harness trace ran `languages.py resolve --scope=mechanics en-US`; its successful JSON carried only the `mechanics` scope and no backing path, then the run opened `editorial/mechanics.md`. No Language Resource file was opened, and no composition, review, or anti-slop guidance, base contract, genre, or technique appears anywhere in the trace.
- **unresolved findings** — `none`
- **defects filed** — `none`
- **notes** — The delivered artifact corrects every planted mechanical error and preserves the explanatory contrastive comma, but that result was not used to infer which resources had loaded.

## `flawed-en-US` — model trigger by mechanical-only request

- **fixture** — `flawed-en-US`
- **invocation** — `Fix only the spelling, grammar, punctuation, agreement, inflection, duplicated-word, and missing-word errors in corpus/flawed-en-US.md.`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — The Harness loaded Proofread, mechanically corrected the artifact, and replaced the isolated source copy.
- **side effects** — `corpus/flawed-en-US.md` replaced inside the isolated run directory
- **criteria** —
  - `narrow trigger` — `pass` — A specific Text Artifact and an unambiguous request limited to mechanical language errors started Proofread without invocation by name.
  - `same path` — `pass` — The Harness trace entered the Skill's numbered steps, ran the dependency check, read the shared delivery contract, and resolved American English through the same command the named invocation specifies.
  - `rule loading` — `pass` — The Harness trace ran `languages.py resolve --scope=mechanics en-US`; its successful JSON carried only the `mechanics` scope and no backing path, then the run opened `editorial/mechanics.md`. No Language Resource file was opened, and no composition, review, or anti-slop guidance, base contract, genre, or technique appears anywhere in the trace.
- **unresolved findings** — `none`
- **defects filed** — `none`
- **notes** — The replacement is the already-filed model-invoked Output Target ambiguity in #168, which is outside #170. The run is evidence for this ticket's loading boundary only; its side effect is recorded rather than treated as a passing delivery verdict.

## Fixtures deliberately skipped

Every corpus fixture except `flawed-en-US` was skipped because #170 was a focused rerun of only the two model-trigger branches.

- `brief-short` — `skipped` — #170 was a focused rerun of only the two model-trigger branches.
- `brief-article-abt` — `skipped` — #170 was a focused rerun of only the two model-trigger branches.
- `brief-report-pac` — `skipped` — #170 was a focused rerun of only the two model-trigger branches.
- `brief-press-release-sv` — `skipped` — #170 was a focused rerun of only the two model-trigger branches.
- `interview-transcript` — `skipped` — #170 was a focused rerun of only the two model-trigger branches.
- `factual-source-long` — `skipped` — #170 was a focused rerun of only the two model-trigger branches.
- `url-source` — `skipped` — #170 was a focused rerun of only the two model-trigger branches.
- `clean-en-GB` — `skipped` — #170 was a focused rerun of only the two model-trigger branches.
- `flawed-sv` — `skipped` — #170 was a focused rerun of only the two model-trigger branches.
- `slop-heavy` — `skipped` — #170 was a focused rerun of only the two model-trigger branches.
- `slop-heavy-sv` — `skipped` — #170 was a focused rerun of only the two model-trigger branches.
- `code-carrying` — `skipped` — #170 was a focused rerun of only the two model-trigger branches.
- `code-carrying-sv` — `skipped` — #170 was a focused rerun of only the two model-trigger branches.
- `resembles-abt` — `skipped` — #170 was a focused rerun of only the two model-trigger branches.
- `mixed-language` — `skipped` — #170 was a focused rerun of only the two model-trigger branches.
- `locale-divergent` — `skipped` — #170 was a focused rerun of only the two model-trigger branches.
- `handoff-present` — `skipped` — #170 was a focused rerun of only the two model-trigger branches.
- `handoff-conflicting` — `skipped` — #170 was a focused rerun of only the two model-trigger branches.
- `handoff-partial` — `skipped` — #170 was a focused rerun of only the two model-trigger branches.
- `handoff-unusable` — `skipped` — #170 was a focused rerun of only the two model-trigger branches.
- `frontmatter-unrelated` — `skipped` — #170 was a focused rerun of only the two model-trigger branches.
- `frontmatter-absent` — `skipped` — #170 was a focused rerun of only the two model-trigger branches.
- `response-default` — `skipped` — #170 was a focused rerun of only the two model-trigger branches.
- `new-file` — `skipped` — #170 was a focused rerun of only the two model-trigger branches.
- `existing-file` — `skipped` — #170 was a focused rerun of only the two model-trigger branches.
- `existing-directory` — `skipped` — #170 was a focused rerun of only the two model-trigger branches.
- `derived-name-collision` — `skipped` — #170 was a focused rerun of only the two model-trigger branches.
- `read-only-source` — `skipped` — #170 was a focused rerun of only the two model-trigger branches.
- `in-place-request` — `skipped` — #170 was a focused rerun of only the two model-trigger branches.
- `output-equals-source` — `skipped` — #170 was a focused rerun of only the two model-trigger branches.
- `output-and-in-place` — `skipped` — #170 was a focused rerun of only the two model-trigger branches.

## Outcome

Both model-invocation branches now converge on the same scoped resolver path. In both traces the complete language-specific rule set in context was the `mechanics` content returned by `resolve --scope=mechanics`, and the only separately loaded editorial resource was the shared mechanics contract. No trace opened `en_US.md` or any other Language Resource file, so composition, review, and anti-slop scopes never entered either run's context.
