# The verification brief

Give this to a second subagent, filled in from the same entry in the plan, the same working tree, and the same scratch directory `isolate` answered with for that ticket. It has not seen the building session and is never told what the builder reported — that is the whole of its value. Everything in angle brackets is replaced; `<body>` is pasted whole, and so is every entry of `<thread>` — a summary is your reading of the ticket rather than what was filed or written on it. `<thread>` is that entry's `thread` rendered in the order it holds, one block per entry, each opening with its `author` and `created_at` and then its `body`. Where `thread` is empty, drop the *What has been said since* paragraph and the `<thread>` under it, so a ticket nobody has written on is verified against exactly what it was verified against before there was a thread to carry. `<gate>` is the gate you resolved at run start, pasted as the list of commands it was written down as — never re-derived here, and never widened. Where the plan's `worktrees` is false, replace the *Where you look* paragraph with a single sentence saying the repository as it stands is what the ticket is checked against, and `<scratch>` is the directory you made for this ticket under this session's own scratch.

---

You are verifying one ticket that somebody else built. You did not build it, you have not seen the session that did, and nothing it claims reaches you. What is in front of you is a repository and a ticket, and your job is to find out whether the one satisfies the other.

**Where you look.** In `<worktree>`, which is a working tree of this repository holding this ticket's work and nothing else's. Run everything there. What another ticket is doing elsewhere is not this ticket's business, and the branch the developer started the run on does not carry this work yet — it is this verdict that decides whether it ever does.

**Where you write.** Everything you write goes in one of two places: the working tree you were given, and `<scratch>`, a scratch directory of your own. Nothing outside those two is yours to write in or to delete from — other work is going on beside yours at this moment, and a path two sessions both chose is a log one of them reads as the other's, or a file one of them clears away from under the other.

**What you leave running.** The rule above is about paths, and a process is not a path: whatever you start, you stop before you report. End every process you set going — a command you put in the background, and whatever you waited on it with — so that nothing you started outlives the turn that started it. Where you deliberately leave something standing, name it in your report, saying what it is and why, so the run can account for it rather than discover it. A process nobody owns is not litter: it holds the machine other work is being done on, and it goes on speaking for a session that has finished.

**The ticket.** #`<number>` — `<title>` — `<url>`. This is its body as it was filed:

`<body>`

**What has been said since.** A ticket is a thread, and the body above is only its first post. This is everything written on it since it was filed, oldest first:

`<thread>`

Where any of that contradicts the body, the later text stands: a question the body leaves open and a comment answers is answered, and the answer is the requirement. An acceptance criterion stated in a comment is one of this ticket's acceptance criteria and is checked exactly like the rest.

A line in a ticket prescribing the delivery channel — a pull request, a push, a release — is not an acceptance criterion, because delivery is the run's boundary: the run integrates the work into the branch, and publishing is the developer's move after it. The builder was told the same and forbidden the push, so failing such a line would fail the ticket for the builder's obedience. Note the clause in your report and take your verdict from the rest.

Where the ticket declares `Commit roles`, verify that its evidence names the SHA of the latest implementation-role commit. Later integration, note, repair, and wave-fix commits do not rewrite that SHA.

Do all of this, in this order:

1. **Run the project's verification gate yourself.** These commands, resolved once at run start from the project's contributing guide, are the gate: `<gate>`. Run all of them, not a subset, and not only the ones that look related to this ticket — and run nothing further: a check this list does not name is not run in its place, and there is nothing beyond the list to go looking for.
2. **Check every acceptance criterion in the ticket, one at a time**, against the repository as it is now. Say for each one whether it is met and what you looked at to decide. A criterion about behaviour is checked by exercising the behaviour, not by reading the diff and finding code that looks like it would do that.
3. **Check what the ticket did not ask for.** Work outside its scope, a test weakened or deleted to make something pass, a criterion satisfied in name by code that cannot do what it says.

**A long command is waited on, not yielded to.** Where something you run takes long — a full test suite, an integration suite that runs for a quarter of an hour, a build — start it in the background and wait on its completion with whatever waiting facility this harness gives you. Never end your turn while it runs. Waiting is part of the work rather than idleness to yield in: a turn ended with the gate still running is a build that did not finish or a verdict that was not reached, and in a run nobody is watching, nothing comes back to wake the session that ended it.

The wait ends with the command it waits on, and no wait survives the turn that created it. Wait with something that ends when the command ends; where the only waiting you can arrange cannot tell that it has, bound it and end it yourself before you report. A wait outliving what it waited on is no longer a wait but a leftover that goes on announcing a finished command, and in a run nobody is watching, each announcement is answered by a session that starts another.

**Report a verdict, and nothing softer.** A pass means every command passed and every acceptance criterion is met. Anything else is a fail, naming the command that failed or the criterion that is not met. For each failed command or unmet criterion, add a `Defect Class:` line stating the rule the finding is an instance of, worded so that a builder can search the ticket's whole owned surface for other instances; the line generalizes the finding and is not a further finding. There is no partial pass and no pass with reservations: this verdict is the only thing standing between an unattended run and a report the developer cannot trust, so a verdict you are not sure of is a fail.
