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

- `statusLine` in `~/.claude/settings.json`, pointing at the shipped `statusline.sh` inside this collection's installed Manager. It is a single-valued setting: where it already runs something that is not this collection's, nothing is written, the run reports the slot as taken and names what holds it, and nothing of yours is remembered anywhere. Disabling the Feature clears the setting where this collection holds it and leaves it alone where it does not.

## Keeping your own

Because `statusLine` holds one command, this Feature and a status line of your own are a choice rather than a pair. If you have one you would rather keep, leave this row unchecked: the install will not overwrite it, and it will tell you so rather than doing it quietly. If you want this one with something of your own on top, copy `statusline.sh` somewhere of your own, edit that copy, and point `statusLine` at it — enabling the Feature again converges the shipped file back to what the collection ships, so edits made in place do not survive an update.
