**The run stopped before delivery. No source comparison could be made, so nothing was written to `article.md`.**

The draft is complete but unchecked, and it is preserved at:

`/Users/thomas/Projects/skills/.git/kntnt-orchestrate/376.scratch/regression/R-B3/work/article.NOT-SOURCE-CHECKED.draft.md`

`article.md` was left unwritten, as the requested artifact must not be mistaken for prose no comparison has read.

**The obstacle.** The source comparison has to save the complete prose in a fresh scratch file, hand the checker that exact file, and have the checker write its report to a path in the same scratch directory. The only scratch location available to this run is `.../R-B3/scratch/`, and it is not writable: creating a file in it and creating a directory inside it both fail with "Permission denied" (mode `dr-x------`). The comparison's scratch, drafts and reports may not be placed anywhere else, and file permissions may not be changed, so there is no way to give the checker the prose or to receive a report. A missing report is not a completed comparison.

**What was and was not compared.** No comparisons ran — zero of the one or two this Skill would make. No passage of the draft has been set beside the material it rests on, and no finding is claimed or ruled out. I assert no fidelity for the preserved prose; it has been written with care against the material, and that is not the same as checked.

**What was resolved.**

- Genre: `article`, from the invocation.
- Language: `en_GB`, from the invocation, verified against the installed Language Resources (English, United Kingdom).
- Technique: none. The `article` resource states that this genre has no technique it is ordinarily written with, so no arc was imposed and the draft runs on ordinary exposition.
- Output target: `article.md` in the working directory — a path distinct from the supplied `source.md`, so nothing would have overwritten the material. It remains unwritten.
- Handoff metadata: not attached. The `kntnt` map marks a finished artifact for the Skills that read one, and the preserved file is not that.

**Where the material stopped.** The brief asks for the case that the pilot is worth copying, and the material carries no outcome for that case to rest on. The 25 per cent dwell-time figure is a published objective of the municipality's FRAKT-N programme, not a measured result; the technical annex records that noise modelling and continuous sound-level monitoring at three kerbside points exist, but no value they produced; the 412 deliveries come with the operator's own statement that no comparison with vans is claimed, because the routes were not matched; and the evaluation report is planned but unwritten. The draft therefore argues from the pilot's method rather than from its results, which is the strongest case the material supports.

Two things the material leaves open, which the draft is careful not to close: it does not say that the cargo-cycle pilot is part of the FRAKT-N programme, so the programme's objective and season are attributed to the programme and not to the pilot; and it does not identify "the operator" who supplied the delivery figures as Nordvik Logistik AB, so the two are kept apart throughout. Material that settled either point would let the argument be drawn tighter. Measured noise levels from the three kerbside points, a dwell-time measurement, or a matched-route comparison would let the case rest on results instead of on method.

**To resume.** Make a writable scratch directory available to the run and invoke `/write` again with the same arguments; the comparison would then read the prose preserved above rather than starting the draft over.
