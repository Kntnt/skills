# help

Print the manager's own manpage, the manpage of one of its subcommands, or the help of one collection skill. Bare `/kntnt` arrives here.

`$HERE` is the manager directory (the parent of `scripts/`).

## Steps

1. If the user named a subcommand or a skill (or the arguments are `help <name>`), run `uv run "$HERE/scripts/kntnt.py" help <name>`. Otherwise run `uv run "$HERE/scripts/kntnt.py" help`. Done when stdout is the help text.
2. Emit that text as it stands. It is a manpage the collection ships, so it is printed, not summarised, extended, or rewritten. A named skill that is Disabled has no files on disk, so its help is the Catalog description alone; say that Enabling it from `/kntnt select` gives the rest. Stop.
