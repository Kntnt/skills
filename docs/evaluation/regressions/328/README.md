# Redline caller-owned invocation recovery — issue #328

This focused native regression is separate from the fixture-corpus evaluations governed by [`../../protocol.md`](../../protocol.md). It exercises one diagnosed caller construction error at Redline's current private-file Proofread handoff.

- **date** — `2026-09-20`
- **product revision** — `e5d0ff630678830470632c5ed8afc3e708423811`
- **model** — `gpt-6-astra`, reasoning `high`, observed in both native turn contexts
- **harness** — native Codex CLI `0.155.1`, using the editorial #329 runner
- **duration** — 300.6 seconds; exit 0; no timeout
- **fixture** — [`input.md`](input.md)
- **invocation envelope** — [`prompt.txt`](prompt.txt), comprising the Formal Invocation and Contextual Instruction separated by `--`
- **artifact before Proofread** — [`pre-proofread.md`](pre-proofread.md), SHA-256 `0fe1f2d2f76ee583fa1fe5b5964dd2ddf10e1d7c144ee102e2078c3effad99a8`
- **delivered artifact** — [`final.md`](final.md)
- **event evidence** — [`trace-excerpt.jsonl`](trace-excerpt.jsonl)
- **filesystem evidence** — [`filesystem-summary.json`](filesystem-summary.json)

## Setup

The runner checked out the exact product revision in an isolated worktree, copied the fixture to `work/input.md`, and invoked the prompt verbatim. The valid outer invocation was `/redline --in-place --max=1 input.md`. The instruction asked Redline to complete its review and permitted correction round, then deliberately use `--lang=en_GB` once instead of `--language=en_GB` when invoking Proofread with the already required immutable private input and distinct private output.

The fixture carries `article` / `abt` / `en_GB` metadata, editorial defects, the mechanical agreement error `Teams has`, apostrophes, the double-quoted label `"Focus first"`, newlines, and a `--retain-this-source-marker` line. The current Redline handoff transports only file paths through the shim.

## Observed sequence

1. Redline accepted the outer request, settled the original file as the in-place destination, completed review, ran one correction child, re-reviewed its result, and retained the corrected artifact.
2. It opened Proofread once and froze the complete corrected artifact in a read-only private input. The trace printed the input's SHA-256 before either nested invocation.
3. Its first nested Formal Invocation used `--lang=en_GB` with the private input and output paths. The engine exited 2 with `'/proofread' takes no '--lang'`, its synopsis, and its help route. Proofread had not begun.
4. The parent explicitly diagnosed its own flag-name error and said it would retain both paths and continue without repeating review or correction.
5. The corrected invocation changed only the flag name to `--language=en_GB`. The engine accepted it with the same language, input path, output path, null contextual instruction, and satisfied dependencies.
6. Exactly one mechanics resolution and one actual Proofread pass followed. The pass changed only `Teams has` to `Teams have` between the frozen artifact and the complete mechanical result.
7. Redline verified the immutable input against the same SHA-256, read the complete result, wrote it over the original `work/input.md`, removed the private input, output, and directory, and reported the remaining findings and removed claims.

There are two native sessions in total: the Redline parent and its one correction child. The excerpt preserves that session inventory, the review and correction events before the failed boundary, the boundary itself, and the final account. The complete run's before/after inventory reduced Skill-visible filesystem changes to `work/input.md`; no Skill-created path remained.

## Result

The strict refusal, caller diagnosis, corrected submission, one actual mechanical pass, and successful in-place delivery all passed. Review and the single permitted correction round occur before the refusal and do not recur after it. The refusal therefore consumes neither another Correction Budget round nor the actual Proofread pass. The same private paths occur in both invocations, the pre-Proofread artifact's hash is verified after the pass, and frontmatter, apostrophes, quoted content, newlines, and the dash-prefixed marker survive the handoff.

The response reported three unresolved editorial findings and four claims removed by the correction. It did not present the refusal as the outer result.

## Limits

The contextual instruction deliberately injects the caller error, so this run demonstrates the required recovery sequence rather than the frequency of spontaneous construction mistakes. It is one GPT-family run and is not a general model guarantee. The reused runner labels its temporary root for #338; the exact product revision and native turn contexts identify what ran. Two shell cleanup attempts elsewhere in the run were refused by tool policy before execution and replaced with safe cleanup calls; neither is at the nested invocation boundary or alters its result.
