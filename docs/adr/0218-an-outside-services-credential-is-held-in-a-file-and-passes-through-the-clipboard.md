# An outside service's credential is held in a file and passes through the clipboard

This record settles where a Skill keeps a credential an outside service issued, and how the value travels between the user and the Skill without being typed into a conversation. The rule as it now stands is written in [`docs/rules/skills.md`](../rules/skills.md) under the Collection Library, and the writer it names is `skills/kntnt/library/scripts/credentials.py`. This record argues the case (issue #406).

## What forced it

**Four Skills are about to act on outside services on the user's behalf.** ClouDNS, NodePing, Postmark and Hetzner Cloud each issue a credential, and each Skill needs one to do anything at all. Hetzner ships today and keeps its token in `hcloud`'s own store; the other three do not exist yet, and each would otherwise invent its own answer.

**A credential typed into a conversation is copied into every transcript store the machine keeps.** Every Harness on the maintainer's machine runs with no confirmation prompt, so the agent reads, writes and runs what it is asked to without a person approving each step. A Harness transcript is a file on disk that outlives its session. A token pasted into the chat therefore lands in that file, and in every sync, backup and export of the directory the file sits in, for as long as any of them lasts. Rotating the token afterwards is the only repair, and nothing tells the user that one is owed.

## The decision

**A credential is never in the conversation.** It passes between the user and the Skill through the clipboard: the user copies it from the service's console and a Skill's `setup` reads the clipboard into the file, or a Skill draws a fresh value, stores it, and puts it on the clipboard for the user to paste where the service asks for it. Neither direction puts the value in anything the agent reads.

**It is held in a file only its owner can read.** The Credential File is `<home>/.kntnt/<skill>/credentials.json`, a flat JSON object of strings whose keys the owning Skill names. Its directory is `0700` and the file `0600`, which is what `~/.ssh` uses, and every reader refuses a file whose mode admits group or world, as `ssh` refuses such a key. On Windows, where those modes mean nothing, the file's ACL is restricted to its owner with `icacls`, and a failure to restrict is a failure to write. The file is written to a temporary file beside it and moved into place, so no reader sees a partial file and a failure leaves the previous one standing.

**It is used by the Skill's engine, which never prints it.** An engine that makes the service call reads the file itself, and uses each value in the request and nowhere else: not in an argument to another process, a log line, an error, a report or a URL. The first three are what a process listing, a shell history and a transcript capture; the last two are what a user copies into a ticket.

**One writer, in the Library.** All four Skills need the same clipboard handling for the same file, so it lives once, in `library/scripts/credentials.py`, and each Skill's body calls it. Its `exec` subcommand covers the case of a tool that keeps its own store — `hcloud context create --token-from-env` — by putting the value in one environment variable of the child rather than on its command line.

## The alternatives

**The operating system's keyring.** It is the textbook answer, and it was rejected because it is one mechanism per platform: macOS Keychain, the Secret Service over D-Bus on Linux, the Credential Manager on Windows, each with its own tool, its own failure modes and its own behaviour on a machine with no desktop session. The collection serves all three. The Secret Service is absent on exactly the headless server a Skill like Hetzner's is often run from, so the keyring would still need a file as its fallback, and the collection would then have two stores to explain instead of one. A file with the permissions `~/.ssh` uses is what every one of those platforms and every user already understands.

**Environment variables alone.** They are what the services' own tools document, and they were rejected because they have to be set somewhere. That somewhere is a shell profile, a `.env` file or a Harness's own configuration — each a file with no permissions rule of its own, several of them committed to repositories by habit, and one of them read into every process the user starts. An environment variable is still how a value reaches a driven tool; the Credential File is what it is read from.

**The conversation.** It is the cheapest to build and costs the most: every paste is a copy of the credential in the transcript, kept for as long as the transcript is, and on a machine whose Harnesses run without confirmation there is no moment at which a person sees the copy being made. It was ruled out first, and the other two were weighed against the file only once it had been.

## The gates stated once

**A tool that already holds the credential under the same protection is not given a second copy.** Hetzner's `hcloud` keeps its token at `~/.config/hcloud/cli.toml`, mode `0600`. A Credential File beside it would be a second place to rotate and a second place to forget, so the rule admits a driven tool's own store where it already holds the credential that way.

**A `setup` refuses to overwrite a credential the Skill already holds unless `--yes` is given.** Rotation is the one operation that destroys a working credential, and the one a stray invocation reaches by accident.

**An engine refuses without `--yes` any call the service cannot undo** — one that deletes, and one that sends on the user's behalf. A Skill whose destructive operations run through a driven tool rather than an engine of its own states the same gate in its own execution boundaries.

**Both gates are written in the rule rather than in each Skill.** Every one of the four carries them, and three of the tickets building them had each written the `setup` gate out for itself; one gate stated in three places is three texts that can come to disagree, and a gate stated once cannot drift.

## What this leaves out

**The Windows ACL is specified and not verified.** Nothing in this repository runs on Windows, and the suite's continuous integration is Linux alone, so the `icacls` invocation is attempted as the rule states and a failure is a failed write, but whether it restricts what it should is a person's check on a Windows machine.

**The engines' reads are held ticket by ticket.** This record ships the rule and the writer. Each Skill that reads its Credential File is held to the read the rule states by its own tests, in the ticket that builds it.
