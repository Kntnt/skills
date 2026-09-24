#!/bin/sh
# wave_inventory.sh LABEL
#
# Scopes 3 to 5, once around a parallel wave. LABEL is a path prefix.
# Scope 4 reads git status without taking the index lock, because other
# sessions work in the main checkout while these runs are made.
set -eu
label=$1
S=/Users/thomas/Projects/skills/.git/kntnt-orchestrate/398.scratch
P=/private/tmp/claude-501/-Users-thomas-Projects-skills/40416275-c971-4568-a8ae-051cb6943e72/scratchpad
here=$(dirname "$0")
"$here/inventory.sh" "$label-scratch.txt" "$S"
"$here/inventory.sh" "$label-session-scratchpad.txt" "$P"
{
  for repo in /Users/thomas/Projects/skills/.git/kntnt-orchestrate/398 /Users/thomas/Projects/skills; do
    printf '# %s\n' "$repo"
    printf '# HEAD %s\n' "$(git -C "$repo" rev-parse HEAD)"
    GIT_OPTIONAL_LOCKS=0 git -C "$repo" status --porcelain --untracked-files=all
    printf '# end %s\n' "$repo"
  done
} > "$label-repo.txt"
