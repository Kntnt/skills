# redline — claude — 2026-09-24 — #399

- **record** — `redline-claude-2026-09-24-399`
- **date** — `2026-09-24`
- **ticket** — `#399`
- **skill** — `redline`
- **provider family** — `claude`
- **model** — `claude-opus-5-5` at high deliberation, for every run and every judge; the two correction subagents a run started ran `claude-opus-5-5`, one of them a `kntnt-opus-high` subagent and the other a `general-purpose` subagent inheriting the session's model, at a deliberation this record did not keep
- **harness** — Claude Code 2.1.281
- **corpus commit** — `20133068`

## Run conditions

Ten runs of the control `case-study-clean`: the odd-numbered five against the tree #383 began on, `3167fb68`, and the even-numbered five against the tree #383's record names for its post-change arm, `5af1390d`, run one at a time in numeric order so that the arms alternate. Each install is `git archive` of `skills/editorial/{write,redline,proofread,unslop}` and `skills/kntnt`, extracted flat; the two differ in Redline's `SKILL.md`, `help.md` and `references/correction.md`, the Library's `anti-slop.md` and `base.review.md`, `kntnt/catalog.json`, and three Unslop files Redline does not load. The method was frozen before the first run in [`../editorial-399/plan.md`](../editorial-399/plan.md), which re-uses the per-run staging, judging and counting of [`../editorial-383/plan.md`](../editorial-383/plan.md) with the seat read as `claude-opus-5-5`; the turn files are #383's with only paths substituted, and the control judge brief is #383's byte for byte. The whole evaluation is written up in [`../editorial-399/results.md`](../editorial-399/results.md), and every run's artefacts are under [`../editorial-399/runs/`](../editorial-399/runs/).

**How a run was launched.** A first attempt at run `01`, made as a subagent of the evaluating session, was refused by Redline's Capability check because that subagent could start no subagent of its own; it is void and kept under `runs/void/`. Every counted run is a fresh top-level Claude Code session running the `kntnt-opus-high` agent definition — `claude --print --agent=kntnt-opus-high --model=claude-opus-5-5 --effort=high` — in the run's `work/` directory, with the plan's dispatch message on stdin and nothing else. `runs/sessions.json` records each session's model, Claude Code version and subagents. Every run was judged by two fresh `kntnt-opus-high` judges, blind to the arm, to the model and to this ticket, each sent the run's scratch path, the control brief and the frozen expectation.

**The criteria.** `R1` is each judge's verdict against the frozen expectation. A run misses `C1` where either judge fails `R1`. `A1` and `A2` are derived from the judges' sections by #383's rules on the five post-change runs, and are `skipped` on the five pre-change runs, which #383's plan does not define them on and whose product has no closing summary for `A1` to test. `O1` and `S1` are read from the inventories.

**The result.** One `C1` miss of five in each arm — run `08` post-change and run `09` pre-change — is the second outcome the plan fixed in advance: measured on `claude-opus-5-5`, the miss belongs to the headline contract's authority over a subheading that already conforms, which is #397's and #400's territory, and not to #383's six files. #383's miss on `claude-opus-5` is not re-tested. No ticket is filed.

**Declared limits.** The repository-working-copy half of the inventory is `git status --porcelain --untracked-files=all` in this ticket's worktree and in `/Users/thomas/Projects/skills`, as #383 declared. The judges were handed no measured anatomy figure, as in #383. And the protocol's *A clean control*, added by #404 after this ticket's matrix was fixed, judges a clean control's unchanged text only from a file-target run; this ticket's matrix has ten response-target runs and no others, so the eight `R1` passes on a no-change status rest on the run's own statement that nothing changed. The two misses are rewrites in a delivered text and stand on their own evidence. `results.md` sets out what that means for the reading.

## `case-study-clean-01`

