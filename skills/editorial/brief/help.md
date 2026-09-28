# brief

## NAME

brief - interview for, draft or review a writing brief

## SYNOPSIS

**/brief** [**--output=**_TARGET_] [*MATERIAL*] [**--** *INSTRUCTION*]

## DESCRIPTION

Produce a Markdown writing brief using 13 numbered questions. Without material, start an interview, one question at a time. With notes, documents or links, draft from what they support. With an existing brief, review which answers it contains regardless of its layout. Ask which mode is wanted only when unclear.

The questions and brief use your working language. The future text's language is a separate answer. Settled genre, technique and text language are verified against the installed Library and carried as Kntnt metadata for a later `/write` invocation.

An interview allows two follow-up questions per point, then marks a still-weak answer. You can say you do not know or revisit an earlier answer. A draft marks missing information and unconfirmed suggestions, then offers an interview about the gaps. A review reports all 13 points and the coherence check, delivers a mapped brief, and offers both a rewrite and a gap interview.

All modes deliver a brief and run its coherence check. The fixed markers `[MISSING: …]`, `[SUGGESTED: …]` and `[WEAK: …]` stay English in every language. Facts, sources and brand details are never invented. The Skill stops at the brief and does not write the text or start `/write`.

Start it by name or explicitly ask for a brief according to this 13-question template. Merely mentioning a brief does not start it.

## POSITIONAL ARGUMENTS

*MATERIAL*

Free text, notes, paths, URLs or documents for one brief, or an existing brief. Material may instead come from the Contextual Instruction or conversation. Omit it to start an interview.

## OPTIONS

**--output=**_TARGET_

Deliver to `response` (the default) or one filesystem path. A new path creates a file, an existing file is replaced, and an existing directory receives a derived filename. The parent must exist. A file that supplied material cannot also be the output. No in-place editing is offered.

## INVOCATION ENVELOPE

The optional Contextual Instruction follows the reserved separator `--`. See `library/references/invocation-envelope.md` in the Collection Library for the complete contract.

## DEPENDENCIES

Requires `uv` and the Collection Manager with its Library.

## DIAGNOSTICS

An undeclared flag, a flag with no work to do, an incomplete form or a declared flag after an operand is refused rather than ignored or reordered. Nothing is written; use `/brief --help` for the accepted form.

An inaccessible source or an unverified selection is reported and left missing rather than guessed. A destination equal to a supplied file or an unwritable destination is refused before writing. An incomplete brief is delivered with its gaps and is not reported ready to write.

## EXAMPLES

`/brief`

Start the interview without source material.

`/brief --output=writing-brief.md notes.md -- Draft from these notes and keep unanswered questions visible.`

Create a new brief while leaving the notes unchanged.

`/brief existing-brief.md -- Review the answers against the 13-question template.`

Return a mapped brief and review report in the response.

## SEE ALSO

**/write**, **/redline**, **/kntnt help brief**
