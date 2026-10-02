# Amend 1: checker-draft recovery stops short of criterion 5

Attempt `ms-20261002-c948b3`, against starting head
`f0dd508f9bee56c8fee3a75fd2ff4643cffaf5f2`. This is an additional read-only
evidence audit, not another native arm, a new judgement, or a product repair.
Acceptance criterion 5 remains **unestablished**. The other original results
and the conditional non-reproduction decision remain historical evidence.

## What was inspected

[recovery-audit.json](recovery-audit.json) identifies and hashes every one of
the 1,681 files in the existing #488 evaluation surface. The search includes
108 native rollouts: all 105 completed parent, correction, mechanical, checker
and judge sessions, and the three separately preserved interrupted starts.
It also includes both event-stream representations, all 267 top-level transient
file captures, the judges' captures, inventories, operator source snapshots and
operator receipts. No other ticket's worktree or evaluation was opened.

For each of the 18 completed runs, the audit links the parent checker spawn's
call ID to the child session through the native start event. It records the
parent and child trace hashes, ordinals and timestamps, checker return hash,
terminal reply hash, and every top-level capture's hash against its manifest.
Every delegated checker message is encrypted. In each child, the inherited
`agent_message` contains the same encrypted payload as its parent's spawn
argument; its plaintext block holds only the task envelope. The environment
user message is not a replacement for that checker instruction.

## Additional recoverable evidence

Searching only spawn arguments and child user messages misses retained drafts
elsewhere. Ten parents preserved complete draft reports in their tool inputs or
outputs before checking. The receipt retains each report, its exact source
ordinal, the checker return, the terminal report, and a literal diff:

| Run | Parent ordinal | Draft source |
| --- | ---: | --- |
| post-article-clean-response | 171 | Stored string literal |
| post-article-unnamed-1 | 236 | Printed filled checker brief |
| post-article-unnamed-2 | 199 | Stored string literal |
| post-article-unnamed-3 | 196 | Stored string literal |
| post-column-flawed-file | 179 | Stored string literal |
| post-opinion-flawed-3 | 244 | Stored string literal |
| pre-article-unnamed-1 | 183 | Stored string literal |
| pre-column-flawed-file | 192 | Stored string literal |
| pre-opinion-flawed-1 | 215 | Stored template literal |
| pre-opinion-flawed-2 | 218 | Stored template literal |

The reports in `post-article-unnamed-1`, `post-article-unnamed-2`,
`post-article-unnamed-3` and `post-column-flawed-file` are identical to their
terminal reports; each checker returned two empty lists. The other six diffs
preserve the actual revisions beside the actual checker returns, including
inline-code formatting changes in two opinion reports and an added cleanup
rejection reason in `pre-column-flawed-file`. These are observations, not a new
blind judgement or an inferred proof that an encrypted checker prompt contained
the same complete report. Nothing reconstructs a draft from the delivered
report or expands a checker's partial quotations into an invented draft.

The complete filled brief in `post-article-unnamed-1` was printed by parent tool
output ordinal 236, after input/output inspection and cleanup, before checker
spawn ordinal 238. The earlier tool input at ordinal 233 prints the filled
template from stored values. This provides more evidence than the original
campaign summary described. The underlying trace bytes were already present
at the starting head; this amend adds their reading, not a recreated native
event.

## Remaining blocker

Eight runs have no recoverable complete plaintext draft in the owned evidence:

- `post-article-clean-file`
- `post-opinion-flawed-1`
- `post-opinion-flawed-2`
- `pre-article-clean-file`
- `pre-article-clean-response`
- `pre-article-unnamed-2`
- `pre-article-unnamed-3`
- `pre-opinion-flawed-3`

Even for the ten recovered draft reports, the encrypted dispatched instruction
cannot independently be compared byte for byte with the plaintext snapshot.
The available native trace provides no decoder or recoverable key. The search
does not claim to recover undocumented encodings or encrypted content. It
cannot establish every unfaulted checked statement across all 18 runs. A
completed checker and the text of its two lists do not fill the missing inputs.

[recovery-probe.txt](recovery-probe.txt) is the executable diagnostic source
snapshot. From the assigned worktree:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 docs/evaluation/editorial-488/amend-1/recovery-probe.txt
```

It writes the separately named recovery audit, prints the affected runs, and
exits 1 when a complete plaintext draft is unavailable. Its observed failure
is preserved in [recovery-probe.log](recovery-probe.log). The initial probe's
failure and receipt are retained separately: it tested direct inherited-input
recovery and its wider scan exposed the printed brief, leading to inspection of
stored draft literals. There is no green repair result to claim, and this
diagnostic is not substituted for any of the four project checks.

The unresolved next step is access to recoverable original checker inputs, or
a settled prospective native capture method that supplies complete checker
inputs without changing the product, the one-shot check, or the checked reply.
This amend does not guess that a newly instrumented campaign can replace the
completed frozen campaign's missing proof. The frozen plan expressly reports
missing provider capability or a genuine requirement decision as blocked. No
native run is resumed to ask a model to reproduce an earlier draft from memory.

## Scope and verification

No Skill, shared contract, production Harness, test, gate, frozen plan, input,
judge brief, original native packet or ADR changes. No new editorial campaign
starts, and no unrelated editorial finding is repaired. No catalog regeneration
is due. The shared changelog and record index are untouched.

All four unchanged CONTRIBUTING.md commands passed: Ruff lint, Ruff formatting,
mypy (89 source files), and pytest (2,733 tests in 130.95 seconds). Their full
logs and exact command/environment receipt are retained in
[gate-receipt.json](gate-receipt.json). The verification supervisor and all four
command groups were registered and awaited; cleanup is recorded separately.
The green gate cannot turn missing native evidence into a pass of criterion 5.
