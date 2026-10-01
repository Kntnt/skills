# The reply check

Give this to a subagent started fresh once step 9 has produced the final Text Artifact and the reply is drafted, before anything is delivered. It runs on every run whose reply says anything about a text, which is every run except one that returns only the short no-change status. Everything in angle brackets is replaced; nothing else is rewritten.

`<received>` is the Text Artifact as it arrived, pasted whole, frontmatter included. `<delivered>` is the final Text Artifact step 9 produced, pasted whole. `<reply>` is the reply as drafted, pasted whole: every finding, the claim account, the closing paragraph and every other sentence it will deliver, leaving out only the delivered text where the reply carries it. `<measurement>` is, for `article`, `casestudy`, `column`, `opinion` and `pressrelease`, the full output of step 6's command run on the delivered text, as step 11 says, pasted whole; for any other genre, drop the paragraph headed **The measurement of the delivered text** and the placeholder under it. `<library>` is the Collection Library path this run resolved.

Tell the subagent nothing else. Not the review's reasoning, not the rounds or what any of them attempted, not why any change was made, and not this Skill's own instructions: the checker is a reader who knows what the reader of the reply will know, the two texts and what the reply says of them, and that is what lets it see what a change did beyond what it was meant to do. Hand the filled-in brief to the subagent directly, as the whole of its instruction, and never as a file whose path you send in its place: it holds the user's text twice, and a file is a name another process can read, replace or delete while the check runs.

**What you do with what it returns.** The subagent returns two lists. Act on every item of both, and correct only the reply:

- A statement on the first list is rewritten so that it is true of the text it names, or left out, as *The truth of a report about the text* in `$LIBRARY/references/delivery.md` says. A count or length about the delivered text takes its figure from the measurement you handed over.
- A difference on the second list is added to the claim account, or its entry completed, the way step 11 reports a removed, changed or added claim. Anything the reply says about the claims as a whole that the new or completed entry contradicts is narrowed to what holds, or left out.

The list is a check of the reply, not a note of what a correction did, so the closing paragraph is still built from your own comparison of the two texts, and is corrected from the list like every other statement. The text is not touched: the Text Artifact step 9 produced is delivered as it is, and step 10 holds. The check is made once, and the corrected reply is delivered without being checked again.

---

You are checking one reply against the two texts it describes. You did not write the reply and you did not make the changes it reports; you know only what is below, which is what the reply's own reader will know. Find what the reply gets wrong about the texts, and only that: whether a change was a good one, whether a finding was worth making and how the text reads are questions for somebody else.

**The text as it arrived.** This is the complete text the run received:

`<received>`

**The text as delivered.** This is the complete text the run delivers:

`<delivered>`

**The reply.** This is everything the run is about to say about the two texts:

`<reply>`

**The measurement of the delivered text.** This is the full output of the collection's measuring script, run on the delivered text. A count or length the reply states about the delivered text is read against it:

`<measurement>`

**The duties the reply is held to.** Before you read the reply, read two passages and apply them as written: the section *The truth of a report about the text* in `<library>/references/delivery.md`, and the sentences of `<library>/references/editorial/base.review.md` that say what the claim account holds, from *A claim removed because the finding named that claim itself* to the end of that paragraph. Read nothing else of either file, and no other file.

**First compare the two texts yourself**, passage by passage, frontmatter and headings included, and note every difference, before you read what the reply says about them. The reply's own account is what you are checking, so it is never how you find a difference.

**Then return two lists.**

1. **False statements.** Every statement of the reply that the text it names contradicts, read as *The truth of a report about the text* reads it: a statement about the text as it arrived against that text, and every other statement against the delivered text. A finding's description of a passage, a count, a length, a grammatical label, where a passage stands, what a round did to a passage, a statement that something holds everywhere or nowhere, and every entry and sentence of the claim account are statements the text can contradict. A judgement of quality — that a heading was vague, that a passage read as filler — is not. For each: quote the statement, name the text it is about, quote the passage that contradicts it, and say what is true.
2. **Claim changes the account misses.** Every difference between the two texts that moves a claim and that the claim account leaves out, or reports short of what it did: scope narrowed or widened; a condition, a qualification, a limit or a connective lost; chronology, causality or attribution moved; or the meaning moved, a sense or a double sense lost and an actor, an ordering or a framing added among it. A headline, a standfirst and a subheading carry claims like any other passage. A sentence that says whose a body of content is — that a person tells it, that a document shows it — carries an attribution for all of that content, wherever the content itself stands: where the delivered text gives a person or a source content that the text as it arrived gave to another voice, the narrator's own among them, the attribution has moved even though every fact still stands where it stood. A statement on your first list that gets wrong whose a passage's content is may have a change built on it: read what the delivered text now says about whose that content is, and put that change on this list where the account reports it short. For each: quote the passage before and after, say what the difference did to the claim — for a moved attribution, who the text gave which content to before and whom it gives it to now — and quote what the account says of it, or say that it says nothing. An entry that names one of the voices a moved attribution took content from, and leaves out another, reports it short.

Write `none` under a list with nothing on it. Return the two lists and nothing else, and write no file.
