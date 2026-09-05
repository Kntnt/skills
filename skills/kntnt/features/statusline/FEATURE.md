---
name: statusline
description: A two-line Claude Code status line — path, worktree, branch and working-tree state above; model, reasoning effort, context usage and subscription windows below.
metadata:
  kntnt.category: environment
  kntnt.harnesses: claude-code
  kntnt.binaries: git jq
  kntnt.capabilities: ""
  kntnt.integrations: scripts/statusline_feature.py
---

# statusline

Two lines under the prompt, drawn from what Claude Code already hands its status line plus one `git status` call.

The first line is where you are: the working directory with `~` for home, a marker when you are standing in a linked worktree — including one made by hand, which nothing else in the path gives away — the branch or the abbreviated commit of a detached head, then Starship's own working-tree vocabulary (`+` staged, `!` modified, `?` untracked, `$` stashed, `=` conflicted, `⇡⇣` against upstream), and any git operation left in progress: `REBASING 3/7`, `MERGING`, `CHERRY-PICKING`, `BISECTING`.

The second line is the run: the model, its reasoning effort where the model has one, the context window as thousands of tokens and a percentage coloured green, amber and red, and each subscription window Claude Code puts on stdin with the time it resets.

It reads what the Harness hands it, plus git. It calls no network service, reads no credential, and starts no background work — a status line runs on every render, so anything it did it would do again a moment later. A one-second timeout on the `git status` call keeps a huge or busy repository from ever stalling the prompt.

Glyphs come from a Nerd Font where the terminal is known to bundle one — Ghostty does; the web UI and the VS Code extension do not — and from plain characters otherwise. `CLAUDE_STATUSLINE_ICONS=nerd` or `=text` settles it by hand.

## Writes

- `statusLine` in `~/.claude/settings.json`, pointing at the shipped `statusline.sh` inside this collection's installed Manager. It is a single-valued setting, so it cannot hold two: where it already runs a command that is not this collection's, the row names that command and the confirmation asks whether to replace it, and nothing is written until you answer yes. Nothing is kept of what is replaced, so disabling the Feature afterwards clears the setting rather than restoring the command that was there. Disabling leaves the setting alone where this collection does not hold it.

## Keeping your own

Because `statusLine` holds one command, this Feature and a status line of your own are a choice rather than a pair — and it is your choice, asked at the list rather than decided for you. Checking the row when something of yours is there names that command and asks whether to replace it; answering no leaves it exactly as it was.

If you want this one with something of your own on top, copy `statusline.sh` somewhere of your own, edit that copy, and point `statusLine` at it — enabling the Feature again converges the shipped file back to what the collection ships, so edits made in place do not survive an update.
