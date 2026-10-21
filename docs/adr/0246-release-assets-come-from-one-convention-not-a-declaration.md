# Release assets come from one convention, not a declaration

Recorded on 2026-10-21. `/release` is used for WordPress plugins, Rust and
TypeScript code, web projects and text documents, and has to work for a Project
with no build at all.

## What forced the question

Releasing a WordPress plugin bumped only `CHANGELOG.md`, because the engine did
not know the plugin header, and attached no archive, because the plugin's
`build-release-zip.sh` was not among the names the engine guessed at
(`scripts/build-zip.sh`, `make zip`, `npm run zip` and a few more). Eight plugin
repositories carried their own copy of that script, drifted into three
incompatible generations, seven of them also able to upload to GitHub on their
own. Five repositories described their version locations and build in a prose
`## Release configuration` block that an earlier release Skill had written and
the present engine never read.

## The alternatives

**A declaration file per Project**, naming each version location as a file and
a pattern and the build command, read by the engine. It handles any layout,
including a version repeated in several places. It also makes every Project
carry a file whose only reader is this Skill, lets a Project keep several
version locations instead of removing the duplicates, and needs a name and a
place nobody agreed on.

**More guessing.** Teaching the engine each ecosystem's build tool never ends,
and a guess that runs the wrong command is worse than no build.

**One convention for the build, standard locations for the version.** Chosen.

## The choice

The version lives in the one place the Project's ecosystem prescribes, which
the engine reads: `package.json`, `composer.json`, `pyproject.toml`,
`Cargo.toml`, `.claude-plugin/plugin.json`, or a WordPress plugin header. A
Project whose ecosystem prescribes none but needs the version at run time keeps
a `VERSION` file. Any other Project is versioned by its tag and changelog
alone. A Project with the version in more than one place removes the
duplicates rather than declaring them.

A Project that ships files with its release has an executable
`bin/build-release-assets`, in any language, which writes the finished files to
`release-assets/`. The release empties that directory, runs the command and
attaches every file it leaves there. The command never publishes. Running it by
hand builds the same files.

`release-assets/` rather than `dist/` or `build/`, because the release empties
the directory and every common name already belongs to some tool: JavaScript
libraries and WordPress plugins commit `dist/`, WordPress block tooling commits
`build/`, Cargo owns `target/`. A directory the release empties has to belong
to the release alone. The engine still refuses to empty it when git tracks a
file there.

`bin/` because that is where a Kntnt repository keeps a command meant to be run
by hand: no extension, a shebang, executable. That is also what makes the
convention language-neutral, since the release only executes the file.

## What it costs

A Project with a version in several places, such as a plugin constant beside
the header, has to be changed before its release is right. A build that needs
arguments needs a wrapper. Every Project that attached an archive through the
old guesses has to adopt the new name; none of the Kntnt repositories did.
