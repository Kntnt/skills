# #485: Write private-directory cleanup results

Write now carries Redline’s existing full-path, stay-outside, separate-command recovery and refusal-preservation paragraph. The regression was observed failing before implementation and passing afterwards. The fresh candidate response runs left no unneeded working files; the candidate file run retained the requested draft. All four CONTRIBUTING gates passed.

The existing-directory refusal branch remains **unverified by these fresh runs**. Seven real command refusals occurred before directory creation, and all six parents subsequently used Python to perform the UV operation and clean a different, newly created directory. This behavior is visible in the packets, not certified as successful refusal preservation. There is no fresh reproduction of the earlier Claude working-directory refusal and no causal or frequency claim from these six observations.

## Frozen method and revisions

[Plan and role pathspecs](plan.md) were committed as `2b2dbbcf` before native execution. Pre-change and corpus revision: `5457c89405aece11b325937f9f07407f01974f7c`. Latest implementation-role candidate: **`686e0c41011346df092a5d10565da568ca467b3f`**. The implementation changes only Write’s body, its regression and the generated catalog. Write’s source-check contract, Redline’s shipped guard and Unslop are unchanged. No ADR meets the repository’s decision-record threshold.

All six independent parent sessions and eleven owned checker sessions used `gpt-6.1-sol` at `high`, through native Codex CLI 0.160.0. Every native session has a terminal `task_complete`; all six runners exited 0 without timeout. No void, environmental interruption or revise round occurred. The frozen runner remained unchanged, with ordinary workspace-write permissions and no ignored rules, provider crossing or approval/sandbox bypass flag. No fresh Claude session or refusal probe was launched.

One staging description in the freeze needs precision: “Authentication is copied read-only” describes reading the real authentication source without altering it. The isolated copy actually retained owner-writable mode 0600; it was not chmodded read-only. Each root inventory shows that copy unchanged, and no authentication file is published. The frozen code is the actual method; the freeze has not been rewritten to conceal this wording imprecision.

## Six native observations

All source bytes, modes, inodes and mtimes stayed unchanged. All recorded command working directories are each run’s staged `work` directory. Neither arm contains an executed shell `cd` or Python `chdir` into its owned private directory; consequently the separate-command recovery branch was not exercised either. The W1 result is direct observation in both arms, not evidence that the paragraph caused a behavioral change.

| Packet | Seconds | Remaining Skill-owned paths | Refusals before execution | Measured cleanup/account |
| --- | ---: | --- | ---: | --- |
| [pre-case-question-en_GB](runs/pre-case-question-en_GB/) | 554.30 | none | 1 | O1, H3 pass |
| [pre-case-study-sv](runs/pre-case-study-sv/) | 457.24 | 124 paths beneath the checker-created `scratch/uv-cache/` | 2 | O1, H3 fail |
| [pre-article-en_US-file](runs/pre-article-en_US-file/) | 777.87 | requested `work/draft.md`, 2982 bytes | 1 | O1, H3 pass |
| [post-case-question-en_GB](runs/post-case-question-en_GB/) | 562.44 | none | 1 | O1, H3 pass |
| [post-case-study-sv](runs/post-case-study-sv/) | 795.19 | none | 1 | O1, H3 pass |
| [post-article-en_US-file](runs/post-article-en_US-file/) | 684.17 | requested `work/draft.md`, 3010 bytes | 1 | O1, H3 pass |

S1, I1, W1, T1 and X1 pass in each measured row. H1 records the counts above and is skipped as a verdict because the freeze defines it as a measurement. H2 is skipped for every row: no removal of an existing affected path was held. These are criterion-level results, not an all-criteria-pass claim. [The protocol record](../records/write-gpt-2026-10-02-485.md) supplies all six entries and their delivered findings. [Observations](runs/observations.json) give each full private root, session and call IDs, working directories, unchanged source evidence, retained paths and final delivery.

In pre Swedish, the checker’s direct language-resolution command created its own UV environment/cache under scratch. The 124 retained entries are Skill effects, not exempted Harness cache effects. The parent’s final “Inga filer från körningen finns kvar” omits them, so both O1 and H3 fail. The candidate Swedish checker used private no-cache execution and left no comparable paths. A single pair is insufficient to assign causality or a regression rate.

Both response candidates delivered the draft in their response and removed their comparison drafts/reports. Both file arms delivered a nonempty `draft.md`; captured output bytes match the inventoried file digests. The candidate digest is `57f9d3d15baedc7b5feab5e719347d0ff30b94a59d37c0ea8e879670b7794168`. Parent traces show consumed completed source-check reports and terminal checker verification before comparison scratch removal, with no more than two comparisons. Known findings from the final comparison remain in delivery accounting. Editorial correctness itself is outside this cleanup evaluation.

