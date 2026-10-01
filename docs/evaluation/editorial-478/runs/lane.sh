#!/bin/sh
# lane.sh LANE [MATRIX]
#
# Makes, one after the other, every run of one lane of matrix.tsv with the
# protocol's Claude-family runner. A lane holds every run of its inputs, so no
# two runs of one input are ever in flight at once. A run whose packet already
# exists is not made again; a void run's packet is moved to voided/ first.
#
# A `redline` run's input is written from the corpus commit with `git show`,
# never read from a working tree, and the runner stages the Skills from the
# run's revision with `git archive` into a private root of its own. A `replay`
# run is a reply-check diagnosis: its prompt, frozen with the plan, is the
# whole invocation, and it is given no input file.
set -u
lane=$1
here=$(cd "$(dirname "$0")" && pwd)
matrix=${2:-$here/matrix.tsv}
repo=$(cd "$here/../../../.." && pwd)
S=/Users/thomas/Projects/skills/.git/kntnt-orchestrate/478.scratch
corpus=fb169087
mkdir -p "$S/inputs" "$S/packets" "$S/logs"
tail -n +2 "$matrix" | while IFS="$(printf '\t')" read -r l run kind arm revision input invocation capture; do
    [ "$l" = "$lane" ] || continue
    [ -e "$S/packets/$run" ] && continue
    if [ "$kind" = replay ]; then
        set -- --revision="$revision" --corpus-revision="$corpus" \
            --invocation="$(cat "$repo/$input")" \
            --output="$S/packets/$run" --model=claude-opus-5-5 --effort=high
    else
        staged="$S/inputs/$(printf '%s' "$input" | tr '/' '_')"
        [ -f "$staged" ] || git -C "$repo" show "$corpus:$input" > "$staged"
        set -- --revision="$revision" --corpus-revision="$corpus" \
            --invocation="$invocation" --input="$staged" --input-name=input.md \
            --output="$S/packets/$run" --model=claude-opus-5-5 --effort=high
        [ "$capture" = yes ] && set -- "$@" --capture-output-name=output.md
    fi
    printf '%s start %s\n' "$(date -u +%FT%TZ)" "$run" >> "$S/logs/lane-$lane.log"
    (cd "$repo" && uv run docs/evaluation/editorial-388/harness/staged_run.py "$@") \
        > "$S/logs/$run.log" 2>&1 < /dev/null
    rc=$?
    printf '%s end %s exit %s\n' "$(date -u +%FT%TZ)" "$run" "$rc" >> "$S/logs/lane-$lane.log"
done
