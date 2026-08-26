# The correction brief

Give this to a subagent started fresh for one correction, filled in from the run as it now stands. Everything in angle brackets is replaced; nothing else is rewritten.

`<text>` is the current Text Artifact pasted whole — the text as it stands after every correction so far, never the text as it arrived and never an extract of it. `<findings>` is every finding of the most recent review, in the order it was recorded, each pasted whole under the same rule. `<genre>`, `<technique>` and `<language>` are the values the run resolved, written as the resources are named; write `none` for `<technique>` where no technique was resolved, and drop the sentence naming its resource with it. `<library>` is the Collection Library path this run resolved.

Tell the subagent nothing else. Not what an earlier round found, not what an earlier correction attempted, not which findings you think matter most, and not your reading of what the text is trying to do — that reading is the thing a fresh subagent is dispatched to be without.

Hand the filled-in brief to the subagent directly, as the whole of its instruction, and hand it over no other way. Never write it to a file and send a path in its place: this brief holds the user's text entire and every finding standing against it, and a file is a name some other process can read, replace, or delete for as long as the round lasts. A long text makes a long brief, and a long brief is passed whole anyway — trimming it, summarising it, and pointing at it are the three things this brief exists to rule out.

---

You are making one correction to one text. You have not seen this text before, and there is nothing you are expected to remember: the text below is its current state, and the findings below are the current review's, complete and as they were written. Repair them.

**The text.** This is the complete Text Artifact, exactly as it now stands:

`<text>`

**The findings.** This is every finding the review recorded against that text, complete and in the order it recorded them:

`<findings>`

**The contract.** The text is a `<genre>` in `<language>`, and it is held to `<technique>`. Read what it is held to before you change anything: `<library>/references/editorial/base.md` and `<library>/references/editorial/base.review.md`; `<library>/references/editorial/genres/<genre>.md` and the `.review.md` file beside it where one exists; `<library>/references/editorial/techniques/<technique>.md` and its `.review.md` the same way; `<library>/references/editorial/anti-slop.md`; and the `composition`, `review` and `anti-slop` scopes of the resolved language, which `uv run "<library>/scripts/languages.py" resolve --scope=composition --scope=review --scope=anti-slop "<language>"` returns. A review extension that is not there is not a defect. Load no mechanics guidance and correct no spelling, punctuation, or grammar: a mechanical pass runs after you, and work you do there is work done twice.

**What you change, and what you preserve.** Repair what the findings name and nothing else. Preserve everything the findings do not concern: every sentence, every fact, every quotation, every code sample, every heading, every piece of formatting and every line of frontmatter among them comes back exactly as you received it — a repair that improves a paragraph nobody complained about is a change nobody asked for and nobody will review. A code sample — a fenced block, an indented block, or an inline code span — is quoted material rather than the text's own prose: its contents are read past rather than read against the rules, so nothing inside one is a finding and nothing inside one is changed, the docstrings, comments, and string literals among them. Prose about code is ordinary prose and is read like every other sentence. Where a finding can be repaired several ways, make the smallest change that removes it. Where a finding names something you cannot repair without inventing a fact, changing what the text claims, or altering a quotation's meaning, stance, certainty or distinctive wording, leave that passage alone and say so: this text is answerable to material you do not have, and a plausible invention is worse than an unrepaired finding.

**What a repair may take with it, and what it may not.** A finding names a defect, and what a repair removes is that defect. Where the defect a finding names is the whole of the passage — an opening that would sit in front of any text, a closing that restates what the reader has just read, a claim credited to nobody that the text cannot source — cutting the passage removes the defect and takes no claim with it, and cutting it stays the repair. Where the passage carries a claim beside the defect — a fact, an observation, the point the passage exists to make — the smallest change is the one that leaves that claim standing, and deleting the passage entire is not that change. And where you can see no way to remove the defect that does not take the claim with it, leave the passage alone and say so, exactly as you would a finding you cannot repair without inventing a fact: a person can give that claim what it needs or let it go, and a round that deletes it leaves them nothing to weigh. That judgement is about the passage in front of you and never about how much of the text is left — a short text is no licence to leave a finding standing, and a long one is no licence to go on cutting.

**What you return.** The complete corrected text and a short note of which findings you repaired and which you left, with the reason for each you left. The complete text: not a diff, not the changed passages, not a description of what you did. Return no commentary inside the text itself.
