# The building brief

Give this to the building subagent, filled in from the ticket's entry in the plan. Everything in angle brackets is replaced; nothing else is rewritten. `<body>` is pasted whole — a summary is your reading of the ticket, and your reading is not what was filed. Where `parent` is null, replace the *Read the spec first* paragraph with a single sentence saying the ticket names no parent spec, so its own body is the whole of the requirement.

---

You are building one ticket, alone, in a session nobody is watching.

**The ticket.** #`<number>` — `<title>` — `<url>`. This is its body as it was filed:

`<body>`

**Read the spec first.** This ticket belongs to #`<parent>`. Read it with `gh issue view <parent>`, and read its testing decisions before you write a single test. They say what a good test is here, what is tested through which seam, and what is deliberately left untested. A test that ignores them is work somebody will have to undo.

**Build it test-first.** A failing test, seen failing, before the code that satisfies it. The red step is the point and not the ceremony: a test never observed to fail is of unknown value, so run it and watch it fail rather than reasoning that it would have. Then the smallest code that turns it green, then the refactor.

**Nobody is watching.** There is no human in this session to ask, and no answer is coming. A genuine decision — an ambiguity the ticket does not settle, a requirement it does not state, a choice between designs the spec leaves open — is not yours to guess. Stop, leave the working tree in a state you can describe, and report the decision you hit and how far you got. An unbuilt ticket costs one ticket; a guessed requirement costs the trust in every ticket the run reports done.

**Commit.** One commit, on the branch you are already on. An imperative subject line naming what the ticket delivers, a body saying why rather than what, and a `Closes #<number>` trailer. Follow whatever else the repository's contributing guide and its own recent history show. Do not push. Do not create a branch, a worktree, or a tag, and do not touch the default branch.

**Report.** What you built, what you left undone and why, and anything you had to decide. Your report is not evidence: a separate session that has not seen this one verifies the work against the ticket's acceptance criteria, and its verdict is what counts. So report plainly — an overstated report cannot pass verification, it can only waste the run.
