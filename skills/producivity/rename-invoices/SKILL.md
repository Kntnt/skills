---
name: rename-invoices
description: Safely plan and apply configurable filenames for text-based accounting PDFs.
disable-model-invocation: true
argument-hint: "--folder=<path> --type=<name> [--config=<path>|--no-config] [--locale=<name> ...] [--locale-file=<path> ...] [--prefix=<text>] [--template=<template>] [--date-format=<format>] [--description-template=<template>] [--extension=<extension>] [--identifier-template=<template>] [--date-source=<source> ...] [--counterparty-source=issuer|recipient] [--identifier-policy=always|collision|never] [--overrides=<path>] [--apply] [-- <instruction>]"
compatibility: Requires pdftotext and uv
metadata:
  kntnt.internal: "true"
  kntnt.binaries: "pdftotext uv"
  kntnt.skills: ""
  kntnt.externals: ""
  kntnt.capabilities: ""
---

# rename-invoices

Plan deterministic filenames for every text-based accounting PDF directly inside one folder, then apply the intact plan only when the Formal Invocation carries `--apply`.

**Dependencies.** Checker: `$HERE/../kntnt/scripts/kntnt.py` if that file exists, else `kntnt/scripts/kntnt.py` under a Global harness skills directory (`~/.claude/skills`, `~/.config/opencode/skills`, or wherever another Harness keeps them). Run `uv run "<checker>" check --here="$HERE"`. Exit 2: emit stdout and stop. If no checker is found, tell the user to install the Manager (`npx skills add Kntnt/skills`).

`$HERE` is the directory that contains this SKILL.md.

## Invocation Envelope

Before help routing or formal validation, read the `## INVOCATION ENVELOPE` section of `$HERE/help.md` and follow it. Pass only the Formal Invocation to scripts and nested formal parsers. Apply Help and Arguments below only to the Formal Invocation.

## Help

If the arguments are `--help`, `-h`, or `help`, print `$HERE/help.md` verbatim and stop.

## Arguments

`/rename-invoices --folder=<path> --type=<name> [--config=<path>|--no-config] [--locale=<name> ...] [--locale-file=<path> ...] [--prefix=<text>] [--template=<template>] [--date-format=<format>] [--description-template=<template>] [--extension=<extension>] [--identifier-template=<template>] [--date-source=<source> ...] [--counterparty-source=issuer|recipient] [--identifier-policy=always|collision|never] [--overrides=<path>] [--apply]`, and nothing else. Flags may appear in any order. `--folder` and the exact configured `--type` are required; obtain neither from Conversation Context, PDF contents, filenames, or earlier turns. Locale selection must come from repeated `--locale` flags or the selected configuration.

`--apply` is the only authorization to rename files. Without it, the run is a dry run regardless of Contextual Instruction or Conversation Context. Pass every supplied configuration and filename override unchanged to the planner. Read `$HERE/references/configuration.md` only for configuration work or a configuration error.

Anything outside the documented form is invalid. Name in one line what was wrong, print the `## SYNOPSIS` section of `$HERE/help.md` verbatim, and point at `/rename-invoices --help` for the page in full. Then rename nothing and stop. A flag is refused rather than ignored where it has no work to do here, because a flag accepted and ignored teaches that flags sometimes do nothing.

## Steps

1. Run the dependency checker, create a temporary working directory outside the target folder, and arrange to remove that directory before every later stop. Done when both dependencies are satisfied and the temporary directory exists.
2. Run `uv run "$HERE/scripts/rename_invoices.py" check` with the invocation's `--config` or `--no-config`, every `--locale`, and every `--locale-file`, preserving their order. Relay an exit-2 dependency, configuration, or locale error, remove the temporary directory, and stop. Poppler `pdftotext` is the sole PDF extractor; use no fallback library or OCR tool. Done when the command exits 0.
3. Run `uv run "$HERE/scripts/rename_invoices.py" plan --folder="$FOLDER" --type="$DOCUMENT_TYPE" --output="$WORK_DIR/plan.json"` with every applicable formal configuration, locale, filename, and overrides flag inserted before `--output`. Inspect the summary and every item that is not `already_correct`. Done when every direct PDF child is accounted for in the fresh plan.
4. For each `needs_review` item, read `$HERE/references/manual-review.md`, extract that PDF's text with `pdftotext`, and resolve only fields listed in `issues`. Put those decisions in a separate overrides JSON file, combining them with any supplied overrides without changing a supplied decision, then create a fresh plan with `--overrides=<path>`. A directly edited plan is invalid. Repeat only while new PDF evidence resolves a listed issue; leave unsupported facts unresolved. Done when the fresh plan has no reviewable issue left or every remaining issue is explicitly unresolved.
5. Without `--apply`, report the summary, proposed old-to-new mappings, verified `already_correct` files, and unresolved files; remove the temporary directory and stop. Done when the dry-run result accounts for every target PDF and no filename changed.
6. With `--apply`, require a fresh plan whose `needs_review` count is zero, then run `uv run "$HERE/scripts/rename_invoices.py" apply --output="$WORK_DIR/report.json" "$WORK_DIR/plan.json"`. Report applied mappings from the plan, verified `already_correct` files, unresolved files, and result counts, then remove the temporary directory. Done when every target PDF is accounted for as renamed, already correct, or explicitly unresolved.
