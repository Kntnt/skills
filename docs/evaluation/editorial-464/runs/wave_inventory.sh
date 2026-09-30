#!/bin/sh
# wave_inventory.sh LABEL
#
# Scopes 3 to 5, once around a wave. LABEL is a path prefix. Scope 4 reads git
# status without taking the index lock, because other sessions work in the
# main checkout while these runs are made.
set -eu
label=$1
S=/Users/thomas/Projects/skills/.git/kntnt-orchestrate/464.scratch
P=/private/tmp/claude-501/-Users-thomas-Projects-skills/041e1ba1-3ffd-418b-8405-c4d6affc600c/scratchpad
here=$(dirname "$0")
"$here/inventory.sh" "$label-scratch.txt" "$S"
"$here/inventory.sh" "$label-session-scratchpad.txt" "$P"
{
  for repo in /Users/thomas/Projects/skills/.git/kntnt-orchestrate/464 /Users/thomas/Projects/skills; do
    printf '# %s\n' "$repo"
    printf '# HEAD %s\n' "$(git -C "$repo" rev-parse HEAD)"
    GIT_OPTIONAL_LOCKS=0 git -C "$repo" status --porcelain --untracked-files=all
    printf '# end %s\n' "$repo"
  done
} > "$label-repo.txt"
