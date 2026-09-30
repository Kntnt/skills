# help

Print compact help for the Manager, one of its subcommands, or an Enabled Skill. Bare `/kntnt` arrives here, and so does `help` with a *NAME* operand; the exact help forms never do, the engine having printed compact help already.

`$HERE` is the manager directory (the parent of `scripts/`).

## Steps

1. Run `uv run "$HERE/scripts/kntnt.py" help`, with the one entry of `operands` after it as a single argument where there is one. Done when the command has answered, on stdout or on stderr.
2. Emit what it answered with, as it stands. On success that is the engine's compact help, including the installed full-reference path; a Skill's help is only read, never a cue to run that Skill. On a name that is neither a Manager command nor an Enabled Skill the command fails instead, and its refusal already names `/kntnt select` as the route to help for a Skill the user does not have, so that message is what the user gets, unrewritten and unsupplemented. Stop.
