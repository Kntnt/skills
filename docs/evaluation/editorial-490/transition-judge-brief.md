# Correction judge brief

You judge one step of one run of a reviewing Skill. The Skill received a text, reviewed and corrected it, and drafted a reply reporting what it found and what it changed. Before delivering anything it handed the two texts and the drafted reply to a separate checker, which returned a list of what it found wrong in the reply. The Skill then corrected its reply and delivered it. You judge that last step: what happened to the reply between the draft the checker read and the reply that was delivered.

The run directory named in the message that sent you here holds five files. Read exactly those, and nothing else — no other run, no repository file, no ticket. You are not told how the Skill or the run was configured, which version of it ran, or which model produced the reply, and you must not guess or try to find out.

- `input.md` — the text as it arrived.
- `delivered.md` — the text as delivered, as the checker was handed it.
- `draft.md` — the reply as drafted, which is what the checker read.
- `check.md` — what the checker returned.
- `response.md` — the reply as delivered, without the delivered text.

## What a statement about a text is

The reply says things about two texts. A statement about the text as it arrived is read against `input.md`; every other statement is read against `delivered.md`. A statement is **false** where the text it names contradicts it. That covers a finding's description of a passage, a quotation, a count, a length, a grammatical label, where a passage stands, what a change did to a passage, a statement that something holds everywhere or nowhere, every entry of an account of what happened to the text's claims, and what the reply says a passage asserts, denies or leaves open — who it credits, what it says caused what, and how certainly. A passage that declines to credit something with a result has not said that it did not cause it, and a passage that says it did not has not left the question open; a statement that reports one as the other is false. A judgement of quality is not a statement the text can contradict. The checker can be wrong too: judge every statement against the texts, never against what `check.md` says of it.

## What to write

Write `judgement-<your letter>.md` in the run directory, with the letter the message gave you. Answer every heading.

**1. The checker's items.** Every item `check.md` lists, one at a time: quote it, and say what `response.md` did with it — **corrected** (the statement now says what is true of the text it names, or the account now carries what the item said it lacked), **left out** (the statement is no longer in the reply), or **not handled** (the statement or the gap is still there). Quote what `response.md` says in its place. Where the item itself is wrong about the texts, say so, and say whether `response.md` followed it into a false statement. Write `none` where `check.md` lists nothing.

**2. What changed after the check.** Compare `draft.md` with `response.md` sentence by sentence. List every statement about either text that `response.md` makes and `draft.md` does not make in the same words — reworded, split, merged, moved into another statement or added — ignoring changes of formatting alone, such as bold type, a list marker or a heading level. For each: quote it, quote the sentence of `draft.md` it replaces or write `added`, say whether an item of `check.md` called for the change, and say whether the text it names contradicts it, quoting the passage that does. Write `none` where `response.md` makes every statement in the draft's words.

**3. Made false.** From heading 2, every statement that was true in `draft.md` and is false in `response.md`. Write `none` where there is none.

**4. Removed.** Every statement of `draft.md` about either text that `response.md` no longer makes, and whether an item of `check.md` called for its removal.

Then reply in at most 120 words: how many items `check.md` lists and how many were corrected, left out or not handled; how many statements changed after the check and how many of those are false; the number under heading 3; and the path you wrote.
