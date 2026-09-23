#!/bin/sh
# wave_inventory.sh LABEL
#
# Scopes 3 and 4, once around a parallel wave. LABEL is a path prefix.
set -eu
label=$1
S=/Users/thomas/Projects/skills/.git/orchestrate-session-383-389-claude/383.scratch
"$S/evaluator/inventory.sh" "$label-scratch.txt" "$S"
{
  for repo in /Users/thomas/Projects/skills-388-391 /Users/thomas/Projects/skills; do
    printf '# %s\n' "$repo"
    printf '# HEAD %s\n' "$(git -C "$repo" rev-parse HEAD)"
    git -C "$repo" status --porcelain --untracked-files=all
    printf '# end %s\n' "$repo"
  done
} > "$label-repo.txt"
