# Final quotation revision: five fixed controls

- **record** — `redline-gpt-2026-09-20-341-final-quotation-controls`
- **date** — 2026-09-20 (native UTC)
- **tickets** — #329, #341
- **skill** — redline
- **provider/model** — gpt / gpt-6-astra, high, verified from every native turn context
- **harness** — Codex CLI 0.155.1
- **corpus** — bf14dc2, exact selected input bytes and origins retained per run
- **product** — 3f21d9b1
- **matrix** — `../editorial-329/followup/matrix-quotation-final.md`
- **invocation for every row** — `/redline --output=response input.md`
- **contextual instructions** — none; fresh isolated native runs, no retries

Evidence is under `../editorial-329/followup/runs/final-quotation-controls/`: complete inputs, input provenance, exact prompts/argv/executed helper, raw native sessions, inventories, response, observed reports, independent audit and cleanup receipts. These five rows are the original fixed set. The later declared English preservation replay and subsequent complete pairs remain separate evidence.

The target idiom is repaired in 3/4 defect controls. Whole-control success is 3/5: one repaired result introduces a mechanical error; another misses the idiom defect. The quote-free bypass succeeds. This is a bounded observed result, not a reliability estimate or grounds to close #341.

## Shared applicable assessments

G1/G2 pass in all five: each text retains its genre, actor, customer agency or advocated decision, and all visible qualifications. P1/W1 pass: reasoning, paragraph progression and useful information remain. T1 passes from the resolved metadata; T2 is skipped because no technique applies. F1 and Write-only S1 are not scored for this source-blind review. L1/L2 and R1 vary below.

R2 passes the visible process in all five: the four quoted inputs receive a fresh focused reader; repaired artifacts receive fresh re-reading; exactly one closing installed Proofread invocation occurs per row. Every quotation reader visibly reads the complete current artifact and complete base/genre composition and review guidance plus only the resolved Swedish composition/review language scopes. No unrelated language scope is visibly loaded by those readers. All spawned seats inherit identity and use `fork_turns=none`; no model or effort override appears. The bypass has no focused reader and invokes Proofread in the parent seat.

R2 exact correction/mechanical dispatch is skipped where encrypted native messages conceal passed bytes. File reads establish quotation-reader transport; they do not establish the later mechanical input. In particular, frozen-clean-r1's typo cannot be assigned to an unobserved transport step.

O1 passes for every row: whole-root before/after inventories show unchanged input and authentication and no surviving non-home file, including scratch. Harness private-home bootstrap/cache changes are retained separately. All five isolated roots were removed after capture; the registered batch and child processes ended. Response-target delivery creates no Skill artifact.

## Per-run outcomes

| Case | L1 | L2 | R1 | Whole result | Seconds |
| --- | --- | --- | --- | --- | --- |
| frozen-clean-r1 | pass | **fail** | **fail** | fail | 328.81 |
| frozen-clean-r2 | pass | pass | pass | pass | 325.86 |
| first-case-sv-r1 | **fail** | pass | **fail** | fail | 176.04 |
| first-case-sv-r2 | pass | pass | pass | pass | 429.52 |
| quote-free-bypass | pass | pass | pass | pass | 71.75 |

**frozen-clean-r1.** The reader detects “innan nästa hus börjar”, the correction changes it to “innan försöket börjar i nästa hus”, and the fresh reader approves the complete corrected artifact. That artifact still spells “arbetsbelastning” correctly. The final response instead contains “arbetsbelastningning”. The closing Proofread reports no changes; its exact passed prose is encrypted. The new typo is first directly visible in the parent's final response. Count the target repair, but fail mechanics and preservation. Neither a correct intermediate correction nor a no-change mechanical report certifies the final bytes. No unresolved finding is reported.

**frozen-clean-r2.** Only “innan nästa hus börjar” changes to “innan vi börjar med loggen i nästa hus”. The smallest context-supported repair preserves meaning and voice; the rest of the complete input is identical after outer-newline normalization. Full artifact response, no unresolved findings.

**first-case-sv-r1.** The reader calls “nästa byggnad kommer i gång” intelligible in the trial context and functioning Swedish idiom; the parent gives clean no-change status. The frozen mandatory idiom failure survives. Recoverable intent does not satisfy the existing native-expression criterion. No unrelated change occurs. This is the existing #341 defect, not an invented new rule.

**first-case-sv-r2.** Only “innan nästa byggnad kommer i gång” changes to “innan försöket kommer i gång i nästa byggnad”. Full corrected artifact, fresh no-findings quotation re-read, final mechanics and exact preservation of surrounding text pass. No unresolved findings.

**quote-free-bypass.** British-English opinion, no quoted-person speech. Short no-change response, no focused reader, one final Proofread, entire input preserved. No invented finding or unresolved condition.

Total native run time: 1,331.98 seconds; overlapping execution means this is not elapsed batch wall time. No run error or timeout. Neither failed row was retried or replaced.


## Tracker attribution added after filing

The existing judgments are unchanged. The distinct observed defects now have native #329 child/blocker issues: [#358 — unnecessary changes to functioning quoted wording](https://github.com/Kntnt/skills/issues/358), [#359 — final artifact corruption across the mechanical/delivery boundary](https://github.com/Kntnt/skills/issues/359), and [#360 — translated measurement-construct substitution](https://github.com/Kntnt/skills/issues/360). The fixed-control typo belongs to #359; the unresolved Swedish idiom remains [#341](https://github.com/Kntnt/skills/issues/341). No disputed diagnostic finding is promoted to a definite defect by these links.
