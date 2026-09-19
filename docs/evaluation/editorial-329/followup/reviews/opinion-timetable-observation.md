# Opinion timetable observation

Observed in the unchanged candidate `8f92e12`, `opinion-absence-en_GB-r2`. The source explicitly requests an eight-week deferral while acknowledging that completion within eight weeks is not established. Write preserves both. Its independent F1 judgement passes.

Source-blind Redline identifies that same qualified request as a defect, delegates one correction and retains the text because changing the request would alter the author's position. It reports: “Readers cannot judge whether the deferral is sufficient. Resolving this requires evidence or a change to the author’s proposal.” The response then repeats the complete artifact in a Markdown fence. The prose and metadata are unchanged; the extracted copy has one fewer trailing blank line.

The timing finding is a false positive: a requested policy timetable with expressly acknowledged uncertainty does not claim that the study can or will finish within it. Requiring evidence of timely completion as a condition of accepting the opinion changes the author's advocacy into a feasibility guarantee. The correction agent properly preserves the author's claim, so this is a review-finding problem rather than an introduced factual error or loss of position.

Filed separately as [#354](https://github.com/Kntnt/skills/issues/354), the timetable false positive, and [#353](https://github.com/Kntnt/skills/issues/353), the delivery-rule collision below.

## Initial delivery assessment and correction

The evaluator initially described repetition of the unchanged artifact as a clear no-change delivery violation and, before checking the final trailing whitespace, as byte-identical. Both statements need qualification. The extracted prose and metadata match, but one trailing blank line differs. More importantly, Redline step 11 expressly requires artifact delivery when findings remain even if nothing changed, while the shared delivery contract says response-targeted unchanged runs return only status. Root's independent review identified this contract collision; direct reading of the full Redline body confirms it.

The repetition therefore is not scored as unambiguous model disobedience. The observed filesystem outcome is clean. The disputed no-change delivery branch is marked as a contract ambiguity pending the root's disposition, separately from the false-positive finding. Neither observation changes Write's source-fidelity pass or erases the complete native evidence.

Evidence: [Write draft](../runs/candidate/opinion-absence-en_GB-r2/write/artifact.md), [Redline response](../runs/candidate/opinion-absence-en_GB-r2/redline/response.txt), [extracted final](../runs/candidate/opinion-absence-en_GB-r2/redline/artifact.md), [native audit](../runs/candidate/opinion-absence-en_GB-r2/redline/native-audit.json), [filesystem changes](../runs/candidate/opinion-absence-en_GB-r2/redline/filesystem-changes.json).
