#!/bin/bash
# Claude Code status line, installed and owned by kntnt.statusline.
#
# Reads the status JSON Claude Code writes to stdin and prints two lines: the
# repo-relative path, worktree marker, branch, working-tree flags and any git
# operation in progress on the first; the model, its reasoning effort, context
# usage and the subscription windows on the second.
#
# It reads what the Harness hands it, plus git. It calls no network service,
# reads no credential and starts no background work: a status line runs on every
# render, so anything it does it does again a moment later.
#
# This file is the Feature's own. Enabling the Feature again converges it back
# to what the collection ships, so put your own edits in your own copy and point
# the statusLine setting at that instead.

# Capture the status payload Claude Code provides on stdin.
input=$(cat)

# Icon set. Nerd Font glyphs live in the Private Use Area, so they render only
# where a symbol font backs them up: Ghostty bundles Symbols Nerd Font, the web
# UI and the VS Code extension do not. The glyphs are built from hex escapes
# rather than written literally, so no editor or pipeline can silently drop
# them. CLAUDE_STATUSLINE_ICONS=nerd|text overrides the detection.
icons=${CLAUDE_STATUSLINE_ICONS:-auto}
if [ "$icons" = auto ]; then
  if [ "$TERM_PROGRAM" = ghostty ]; then icons=nerd; else icons=text; fi
fi
if [ "$icons" = nerd ]; then
  icon_branch=$(printf '\xee\x82\xa0')    # U+E0A0 powerline branch
  icon_worktree=$(printf '\xef\x89\x8d')  # U+F24D clone: a second checkout
else
  icon_branch="⑂"
  icon_worktree="wt"
fi

# Pull out the fields we want to display, with safe fallbacks for values
# that may be null before the first API call.
raw_dir=$(jq -r '.workspace.current_dir // .cwd // ""' <<<"$input")
model=$(jq -r '.model.display_name // "?"' <<<"$input")

# Current reasoning effort, used as-is; the field is absent on models without
# effort support, in which case the segment is omitted entirely.
effort=$(jq -r '.effort.level // ""' <<<"$input")
[ -n "$effort" ] && effort=" $effort"

used_tokens=$(jq -r '.context_window.total_input_tokens // 0' <<<"$input")
used_pct=$(jq -r '.context_window.used_percentage // 0 | floor' <<<"$input")

# Express the token count in thousands (K).
used_k=$((used_tokens / 1000))

# Context-window usage colour: green below 20 %, yellow below 50 %, red at 50 %+.
ctx_color=32
[ "$used_pct" -ge 20 ] && ctx_color=33
[ "$used_pct" -ge 50 ] && ctx_color=31

# Worktree name as Claude Code knows it: the --worktree session object first,
# then the linked-worktree name it reports for a plain cwd.
worktree=$(jq -r '.worktree.name // .workspace.git_worktree // ""' <<<"$input")
branch=$(jq -r '.worktree.branch // ""' <<<"$input")

# Locate the repository. The two git dirs differ exactly inside a linked
# worktree, which is how a worktree created by hand — with no --worktree
# session behind it — is recognised.
if [ -d "$raw_dir" ]; then
  { read -r git_dir; read -r git_common_dir; read -r git_top; } < <(
    git --no-optional-locks -C "$raw_dir" rev-parse \
      --absolute-git-dir --path-format=absolute --git-common-dir --show-toplevel 2>/dev/null
  )
fi

# A linked worktree is exactly where the two git dirs part ways, which is how
# one created by hand — with no --worktree session behind it — is recognised.
in_worktree=""
[ -n "$git_top" ] && [ "$git_dir" != "$git_common_dir" ] && in_worktree=1

