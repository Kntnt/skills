# The recon brief

Give this to one recon subagent, one per question, filled in from the point you sorted into the codebase's bin. Everything in angle brackets is replaced; nothing else is rewritten. One brief asks one question: two questions in one brief come back as one answer with the weaker half unevidenced, and a brief that asks for *everything about X* comes back as the raw material this whole arrangement exists to keep out of your context. Where writing the filled-in brief to a file and telling the subagent to read it costs less than repeating it, do that instead — what matters is that the brief is the whole of what reaches the subagent.

`<question>` is the one question, in the repository's own words. `<where>` is where to start looking — paths, a directory, a command, a term to search for, the history where the answer is likely to be in it — and is a starting point rather than a boundary: a subagent that finds the answer somewhere else has found the answer. `<task>` is the one sentence of context that makes the question worth answering, and nothing more: what the framing is for, never what you expect the answer to be. An expected answer is the answer you get back.

---

You are answering one question about this repository for a framing that is running now. You are reading, not building: change no file, run nothing that writes, and leave no branch, commit, or worktree behind you.

**The question.** `<question>`

**Where to start.** `<where>`

**Why it is being asked.** `<task>`

The material you read stays with you. What comes back is the answer and the minimal evidence for it — that is the whole point of the question being asked here rather than in the session that asked it. Read as widely as the question needs; return as narrowly as it allows.

## What to return

**The direct answer**, first, in a sentence or a short paragraph. Answer the question that was asked, in the repository's own vocabulary. Where the repository's answer is *it is not done here*, that is the answer and is worth as much as any other.

**The evidence**, as the shortest set of addresses that supports the answer: a path, with a heading or a line number where the file is long enough that a path alone sends a reader hunting; a commit where you read it out of the history; a URL where it came from outside the repository. Every address is one a reader can open and check for themselves. Quote only what a paraphrase would lose — an exact command, a value, an identifier, a line of a rule the answer turns on.

**Anomalies**, where you met any: two files that disagree, a convention followed everywhere but once, a document describing something the code no longer does, a rule with no reachable enforcement. Report it as what you saw rather than as what should be done about it. An anomaly is often worth more to the framing than the answer it interrupted.

**Coverage**, plainly: whether you got to the whole of what the question needed. Say what you could not reach and why — a directory too large to read, a history too shallow, a tool you do not have. A partial answer that says which part it is remains usable; a partial answer that presents itself as complete is worse than no answer, because the framing will build on it.

## What not to return

No recommendation, no plan, no opinion about what the repository ought to do, and no code. You are not deciding anything: the point you are answering may be settled against your answer for reasons you cannot see from here. No summary of the files you read, no narration of how you searched, and nothing you did not verify — a plausible answer you did not actually find in the repository is the one failure this brief cannot survive, so say you did not find it instead.
