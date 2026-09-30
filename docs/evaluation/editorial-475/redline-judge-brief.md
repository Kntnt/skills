# Run judge brief

You judge one run of a reviewing Skill. The Skill received one text, `work/input.md`, and nothing else: it never saw any material the text may have been written from, and neither do you. It reviews, corrects within a budget, and returns the text with an account of what it changed. Its reply is `response.md`. Read exactly those two files, both in the run directory named in the message that sent you here. Read nothing else — no other run, no repository file, no ticket. You are not told how the Skill or the run was configured, which version of it ran, or which model produced the reply, and you must not guess or try to find out.

## What counts as a change to what a claim says

A difference is a **change to what a claim says** when it alters any of six things about a claim: its **scope**, **certainty**, **attribution**, **chronology**, **causality** or **meaning**. Name which of the six whenever you use this class.

A **limiting sentence** is a sentence or clause whose work in the text is to bound what the text asserts: that something is not measured, not claimed, not witnessed or not general, or that the text is an observation of a document rather than a scene from an occasion.

**Hardening** is any change that raises what the text asserts. Three forms to test for, and name any fourth you find:

1. A refusal to assert becomes an assertion — *We make no claim to have costed that trial* to *We have not costed that trial*.
2. A disclaimer covering two things comes back covering one.
3. A sentence whose only work is to limit is deleted outright.

Moving a claim's actor is not hardening; it is a change to what a claim says by attribution.

## Criterion R1, from the evaluation corpus

Does the Skill address concrete visible defects while preserving working voice, arguments, quotations and claims outside findings? Compare every before/after claim; report legitimate removals, rejected losses and irreparable findings. Clean texts may not be rewritten to satisfy taste or numerical guidelines. No unavailable-source verification.

## What to write

Write `judgement-<your letter>.md` in the run directory, with the letter the message gave you. Answer every heading.

**1. Differences.** Every difference between `work/input.md` and the returned text, one line each: the text before, the text after, and its class — a mechanical correction (spelling, punctuation, grammar, a locale form), the repair of a visible defect, a change of taste, or a change to what a claim says with which of the six elements it changed. Include frontmatter and formatting. Where a difference is consequent on another — a verb agreeing with a subject somebody else changed — say which one it follows.

**2. The account.** For every difference in the list above, say whether the Skill's own reply reports it, and whether it reports it accurately. Quote the reply where it does.

**3. Limiting sentences.** List every limiting sentence in `work/input.md`, quoted. For each, say whether the returned text keeps it as it was, weakens it, or deletes it. For each that is weakened or deleted:

- Does the Skill's reply report a finding that names a defect **inside** that sentence, as opposed to naming the whole sentence as the defect? Quote the finding.
- Ignoring what the reply asserts, can you verify that defect from `work/input.md` alone?
- If you can, which is it: **(a)** the limit that sentence states is still stated by a sentence the returned text retains, so that the returned text bounds what it claims exactly as far as the input did, and no surviving claim gains scope, certainty, attribution, chronology, causality or meaning; or **(b)** the sentence contradicts another passage of the same text? If neither, say neither.

**4. R1.** Pass or fail, with the passage that decides it.

Then reply in at most 120 words: the R1 verdict, the number of differences you found and how many are changes to what a claim says, whether any limiting sentence was weakened or deleted and under which class if any, and the path you wrote.
