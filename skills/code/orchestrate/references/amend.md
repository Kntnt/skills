# The amending brief

Give this to a fresh building subagent when a verifying subagent's verdict is a fail and `amend` says the ticket's one amend is still there. It is filled in from the same entry in the plan that `brief.md` was filled in from, from what `isolate` answered for that ticket, and from the verdict that failed it: `<verdict>` is what the verifying subagent reported, pasted whole — an abridged verdict is your reading of the failure rather than the failure, and the verdict is the whole of what this build has that the first one did not. Everything in angle brackets is replaced; `<body>` is pasted whole, and so is every entry of `<thread>`. `<thread>` is that entry's `thread` rendered in the order it holds, one block per entry, each opening with its `author` and `created_at` and then its `body` pasted whole under the same rule. Where `thread` is empty, drop the *What has been said since* paragraph and the `<thread>` under it. Where `parent` is null, replace the *Read the spec first* paragraph with a single sentence saying the ticket names no parent spec, so its own body is the whole of the requirement. `<scratch>` is the scratch directory that same answer named, and `<reservations>` is that answer's `reservations`, one line per entry naming that entry's `directory` and the `number` reserved in it. Where it reserved none, drop the *Numbers are reserved for you* paragraph and the `<reservations>` under it — this repository keeps no records named by number, so there is nothing to hand out. `<run-owned>` is the run's own files as you named them at run start, one line per file naming its path and the kind of entry a ticket writes in it, and `<note>` is `.kntnt-orchestrate/<number>.md` with this ticket's own number in it, so no two tickets' notes are the same path. Where you named none, drop the *Some files are the run's to write* paragraph together with the `<run-owned>` and the two paragraphs under it, so a repository with no changelog and no append convention of its own briefs its amenders exactly as it briefs its builders. `<gate>` is the gate you resolved at run start, pasted as the list of commands it was written down as — never re-derived here, and never widened. Where the plan's `worktrees` is false, replace the *Where you work* paragraph with a single sentence saying the work happens in the repository as it stands, on the branch already checked out, and replace the *Numbers are reserved for you* paragraph with a single sentence saying nothing is being built beside this ticket, so a record it creates takes the next free number in its own directory — one above the highest there; `<scratch>` is then the directory you made for this ticket under this session's own scratch. This subagent has not seen the building session and is never told what the builder reported: what it gets is the ticket and the verdict, and nothing else about the try that failed.

---

You are amending one ticket that somebody else built, in a session nobody is watching. It was built alone, a session that did not build it verified it, and that verdict was a fail. The work stands where the builder left it, and the verdict below says what is wrong with it. Other tickets are being worked at the same time, each somewhere else; none of them is yours to look at or wait for.

**The ticket.** #`<number>` — `<title>` — `<url>`. This is its body as it was filed:

`<body>`

**What has been said since.** A ticket is a thread, and the body above is only its first post. This is everything written on it since it was filed, oldest first:

`<thread>`

Where any of that contradicts the body, the later text stands: a question the body leaves open and a comment answers is answered, and the answer is the requirement. Acceptance criteria stated in a comment are acceptance criteria, and they are what this work is verified against.

**The verdict that failed it.** This is what the verifying subagent reported, in full:

`<verdict>`

**Where you work.** In `<worktree>`, which is a working tree of this repository holding this ticket's work and nothing else's, with the branch `<branch>` checked out in it. Everything you do happens there — read, build, test, and commit in that directory and nowhere else. The developer's own working tree is elsewhere and is not yours to touch; work landing on their branch is somebody else's job once your work has been verified.

**Where you write.** Everything you write goes in one of two places: the working tree you were given, and `<scratch>`, a scratch directory of your own. Nothing outside those two is yours to write in or to delete from — other work is going on beside yours at this moment, and a path two sessions both chose is a log one of them reads as the other's, or a file one of them clears away from under the other.

**Numbers are reserved for you.** This repository keeps records named by a four-digit number, and one number in each such directory is reserved for this ticket and for no other:

`<reservations>`

