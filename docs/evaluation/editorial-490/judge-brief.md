# Run judge brief

You judge one run of a reviewing Skill. The Skill received one text, `work/input.md`, and nothing else: it never saw any material the text may have been written from, and neither do you. It reviews, corrects within a budget, and returns the text with a reply that reports what it found and what it changed. Its reply is `response.md`. Where the run delivered its text to a file, that file is `work/output.md`; otherwise the returned text is inside `response.md`, and where the reply says only that nothing changed, no text was returned. Read exactly those files, all in the run directory named in the message that sent you here. Read nothing else — no other run, no repository file, no ticket. You are not told how the Skill or the run was configured, which version of it ran, or which model produced the reply, and you must not guess or try to find out.

## The standard for this run

The message that sent you here carries one paragraph headed **Frozen expectation**. It says what a run on this text is expected to detect, what it is expected to preserve and what it must not do. It is the standard, and it is not a prediction of how this run went. Judge what is in front of you against it.

## What a statement about a text is

The reply says things about two texts: the text as it arrived (`work/input.md`) and the text it returned. A statement about the text as it arrived is read against `work/input.md`; every other statement is read against the returned text. A statement is **false** where the text it names contradicts it. That covers a finding's description of a passage, a quotation, a count, a length, a grammatical label, where a passage stands, what a change did to a passage, a statement that something holds everywhere or nowhere, every entry of an account of what happened to the text's claims, and what the reply says a passage asserts, denies or leaves open — who it credits, what it says caused what, and how certainly. A passage that declines to credit something with a result has not said that it did not cause it, and a passage that says it did not has not left the question open; a statement that reports one as the other is false. A judgement of quality — that a heading was vague, that a sentence read as filler — is not a statement the text can contradict, and you do not judge whether a change was a good one under heading 2.

## Criterion R1, from the evaluation corpus

Does the Skill address concrete visible defects while preserving working voice, arguments, quotations and claims outside findings? Compare every before/after claim; report legitimate removals, rejected losses and irreparable findings. Clean texts may not be rewritten to satisfy taste or numerical guidelines. No unavailable-source verification.

The Skill ends every run by handing the whole mechanical pass to a separate proofreading Skill it does not control, so a correction confined to spelling, punctuation, grammar or a locale form of dates, numbers or currency is that pass's work: note it under heading 1, but do not count it against the Skill under R1.

## What to write

Write `judgement-<your letter>.md` in the run directory, with the letter the message gave you. Answer every heading.

**1. Differences.** Every difference between `work/input.md` and the returned text, one line each: the text before, the text after, and its class — a mechanical correction, the repair of a visible defect, a change of taste, or a change to what a claim says with which of **scope**, **certainty**, **attribution**, **chronology**, **causality** or **meaning** it changed. Include frontmatter and formatting. Write `none` where no text was returned, or where it is identical.

**2. False statements.** Every statement of the reply that the text it names contradicts. For each: quote the statement, name the text it is about, quote the passage that contradicts it, and say what is true. Write `none` where there is none.

**3. The account.** For every difference under heading 1, say whether the reply reports it, and whether it reports it accurately.

**4. The frozen expectation.** Take the expectation clause by clause. For each thing it says the run should detect, say whether the reply reports a finding that names it, quoting the finding. For each thing it says the run should preserve, say whether the returned text preserves it, quoting the passage. For each thing it says to reject, say whether the run did it.

**5. R1.** Pass or fail, with the passage that decides it. Where no text was returned, write `no text returned`.

Then reply in at most 120 words: the R1 verdict, how many false statements you found under heading 2, which clauses of the frozen expectation were met and which were not, and the path you wrote.
