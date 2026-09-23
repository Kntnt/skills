# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
"""Hold an outside service's credential for a Skill, filled through the clipboard or stdin.

A Skill's credential lives in its Credential File,
`<home>/.kntnt/<skill>/credentials.json`: a flat JSON object of strings whose
keys the owning Skill names, readable by its owner alone. This script is the
one writer of that file and the way a value passes between the user and it —
through the clipboard, so a credential never stands in a conversation, and so
never in the transcript every Harness keeps of one (ADR-0218). A value one of
the Skill's own processes already holds, as a token it fetched from the
service, reaches the file over standard input instead, the one channel that
is neither the clipboard nor an argument every user can read through `ps`.

Four subcommands, each exiting 0 on success and 2 on a refusal it can name,
with the reason on stderr. None of them prompts, none reaches the network, and
nothing any of them prints is ever a value the file holds:

- `set` reads the clipboard (`--from-clipboard`) or standard input
  (`--from-stdin`) into one key and merges `--set=<key>=<value>` pairs over
  what the file already holds.
- `generate` draws a fresh value into one key and puts it on the clipboard.
- `show` names the keys the file holds and its mode.
- `exec` runs a command with one value in one environment variable of the
  child, which is how a value reaches a tool that keeps its own store.

`set` and `generate` are the overwrite gate every Skill's `setup` passes
through, so no Skill states one of its own. Without `--yes`, each refuses where
the file already holds a non-empty value under `--key` or under a key a
`--set` pair names: a key written beside the one filled is as much a working
credential as that one, and replacing either is a rotation. The refusal comes
before the clipboard or stdin is read, before the clipboard is written, and
before the file is, and names the file, the keys held, and what `--yes`
asserts: that the user means to replace a working credential, which the
service goes on expecting until the new value is pasted or regenerated there.
A key the file does not hold, or holds empty, is nothing to overwrite, and a
file that does not exist holds none.

An engine that makes a service call reads the file itself rather than through
this script; `docs/rules/skills.md` states how.
"""

from __future__ import annotations

import argparse
import getpass
import json
import os
import re
import secrets
import shutil
import stat
import subprocess
import sys
import tempfile
from collections.abc import Sequence
from pathlib import Path
from typing import Final

# The exit status of every refusal this script can name.
REFUSED: Final = 2

# How many random bytes a generated value is drawn over. `token_urlsafe` spells
# 32 bytes in 43 characters.
GENERATED_BYTES: Final = 32

# The mode a Credential File is written with, the mode its directory is
# created with, and the bits no reader accepts: any access for group or world.
FILE_MODE: Final = 0o600
DIRECTORY_MODE: Final = 0o700
LOOSE_BITS: Final = 0o077

# What a Skill's name looks like in this collection. It becomes a directory
# name under `~/.kntnt`, so nothing that could climb out of it is accepted.
SKILL_NAME: Final = re.compile(r"^[a-z0-9][a-z0-9-]*$")

# The clipboard tools, per platform family, in the order they are tried. Each
# is a command line whose first word is looked up on the `PATH`; the first one
# found is the one used. Linux has no single clipboard, so Wayland's tools come
# first and the two X11 ones after.
READERS: Final[dict[str, tuple[tuple[str, ...], ...]]] = {
    "darwin": (("pbpaste",),),
    "linux": (
        ("wl-paste",),
        ("xclip", "-selection", "clipboard", "-o"),
        ("xsel", "--clipboard", "--output"),
    ),
    "win32": (("powershell", "-command", "Get-Clipboard"),),
}
WRITERS: Final[dict[str, tuple[tuple[str, ...], ...]]] = {
    "darwin": (("pbcopy",),),
    "linux": (
        ("wl-copy",),
        ("xclip", "-selection", "clipboard"),
        ("xsel", "--clipboard", "--input"),
    ),
    "win32": (("clip",),),
}


