# Redline brief review evaluation — #445

Frozen criteria before native runs. All fixture organisations and events are invented. Runs use the native Codex harness, capture complete RPC traces and inventory the staged working directory and separate scratch area. Provider isolation and the five rejection classes in [the protocol](../protocol.md) apply. No other provider record informs judging.

The first behavioural run (`pre-context`) uses the pre-change review instructions, after the option grammar has been added. It must produce the brief section for an instruction-selected brief; failure establishes the red step for the semantic branch.

## Criteria

- B1: A brief explicitly selected by the option, Contextual Instruction or Conversation Context produces a brief section; the option suppresses a conflicting instruction and the delivery names that suppression. Mere prior presence selects nothing.
- B2: Every answered template question has fulfilled, partly fulfilled or not fulfilled status, text evidence (or explicit absence), and reader loss for shortfalls. Unanswered questions are named; MISSING-only answers are unanswered, SUGGESTED and WEAK answers are reviewed with their qualification. A differently shaped brief is mapped by meaning.
- B3: The fulfilling notice and the reminiscence are distinguished on angle, message and effect. Assessment concerns the text, not actual audience behaviour or the quality of the brief.
- B4: Brief metadata wins over text metadata below explicit options, with each disagreement reported. The Library template is actually read.
- B5: Repairable shortfalls join the existing correction flow and budget; unsupported facts, sources and quotations are left unresolved. The trace and before/after artifacts establish source-bound repair and the closing mechanical pass.
- B6: The brief remains unchanged; output to its path is refused before writes. Only requested artifacts survive workspace cleanup. Harness-owned state is accounted separately.
- N1: No selected brief leaves existing contract review intact, with no brief section or template load. Clean controls run separately for response and file targets; only the delivered file establishes unchanged text.

Exact user turns live in `fixtures/*.json`. Records distinguish failed setup, failed behaviour and completed runs; a skipped case never counts as passed.

## Staged coverage

`option-fulfil`, `context-miss` and `conversation` exercise the three selection levels. `suppression` names different briefs at the first two levels. `markers` uses an unstructured brief with a MISSING title, SUGGESTED voice and WEAK unsupported success-rate requirement. `map-conflict` and `map-explicit` cover both maps and a higher formal language option. `protected-brief` targets the brief itself. `repair` permits the default one correction on the mismatching text with the marker brief and its source. `prior-presence` actually produces a new brief through `/brief` in its first turn, then invokes Redline without pointing at it. Its first turn's requested `prior.md` is accounted separately from Redline's output.

The existing corpus's `web-copy-clean` runs to response and file, and `web-copy-flawed` to file. Their frozen corpus criteria, including source preservation and the clean artifact's exact equality, apply. Other corpus fixtures are recorded as skipped rather than represented by these cases.

## Harness dispatch correction

The first post-change batch sometimes read the installed global Redline before finding the staged copy. `conversation` used the global copy throughout and omitted the brief section. These runs are retained as contaminated setup observations, not sole evidence for the candidate. The runner now names the exact staged Skill paths in its neutral dispatch instruction and excludes global copies. The `-r2` fixtures repeat the same user turns without changing criteria or material. They establish the final brief-review results against the staged install.

## Result and reproducibility

The [evaluation record](../records/redline-gpt-2026-09-28-445.md) contains per-run judgements, skipped corpus cases, dispatch failures and trace limitations. Thirteen candidate runs under exact-path dispatch completed; the baseline and seven earlier mixed-dispatch runs remain alongside them. `checks/artifacts.json` checks source preservation and artifact equality; `checks/gate.json` records all four repository commands.

The controller's writable roots are the work and scratch directories beneath this ticket's private root. Authentication is read from the existing native Codex account; no credential is copied into evidence. Native SQLite state and user-session cleanup registration effects are distinguished from Skill artifacts by the inventories and trace. Supplemental directory audits reconstruct baseline directories from known staging and capture the final directory set. RPC preserves child identities and emitted activity but not every inner child command; the record states that limitation.

To reproduce a fixture, first provide an unused private root in `run.py`, then run `python3 docs/evaluation/redline-445/run.py <fixture>`. Existing evidence directories are refused. The staged files are the working tree's version; their full digests remain in each before-inventory. The user's single-commit delivery rule means evaluation was completed before that commit, rather than claiming a self-referential implementation SHA.
