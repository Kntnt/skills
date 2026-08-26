# The Frame Record

A Frame Record is the file `/frame` writes when it maps a task, and the file `/to-slices` reads when it produces the decision document and the tickets. This document is the contract between them: the record's seven sections, what each holds and what a consumer may rely on from it, where the file lives, and how long it lives. It is written once here and belongs to neither end, because a format one Skill owned would be one Skill owning another's input contract.

What is fixed here is what a writer puts in a section and what a reader is therefore entitled to find there. How a record is written during a framing, how an unfinished one is resumed, and how an unconsumed one is discarded are behaviours of the Skill that writes it, stated in that Skill's own shipped documents.

## The shape of the file

One Markdown file, `#` title naming the task, then these seven headings in this order and with these words:

```
## 1. Task
## 2. Frames
## 3. Findings
## 4. Decided by the owner
## 5. Decision ledger
## 6. Open
## 7. Knowledge written
```

All seven are present in every record, whether or not they have entries. A section standing empty is itself an answer — nothing was needed there — and it is why a consumer never has to tell an empty section from a missing one.

Entries are prose — a bulleted entry where the section has several of one kind, a short paragraph where it has one thing to say. Nothing here fixes a field syntax: the reader is an agent, and what it needs is that the section it opens holds what this document says it holds.

**An address is what makes an entry checkable, and it is written the same way everywhere.** A repository path, with a heading or a line where the file is long enough that a path alone sends the reader hunting; a commit where the thing was read from history; a URL where it came from outside the repository. Sections 2, 3 and 7 carry addresses on every entry, and a consumer may re-read any of them instead of trusting the paraphrase beside it.

## The seven sections

### 1. Task

The task in the owner's own words, and the commit the framing was made against.

The words are the owner's rather than the Skill's restatement of them, so that a consumer synthesising the work is answerable to what was asked and not to an interpretation already one step away from it. The commit is the tree every finding in section 3 was read from, and is what tells a later reader how old those findings are.

A consumer may rely on both being present, and on nothing else in this section: the task is stated, not analysed. It may not rely on the commit still being the tip — a record outlives the tree it was written against, which is why the durable layer built from it carries no code excerpts and no line numbers.

### 2. Frames

What binds, each with the address it was read from: the repository's always-loaded file, the rule modules the task actually touches, the glossary it keeps, and how it verifies itself.

These are the standing constraints every later decision was checked against, and they are the reason a decision in section 5 could be taken without asking anybody. A frame is quoted or stated closely enough to be applied, and carries its address so a consumer can open the source rather than inherit a summary.

A consumer may rely on this section being the complete set of constraints the framing worked inside, and on every entry in section 5 naming one of them. It is also what a consumer checks its own output against: work proposed outside these frames is work nobody established was allowed.

### 3. Findings

What the codebase answered, each with the address of its evidence.

A finding is an answer, not raw material: the files, the search results and the history a recon pass read stayed in the context that read them, and what reaches the record is the direct answer with the minimal evidence supporting it. A finding whose coverage was incomplete says so, and an anomaly the recon met is a finding of its own.

A consumer may rely on every finding being checkable at the address it carries, on the answer being as of the commit in section 1, and on findings being findings rather than decisions. That a seam exists is a finding; that the tests will be written at it is not, and no such choice is made here.

### 4. Decided by the owner

Every question the owner was asked and every answer they gave, verbatim.

Verbatim is the whole point of the section. The answer is the owner's judgement, and a paraphrase is the Skill's judgement wearing the owner's name — the one substitution this record exists to prevent. A question is kept with its answer, so a reader sees what was actually put to them, including the recommendation they accepted or passed over.

A consumer may rely on everything here having been asked of the owner and answered by them, and on nothing here being the Skill's. It is the section a consumer may quote and build on without checking back, and an answer here outranks every entry in section 5.

### 5. Decision ledger

Every decision the Skill took in the owner's stead, numbered.

Each entry carries four things: the choice, the alternative it passed over, the reason, and the frame from section 2 it was decided under. The numbers exist so a veto can name one; they are stable for the life of the record and are not reused, so a number quoted in conversation or in a later document goes on meaning what it meant.

An entry the owner vetoed stays where its number will still find it and says that it was vetoed. A veto turns the point back into a question, and where the question was then settled is section 4, among the owner's own answers.

A consumer may rely on each entry having been taken inside a stated frame rather than by preference, and on every entry not marked vetoed being a decision in force.

### 6. Open

What is deliberately unanswered: each entry with who owns it and what would answer it.

Deliberate is what separates this section from an unfinished record. An entry here is a point the framing knowingly left open — most often a question only an experiment can answer, in which case what would answer it is the experiment, described closely enough for a consumer to sequence it as work of its own.

A consumer may rely on every entry naming an owner and a way to close it, so that an open point becomes something to schedule rather than something to ask about. An empty section says the framing left nothing open, not that it forgot to look.

### 7. Knowledge written

The glossary terms and the records this framing added to the target repository, with their addresses.

Knowledge is written as it crystallises, into the repository's own durable layer, so this section is not a copy of it — it is the list of what was written and where. Terms pinned down during the framing and decision records the framing earned are both here; a ledger entry that never became a record is not, and belongs to section 5 alone.

**This section is a manifest, and it is the only one.** Two duties are performed against it and neither is possible without it. A framing thrown away takes its section 7 with it as an offer, entry by entry, which is the one moment a framing's knowledge can be withdrawn against a list instead of guessed at. And after the work lands, the knowledge a framing wrote is checked against what the implementation actually did and corrected where the two diverge, against this same list.

A consumer may rely on it listing everything durable the framing wrote outside the record itself. Because that makes it the only complete list, a consumer that deletes the record carries what section 7 names into the durable layer it publishes — deleting the manifest without carrying it forward strands the reconciliation the list exists for.

## The degenerate case is a complete record

A record whose section 4 has no entries and whose section 6 is empty is a simple task, framed without a single round: nothing had to be asked, and nothing was left open. That is a complete record and a consumer treats it as one.

Nothing in this format sets a floor. Section 5 may be empty too, and section 3 may hold few findings on a task the codebase had little to say about. Completeness is the seven sections being present and each holding what this document says it holds — never volume, and never evidence that the framing worked hard.

## Where a record lives, and how long

**Untracked, at `.kntnt/frames/<slug>.md` in the repository being framed.** One file per framing, the slug naming the task. The record is a working artifact and not the layer meant to be read later: what is built to be read later is the decision document its consumer publishes, and a tracked record would set a second account of the same decisions beside it.

**A record is a baton rather than an archive.** Its consumer deletes it once the decision document and the tickets are published. By that moment everything durable has moved into layers built to last — the tracker, the glossary, the archive — and a record kept past it is a stale second telling of decisions those layers now hold, competing with them for a later reader's trust.

**A record nobody consumed is still a record.** It survives the session that wrote it, and nothing in this format expires. What becomes of a record no consumer ever takes up belongs to the Skill that writes it.