class Refusal(Exception):
    """A refusal this script can name, carrying the reason it prints."""


def platform_family() -> str:
    """The key into `READERS` and `WRITERS` for the platform this runs on.

    Anything that is neither macOS nor Windows is treated as Linux, which is
    what every other POSIX desktop this collection meets offers the same
    clipboard tools as.
    """

    if sys.platform == "darwin":
        return "darwin"
    if sys.platform == "win32":
        return "win32"
    return "linux"


def home() -> Path:
    """The home `~/.kntnt` is under, resolved exactly as the shim resolves it.

    Raises:
        Refusal: where there is no home to resolve and `KNTNT_HOME` is unset.
    """

    try:
        return Path(os.environ.get("KNTNT_HOME", str(Path.home())))
    except RuntimeError as error:
        raise Refusal(
            f"no home directory could be resolved ({error}); set KNTNT_HOME to"
            " the directory `.kntnt` should be under"
        ) from error


def credential_file(root: Path, skill: str) -> Path:
    """The Credential File of *skill* under *root*."""

    return root / ".kntnt" / skill / "credentials.json"


def by_hand(path: Path) -> str:
    """The recovery a machine without a clipboard has, naming the file."""

    return (
        f"A person may write the Credential File {path} by hand instead: a flat"
        ' JSON object of strings, such as {"token": "..."}, in a directory'
        " only its owner can enter, readable by its owner alone (chmod 600)."
    )


def loose_mode(path: Path) -> str:
    """Why a file whose mode admits group or world is refused."""

    mode = stat.S_IMODE(path.stat().st_mode)
    return (
        f"{path} has mode {mode:04o}, which admits group or world; a Credential"
        f" File needs mode {FILE_MODE:04o} (chmod 600 {path}), or remove it"
    )


def read_credentials(path: Path) -> dict[str, str]:
    """Read a Credential File, refusing one that others may read.

    Raises:
        Refusal: where the file is missing, admits group or world, or is not
            a flat JSON object of strings.
    """

    # Refuse a file others can read, as `ssh` refuses such a key. Mode bits
    # mean nothing on Windows, where the file's ACL carries the restriction.
    if not path.exists():
        raise Refusal(f"there is no Credential File at {path}")
    if os.name == "posix" and stat.S_IMODE(path.stat().st_mode) & LOOSE_BITS:
        raise Refusal(loose_mode(path))

    # Accept only the shape the rule gives the file, since a person may have
    # written it by hand.
    try:
        content = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
        raise Refusal(f"{path} could not be read as JSON ({error})") from error
    if not isinstance(content, dict) or not all(
        isinstance(key, str) and isinstance(value, str)
        for key, value in content.items()
    ):
        raise Refusal(f"{path} is not a flat JSON object of strings")
    return content


