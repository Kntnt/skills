Candidate evidence from the independent article/case batch confirms this defect at `d60c4fcc0228ae37b348c57374f4d8c6ead5a0bd` (corpus `6e531f5`, GPT-6-astra/high, Codex CLI 0.155.1).

The normal case-study/sv Write invocation again produced “Jag skulle avsätta den tiden innan nästa byggnad börjar.” This was judged against the English source and frozen L1 criterion **before** reading this issue for comparison. Redline then received only the complete draft and metadata, with no source or evaluation hint, and returned no-change. The phrase therefore remains after its actual installed Proofread pass. All other claims, customer reservations and quotation substance were preserved.

Evidence: `docs/evaluation/editorial-329/runs/candidate/case-study-sv/{write,redline}/` contains response, full artifact, traces/native child session, inventories and cleanup. Separate Write/Redline judgments are in the `*-338-part-article-case.md` records.

This is a repeated idiom defect and missed editorial diagnosis, not a mechanical spelling failure. A later instruction repair/rerun must preserve this observed outcome rather than replace it.
