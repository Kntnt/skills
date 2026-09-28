#!/bin/sh
# wave_inventory.sh LABEL
#
# Scopes 3 to 5, once around a wave. LABEL is a path prefix. Scope 4 is every
# checkout `git worktree list` showed when the plan was frozen, read by HEAD
# and by status without taking the index lock, because other sessions work in
# them while these runs are made.
set -eu
label=$1
S=/Users/thomas/Projects/skills/.git/kntnt-orchestrate/400.scratch
P=/private/tmp/claude-501/-Users-thomas-Projects-skills/40416275-c971-4568-a8ae-051cb6943e72/scratchpad
here=$(dirname "$0")
# Every directory of the scratch root but env/, whose private roots hold the
# credential a run authenticates with and are inventoried as scopes 1 and 2.
set --
for dir in "$S"/*; do
  [ "$(basename "$dir")" = env ] && continue
  set -- "$@" "$dir"
done
"$here/inventory.sh" "$label-scratch.txt" "$@"
"$here/inventory.sh" "$label-session-scratchpad.txt" "$P"
{
  for repo in /Users/thomas/Projects/skills \
      /Users/thomas/Projects/skills-rework \
      /Users/thomas/Projects/skills/.git/kntnt-orchestrate/385 \
      /Users/thomas/Projects/skills/.git/kntnt-orchestrate/400; do
    printf '# %s\n' "$repo"
    printf '# HEAD %s\n' "$(git -C "$repo" rev-parse HEAD)"
    GIT_OPTIONAL_LOCKS=0 git -C "$repo" status --porcelain --untracked-files=all
    printf '# end %s\n' "$repo"
  done
} > "$label-repo.txt"