- **fixture** — `case-study-clean`, from the corpus's *Redline controls* table, against the pre-change install, `git archive 3167fb68`
- **invocation** — `/redline --genre=case-study --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the short no-change status, in Swedish, reporting no finding.
- **side effects** — `none` from the Skill: the staged install's digest is identical before and after, `work/input.md` is unchanged, and no file survived in `scratch/`. `response.md` was created at the evaluator's request; the two judgements were written after the after-inventory was taken.
- **criteria** —
  - `R1` — `pass` — both judges: no difference between the input and the text, every preservation clause of the expectation met, every named rejection avoided.
  - `C1` — `pass` — neither judge fails `R1`.
  - `A1` — `skipped` — defined on post-change runs only; the pre-change product has no closing summary to test.
  - `A2` — `skipped` — defined on post-change runs only.
  - `O1` — `pass` — the inventories differ only by the evaluator's `response.md`.
  - `S1` — `pass` — `work/input.md` was the only file in the working directory when the turn was dispatched.
  - `T1` — `skipped` — answerable only from a Harness trace, which this evaluation does not answer from.
  - `R2` — `skipped` — same reason.
  - `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2`, `N1`, `N2`, `C2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — `none`.
- **defects filed** — `none`.
- **notes** — the pass rests on the no-change status; see *Declared limits*. Judgements: [`../editorial-399/runs/case-study-clean-01/judgement-a.md`](../editorial-399/runs/case-study-clean-01/judgement-a.md) and `judgement-b.md` beside it.

## `case-study-clean-02`

- **fixture** — `case-study-clean`, from the corpus's *Redline controls* table, against the post-change install, `git archive 5af1390d`
- **invocation** — `/redline --genre=case-study --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the short no-change status, in Swedish, reporting no finding.
- **side effects** — `none` from the Skill: the staged install's digest is identical before and after, `work/input.md` is unchanged, and no file survived in `scratch/`. `response.md` was created at the evaluator's request; the two judgements were written after the after-inventory was taken.
- **criteria** —
  - `R1` — `pass` — both judges: no difference between the input and the text, every preservation clause of the expectation met, every named rejection avoided.
  - `C1` — `pass` — neither judge fails `R1`.
  - `A1` — `pass` — no difference to count.
  - `A2` — `pass` — both judges find the no-change statement accurate and nothing uncovered.
  - `O1` — `pass` — the inventories differ only by the evaluator's `response.md`.
  - `S1` — `pass` — `work/input.md` was the only file in the working directory when the turn was dispatched.
  - `T1` — `skipped` — answerable only from a Harness trace, which this evaluation does not answer from.
  - `R2` — `skipped` — same reason.
  - `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2`, `N1`, `N2`, `C2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — `none`.
- **defects filed** — `none`.
- **notes** — the pass rests on the no-change status; see *Declared limits*. Judgements: [`../editorial-399/runs/case-study-clean-02/judgement-a.md`](../editorial-399/runs/case-study-clean-02/judgement-a.md) and `judgement-b.md` beside it.

## `case-study-clean-03`

- **fixture** — `case-study-clean`, from the corpus's *Redline controls* table, against the pre-change install, `git archive 3167fb68`
- **invocation** — `/redline --genre=case-study --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the short no-change status, in Swedish, reporting no finding.
- **side effects** — `none` from the Skill: the staged install's digest is identical before and after, `work/input.md` is unchanged, and no file survived in `scratch/`. `response.md` was created at the evaluator's request; the two judgements were written after the after-inventory was taken.
- **criteria** —
  - `R1` — `pass` — both judges: no difference between the input and the text, every preservation clause of the expectation met, every named rejection avoided.
  - `C1` — `pass` — neither judge fails `R1`.
  - `A1` — `skipped` — defined on post-change runs only; the pre-change product has no closing summary to test.
  - `A2` — `skipped` — defined on post-change runs only.
  - `O1` — `pass` — the inventories differ only by the evaluator's `response.md`.
  - `S1` — `pass` — `work/input.md` was the only file in the working directory when the turn was dispatched.
  - `T1` — `skipped` — answerable only from a Harness trace, which this evaluation does not answer from.
  - `R2` — `skipped` — same reason.
  - `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2`, `N1`, `N2`, `C2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — `none`.
- **defects filed** — `none`.
- **notes** — the pass rests on the no-change status; see *Declared limits*. Judgements: [`../editorial-399/runs/case-study-clean-03/judgement-a.md`](../editorial-399/runs/case-study-clean-03/judgement-a.md) and `judgement-b.md` beside it.

