# help

Print the manager's own manpage, or the manpage of one of its subcommands. Bare `/kntnt` arrives here.

`$HERE` is the manager directory (the parent of `scripts/`).

## Steps

1. `--help` and `-h` are routes rather than flags on a verb. For `<subcommand> --help` or `<subcommand> -h`, keep the subcommand as the requested page and drop the help flag. At the top level, drop the help flag and request the Manager's own page. Every other argument the user gave goes to the script as it stands: `help` takes no flags, and the script refuses one with Help's own synopsis (ADR-0059).
2. If the user named a subcommand directly or as `help <command>`, run `uv run "$HERE/scripts/kntnt.py" help <command>` with any other arguments they gave. Otherwise run `uv run "$HERE/scripts/kntnt.py" help`, again with any other arguments. Done when the command has answered, on stdout or on stderr.
3. Emit what it answered with, as it stands. On success that is a manpage the collection ships, so it is printed, not summarised, extended, or rewritten. On a name the manager does not document the command fails instead, and its refusal already names both routes to a skill's own help — `/<skill> --help` for one the user has, `/kntnt select` for one they do not — so that message is what the user gets, unrewritten and unsupplemented. Stop.