# The working directory in full, with ~ standing in for the home directory.
dir="$raw_dir"
case "$dir" in
  "$HOME") dir="~" ;;
  "$HOME"/*) dir="~${dir#"$HOME"}" ;;
esac

# Working-tree summary in one pass: the branch header, the ahead/behind counts
# and a tally of staged, modified, untracked and conflicted paths. A timeout
# keeps a huge or busy repository from ever stalling the status line.
if [ -n "$git_top" ]; then
  timeout_cmd=""
  command -v timeout >/dev/null 2>&1 && timeout_cmd="timeout 1s"
  status_out=$($timeout_cmd git --no-optional-locks -C "$raw_dir" \
    status --porcelain=v2 --branch --show-stash 2>/dev/null)
  IFS=$'\t' read -r git_head git_oid ahead behind staged modified untracked conflicts stashed < <(
    awk '
      /^# branch\.head / { head = $3 }
      /^# branch\.oid /  { oid = $3 }
      /^# branch\.ab /   { ahead = substr($3, 2) + 0; behind = substr($4, 2) + 0 }
      /^# stash /        { stashed = $3 + 0 }
      /^[12] /           { if (substr($2, 1, 1) != ".") staged++
                           if (substr($2, 2, 1) != ".") modified++ }
      /^u /              { conflicts++ }
      /^\? /             { untracked++ }
      END { printf "%s\t%s\t%d\t%d\t%d\t%d\t%d\t%d\t%d\n",
              head, oid, ahead, behind, staged, modified, untracked, conflicts, stashed }
    ' <<<"$status_out"
  )

  # A detached HEAD has no branch name; show the abbreviated commit instead.
  # Should the status call have timed out, the branch alone is still worth a
  # second, much cheaper question.
  if [ -z "$branch" ]; then
    if [ -n "$git_head" ] && [ "$git_head" != "(detached)" ]; then
      branch="$git_head"
    elif [ -n "$git_oid" ] && [ "$git_oid" != "(initial)" ]; then
      branch="@${git_oid:0:7}"
    else
      branch=$(git --no-optional-locks -C "$raw_dir" branch --show-current 2>/dev/null)
    fi
  fi
fi

# In-progress operations, read straight from the git directory: an interrupted
# rebase, merge or bisect is the single most useful thing a status line can say.
state=""
if [ -n "$git_dir" ]; then
  if [ -d "$git_dir/rebase-merge" ]; then
    state="REBASING"
    if [ -r "$git_dir/rebase-merge/msgnum" ] && [ -r "$git_dir/rebase-merge/end" ]; then
      state="$state $(<"$git_dir/rebase-merge/msgnum")/$(<"$git_dir/rebase-merge/end")"
    fi
  elif [ -d "$git_dir/rebase-apply" ]; then
    state="REBASING"
    [ -f "$git_dir/rebase-apply/applying" ] && state="AM"
  elif [ -f "$git_dir/MERGE_HEAD" ]; then
    state="MERGING"
  elif [ -f "$git_dir/CHERRY_PICK_HEAD" ]; then
    state="CHERRY-PICKING"
  elif [ -f "$git_dir/REVERT_HEAD" ]; then
    state="REVERTING"
  elif [ -f "$git_dir/BISECT_LOG" ]; then
    state="BISECTING"
  fi
fi

# First line: the blue path, then the optional worktree, branch, working-tree
# flags and any operation in progress.
printf '\033[01;34m%s\033[00m' "$dir"
# Standing inside the worktree, the path already names it and the marker alone
# is enough — including for one created by hand, where nothing else in the path
# would give it away. The name is spelled out only when the session says it is
# in a worktree that the working directory is not.
if [ -n "$in_worktree" ]; then
  printf ' \033[01;35m%s\033[00m' "$icon_worktree"
elif [ -n "$worktree" ]; then
  printf ' \033[01;35m%s %s\033[00m' "$icon_worktree" "$worktree"
fi
[ -n "$branch" ] && printf ' \033[01;32m%s %s\033[00m' "$icon_branch" "$branch"

# Starship's git_status vocabulary: + staged, ! modified, ? untracked,
# $ stashed, = conflicted, and the ahead/behind arrows against upstream.
[ "${staged:-0}" -gt 0 ] && printf ' \033[01;33m+%d\033[00m' "$staged"
[ "${modified:-0}" -gt 0 ] && printf ' \033[01;33m!%d\033[00m' "$modified"
[ "${untracked:-0}" -gt 0 ] && printf ' \033[01;33m?%d\033[00m' "$untracked"
[ "${stashed:-0}" -gt 0 ] && printf ' \033[01;33m$%d\033[00m' "$stashed"
[ "${conflicts:-0}" -gt 0 ] && printf ' \033[01;31m=%d\033[00m' "$conflicts"
[ "${ahead:-0}" -gt 0 ] && printf ' \033[01;36m⇡%d\033[00m' "$ahead"
[ "${behind:-0}" -gt 0 ] && printf ' \033[01;36m⇣%d\033[00m' "$behind"
[ -n "$state" ] && printf ' \033[01;31m%s\033[00m' "$state"

printf '\n'

# Second line: model and effort, then colour-coded context usage, and after it
# every usage window; %% escapes the literal percent sign.
printf '%s%s · \033[01;%dm%dK (%d%%)\033[00m' \
  "$model" "$effort" "$ctx_color" "$used_k" "$used_pct"

# Append a rate-limit segment for one usage window. Claude Code provides these
# fields only on Claude.ai Pro/Max plans, and only after the first API response;
# each window is independently optional, so a missing percentage prints nothing.
emit_limit() {
  local pct="$1" label="$2" resets="$3" datefmt="$4"

  # Skip the window entirely when its usage is absent.
  if [ -z "$pct" ] || [ "$pct" = "null" ]; then
    return
  fi
  pct=$(printf '%.0f' "$pct")

  # Severity colour: green below 50 %, yellow from 50 %, red from 80 %.
  local color=32
  [ "$pct" -ge 50 ] && color=33
  [ "$pct" -ge 80 ] && color=31

  # Reset clock, formatted from the Unix epoch when a timestamp is available.
  # Try BSD date (-r <epoch>) first, then GNU date (-d @<epoch>).
  local reset="" clock=""
  if [ -n "$resets" ] && [ "$resets" != "null" ]; then
    clock=$(date -r "$resets" +"$datefmt" 2>/dev/null \
      || date -d "@$resets" +"$datefmt" 2>/dev/null)
    [ -n "$clock" ] && reset=" ↻ $clock"
  fi

  printf ' · %s \033[01;%dm%d%%\033[00m%s' "$label" "$color" "$pct" "$reset"
}

# Extract the 5-hour and 7-day windows (percentage used and reset timestamp).
five_pct=$(jq -r '.rate_limits.five_hour.used_percentage // empty' <<<"$input")
five_rst=$(jq -r '.rate_limits.five_hour.resets_at // empty' <<<"$input")
week_pct=$(jq -r '.rate_limits.seven_day.used_percentage // empty' <<<"$input")
week_rst=$(jq -r '.rate_limits.seven_day.resets_at // empty' <<<"$input")

# Show the 5-hour window with a wall-clock reset and the 7-day window with a
# month-day reset.
emit_limit "$five_pct" "5h" "$five_rst" "%H:%M"
emit_limit "$week_pct" "7d" "$week_rst" "%m-%d"

