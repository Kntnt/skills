# Redline pair judge brief

You judge one run of a reviewing Skill. The Skill received one text, `redline/work/input.md`, and nothing else: it never saw the material the text was written from. It reviews, corrects within a budget, and returns the text with an account of what it changed. Its reply is `redline/response.md`. Read those two files, and also `write/work/source.md`, the material the input was originally written from. The Skill did not have that file; you have it only to answer question 3. Read nothing else. You are not told how the Skill or the run was configured and must not guess.

Criterion R1, from the evaluation corpus: Does Redline address concrete visible defects while preserving working voice, arguments, quotations and claims outside findings? Compare every before/after claim; report legitimate removals, rejected losses and irreparable findings. Clean texts may not be rewritten to satisfy taste or numerical guidelines. No unavailable-source verification.

Write `redline/judgement.md` in the run directory:

1. Every difference between input and returned text, one line each: before, after, and whether it is a mechanical correction, the repair of a visible defect, a change of taste, or a change to what a claim says (its strength, subject, scope or modality).
2. R1: pass or fail. For every removal and every changed claim, say whether the Skill's own account reports it, and reports it accurately.
3. Separately, and not part of R1, since the Skill could not know: did any change remove or alter something the source material required, such as a stated caveat or a careful formulation of what is and is not claimed? Quote the source.

Reply in at most 100 words with the R1 verdict, the answer to question 3, and the path.