def restrict_to_owner(path: Path) -> None:
    """Restrict *path* to the current user alone, by the platform's own means.

    On POSIX the temporary file is already created at `0600`, so this is
    Windows' half: inheritance removed and full control to this user and
    nobody else. A failure to restrict is a failure to write.
    """

    if os.name != "nt":
        return
    result = subprocess.run(
        ["icacls", str(path), "/inheritance:r", "/grant:r", f"{getpass.getuser()}:F"],
        cwd=path.parent,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        raise OSError(f"icacls could not restrict {path}: {result.stderr.strip()}")


def write_credentials(path: Path, content: dict[str, str]) -> None:
    """Write *content* to *path* whole, or leave what stood there untouched.

    The value is written to a temporary file beside the destination and then
    moved over it, so no reader ever sees a partial file and a failure at any
    point leaves the previous file byte-identical.

    Raises:
        Refusal: where the directory or the file could not be written.
    """

    # Create the Skill's directory for its owner alone. An existing one is
    # left as it is: the file's own mode is what every reader checks.
    directory = path.parent
    try:
        if not directory.exists():
            directory.mkdir(parents=True, mode=DIRECTORY_MODE)
            directory.chmod(DIRECTORY_MODE)
    except OSError as error:
        raise Refusal(f"could not create {directory} ({error})") from error

    # Write beside the destination, then move into place. `mkstemp` creates
    # the file at 0600, so it is never readable by anyone else for a moment.
    try:
        descriptor, temporary = tempfile.mkstemp(
            dir=directory, prefix=".credentials-", suffix=".tmp"
        )
    except OSError as error:
        raise Refusal(f"could not write in {directory} ({error})") from error
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            json.dump(dict(sorted(content.items())), handle, indent=2)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        restrict_to_owner(Path(temporary))
        os.replace(temporary, path)
    except OSError as error:
        Path(temporary).unlink(missing_ok=True)
        raise Refusal(f"could not write {path} ({error})") from error


def clipboard_tool(table: dict[str, tuple[tuple[str, ...], ...]]) -> list[str] | None:
    """The first of this platform's clipboard commands found on the `PATH`."""

    for command in table[platform_family()]:
        if shutil.which(command[0]) is not None:
            return list(command)
    return None


def read_stdin(recovery: str) -> str:
    """Standard input's text with one trailing newline stripped.

    Raises:
        Refusal: where standard input holds nothing but whitespace, naming
            *recovery*, as an empty clipboard is refused.
    """

    value = sys.stdin.read().removesuffix("\n")
    if not value.strip():
        raise Refusal(f"standard input holds no text. {recovery}")
    return value


def read_clipboard(root: Path, recovery: str) -> str:
    """The clipboard's text with surrounding whitespace removed.

    Raises:
        Refusal: where no tool can read the clipboard, the tool fails, or the
            clipboard holds nothing but whitespace, each naming *recovery*.
    """

    command = clipboard_tool(READERS)
    if command is None:
        raise Refusal(f"no clipboard tool was found on the PATH. {recovery}")
    result = subprocess.run(
        command, cwd=root, capture_output=True, text=True, check=False
    )
    value = result.stdout.strip()
    if result.returncode != 0 or not value:
        raise Refusal(f"the clipboard holds no text. {recovery}")
    return value


def write_clipboard(root: Path, command: list[str], value: str) -> None:
    """Put *value* on the clipboard through *command*.

    Raises:
        Refusal: where the tool fails.
    """

    result = subprocess.run(
        command, cwd=root, input=value, capture_output=True, text=True, check=False
    )
    if result.returncode != 0:
        raise Refusal(
            f"{command[0]} could not write the clipboard"
            f" ({result.stderr.strip() or f'exit {result.returncode}'})"
        )


def pairs(
    given: Sequence[str], key: str, parser: argparse.ArgumentParser
) -> dict[str, str]:
    """The `--set=<key>=<value>` pairs, refusing one that names no key or *key*."""

    merged: dict[str, str] = {}
    for pair in given:
        name, separator, value = pair.partition("=")
        if not separator or not name:
            parser.error(f"--set={pair} is not in the form --set=<key>=<value>")
        if name == key:
            parser.error(f"--set={name}=... names the key --key={key} fills")
        merged[name] = value
    return merged


def report(path: Path, content: dict[str, str], key: str) -> None:
    """Say what was stored: the file, its keys, and the stored value's length."""

    print(
        json.dumps(
            {
                "path": str(path),
                "keys": sorted(content),
                "key": key,
                "length": len(content[key]),
            }
        )
    )


def refuse_overwrite(path: Path, keys: Sequence[str]) -> None:
    """Refuse to replace a value the file at *path* holds under any of *keys*.

    Rotation is the one operation that destroys a working credential, and the
    one a stray invocation reaches by accident, so only `--yes` passes it.

    Raises:
        Refusal: where the file holds a non-empty value under one of *keys*,
            or cannot be read.
    """

    content = read_credentials(path) if path.exists() else {}
    held = [key for key in dict.fromkeys(keys) if content.get(key)]
    if held:
        raise Refusal(
            f"{path} already holds {', '.join(held)}, and nothing was written."
            " Pass --yes to assert that you mean to replace a working credential;"
            " the service goes on expecting the old value until the new one is"
            " pasted or regenerated there"
        )


def store(
    root: Path, skill: str, key: str, value: str, extra: dict[str, str]
) -> dict[str, str]:
    """Merge *value* under *key* and *extra* over the file, and write it."""

    path = credential_file(root, skill)
    content = read_credentials(path) if path.exists() else {}
    content |= extra
    content[key] = value
    write_credentials(path, content)
    return content


def command_set(root: Path, args: argparse.Namespace, extra: dict[str, str]) -> int:
    """Read the clipboard or stdin into `--key`, merge the pairs, and write the file.

    Without `--yes`, a held key is refused before the clipboard or stdin is read.
    """

    path = credential_file(root, args.skill)
    if not args.yes:
        refuse_overwrite(path, [args.key, *extra])
    if args.from_stdin:
        value = read_stdin(by_hand(path))
    else:
        value = read_clipboard(root, by_hand(path))
    report(path, store(root, args.skill, args.key, value, extra), args.key)
    return 0


def command_generate(
    root: Path, args: argparse.Namespace, extra: dict[str, str]
) -> int:
    """Draw a value into `--key`, write the file, and put the value on the clipboard.

    The file is written before the clipboard is, so the user is never handed a
    value that was not stored; and a held key without `--yes`, and a machine
    with no clipboard tool, are each refused before anything is written at all.
    """

    path = credential_file(root, args.skill)
    if not args.yes:
        refuse_overwrite(path, [args.key, *extra])
    command = clipboard_tool(WRITERS)
    if command is None:
        raise Refusal(f"no clipboard tool was found on the PATH. {by_hand(path)}")
    value = secrets.token_urlsafe(GENERATED_BYTES)
    content = store(root, args.skill, args.key, value, extra)
    try:
        write_clipboard(root, command, value)
    except Refusal as error:
        raise Refusal(
            f"{error}; {path} now holds a {args.key} the clipboard never received,"
            " so run generate again"
        ) from error
    report(path, content, args.key)
    return 0


def command_show(root: Path, args: argparse.Namespace) -> int:
    """Name the keys the file holds and its mode, never a value."""

    path = credential_file(root, args.skill)
    content = read_credentials(path)
    mode = stat.S_IMODE(path.stat().st_mode)
    print(
        json.dumps({"path": str(path), "mode": f"{mode:04o}", "keys": sorted(content)})
    )
    return 0


def command_exec(root: Path, args: argparse.Namespace, command: list[str]) -> int:
    """Run *command* with the value in one variable of its environment.

    The value never stands in an argument, so it never shows in a process
    listing or a shell's history, and the child's exit status is this
    script's.
    """

    # Take the value from the clipboard or from the Skill's file.
    if args.from_clipboard:
        value = read_clipboard(
            root,
            "Write the value into a Skill's Credential File by hand and pass"
            " --skill=<name> --key=<key> instead; "
            + by_hand(credential_file(root, "<skill>")),
        )
    else:
        path = credential_file(root, args.skill)
        content = read_credentials(path)
        if args.key not in content:
            raise Refusal(f"{path} holds no key {args.key}")
        value = content[args.key]

    try:
        # Run the caller's command in the caller's own working directory,
        # which is where the person or engine asking for it meant it to run.
        result = subprocess.run(
            command, env=os.environ | {args.env: value}, check=False
        )
    except OSError as error:
        raise Refusal(
            f"{command[0]} could not be started ({error.strerror})"
        ) from error
    return result.returncode


# Each subcommand's usage, written out because `argparse` would print a valued
# flag with its value separated, and this collection's grammar attaches it
# (ADR-0176).
USAGES: Final = {
    "set": (
        "[--yes] --skill=<name> --key=<key> (--from-clipboard | --from-stdin)"
        " [--set=<key>=<value>]..."
    ),
    "generate": "[--yes] --skill=<name> --key=<key> --to-clipboard [--set=<key>=<value>]...",
    "show": "--skill=<name>",
    "exec": "--env=<VAR> (--from-clipboard | --skill=<name> --key=<key>) -- <command>...",
}


def parser() -> tuple[argparse.ArgumentParser, dict[str, argparse.ArgumentParser]]:
    """The command line and each subcommand's own parser.

    A usage error exits 2 with the usage line of the parser it belongs to.
    """

    root = argparse.ArgumentParser(
        prog="credentials.py",
        usage="\n".join(f"%(prog)s {name} {usage}" for name, usage in USAGES.items()),
        description="Hold an outside service's credential for a Skill.",
    )
    commands = root.add_subparsers(dest="command", required=True)
    subcommands = {
        name: commands.add_parser(
            name, prog=f"credentials.py {name}", usage=f"%(prog)s {usage}"
        )
        for name, usage in USAGES.items()
    }

    set_command = subcommands["set"]
    set_command.add_argument("--yes", action="store_true")
    set_command.add_argument("--skill", required=True)
    set_command.add_argument("--key", required=True)
    set_source = set_command.add_mutually_exclusive_group(required=True)
    set_source.add_argument("--from-clipboard", action="store_true")
    set_source.add_argument("--from-stdin", action="store_true")
    set_command.add_argument("--set", action="append", default=[])

    generate = subcommands["generate"]
    generate.add_argument("--yes", action="store_true")
    generate.add_argument("--skill", required=True)
    generate.add_argument("--key", required=True)
    generate.add_argument("--to-clipboard", action="store_true", required=True)
    generate.add_argument("--set", action="append", default=[])

    subcommands["show"].add_argument("--skill", required=True)

    run = subcommands["exec"]
    run.add_argument("--env", required=True)
    source = run.add_mutually_exclusive_group(required=True)
    source.add_argument("--from-clipboard", action="store_true")
    source.add_argument("--skill")
    run.add_argument("--key")

    return root, subcommands


def main(argv: Sequence[str] | None = None) -> int:
    """Parse *argv*, run the subcommand, and return its exit status."""

    # Split the child's command line off before parsing, so none of its own
    # flags is read as one of this script's.
    arguments = list(sys.argv[1:] if argv is None else argv)
    separator = "--" in arguments
    ours = arguments[: arguments.index("--")] if separator else arguments
    theirs = arguments[len(ours) + 1 :]
    root_parser, subcommands = parser()
    args = root_parser.parse_args(ours)
    command_parser = subcommands[args.command]

    # Hold each subcommand to the combinations its usage states.
    if args.command == "exec":
        if not separator or not theirs:
            command_parser.error("exec needs -- and the command to run after it")
        if args.skill is not None and args.key is None:
            command_parser.error("exec --skill needs --key")
        if args.from_clipboard and args.key is not None:
            command_parser.error("exec --from-clipboard takes no --key")
    elif separator:
        command_parser.error(f"{args.command} takes no command after --")
    skill = getattr(args, "skill", None)
    if skill is not None and not SKILL_NAME.match(skill):
        command_parser.error(f"--skill={skill} is not a Skill name")

    # Run it, turning every refusal into its reason on stderr and exit 2.
    try:
        root = home()
        match args.command:
            case "set":
                return command_set(
                    root, args, pairs(args.set, args.key, command_parser)
                )
            case "generate":
                return command_generate(
                    root, args, pairs(args.set, args.key, command_parser)
                )
            case "show":
                return command_show(root, args)
            case _:
                return command_exec(root, args, theirs)
    except Refusal as refusal:
        print(f"credentials.py: {refusal}", file=sys.stderr)
        return REFUSED


if __name__ == "__main__":
    sys.exit(main())
