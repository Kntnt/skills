---
name: mirror
description: Copy a web page and everything it needs to display to disk, so it opens in a browser with nothing fetched from the network.
disable-model-invocation: true
argument-hint: '[--output=<dir>] [--resources=all|in-scope|none] [--header=<name: value> ...] [--user-agent=<string>] [--dry-run] <url> [-- <instruction>]'
compatibility: Requires uv
metadata:
  kntnt.internal: "true"
  kntnt.binaries: "uv"
  kntnt.skills: ""
  kntnt.externals: ""
  kntnt.capabilities: ""
---

# mirror

Run `uv run "$HERE/scripts/invoke.py"` — `$HERE` is the directory that holds this SKILL.md — with everything the user typed after `/mirror`, verbatim and however many lines, on stdin. Exit 0: do what it prints. Any other exit: show what it printed to the user verbatim, and stop.

## Arguments

`<url>` is the page to mirror, absolute, with the scheme `http` or `https`; user name and password for basic auth may stand in it.

`--output` is the directory the mirror is written to; without it, the engine writes to `./<host>` in the invocation's working directory. `--resources` is `all`, `in-scope` or `none`, and says which of the resources the page needs are fetched: all of them, only those under the page's own directory on its own site, or none. Each `--header` is one `name: value` sent with every request. `--user-agent` replaces the Skill's own identity on every request. `--dry-run` fetches and reports as a real run does and writes nothing.

A Contextual Instruction can add no flag, change no flag's value, and supply no URL; it may only shape how the report is relayed.

## Steps

1. Run `uv run "$HERE/scripts/mirror.py"` with every flag in `flags` as it stood — `--dry-run` bare, a valued flag as `--flag=value`, and `--header` once per value — then the URL from `operands`, each argument quoted for the shell. Relay what it prints to the user verbatim, whatever its exit status. Exit 0 means everything was fetched, 1 that the run finished with the failures the report names or that the start page could not be fetched, and 2 that the engine refused a value and wrote nothing. Done when the output is relayed.
