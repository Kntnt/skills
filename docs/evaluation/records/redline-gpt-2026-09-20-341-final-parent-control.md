# Exact original Swedish idiom control after quotation rollback

- **record** — `redline-gpt-2026-09-20-341-final-parent-control`
- **date** — 2026-09-20 (native UTC)
- **ticket** — [#341](https://github.com/Kntnt/skills/issues/341), #329
- **skill** — redline
- **provider/model** — gpt / gpt-6-astra, high, verified native turn context
- **harness** — Codex CLI 0.155.1
- **corpus commit** — bf14dc2; exact prior `second-candidate/idiom-frozen-clean/redline/supplied-input.md`, SHA-256 `8821f2ea42f723956ccb5d1127b212227d04c7035b3944e4a81be990dda82e66`
- **product** — 5ecadb76
- **matrix** — `../editorial-329/followup/matrix-final-delivery.md`, mandatory-acceptance amendment declared before launch

## original case-study-clean

- **fixture** — exact original frozen Swedish `case-study-clean` artifact
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — none; one fresh isolated invocation, no retry
- **output target** — response
- **observed delivery** — short clean no-change status; the entire original artifact remains unchanged, including “innan nästa hus börjar”
- **side effects** — private mechanical input and distinct result created and removed; no surviving non-home Skill artifact or authentication/source change; complete root removed after capture
- **criteria** —
  - G1/G2, P1/W1 — pass: customer agency, experience, quantitative limitations and useful progression preserved.
  - T1 — pass: case-study/sv inferred under allowed resource scopes; none technique. T2 skipped.
  - L1 — **fail**: the frozen mandatory idiom obstruction survives inside quoted speech; recoverable trial meaning does not make “innan nästa hus börjar” idiomatic target-language reference.
  - L2 — pass: no mechanical error is introduced.
  - R1 — **fail**: substantive review misses the concrete required defect and calls the artifact clean. This is the existing #341 rejection, not a changed criterion or a new issue.
  - R2 — pass for visible process: parent-only review, exactly one installed Proofread shim invocation, full private input read, separate complete output written/read, unchanged input verified. The actual result is byte-identical to input and preserved as `mechanical-result.md`.
  - O1 — pass: correct response destination, no extra artifact, private cleanup before return, source/authentication unchanged and isolated root removed.
  - F1 and Write-only S1 — skipped: this is source-blind Redline, with no source package supplied.
- **unresolved findings** — none reported; the actual idiom defect remains.
- **defects filed** — existing #341 remains supported as unresolved.
- **notes** — 87.75 native seconds, return code 0, no timeout. Full input, provenance, prompt, argv, native trace, visible commands, result, inventories and cleanup receipt are under `../editorial-329/followup/runs/final-idiom-control/`. PID 59502 ended; all own scratch is cleaned. This mandatory original acceptance replay is separate from newer Swedish artifacts and both mechanical controls; its failure is retained without retry.
