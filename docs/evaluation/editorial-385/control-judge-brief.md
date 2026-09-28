# Control judge brief

You judge one run of a reviewing Skill against a control text. The Skill received one text, `work/input.md`, and nothing else: it never saw any material the text may have been written from, and neither do you. It reviews, corrects within a budget, and returns the text with an account of what it changed. Its reply is `response.md`, and the standard it is judged against is `expectation.md`. Read exactly those three files, all in the run directory named in the message that sent you here. Read nothing else — no other run, no repository file, no ticket. You are not told how the Skill or the run was configured, which version of it ran, or which model produced the reply, and you must not guess or try to find out.

## The standard for this control

The file `expectation.md` in the run directory holds this control's expectation. It comes from this evaluation's plan, not from the evaluation corpus. Where the expectation refers to another row or to a line of the corpus, the text it refers to is written out in full beneath it and labelled as such. It says what a run of this control is expected to detect and what it is expected to preserve. It is the standard, and it is not a prediction of how this run went. Judge what is in front of you against it.

## What to write

Write `judgement-<your letter>.md` in the run directory, with the letter the message gave you. Answer every heading.

**1. Differences.** Every difference between `work/input.md` and the returned text, one line each: the text before, the text after, and its class — a mechanical correction, the repair of a visible defect, a change of taste, or a change to what a claim says with which of **scope**, **certainty**, **attribution**, **chronology**, **causality** or **meaning** it changed. Include frontmatter and formatting.

**2. The account.** For every difference above, say whether the Skill's own reply reports it, and whether it reports it accurately.

**3. The frozen expectation.** Take the expectation clause by clause. For each thing it says the run should detect, say whether the reply reports a finding that names it, quoting the finding. For each thing it says the run should preserve, say whether the returned text preserves it, quoting the passage. For each rejection it names, say whether the run made that mistake.

**4. The expectation: pass or fail**, with the passage that decides it.

Then reply in at most 120 words: the verdict on the expectation, which clauses of the expectation were met and which were not, and the path you wrote.
