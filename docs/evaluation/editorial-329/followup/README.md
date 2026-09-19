# Source fidelity follow-up — #329

Thomas approved reopening #329 with #349 and #352 blocking quality completion; #341 follows at lower priority. Starting revision: `7ff6ec0`. Original corpus and failed outputs remain immutable. This directory contains supplementary diagnosis and evaluation, not replacements for the first delivery.

## Diagnosis plan

1. Reconfirm original failures from the preserved complete sources and outputs. The existing native pipeline is the red-capable loop; model runs take minutes and semantic judgement cannot be reduced to a deterministic seconds-long text assertion. That limitation justifies using frozen replay probes rather than claiming a unit test establishes prose fidelity.
2. Ranked hypotheses: (H1) composing and self-checking share a completion decision that prematurely accepts the draft; a fresh source-aware checker should detect failures the writer delivered. (H2) checking focuses on prominent numbers/quotes and misses implications and narrative circumstances; an explicit claim-to-support check should improve both patterns. (H3) the source is pragmatically misread, not overlooked; a fresh comparison would repeat the same absent-versus-unknown confusion. Quote idiom is assessed separately.
3. Replay the complete two failed drafts with their sources in fresh native sessions, using a neutral fact-check prompt that names neither issue nor faulty passage. These are diagnostic probes, not Skill evaluations. Preserve all outputs, actual model identity and writable-root inventories.
4. Freeze supplementary cases, repetition counts and outcomes before product changes or candidate runs. Test a bounded repair and assess all original editorial criteria plus source-check execution, without new style prescriptions.

## Tracker

#329 reopened: https://github.com/Kntnt/skills/issues/329#issuecomment-5744979279. Before-state threads are preserved in `tracker/`.

## Replay result

Both neutral source-aware replay probes detected exactly the original unsupported claim without an issue hint: the opinion checker distinguished no claim from no work, and the case checker rejected the invented request to assess. Responses are preserved in `probes/`; both private roots were inspected and removed. The probes took 20.92 and 18.35 seconds. They establish a viable detector seam, not end-to-end repair or general reliability. The original complete examples remain the regression seam; shrinking them would discard genre and context interactions that the final repair must preserve.

The predeclared supplementary run plan is [matrix.md](matrix.md). New source packages were prepared independently and read in full before freezing.

## Candidate mechanism

The candidate replaces unobservable composition-only self-checking with a fresh, read-only source comparison on the inherited seat. The writer owns supported repairs. A changed or disputed draft receives one final fresh comparison; unresolved checking withholds delivery. Sources and checked prose are preserved, reports remain private and are cleaned. This adds subagent capability and latency, which help/README/declarations expose. No genre rule, source fixture or editorial quality criterion changes. The broad code-preservation quantifier in the Skills rule now explicitly names editorial, anti-slop and mechanical passes, matching its existing subject; source comparison of newly generated claims is a different operation.

The supplementary corpus was frozen at `bf14dc2` before product edits. Original material is still byte-identical to `6e531f5`. Focused loading/account checks passed (3 tests). The external Skill validator reports the same two previously accepted extension-field complaints on baseline and candidate, with no new complaint.
