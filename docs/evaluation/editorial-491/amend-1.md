# Amend 1: unresolved prerequisite decision

Attempt `ms-20261002-adc76d` began at `64d5288ea8d91062f091dd71eb93ced0a379c8ee`.
This amend does not complete #491. It adds an audit and fresh project-check
receipts while preserving the prior freeze, completed readings and stopped
evaluation. No Redline run, candidate or product change is claimed.

## The decision that prevents dependent work

The [frozen plan](plan.md), under **Inputs and independent validation**, says:

> A disagreement or real contract conflict stops dependent work for this
> unattended session; preserve the readings, record the decision required,
> and neither silently modify an input nor assume validation passed.

The two completed readers of the complete `supported-appraisal` text agree
that its headline is supported and its opening works. They disagree about
the quotation **“innan nästa hus börjar”**:

- [Reader a](validation/supported-appraisal-a/validation-a.md) treats the
  unstated activity after *börjar* as a reference omission requiring
  clarification from the surrounding log context.
- [Reader b](validation/supported-appraisal-b/validation-b.md) reads it as a
  contextual ellipsis for the log trial or introduction beginning in the
  next house, without a concrete reader loss.

The existing base review requires judging reader loss in context rather
than constructing the strictest reading of one word; the case-study review
requires repairing a genuinely missing referent even inside a quotation.
Those rules distinguish the two classes but do not supply an adjudication
procedure for these completed, conflicting validation readings. The
ticket's settled headline/appraisal ruling does not decide this separate
quotation. The verdict requires completed validation and measurements; it
does not settle the quotation or authorize replacing this frozen contrast.

The decision needed is either a ruling on whether this quotation has an
actual reference omission, or commissioning a new prospective contrast and
validation pass with an explicit relationship to the retained freeze. The
original plan, inputs and adverse reading must remain preserved whichever
route is chosen. Applying the later R1/C1 judge split rule to these
prerequisite validators would change the frozen method. Launching another
reader until agreement appears would also supply an unfrozen method.

The amend instruction **Nobody is watching** requires stopping at a genuine
decision the ticket does not settle. This amend therefore chooses neither
reading, changes no input or expectation, and starts no dependent native
evaluation. This stop remains an incomplete build, not a repair or measured
non-reproduction.

## Audit of every unmet defect class

[The fresh audit](checks/amend-1/evidence-audit.json) inventories the complete
ticket-owned evidence surface and checks the prospective digests against
both committed and working bytes. All eighteen prospective files remain
preserved. The six completed validation packets remain present. The
protocol record contains twenty-eight scheduled but unstarted entries.

| Verdict defect class | Entire affected surface | Outstanding requirement |
| --- | --- | --- |
| Required matrix and prerequisite distinctions need completed native evidence | All three contrasts, fourteen baseline rows and fourteen conditional candidate rows | Resolve the supported contrast prerequisite before the planned runs. The other two contrasts' classifications do not establish Redline behavior. |
| Delivery-based target criteria need authentic artifacts, replies and review traces | All three clean response/file pairs in each arm | No target run exists; unchanged input bytes establish neither delivered preservation nor absence of a false finding. |
| Preservation and genuine-defect controls must exercise the Skill | Both flawed runs and all three contrast response/file pairs in each arm | No scheduled control run exists; fixture classifications establish neither preservation nor actual detection/reporting. |

Acceptance criteria 2, 4 and 5 remain unmet for those reasons. Criterion 3
has no editorial edit to record; its initial-finding/correction/re-review/
delivery ledger remains unmeasured. Criteria 1, 6 and 7's existing safeguards
are preserved. No product change is justified without fresh reproduction,
and no semantic failing test or green result has been observed. A prose
substring assertion would not supply the ticket's required behavioral red
step. No test is added, weakened, skipped or deleted.

## Checks, scope and cleanup

All four exact commands in the unchanged CONTRIBUTING guide are run again
for this amend. [Gate receipts](checks/amend-1/gate-results.json) and their
four full logs record the actual results. Ruff check, formatting and mypy
passed; pytest passed all **2,735 tests** in 120.45 seconds. These checks
establish the project gate only, not the unperformed behavioral evaluation.

No shipped file, corpus, prior evidence, test, gate command or aggregate
file is edited. No catalog regeneration, changelog entry or additional
records-index entry is due. Reserved ADR `0242` remains unused because
there is no non-reproduction measurement or settled corpus-conflict
decision. No other ticket is inspected or awaited. Nothing is pushed or
merged.

[The cleanup receipt](checks/amend-1/cleanup.json) records owned process
groups and the exact amend scratch path removed after retaining the
receipts. The inherited `verify-fresh-491` directory is preserved. No amend
process is deliberately left running.
