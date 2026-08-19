# help

Print the manager's own manpage, or the manpage of one of its subcommands. Bare `/kntnt` arrives here.

`$HERE` is the manager directory (the parent of `scripts/`).

## Steps

1. `--help` and `-h` are how this verb is reached and are not flags on it, so they are dropped here rather than passed on. Every other argument the user gave goes to the script as it stands, flags included: `help` takes no flags — it changes nothing, asks nothing, and writes nothing — and the script is what refuses one, with the flag named, Help's own synopsis, and where to read the page in full (ADR-0059). The page is not printed anyway, and the refusal is not yours to write.
2. If the user named a subcommand (or the arguments are `help <command>`), run `uv run "$HERE/scripts/kntnt.py" help <command>` with any other arguments they gave. Otherwise run `uv run "$HERE/scripts/kntnt.py" help`, again with any other arguments. Done when the command has answered, on stdout or on stderr.
3. Emit what it answered with, as it stands. On success that is a manpage the collection ships, so it is printed, not summarised, extended, or rewritten. On a name the manager does not document the command fails instead, and its refusal already names both routes to a skill's own help — `/<skill> --help` for one the user has, `/kntnt select` for one they do not — so that message is what the user gets, unrewritten and unsupplemented. Stop.
