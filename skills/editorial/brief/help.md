# brief

## NAME

brief - interview for, draft or review a writing brief

## SYNOPSIS

**/brief** [**--output=**_TARGET_] [*MATERIAL*] [**--** *INSTRUCTION*]

## DESCRIPTION

Produce a Markdown writing brief from the Library's template of numbered questions to answer before you write. Without material, start an interview, one question at a time. With notes, documents or links, draft from what they support. With an existing brief, review which answers it contains regardless of its layout, including a brief written to an older version of the template. Ask which mode is wanted only when unclear.

A brief is a direction, not a finished dossier: it is often written before the research is done. The Skill takes each answer as given and marks no answer as weak. Where the template names a common mistake, such as a topic where the sender's message or the text's conclusion should be a one-sentence claim, it says so once, as a suggestion. It asks at most one follow-up question per answer, and only when the angle, the sender's message or the conclusion leaves the direction of the text unclear. No sources are required: what needs to be found out is listed as open questions under the last question.

The questions and brief use your working language. The future text's language is part of the assignment and can differ from it. Settled genre, technique and text language are verified against the installed Library and carried as Kntnt metadata for a later `/write` invocation. The structure question asks for the whole text in one sentence and a sketch step by step; the Skill reads the chosen technique's or genre's resource when it helps with the sketch.

All modes deliver a brief with its chain check written down, and say whether the brief is enough to write: that is when the angle, the sender's message and the conclusion are settled and every question before the sources has an answer, even while research questions remain open. The fixed markers `[MISSING: …]` and `[SUGGESTED: …]` stay English in every language. Facts, sources and brand details are never invented. A draft offers an interview about the gaps; a review reports each question as answered, answered with an open research question or unanswered, delivers a mapped brief, and offers both a rewrite and a gap interview. The Skill stops at the brief and does not write the text or start `/write`.

Start it by name or explicitly ask for a brief according to this writing-brief template. Merely mentioning a brief does not start it.

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

An inaccessible source or an unverified selection is reported and left missing rather than guessed. A destination equal to a supplied file or an unwritable destination is refused before writing. A brief whose direction is not settled is delivered with its gaps and the questions that would settle it, and is not reported enough to write; open research questions alone never hold it back.

## EXAMPLES

`/brief`

Start the interview without source material.

`/brief --output=writing-brief.md notes.md -- Draft from these notes and keep unanswered questions visible.`

Create a new brief while leaving the notes unchanged.

`/brief existing-brief.md -- Review the answers against the writing-brief template.`

Return a mapped brief and review report in the response.

## SEE ALSO

**/write**, **/redline**, **/kntnt help brief**
