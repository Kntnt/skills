#!/bin/sh
# probe.sh RUN
#
# Makes one session of the cleanup-boundary probe with the protocol's
# Claude-family runner: the frozen probe-prompt.md is the session's whole
# prompt, typed into the same staged configuration a Redline run gets, with
# no input placed. A probe whose packet already exists is not made again.
set -u
run=$1
here=$(cd "$(dirname "$0")" && pwd)
repo=$(cd "$here/../../../.." && pwd)
S=/Users/thomas/Projects/skills/.git/kntnt-orchestrate/476.scratch
revision=fb169087
mkdir -p "$S/packets" "$S/logs"
[ -e "$S/packets/$run" ] && exit 0
printf '%s start %s\n' "$(date -u +%FT%TZ)" "$run" >> "$S/logs/lane-P.log"
(cd "$repo" && uv run docs/evaluation/editorial-388/harness/staged_run.py \
    --revision="$revision" --corpus-revision="$revision" \
    --invocation="$(cat "$here/../probe-prompt.md")" \
    --output="$S/packets/$run" --model=claude-opus-5-5 --effort=high) \
    > "$S/logs/$run.log" 2>&1 < /dev/null
rc=$?
printf '%s end %s exit %s\n' "$(date -u +%FT%TZ)" "$run" "$rc" >> "$S/logs/lane-P.log"