## Actual refusals and limitation

The native result says `rejected: rm -f style commands are not permitted. Use a safer approach`. The command was rejected at `CreateProcess`, before the initial `mktemp` could run. No directory or draft affected by that proposed removal existed. Each parent then re-expressed its invocation and cleanup through Python `tempfile`/`shutil`; the new directory had a different generated name. The Swedish pre checker also encountered a pre-execution rejection. The exact refused calls are:

| Packet | Native call IDs |
| --- | --- |
| pre-case-question-en_GB | `call_kyV2L7URqCuXyOE5IthfCffB` |
| pre-case-study-sv | `call_rqz4tfw1ZNrXR3aY8dLg8Zlp`, checker `call_n6JcwpuFJ0r1I1zjp6ZgZp5n` |
| pre-article-en_US-file | `call_fBN9mR4bmGAfTSHMTKetm2bB` |
| post-case-question-en_GB | `call_FQgSb9oLe0mnhhB3kdaWGBxZ` |
| post-case-study-sv | `call_wXAULRQfuVhKIXT8laVXVNYP` |
| post-article-en_US-file | `call_RXpbspmlZvmbXRTFLIhPqIiQ` |

The unchanged native sessions and CLI traces contain those results and subsequent calls; `native-index.json` in each packet is a derived navigation aid, not a substitute for the originals or a Claude trace-index schema. Re-expression after this kind of pre-execution refusal does not establish the held-existing-file branch. No fresh run tests whether Write retains and reports existing files after a workspace-directory removal hold. The shipped sentence and test cover that instruction, while the behavioral claim remains limited.

## Separate inspection of previous evidence

[Prior-evidence inspection](runs/prior-evidence.json) preserves pointers and relevant original call data, with no changes to earlier packets. In [#438’s Swedish post run](../editorial-438/runs/post/case-study-sv-r2/trace-index.json), call 12 enters `scratch/tmp/write-NHfb`; call 15’s removal is held because the shell stands there. Call 16’s compound leave/remove/rmdir is held too. Its [filesystem changes](../editorial-438/runs/post/case-study-sv-r2/filesystem-changes.json) retain the directory, draft and report.

[#476’s two independent native probes](../editorial-476/results.md) retain a `cd` between calls, hold `rm` and `rmdir` while the shell stands in the owned directory, then allow removal after leaving in a command of its own. These earlier Claude measurements support the reason for the guard. They are neither a fresh Write reproduction nor a GPT arm, and do not supply an H2 pass here.

## Verification and wave accounting

The new Write test was run before implementation: one Write failure and one unchanged Redline pass. After the paragraph was added, the focused guard and source-check/draft-preservation tests passed (4 passed). `KNTNT_SOURCE=. uv run skills/kntnt/scripts/kntnt.py catalog --write` regenerated only Write’s catalog digest.

[Gate commands, exit codes and durations](runs/checks/gate-results.json) preserve the exact four commands in CONTRIBUTING.md, without changing that guide or narrowing any command:

- Ruff check: pass.
- Ruff format check: pass, 7945 files already formatted.
- Full prescribed mypy command: pass, 89 source files.
- Full parallel pytest command: **2734 passed in 175.65 seconds**.

The compressed wave inventories [before](runs/waves/before.json.gz) and [after](runs/waves/after.json.gz) record this assigned tree’s Git state and scratch metadata; after also enumerates its physical tree. The before-wave tree measurement is Git HEAD/status rather than a physical file listing, so it cannot establish absence of pre-existing ignored tree caches; this is a wave-accounting limitation, not a retrospective inventory. They never inventory another ticket’s checkout. Per-run inventories are complete and uncompressed in each packet. Native home plugin/configuration/session changes are Harness effects; checker-created UV caches are separately attributed above. Builder UV environments, pytest caches, logs, staging roots, inventories and packet copies are builder effects and are removed after preservation, not misrepresented as Skill cleanup.

[Owned-resource receipt](runs/waves/resources.json) records all 14 registered runner/campaign/gate process identities. None of those original processes or recorded groups remains alive. [Cleanup receipt](runs/waves/cleanup.json) records literal owned paths removed after packet preservation and confirms the assigned scratch directory is empty. Requested draft bytes remain deliverables in the committed packets. No shared changelog or record-index file was edited; their exact additions are in `.kntnt-orchestrate/485.md` for the integration wave.

The ticket’s maintainer ruling ships the guard even without fresh reproduction. The measured candidate cleanup/lifecycle criteria have no remaining miss requiring a revise round or separate defect ticket; the unexercised existing-path refusal and recovery branches remain explicit limitations. No broader cleanup, permission, Unslop or composition change was made.
