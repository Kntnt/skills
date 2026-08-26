# The correction brief

Give this to a subagent started fresh for one correction, filled in from the run as it now stands. Everything in angle brackets is replaced; nothing else is rewritten.

`<text>` is the current Text Artifact pasted whole — the text as it stands after every correction so far, never the text as it arrived and never an extract of it. `<findings>` is every finding of the most recent pass, in the order it was recorded, each pasted whole under the same rule. `<language>` is the language the run resolved, written as the resources are named. `<library>` is the Collection Library path this run resolved.

Tell the subagent nothing else. Not what an earlier round found, not what an earlier correction attempted, not which findings you think matter most, and not your reading of what the text is trying to do — that reading is the thing a fresh subagent is dispatched to be without.

Hand the filled-in brief to the subagent directly, as the whole of its instruction, and hand it over no other way. Never write it to a file and send a path in its place: this brief holds the user's text entire and every finding standing against it, and a file is a name some other process can read, replace, or delete for as long as the round lasts. A long text makes a long brief, and a long brief is passed whole anyway — trimming it, summarising it, and pointing at it are the three things this brief exists to rule out.

---

You are making one correction to one text. You have not seen this text before, and there is nothing you are expected to remember: the text below is its current state, and the findings below are the current pass's, complete and as they were written. Repair them.

**The text.** This is the complete Text Artifact, exactly as it now stands:

`<text>`

**The findings.** This is every finding the pass recorded against that text, complete and in the order it recorded them:

`<findings>`

**What the findings are.** They are anti-slop findings and nothing else. Read what they are read against before you change anything: `<library>/references/editorial/anti-slop.md`, and the anti-slop guidance of the resolved language, which `uv run "<library>/scripts/languages.py" resolve --scope=anti-slop "<language>"` returns. The text is in `<language>`, and each pattern is applied by what it does in that language rather than by the English words the catalogue writes it with. Read nothing else and load no wider editorial guidance: this text is otherwise finished, and a repair made against rules the pass never applied is a change nobody asked for. Correct no spelling, punctuation, or grammar either — a mechanical error is a separate gesture the caller has not made.

**What you change, and what you preserve.** Repair what the findings name and nothing else. Preserve everything the findings do not concern: every sentence, every fact, every quotation, every heading, every piece of formatting and every line of frontmatter among them comes back exactly as you received it — a repair that improves a paragraph nobody complained about is a change nobody asked for and nobody will review. Where a finding can be repaired several ways, make the smallest change that removes it, and prefer removing the pattern to replacing it with a better version of itself. The writer's vocabulary, bluntness, humour, admitted uncertainty, and rhythm are what makes the text theirs; a pass that tidies all of it into even prose has replaced one machine voice with another. Where a finding names something you cannot repair without inventing a fact, changing what the text claims, or altering a quotation's meaning, stance, certainty or distinctive wording, leave that passage alone and say so: this text is answerable to material you do not have, and a plausible invention is worse than an unrepaired finding.

**What a repair may take with it, and what it may not.** A finding names a pattern, and what a repair removes is that pattern. Where the pattern a finding names is the whole of the passage — an opening that would sit in front of any text, a closing that restates what the reader has just read, a claim credited to nobody that the text cannot source — cutting the passage removes the pattern and takes no claim with it, and cutting it stays the repair. Where the passage carries a claim beside the pattern — a fact, an observation, the point the passage exists to make — the smallest change is the one that leaves that claim standing, and deleting the passage entire is not that change. And where you can see no way to remove the pattern that does not take the claim with it, leave the passage alone and say so, exactly as you would a finding you cannot repair without inventing a fact: a person can give that claim what it needs or let it go, and a round that deletes it leaves them nothing to weigh. That judgement is about the passage in front of you and never about how much of the text is left — a short text is no licence to leave a finding standing, and a long one is no licence to go on cutting.

**What you return.** The complete corrected text and a short note of which findings you repaired and which you left, with the reason for each you left. The complete text: not a diff, not the changed passages, not a description of what you did. Return no commentary inside the text itself.
