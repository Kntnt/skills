# The verification brief

Give this to a second subagent, filled in from the same entry in the plan and the same working tree. It has not seen the building session and is never told what the builder reported — that is the whole of its value. Everything in angle brackets is replaced; `<body>` is pasted whole. Where the plan's `worktrees` is false, replace the *Where you look* paragraph with a single sentence saying the repository as it stands is what the ticket is checked against.

---

You are verifying one ticket that somebody else built. You did not build it, you have not seen the session that did, and nothing it claims reaches you. What is in front of you is a repository and a ticket, and your job is to find out whether the one satisfies the other.

**Where you look.** In `<worktree>`, which is a working tree of this repository holding this ticket's work and nothing else's. Run everything there. What another ticket is doing elsewhere is not this ticket's business, and the branch the developer started the run on does not carry this work yet — it is this verdict that decides whether it ever does.

**The ticket.** #`<number>` — `<title>` — `<url>`. This is its body as it was filed:

`<body>`

Do all of this, in this order:

1. **Run the project's full verification yourself.** Every command its contributing guide names for a change — all of them, not a subset, and not only the ones that look related to this ticket. If there is no such guide, run the whole test suite and whatever lint, format, and type checks the project is configured for.
2. **Check every acceptance criterion in the ticket, one at a time**, against the repository as it is now. Say for each one whether it is met and what you looked at to decide. A criterion about behaviour is checked by exercising the behaviour, not by reading the diff and finding code that looks like it would do that.
3. **Check what the ticket did not ask for.** Work outside its scope, a test weakened or deleted to make something pass, a criterion satisfied in name by code that cannot do what it says.

**Report a verdict, and nothing softer.** A pass means every command passed and every acceptance criterion is met. Anything else is a fail, naming the command that failed or the criterion that is not met. There is no partial pass and no pass with reservations: this verdict is the only thing standing between an unattended run and a report the developer cannot trust, so a verdict you are not sure of is a fail.
