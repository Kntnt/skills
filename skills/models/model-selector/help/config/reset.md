# model-selector config reset

## NAME

model-selector config reset - remove the active profile, or discard this machine's own measurement

## SYNOPSIS

**/model-selector** **config** **reset** [**--data=**_PATH_] [**--** *INSTRUCTION*]

**/model-selector** **config** **reset** **--evidence** [**--yes**] [**--data=**_PATH_] [**--** *INSTRUCTION*]

## DESCRIPTION

`model-selector config reset` shows the exact active configuration path, requests confirmation, appends a tombstone to configuration history, and removes only the active `config.json`. Evidence and revision history are retained.

The next command that requires model selections starts guided setup.

`--evidence` is the mirror move: bare `config reset` removes configuration and keeps measurement, `--evidence` removes measurement and keeps configuration. It shows the exact paths and the row or byte count of everything this machine measured — the evidence ledger and its derived frontiers, the quota store, the Standing Policy override and its history, capture and the Usage Record store — names any of them the selected data directory does not hold as absent, requests confirmation or reads it from a supplied `--yes`, then removes exactly those paths and reports what went, per path, by count of rows or bytes. `config.json`, its history, and every other file `references/evidence-ledger.md`'s `## Store` table names are untouched. Removing `capture/` clears its in-flight drafts; the Harness hooks stay installed and keep measuring.

## OPTIONS

**--data=**_PATH_

Use *PATH* as the profile and evidence directory instead of `~/.kntnt/model-selector/`.

**--evidence**

Discard this machine's own measurement instead of the profile. See `DESCRIPTION`.

**--yes**

Answer `--evidence`'s confirmation yes rather than asking, for an unattended run. Valid only combined with `--evidence`.

## DIAGNOSTICS

A declined confirmation, an absent profile or absent measurement, or an unsupported option changes nothing. Invalid syntax is refused rather than ignored; the Skill prints this SYNOPSIS and points to `/model-selector config reset --help`. `--yes` is refused, not ignored, on every other form of this Skill, `config reset` bare included.

## INVOCATION ENVELOPE

Every form above ends with [**--** *INSTRUCTION*]. The first standalone, unquoted `--` token is the reserved separator: everything before it is the Formal Invocation and everything after it is a Contextual Instruction, natural-language guidance that may clarify or narrow choices this Skill leaves open but cannot contradict the formal input, widen the Skill, or disable a required gate.

That contract belongs to the collection rather than to this page, and it is stated once, in the Collection Library the Manager ships, at `library/references/invocation-envelope.md`: the separator's quoted and attached forms, the boundaries this guidance and applicable Conversation Context are held to, the syntax refusal a malformed Envelope or Formal Invocation takes, the distinct context refusal unusable guidance takes, what a documented precedence suppresses rather than refuses, and how guidance is passed on to a nested Skill.

## DEPENDENCIES

`uv` runs the Skill's dependency check.

## SEE ALSO

**/model-selector setup --help**, **/model-selector config history --help**, **/model-selector config remove --help**