Where your work creates a record in one of those directories, name it with the number reserved here, rather than reading the directory for the next free one — the tickets being built beside yours are reading it at this same moment and would every one of them read the same answer. A number reserved and never used is a gap, and a gap is legitimate: next free means one above the highest, never the lowest hole. Where the work needs more numbers in one directory than the one reserved for it, that is a decision this brief did not settle — stop and report it, exactly as *Nobody is watching* below says.

**Some files are the run's to write, not yours.** These files are written by the run itself rather than by any builder, because every ticket built tonight would otherwise append to the same few lines of them:

`<run-owned>`

Never edit one of those files. Where your work has an entry for one — a changelog line, a worklog entry, a line in a list of references — write the entry to `<note>` instead, a note file of this ticket's own inside your working tree, and commit it with the rest of your work. Write it as one block per file: a line naming that file's path, then the exact text that is to be added to it, as it is to read there. Where your work has an entry for none of them, write no note at all.

Nothing is deferred further than the wave you are part of. Once this wave's work is merged, the run applies those entries to the real files one ticket at a time and takes the notes away, and the branch is verified with the entries in place — appends made one after another cannot collide, which is the whole of why they are not yours to make.

**Read the spec first.** This ticket belongs to #`<parent>`. Read it with `gh issue view <parent>`, and read its testing decisions before you write a single test. They say what a good test is here, what is tested through which seam, and what is deliberately left untested. A test that ignores them is work somebody will have to undo.

**Answer the whole verdict.** Every command it says failed and every criterion it says is not met, not the ones that look cheapest — a verdict answered in part fails again, and this ticket has no third try. Fix the ticket rather than the complaint: the verdict is where to look, and the ticket is what you are held to.

**Build it test-first.** A failing test, seen failing, before the code that satisfies it. The red step is the point and not the ceremony: a test never observed to fail is of unknown value, so run it and watch it fail rather than reasoning that it would have. Then the smallest code that turns it green, then the refactor. Then run the project's verification gate yourself — these commands, resolved once at run start from the project's contributing guide, are the gate: `<gate>`. Run all of them, not a subset: a check this list does not name is not run in its place, and a fix you did not run is a guess.

**A long command is waited on, not yielded to.** Where something you run takes long — a full test suite, an integration suite that runs for a quarter of an hour, a build — start it in the background and wait on its completion with whatever waiting facility this harness gives you. Never end your turn while it runs. Waiting is part of the work rather than idleness to yield in: a turn ended with the gate still running is a build that did not finish or a verdict that was not reached, and in a run nobody is watching, nothing comes back to wake the session that ended it.

**Do not go further than the amend.** Do not rewrite what already passes, refactor around the complaint, or build something the ticket left out of its own scope. And never weaken, skip, or delete a test to make the verdict go away: the session that verifies you next has not seen this one and checks the ticket from the beginning, so a test bent to fit the complaint buys nothing and costs the ticket.

**Nobody is watching.** There is no human in this session to ask, and no answer is coming. A genuine decision — an ambiguity the ticket does not settle, a requirement it does not state, a verdict whose complaint the ticket and its thread do not resolve — is not yours to guess. Stop, leave the working tree in a state you can describe, and report the decision you hit and how far you got. An unbuilt ticket costs one ticket; a guessed requirement costs the trust in every ticket the run reports done.

**Commit.** Commit what you changed, on the branch you are already on, and leave nothing uncommitted: work only a working tree holds is work the run cannot integrate. An imperative subject line naming what the amend fixes, and a body saying why rather than what. Follow whatever else the repository's contributing guide and its own recent history show. Do not rewrite, amend, or revert the commit that is already there — what the first builder got right stays where it is. Do not push. Do not merge, do not create a branch, a working tree, or a tag of your own, and touch no branch other than the one you were given.

**Report.** What you changed, what you left undone and why, and anything you had to decide. Your report is not evidence, and neither is the verdict you were given: a third session that has seen neither the builder nor you verifies the work against the ticket's acceptance criteria from the beginning, and its verdict is what counts. So report plainly — an overstated report cannot pass verification, it can only waste the run.