## `case-study-clean-04`

- **fixture** — `case-study-clean`, from the corpus's *Redline controls* table, against the post-change install, `git archive 5af1390d`
- **invocation** — `/redline --genre=case-study --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the short no-change status, in Swedish, reporting no finding.
- **side effects** — `none` from the Skill: the staged install's digest is identical before and after, `work/input.md` is unchanged, and no file survived in `scratch/`. `response.md` was created at the evaluator's request; the two judgements were written after the after-inventory was taken.
- **criteria** —
  - `R1` — `pass` — both judges: no difference between the input and the text, every preservation clause of the expectation met, every named rejection avoided.
  - `C1` — `pass` — neither judge fails `R1`.
  - `A1` — `pass` — no difference to count.
  - `A2` — `pass` — both judges find the no-change statement accurate and nothing uncovered.
  - `O1` — `pass` — the inventories differ only by the evaluator's `response.md`.
  - `S1` — `pass` — `work/input.md` was the only file in the working directory when the turn was dispatched.
  - `T1` — `skipped` — answerable only from a Harness trace, which this evaluation does not answer from.
  - `R2` — `skipped` — same reason.
  - `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2`, `N1`, `N2`, `C2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — `none`.
- **defects filed** — `none`.
- **notes** — the pass rests on the no-change status; see *Declared limits*. Judgements: [`../editorial-399/runs/case-study-clean-04/judgement-a.md`](../editorial-399/runs/case-study-clean-04/judgement-a.md) and `judgement-b.md` beside it.

## `case-study-clean-05`

- **fixture** — `case-study-clean`, from the corpus's *Redline controls* table, against the pre-change install, `git archive 3167fb68`
- **invocation** — `/redline --genre=case-study --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the short no-change status, in Swedish, reporting no finding.
- **side effects** — `none` from the Skill in the file inventory: the staged install's digest is identical before and after, `work/input.md` is unchanged, and `response.md` was created at the evaluator's request. The run left one empty directory, `scratch/`, in the run directory — the place the turn gave it for scratch — holding no file; a file inventory does not see it, and it is stated here. The two judgements were written after the after-inventory was taken.
- **criteria** —
  - `R1` — `pass` — both judges: no difference between the input and the text, every preservation clause of the expectation met, every named rejection avoided.
  - `C1` — `pass` — neither judge fails `R1`.
  - `A1` — `skipped` — defined on post-change runs only; the pre-change product has no closing summary to test.
  - `A2` — `skipped` — defined on post-change runs only.
  - `O1` — `pass` — the inventories differ only by the evaluator's `response.md`.
  - `S1` — `pass` — `work/input.md` was the only file in the working directory when the turn was dispatched.
  - `T1` — `skipped` — answerable only from a Harness trace, which this evaluation does not answer from.
  - `R2` — `skipped` — same reason.
  - `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2`, `N1`, `N2`, `C2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — `none`.
- **defects filed** — `none`.
- **notes** — the pass rests on the no-change status; see *Declared limits*. Judgements: [`../editorial-399/runs/case-study-clean-05/judgement-a.md`](../editorial-399/runs/case-study-clean-05/judgement-a.md) and `judgement-b.md` beside it.

## `case-study-clean-06`

- **fixture** — `case-study-clean`, from the corpus's *Redline controls* table, against the post-change install, `git archive 5af1390d`
- **invocation** — `/redline --genre=case-study --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the short no-change status, in Swedish, reporting no finding.
- **side effects** — `none` from the Skill: the staged install's digest is identical before and after, `work/input.md` is unchanged, and no file survived in `scratch/`. `response.md` was created at the evaluator's request; the two judgements were written after the after-inventory was taken.
- **criteria** —
  - `R1` — `pass` — both judges: no difference between the input and the text, every preservation clause of the expectation met, every named rejection avoided.
  - `C1` — `pass` — neither judge fails `R1`.
  - `A1` — `pass` — no difference to count.
  - `A2` — `pass` — both judges find the no-change statement accurate and nothing uncovered.
  - `O1` — `pass` — the inventories differ only by the evaluator's `response.md`.
  - `S1` — `pass` — `work/input.md` was the only file in the working directory when the turn was dispatched.
  - `T1` — `skipped` — answerable only from a Harness trace, which this evaluation does not answer from.
  - `R2` — `skipped` — same reason.
  - `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2`, `N1`, `N2`, `C2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — `none`.
