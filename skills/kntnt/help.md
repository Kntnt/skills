# help

Print help for the manager, or for one named collection skill. Bare `/kntnt` arrives here.

`$HERE` is the manager directory (the parent of `scripts/`).

## Steps

1. If the user named a skill (or the arguments are `help <name>`), run `uv run "$HERE/scripts/kntnt.py" help <name>`. Otherwise run `uv run "$HERE/scripts/kntnt.py" help`. Done when stdout is the help text.
2. Emit that text. A named skill that is Disabled has no `SKILL.md` on disk, so its help is the Catalog description alone; say `/kntnt enable <name>` gives the rest. Stop.
