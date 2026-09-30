#!/bin/sh
# wave.sh WAVE REVISION [ROW ...]
#
# Makes every run of one wave of matrix.tsv at once, with the protocol's
# Claude-family runner, staged from REVISION, and takes the wave inventory
# (scopes 3 to 5) before and after it. Where ROWs are given, only the wave's
# runs of those rows are made: a revise round re-runs only the rows that
# missed. A wave holds at most four runs, each on a different row, so no two
# runs of one input are ever in flight at once. A run whose packet already
# exists is not made again; a void run's packet is moved to voided/ first.
#
# Each input is written from the corpus commit with `git show`, never read from
# a working tree, and the runner stages the Skills from REVISION with
# `git archive` into a private root of its own.
set -u
wave=$1
revision=$2
shift 2
here=$(cd "$(dirname "$0")" && pwd)
repo=$(cd "$here/../../../.." && pwd)
S=/Users/thomas/Projects/skills/.git/kntnt-orchestrate/433.scratch
corpus=2afeb95e
mkdir -p "$S/inputs" "$S/packets" "$S/logs"
selected="$S/logs/wave-$wave.tsv"
tail -n +2 "$here/matrix.tsv" | awk -F '\t' -v w="$wave" '$1 == w' > "$selected"
"$here/wave_inventory.sh" "$here/wave-$wave-before"
while IFS="$(printf '\t')" read -r w run arm row invocation; do
    if [ "$#" -gt 0 ]; then
        wanted=no
        for r in "$@"; do [ "$r" = "$row" ] && wanted=yes; done
        [ "$wanted" = yes ] || continue
    fi
    [ -e "$S/packets/$run" ] && continue
    staged="$S/inputs/$row.md"
    [ -f "$staged" ] || git -C "$repo" show \
        "$corpus:docs/evaluation/corpus/editorial-quality/controls/$row.md" > "$staged"
    printf '%s start %s %s\n' "$(date -u +%FT%TZ)" "$run" "$revision" >> "$S/logs/waves.log"
    (
        cd "$repo" && uv run docs/evaluation/editorial-388/harness/staged_run.py \
            --revision="$revision" --corpus-revision="$corpus" \
            --invocation="$invocation" \
            --input="$staged" --input-name=input.md \
            --output="$S/packets/$run" \
            --model=claude-opus-5-5 --effort=high
        printf '%s end %s exit %s\n' "$(date -u +%FT%TZ)" "$run" "$?" >> "$S/logs/waves.log"
    ) > "$S/logs/$run.log" 2>&1 < /dev/null &
done < "$selected"
wait
"$here/wave_inventory.sh" "$here/wave-$wave-after"