- **defects filed** — `none`.
- **notes** — the pass rests on the no-change status; see *Declared limits*. Judgements: [`../editorial-399/runs/case-study-clean-06/judgement-a.md`](../editorial-399/runs/case-study-clean-06/judgement-a.md) and `judgement-b.md` beside it.

## `case-study-clean-07`

- **fixture** — `case-study-clean`, from the corpus's *Redline controls* table, against the pre-change install, `git archive 3167fb68`
- **invocation** — `/redline --genre=case-study --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the short no-change status, in Swedish, reporting no finding.
- **side effects** — `none` from the Skill: the staged install's digest is identical before and after, `work/input.md` is unchanged, and no file survived in `scratch/`. `response.md` was created at the evaluator's request; the two judgements were written after the after-inventory was taken.
- **criteria** —
  - `R1` — `pass` — both judges: no difference between the input and the text, every preservation clause of the expectation met, every named rejection avoided.
  - `C1` — `pass` — neither judge fails `R1`.
  - `A1` — `skipped` — defined on post-change runs only; the pre-change product has no closing summary to test.
  - `A2` — `skipped` — defined on post-change runs only.
  - `O1` — `pass` — the inventories differ only by the evaluator's `response.md`.
  - `S1` — `pass` — `work/input.md` was the only file in the working directory when the turn was dispatched.
  - `T1` — `skipped` — answerable only from a Harness trace, which this evaluation does not answer from.
  - `R2` — `skipped` — same reason.
  - `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2`, `N1`, `N2`, `C2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — `none`.
- **defects filed** — `none`.
- **notes** — the pass rests on the no-change status; see *Declared limits*. Judgements: [`../editorial-399/runs/case-study-clean-07/judgement-a.md`](../editorial-399/runs/case-study-clean-07/judgement-a.md) and `judgement-b.md` beside it.

## `case-study-clean-08`

