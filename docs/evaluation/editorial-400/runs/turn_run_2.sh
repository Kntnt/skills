#!/bin/sh
# turn_run_2.sh TURN RUNDIR WORKDIR ENVROOT PACKET INVOCATION
#
# turn_run.sh as the plan froze it, and one change, which plan-amendment.md
# gives the reason for: the private home carries a copy of the staged
# install's proofread under ~/.agents/skills, so that the Manager finds the
# Skill Redline declares it depends on Enabled at the Global layer, as the
# machine #383's runs were made on had it. Claude Code reads no Skill from
# that directory, so the session is offered none.
#
# One Redline run of this evaluation: a fresh top-level Claude Code session on
# claude-opus-5-5 at high deliberation, sent the turn file TURN followed by the
# message that names its working directory, the invocation the user typed and
# its run directory, as #383's plan dispatches a turn. The session starts in
# WORKDIR, which holds input.md and nothing else.
#
# ENVROOT is made here and must not exist: it becomes the session's HOME, its
# Claude configuration directory, its temporary directory and its caches, so
# no hook, Skill, memory or setting of this machine's own reaches the run and
# the run's own start fires none of them. It is removed on every exit. The
# credential is the one the machine's Harness keeps in the keychain, written
# 0600 inside ENVROOT and removed with it.
#
# PACKET receives the evaluator's evidence: the prompt, the stream, the reply
# the Harness returned, the session's transcripts and the models they record,
# and the before-and-after inventories of RUNDIR and the staged install the
# turn names (scopes 1 and 2).
#
# The environment is this one's, less every CLAUDE_*, ANTHROPIC_* and KNTNT_*
# variable and CLAUDECODE, so that nothing points the run at this session or
# at the machine's installation of the collection.

set -eu

if [ "$#" -ne 6 ]; then
    echo "usage: $0 TURN RUNDIR WORKDIR ENVROOT PACKET INVOCATION" >&2
    exit 2
fi

turn=$1
rundir=$2
work=$3
envroot=$4
packet=$5
invocation=$6
here=$(cd "$(dirname "$0")" && pwd)

# The install the turn names, read out of the turn so the inventory covers the
# install the run was actually sent to.
install=$(sed -n 's/.*`\$HERE` is `\([^`]*\)\/redline`.*/\1/p' "$turn")
[ -n "$install" ] && [ -d "$install" ] || {
    echo "no staged install named in $turn" >&2
    exit 2
}

mkdir "$envroot"
trap 'rm -rf "$envroot"' EXIT
trap 'exit 130' INT TERM
mkdir -p "$envroot/home/.claude" "$envroot/tmp" "$envroot/cache" \
    "$envroot/data" "$envroot/uv-cache" "$envroot/config" "$packet"
chmod 700 "$envroot/home/.claude"
mkdir -p "$envroot/home/.agents/skills"
cp -R "$install/proofread" "$envroot/home/.agents/skills/proofread"
(
    umask 077
    security find-generic-password -s "Claude Code-credentials" -w |
        jq '{claudeAiOauth: .claudeAiOauth}' >"$envroot/home/.claude/.credentials.json"
)

{
    cat "$turn"
    printf '\n---\n\n'
    printf 'Your working directory: `%s`\n\n' "$work"
    printf 'The invocation the user typed: `%s`\n\n' "$invocation"
    printf 'Your run directory: `%s`\n' "$rundir"
} >"$packet/prompt.txt"

"$here/inventory.sh" "$packet/inventory-before.txt" "$rundir" "$install"

session=$(uuidgen | tr 'A-Z' 'a-z')
unset_args=""
for name in $(env | cut -d= -f1 | grep -E '^(CLAUDE|ANTHROPIC|KNTNT)' || true); do
    unset_args="$unset_args -u $name"
done

printf '{"session_id": "%s", "invocation": "%s", "model": "claude-opus-5-5", "effort": "high", "started": "%s"}\n' \
    "$session" "$invocation" "$(date -u +%Y-%m-%dT%H:%M:%SZ)" >"$packet/run.json"

# The working directory sits under /Users/thomas, whose .claude/CLAUDE.md, and
# under this repository, whose CLAUDE.md and the AGENTS.md it links to, a
# session loads from every directory above it. Neither is the Skill's, so
# neither reaches the run.
exclusions='{"claudeMdExcludes": ["/Users/thomas/.claude/CLAUDE.md", "/Users/thomas/Projects/skills/CLAUDE.md", "/Users/thomas/Projects/skills/AGENTS.md"]}'

status=0
(
    cd "$work"
    # shellcheck disable=SC2086
    env $unset_args -u CLAUDECODE \
        HOME="$envroot/home" \
        CLAUDE_CONFIG_DIR="$envroot/home/.claude" \
        TMPDIR="$envroot/tmp" \
        UV_CACHE_DIR="$envroot/uv-cache" \
        XDG_DATA_HOME="$envroot/data" \
        XDG_CACHE_HOME="$envroot/cache" \
        XDG_CONFIG_HOME="$envroot/config" \
        timeout 3600 claude --print \
        --session-id "$session" \
        --model claude-opus-5-5 \
        --effort high \
        --dangerously-skip-permissions \
        --strict-mcp-config \
        --settings "$exclusions" \
        --output-format stream-json \
        --verbose \
        --add-dir "$install" \
        --add-dir "$rundir" \
        <"$packet/prompt.txt" >"$packet/stream.jsonl" 2>"$packet/stderr.txt"
) || status=$?

"$here/inventory.sh" "$packet/inventory-after.txt" "$rundir" "$install"

# The reply the Harness returned, beside the one the run saved.
jq -r 'select(.type == "result") | .result // ""' "$packet/stream.jsonl" >"$packet/response.txt" || true
jq -c 'select(.type == "result") | {is_error, subtype, num_turns, terminal_reason, duration_ms, modelUsage}' \
    "$packet/stream.jsonl" >"$packet/result.json" || true

# The session's own record and every nested agent's, and the model each one ran.
mkdir -p "$packet/transcripts"
parent=$(find "$envroot/home/.claude/projects" -name "$session.jsonl" 2>/dev/null | head -n 1)
if [ -n "$parent" ]; then
    cp "$parent" "$packet/transcripts/parent.jsonl"
    beside=${parent%.jsonl}
    if [ -d "$beside/subagents" ]; then
        cp -R "$beside/subagents" "$packet/transcripts/subagents"
    fi
fi
{
    for record in "$packet/transcripts/parent.jsonl" "$packet/transcripts/subagents"/*.jsonl; do
        [ -f "$record" ] || continue
        printf '%s\t%s\n' "$(basename "$record")" \
            "$(jq -r 'select(.type == "assistant") | .message.model // empty' "$record" | sort -u | tr '\n' ' ')"
    done
} >"$packet/seats.tsv"

printf '{"returncode": %s, "finished": "%s", "envroot_removed_on_exit": "%s"}\n' \
    "$status" "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$envroot" >"$packet/exit.json"
exit "$status"
