## What to build

Diagnose and repair a source-support failure in Write without weakening the frozen editorial-quality F1 criterion or adding an example-specific writing rule. The final `case-study-en_US` sample writes “Asked to assess the experience, Lind offered a qualified judgment”. The supplied source establishes an email interview and Lind's actual qualified assessment, but supplies no question or account of a request to assess it. The framing adds a plausible interview event; “Lind offered a qualified judgment” would convey the supplied fact without that event.

This is distinct from #341's Swedish idiom and #349's unknown-versus-known-absent problem. The existing base Claims boundary already covers circumstantial detail, and Write's new completion criterion requires source checking as part of writing. Both were actually loaded here. No new runtime rule or rubric amendment is justified merely by this failure.

## Evidence

- Instructions: `29ff2047ad2dac330dd705feccdb3f2d0778831b`; corpus: `6e531f5fe0b610e046ae58787f246cc6239acbcc`.
- Exact invocation: `/write --genre=case-study --language=en_US --output=response source.md`.
- Native Codex CLI 0.155.1; inherited gpt-6-astra/high, no model override.
- Complete source, response, extracted artifact, actual loads/native trace, full writable-root inventories and cleanup: `docs/evaluation/editorial-329/runs/rerun-341-translation/case-study-en_US/write/`.
- Source package: `docs/evaluation/corpus/editorial-quality/sources/case-study.md`; original question is absent, not contradicted by some alternate supplied question.
- Record: `docs/evaluation/records/write-gpt-2026-09-19-341-translation-part-article-case.md`, case-study-en_US, F1 fail (unsupported circumstance). Every figure, chronological limit and all three source quotations otherwise survive accurately.
- The independent Redline pair receives only the full artifact, no source or this finding. An unseen source omission cannot fairly be required of that review.

## Acceptance criteria

- Preserve this failed artifact and criterion; do not convert the observation to a pass because the added prompt seems likely.
- Establish whether an actual contract conflict or execution defect caused unsupported interview framing. Retain the concise source-support contract unless a concrete ambiguity warrants a change.
- Verify any repair on the unchanged source and prompt in a fresh GPT-native session, including the quoted assessment without invented interview questions or actions. Record every applicable criterion and complete side effects, with a separate source-blind Redline stage.
- Keep the original and later outcomes separate, including any limits of a successful stochastic rerun. Documentation alone does not close the underlying defect.

Written against editorial-329 at `29ff204`, corpus `6e531f5`, and the frozen evaluation protocol/matrix.
