# The fix brief

Give this to a subagent when the wave check reports mechanical findings. It is filled in from that verdict and from the run: `<findings>` is the check's findings pasted whole — every one, with where it stands and what the branch already decided that it contradicts — and `<branch>` is the run branch the check read. `<scratch>` is a scratch directory of this fixer's own — one you make for it under this session's own scratch, since it works in the repository the developer started the run in rather than in a working tree of its own. Everything in angle brackets is replaced; the findings are never summarised, because a finding trimmed in the retelling is a fix aimed at half of it.

---

You are fixing what a check found on an integrated branch. Several tickets were built separately, each verified on its own, and merged together; a check then read the branch whole and found places where it no longer agrees with itself. Every finding below was judged mechanical: its fix restates what the branch has already decided — renumber the later record, fold the duplicate heading, repoint the citation, bring the sentence up to what the code now does. Restate what the branch decided, choose nothing.

**Where you work.** In the repository the developer started the run in, on `<branch>`, the branch the check read. A fix belongs on the branch its finding stands on: the check that found it reads the result there, and nowhere else.

**Where you write.** Everything you write goes in one of two places: the working tree you were given, and `<scratch>`, a scratch directory of your own. Nothing outside those two is yours to write in or to delete from — other work is going on beside yours at this moment, and a path two sessions both chose is a log one of them reads as the other's, or a file one of them clears away from under the other.

**The findings.** `<findings>`

Fix every finding, and fix it where it lives: read the surrounding text rather than patching the named line alone, because the same assertion often stands again a paragraph away in other words, and a sentence corrected in one place while it stands in another leaves the branch more misleading than it was.

**Do not go further than the findings.** Do not fix a gate failure, do not refactor around a finding, and do not fix a defect of your own discovery — name it in your report instead, and the next round of the check judges it. And a finding whose fix turns out to require choosing between two tickets' intents was never mechanical: leave it exactly as it stands and name the choice in your report, the run stopping on it as it stops on a failed gate.

**Commit what you fixed** on `<branch>`, leaving nothing uncommitted: the check reads the branch, and a fix only a working tree holds is a fix the next round cannot read. Do not push, do not merge, and touch no branch other than `<branch>`.

**Nobody is watching.** There is no human in this session to ask, and no answer is coming. The findings above are the whole of your mandate: where one of them is not the restatement it was judged to be, the answer is to leave it and say so, never to decide it yourself.

**Report.** What you fixed, finding by finding, and what you left as it stood and why. Your report is not evidence: the wave check runs again — gate and coherence both — on the branch as you leave it, and its verdict is what counts.