- **fixture** — `case-study-clean`, from the corpus's *Redline controls* table, against the post-change install, `git archive 5af1390d`
- **invocation** — `/redline --genre=case-study --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the returned text in one fence, with two findings reported as repaired, a changed claim, and a closing paragraph saying two subheadings were rewritten.
- **side effects** — `none` from the Skill: the staged install's digest is identical before and after, `work/input.md` is unchanged, and no file survived in `scratch/`. `response.md` was created at the evaluator's request; the two judgements were written after the after-inventory was taken.
- **criteria** —
  - `R1` — `fail` — both judges: `## Två perioder med olika arbetsbelastning` (39 characters) became `## Mediantiden sjönk till två arbetsdagar, men belastningen skilde sig` (67) on the finding that it `saknade verb`, a change of taste on a clean text; and `## Kunden vill ge förberedelserna mer tid` became `## Maya Lind vill ge förberedelserna mer tid`, a change of attribution neither judge calls the repair of a visible defect. A substantive edit.
  - `C1` — `fail` — both judges fail `R1`; the run filed findings against a text the expectation says conforms.
  - `A1` — `fail` — both judges class the section 2 subheading rewrite as a change of taste.
  - `A2` — `fail` — judge A finds `alla räknade krav i artikelanatomin är uppfyllda` false, reading the expectation's 36–39-character band as the limit, and the length change unreported; judge B finds the stated reason `ett namn som brödtexten aldrig inför` inaccurate and the length change and the shift of emphasis unreported. The staged anatomy's subheading limit is 70 characters, so that sentence is true against the resource the run measured with, and judge A's reading of it takes the band for the limit, no judge having been handed a measured figure; the verdict is recorded as judged.
  - `O1` — `pass` — the inventories differ only by the evaluator's `response.md`.
  - `S1` — `pass` — `work/input.md` was the only file in the working directory when the turn was dispatched.
  - `T1` — `skipped` — answerable only from a Harness trace, which this evaluation does not answer from.
  - `R2` — `skipped` — same reason.
  - `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2`, `N1`, `N2`, `C2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — `none`; the reply reports both findings repaired.
- **defects filed** — `none` filed on this run. The rewrite is the headline contract's authority over a conforming subheading, #397's territory, and the account giving a taste rewrite as a defect repaired is #400's.
- **notes** — this run's correction subagent was a `kntnt-opus-high` subagent. Judgements: [`../editorial-399/runs/case-study-clean-08/judgement-a.md`](../editorial-399/runs/case-study-clean-08/judgement-a.md) and `judgement-b.md` beside it.

## `case-study-clean-09`

- **fixture** — `case-study-clean`, from the corpus's *Redline controls* table, against the pre-change install, `git archive 3167fb68`
- **invocation** — `/redline --genre=case-study --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the returned text in one fence, one finding repaired, one finding reported unresolved as created by the correction, and the changed claims listed.
- **side effects** — `none` from the Skill: the staged install's digest is identical before and after, `work/input.md` is unchanged, and no file survived in `scratch/`. `response.md` was created at the evaluator's request; the two judgements were written after the after-inventory was taken.
- **criteria** —
  - `R1` — `fail` — both judges: `## Två perioder med olika arbetsbelastning` (39 characters) became `## Mediantiden till tilldelning sjönk från tre arbetsdagar till två` (64) on the finding that it `saknade verb och sa inte vad avsnittet visar`, rewriting a conforming subheading; both read the new heading as stating the result without its caveat. A substantive edit.
  - `C1` — `fail` — both judges fail `R1`; the run filed a finding against a text the expectation says conforms.
  - `A1` — `skipped` — defined on post-change runs only; the pre-change product has no closing summary to test.
  - `A2` — `skipped` — defined on post-change runs only.
  - `O1` — `pass` — the inventories differ only by the evaluator's `response.md`.
  - `S1` — `pass` — `work/input.md` was the only file in the working directory when the turn was dispatched.
  - `T1` — `skipped` — answerable only from a Harness trace, which this evaluation does not answer from.
  - `R2` — `skipped` — same reason.
  - `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2`, `N1`, `N2`, `C2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — one: the new subheading gives the result without its caveat, reported by the run as created by its own correction, the budget being spent.
- **defects filed** — `none` filed on this run. The rewrite is the headline contract's authority over a conforming subheading, #397's territory.
- **notes** — both judges find the account complete and accurate. This run's correction subagent was a `general-purpose` subagent. Judgements: [`../editorial-399/runs/case-study-clean-09/judgement-a.md`](../editorial-399/runs/case-study-clean-09/judgement-a.md) and `judgement-b.md` beside it.

## `case-study-clean-10`

- **fixture** — `case-study-clean`, from the corpus's *Redline controls* table, against the post-change install, `git archive 5af1390d`
- **invocation** — `/redline --genre=case-study --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the short no-change status, in Swedish, reporting no finding.
- **side effects** — `none` from the Skill: the staged install's digest is identical before and after, `work/input.md` is unchanged, and no file survived in `scratch/`. `response.md` was created at the evaluator's request; the two judgements were written after the after-inventory was taken.
- **criteria** —
  - `R1` — `pass` — both judges: no difference between the input and the text, every preservation clause of the expectation met, every named rejection avoided.
  - `C1` — `pass` — neither judge fails `R1`.
  - `A1` — `pass` — no difference to count.
  - `A2` — `pass` — both judges find the no-change statement accurate and nothing uncovered.
  - `O1` — `pass` — the inventories differ only by the evaluator's `response.md`.
  - `S1` — `pass` — `work/input.md` was the only file in the working directory when the turn was dispatched.
  - `T1` — `skipped` — answerable only from a Harness trace, which this evaluation does not answer from.
  - `R2` — `skipped` — same reason.
  - `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2`, `N1`, `N2`, `C2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — `none`.
- **defects filed** — `none`.
- **notes** — the pass rests on the no-change status; see *Declared limits*. Judgements: [`../editorial-399/runs/case-study-clean-10/judgement-a.md`](../editorial-399/runs/case-study-clean-10/judgement-a.md) and `judgement-b.md` beside it.
