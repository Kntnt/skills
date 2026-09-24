#!/bin/sh
# wave_inventory.sh LABEL
#
# Scopes 3 and 4, once around a wave. LABEL is a path prefix. Scope 3 is the
# whole scratch staging root; scope 4 is the two checkouts of this repository
# a run is told not to read, by HEAD and porcelain status. The status is read
# with --no-optional-locks so that taking the inventory writes nothing into
# either checkout's index.
set -eu
label=$1
S=/Users/thomas/Projects/skills/.git/kntnt-orchestrate/385.scratch/kntnt-eval-385
H=$(dirname "$0")
"$H/inventory.sh" "$label-scratch.txt" "$S"
{
  for repo in /Users/thomas/Projects/skills/.git/kntnt-orchestrate/385 /Users/thomas/Projects/skills; do
    printf '# %s\n' "$repo"
    printf '# HEAD %s\n' "$(git -C "$repo" rev-parse HEAD)"
    git --no-optional-locks -C "$repo" status --porcelain --untracked-files=all
    printf '# end %s\n' "$repo"
  done
} > "$label-repo.txt"
