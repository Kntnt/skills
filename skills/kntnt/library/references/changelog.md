# Reconcile `[Unreleased]`

Bring `CHANGELOG.md` in line with what actually changed since the last release. Edit only `[Unreleased]`. Do not bump, promote, commit, tag, or push.

## Steps

1. If `CHANGELOG.md` is missing, create Keep a Changelog + SemVer boilerplate with an empty `## [Unreleased]`. If the file exists but has no `## [Unreleased]`, add an empty one under the intro. Done when that heading exists.
2. Baseline: the plan's `last_tag`, or the whole history when it is null. Done when the look-back point is known.
3. Read the plan's `commits` first. Open a diff only when a subject is too thin to write a clear entry. Include the working tree (`git status`, `git diff HEAD`). Done when the real changes are known.
4. Write Keep a Changelog sections that have content, in this order: `Added` · `Changed` · `Deprecated` · `Removed` · `Fixed` · `Security`. One user-facing bullet per change, in the file's existing language and voice. Never a git-log dump. Done when every real change has a bullet or is already recorded anywhere in the file.
5. Merge into `[Unreleased]` without duplicating a change that is already in `[Unreleased]` or in any dated version section. A second run — including after a release bump that just promoted the section — must add nothing. An empty section afterwards is fine here — report it; do not invent entries. Done when the file is saved.
