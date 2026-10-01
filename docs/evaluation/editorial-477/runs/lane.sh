#!/bin/sh
# lane.sh LANE ARM [MATRIX]
#
# Makes, one after the other, every run of one lane and one arm of matrix.tsv
# with the protocol's Claude-family runner. A lane holds every run of its
# input, so no two runs of one input are ever in flight at once. A run whose
# packet already exists is not made again; a void run's packet is moved to
# voided/ first.
#
# An input whose source is `corpus` is written from the corpus commit with
# `git show`; one whose source is `plan` is written with `git show` from the
# commit that last wrote it, which is the commit that froze the plan, and that
# commit is logged. Nothing is read from a working tree. The runner stages the
# Skills from the run's revision with `git archive` into a private root of its
# own.
set -u
lane=$1
want=$2
here=$(cd "$(dirname "$0")" && pwd)
matrix=${3:-$here/matrix.tsv}
repo=$(cd "$here/../../../.." && pwd)
S=/Users/thomas/Projects/skills/.git/kntnt-orchestrate/477.scratch
corpus=fb169087
mkdir -p "$S/inputs" "$S/packets" "$S/logs"
tail -n +2 "$matrix" | while IFS="$(printf '\t')" read -r l run arm revision source input invocation capture; do
    [ "$l" = "$lane" ] || continue
    [ "$arm" = "$want" ] || continue
    [ -e "$S/packets/$run" ] && continue
    if [ "$source" = corpus ]; then
        from=$corpus
    else
        from=$(git -C "$repo" log -1 --format=%H -- "$input")
    fi
    staged="$S/inputs/$(printf '%s' "$input" | tr '/' '_')"
    [ -f "$staged" ] || git -C "$repo" show "$from:$input" > "$staged"
    set -- --revision="$revision" --corpus-revision="$from" \
        --invocation="$invocation" --input="$staged" --input-name=input.md \
        --output="$S/packets/$run" --model=claude-opus-5-5 --effort=high
    [ "$capture" = yes ] && set -- "$@" --capture-output-name=output.md
    printf '%s start %s input-from %s\n' "$(date -u +%FT%TZ)" "$run" "$from" >> "$S/logs/lane-$lane.log"
    (cd "$repo" && uv run docs/evaluation/editorial-388/harness/staged_run.py "$@") \
        > "$S/logs/$run.log" 2>&1 < /dev/null
    rc=$?
    printf '%s end %s exit %s\n' "$(date -u +%FT%TZ)" "$run" "$rc" >> "$S/logs/lane-$lane.log"
done
