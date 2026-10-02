# Control judge brief

You judge one run of a reviewing Skill against a control text. The Skill received one text, `work/input.md`, and nothing else: it never saw any material the text may have been written from, and neither do you. It reviews, corrects within a budget, and returns the text with an account of what it changed. Its reply is `response.md`. Read exactly those two files, both in the run directory named in the message that sent you here. Read nothing else — no other run, no repository file, no ticket. You are not told how the Skill or the run was configured, which version of it ran, or which model produced the reply, and you must not guess or try to find out.

## The standard for this control

The message that sent you here carries one paragraph headed **Frozen expectation**, taken verbatim from the evaluation corpus. It says what a run of this control is expected to detect and what it is expected to preserve. It is the standard, and it is not a prediction of how this run went. Judge what is in front of you against it.

## Criterion R1, from the evaluation corpus

Does the Skill address concrete visible defects while preserving working voice, arguments, quotations and claims outside findings? Compare every before/after claim; report legitimate removals, rejected losses and irreparable findings. Clean texts may not be rewritten to satisfy taste or numerical guidelines. No unavailable-source verification.

Two things the corpus settles for you. A corrected example may legitimately retain reported findings that require facts the text does not hold: detection and preservation are scored apart from the final text's quality. And the Skill ends every run by handing the whole mechanical pass to a separate proofreading Skill it does not control, so a correction confined to spelling, punctuation, grammar or a locale form of dates, numbers or currency is that pass's work: note it in your list of differences, but do not count it against the Skill under R1 and do not treat it as a failure to report.

## What to write

Write `judgement-<your letter>.md` in the run directory, with the letter the message gave you. Answer every heading.

**1. Differences.** Every difference between `work/input.md` and the returned text, one line each: the text before, the text after, and its class — a mechanical correction, the repair of a visible defect, a change of taste, or a change to what a claim says with which of **scope**, **certainty**, **attribution**, **chronology**, **causality** or **meaning** it changed. Include frontmatter and formatting.

**2. The account.** For every difference above, say whether the Skill's own reply reports it, and whether it reports it accurately.

**3. The frozen expectation.** Take the expectation clause by clause. For each thing it says the run should detect, say whether the reply reports a finding that names it, quoting the finding. For each thing it says the run should preserve, say whether the returned text preserves it, quoting the passage. For each rejection it names, say whether the run made that mistake.

**4. R1.** Pass or fail, with the passage that decides it.

Then reply in at most 120 words: the R1 verdict, which clauses of the frozen expectation were met and which were not, and the path you wrote.
