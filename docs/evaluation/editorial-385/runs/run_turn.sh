#!/bin/sh
# run_turn.sh RUN INSTALL INPUT INVOCATION [LOCK]
#
# Makes one Unslop run as a fresh top-level Claude Code session. RUN is the
# run's name, INSTALL is pre, post or revise, INPUT is the file copied to the
# run's input.md, INVOCATION is the Formal Invocation verbatim, and LOCK, where
# given, is the draft whose machine-wide lock is held while the session runs.
#
# The prompt is the install's turn file, then the three things the turn says
# the dispatching message gives: the working directory, the run directory and
# the invocation. The session is started with --safe-mode, so no CLAUDE.md, no
# installed Skill, no hook and no custom agent reaches it, and on the seat the
# plan names. Its stream is kept outside the run directory, under logs/.
set -eu
run=$1; install=$2; input=$3; invocation=$4; lock=${5:-}
S=/Users/thomas/Projects/skills/.git/kntnt-orchestrate/385.scratch/kntnt-eval-385
H=$(cd "$(dirname "$0")" && pwd)
turn="$H/../unslop-turn-$install.md"
rundir="$S/runs/$run"
work="$rundir/work"
[ -e "$rundir" ] && { echo "exists: $rundir" >&2; exit 2; }
mkdir -p "$work" "$S/logs"
cp "$input" "$work/input.md"
"$H/run_inventory.sh" "$rundir/inventory-before.txt" "$rundir" "$S/install-$install"
{
  cat "$turn"
  printf '\n---\n\nYour working directory: %s\n\nThe run directory: %s\n\nThe user typed:\n\n%s\n' \
    "$work" "$rundir" "$invocation"
} > "$S/logs/$run.prompt.txt"
held=
trap '[ -n "$held" ] && rmdir "$held"; held=' EXIT
trap 'exit 143' INT TERM
if [ -n "$lock" ]; then
  L="/Users/thomas/Projects/skills/.git/kntnt-eval-lock-$lock"
  until mkdir "$L" 2>/dev/null; do sleep 30; done
  held=$L
fi
date -u +%Y-%m-%dT%H:%M:%SZ > "$S/logs/$run.started"
set +e
( cd "$work" && timeout 5400 claude --print --safe-mode \
    --model claude-opus-5-5 --effort high \
    --dangerously-skip-permissions --strict-mcp-config \
    --output-format stream-json --verbose \
    < "$S/logs/$run.prompt.txt" > "$S/logs/$run.jsonl" 2> "$S/logs/$run.err" )
status=$?
set -e
[ -n "$held" ] && rmdir "$held"
held=
"$H/run_inventory.sh" "$rundir/inventory-after.txt" "$rundir" "$S/install-$install"
printf '%s %s\n' "$status" "$(date -u +%Y-%m-%dT%H:%M:%SZ)" > "$S/logs/$run.done"
