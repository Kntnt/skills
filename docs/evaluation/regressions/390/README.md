# Heading-pair evidence — native outcomes and verification limits

For [#390](https://github.com/Kntnt/skills/issues/390). Amend
`ms-20260922-1a1acf` exercises the implementation at `09fb8991` without changing
shipped code, instructions or tests. The [frozen plan](plan.md), [fixture
hashes](fixtures.sha256.json), [tasks](tasks/) and semantic criteria are unchanged.
No #382 baseline was sought. The recorded echo remains the preserved #386 text.

The earlier incomplete attempts are retained in [attempt-37af51.md](attempt-37af51.md)
and [attempt-59e6c1.md](attempt-59e6c1.md), with their original traces and checks.
The amend first observed the missing native outcomes in the
[red completeness check](amend-1a1acf/checks/red-native-completeness.json), then ran
the frozen cases. The [completed packet check](amend-1a1acf/checks/green-native-completeness.json) now passes for all five cases. No unsuccessful attempt was replaced or relabeled as a pass.

## Native evidence

The [amend plan](amend-1a1acf/plan.md) was written before execution. Each case uses
Codex CLI 0.155.1, `gpt-5.6-sol`, `xhigh`, default service tier and a fresh staged
installation. Workspace-write permits network access and confines writes to the
case's private root; the default temporary write roots are excluded. Product
files are byte copies, with SHA-256 inventories. This resolves the previous
execution containment problem without changing editorial guidance.

| Frozen case | Outcome and evidence |
| --- | --- |
| Recorded Swedish echo | [Target repaired](amend-1a1acf/recorded-column/judgement.md); one fresh correction, complete candidate measurement and parent re-review; original uncertainty retained. |
| Paraphrased Swedish echo | [Target repaired, extra finding retained](amend-1a1acf/paraphrased-column/judgement.md); the echo is recognized with only “en” shared. The child and parent also report an overbroad headline/standfirst concern, disclosed below. |
| Legitimate name/topic reuse | [Pass](amend-1a1acf/clean-reuse/judgement.md); every heading pair retained, correction budget unspent. Proofread removes one comma. |
| Paraphrased headline | [Target repaired](amend-1a1acf/paraphrased-headline/judgement.md); the correction agent also retains both clean control section pairs. |
| Write column | [Pass](amend-1a1acf/write-column/judgement.md); pairs judged before comparison, two completed source comparisons, delivered prose identical to the final compared draft. |

Every case directory preserves exact argv and invocation, harness context,
staged instruction digests, full native sessions, event stream, stderr,
before/after work inventories, response, extracted delivered text, complete
before/after anatomy JSON and a trace-backed judgment. Correction cases also
preserve the child's complete response and actual candidate measurements.
`command-index.json` indexes native command records by trace and ordinal;
it makes no semantic judgment. Source-comparison snapshots and ordering evidence
are retained in the Write directory. The JSON's lexical overlap never decides
a case: the judgments read full paired text and its section.

### What these runs do and do not demonstrate

The recorded and low-overlap targets are recognized semantically, and the clean
control's necessary Riverton/Saturday/library reuse is accepted. The headline
correction agent also accepts the control section pairs, so restraint is observed
inside a fresh correction as well as in a parent review. All measurements retain
their structural meaning: echo-bearing inputs conform too.

The paraphrased-column run exposes a limitation. Its child calls the unchanged
headline/standfirst another echo, and the parent carries that finding to delivery.
The standfirst also adds the author, proposal and uncertainty, so the finding is
overbroad in this amend's assessment; the recorded-column run accepts the same
pair. The target repair passes its frozen criterion, but these results do not
establish flawless semantic discrimination or population-wide reliability.

The native CLI encrypts inter-agent task bodies. The original encrypted records
are preserved; this packet does not claim to decode them. Fresh child identity,
commands, resource loading, complete measurement outputs, returned candidates,
and parent re-review are readable in the retained traces. Brief completeness is
not inferred from an unreadable message. The supplied outer invocation material
and staged instruction digests are preserved exactly.

## Required checks

All four exact CONTRIBUTING commands ran to completion. Their argv, environment,
process groups, exit statuses and durations are in
[processes.json](amend-1a1acf/checks/processes.json).

| Check | Result |
| --- | --- |
| Ruff lint | [Pass](amend-1a1acf/checks/ruff.txt) |
| Ruff format | [Pass](amend-1a1acf/checks/format.txt) |
| Published mypy command | [Pass, 71 files](amend-1a1acf/checks/mypy.txt) |
| Published full pytest command | [2,139 passed, three failed](amend-1a1acf/checks/pytest.txt) |

The three failures remain confined to `tests/test_ms_scheduler.py`: the manager's
two-word integration command, redirected-home install and temporary-root
install/status/disable cases. Their temporary paths are inside `/Users/thomas`
because both authorized write roots are inside that real account home.
`integrations._real_account()` deliberately reads the password database and
treats those paths as real-account paths; the tests expect temporary paths outside
it. Their stand-in launchctl reports loaded/healthy instead of the expected
not-loaded/degraded. No real launchctl invocation is implicated by these failures.
The [environment record](amend-1a1acf/checks/environment.json) preserves this
constraint; the earlier unchanged-source reproduction remains in
[the previous attempt](attempt-59e6c1.md).

The verifier's passing gate was not reproduced under this amend's authorized
temporary-storage roots. **The four-check acceptance criterion is not met here.**
Resolving that requires authorization for temporary storage outside the account
home or a separately scoped scheduler-test correction. No test was weakened,
skipped or changed, and no unrelated product fix was guessed. Catalog
[regeneration](amend-1a1acf/checks/catalog.txt) completed and left its bytes unchanged.

## Filesystem and process account

The per-case before/after inventories show unchanged supplied inputs and staged
instructions. The remaining additions are private UV lock files; they are
accounted for rather than presented as clean Skill cleanup. The amend removes its
runtime tree after preserving evidence, including staged installations,
authentication copies, caches, comparison scratch and test temporary files.
The final [cleanup record](amend-1a1acf/checks/cleanup.json) records the result.
All native groups, wrappers and gate processes are waited to completion and
reaped; nothing is intentionally left running.

The reserved regression-index update remains in `.kntnt-orchestrate/390.md`.
Neither the shared index nor CHANGELOG.md is edited by this amend.
