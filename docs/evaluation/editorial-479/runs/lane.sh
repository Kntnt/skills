#!/bin/sh
# lane.sh LANE ARM [REVISION] [MATRIX]
#
# Makes, one after the other, every run of one lane and one arm of matrix.tsv
# with the protocol's Claude-family runner. A lane holds every run of its
# input, so no two runs of one input are ever in flight at once. A run whose
# packet already exists is not made again; a void run's packet is moved to
# voided/ first.
#
# A row's revision `candidate` is replaced by REVISION, which is required for
# such a row: the candidate is committed only after the pre-change arm has
# been read, so the matrix cannot name it.
#
# Each input is written with `git show`, never read from a working tree: a
# corpus input from the corpus commit, and an input of this evaluation's own
# (source `frozen`) from the commit that last changed it, which is the commit
# that froze this plan.
set -u
lane=$1
arm=$2
candidate=${3:-}
here=$(cd "$(dirname "$0")" && pwd)
matrix=${4:-$here/matrix.tsv}
repo=$(cd "$here/../../../.." && pwd)
S=/Users/thomas/Projects/skills/.git/kntnt-orchestrate/479.scratch
corpus=fb169087
mkdir -p "$S/inputs" "$S/packets" "$S/logs"
tail -n +2 "$matrix" | while IFS="$(printf '\t')" read -r l run a revision source input invocation capture; do
    [ "$l" = "$lane" ] || continue
    [ "$a" = "$arm" ] || continue
    [ -e "$S/packets/$run" ] && continue
    if [ "$revision" = candidate ]; then
        [ -n "$candidate" ] || { echo "no candidate revision for $run" >&2; exit 2; }
        revision=$candidate
    fi
    if [ "$source" = frozen ]; then
        source=$(git -C "$repo" log -1 --format=%h -- "$input")
    fi
    staged="$S/inputs/$source-$(printf '%s' "$input" | tr '/' '_')"
    [ -f "$staged" ] || git -C "$repo" show "$source:$input" > "$staged"
    set -- --revision="$revision" --corpus-revision="$source" \
        --invocation="$invocation" --input="$staged" --input-name=input.md \
        --output="$S/packets/$run" --model=claude-opus-5-5 --effort=high
    [ "$capture" = yes ] && set -- "$@" --capture-output-name=output.md
    printf '%s start %s\n' "$(date -u +%FT%TZ)" "$run" >> "$S/logs/lane-$lane.log"
    (cd "$repo" && uv run docs/evaluation/editorial-388/harness/staged_run.py "$@") \
        > "$S/logs/$run.log" 2>&1 < /dev/null
    rc=$?
    printf '%s end %s exit %s\n' "$(date -u +%FT%TZ)" "$run" "$rc" >> "$S/logs/lane-$lane.log"
done
