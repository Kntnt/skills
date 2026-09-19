# Read-only diagnosis of #359

No new run or product edit was made. Read complete current Redline steps 7–11, its correction brief, installed Proofread body, shared delivery and the preserved frozen-clean-r1 native stages.

## What is observed

The initial artifact spells “arbetsbelastning” correctly. The correction agent returns the complete artifact with the intended local quotation repair and still correct spelling. The fresh quotation re-reader reads that complete artifact from an actual scratch file; its stdout also has the correct spelling. The final parent response contains “arbetsbelastningning”. The mechanical child follows the installed Proofread Skill once and reports no change. Its exact input arrives in an encrypted native dispatch, and it does not independently read an artifact file. The trace therefore cannot distinguish corruption during mechanical dispatch from a missed mechanical error or later parent transcription. Only the final corruption and last visible correct artifact are established.

Exact evidence and native filenames are retained in `unfiled-defects.md`, `runs/final-quotation-controls/frozen-clean-r1/redline/independent-audit.json` and the full native directory. Issue: [#359](https://github.com/Kntnt/skills/issues/359).

## Existing contracts and transport seams

The correction brief deliberately requires complete text in the direct delegation message and forbids replacing that message with a file path. That is an existing explicit boundary; a file-based correction transport would change its contract and cannot be introduced as if already available. In this failure its complete returned artifact is visibly correct, so it is not the observed failing seam.

Proofread's public interface already accepts one local file as input and a separate explicit output path, or a single current-turn artifact through the omitted-operand form. Shared delivery requires the complete artifact at an explicit different output destination even if no correction is needed. Those capabilities already exist; no new parser option or mechanical criterion is required to use them.

Redline currently chooses a narrower transport: fixed `--language=<resolved> --output=response`, no formal operand, with the complete current artifact supplied separately. It then accepts the complete returned result, or retains its held artifact when Proofread says no change. Neither current step requires the mechanical child to read an exact frozen file or to return an inspectable file. This is a concrete observability/state-selection seam, not evidence that the mechanical child actually received the wrong text.

One possible operational repair, if separately authorized and evaluated, is to materialize the approved complete current artifact once, invoke the public Proofread file-input/separate-file-output forms on private scratch paths, then read and deliver the resulting file as the sole final artifact. The explicit output exists even on a clean pass, removing the no-change branch's dependence on a separately remembered text. This requires changing Redline's present step-9 formal invocation and coherent documentation, not Proofread's grammar or quality norm. The source snapshot, result and inventories would make the mechanical boundary inspectable; the outer response still must preserve those bytes, so a file alone does not prove that final transcription is exact.

A smaller observability-only option would keep the current omitted-operand/response form and explicitly identify the frozen input file for a full child read. It establishes what was checked and preserves a definite no-change input, but leaves a changed response and final parent transcription as text transport. Neither option is verified by the existing failure, and neither is a reason to claim #359 fixed without a declared native test of exact final preservation.

The existing norms already require the full mechanical result, unchanged nonmechanical wording and nothing touched after the final pass. A new sentence saying “do not introduce this typo” would add no missing requirement. Do not expand the mechanical pass count or add a word-specific scanner to compensate for an unlocated execution failure.
