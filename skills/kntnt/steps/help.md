# help

Print the manager's own manpage, or the manpage of one of its subcommands. Bare `/kntnt` arrives here.

`$HERE` is the manager directory (the parent of `scripts/`).

## Steps

1. `--help` and `-h` are how this verb is reached and are not flags on it. Any other flag is answered by saying that `help` takes no flags — it changes nothing, asks nothing, and writes nothing — before carrying on to print the page regardless. Saying so is the whole of the refusal: the script accepts the flag rather than crashing on it, because a flag the agent forwards on its own must never be what breaks a run (ADR-0029).
2. If the user named a subcommand (or the arguments are `help <command>`), run `uv run "$HERE/scripts/kntnt.py" help <command>`. Otherwise run `uv run "$HERE/scripts/kntnt.py" help`. Done when the command has answered, on stdout or on stderr.
3. Emit what it answered with, as it stands. On success that is a manpage the collection ships, so it is printed, not summarised, extended, or rewritten. On a name the manager does not document the command fails instead, and its refusal already names both routes to a skill's own help — `/<skill> --help` for one the user has, `/kntnt select` for one they do not — so that message is what the user gets, unrewritten and unsupplemented. Stop.
