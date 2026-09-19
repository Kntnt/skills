## What to build

Part of #329; observed in candidate evaluation #338. Preserve the event to which a supplied date belongs when writing a customer case. This is a concrete Source Fidelity rejection, not a proposal for another general writing rule.

On `d60c4fc`, corpus `6e531f5`, GPT-6-astra/high and native Codex CLI 0.155.1, `/write --genre=case-study --language=en_GB --output=response source.md` produced:

> Before the trial began in September 2025, telephone reports and emails were stored separately.

The frozen source says that in September 2025 the maintenance team **decided to trial** a shared repair log. It gives the duration (eight weeks) and an internal-note date (4 December), but no actual start date. The output assigns September to commencement rather than the supplied decision. Neither plausible timing nor the later note establishes that date.

Evidence lives in `docs/evaluation/editorial-329/runs/candidate/case-study-en_GB/write/`: `supplied-input.md`, `artifact.md`, complete response and native traces. The independent F1 judgment is in `docs/evaluation/records/write-gpt-2026-09-19-338-part-article-case.md`. Redline receives only the draft, so it cannot be required to discover this hidden source mismatch.

Check whether the current source-fidelity contract already handles the distinction before adding any instruction. If a revision is warranted, address the actual ambiguity or conflicting instruction; keep the frozen material and failed observation intact. Several different faithful wordings can pass.

## Acceptance criteria

- [ ] The observed unsupported chronology remains recorded as an F1 failure, including exact input and output evidence.
- [ ] A real new candidate run is judged independently against the frozen matrix; the decision date is not silently converted to a trial-start date.
- [ ] Redline is judged only against text-visible support and claim preservation; no inaccessible-source check is imposed.
- [ ] Any changed instruction addresses a demonstrated cause without prescribing this fixture’s wording.
- [ ] The four checks in CONTRIBUTING.md pass for the integrated change.

---
Written against d60c4fc
