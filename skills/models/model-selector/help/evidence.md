# model-selector evidence

## NAME

model-selector evidence - report what has been measured and what the answers rest on

## SYNOPSIS

**/model-selector** **evidence** [**--data=**_PATH_] [*KIND*] [**--** *INSTRUCTION*]

## DESCRIPTION

Every recommendation is an estimate over rows this machine collected while you worked. This is those rows, grouped the way the estimate groups them: by kind of work, model, and deliberation level, which together are the whole of a measurement's identity.

Each group reports how many rows stand behind it, the mean score and who established it, the mean cost, the mean elapsed time, and the earliest and latest date. The row count is what separates an answer resting on measurement of exactly that point from one pooled up from the same model's other work, or from its published capability alone.

A figure no row carries is reported absent, never as a zero. An absence read as a zero is exactly how an unmeasured configuration becomes the cheapest thing on a list, and this Skill exists to stop that happening.

Scores come from four places, in descending authority: a checker's verdict on the finished work, a cheap model asked to grade a unit nothing else judged, a free signal such as tests that ran and passed or an attempt that was immediately redone, and you. Work never grades itself — a builder's own report of how it went establishes nothing.

Nothing is reported here that could identify the work. A row carries counts, times, prices and dates, and no text from the job it measured.

This command reads. It writes nothing, reaches no network, and grades nothing.

## POSITIONAL ARGUMENTS

*KIND*

Narrow the account to one class of work: `mechanical`, `implement`, `design`, `debug`, `review`, `analyze`, `prose`, or `converse`. Omitted, every kind is reported.

## OPTIONS

**--data=**_PATH_

Use *PATH* as the profile, catalogue and measurement directory instead of `~/.kntnt/model-selector/`.

## DIAGNOSTICS

A measurement store that does not exist yet is an empty account rather than an error, and the page says that measuring runs on its own while the Skill is Enabled. An option with no work to do here is refused rather than ignored: the Skill names the error, prints this SYNOPSIS, changes nothing, and points at `/model-selector evidence --help`.

## INVOCATION ENVELOPE

Every form above ends with [**--** *INSTRUCTION*]. The first standalone, unquoted `--` token is the reserved separator: everything before it is the Formal Invocation and everything after it is a Contextual Instruction, natural-language guidance that may clarify or narrow choices this Skill leaves open but cannot contradict the formal input, widen the Skill, or disable a required gate.

That contract belongs to the collection rather than to this page, and it is stated once, in the Collection Library the Manager ships, at `library/references/invocation-envelope.md`: the separator's quoted and attached forms, the boundaries this guidance and applicable Conversation Context are held to, the syntax refusal a malformed Envelope or Formal Invocation takes, the distinct context refusal unusable guidance takes, what a documented precedence suppresses rather than refuses, and how guidance is passed on to a nested Skill.

## DEPENDENCIES

`uv` runs the Skill's dependency check. Reading the measurement store needs nothing beyond the file itself.

## SEE ALSO

**/model-selector status --help**, **/model-selector reset --help**
