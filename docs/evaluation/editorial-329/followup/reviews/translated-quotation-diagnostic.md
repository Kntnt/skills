# Neutral translated-quotation diagnostic — #341

One bounded diagnostic used the complete original customer-case source and the complete failed Swedish `case-study-sv-r1` draft. The neutral task asked only whether each translated quotation was idiomatic Swedish speech while preserving source meaning, stance, certainty and voice. It named no suspect phrase and did not ask for a broad editorial or mechanical review. This is an additional diagnostic, not a replacement for any frozen matrix result or a formal Write/Redline pass.

The fresh native session at `8f92e12` independently identified exactly one problem: “innan nästa byggnad kommer i gång”. It explained that the source's compressed expression had become unnatural Swedish and proposed “innan vi kommer i gång i nästa byggnad”. It retained the other quotation language as valid speech rather than replacing it to taste.

The finding is justified. The proposed repair makes the activity's human participants explicit and moves the building to its locative role, preserving the conditional preparation recommendation and informal customer voice. The complete source supplies the team's trial and the potential next building; no new outcome, date, question, stance or certainty is added. The existing text alone also supplies enough context to recognize the missing activity. This diagnostic therefore supports an attention/operation hypothesis, not a missing-rule hypothesis: the model can identify the issue when quoted target-language speech is the explicit review unit.

## Existing obligation and smallest next experiment

The frozen source-blind `case-study-clean` control contains “innan nästa hus börjar”. Its `clean` label does not exempt that language from L1/R1. The original source-free control's other jobs remain preservation obligations: customer agency, qualified appraisal, measured facts, supplier stance and no gratuitous sales block. The supplied artifact provides the trial/log context; a reviewer can clarify only that established activity. It must not invent a different customer's experience or require source access. The matrix explicitly requires this unchanged control once after any idiom-specific repair.

Current case-study review guidance already requires checking quoted speech for target-language idiom, identifying missing referents, and clarifying only what the surrounding text settles. Base guidance already preserves meaning and voice. No fixture-specific prohibition or additional general ban is justified.

The smallest general execution experiment is to make **each passage of reported speech an explicit review unit inside Redline step 6**, before an overall no-findings decision: read its target-language phrasing against the already loaded language and genre guidance, record any concrete reader-facing defect through the existing findings format, then review the surrounding prose and bridges. Preserve valid speech; repairs still go through the existing correction budget and re-review. This adds no source comparison, new Skill, extra correction round, mandatory rewrite or separate mechanical pass. It changes the unit of attention rather than adding another rule about buildings.

This single diagnostic does not prove that procedural change works under the full Redline load. Verify it with the unchanged frozen control and both failed Swedish artifacts, preserving every old failure. Keep Write's source-comparison task limited to source support; a source check approving meaning must not be reported as an idiom pass. Any corresponding Write composition change should apply the existing translation policy while composing quotations, not disguise a broad editorial pass as source fidelity.

## Evidence and cleanup

- [Exact neutral prompt](../probes/translated-quotation/prompt.txt)
- [Complete supplied source and draft](../probes/translated-quotation/input.md)
- [Complete diagnostic report](../probes/translated-quotation/run-1/response.txt)
- [Native trace and invocation capture](../probes/translated-quotation/run-1/trace.jsonl)
- [Identity and tool-call audit](../probes/translated-quotation/run-1/trace-audit.json)
- [All-root filesystem changes](../probes/translated-quotation/run-1/filesystem-changes.json)
- [Cleanup receipt](../probes/translated-quotation/run-1/cleanup.json)

Codex CLI 0.155.1 observed `gpt-6-astra` / `high`, one native session, 28.7 seconds, exit 0. Its only tool operation read the complete input; it neither delegated nor invoked a Skill. No source or Skill filesystem effects remain, authentication is unchanged, and the private root was removed by its literal absolute path after capture. No product files were changed.
