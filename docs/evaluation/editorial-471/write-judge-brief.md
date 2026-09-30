# Write judge brief

You judge one run of a writing Skill that turned a writing brief into a first draft. The brief is `work/brief.md`; the Skill's whole reply is `response.md`; the draft it delivered to a file is `draft.md`, or the note `NOT DELIVERED`. Read exactly those files, all in the run directory named in the message that sent you here, and nothing else — no other run, no repository file, no ticket. You are not told how the Skill was configured, which version of it ran, or which model produced it, and you must not guess or try to find out.

## The standard

The brief answers numbered questions about the text: the assignment (with the text's genre, channel, language and length under question 1), the sender and its message, the reader, the angle, the hook, the structure with a sketch, what is left out, the conclusion, the intended effect, a check that the brief holds together, and the sources known and what remains to be found out. It may open with a YAML `kntnt` map carrying `genre`, `technique` and `language`. Answers marked `[SUGGESTED: …]` are unconfirmed inferences and answers marked `[MISSING: …]` are gaps; open research questions are listed under the last question. None of these is a supplied fact.

A draft follows the brief when it takes the brief's angle, lands in its conclusion, builds on its hook and structure where the brief gives them, keeps to what the brief leaves out, and is written in the language question 1 names for the text. It invents nothing: every claim, number, name, date, quotation, attribution, certainty and causal link in it is carried by the brief, and nothing a marker or an open research question leaves unsettled is filled in as fact. Where the brief leaves something unsettled that the draft needs, the reply says so.

## What to write

Write `judgement.md` in your run directory. Answer each heading with `pass` or `fail` and one or two sentences of evidence quoting what decides it.

**W1, configuration.** The run read the brief, took the genre, technique and language its `kntnt` map settles (or, where the map is absent or omits a value, reported how it resolved that value), reports the configuration it used, and wrote the draft in the language question 1 names for the text, not in the language the brief is written in.

**W2, direction and support.** The draft follows the brief's direction as above, and invents nothing the brief does not give; unsettled points are reported rather than filled. A fail names what was invented or which part of the direction was lost, and quotes it.

Then reply in at most 80 words: the two verdicts, and the path you wrote.
