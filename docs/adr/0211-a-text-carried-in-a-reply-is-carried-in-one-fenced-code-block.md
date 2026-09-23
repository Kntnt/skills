# A text carried in a reply is carried in one fenced code block

This record decides how a response carries a Text Artifact. The shared delivery contract, [`delivery.md`](../../skills/kntnt/library/references/delivery.md), said where a result goes and was silent on how the reply holds it, so each run answered that for itself; it now states the answer in a section of its own, and Write, Redline, Unslop and Proofread deliver by it. `delivery.md` is where the rule is, and this record is why it has this shape (issue #384). It extends [ADR-0178](0178-how-a-text-is-written-reviewed-and-delivered.md), *Where a result goes*, which settled the destination and the response's contents and never the response's form.

## The silence was not neutrality, and sixteen replies show what it produced

**Every saved Redline reply carrying a `kntnt` map under `docs/evaluation/editorial-362/runs/` and `docs/evaluation/editorial-377/runs/` was read, and the sixteen of them carry the artifact three ways.** Nine open it with a fence naming `markdown`, three with a bare fence, and four with no fence at all. No run disobeyed anything: the contract had settled that a response-targeted run delivers the complete artifact in the response, and left the carriage of it to whatever the surrounding context made salient.

**One of the four unfenced replies came back with its frontmatter block broken.** `column-sv-r2` opens with a paragraph of the run's own Swedish prose, a blank line, `---`, a blank line, and then `kntnt:`. The input it was given, `work/input.md`, opens `---` and then `kntnt:` with nothing between them. What the reader of the delivered text now has is a horizontal rule followed by a paragraph of YAML, and the run's own judgement recorded it as formatting damage the account never mentioned.

**The other three unfenced replies escaped by a margin of one line.** Two of them set the `---` after a blank line and put `kntnt:` immediately beneath it, and the third begins the reply with the artifact itself. Their frontmatter bytes are intact because the blank line landed above the delimiter rather than below it. That is the whole of the difference between the damaged reply and the ones beside it, and it is not a difference any run was asked to get right.

## Markdown is where the silence costs, and the cost is not a slip

**Three hyphens directly beneath a line of text are a heading marker, and after a blank line they are a horizontal rule.** A run about to set an artifact opening on `---` under a paragraph it has just written is looking at the one position in Markdown where a frontmatter delimiter, a setext heading underline and a thematic break are the same three characters. Adding a blank line is what a competent writer of Markdown does there, and it is also exactly what stops a frontmatter block from being one.

**So the defect is the shape of the reply rather than a step inside the Skill.** Redline synchronises the `kntnt` map, hands the whole text including frontmatter to Proofread, and forbids anything substantive afterwards; any of the three could have been where the line went in, and the evidence cannot tell them apart. Chasing it further would settle which step improvised the answer and leave every other run free to improvise a different one. A fence removes the position in which the question arises at all.

## A fence rather than a file, and what the fence costs

**The live alternative was to write every text to a file and put a path in the reply.** It is the stronger guarantee — a file cannot be run together with the words about it — and it was set aside for what it takes away: a response-targeted run changes nothing on disk, which is the property the default was built around and the reason a caller can ask for a text without authorizing a write.

**What the fence costs is the rendered text.** A caller who wanted to read the Swedish column reads it as source now, monospaced and unstyled, and a caller who wanted to copy it out gets exactly the bytes the run settled. That second thing is what was bought: byte fidelity from the run to the reader, and a boundary a later Skill or a script can find without guessing where the run's prose stopped.

**The two mechanical properties exist because the general case has them.** The fence is longer than the longest run of backticks inside the artifact, or a text carrying fenced code of its own closes the delivery early and the rest of it leaves the block — the failure the naive three-backtick fence has, on exactly the texts this collection is written for. The info string names the format, because a block with no info string says only *this is not prose*, and the nine runs that reached for `markdown` unprompted were answering a question a reader really has.

## Which side of the fence a thing belongs on

**What the run says about the text is the reply's own words and stays outside.** The resolved configuration, the findings and which are unresolved, the claim account, where a technique came from, what the run could not do. Putting any of it inside would place words the text never had inside the text, which is the same defect as the one this record is about, with the damage running the other way.

**What the run settled as part of the document stays inside.** The Handoff Metadata is part of the artifact — it is the `kntnt` map whose breakage started this — and so are markings the user asked to have placed in the document itself, which issue #376 shipped and this does not retract. The test is not whether the run wrote it but whether it is the document as delivered.

## It reaches a text the contract never called delivered

**A stopped Write run carries its complete prose in the reply without delivering it.** The prose is preserved, marked as not source-checked, and handed to a user who has to be able to reach it once the session is over — which is to say it is a complete text carried in a reply, with the run's own account of what it has not been through beside it. A rule scoped to what the contract calls *delivered* would leave that text, of all texts, carried as bare prose.

**So the rule is written about what a reply carries rather than about what a run delivers**, and `source-check.md` points at it rather than answering for itself. The short no-change status is the one reply that carries no text at all, and it carries no fence; an explicit destination and In-place Editing receive the text itself, a fence being how a reply holds a text apart from its own words and a file having no words of its own to be held apart from.

## What this leaves unmeasured

**Nothing here establishes that the three Skills obey the rule in the general case.** The regression packet at [`docs/evaluation/regressions/384/`](../evaluation/regressions/384/README.md) puts six runs on one Swedish column and checks one thing mechanically: that the fenced text's frontmatter block is byte-identical to the input's. Write is bound by the same contract and is measured on its own corpus by issue #380.

**And the fence is a rule a body obeys rather than a check anything enforces.** That is what the whole of `delivery.md` costs, for the reason ADR-0178 gives: the suite can hold the document's placement, its silence about flag spellings and the presence of the rules a consumer depends on, and whether a run obeys it is visible only in that run's output.
