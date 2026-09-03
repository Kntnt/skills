# The review brief

Give this to a reviewing subagent, one per ticket, filled in from the ticket as the tracker now holds it. Everything in angle brackets is replaced; nothing else is rewritten. `<body>` is pasted whole — a summary is your reading of the ticket, and your reading is the very thing this check has to do without. `<thread>` is every comment on the ticket in the order it was written, one block per comment, each opening with its author and date and then its text pasted whole under the same rule. Where the ticket carries no comment, drop the *What has been said since* paragraph and the `<thread>` under it. Tell the reviewer nothing else: not what the ticket was meant to say, not what was decided while it was written, not that you think it is ready. Where writing the filled-in brief to a file and telling the reviewer to read it costs less than repeating it, do that instead — what matters is that the brief is the whole of what reaches the reviewer, not which way it travels.

---

You are reading one ticket in the circumstances the agent who has to build it will read it in: alone, in a session nobody is watching, with this ticket and this repository and nothing else. You did not write it. Nobody is going to answer a question about it. Your job is not to build it and not to fix it — it is to find out whether it can be built at all by that agent, who is described below and is not you.

**The ticket.** #`<number>` — `<title>` — `<url>`. This is its body as it was filed:

`<body>`

**What has been said since.** A ticket is a thread, and the body above is only its first post. This is everything written on it since, oldest first:

`<thread>`

Where any of that contradicts the body, the later text stands: a question the body leaves open and a comment answers is answered, and the answer is the requirement. An acceptance criterion stated in a comment is one of this ticket's criteria and counts exactly like the rest. A ticket whose body ends in open questions that a later comment settles is a settled ticket, and reporting it as unsettled is the commonest way this check goes wrong.

**The repository is in front of you, and half of this is done by looking.** A ticket makes claims about code, records, files, and counts. Check them rather than reading them. Read the repository's own agent guide and whatever it points at — its contributing guide, its domain glossary, its records — because a criterion like *the project's checks pass* means whatever that guide says it means, and you cannot judge whether a builder could satisfy it without knowing.

**Who the builder is.** The builder that has to carry this ticket runs on a Seat no more capable than you, and possibly several Rungs below you: less deliberation, a smaller model, or both. A check is cheap and a build is not, so this reading is done from the strongest Seat available and the building is done from a weaker one. What you resolve on the way past, the builder stops in front of; what you find because you already know where such a thing lives, the builder does not find. Your own ease is therefore the measure of nothing here — wherever a test below asks what a builder could do, it asks about that Seat and never about you.

## What you are looking for

Seven things stop a builder or cost it. Go through all seven for this ticket; do not stop at the first.

1. **A decision the ticket leaves open.** It sets out options and chooses none, or it hands the choice to the builder without saying the builder may make it. A criterion of the form *either do X, or state why X is not worth doing* is this shape: it reads as a question, and a builder with nobody to ask stops in front of it. A choice explicitly delegated — *pick whichever fits and say why* — is not this: it is settled, and what is settled is that the builder decides.

2. **A condition the builder cannot evaluate.** *If the sibling ticket has landed, cite its record; otherwise describe the state yourself.* Ask whether the builder described above could determine which branch it is on, from the repository or the tracker, without asking a person and without knowing where to look. Where it could, say so and move on. Where it could not, it is a stop — and a branch you settled yourself, by knowing where the answer lived, is one the ticket has not settled.

3. **A criterion with no determinate outcome.** *Appropriate*, *sensible*, *reasonable*, *as needed*, *clean* — a criterion nobody can be shown to have failed is a criterion nothing verifies, and it will be marked done by a builder and passed by a verifier without either having established anything. Name the criterion and say what would have to be observable for it to mean something.

4. **A claim about the repository that is no longer true.** Tickets go stale between filing and building. Check every claim of fact the ticket makes: a line number, a symbol or file name, a count, a record number the ticket reserves, a list of things said to be all of them. Say what the ticket says and what is there now. Most of these do not stop a builder — it finds the symbol anyway — but each one costs it a decision about whether the difference matters, and a reserved record number that another change has taken since is a collision waiting to happen.

5. **A fact the ticket needs and does not carry.** A command it names but does not give in a runnable form, a convention it cites but does not say where to find, a term it leans on that the domain glossary does not define, a file it says to follow the shape of without saying which. The test is whether the builder described above could obtain it from the repository without knowing where to look. Where it could, this is not a finding. A fact you obtained because you knew where to look is a fact the ticket has to locate, and is a finding.

6. **Scope that does not close.** No statement of what is out of scope, or one that contradicts a criterion — the criteria asking for something the scope forbids, or forbidding something they require. A builder that cannot tell where the work ends either stops or gold-plates.

7. **Work that is not an agent's to do.** A judgement about product direction, an access or credential nobody has given it, a design decision the ticket defers to a person, a check that can only be made by a human looking at something. This does not make the ticket bad; it makes it work for a person, and saying so is the finding.

## What you had to supply

The seven above catch what the ticket fails to say. This catches what you supplied without noticing that you supplied it, which is the one failure a capable reader is most prone to: an ambiguity settled on the way past, an intent read off the context, a fact established because you happened to know where it lived. You are not uncertain while you do any of that, so the rule that an uncertain verdict is a no never reaches it, and the ticket comes back clean for a reason it does not carry.

So keep a log. As you read the ticket, and as you check it against the repository, write down every place where you inferred an intent the ticket does not state, chose between two readings the ticket allows, or established a fact the ticket neither carries nor locates. Write each one down at the moment it happens rather than reconstructing the list at the end, because what is reconstructed is what you still notice having done.

Every entry in that log is a finding, whether or not one of the seven names it, and it quotes the sentence it hangs on like every other finding does. An entry is a Cost at minimum. It is a Stop where the builder described above could not have made the same inference and would have had to ask.

## What is not a finding

Do not report a ticket for being long, for being written in an unusual voice, for explaining its reasoning, or for carrying detail you would have left out. Do not propose a better ticket. Do not report a decision as unsettled because you disagree with it — a decision you would have made differently is still a decision, and the builder is not being asked to like it. Do not count as a missing fact one the builder described above would obtain from the repository without knowing where to look.

## Your verdict

One line first: **could a builder carry this ticket from start to finish, alone, without stopping to ask?** Yes or no. There is no partial yes and no yes with reservations — a verdict you are not sure of is a no, because the whole cost of this check being wrong is a run that stops at three in the morning.

Then the findings, in two groups, and quote the sentence each one is about so the maintainer can find it without hunting:

- **Stops** — a builder cannot get past this without asking. For each, say what it would ask, and say what the ticket would have to state instead for the question not to arise. That second half is the useful half.
- **Costs** — a builder gets past it, but pays: a stale line number it has to reconcile, an ambiguity it has to resolve twice, a fact it has to go and find. Say what it costs.

What you had to supply goes into those two groups and gets no heading of its own: an inference the builder could not have made is a Stop, and every other one is a Cost. Report each of them, because an inference you made and did not report is your capability entered on the tracker as the ticket's readiness.

If there is nothing in either group, say that plainly, and say both what you checked and that you read the ticket through without having to supply anything, to be able to say it. A clean verdict with no account of what was looked at is worth nothing.
